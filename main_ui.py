import sys

from PyQt5.QtWidgets import QApplication

from libs.connect import connect_with_ip
from libs.ui_for_log_loader import UiForLogLoader


def start_ui():
    app = QApplication(sys.argv)
    ex = UiForLogLoader()
    ex.show()
    sys.exit(app.exec_())


def debug():
    # file_name = "Serial_240101000000000_30.07.25_12.36.41.xlsx"
    # current_log_analysis(file_name)
    # self_diagnosis_log_analysis(file_name)
    # network_quality_log_analysis(file_name)
    # voltage_log_analysis(file_name)
    # communication_events_log_analysis(file_name)
    # access_control_log_analysis(file_name)
    # data_correction_log_analysis(file_name)
    # time_correction_log_analysis(file_name)
    # battery_charge_status_log_analysis(file_name)
    # power_log_analysis(file_name)
    # tangent_excess_log_analysis(file_name)
    # tangent_output_log_analysis(file_name)
    # network_quality_for_period_log_analysis(file_name)
    # on_and_off_log_analysis(file_name)
    # external_influences_log_analysis(file_name)
    # sampling_status_log_analysis(file_name)
    # sampling_status_log_analysis(file_name)
    # month_profile_log_analysis(file_name)
    # energy_profile_for_1_log_analysis(file_name)
    # energy_profile_for_2_log_analysis(file_name)
    # artur_profile_log_analysis(file_name)
    reader = connect_with_ip()
    print(reader.deviceType)
    reader.close()


if __name__ == "__main__":
    start_ui()
