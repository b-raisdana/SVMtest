import pandas as pd

from generating_random_data import config

daily_timesheet = pd.read_csv("shift_employees.csv", parse_dates=['Day'])

# def generate_devices(total_number_of_devices, devices_distribution):
#     '''
#     devices_distribution = {
#         'workstation': 0.93,
#         'normal_server': 0.055,
#         'sensitive_server': 0.015,
#     }
#     :return:
#     '''
#     _devices = []
#     sum_of_proportions = sum(devices_distribution.values())
#     for device_type, proportion_of_device in devices_distribution.items():
#         _devices += [device_type] * int(total_number_of_devices * proportion_of_device / sum_of_proportions)
#     return _devices
#
#
# devices = generate_devices(config.total_number_of_devices, config.devices_distribution)

devices_df = pd.DataFrame(devices, columns=['Device Type'])
devices_df.to_csv('devices.csv')
