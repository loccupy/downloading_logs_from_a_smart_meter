class Config:
    def __init__(self, com, serial_number, passw, flag_temperature, flag_viborka, first_date, second_date):
        self.com_meter = com
        # self.port_number = port_number
        self.serial_number = serial_number
        self.passw = passw
        self.flag_temperature = flag_temperature
        self.flag_viborka = flag_viborka
        self.first_date = first_date
        self.second_date = second_date
        self.baud = 9600
