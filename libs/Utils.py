from datetime import datetime

import pandas as pd

from libs.gurux.dlms import GXDateTime
from libs.gurux.dlms.objects import GXDLMSProfileGeneric


def unloading_energy_profile_for_recording_interval_1(open_and_close_connection, sample):
    print("Начал запись Профиль энергии на 1-ом интервале...")
    data = GXDLMSProfileGeneric("1.0.99.1.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    active_energy_import_on_interval_1 = []
    active_energy_export_on_interval_1 = []
    reactive_energy_import_on_interval_1 = []
    reactive_energy_export_on_interval_1 = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        active_energy_import_on_interval_1.append(logs[i][1])
        active_energy_export_on_interval_1.append(logs[i][2])
        reactive_energy_import_on_interval_1.append(logs[i][3])
        reactive_energy_export_on_interval_1.append(logs[i][4])
    dictionary = {"Время фиксации записи": time,
                  "Активная энергия, импорт": active_energy_import_on_interval_1,
                  'Активная энергия, экспорт': active_energy_export_on_interval_1,
                  'Реактивная энергия, импорт': reactive_energy_import_on_interval_1,
                  'Реактивная энергия, экспорт': reactive_energy_export_on_interval_1}
    df = pd.DataFrame(dictionary)
    print("Профиль энергии на 1-ом интервале записан")
    return df


def unloading_energy_profile_for_recording_interval_2(open_and_close_connection, sample):
    print("Начал запись Профиль энергии на 2-ом интервале...")
    data = GXDLMSProfileGeneric("1.0.99.2.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    active_energy_import_on_interval_2 = []
    active_energy_export_on_interval_2 = []
    reactive_energy_import_on_interval_2 = []
    reactive_energy_export_on_interval_2 = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        active_energy_import_on_interval_2.append(logs[i][1])
        active_energy_export_on_interval_2.append(logs[i][2])
        reactive_energy_import_on_interval_2.append(logs[i][3])
        reactive_energy_export_on_interval_2.append(logs[i][4])
    dictionary = {"Время фиксации записи": time,
                  "Активная энергия, импорт": active_energy_import_on_interval_2,
                  'Активная энергия, экспорт': active_energy_export_on_interval_2,
                  'Реактивная энергия, импорт': reactive_energy_import_on_interval_2,
                  'Реактивная энергия, экспорт': reactive_energy_export_on_interval_2}
    df = pd.DataFrame(dictionary)
    print("Профиль энергии на 2-ом интервале записан")
    return df


def unloading_monthly_profile(open_and_close_connection, sample):
    print("Начал запись Месячного профиля...")
    data = GXDLMSProfileGeneric("1.0.98.1.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    accumulated_active_energy_import_total_for_all_time = []
    accumulated_active_energy_import_tariff_1_for_all_time = []
    accumulated_active_energy_import_tariff_2_for_all_time = []
    accumulated_active_energy_import_tariff_3_for_all_time = []
    accumulated_active_energy_import_tariff_4_for_all_time = []
    accumulated_active_energy_export_total_for_all_time = []
    accumulated_active_energy_export_tariff_1_for_all_time = []
    accumulated_active_energy_export_tariff_2_for_all_time = []
    accumulated_active_energy_export_tariff_3_for_all_time = []
    accumulated_active_energy_export_tariff_4_for_all_time = []
    total_reactive_energy_import = []
    reactive_energy_at_tariff_1_import = []
    reactive_energy_at_tariff_2_import = []
    reactive_energy_at_tariff_3_import = []
    reactive_energy_at_tariff_4_import = []
    total_reactive_energy_export = []
    reactive_energy_at_tariff_1_export = []
    reactive_energy_at_tariff_2_export = []
    reactive_energy_at_tariff_3_export = []
    reactive_energy_at_tariff_4_export = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        accumulated_active_energy_import_total_for_all_time.append(logs[i][1])
        accumulated_active_energy_import_tariff_1_for_all_time.append(logs[i][2])
        accumulated_active_energy_import_tariff_2_for_all_time.append(logs[i][3])
        accumulated_active_energy_import_tariff_3_for_all_time.append(logs[i][4])
        accumulated_active_energy_import_tariff_4_for_all_time.append(logs[i][5])
        accumulated_active_energy_export_total_for_all_time.append(logs[i][6])
        accumulated_active_energy_export_tariff_1_for_all_time.append(logs[i][7])
        accumulated_active_energy_export_tariff_2_for_all_time.append(logs[i][8])
        accumulated_active_energy_export_tariff_3_for_all_time.append(logs[i][9])
        accumulated_active_energy_export_tariff_4_for_all_time.append(logs[i][10])
        total_reactive_energy_import.append(logs[i][11])
        reactive_energy_at_tariff_1_import.append(logs[i][12])
        reactive_energy_at_tariff_2_import.append(logs[i][13])
        reactive_energy_at_tariff_3_import.append(logs[i][14])
        reactive_energy_at_tariff_4_import.append(logs[i][15])
        total_reactive_energy_export.append(logs[i][16])
        reactive_energy_at_tariff_1_export.append(logs[i][17])
        reactive_energy_at_tariff_2_export.append(logs[i][18])
        reactive_energy_at_tariff_3_export.append(logs[i][19])
        reactive_energy_at_tariff_4_export.append(logs[i][20])

    dictionary = {"Время фиксации записи": time,
                  "Накопленная активная энергия (импорт) общая за все время": accumulated_active_energy_import_total_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 1 за все время': accumulated_active_energy_import_tariff_1_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 2 за все время': accumulated_active_energy_import_tariff_2_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 3 за все время': accumulated_active_energy_import_tariff_3_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 4 за все время': accumulated_active_energy_import_tariff_4_for_all_time,
                  'Накопленная активная энергия (экспорт) общая за все время': accumulated_active_energy_export_total_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 1 за все время': accumulated_active_energy_export_tariff_1_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 2 за все время': accumulated_active_energy_export_tariff_2_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 3 за все время': accumulated_active_energy_export_tariff_3_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 4 за все время': accumulated_active_energy_export_tariff_4_for_all_time,
                  'Суммарная реактивная энергия, импорт': total_reactive_energy_import,
                  'Реактивная энергия по тарифу 1, импорт': reactive_energy_at_tariff_1_import,
                  'Реактивная энергия по тарифу 2, импорт': reactive_energy_at_tariff_2_import,
                  'Реактивная энергия по тарифу 3, импорт': reactive_energy_at_tariff_3_import,
                  'Реактивная энергия по тарифу 4, импорт': reactive_energy_at_tariff_4_import,
                  'Суммарная реактивная энергия, экспорт': total_reactive_energy_export,
                  'Реактивная энергия по тарифу 1, экспорт': reactive_energy_at_tariff_1_export,
                  'Реактивная энергия по тарифу 2, экспорт': reactive_energy_at_tariff_2_export,
                  'Реактивная энергия по тарифу 3, экспорт': reactive_energy_at_tariff_3_export,
                  'Реактивная энергия по тарифу 4, экспорт': reactive_energy_at_tariff_4_export,
                  }
    df = pd.DataFrame(dictionary)
    print("Месячный профиль записан")
    return df


def unloading_daily_profile(open_and_close_connection, sample):
    print("Начал запись Суточного профиля...")
    data = GXDLMSProfileGeneric("1.0.98.2.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    accumulated_active_energy_import_total_for_all_time = []
    accumulated_active_energy_import_tariff_1_for_all_time = []
    accumulated_active_energy_import_tariff_2_for_all_time = []
    accumulated_active_energy_import_tariff_3_for_all_time = []
    accumulated_active_energy_import_tariff_4_for_all_time = []
    accumulated_active_energy_export_total_for_all_time = []
    accumulated_active_energy_export_tariff_1_for_all_time = []
    accumulated_active_energy_export_tariff_2_for_all_time = []
    accumulated_active_energy_export_tariff_3_for_all_time = []
    accumulated_active_energy_export_tariff_4_for_all_time = []
    total_reactive_energy_import = []
    reactive_energy_at_tariff_1_import = []
    reactive_energy_at_tariff_2_import = []
    reactive_energy_at_tariff_3_import = []
    reactive_energy_at_tariff_4_import = []
    total_reactive_energy_export = []
    reactive_energy_at_tariff_1_export = []
    reactive_energy_at_tariff_2_export = []
    reactive_energy_at_tariff_3_export = []
    reactive_energy_at_tariff_4_export = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        accumulated_active_energy_import_total_for_all_time.append(logs[i][1])
        accumulated_active_energy_import_tariff_1_for_all_time.append(logs[i][2])
        accumulated_active_energy_import_tariff_2_for_all_time.append(logs[i][3])
        accumulated_active_energy_import_tariff_3_for_all_time.append(logs[i][4])
        accumulated_active_energy_import_tariff_4_for_all_time.append(logs[i][5])
        accumulated_active_energy_export_total_for_all_time.append(logs[i][6])
        accumulated_active_energy_export_tariff_1_for_all_time.append(logs[i][7])
        accumulated_active_energy_export_tariff_2_for_all_time.append(logs[i][8])
        accumulated_active_energy_export_tariff_3_for_all_time.append(logs[i][9])
        accumulated_active_energy_export_tariff_4_for_all_time.append(logs[i][10])
        total_reactive_energy_import.append(logs[i][11])
        reactive_energy_at_tariff_1_import.append(logs[i][12])
        reactive_energy_at_tariff_2_import.append(logs[i][13])
        reactive_energy_at_tariff_3_import.append(logs[i][14])
        reactive_energy_at_tariff_4_import.append(logs[i][15])
        total_reactive_energy_export.append(logs[i][16])
        reactive_energy_at_tariff_1_export.append(logs[i][17])
        reactive_energy_at_tariff_2_export.append(logs[i][18])
        reactive_energy_at_tariff_3_export.append(logs[i][19])
        reactive_energy_at_tariff_4_export.append(logs[i][20])

    dictionary = {"Время фиксации записи": time,
                  "Накопленная активная энергия (импорт) общая за все время": accumulated_active_energy_import_total_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 1 за все время': accumulated_active_energy_import_tariff_1_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 2 за все время': accumulated_active_energy_import_tariff_2_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 3 за все время': accumulated_active_energy_import_tariff_3_for_all_time,
                  'Накопленная активная энергия (импорт) тариф 4 за все время': accumulated_active_energy_import_tariff_4_for_all_time,
                  'Накопленная активная энергия (экспорт) общая за все время': accumulated_active_energy_export_total_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 1 за все время': accumulated_active_energy_export_tariff_1_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 2 за все время': accumulated_active_energy_export_tariff_2_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 3 за все время': accumulated_active_energy_export_tariff_3_for_all_time,
                  'Накопленная активная энергия (экспорт) тариф 4 за все время': accumulated_active_energy_export_tariff_4_for_all_time,
                  'Суммарная реактивная энергия, импорт': total_reactive_energy_import,
                  'Реактивная энергия по тарифу 1, импорт': reactive_energy_at_tariff_1_import,
                  'Реактивная энергия по тарифу 2, импорт': reactive_energy_at_tariff_2_import,
                  'Реактивная энергия по тарифу 3, импорт': reactive_energy_at_tariff_3_import,
                  'Реактивная энергия по тарифу 4, импорт': reactive_energy_at_tariff_4_import,
                  'Суммарная реактивная энергия, экспорт': total_reactive_energy_export,
                  'Реактивная энергия по тарифу 1, экспорт': reactive_energy_at_tariff_1_export,
                  'Реактивная энергия по тарифу 2, экспорт': reactive_energy_at_tariff_2_export,
                  'Реактивная энергия по тарифу 3, экспорт': reactive_energy_at_tariff_3_export,
                  'Реактивная энергия по тарифу 4, экспорт': reactive_energy_at_tariff_4_export,
                  }
    df = pd.DataFrame(dictionary)
    print("Суточный профиль записан")
    return df


def unloading_arthur_slice(open_and_close_connection, sample):
    print("Начал запись Среза мгновенных значений...")
    data = GXDLMSProfileGeneric("1.0.99.164.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    if open_and_close_connection.deviceType == '1PH':
        time = []
        data_1 = []
        data_2 = []
        data_3 = []
        data_4 = []
        data_5 = []
        data_6 = []
        data_7 = []
        data_8 = []
        data_9 = []
        data_10 = []
        data_11 = []
        data_12 = []
        data_13 = []
        data_14 = []
        data_15 = []
        leave = []
        for i in range(len(logs)):
            time.append(ref_date_time(logs[i][0]))
            data_1.append(current_with_scalar(logs[i][1]))
            data_2.append(current_with_scalar(logs[i][2]))
            data_3.append(voltage_with_scalar(logs[i][3]))
            data_4.append(logs[i][4])
            data_5.append(hertz_with_scalar(logs[i][5]))
            data_6.append(power_with_scalar(logs[i][6]))
            data_7.append(power_with_scalar(logs[i][7]))
            data_8.append(power_with_scalar(logs[i][8]))
            data_9.append(logs[i][9])
            data_10.append(logs[i][10])
            data_11.append(logs[i][11])
            data_12.append(logs[i][12])
            data_13.append(logs[i][13])
            data_14.append(logs[i][14])
            data_15.append(logs[i][15])
            leave.append(logs[i][16])
        dictionary = {"Время фиксации записи": time,
                      "Ток фазы": data_1,
                      'Ток нейтрали': data_2,
                      'Напряжение фазы': data_3,
                      'Коэффициент мощности': data_4,
                      'Частота сети': data_5,
                      'Полная мощность': data_6,
                      'Активная мощность': data_7,
                      'Реактивная мощность': data_8,
                      'Активная энергия, импорт': data_9,
                      'Активная энергия, экспорт': data_10,
                      'Реактивная энергия, импорт': data_11,
                      'Реактивная энергия, экспорт': data_12,
                      'Дифф. ток': data_13,
                      'Дифф. ток, % от фазного тока': data_14,
                      'Коэффициент реактивной мощности': data_15,
                      'Время работы ПУ': leave
                      }
    else:
        time = []
        data_1 = []
        data_2 = []
        data_3 = []
        data_4 = []
        data_5 = []
        data_6 = []
        data_7 = []
        data_8 = []
        data_9 = []
        data_10 = []
        data_11 = []
        data_12 = []
        data_13 = []
        data_14 = []
        data_15 = []
        data_16 = []
        data_17 = []
        data_18 = []
        data_19 = []
        data_20 = []
        data_21 = []
        data_22 = []
        data_23 = []
        data_24 = []
        leave = []
        for i in range(len(logs)):
            time.append(ref_date_time(logs[i][0]))
            data_1.append(current_with_scalar(logs[i][1]))
            data_2.append(current_with_scalar(logs[i][2]))
            data_3.append(current_with_scalar(logs[i][3]))
            data_4.append(current_with_scalar(logs[i][4]))
            data_5.append(current_with_scalar(logs[i][5]))
            data_6.append(voltage_with_scalar(logs[i][6]))
            data_7.append(voltage_with_scalar(logs[i][7]))
            data_8.append(voltage_with_scalar(logs[i][8]))
            data_9.append(logs[i][9])
            data_10.append(hertz_with_scalar(logs[i][10]))
            data_11.append(power_with_scalar(logs[i][11]))
            data_12.append(power_with_scalar(logs[i][12]))
            data_13.append(power_with_scalar(logs[i][13]))
            data_14.append(logs[i][14])
            data_15.append(logs[i][15])
            data_16.append(logs[i][16])
            data_17.append(logs[i][17])
            data_18.append(voltage_with_scalar(logs[i][18]))
            data_19.append(voltage_with_scalar(logs[i][19]))
            data_20.append(voltage_with_scalar(logs[i][20]))
            data_21.append(logs[i][21])
            data_22.append(logs[i][22])
            data_23.append(logs[i][23])
            data_24.append(logs[i][24])
            leave.append(logs[i][25])
        dictionary = {"Время фиксации записи": time,
                      "Ток фазы А": data_1,
                      'Ток фазы B': data_2,
                      'Ток фазы C': data_3,
                      'Ток нейтрали': data_4,
                      'Диф. ток': data_5,
                      'Напряжение фазы А': data_6,
                      'Напряжение фазы B': data_7,
                      'Напряжение фазы C': data_8,
                      'Коэффициент мощности, суммарный': data_9,
                      'Частота': data_10,
                      'Полная мощность, сумма всех фаз': data_11,
                      'Активная мощность, сумма всех фаз': data_12,
                      'Реактивная мощность, сумма всех фаз': data_13,
                      'Активная энергия, импорт': data_14,
                      'Активная энергия, экспорт': data_15,
                      'Реактивная энергия, импорт': data_16,
                      'Реактивная энергия, экспорт': data_17,
                      'Линейное напряжение AB': data_18,
                      'Линейное напряжение BC': data_19,
                      'Линейное напряжение CA': data_20,
                      'Коэффициент реакт. мощности, фаза A': data_21,
                      'Коэффициент реакт. мощности, фаза B': data_22,
                      'Коэффициент реакт. мощности, фаза C': data_23,
                      'Коэффициент реакт. мощности, суммарный': data_24,
                      'Время работы ПУ': leave
                      }
    df = pd.DataFrame(dictionary)
    print("Срез мгновенных значений записан")
    return df


def unloading_the_voltage_log(open_and_close_connection, sample):
    print("Начал запись Журнала напряжения...")
    data = GXDLMSProfileGeneric("0.0.99.98.0.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    voltage = []
    depth = []
    duration = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(voltage_event_code)):
            if logs[i][1] == voltage_event_code[z][0]:
                err.append(f'{voltage_event_code[z][0]}, {voltage_event_code[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        voltage.append(voltage_with_scalar(logs[i][2]))
        depth.append(logs[i][3])
        duration.append(logs[i][4])
        leave.append(logs[i][5])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  'Напряжение любой фазы': voltage,
                  'Глубина провала/перенапряжения': depth,
                  'Длительность провала/перенапряжения': duration,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал напряжения записан")
    return df


def unloading_currents_log(open_and_close_connection, sample):
    print("Начал запись Журнала токов...")
    data = GXDLMSProfileGeneric("0.0.99.98.1.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventAmperageCode)):
            if logs[i][1] == EventAmperageCode[z][0]:
                err.append(f'{EventAmperageCode[z][0]}, {EventAmperageCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал токов записан")
    return df


def unloading_on_off_log(open_and_close_connection, sample):
    print("Начал запись Журнала вкл/выкл...")
    data = GXDLMSProfileGeneric("0.0.99.98.2.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(turn_off_even_code)):
            if logs[i][1] == turn_off_even_code[z][0]:
                err.append(f'{turn_off_even_code[z][0]}, {turn_off_even_code[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал включений / выключений записан")
    return df


def unloading_data_correction_log(open_and_close_connection, sample):
    print("Начал запись Журнала коррекции данных...")
    data = GXDLMSProfileGeneric("0.0.99.98.3.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    port_number = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventProgramingCode)):
            if logs[i][1] == EventProgramingCode[z][0]:
                err.append(f'{EventProgramingCode[z][0]}, {EventProgramingCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        port_number.append(parsing_port_number(logs[i][2]))
        leave.append(logs[i][3])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  'Номер порта, по которому установлено соединение': port_number,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал коррекции данных записан")
    return df


def unloading_external_impacts_log(open_and_close_connection, sample):
    print("Начал запись Журнала внешних воздействий...")
    data = GXDLMSProfileGeneric("0.0.99.98.4.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventExternalInfluenceCode)):
            if logs[i][1] == EventExternalInfluenceCode[z][0]:
                err.append(f'{EventExternalInfluenceCode[z][0]}, {EventExternalInfluenceCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал внешних воздействий записан")
    return df


def unloading_communication_events_log(open_and_close_connection, sample):
    print("Начал запись Журнала коммуникационных событий...")
    data = GXDLMSProfileGeneric("0.0.99.98.5.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    port_number = []
    address = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventCommunicationCode)):
            if logs[i][1] == EventCommunicationCode[z][0]:
                err.append(f'{EventCommunicationCode[z][0]}, {EventCommunicationCode[z][1]}')
                break
        else:
            err.append(f'[{logs[i][1]}] - несуществующий код')
        port_number.append(parsing_port_number(logs[i][2]))

        for y in range(len(client_address)):
            if logs[i][3] == client_address[y][0]:
                address.append(f'{client_address[y][0]}, {client_address[y][1]}')
                break
        else:
            address.append(f'{logs[i][3]}, Неописанный адрес')

        leave.append(logs[i][4])
    dictionary = {"Время фиксации записи": time,
                  "Коммуникационные события": err,
                  'Номер порта, по которому установлено соединение': port_number,
                  'Адрес клиента': address,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал коммуникационных событий записан")
    return df


def unloading_access_control_log(open_and_close_connection, sample):
    print("Начал запись Журнала контроля доступа...")
    data = GXDLMSProfileGeneric("0.0.99.98.6.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    port_number = []
    address = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventAccessCode)):
            if logs[i][1] == EventAccessCode[z][0]:
                err.append(f'{EventAccessCode[z][0]}, {EventAccessCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        port_number.append(parsing_port_number(logs[i][2]))
        for y in range(len(client_address)):
            if logs[i][3] == client_address[y][0]:
                address.append(f'{client_address[y][0]}, {client_address[y][1]}')
                break
        else:
            address.append(f'{logs[i][3]}, Неописанный адрес')
        leave.append(logs[i][4])
    dictionary = {"Время фиксации записи": time,
                  "Код последнего события в журнале контроля доступа": err,
                  'Номер порта, по которому установлено соединение': port_number,
                  'Адрес клиента': address,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал контроля доступа записан")
    return df


def unloading_self_diagnosis_log(open_and_close_connection, sample):
    print("Начал запись Журнала самодиагностики...")
    data = GXDLMSProfileGeneric("0.0.99.98.7.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventSelfDiagCode)):
            if logs[i][1] == EventSelfDiagCode[z][0]:
                err.append(f'{EventSelfDiagCode[z][0]}, {EventSelfDiagCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Событие": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал самодиагностики записан")
    return df


def unloading_excess_load_tangent_log(open_and_close_connection, sample):
    print("Начал запись Журнала превышения тангенса нагрузки...")
    data = GXDLMSProfileGeneric("0.0.99.98.8.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventTangentCode)):
            if logs[i][1] == EventTangentCode[z][0]:
                err.append(f'{EventTangentCode[z][0]}, {EventTangentCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "События по превышению реактивной мощности 𝑡𝑔(𝜑)": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал превышения тангенса нагрузки записан")
    return df


def unloading_network_quality_log(open_and_close_connection, sample):
    print("Начал запись Журнала качества сети...")
    data = GXDLMSProfileGeneric("0.0.99.98.9.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventQualityLog)):
            if logs[i][1] == EventQualityLog[z][0]:
                err.append(f'{EventQualityLog[z][0]}, {EventQualityLog[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код или слияние масок')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Статус качества сети": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал качество сети записан")
    return df


def unloading_tangent_goes_beyond_log(open_and_close_connection, sample):
    print("Начал запись Журнала выход тангенса за порог...")
    data = GXDLMSProfileGeneric("0.0.99.98.12.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        err.append(logs[i][1])
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  "Коэффициент реактивной мощности (tg φ). Среднее значение на интервале интегрирования 2": err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал выход тангенса за порог на интервале интегрирования 2 записан")
    return df


def unloading_time_correction_log(open_and_close_connection, sample):
    print("Начал запись Журнала коррекции времени...")
    data = GXDLMSProfileGeneric("0.0.99.98.13.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        err.append(ref_date_time(logs[i][1]))
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Старое время': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал коррекции времени записан")
    return df


def unloading_network_quality_for_the_billing_period_log(open_and_close_connection, sample):
    print("Начал запись Журнала качества сети за расчетный период...")
    data = GXDLMSProfileGeneric("0.0.99.98.15.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    num = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        err.append(logs[i][1])
        num.append(logs[i][2])
        leave.append(logs[i][3])
    dictionary = {"Время фиксации записи": time,
                  'Длительность отклонения напряжения': err,
                  'Количество перенапряжений за расчётный период': num,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал качества сети за расчетный период записан")
    return df


def unloading_power_log(open_and_close_connection, sample):
    print("Начал запись Журнала мощности...")
    data = GXDLMSProfileGeneric("0.0.99.98.16.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventPowerCode)):
            if logs[i][1] == EventPowerCode[z][0]:
                err.append(f'{EventPowerCode[z][0]}, {EventPowerCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Слово состояний контроля мощности': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал мощности записан")
    return df


def unloading_battery_charge_status_monitoring_log(open_and_close_connection, sample):
    print("Начал запись Журнала контроля состояния заряда батареи...")
    data = GXDLMSProfileGeneric("0.0.99.98.17.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(EventBatteryChargeMonitoringCode)):
            if logs[i][1] == EventBatteryChargeMonitoringCode[z][0]:
                err.append(f'{EventBatteryChargeMonitoringCode[z][0]}, {EventBatteryChargeMonitoringCode[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Текущее состояние заряда батареи': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал контроля состояния заряда батареи записан")
    return df


def unloading_load_relay_blocker_control_log(open_and_close_connection, sample):
    print("Начал запись Журнала контроля блокиратора реле нагрузки...")
    data = GXDLMSProfileGeneric("0.0.99.98.18.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(PositionRelay)):
            if logs[i][1] == PositionRelay[z][0]:
                err.append(f'{PositionRelay[z][0]}, {PositionRelay[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Текущее положение аппаратной блокировки реле': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал контроля блокиратора реле нагрузки записан")
    return df


def unloading_temperature_log(open_and_close_connection, sample):
    print("Начал запись Журнала температуры...")
    data = GXDLMSProfileGeneric("0.0.99.98.19.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        for z in range(len(TemperatureJournalEvents)):
            if logs[i][1] == TemperatureJournalEvents[z][0]:
                err.append(f'{TemperatureJournalEvents[z][0]}, {TemperatureJournalEvents[z][1]}')
                break
        else:
            err.append(f'{logs[i][1]} - несуществующий код')
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Код события изменения температуры': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал температуры записан")
    return df


def unloading_discrete_in_and_out_states_log(open_and_close_connection, sample):
    print("Начал запись Журнала состояний дискреток...")
    data = GXDLMSProfileGeneric("0.0.99.98.10.255")
    open_and_close_connection.read(data, 3)
    logs = range_by_date(open_and_close_connection, data, sample)
    time = []
    err = []
    leave = []
    for i in range(len(logs)):
        time.append(ref_date_time(logs[i][0]))
        err.append(logs[i][1])
        leave.append(logs[i][2])
    dictionary = {"Время фиксации записи": time,
                  'Состояние дискретных входов и выходов': err,
                  "Время работы ПУ": leave}
    df = pd.DataFrame(dictionary)
    print("Журнал состояний дискреток записан")
    return df


voltage_event_code = [
    (1, "Фаза A - пропадание напряжения"),
    (2, "Фаза A - восстановление напряжения"),
    (3, "Фаза B - пропадание напряжения"),
    (4, "Фаза B - восстановление напряжения"),
    (5, "Фаза C - пропадание напряжения"),
    (6, "Фаза C - восстановление напряжения"),
    (7, "Превышение напряжения любой фазы"),
    (8, "Окончание перенапряжения любой фазы"),
    (9, "Низкое напряжение любой фазы - начало"),
    (10, "Низкое напряжение любой фазы - окончание"),
    (11, "Превышение коэффициента несимметрии напряжений по обратной последовательности - начало"),
    (12, "Превышение коэффициента несимметрии напряжений по обратной последовательности - окончание"),
    (13, "Фаза A - перенапряжение - начало"),
    (14, "Фаза A - перенапряжение - окончание"),
    (15, "Фаза B - перенапряжение - начало"),
    (16, "Фаза B - перенапряжение - окончание"),
    (17, "Фаза C - перенапряжение - начало"),
    (18, "Фаза C - перенапряжение - окончание"),
    (19, "Фаза A - провал - начало"),
    (20, "Фаза A - провал - окончание"),
    (21, "Фаза B - провал - начало"),
    (22, "Фаза B - провал - окончание"),
    (23, "Фаза C - провал - начало"),
    (24, "Фаза C - провал - окончание"),
    (25, "Неправильная последовательность фаз - начало"),
    (26, "Неправильная последовательность фаз - окончание"),
    (27, "Прерывание напряжения"),
    (28, "Восстановление напряжения")
]

turn_off_even_code = [
    (1, "Выключение питания ПУ"),
    (2, "Включение питания ПУ"),
    (3, "Выключение абонента - дистанционное"),
    (4, "Включение абонента - дистанционное"),
    (5, "Получение разрешения на включение абоненту"),
    (6, "Выключение реле нагрузки абонентом"),
    (7, "Включение реле нагрузки абонентом"),
    (8, "Выключение локальное по превышению лимита мощности"),
    (9, "Выключение локальное по превышению максимального тока"),
    (10, "Выключение локальное при воздействии магнитного поля"),
    (11, "Выключение локальное по превышению напряжения"),
    (12, "Включение локальное при возвращение напряжения в норму"),
    (13, "Выключение локальное по наличию тока при отсутствии напряжения"),
    (14, "Выключение локальное по небалансу токов"),
    (15, "Выключение локальное по температуре"),
    (16, "Включение резервного питания"),
    (17, "Отключение резервного питания"),
    (18, "Выключение локальное при вскрытии клеммной крышки или корпуса"),
    (19, "Выключение реле при превышении лимитов энергии по тарифам"),
    (20, "Включение реле после выключения по причине превышения активной мощности"),
    (21, "Включение реле после выключения по причине превышения тока"),
    (22, "Включение реле после выключения по причине превышения небаланса токов"),
    (23, "Включение реле после возвращения температуры в норму"),
    (24, "Включение реле после возвращения магнитного поля в норму"),
    (25, "Выключение реле через арбитр"),
    (26, "Включение реле через арбитр"),
    (27, "Включение реле через физический блокиратор"),
    (28, "Выключение реле через физический блокиратор"),
    (29, "Полное пропадание питания ПУ"),
    (50, "непонятное событие")
]

EventAmperageCode = [
    (1, "Фаза А - экспорт начало"),
    (2, "Фаза А - экспорт окончание"),
    (3, "Фаза B- экспорт начало"),
    (4, "Фаза B - экспорт окончание"),
    (5, "Фаза C - экспорт начало"),
    (6, "Фаза C - экспорт окончание"),
    (7, "Обрыв трансформатора тока фазы А"),
    (8, "Восстановление трансформатора тока фазы А"),
    (9, "Обрыв трансформатора тока фазы В"),
    (10, "Восстановление трансформатора тока фазы B"),
    (11, "Обрыв трансформатора тока фазы C"),
    (12, "Восстановление трансформатора тока фазы C"),
    (13, "Небаланс токов - начало"),
    (14, "Небаланс токов - окончание"),
    (15, "Замыкание трансформатора тока — начало"),
    (16, "Окончание замыкания трансформатора тока"),
    (17, "Превышение тока любой фазы - начало"),
    (18, "Окончание превышения тока любой фазы"),
    (19, "Фаза А - наличие тока при отсутствии напряжения начало"),
    (20, "Фаза А - наличие тока при отсутствии напряжения окончание"),
    (21, "Фаза B - наличие тока при отсутствии напряжения начало"),
    (22, "Фаза B - наличие тока при отсутствии напряжения окончание"),
    (23, "Фаза C - наличие тока при отсутствии напряжения начало"),
    (24, "Фаза C - наличие тока при отсутствии напряжения окончание"),
    (25, "Фаза А - превышение максимального тока начало"),
    (26, "Фаза А - превышение максимального тока окончание"),
    (27, "Фаза B - превышение максимального тока начало"),
    (28, "Фаза B - превышение максимального тока окончание"),
    (29, "Фаза C - превышение максимального тока начало"),
    (30, "Фаза C - превышение максимального тока окончание"),
    (31, "Наличие тока при отсутствии напряжения (обрыв нейтрали) – начало"),
    (32, "Наличие тока при отсутствии напряжения (обрыв нейтрали) - окончание"),
    (33, "Обратный поток мощности (экспорт тока) в однонаправленном приборе учета - начало"),
    (34, "Обратный поток мощности (экспорт тока) в однонаправленном приборе учета - окончание"),
    (35, "Разнонаправленная мощность по фазам в трёхфазном и однофазном двухэлементном приборе учета - начало"),
    (36, "Разнонаправленная мощность по фазам в трёхфазном и однофазном двухэлементном приборе учета – окончание"),
    (37, "Наличие тока при выключенном реле нагрузки – начало"),
    (38, "Наличие тока при выключенном реле нагрузки – окончание")
]

EventBatteryChargeMonitoringCode = [
    (0, "Батарея заряжена"),
    (1, "Батарея скоро будет полностью разряжена"),
    (2, "Батарея полностью разряжена или отсутствует")
]

EventCommunicationCode = [
    (1, "Разорвано соединение"),
    (2, "Установлено соединение")
]

# EventCurrentCode = [
#     (1, "Фаза A - экспорт начало"),
#     (2, "Фаза A - экспорт окончание"),
#     (3, "Фаза B - экспорт начало"),
#     (4, "Фаза B - экспорт окончание"),
#     (5, "Фаза C - экспорт начало"),
#     (6, "Фаза C - экспорт окончание"),
#     (7, "Обрыв трансформатора тока фазы A"),
#     (8, "Восстановление трансформатора тока фазы A"),
#     (9, "Обрыв трансформатора тока фазы B"),
#     (10, "Восстановление трансформатора тока фазы B"),
#     (11, "Обрыв трансформатора тока фазы C"),
#     (12, "Восстановление трансформатора тока фазы C"),
#     (13, "Небаланс токов - начало"),
#     (14, "Небаланс токов - окончание"),
#     (15, "Замыкание трансформатора тока - начало"),
#     (16, "Окончание замыкания трансформатора тока")
# ]

EventProgramingCode = [
    (1, "Изменение адреса или скорости обмена RS-485-1 (Порт P2)"),
    (2, "Изменение адреса или скорости обмена RS-485-2 (Порт P3)"),
    (3, "Установка времени"),
    (4, "Изменение параметров перехода на летнее время"),
    (5, "Изменение сезонного профиля тарифного расписания(ТР)"),
    (6, "Изменение недельного профиля ТР"),
    (7, "Изменение суточного профиля ТР"),
    (8, "Изменение даты активации ТР"),
    (9, "Активация ТР"),
    (10, "Изменение расчетного дня / часа(РДЧ)"),
    (11, "Изменение режима индикации(параметры)"),
    (12, "Изменение режима индикации(автопереключение)"),
    (13, "Изменение пароля низкой секретности(на чтение)"),
    (14, "Изменение пароля высокой секретности (на запись)"),
    (15, "Изменение данных точки учета"),
    (16, "Изменение коэффициента трансформации по току"),
    (17, "Изменение коэффициента трансформации по напряжению"),
    (18, "Изменение параметров линии для вычисления потерь в ЛЭП"),
    (19, "Изменение лимита активной мощности для отключения"),
    (20, "Изменение интервала времени на отключение по активной мощности"),
    (21, "Изменение интервала времени на отключение по превышению максимального тока"),
    (22, "Изменение интервала времени на отключение по максимальному напряжению"),
    (23, "Изменение интервала времени на отключение по воздействию магнитного поля"),
    (24, "Изменение порога для фиксации перерыва в питании"),
    (25, "Изменение порога для фиксации перенапряжения"),
    (26, "Изменение порога для фиксации провала напряжения"),
    (27, "Изменение порога для фиксации превышения тангенса"),
    (28, "Изменение порога для фиксации коэффициента несимметрии напряжений"),
    (29, "Изменение согласованного напряжения"),
    (30, "Изменение интервала интегрирования пиковой мощности"),
    (31, "Изменение периода захвата профиля 1"),
    (32, "Изменение периода захвата профиля 2"),
    (33, "Изменение режима подсветки ЖКИ"),
    (34, "Изменение режима телеметрии 1"),
    (35, "Очистка «Месячного журнала»"),
    (36, "Очистка «Суточного журнала»"),
    (37, "Очистка «Журнала напряжения»"),
    (38, "Очистка «Журнала тока»"),
    (39, "Очистка «Журнала вкл/выкл»"),
    (40, "Очистка журнала «Внешних воздействий»"),
    (41, "Очистка журнала «Коммуникационные события»"),
    (42, "Очистка журнала «Контроль доступа»"),
    (43, "Очистка журнала «Параметры качества сети»"),
    (44, "Очистка журнала «Превышение тангенса»"),
    (45, "Очистка журнала «Состояний дискретных входов и выходов»"),
    (46, "Очистка профиля 1"),
    (47, "Очистка профиля 2"),
    (48, "Очистка профиля 3"),
    (49, "Изменение таблицы специальных дней"),
    (50, "Изменение режима управления реле нагрузки"),
    (51, "Фиксация показаний в месячном журнале"),
    (52, "Изменение режима инициативного выхода"),
    (53, "Изменение одноадресного ключа для низкой секретности"),
    (54, "Изменение широковещательного ключа шифрования для низкой секретности"),
    (55, "Изменение одноадресного ключа для высокой секретности"),
    (56, "Изменение широковещательного ключа для высокой секретности"),
    (57, "Изменение ключа аутентификации для высокой секретности"),
    (58, "Изменение мастер-ключа"),
    (59, "Изменение уровня преобразования для низкой секретности"),
    (60, "Изменение уровня преобразования для высокой секретности"),
    (61, "Изменение номера дистанционного дисплея"),
    (62, "Изменение режима учета активной энергии (по модулю или в раздельно в двух направлени"),
    (63, "Установка времени по GPS/ГЛОНАСС"),
    (64, "Изменение режима отключения по обрыву нейтрали"),
    (65, "Обновление ПО"),
    (66, "Изменение режима отключения по небалансу токов"),
    (67, "Изменение режима отключения по температуре"),
    (68, "Коррекция времени"),
    (69, "Изменение ключа аутентификации для низкой секретности"),
    (70, "Очистка флагов инициативного выхода"),
    (71, "Изменение таймаута для HDLC-соединения"),
    (72, "Изменение часов больших нагрузок"),
    (73, "Изменение часов контроля максимума"),
    (74, "Изменение схемы подключения"),
    (75, "Изменение режима телеметрии 2"),
    (76, "Изменение режима телеметрии 3"),
    (77, "Изменение режима телеметрии 4"),
    (78, "Резерв"),
    (79, "Изменение настройки активного коммуникационного профиля для портов связи"),
    (80, "Очистка журнала качества сети за расчётный период"),
    (81, "Резерв"),
    (82, "Изменение пороговое значение по времени. Коэффициент реактивной мощности (tg φ) средний по всем фазам."),
    (83, "Изменение порогового значения по времени. Дифференциальный ток, %."),
    (84, "Изменение порогового значения по времени. Коэффициент несимметрии по обратной последовательности."),
    (85, "Изменение адреса или скорости обмена (Оптопорт P1)"),
    (86, "Изменение адреса или скорости обмена (Порт P4)"),
    (87, "Изменение фильтра событий отключения реле нагрузки"),
    (88, "Резерв"),
    (89, "Резерв"),
    (90, "Изменение порогового значения отклонения частоты"),
    (91, "Изменение порогового значения контроля активной мощности на интервале интегрирования"),
    (
        92,
        "Изменение порогового значения контроля активной мощности на интервале интегрирования в часы пиковых нагрузок"),
    (93, "Изменение времени фиксации стоп кадра / Фиксация стоп кадра"),
    (94, "Монитор событий реле нагрузки"),
    (95, "Монитор событий реле сигнализации 1"),
    (96, "Монитор событий реле сигнализации 2"),
    (97, "Монитор событий реле сигнализации 3"),
    (98, "Монитор событий реле сигнализации 4"),
    (99, "Изменение параметров арбитра реле нагрузки"),
    (100, "Изменение параметров арбитра реле сигнализации 1"),
    (101, "Изменение параметров арбитра реле сигнализации 2"),
    (102, "Изменение параметров арбитра реле сигнализации 3"),
    (103, "Изменение параметров арбитра реле сигнализации 4"),
    (104, "Изменение фильтра событий реле сигнализации 1"),
    (105, "Изменение фильтра событий реле сигнализации 2"),
    (106, "Изменение фильтра событий реле сигнализации 3"),
    (107, "Изменение фильтра событий реле сигнализации 4"),
    (108, "Изменение режима управления реле сигнализации 1"),
    (109, "Изменение режима управления реле сигнализации 2"),
    (110, "Изменение режима управления реле сигнализации 3"),
    (111, "Изменение режима управления реле сигнализации 4"),
    (112, "Изменение типа контакта реле сигнализации"),
    (113, "Изменение таймаута для TCP/UDP соединения (Оптопорт P1)"),
    (114, "Изменение таймаута для TCP/UDP соединения (Порт P2)"),
    (115, "Изменение таймаута для TCP/UDP соединения (Порт P3)"),
    (116, "Изменение таймаута для TCP/UDP соединения (Порт P4)"),
    (117, "Очистка журнала «выхода тангенса за порог на интервале интегрирования»"),
    (118, "Очистка журнала «коррекции времени»"),
    (119, "Очистка журнала «На начало года»"),
    (120, "Резерв"),
    (121, "Очистка журнала «Контроля мощности»"),
    (122, "Очистка журнала «Батареи»"),
    (123, "Очистка журнала «Контроль блокиратора реле нагрузки»"),
    (124, "Очистка журнала «Контроль температуры»"),
    (125, "Очистка журнала «Отклонение напряжения фазы А»"),
    (126, "Очистка журнала «Отклонение напряжения фазы B»"),
    (127, "Очистка журнала «Отклонение напряжения фазы C»"),
    (128, "Очистка журнала «Отклонение линейного напряжения AB»"),
    (129, "Очистка журнала «Отклонение линейного напряжения BC»"),
    (130, "Очистка журнала «Отклонение линейного напряжения CA»"),
    (131, "Очистка журнала «Превышение напряжения»"),
    (132, "Очистка журнала «Прерывание напряжения"),
    (133, "Очистка журнала «Телесигнализация"),
    (134, "Очистка журнала «Нештатная ситуация сети»"),
    (135,
     "Изменение порога напряжения по нулевой последовательности, максимальное значение, В (нештатная ситуация сети)"),
    (136,
     "Изменение порога напряжения по нулевой последовательности, время до срабатывания события, с (нештатная ситуация сети)"),
    (137,
     "Изменение порога напряжения по нулевой последовательности, время задержки установки события PUSH, с (нештатная ситуация сети)"),
    (138, "Изменение порога напряжения, минимальное значение, В (нештатная ситуация сети)"),
    (139, "Изменение порога напряжения, время до срабатывания события, с(нештатная ситуация сети)"),
    (140, "Изменение порога напряжения, время задержки установки события PUSH, с (нештатная ситуация сети)"),
    (141,
     "Изменение порога напряжения по обратной последовательности, максимальное значение, В (нештатная ситуация сети)"),
    (142,
     "Изменение порога напряжения по обратной последовательности, время до срабатывания события, с (нештатная ситуация сети)"),
    (143,
     "Изменение порога напряжения по обратной последовательности, время задержки установки события PUSH, с (нештатная ситуация сети)"),
    (144, "Обжатие электронных пломб"),
    (145, "Очистка фиксации событий воздействия магнитного и/или ВЧ поля"),
    (146, "Изменение часового пояса"),
    (147, "Изменение последовательности вывода на ЖКИ в режиме «Автопрокрутка»"),
    (148, "Изменение последовательности вывода на ЖКИ в режиме «По кнопке»"),
    (149, "Изменение уровня лимита по току"),
    (150, "Изменение уровня лимита по напряжению"),
    (151, "Номер аварийного тарифа"),
    (152, "Настройка индикации, время неактивности кнопок"),
    (153, "Условие выдачи Push для 0.0.25.9.0.255"),
    (154, "Условие выдачи Push для 0.1.25.9.0.255"),
    (155, "Условие выдачи Push для 0.2.25.9.0.255"),
    (156, "Изменение настроек фильтра инициативного выхода"),
    (157, "Изменение настроек инициативного выхода №2"),
    (158, "Изменение настроек инициативного выхода №3"),
    (1024, "Изменение размера информационного поля на передачу (оптопорт)"),
    (1025, "Изменение размера информационного поля на передачу (RS)"),
    (1026, "Изменение размера информационного поля на передачу (модуль связи)"),
    (1027, "Изменение размера информационного поля на прием (оптопорт)"),
    (1028, "Изменение размера информационного поля на прием (RS)"),
    (1029, "Изменение размера информационного поля на прием (модуль связи)"),
    (1030, "Изменение настроек пуш сообщений периодических, интервал 1"),
    (1031, "Изменение настроек пуш сообщений периодических, интервал 2"),
    (1032, "Изменение настроек защиты оптопорта"),
    (1033, "Изменение настроек защиты порта RS-485"),
    (1034, "Изменение настроек защиты порта модема"),
    (1035, "Сброс состояния защиты оптопорта"),
    (1036, "Сброс состояния защиты порта RS-485"),
    (1037, "Сброс состояния защиты порта модема"),
    (1040, "Настройка периодичности отправки пуш сообщений периодических, интервал 1"),
    (1041, "Настройка периодичности отправки пуш сообщений периодических, интервал 2")
]

EventSelfDiagCode = [
    (1, "Инициализация ПУ"),
    (2, "Измерительный блок - ошибка"),
    (3, "Измерительный блок - норма"),
    (4, "Вычислительный блок - ошибка"),
    (5, "Часы реального времени - ошибка"),
    (6, "Часы реального времени - норма"),
    (7, "Блок питания - ошибка"),
    (8, "Блок питания - норма"),
    (9, "Дисплей - ошибка"),
    (10, "Дисплей - норма"),
    (11, "Блок памяти - ошибка"),
    (12, "Блок памяти - норма"),
    (13, "Блок памяти программ - ошибка"),
    (14, "Блок памяти программ - норма"),
    (15, "Система тактирования ядра - ошибка"),
    (16, "Система тактирования ядра - норма"),
    (17, "Система тактирования часов - ошибка"),
    (18, "Система тактирования часов - норма"),
    (19, "Вычислительный блок — норма"),
    (129, "Аппаратный сброс часов реального времени"),
    (130, "Программный сброс часов реального времени"),
    (131, "Сброс микроконтроллера при просадке напряжения"),
    (132, "Сброс микроконтроллера сторожевым таймером")
]

EventExternalInfluenceCode = [
    (1, "Магнитное поле - начало"),
    (2, "Магнитное поле - окончание"),
    (3, "Срабатывание электронной пломбы крышки клеммников - открытие"),
    (4, "Срабатывание электронной пломбы корпуса - открытие"),
    (5, "Срабатывание электронной пломбы внешнего датчика"),
    (6, "Воздействие ВЧ поля - начало"),
    (7, "Воздействие ВЧ поля- окончание"),
    (103, "Срабатывание электронной пломбы крышки клеммников - закрытие"),
    (104, "Срабатывание электронной пломбы корпуса - закрытие")
]

EventTangentCode = [(1, "Threshold exceeded - start"), (2, "Threshold exceeded - end")]

EventQualityLog = [(1, "Снижение напряжения более, чем на 10%"),
                   (2, "Резерв"),
                   (4, "Резерв"),
                   (8, "Повышение напряжения более, чем на 10%"),
                   (16, "Снижение частоты более, чем на 0,4 Гц"),
                   (32, "Снижение частоты более, чем на 0,2 Гц"),
                   (48, "Снижение частоты более, чем на 0,2 Гц и на 0,4"),
                   (64, "Увеличение частоты более, чем на 0,2 Гц"),
                   (128, "Увеличение частоты более, чем на 0,4 Гц"),
                   (256, "Резерв"),
                   (512, "Резерв"),
                   (1024, "Резерв"),
                   (2048, "Резерв"),
                   (4096, "Резерв"),
                   (8192, "Резерв"),
                   (16384, "Снижение частоты более, чем на заданный порог"),
                   (32768, "Увеличение частоты более, чем на заданный порог")]

EventPowerCode = [
    (0, "Normal power state"),
    (1, "Exceeding the specified level of active power on the integration interval 2"),
    (2, "Exceeding the specified level of active power on the integration interval 2 during peak load hours")]

TemperatureJournalEvents = [(1, "Начало выхода температуры за верхнюю границу"),
                            (2, "Окончание выхода температуры за верхнюю границу"),
                            (3, "Начало выхода температуры за нижнюю границу"),
                            (4, "Окончание выхода температуры за нижнюю границу")]

PositionRelay = [(0, "Блокировка выключена (управление реле разрешено)"),
                 (1, "Блокировка включена(управление реле запрещено)")]

EventAccessCode = [(1, "Попытка несанкционированного доступа(интерфейс)"),
                   (2, "Нарушение требований протокола"),
                   (3, "Блокировка по превышению количества неправильных паролей"),
                   (4, "Ошибка верификации прошивки")]


def create_sheet_in_excel_file(data, writer, sheet_name, reader, sample):
    try:
        data(reader, sample).to_excel(writer, sheet_name=sheet_name, index=False)
        sheet1 = writer.sheets[sheet_name]
        sheet1.set_column('A:A', 23)
        sheet1.set_column('B:B', 60)
        sheet1.set_column('C:U', 40)
    except Exception as e:
        print(f"Ошибка {e} при создании excel файла или считывании '{sheet_name}'")


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def is_valid_date_for_anal(date_string):
    try:
        datetime.strptime(date_string, "%d.%m.%y %H:%M:%S")
        return True
    except ValueError:
        return False


def sample_config(flag, start, end):
    if flag:
        return [start, end]
    else:
        return ['N']


def parse_log_name(log_name):
    name = log_name.split()[0]
    if name == 'Журнал':
        new_log_name = log_name.replace(" ", "е ", 1)
    elif name == 'Профиль':
        new_log_name = log_name.replace("ь", "е", 1)
    elif name == 'Срез':
        new_log_name = log_name.replace(" ", "е ", 1)
    else:
        new_log_name = log_name.replace("ый", "ом", 1).replace("ь", "е", 1)
    return new_log_name


def range_by_date(reader, data, sample):
    if sample[0] not in ['N', 'n']:
        start = GXDateTime(f'{sample[0]} 00:00:00', "%d.%m.%Y %H:%M:%S")
        end = GXDateTime(f'{sample[1]} 23:59:59', "%d.%m.%Y %H:%M:%S")
        logs = reader.read_rows_by_range(data, start, end)
    else:
        logs = reader.read(data, 2)
    return logs


def ref_date_time(date_time):
    try:
        res = datetime.strptime(str(date_time), "%m/%d/%y %H:%M:%S")
        res = res.strftime("%d.%m.%y %H:%M:%S")
        return res
    except Exception as e:
        return "FFFFFFFF"


def parsing_port_number(port_number):
    data_list = list(bin(port_number).replace('0b', ''))
    data_list.reverse()
    for i in range(len(data_list), 8):
        data_list.append('0')
    data_list.reverse()
    data_str_first = ''.join(data_list[5:])
    data_str_second = ''.join(data_list[:5])
    for z in range(len(communication_channel_number)):
        if data_str_first == communication_channel_number[z][0]:
            res_1 = communication_channel_number[z][1]
            break
    else:
        res_1 = f'{data_str_first}-неописанный код'
    for y in range(len(interface_type)):
        if data_str_second == interface_type[y][0]:
            res_2 = interface_type[y][1]
            break
    else:
        res_2 = f'{data_str_second} - неописанный код'
    return f'№ порта:[{port_number}];№ канала:[{res_1}];интерфейс:[{res_2}]'


communication_channel_number = [("000", "резерв"),
                                ("001", "Opto P1"),
                                ('010', "P2"),
                                ('011', "P3"),
                                ('100', "P4"),
                                ('101', "для других портов связи"),
                                ('110', "внутренняя причина"),
                                ('111', "Кнопки ПУ")]

interface_type = [("00000", "не определено"),
                  ("00001", "Opto"),
                  ("00010", "RS485"),
                  ("00011", "PLC"),
                  ("00100", "GSM"),
                  ("00101", "NBIO"),
                  ("00110", "Ethernet"),
                  ("00111", "RF"),
                  ("01000", "LoRa"),
                  ("01001", "Wi-Fi"),
                  ("01010", "Bluetooth"),
                  ("01011", "не определено")]

client_address = [(16, "Публичный клиент"),
                  (32, "Считыватель показаний"),
                  (48, "Конфигуратор")]


def voltage_with_scalar(voltage):
    return voltage * 0.001


def hertz_with_scalar(hertz):
    return hertz * 0.001


def current_with_scalar(current):
    return current * 0.001


def power_with_scalar(power):
    return power * 0.001
