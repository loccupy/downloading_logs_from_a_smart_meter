from time import sleep
import pandas as pd

from libs.Utils import *
from libs.connect import *

com = input("Введите номер COM порта: ")

while True:
    try:
        sample = sample_config()
        reader = connecting(com)

        reader.initializeConnection()
        print("Установлено соединение для считывания журналов")
        serial_number = reader.read(GXDLMSData('0.0.96.1.0.255'), 2).decode('utf-8')
        time = datetime.now().strftime("%d.%m.%y_%H.%M")
        excel_writer = pd.ExcelWriter(f"{serial_number}_{time}.xlsx")

        create_sheet_in_excel_file(unloading_currents_log, excel_writer, 'Журнал токов', reader, sample)
        create_sheet_in_excel_file(unloading_the_voltage_log, excel_writer, 'Журнал напряжения', reader, sample)
        create_sheet_in_excel_file(unloading_power_log, excel_writer, 'Журнал мощности', reader, sample)
        # create_sheet_in_excel_file(unloading_temperature_log, excel_writer, 'Журнал температуры', reader, sample)
        create_sheet_in_excel_file(unloading_self_diagnosis_log, excel_writer, 'Журнал самодиагностики', reader, sample)
        create_sheet_in_excel_file(unloading_network_quality_log, excel_writer, 'Журнал качества сети', reader, sample)
        create_sheet_in_excel_file(unloading_time_correction_log, excel_writer, 'Журнал коррекции времени', reader, sample)
        create_sheet_in_excel_file(unloading_battery_charge_status_monitoring_log, excel_writer,
                                   'Журнал состояния заряда батареи', reader, sample)
        create_sheet_in_excel_file(unloading_excess_load_tangent_log, excel_writer, 'Журнал превышения тангенса', reader, sample)
        create_sheet_in_excel_file(unloading_tangent_goes_beyond_log, excel_writer, 'Журнал Выход тангенса', reader, sample)
        if reader.deviceType != 'TT':
            create_sheet_in_excel_file(unloading_load_relay_blocker_control_log, excel_writer,
                                       'Журнал блокиратора реле', reader, sample)
        create_sheet_in_excel_file(unloading_network_quality_for_the_billing_period_log, excel_writer,
                                   'Журнал качества сети за период.', reader, sample)
        create_sheet_in_excel_file(unloading_on_off_log, excel_writer, 'Журнал включений и выключений', reader, sample)
        create_sheet_in_excel_file(unloading_communication_events_log, excel_writer,
                                   'Журнал коммуникационных событий', reader, sample)
        create_sheet_in_excel_file(unloading_access_control_log, excel_writer, 'Журнал контроля доступа', reader, sample)
        create_sheet_in_excel_file(unloading_data_correction_log, excel_writer, 'Журнал коррекции данных', reader, sample)
        create_sheet_in_excel_file(unloading_external_impacts_log, excel_writer, 'Журнал внешних воздействий', reader, sample)
        if reader.deviceType == 'TT':
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

        excel_writer._save()
        print("\nВСЕ ЖУРНАЛЫ ЗАПИСАНЫ\n")
        setting_the_speed_to_default_values(reader)
        reader.close()
        print("Разорвано соединение для считывания журналов")
        print("\nПЕРЕХОД К СЛЕДУЮЩЕМУ СЧЕТЧИКУ\n")
    except Exception as e:
        print(e.args)
    sleep(1)
