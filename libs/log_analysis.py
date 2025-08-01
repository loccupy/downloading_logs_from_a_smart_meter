import datetime
from datetime import timedelta

from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill

from libs.Utils import is_valid_date_for_anal

pink_fill = PatternFill(start_color='FFCC99FF',
                        end_color='FFCC99FF',
                        fill_type='solid')


# считать excel
def read_excel(path_to_file):
    try:
        sheets = load_workbook(path_to_file)

        # analysis_correct_date_ref(sheets, 'Журнал напряжения')
        # time_ordering_analysis_ref(sheets, 'Журнал коммуникационных событий')
        # ipu_working_hours_ref(sheets, 'Журнал напряжения')

        sheets.save(path_to_file)

    except Exception as e:
        raise


# анализирует "Время фиксации записи" на предмет невалидных дат, FFF-ок
def analysis_correct_date_ref(sheets, log_name):
    try:
        sheet = sheets[log_name]
        column = None
        column_names = [cell for cell in sheet[1]]
        # Получаем номер столбца по названию
        for i in column_names:
            if i.value == 'Время фиксации записи':
                column = i.column

        # Проверяем все значения столбца и, в случае совпадения условия, перекрашиваем ячейку
        for row in sheet.iter_rows(min_row=2, min_col=column, max_col=column):
            # Получаем ячейку
            cell = row[0]
            # Проверяем условие
            if not is_valid_date_for_anal(str(cell.value)):
                cell.fill = pink_fill
                print(f"Невалидная дата в строчке {cell.row} в '{log_name.replace(" ", "е ", 1)}'")
    except Exception as e:
        raise


# проверяет очередность валидных дат в столбце "Время фиксации записи"
def time_ordering_analysis_ref(sheets, log_name):
    format_dt = "%d.%m.%y %H:%M:%S"
    try:
        sheet = sheets[log_name]
        column = None
        column_names = [cell for cell in sheet[1]]
        # Получаем номер столбца по названию
        for i in column_names:
            if i.value == 'Время фиксации записи':
                column = i.column
                break

        # Проверяем все значения столбца и, в случае совпадения условия, перекрашиваем ячейку
        for i, row in enumerate(sheet.iter_rows(min_row=2, min_col=column, max_col=column)):
            # Получаем и сохраняем первую ячейку + пропускаем ее для обработки
            if i == 0:
                cell_0 = row[0]
                continue

            # Получаем ячейку
            cell_1 = row[0]

            if is_valid_date_for_anal(str(cell_0.value)) and is_valid_date_for_anal(str(cell_1.value)):
                # Проверяем условие
                if ((datetime.datetime.strptime(str(cell_0.value), format_dt) -
                     datetime.datetime.strptime(str(cell_1.value), format_dt) > timedelta())):
                    cell_0.fill = pink_fill
                    cell_1.fill = pink_fill

                    print(
                        f"Некорректная последовательность фиксации записи в строчках {cell_0.row}-{cell_1.row} в"
                        f" '{log_name.replace(" ", "е ", 1)}'")
            cell_0 = row[0]
    except Exception as e:
        raise


# Проверяет последовательность значений в столбце "Время работы ИПУ"
def ipu_working_hours_ref(sheets, log_name):
    try:
        sheet = sheets[log_name]
        column = None
        column_names = [cell for cell in sheet[1]]
        # Получаем номер столбца по названию
        for i in column_names:
            if i.value == 'Время работы ПУ':
                column = i.column
                break

        # Проверяем все значения столбца и, в случае совпадения условия, перекрашиваем ячейку
        for i, row in enumerate(sheet.iter_rows(min_row=2, min_col=column, max_col=column)):
            # Получаем и сохраняем первую ячейку + пропускаем ее для обработки
            if i == 0:
                cell_0 = row[0]
                continue

            # Получаем ячейку
            cell_1 = row[0]
            res = int(cell_1.value) - int(cell_0.value)

            # Проверяем условие
            if res <= 0:
                cell_0.fill = pink_fill
                cell_1.fill = pink_fill

                print(f"Некорректная последовательность 'Время работы ПУ' в строчках {cell_0.row}-{cell_1.row} в"
                      f" '{log_name.replace(" ", "е ", 1)}'")

            cell_0 = row[0]

    except Exception as e:
        raise e
