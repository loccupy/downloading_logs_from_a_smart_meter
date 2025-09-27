from libs.Utils import *
from libs.connect import *


def read_type(config):
    print("\nСчитываю тип счетчика и серийный номер с прибора учета, формирую стартовый excel файл...\n")
    reader_list = get_reader_with_ip(config.ip_meter, config.passw, config.serial_number, config.port_number)
    reader = reader_list[0]
    settings = reader_list[1]
    try:
        init_connect(reader, settings)
        device_type = reader.deviceType
        serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
        print("Тип счетчика и серийный номер с прибора учета успешно считаны.")
        close_reader(reader)
        time = datetime.now().strftime("%d.%m.%y_%H.%M.%S")
        file_name = f"Номер_[{serial_number[-5:]}]_тип_[{device_type}]_{time}.xlsx"
        excel_writer = pd.ExcelWriter(file_name)
        return device_type, excel_writer, file_name
    except Exception as e:
        close_reader(reader)
        print(f'Ошибка при считывании типа счетчика и формировании стартового excel файла >> {e} ')
        raise


def read_logs(config):
    try:
        print("\nСтарт считывания журналов...\n")
        sample = sample_config(config.flag_viborka, config.first_date, config.second_date)
        # device_type = reader.deviceType
        # serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
        # time = datetime.now().strftime("%d.%m.%y_%H.%M.%S")
        # file_name = f"Номер_[{serial_number[-5:]}]_тип_[{device_type}]_{time}.xlsx"
        # excel_writer = pd.ExcelWriter(file_name)

        device_type, excel_writer, file_name = read_type(config)

        reader = config

        create_sheet_in_excel_file(unloading_currents_log, excel_writer, 'Журнал токов', reader, sample)
        create_sheet_in_excel_file(unloading_the_voltage_log, excel_writer, 'Журнал напряжения', reader, sample)
        create_sheet_in_excel_file(unloading_power_log, excel_writer, 'Журнал мощности', reader, sample)
        if config.flag_viborka:
            create_sheet_in_excel_file(unloading_temperature_log, excel_writer, 'Журнал температуры', reader, sample)
        create_sheet_in_excel_file(unloading_self_diagnosis_log, excel_writer, 'Журнал самодиагностики', reader, sample)
        create_sheet_in_excel_file(unloading_network_quality_log, excel_writer, 'Журнал качества сети', reader, sample)
        create_sheet_in_excel_file(unloading_time_correction_log, excel_writer, 'Журнал коррекции времени', reader, sample)
        create_sheet_in_excel_file(unloading_battery_charge_status_monitoring_log, excel_writer,
                                   'Журнал состояния заряда батареи', reader, sample)
        create_sheet_in_excel_file(unloading_excess_load_tangent_log, excel_writer, 'Журнал превышения тангенса', reader, sample)
        create_sheet_in_excel_file(unloading_tangent_goes_beyond_log, excel_writer, 'Журнал Выход тангенса', reader, sample)
        if device_type != 'TT':
            create_sheet_in_excel_file(unloading_load_relay_blocker_control_log, excel_writer,
                                       'Журнал блокиратора реле', reader, sample)
        create_sheet_in_excel_file(unloading_network_quality_for_the_billing_period_log, excel_writer,
                                   'Журнал качества сети за период', reader, sample)
        create_sheet_in_excel_file(unloading_on_off_log, excel_writer, 'Журнал включений и выключений', reader, sample)
        create_sheet_in_excel_file(unloading_communication_events_log, excel_writer,
                                   'Журнал коммуникационных событий', reader, sample)
        create_sheet_in_excel_file(unloading_access_control_log, excel_writer, 'Журнал контроля доступа', reader, sample)
        create_sheet_in_excel_file(unloading_data_correction_log, excel_writer, 'Журнал коррекции данных', reader, sample)
        create_sheet_in_excel_file(unloading_external_impacts_log, excel_writer, 'Журнал внешних воздействий', reader, sample)
        if device_type == 'TT':
            create_sheet_in_excel_file(unloading_discrete_in_and_out_states_log, excel_writer, 'Журнал состояний дискреток',
                                       reader, sample)
        create_sheet_in_excel_file(unloading_daily_profile, excel_writer, 'Суточный профиль', reader, sample)
        create_sheet_in_excel_file(unloading_monthly_profile, excel_writer, 'Месячный профиль', reader, sample)
        create_sheet_in_excel_file(unloading_energy_profile_for_recording_interval_1, excel_writer,
                                   'Профиль энергии за инт. 1', reader, sample)
        create_sheet_in_excel_file(unloading_energy_profile_for_recording_interval_2, excel_writer,
                                   'Профиль энергии за инт. 2', reader, sample)
        create_sheet_in_excel_file(unloading_arthur_slice, excel_writer,
                                   'Срез мгновенных значений', reader, sample)

        # reader.close()

        excel_writer.close()

        print("\nВСЕ ЖУРНАЛЫ ЗАПИСАНЫ\n")

        return file_name, device_type
    except Exception as e:
        # print(f'Ошибка при общем считывании журналов >> {e} ')
        raise
