import os
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog

from libs.connect import get_reader, speeding_up_the_connection, init_connect, \
    close_reader, setting_the_speed_to_default_values
from libs.log_analysis_main import *
from libs.read import read_logs


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

    def initUI(self):
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, 'libs', 'maket.ui')

        uic.loadUi(ui_path, self)

        self.baud = self.findChild(QtWidgets.QLineEdit, 'speed')
        self.baud.setValidator(QIntValidator())
        self.baud.setMaxLength(6)

        self.serial = self.findChild(QtWidgets.QLineEdit, 'serial')
        self.serial.setValidator(QIntValidator())
        self.serial.setMaxLength(4)

        self.com = self.findChild(QtWidgets.QLineEdit, 'com')
        self.com.setValidator(QIntValidator())
        self.com.setMaxLength(2)

        self.field_password = self.findChild(QtWidgets.QLineEdit, 'field_password')
        self.field_password.setEnabled(False)
        self.field_password.setMaxLength(16)

        self.password = self.findChild(QtWidgets.QCheckBox, 'password')

        self.password.stateChanged.connect(self.update_password_field)

        self.checkbox_temperature = self.findChild(QtWidgets.QCheckBox, 'temperature')
        self.checkbox_viborka = self.findChild(QtWidgets.QCheckBox, 'viborka')

        self.end_date = self.findChild(QtWidgets.QDateTimeEdit, 'end_date')
        self.end_date.setEnabled(False)
        self.start_date = self.findChild(QtWidgets.QDateTimeEdit, 'start_date')
        self.start_date.setEnabled(False)

        self.checkbox_viborka.stateChanged.connect(
            lambda state: self.toggle_fields(state, self.start_date, self.end_date)
        )

        self.read = self.findChild(QtWidgets.QPushButton, 'read')
        # self.read.clicked.connect(self.read_log)

        self.analisys = self.findChild(QtWidgets.QPushButton, 'analisys')
        # self.analisys.clicked.connect(self.analysis)

        self.text_edit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        # self.text_edit.setFixedSize(880, 450)
        self.redirect_stdout()
        self.stream.textWritten.connect(self.on_text_written)

        # Применение темной темы
        self.applyDarkTheme()

        self.read.clicked.connect(self.start_read_log_thread)
        self.analisys.clicked.connect(self.start_analysis_thread)

    def get_params(self):
        try:
            self.com_port = int(self.com.text())
            self.baud_rate = int(self.baud.text())
            self.serial_number = int(self.serial.text())
            self.passw = self.field_password.text()
            if self.password.isChecked() is False:
                self.passw = '1234567898765432'
            self.flag_temperatyre = self.checkbox_temperature.isChecked()
            self.flag_viborka = self.checkbox_viborka.isChecked()
            self.first_date = self.start_date.text()
            self.second_date = self.end_date.text()
        except Exception as e:
            print(f"Ошибка при считывании данных из полей >> {e}")
            raise

    def _speeding_up(self):
        try:
            self.get_params()

            self.reader, self.settings = get_reader(self.com_port, self.passw, self.serial_number, self.baud_rate)

            init_connect(self.reader, self.settings)
            new_baud = speeding_up_the_connection(self.reader)
            print('Переподключение с новой скоростью....')
            close_reader(self.reader)

            self.reader, self.settings = get_reader(self.com_port, self.passw, self.serial_number, new_baud)

            init_connect(self.reader, self.settings)
        except Exception as e:
            self.settings.media.close()
            raise

    def _speeding_down_and_close(self):
        try:
            # init_connect(self.reader, self.settings)
            setting_the_speed_to_default_values(self.reader)
            close_reader(self.reader)
        except Exception as e:
            self.settings.media.close()
            print(f"Ошибка при установке соединения на дефолтные 9600 >> {e}.")
            raise

    def read_log(self):
        try:
            self._speeding_up()

            result = read_logs(self.reader, self.flag_temperatyre, self.flag_viborka, self.first_date,
                               self.second_date)[1]

            self._speeding_down_and_close()

        except Exception as e:
            print(f"Ошибка при считывании журналов >> {e}")


    def check_device_type_from_filename(self, filename):
        if '1PH' in filename:
            return '1PH'
        elif '3PH' in filename:
            return '3PH'
        elif 'TT' in filename:
            return 'TT'
        else:
            print('Тип счетчика не распознан')
            raise Exception('Тип счетчика не распознан')


    def analysis(self):
        try:
            old_file_name = self.file_name
            device_type = self.check_device_type_from_filename(old_file_name)
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

            print("АНАЛИЗ ЖУРНАЛОВ ЗАВЕРШЕН")
        except Exception as e:
            print(f"Ошибка при анализе {e}")

    def start_read_log_thread(self):
        try:
            if not self.com.text().strip():
                raise ValueError("Поле COM-порта не может быть пустым")
            if not self.baud.text().strip():
                raise ValueError("Поле скорости соединения не может быть пустым")
            if not self.serial.text().strip():
                raise ValueError("Поле серийного номера не может быть пустым")
            if not self.field_password.text().strip() and self.password.isChecked() is True:
                raise ValueError("Поле пароля не может быть пустым")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Ошибка ввода",
                f"Ошибка в заполнении формы: {e}"
            )
            return
        if self.thread and self.thread.isRunning():
            return

        self.read.setEnabled(False)
        self.analisys.setEnabled(False)
        self.thread = WorkerThread(self, self.read_log)
        self.thread.finished.connect(self.on_read_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def start_analysis_thread(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Файлы Excel (*.xlsx)",
            options=options
        )
        if filename:
            self.file_name = filename
        if self.thread and self.thread.isRunning():
            return

        self.analisys.setEnabled(False)
        self.read.setEnabled(False)
        self.thread = WorkerThread(self, self.analysis)
        self.thread.finished.connect(self.on_analysis_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def on_read_finished(self, result):
        self.read.setEnabled(True)
        self.analisys.setEnabled(True)
        self.thread = None

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
    file_name = "Serial_240101000000000_30.07.25_12.36.41.xlsx"
    # current_log_analysis(file_name)
    # self_diagnosis_log_analysis(file_name)
    # network_quality_log_analysis(file_name)
    # voltage_log_analysis(file_name)
    # communication_events_log_analysis(file_name)
    # access_control_log_analysis(file_name)
    data_correction_log_analysis(file_name)
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


if __name__ == "__main__":
    start_ui()
