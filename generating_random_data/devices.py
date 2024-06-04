import numpy as np


def generate_devices(total_number_of_devices, devices_distribution):
    '''
    devices_distribution = {
        'workstation': 0.93,
        'normal_server': 0.055,
        'sensitive_server': 0.015,
    }
    :return:
    '''
    devices = []
    sum_of_propotions = sunm(devices_distribution.values)
    for device_type, propotion_of_device in devices_distribution:
        devices += [device_type] * int(propotion_of_device / sum_of_propotions)
    return devices


devices = generate_devices(config.total_number_of_devices, config.devices_distribution)
