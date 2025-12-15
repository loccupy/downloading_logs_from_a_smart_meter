import os
import re
import sys
import time
from copy import copy
from datetime import datetime
from time import sleep

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from libs.Utils import copy_data
from libs.check_self_diagnostic_log import CheckSelfDiagnostic
from libs.check_time import CheckTime
from libs.config import Config
from libs.connect import setting_the_speed_to_default_values, connect_with_ip
from libs.log_analysis_main import *
from libs.read import read_logs, meter_survey
from libs.sending_message import clear_global_list, global_list, message_in_out
from libs.test_get_info_from_rsm import get_serial_numbers


class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, parent=None, method=None, *args, **kwargs):
        super().__init__(parent)
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.method(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass  # Необходимо для совместимости с sys.stdout


class UiForLogLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.ip = None
        self.second_date = None
        self.first_date = None
        self.flag_viborka = None
        self.flag_temperatyre = None
        self.serial_number = None
        self.baud_rate = None
        self.com_port = None
        self.settings = None
        self.reader = None
        self.initUI()
        self.object_connect = None
        self.thread = None
        self.file_name = None
        self.file_names = []

    def initUI(self):
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, 'libs', 'maket_mass.ui')

        uic.loadUi(ui_path, self)

        # self.port = self.findChild(QtWidgets.QLineEdit, 'port')
        # self.port.setValidator(QIntValidator())
        # self.port.setMaxLength(5)

        self.serial = self.findChild(QtWidgets.QLineEdit, 'serial')
        # self.serial.setValidator(QIntValidator())
        # self.serial.setMaxLength(4)

        self.com = self.findChild(QtWidgets.QLineEdit, 'com')
        self.com.setValidator(QIntValidator())
        self.com.setMaxLength(2)

        # self.field_password = self.findChild(QtWidgets.QLineEdit, 'field_password')
        # self.field_password.setEnabled(False)
        # self.field_password.setMaxLength(16)

        # self.password = self.findChild(QtWidgets.QCheckBox, 'password')
        #
        # self.password.stateChanged.connect(self.update_password_field)

        # self.checkbox_temperature = self.findChild(QtWidgets.QCheckBox, 'temperature')
        # self.checkbox_viborka = self.findChild(QtWidgets.QCheckBox, 'viborka')

        # self.end_date = self.findChild(QtWidgets.QDateTimeEdit, 'end_date')
        # self.end_date.setEnabled(False)
        # self.start_date = self.findChild(QtWidgets.QDateTimeEdit, 'start_date')
        # self.start_date.setEnabled(False)

        # self.checkbox_viborka.stateChanged.connect(
        #     lambda state: self.toggle_fields(state, self.start_date, self.end_date)
        # )

        self.read = self.findChild(QtWidgets.QPushButton, 'read')
        # self.read.clicked.connect(self.read_log)

        # self.analisys = self.findChild(QtWidgets.QPushButton, 'analisys')
        # self.analisys.clicked.connect(self.analysis)

        self.text_edit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        # self.text_edit.setFixedSize(880, 450)
        self.redirect_stdout()
        self.stream.textWritten.connect(self.on_text_written)

        # Применение темной темы
        self.applyDarkTheme()

        self.read.clicked.connect(self.start_read_meter_data)
        self.read.clicked.connect(self.start_read_log_thread)
        # self.analisys.clicked.connect(self.start_analysis_thread)

    def get_params(self):
        try:
            self.com_meter = self.com.text()
            # self.port_number = str(self.port.text())
            # self.serial_number = int(serial)
            # self.passw = self.field_password.text()
            # if self.password.isChecked() is False:
            #     self.passw = '1234567898765432'
            # self.flag_temperatyre = self.checkbox_temperature.isChecked()
            # self.flag_viborka = self.checkbox_viborka.isChecked()
            # self.first_date = self.start_date.text()
            # self.second_date = self.end_date.text()
            config = Config(self.com_meter, None, '1234567898765432', self.flag_temperatyre,
                            self.flag_viborka, self.first_date, self.second_date)
            return config
        except Exception as e:
            print(f"Ошибка при считывании данных из полей >> {e}")
            raise

    def get_list_of_serial_numbers(self):
        try:
            list_of_serial = [i.strip() for i in self.serial.text().split(',')]

            return list_of_serial
        except Exception as e:
            print(f"Не удалось идентифицировать введенные серийные номера с ошибкой {e}!!!")
            return []

    def get_list_of_serial_numbers_from_api(self):
        try:
            list_of_serial = get_serial_numbers()

            return list_of_serial
        except Exception as e:
            print(f"Не удалось получить серийные номера по api запросу с ошибкой {e}!!!")
            raise

    def read_meter_data_task(self):
        list_of_serial = self.get_list_of_serial_numbers_from_api()
        config = self.get_params()
        time_for_check = CheckTime(list_of_serial)
        time_for_check_self_diagnostic = CheckSelfDiagnostic(list_of_serial)

        while True:
            current_time = datetime.now()

            # Проверяем, если минуты кратны 50
            # if (current_time.minute / 10 == 1 or current_time.minute / 40 == 1) and current_time.minute != 0:
            if current_time.minute / 40 == 1:
                file_name = f"Логи_опроса_{current_time.strftime("%d.%m.%Y_%H.%M.%S")}.txt"
                # file_path = os.path.join(main_directory, file_name)
                with open(file_name, "w", encoding="utf-8"):
                    pass
                for serial in list_of_serial:
                    print(f'\n{current_time.strftime("%d-%m-%Y %H:%M:%S")} >>> #####   ОПРОС СЧЕТЧИКА №[...{serial}]  #####', end='')
                    config.serial_number = int(serial)
                    try:
                        meter_survey(config, time_for_check, time_for_check_self_diagnostic, file_name)
                        print(f'#####   ОПРОС СЧЕТЧИКА №[...{serial}] ЗАКОНЧЕН #####')
                    except Exception as e:
                        print(f"#####   ОШИБКА ПРИ ОПРОСЕ СЧЕТЧИКА №...{serial} >> ошибка {e}  #####\n")
                        continue
                copy_data(file_name)
            # Ждем 1 минуту
            time.sleep(60)

    def read_log(self):
        list_of_serial = self.get_list_of_serial_numbers_from_api()
        for_report = []
        # with open('report.txt', 'w', encoding='utf-8') as f:
        #     f.write('')
        config = self.get_params()
        while True:
            current_time = datetime.now()
            # Проверяем, если минуты кратны 56
            if current_time.minute / 45 == 1:
                tm = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

                main_directory = f'Выгрузка_журналов_{tm}'

                if not os.path.exists(main_directory):
                    os.makedirs(main_directory)

                file_name = f'report_{tm}.txt'
                file_path = os.path.join(main_directory, file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')

                for serial in list_of_serial:

                    print(f'{current_time.strftime("%d-%m-%Y %H:%M:%S")} >>> #####   ОБРАБОТКА ДАННЫХ ПУ №[...{serial}]  #####')
                    config.serial_number = int(serial)
                    try:
                        # speeding_up_the_connection(config)

                        result = read_logs(config, main_directory)

                        self.file_name = result

                        # setting_the_speed_to_default_values(config)

                        self.analysis()

                        with open(file_path, 'a', encoding='utf-8') as f:
                            formatted_list = '  \n'.join([''.join(f'{i + 1}) {data};') for i, data in enumerate(copy(global_list))])
                            f.write(f'\nДля файла >> {result[0]}:\n')
                            f.write(formatted_list + '\n')

                        clear_global_list()
                        print(f'\n#####   ОБРАБОТКА ДАННЫХ ПУ №[...{serial}] ЗАКОНЧЕНА  #####\t')
                    except Exception as e:
                        setting_the_speed_to_default_values(config)
                        print(f"#####   ОШИБКА ПРИ ОБРАБОТКЕ ДАННЫХ СЧЕТЧИКА №...{serial} >> ошибка {e}  #####\n")
                        continue
                # print(for_report)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                message_in_out(content)
                copy_data(main_directory)

            sleep(60)

    def analysis(self):
        print(f"\n  СТАРТ АНАЛИЗА ЖУРНАЛОВ...")
        try:
            old_file_name = self.file_name[0]
            device_type = self.file_name[1]
            file_name = old_file_name.replace('.xlsx', '_анализ.xlsx')

            sheets = load_workbook(old_file_name)
            sheets.save(file_name)

            current_log_analysis(file_name)
            self_diagnosis_log_analysis(file_name)
            network_quality_log_analysis(file_name)
            voltage_log_analysis(file_name)
            communication_events_log_analysis(file_name)
            access_control_log_analysis(file_name)
            data_correction_log_analysis(file_name)
            time_correction_log_analysis(file_name)
            battery_charge_status_log_analysis(file_name)
            power_log_analysis(file_name)
            tangent_excess_log_analysis(file_name)
            tangent_output_log_analysis(file_name)
            network_quality_for_period_log_analysis(file_name)
            on_and_off_log_analysis(file_name)
            external_influences_log_analysis(file_name)
            if 'TT' == device_type:
                sampling_status_log_analysis(file_name)
            daily_profile_log_analysis(file_name)
            month_profile_log_analysis(file_name)
            energy_profile_for_1_log_analysis(file_name)
            energy_profile_for_2_log_analysis(file_name)
            artur_profile_log_analysis(file_name)

            print(f"  АНАЛИЗ ЖУРНАЛОВ ЗАВЕРШЕН")
        except Exception as e:
            print(f"Ошибка при анализе {e}")

    def start_read_log_thread(self):
        try:
            if not self.com.text().strip():
                raise ValueError("Поле COM не может быть пустым")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка ввода", f"Ошибка в заполнении формы: {e}")
            return

        # Проверяем, запущен ли уже поток выгрузки
        if hasattr(self, 'log_thread') and self.log_thread and self.log_thread.isRunning():
            return

        self.read.setEnabled(False)
        self.log_thread = WorkerThread(self, self.read_log)
        self.log_thread.finished.connect(self.on_log_thread_finished)
        self.log_thread.error.connect(self.on_error)
        self.log_thread.start()

    def start_analysis_thread(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.ReadOnly
        #
        # filename, _ = QFileDialog.getOpenFileName(
        #     self,
        #     "Выберите файл",
        #     "",
        #     "Файлы Excel (*.xlsx)",
        #     options=options
        # )
        # if filename:
        #     self.file_name = filename
        # if self.thread and self.thread.isRunning():
        #     return

        self.analisys.setEnabled(False)
        self.read.setEnabled(False)
        self.thread = WorkerThread(self, self.analysis)
        self.thread.finished.connect(self.on_analysis_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def start_read_meter_data(self):
        try:
            if not self.com.text().strip():
                raise ValueError("Поле COM не может быть пустым")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка ввода", f"Ошибка в заполнении формы: {e}")
            return

        # Проверяем, запущен ли уже поток опроса
        if hasattr(self, 'meter_thread') and self.meter_thread and self.meter_thread.isRunning():
            return

        self.read.setEnabled(False)
        self.meter_thread = WorkerThread(self, self.read_meter_data_task)
        self.meter_thread.finished.connect(self.on_meter_thread_finished)
        self.meter_thread.error.connect(self.on_error)
        self.meter_thread.start()

    def on_meter_thread_finished(self, result):
        self.meter_thread = None
        self.check_threads_and_enable_button()

    def on_log_thread_finished(self, result):
        self.log_thread = None
        self.check_threads_and_enable_button()

    def check_threads_and_enable_button(self):
        """Разблокирует кнопку, если оба потока завершены"""
        if (not hasattr(self, 'meter_thread') or self.meter_thread is None or not self.meter_thread.isRunning()) and \
                (not hasattr(self, 'log_thread') or self.log_thread is None or not self.log_thread.isRunning()):
            self.read.setEnabled(True)

    def on_analysis_finished(self, result):
        self.analisys.setEnabled(True)
        self.read.setEnabled(True)
        self.thread = None

    def on_error(self, error_message):
        self.read.setEnabled(True)
        self.analisys.setEnabled(True)
        self.thread = None
        self.update_text(f"Произошла ошибка: {error_message}\n")

    def update_password_field(self, state):
        self.field_password.setEnabled(state == Qt.Checked)
        if not state:  # Если чекбокс отключен, очищаем поле
            self.field_password.clear()

    def toggle_fields(self, state, start_date, end_date):
        is_checked = (state == Qt.Checked)
        start_date.setEnabled(is_checked)
        end_date.setEnabled(is_checked)

    def update_text(self, text):
        self.text_edit.append(text)

    def redirect_stdout(self):
        self.stream = EmittingStream()
        sys.stdout = self.stream
        sys.stderr = self.stream

    def on_text_written(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        QApplication.processEvents()

    def applyDarkTheme(self):
        # Определяем стили для темной темы
        dark_stylesheet = """
        QWidget {
            background-color: #2c313c;
            color: #ffffff;
        }

        QLineEdit {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px;
        }

        QLineEdit:focus {
            border: 1px solid #61dafb;
        }

        QPushButton {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #444950;
        }

        QPushButton:pressed {
            background-color: #2c313c;
        }
        """

        # Применяем стиль к приложению
        self.setStyleSheet(dark_stylesheet)


def start_ui():
    app = QApplication(sys.argv)
    ex = UiForLogLoader()
    ex.show()
    sys.exit(app.exec_())


def debug():
    # file_name = "Serial_240101000000000_30.07.25_12.36.41.xlsx"
    # current_log_analysis(file_name)
    # self_diagnosis_log_analysis(file_name)
    # network_quality_log_analysis(file_name)
    # voltage_log_analysis(file_name)
    # communication_events_log_analysis(file_name)
    # access_control_log_analysis(file_name)
    # data_correction_log_analysis(file_name)
    # time_correction_log_analysis(file_name)
    # battery_charge_status_log_analysis(file_name)
    # power_log_analysis(file_name)
    # tangent_excess_log_analysis(file_name)
    # tangent_output_log_analysis(file_name)
    # network_quality_for_period_log_analysis(file_name)
    # on_and_off_log_analysis(file_name)
    # external_influences_log_analysis(file_name)
    # sampling_status_log_analysis(file_name)
    # sampling_status_log_analysis(file_name)
    # month_profile_log_analysis(file_name)
    # energy_profile_for_1_log_analysis(file_name)
    # energy_profile_for_2_log_analysis(file_name)
    # artur_profile_log_analysis(file_name)
    reader = connect_with_ip()
    print(reader.deviceType)
    reader.close()


if __name__ == "__main__":
    start_ui()
