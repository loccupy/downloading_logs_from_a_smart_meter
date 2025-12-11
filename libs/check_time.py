from datetime import datetime

from libs.gurux.dlms.objects import GXDLMSClock
from libs.sending_message import message_in_out


def check_time(config, reader, time_for_check):
    try:
        if time_for_check.get_time(config.serial_number) is None:
            time_for_check.set_time(config.serial_number,
                                    datetime.strptime(str(reader.read(GXDLMSClock('0.0.1.0.0.255'), 2)),
                                                      "%m/%d/%y %H:%M:%S"))
            time_for_check.start_timer(config.serial_number)
            duration = 'Не рассчитывается на первом круге'
        else:
            current_time = datetime.strptime(str(reader.read(GXDLMSClock('0.0.1.0.0.255'), 2)), "%m/%d/%y %H:%M:%S")
            duration = (current_time - time_for_check.get_time(config.serial_number) -
                        time_for_check.get_timer(config.serial_number)).total_seconds()
            time_for_check.set_time(config.serial_number, current_time)
            time_for_check.start_timer(config.serial_number)

        return duration
    except Exception as e:
        message_in_out(f'Ошибка при проверке расхождения времени >> {e}')
        raise


class CheckTime:
    def __init__(self, list_of_serial):
        self.all_timer = {}
        self.all_time = {}
        for i in list_of_serial:
            self.all_time[i] = None

    def set_time(self, key, data):
        """Сохранить указанное время по ключу"""
        self.all_time[key] = data

    def get_time(self, key: str):
        return self.all_time.get(key)

    def start_timer(self, key):
        time = datetime.now()
        self.all_timer[key] = time

    def get_timer(self, key):
        time = self.all_timer[key]
        diff = datetime.now() - time
        return diff
