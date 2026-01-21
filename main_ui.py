import sys
from datetime import datetime
from pathlib import Path
from time import sleep

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from libs.Utils import copy_data
from libs.check_self_diagnostic_log import CheckSelfDiagnostic
from libs.check_time import CheckTime
from libs.config import Config
from libs.connect import connect_with_ip
from libs.read import meter_survey
from libs.sending_message import message_in_out
from libs.test_get_info_from_rsm import get_serial_numbers, get_ip
from libs.worker import EmittingStream, WorkerThread


class UiForLogLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_ip_with_port = {}
        self.time_for_check_self_diagnostic_1 = None
        self.time_for_check_1 = None
        self.timer_2 = None
        self.timer_1 = None
        self.list_of_serial = []
        self.ip = None
        self.second_date = None
        self.first_date = None
        self.flag_viborka = False
        self.flag_temperature = False
        self.serial_number = None
        self.baud_rate = None
        self.settings = None
        self.reader = None
        self.initUI()
        self.object_connect = None
        self.meter_thread = None
        self.read_log_thread = None
        self.analysis_thread = None
        self.file_name = None
        self.file_names = []

    def initUI(self):
        current_dir = Path(__file__).parent
        ui_path = current_dir / "libs" / "maket_mass.ui"

        if not ui_path.exists():
            print(f"UI-файл не найден: {ui_path}")
            raise FileNotFoundError(f"UI-файл не найден: {ui_path}")

        uic.loadUi(str(ui_path), self)

        # self.serial = self.findChild(QtWidgets.QLineEdit, 'serial')
        #
        # self.com = self.findChild(QtWidgets.QLineEdit, 'com')
        # self.com.setValidator(QIntValidator())
        # self.com.setMaxLength(2)

        self.read = self.findChild(QtWidgets.QPushButton, 'read')

        self.text_edit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        # self.text_edit.setFixedSize(880, 450),

        self.stream = EmittingStream()
        sys.stdout = self.stream
        sys.stderr = self.stream
        self.stream.textWritten.connect(self.on_text_written)

        # Применение темной темы
        self.applyDarkTheme()

        # # Загрузка серийных номеров
        # self.load_serial_numbers()

        self.read.clicked.connect(self.start_read_meter_data)
        # self.read.clicked.connect(self.start_read_log_thread)

    # def load_serial_numbers(self):
    #     try:
    #         self.list_of_serial = get_serial_numbers()
    #         print(f"Загружено {len(self.list_of_serial)} серийных номеров")
    #     except Exception as e:
    #         print(f"Не удалось получить серийные номера: {e}")
    #         self.list_of_serial = []

    def load_ip_with_port(self) -> dict:
        try:
            self.list_of_ip_with_port = get_ip()
            print(f"\nЗагружено {len(self.list_of_ip_with_port)} ip адресов")
        except Exception as e:
            print(f"Не удалось получить ip адреса: {e}")
            message_in_out(f"Не удалось получить ip адреса: {e}")
            raise

    def get_params(self):
        try:
            # com = self.com.text().strip()
            # if not com or not com.isdigit():
            #     raise ValueError("Поле COM должно быть непустым числом")

            config = Config(None, None, '1234567898765432', self.flag_temperature,
                            self.flag_viborka, self.first_date, self.second_date)
            return config
        except Exception as e:
            print(f"Ошибка при получении параметров: {e}")
            raise

    def read_meter_data_task(self, time_for_check, time_for_check_self_diagnostic):
        # self.load_serial_numbers()
        try:
            self.load_ip_with_port()
        except Exception as e:
            return

        config = self.get_params()
        current_time = datetime.now()
        file_name = f"Логи_опроса_IP_{current_time.strftime('%d.%m.%Y_%H.%M.%S')}.txt"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("")

        all_successful = True
        error_messages = []

        for serial in self.list_of_ip_with_port.keys():
            print('#########################################################')
            print(f"Опрос счётчика №[...{serial}]")
            config.serial_number = serial
            config.ip = self.list_of_ip_with_port[serial].split(':')[0]
            config.port = self.list_of_ip_with_port[serial].split(':')[1]
            try:
                meter_survey(config, time_for_check, time_for_check_self_diagnostic, file_name)
                print(f"Опрос счётчика №[...{serial}] завершён")
                # message_in_out(f"Опрос счётчика №[...{serial}] успешно")
            except Exception as e:
                error_msg = f"Ошибка при опросе счётчика №...{serial}: {e}"
                print(error_msg)
                error_messages.append(error_msg)
                all_successful = False

        if all_successful and self.list_of_ip_with_port:
            message_in_out(f"#Опрос_IP\n"
                           f"С RSM загружено {len(self.list_of_ip_with_port)} ip адреса.\n"
                           f"Опрос счетчиков - успешно.\n"
                           f"Время выполнения - {current_time.strftime('%d.%m.%Y_%H.%M.%S')}")
        else:
            full_error_message = "\n\n".join(error_messages)
            message_in_out(
                f"#Опрос_IP\n"
                f"С RSM загружено {len(self.list_of_ip_with_port)} ip адреса.\n"
                f"Опрос счётчиков завершён с ошибками!!!\n"
                f"_____________________________________________________________\n"
                f"{full_error_message}\n"
                f"_____________________________________________________________\n"
                f"Время выполнения — {current_time.strftime('%d.%m.%Y_%H.%M.%S')}"
            )
        copy_data(file_name)

    def start_read_meter_data(self):
        self.read.setEnabled(False)
        print("Программа запущена...")
        self.time_for_check_1 = CheckTime(self.list_of_serial)
        self.time_for_check_self_diagnostic_1 = CheckSelfDiagnostic(self.list_of_serial)

        if self.timer_2 is None:
            self.timer_2 = QTimer()
            self.timer_2.timeout.connect(self.check_and_run_meter_task)
            self.timer_2.start(60000)  # Проверка каждые 60 секунд

        # Запуск сразу, если условие выполняется
        self.check_and_run_meter_task()

    def check_and_run_meter_task(self):
        current_time = datetime.now()
        if current_time.minute == 0 or current_time.minute == 30 and not self.is_meter_thread_running():
            self.run_meter_task()

    def is_meter_thread_running(self):
        return self.meter_thread is not None and self.meter_thread.isRunning()

    def run_meter_task(self):
        self.meter_thread = WorkerThread(
            self,
            self.read_meter_data_task,
            self.time_for_check_1,
            self.time_for_check_self_diagnostic_1
        )
        self.meter_thread.finished.connect(self.on_meter_thread_finished)
        self.meter_thread.error.connect(self.on_error)
        self.meter_thread.start()

    def on_meter_thread_finished(self, result):
        self.meter_thread = None
        self.check_threads_and_enable_button()

    # def on_log_thread_finished(self, result):
    #     self.read_log_thread = None
    #     self.check_threads_and_enable_button()

    def check_threads_and_enable_button(self):
        """Разблокирует кнопку, если все потоки завершены"""
        threads_running = [
            self.meter_thread and self.meter_thread.isRunning()
            # self.read_log_thread and self.read_log_thread.isRunning(),
            # self.analysis_thread and self.analysis_thread
            # and self.analysis_thread.isRunning()
        ]
        if not any(threads_running):
            self.read.setEnabled(True)

    def on_error(self, error_message):
        self.read.setEnabled(True)
        if self.meter_thread:
            self.meter_thread = None
        # if self.read_log_thread:
        #     self.read_log_thread = None
        # if self.analysis_thread:
        #     self.analysis_thread = None

        self.update_text(f"Произошла ошибка: {error_message}\n")

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

    def closeEvent(self, event):
        print("Закрытие приложения, остановка потоков...")

        # Останавливаем таймеры
        # if self.timer_1 and self.timer_1.isActive():
        #     self.timer_1.stop()
        if self.timer_2 and self.timer_2.isActive():
            self.timer_2.stop()

        # Завершаем все потоки
        threads_to_stop = [self.meter_thread]
        for thread in threads_to_stop:
            if thread and thread.isRunning():
                thread.quit()
                thread.wait(2000)  # Ждём до 2 секунд

        super().closeEvent(event)
        print("Приложение закрыто")


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
