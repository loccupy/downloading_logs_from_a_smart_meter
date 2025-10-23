import time

from libs.gurux.dlms.objects import GXDLMSData, GXDLMSHdlcSetup
from libs.GXDLMSReader import GXDLMSReader
from libs.GXSettings import GXSettings


def connect_with_ip():
    settings = GXSettings()
    settings.getParameters("85.141.70.251", "6603", password='1234567898765432', authentication="High",
                           serverAddress=18,
                           logicalAddress=1, clientAddress=48, baudRate=9600)
    settings.media.open()
    reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
    reader.initializeConnection()
    return reader


def connect():
    settings = GXSettings()
    settings.getParameters("COM", f"COM11", password='1234567898765432', authentication="High",
                           serverAddress=16,
                           logicalAddress=1, clientAddress=48, baudRate=9600)
    settings.media.open()
    reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
    reader.initializeConnection()
    return reader


def get_reader(com, password, serial_number, baud):
    settings = GXSettings()
    settings.getParameters("COM", f"COM{com}", password=password,
                           authentication="High", serverAddress=serial_number + 16,
                           logicalAddress=1, clientAddress=48, baudRate=baud)
    reader = GXDLMSReader(settings.client, settings.media,
                          settings.trace, settings.invocationCounter)

    return reader, settings


def get_reader_with_ip(ip, password, serial_number, port):
    settings = GXSettings()
    settings.getParameters(ip, port, password=password, authentication="High",
                           serverAddress=serial_number + 16,
                           logicalAddress=1, clientAddress=48, baudRate=9600)
    reader = GXDLMSReader(settings.client, settings.media,
                          settings.trace, settings.invocationCounter)

    return reader, settings


def speeding_up_the_connection(config, attempt=1, max_attempts=5):
    print(f"\n   Увеличиваем скорость передачи данных...")
    reader_list = get_reader(
        config.com_meter,
        config.passw,
        config.serial_number,
        config.baud
    )
    reader = reader_list[0]
    settings = reader_list[1]
    try:
        init_connect(reader, settings)

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
                print("Ускоряем RS до 115200")
                reader.write(speed, 2)
                config.baud = 115200
        else:
            speed = GXDLMSHdlcSetup('0.0.22.0.0.255')
            old_speed = reader.read(speed, 2)
            if old_speed == 5:
                speed.communicationSpeed = 6
                print("Ускоряем ОПТОПОРТ до 19200")
                reader.write(speed, 2)
                config.baud = 19200

        new_speed = reader.read(speed, 2)
        # reader.close()

        # Определение новой скорости
        list_of_baud = {"5": 9600, "6": 19200, "9": 115200}
        baud = list_of_baud.get(str(new_speed), 0)
        if val == 18:
            print(f"Скорость для нового соединения по RS >> {baud}")
        else:
            print(f"Скорость для нового соединения по ОПТОПОРТу >> {baud}")

        close_reader(reader)
        return baud
    except Exception as e:
        # print(f"Ошибка при ускорении соединения: {e}")
        # raise
        close_reader(reader)
        if attempt < max_attempts:
            print(f"Попытка подключения для ускорения {attempt} из {max_attempts} не удалась: {e}")
            print(f"Повторяем попытку через 2 секунды...")
            time.sleep(2)  # Ждем 2 секунды перед повторной попыткой
            return speeding_up_the_connection(
                config,
                attempt + 1,
                max_attempts
            )
        else:
            print(f"Превышено количество попыток подключения для ускорения (5). Ошибка: {e}")
            raise
            # raise  # Перебрасываем исключение после всех попыток


def setting_the_speed_to_default_values(config, attempt=1, max_attempts=5):
    print(f"\n   Возвращаем скорость к дефолтному состоянию...")
    reader_list = get_reader(
        config.com_meter,
        config.passw,
        config.serial_number,
        config.baud
    )
    reader = reader_list[0]
    settings = reader_list[1]
    try:
        init_connect(reader, settings)

        # Определение типа интерфейса
        data = GXDLMSData('0.0.96.12.4.255')
        val = reader.read(data, 2)

        if val == 18:
            speed = GXDLMSHdlcSetup('0.1.22.0.0.255')
            old_speed = reader.read(speed, 2)
            if old_speed != 5:
                speed.communicationSpeed = 5
                print("Устанавливаем скорость соединения на RS на 9600...")
                reader.write(speed, 2)
                config.baud = 9600
        else:
            speed = GXDLMSHdlcSetup('0.0.22.0.0.255')
            old_speed = reader.read(speed, 2)
            if old_speed != 5:
                speed.communicationSpeed = 5
                print("Устанавливаем скорость соединения ОПТОПОРТа на 9600...")
                reader.write(speed, 2)
                config.baud = 9600
        close_reader(reader)
        return None
    except Exception as e:
        close_reader(reader)
        # print(f"Не удалось установить скорость на дефолтные значения c ошибкой {e.args}")
        # raise
        if attempt < max_attempts:
            print(f"Попытка подключения для сброса скорости {attempt} из {max_attempts} не удалась: {e}")
            print(f"Повторяем попытку через 2 секунды...")
            time.sleep(2)  # Ждем 2 секунды перед повторной попыткой
            return setting_the_speed_to_default_values(
                config,
                attempt + 1,
                max_attempts
            )
        else:
            print(f"Превышено количество попыток подключения для сброса скорости (5). Ошибка: {e}")
            raise


def init_connect(reader, settings):
    try:
        if not settings.media.isOpen():
            settings.media.open()

        reader.initializeConnection()
    except Exception as e:
        reader.close()
        # print(f"Ошибка при открытии соединения: {e}")
        raise


def close_reader(reader):
    try:
        reader.close()
    except Exception as e:
        # print(f"Ошибка при закрытии соединения: {e}")
        raise
