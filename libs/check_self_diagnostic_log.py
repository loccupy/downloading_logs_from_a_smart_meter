from datetime import datetime

from libs.Utils import write_txt
from libs.gurux.dlms.objects import GXDLMSProfileGeneric, GXDLMSClock
from libs.sending_message import message_in_out


def check_error_code_in_self_diagnostic_log(config, reader, time_for_check_self_diagnostic, file_name):
    try:
        print("Начал опрос Журнала самодиагностики...")

        key = config.serial_number
        current_time = datetime.strptime(str(reader.read(GXDLMSClock('0.0.1.0.0.255'), 2)), "%m/%d/%y %H:%M:%S")

        if time_for_check_self_diagnostic.get_start_time(key) is None:
            time_for_check_self_diagnostic.set_start_time(key, current_time)
            write_txt(file_name, f"\nСтарт отчетного периода для журнала самодиагностики!!!\n")
            print(f"Старт отчетного периода для журнала самодиагностики!!!")
            return
        else:
            time_for_check_self_diagnostic.set_end_time(key, current_time)

            data = GXDLMSProfileGeneric("0.0.99.98.7.255")
            reader.read(data, 3)
            buffer = reader.read_rows_by_range(data, time_for_check_self_diagnostic.get_start_time(key),
                                               time_for_check_self_diagnostic.get_end_time(key))
            code_list = [i[1] for i in buffer]

            errors_dict = {
                2: "Измерительный блок — ошибка",
                4: "Вычислительный блок — ошибка",
                5: "Часы реального времени — ошибка",
                7: "Блок питания — ошибка",
                9: "Дисплей — ошибка",
                11: "Блок памяти — ошибка",
                13: "Блок памяти программ — ошибка",
                15: "Система тактирования ядра — ошибка",
                17: "Система тактирования часов — ошибка",
                129: "Аппаратный сброс часов реального времени",
                132: "Сброс микроконтроллера сторожевым таймером"
            }

            errors_list = list(errors_dict.keys())

            # Преобразуем errors_list в set для ускорения поиска
            errors_set = set(errors_list)

            # Шаблон сообщения
            error_template = "В журнале самодиагностики обнаружен код {}: {}!!!"
            no_error_message = "В журнале самодиагностики аварийного кода не обнаружено."

            # Список найденных ошибок
            found_errors = []

            # Проверка кодов
            for code in code_list:
                if code in errors_set:
                    error_desc = errors_dict.get(code, "описание не найдено")
                    error_msg = error_template.format(code, error_desc)
                    found_errors.append(error_msg)

            # Формирование итогового сообщения
            if found_errors:
                message = "\n".join(found_errors)
                # Добавляем разделитель для читаемости
                full_message = "\n" + message + "\n"
            else:
                message = no_error_message
                full_message = "\n" + message + "\n"

            # Вывод и запись
            message_in_out(full_message)
            write_txt(file_name, full_message)

            time_for_check_self_diagnostic.set_start_time(key, current_time)
            return message
    except Exception as e:
        message_in_out(f'Ошибка при проверке кода ошибки в журнале самодиагностики >> {e}')
        raise


class CheckSelfDiagnostic:
    def __init__(self, list_of_serial):
        self.start_time = {}
        self.end_time = {}
        for i in list_of_serial:
            self.start_time[i] = None
            self.end_time[i] = None

    def set_start_time(self, key, start_time):
        self.start_time[key] = start_time

    def set_end_time(self, key, end_time):
        self.end_time[key] = end_time

    def get_start_time(self, key: str):
        return self.start_time.get(key)

    def get_end_time(self, key: str):
        return self.end_time.get(key)
    #
    # def start_timer(self, key):
    #     time = datetime.now()
    #     self.all_timer[key] = time
    #
    # def get_timer(self, key):
    #     time = self.all_timer[key]
    #     diff = datetime.now() - time
    #     return diff
    #