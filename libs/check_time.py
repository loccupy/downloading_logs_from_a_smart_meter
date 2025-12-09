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

    # def get_duration(self, start_key: str, end_key: str) -> float:
    #     """Получить разницу во времени между двумя метками (в секундах)"""
    #     start = self.all_time.get(start_key)
    #     end = self.all_time.get(end_key)
    #
    #     if not start:
    #         raise KeyError(f"Нет времени с ключом '{start_key}'")
    #     if not end:
    #         raise KeyError(f"Нет времени с ключом '{end_key}'")
    #
    #     return (end - start).total_seconds()
