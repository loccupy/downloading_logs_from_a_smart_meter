import os
from time import sleep

from libs.Utils import *
from libs.check_self_diagnostic_log import check_error_code_in_self_diagnostic_log
from libs.check_time import check_time
from libs.connect import *
from libs.for_restart_driver import install_ch340_windows
from libs.sending_message import message_in_out


def read_data(config, time_for_check, time_for_check_self_diagnostic, file_name,  attempt=1, max_attempts=3):
    print(f"\nПровожу опрос счетчика №[...{config.serial_number}]...", end='')

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

    except Exception as e:
        close_reader(reader)
        if attempt < max_attempts:
            print(f"Попытка подключения при опросе счетчика {attempt} из {max_attempts} не удалась: {e}")
            write_txt(file_name,
                      f"\nПопытка подключения при опросе счетчика {attempt} из {max_attempts} не удалась: {e}\n")

            # if attempt == 1:
            #     write_txt(file_name, f"\nЗапускаю проверку скорости соединения при опросе...\n")
            #     check_speed_for_meter_survey(config)
            # else:
            #     install_ch340_windows()
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


# def read_type(config, main_directory, check_sample, attempt=1, max_attempts=3):
#     print("\nСчитываю тип счетчика и серийный номер с прибора учета, формирую стартовый excel файл...", end='')
#     reader_list = get_reader(config.com_meter, config.passw, config.serial_number, config.baud)
#     reader = reader_list[0]
#     settings = reader_list[1]
#     try:
#         init_connect(reader, settings)
#         sample = sample_config(config, reader, check_sample)
#         device_type = reader.deviceType
#         serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
#         print("Тип счетчика и серийный номер с прибора учета успешно считаны.")
#         close_reader(reader)
#         time = datetime.now().strftime("%d.%m.%y_%H.%M.%S")
#
#         # Создание папки для хранения журналов
#         directory = main_directory + f'/Выгрузка ПУ №[{serial_number}]_{time}'
#
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#
#         file_name = os.path.join(directory, f"Номер_[{serial_number[-5:]}]_тип_[{device_type}]_{time}.xlsx")
#
#         # file_name = f"Номер_[{serial_number[-5:]}]_тип_[{device_type}]_{time}.xlsx"
#         excel_writer = pd.ExcelWriter(file_name)
#         return device_type, excel_writer, file_name, sample
#     except Exception as e:
#         close_reader(reader)
#         if attempt < max_attempts:
#             print(f"Попытка подключения при считывании типа счетчика {attempt} из {max_attempts} не удалась: {e}")
#             print(f"Повторяем попытку через 2 секунды...")
#             sleep(2)  # Ждем 2 секунды перед повторной попыткой
#             return read_type(
#                 config,
#                 main_directory,
#                 check_sample,
#                 attempt + 1,
#                 max_attempts
#             )
#         else:
#             print(f"Превышено количество попыток подключения при считывании типа счетчика (5). Ошибка: {e}")
#             raise Exception(f"Превышено количество попыток подключения при считывании типа счетчика (5). Ошибка: {e}")


# meter survey
def meter_survey(config, time_for_check, time_for_check_self_diagnostic, file_name):
    try:
        read_data(config, time_for_check, time_for_check_self_diagnostic, file_name)
    except Exception as e:
        print(f'ОШИБКА ПРИ ОПРОСЕ СЧЕТЧИКА №...{config.serial_number} >> {e} ')
        raise


# def read_logs(config, main_directory, check_sample):
#     try:
#         speeding_up_the_connection(config)
#
#         device_type, excel_writer, file_name, sample = read_type(config, main_directory, check_sample)
#
#         print(f"\n  СТАРТ СЧИТЫВАНИЯ ЖУРНАЛОВ СЧЕТЧИКА №..{config.serial_number}...")
#
#         reader = config
#
#         create_sheet_in_excel_file(unloading_currents_log, excel_writer, 'Журнал токов', reader, sample)
#         create_sheet_in_excel_file(unloading_the_voltage_log, excel_writer, 'Журнал напряжения', reader, sample)
#         create_sheet_in_excel_file(unloading_power_log, excel_writer, 'Журнал мощности', reader, sample)
#         # if config.flag_viborka:
#         #     create_sheet_in_excel_file(unloading_temperature_log, excel_writer, 'Журнал температуры', reader, sample)
#         create_sheet_in_excel_file(unloading_self_diagnosis_log, excel_writer, 'Журнал самодиагностики', reader, sample)
#         create_sheet_in_excel_file(unloading_network_quality_log, excel_writer, 'Журнал качества сети', reader, sample)
#         create_sheet_in_excel_file(unloading_time_correction_log, excel_writer, 'Журнал коррекции времени', reader, sample)
#         create_sheet_in_excel_file(unloading_battery_charge_status_monitoring_log, excel_writer,
#                                    'Журнал состояния заряда батареи', reader, sample)
#         create_sheet_in_excel_file(unloading_excess_load_tangent_log, excel_writer, 'Журнал превышения тангенса', reader, sample)
#         create_sheet_in_excel_file(unloading_tangent_goes_beyond_log, excel_writer, 'Журнал Выход тангенса', reader, sample)
#         if device_type != 'TT':
#             create_sheet_in_excel_file(unloading_load_relay_blocker_control_log, excel_writer,
#                                        'Журнал блокиратора реле', reader, sample)
#         create_sheet_in_excel_file(unloading_network_quality_for_the_billing_period_log, excel_writer,
#                                    'Журнал качества сети за период', reader, sample)
#         create_sheet_in_excel_file(unloading_on_off_log, excel_writer, 'Журнал включений и выключений', reader, sample)
#         create_sheet_in_excel_file(unloading_communication_events_log, excel_writer,
#                                    'Журнал коммуникационных событий', reader, sample)
#         create_sheet_in_excel_file(unloading_access_control_log, excel_writer, 'Журнал контроля доступа', reader, sample)
#         create_sheet_in_excel_file(unloading_data_correction_log, excel_writer, 'Журнал коррекции данных', reader, sample)
#         create_sheet_in_excel_file(unloading_external_impacts_log, excel_writer, 'Журнал внешних воздействий', reader, sample)
#         if device_type == 'TT':
#             create_sheet_in_excel_file(unloading_discrete_in_and_out_states_log, excel_writer, 'Журнал состояний дискреток',
#                                        reader, sample)
#         create_sheet_in_excel_file(unloading_daily_profile, excel_writer, 'Суточный профиль', reader, sample)
#         create_sheet_in_excel_file(unloading_monthly_profile, excel_writer, 'Месячный профиль', reader, sample)
#         create_sheet_in_excel_file(unloading_energy_profile_for_recording_interval_1, excel_writer,
#                                    'Профиль энергии за инт. 1', reader, sample)
#         create_sheet_in_excel_file(unloading_energy_profile_for_recording_interval_2, excel_writer,
#                                    'Профиль энергии за инт. 2', reader, sample)
#         create_sheet_in_excel_file(unloading_arthur_slice, excel_writer,
#                                    'Срез мгновенных значений', reader, sample)
#
#         # reader.close()
#
#         excel_writer.close()
#
#         print("\nВСЕ ЖУРНАЛЫ ЗАПИСАНЫ")
#
#         setting_the_speed_to_default_values(config)
#
#         return [file_name, device_type]
#     except Exception as e:
#         print(f'ОШИБКА ПРИ ОБЩЕМ СЧИТЫВАНИИ ЖУРНАЛОВ СЧЕТЧИКА №...{config.serial_number} >> {e} ')
#         raise
