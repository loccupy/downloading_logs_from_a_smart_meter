from datetime import datetime


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
