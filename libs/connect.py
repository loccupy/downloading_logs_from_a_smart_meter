from libs.gurux.dlms.objects import GXDLMSData, GXDLMSHdlcSetup
from libs.GXDLMSReader import GXDLMSReader
from libs.GXSettings import GXSettings


def connect():
    settings = GXSettings()
    settings.getParameters("COM", f"COM11", password='1234567898765432', authentication="High",
                           serverAddress=16,
                           logicalAddress=1, clientAddress=48, baudRate=9600)
    settings.media.open()
    reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
    reader.initializeConnection()
    return reader


# def connecting(com, speed, serial, password):
#     # reader = 0
#     settings = GXSettings()
#     settings.getParameters("COM", f"COM{com}", password=password, authentication="High",
#                            serverAddress=serial + 16, logicalAddress=1, clientAddress=48, baudRate=speed)
#     if not settings.media.isOpen():
#         settings.media.open()
#     reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
#     try:
#
#         reader.initializeConnection()
#         print("Установлено соединение для ускорения передачи данных")
#         # меняем скорость
#         data = GXDLMSData('0.0.96.12.4.255')
#         # считываем номер порта
#         val = reader.read(data, 2)
#
#         if val == 9:
#             print(f"Интерфейс >> ОПТОПОРТ")
#         else:
#             print(f"Интерфейс >> RS")
#
#         # RS  - 0b10010, ОПТО - 0b1001
#         if val == 18:
#             speed = GXDLMSHdlcSetup('0.1.22.0.0.255')
#             old_speed = reader.read(speed, 2)
#             if old_speed == 5:
#                 speed.communicationSpeed = 9
#                 print("Ускоряем RS")
#                 reader.write(speed, 2)
#         else:
#             speed = GXDLMSHdlcSetup('0.0.22.0.0.255')
#             old_speed = reader.read(speed, 2)
#             if old_speed == 5:
#                 speed.communicationSpeed = 6
#                 print("Ускоряем ОПТОПОРТ")
#                 reader.write(speed, 2)
#         new_speed = reader.read(speed, 2)
#         reader.close()
#         # организуем новое подключение
#         list_of_baud = {"5": 9600, "6": 19200, "9": 115200}
#         baud = 0
#         for i in list_of_baud.keys():
#             if int(i) == new_speed:
#                 baud = list_of_baud.get(i)
#         # new_setting = GXSettings()
#         settings.getParameters("COM", f"COM{com}", password=password, authentication="High",
#                                serverAddress=serial + 16, logicalAddress=1, clientAddress=48, baudRate=baud)
#         settings.media.open()
#         new_reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
#         print("Создано ускоренное соединение")
#         # new_reader.initializeConnection()
#         return new_reader
#     except Exception as e:
#
#         print(f'Ошибка {e.args} при установке и настройке соединения')
#         raise Exception(f'Ошибка {e.args} при установке и настройке соединения')


def get_reader(com, password, serial_number, baud):
    settings = GXSettings()
    settings.getParameters("COM", f"COM{com}", password=password,
                           authentication="High", serverAddress=serial_number + 16,
                           logicalAddress=1, clientAddress=48, baudRate=baud)
    reader = GXDLMSReader(settings.client, settings.media,
                          settings.trace, settings.invocationCounter)

    return reader, settings


def speeding_up_the_connection(reader):
    try:
        # Определение типа интерфейса
        data = GXDLMSData('0.0.96.12.4.255')
        val = reader.read(data, 2)

        if val == 9:
            print("Интерфейс >> ОПТОПОРТ")
        else:
            print("Интерфейс >> RS")

        # Изменение скорости в зависимости от типа интерфейса
        if val == 18:
            speed = GXDLMSHdlcSetup('0.1.22.0.0.255')
            old_speed = reader.read(speed, 2)
            if old_speed == 5:
                speed.communicationSpeed = 9
                print("Ускоряем RS")
                reader.write(speed, 2)
        else:
            speed = GXDLMSHdlcSetup('0.0.22.0.0.255')
            old_speed = reader.read(speed, 2)
            if old_speed == 5:
                speed.communicationSpeed = 6
                print("Ускоряем ОПТОПОРТ")
                reader.write(speed, 2)

        new_speed = reader.read(speed, 2)
        # reader.close()

        # Определение новой скорости
        list_of_baud = {"5": 9600, "6": 19200, "9": 115200}
        baud = list_of_baud.get(str(new_speed), 0)
        print(f"Скорость для нового соединения >> {baud}")
        return baud
    except Exception as e:
        # print(f"Ошибка при ускорении соединения: {e}")
        raise


def setting_the_speed_to_default_values(reader):
    try:
        data_1 = GXDLMSHdlcSetup('0.0.22.0.0.255')
        data_2 = GXDLMSHdlcSetup('0.1.22.0.0.255')
        data_1.communicationSpeed = 5
        data_2.communicationSpeed = 5
        print("Устанавливаем скорость соединения на всех портах на 9600")
        reader.write(data_1, 2)
        reader.write(data_2, 2)
    except Exception as e:
        # print(f"Не удалось установить скорость на дефолтные значения c ошибкой {e.args}")
        raise


def init_connect(reader, settings):
    try:
        if not settings.media.isOpen():
            settings.media.open()

        reader.initializeConnection()
    except Exception as e:
        settings.media.close()
        # print(f"Ошибка при открытии соединения: {e}")
        raise


def close_reader(reader):
    try:
        reader.close()
    except Exception as e:
        # print(f"Ошибка при закрытии соединения: {e}")
        raise


# class Connecting:
#     def __init__(self, com, baud, serial_number, password):
#         self.com = com
#         self.baud = baud
#         self.serial_number = serial_number
#         self.password = password
#         # self._reader = None
#         # self.settings = GXSettings()
#         # self.settings.getParameters("COM", f"COM{com}", password=password,
#         #                             authentication="High", serverAddress=serial_number + 16,
#         #                             logicalAddress=1, clientAddress=48, baudRate=baud)
#
#     # def __enter__(self):
#     #     """Метод для использования с конструкцией with"""
#     #     self._reader = self.get_reader()
#     #     self.init_connect()
#     #     return self
#     #
#     # def __exit__(self, exc_type, exc_value, traceback):
#     #     """Гарантированное закрытие соединения"""
#     #     self.close_reader()
#     #
#     # def __del__(self):
#     #     """Деструктор для гарантированного закрытия соединения"""
#     #     self.close_reader()
#
#     def get_connection(self):
#         try:
#             get_reader()
#             init_connect()
#             return self._reader
#         except Exception as e:
#             raise Exception(f"Ошибка при получении соединения:{e}")
