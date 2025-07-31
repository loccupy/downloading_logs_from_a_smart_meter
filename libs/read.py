from libs.Utils import *
from libs.connect import *


def read_logs(reader, flag_temperatyre, viborka, start, end):
    try:
        sample = sample_config(viborka, start, end)
        device_type = reader.deviceType

        print("Установлено соединение для считывания журналов")
        serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
        time = datetime.now().strftime("%d.%m.%y_%H.%M.%S")
        file_name = f"Serial_{serial_number}_{time}.xlsx"
        excel_writer = pd.ExcelWriter(file_name)

        create_sheet_in_excel_file(unloading_currents_log, excel_writer, 'Журнал токов', reader, sample)
        create_sheet_in_excel_file(unloading_the_voltage_log, excel_writer, 'Журнал напряжения', reader, sample)
        create_sheet_in_excel_file(unloading_power_log, excel_writer, 'Журнал мощности', reader, sample)
        if flag_temperatyre:
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
