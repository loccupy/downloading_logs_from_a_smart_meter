from datetime import datetime


class CheckSelfDiagnostic:
    def __init__(self, list_of_serial):
        self.start_time = {}
        self.end_time = {}
        for i in list_of_serial:
            self.start_time[i] = None
            self.end_time[i] = None

    def set_start_time(self, key, start_time):
        self.start_time[key] = start_time

    def set_end_time(self, key, end_time):
        self.end_time[key] = end_time

    def get_start_time(self, key: str):
        return self.start_time.get(key)

    def get_end_time(self, key: str):
        return self.end_time.get(key)
    #
    # def start_timer(self, key):
    #     time = datetime.now()
    #     self.all_timer[key] = time
    #
    # def get_timer(self, key):
    #     time = self.all_timer[key]
    #     diff = datetime.now() - time
    #     return diff
    #