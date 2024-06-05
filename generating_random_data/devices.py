import pandas as pd

from generating_random_data import config

daily_timesheet = pd.read_csv("shift_employees.csv", parse_dates=['Day'])

# def generate_devices(total_number_of_devices, devices_distribution):
#     '''
#     devices_distribution = {
#         'workstation': 0.93,
#         'normal server': 0.055,
#         'sensitive server': 0.015,
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
devices = pd.DataFrame()


def generate_workstations(_daily_timesheet):
    users_in_groups = \
        _daily_timesheet.groupby(['UserID', 'GroupID', 'Role']).first().reset_index()[['UserID', 'GroupID', 'Role']]
    workstations = users_in_groups
    workstations['Device Type'] = 'workstation'
    total_number_of_devices = round(len(workstations) / config.devices_distribution['workstation'])
    number_of_normal_server = round(total_number_of_devices * config.devices_distribution['normal server'])
    normal_servers = pd.DataFrame([[500, 'normal server']] * number_of_normal_server,
                                  columns=['GroupID', 'Device Type'])
    number_of_sensitive_server = round(total_number_of_devices * config.devices_distribution['sensitive server'])
    sensitive_servers = pd.DataFrame([[500, 'sensitive server']] * number_of_sensitive_server,
                                     columns=['GroupID', 'Device Type'])
    _devices = pd.concat([workstations, normal_servers, sensitive_servers])
    _devices['DeviceID'] = range(len(_devices))
    return _devices


devices_df = generate_workstations(daily_timesheet)
devices_df.rename(columns={
    'UserID': 'Device UserID',
    'GroupID': 'Device GroupID',
    'Role': 'Device Role',
}, inplace=True)
# devices_df = pd.DataFrame(devices, columns=['Device Type'])
devices_df.to_csv('devices.csv', index=False)
