import os
from time import sleep

from libs.Utils import *
from libs.check_self_diagnostic_log import check_error_code_in_self_diagnostic_log
from libs.check_time import check_time
from libs.connect import *
from libs.sending_message import message_in_out


def read_data(config, time_for_check, time_for_check_self_diagnostic, file_name,  attempt=1, max_attempts=3):
    print(f"\n#############################\nПровожу опрос счетчика №[...{config.serial_number}]...", end='')

    write_txt(file_name, f"\nПровожу опрос счетчика №[...{config.serial_number}]...")

    reader_list = get_reader_with_ip(config.ip, '1234567898765432', config.serial_number, config.port)
    reader = reader_list[0]
    settings = reader_list[1]
    try:
        init_connect(reader, settings)

        device_type = reader.deviceType
        serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
        current_time = datetime.strptime(str(reader.read(GXDLMSClock('0.0.1.0.0.255'), 2)), "%m/%d/%y %H:%M:%S")

        duration = check_time(config, current_time, time_for_check)

        write_txt(file_name, f'\nТип счетчика >> {device_type}')
        write_txt(file_name, f'\nСерийный номер счетчика >> {serial_number}')
        write_txt(file_name, f'\nРасхождение времени >> {duration} сек.')
        message = check_error_code_in_self_diagnostic_log(config, reader, time_for_check_self_diagnostic, file_name)
        write_txt(file_name, f"Тип счетчика и серийный номер с прибора учета успешно считаны!!!\n")

        close_reader(reader)

        print(f'Тип счетчика >> {device_type}')
        print(f'Серийный номер счетчика >> {serial_number}')
        print(f'Расхождение времени >> {duration}')
        if message:
            print(message)
        print("Тип счетчика и серийный номер с прибора учета успешно считаны.")

        if attempt != 1:
            message_in_out(f"#Опрос_IP\n Удалось подключиться к счетчику №[...{config.serial_number}] с {attempt}-ой попытки.")
            write_txt(file_name, f"\nУдалось подключиться к счетчику №[...{config.serial_number}] с {attempt}-ой попытки.")
        print('#############################')

    except Exception as e:
        close_reader(reader)
        if attempt < max_attempts:
            print(f"Попытка подключения при опросе счетчика {attempt} из {max_attempts} не удалась: {e}")
            write_txt(file_name,
                      f"\nПопытка подключения при опросе счетчика {attempt} из {max_attempts} не удалась: {e}\n")

            print(f"Повторяем попытку через 2 секунды...")
            sleep(2)  # Ждем 2 секунды перед повторной попыткой
            return read_data(
                config,
                time_for_check,
                time_for_check_self_diagnostic,
                file_name,
                attempt + 1,
                max_attempts
            )
        else:
            print(f"Превышено количество попыток подключения при опросе счетчика (5). Ошибка: {e}")
            message_in_out(f"#Опрос_IP\n Не удалось подключиться к счетчику №...{config.serial_number}!!!")
            write_txt(file_name, f"\n Не удалось подключиться к счетчику №...{config.serial_number}!!!\n")
            raise Exception(f"Превышено количество попыток подключения при опросе счетчика (5). Ошибка: {e}")


def meter_survey(config, time_for_check, time_for_check_self_diagnostic, file_name):
    try:
        read_data(config, time_for_check, time_for_check_self_diagnostic, file_name)
    except Exception as e:
        print(f'ОШИБКА ПРИ ОПРОСЕ СЧЕТЧИКА №...{config.serial_number} >> {e} ')
        raise
