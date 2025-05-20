from time import sleep

from gurux.dlms.objects import GXDLMSData, GXDLMSHdlcSetup
from libs.GXDLMSReader import GXDLMSReader
from libs.GXSettings import GXSettings


def connecting(com):
    baud = int(input("Введите начальную скорость: "))
    address = int(input("Введите серийник: ")) + 16

    try:
        settings = GXSettings()
        settings.getParameters("COM", f"COM{com}", password='1234567898765432', authentication="High", serverAddress=address,
                               logicalAddress=1, clientAddress=48, baudRate=baud)
        settings.media.open()
        reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
        reader.initializeConnection()
        print("Установлено соединение для ускорения передачи данных")
        # меняем скорость
        data = GXDLMSData('0.0.96.12.4.255')
        # считываем номер порта
        val = reader.read(data, 2)

        if val == 9:
            print(f"Интерфейс >> ОПТОПОРТ")
        else:
            print(f"Интерфейс >> RS")

        # RS  - 0b10010, ОПТО - 0b1001
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
        reader.disconnect()
        settings.media.close()
        print("Разорвано соединение для ускорения передачи данных")
        # организуем новое подключение
        list_of_baud = {"5": 9600, "6": 19200, "9": 115200}
        baud = 0
        for i in list_of_baud.keys():
            if int(i) == new_speed:
                baud = list_of_baud.get(i)
        new_setting = GXSettings()
        new_setting.getParameters("COM", f"COM{com}", password='1234567898765432', authentication="High", serverAddress=address,
                                  logicalAddress=1, clientAddress=48, baudRate=baud)
        new_setting.media.open()
        new_reader = GXDLMSReader(new_setting.client, new_setting.media, new_setting.trace, new_setting.invocationCounter)
        # new_reader.initializeConnection()
        return new_reader
    except Exception as e:
        print(e.args)
        sleep(5)


