from datetime import datetime
from random import seed

import numpy as np

seed(42)
np.random.seed(42)

start_day = datetime(2023, 1, 1)
duration_weeks = 6
days_per_week = 7
duration_days = duration_weeks * days_per_week

employee_shift_change_rate = 0.05  #
# employee_shift_change_min_duration_days = 5#
# employee_shift_change_max_duration_days = 8#

employee_weekly_role_change_rate = 0.01  #
# employee_role_change_min_duration_days = 30#

# normal_starters = 0.8  #
# normal_starters_start_at_shift_start = 0.2  #
# normal_starters_start_at_shift_start_late_start_tolerance_mins = 20  #
self_workstation_first_login_rate = 0.95
self_workstation_next_login_rate = 0.5

login_norms = {
    'Regular User': {
        'roles': ['Regular Day', 'Regular Shift'],
        'target workgroups': ['Regular Day', 'Regular Shift'],
        'rates': {
            'other workstations': {
                'proportion': 0.2,
                'max': 2,
            },
            'normal server': {
                'proportion': 0.8,
                'max': 2,
            },
            'sensitive server': {
                'proportion': 0,
                'max': 2,
            },
        }
    },
    'Support': {
        'roles': ['Support Shift', 'Support Day'],
        'target workgroups': ['Regular Day', 'Regular Shift', 'Support Shift', 'Support Day'],
        'rates': {
            'other workstations': {
                'proportion': 0.5,
                'max': 5,
            },
            'normal server': {
                'proportion': 0.5,
                'max': 4,
            },
            'sensitive server': {
                'proportion': 0.5,
                'max': 1,
            },
        }
    },
    'Admin': {
        'roles': ['Admin'],
        'target workgroups': ['Regular Day', 'Regular Shift', 'Support Shift', 'Support Day', 'Admin'],
        'rates': {
            'other workstations': {
                'proportion': 0.1,
                'max': 5,
            },
            'normal server': {
                'proportion': 0.8,
                'max': 4,
            },
            'sensitive server': {
                'proportion': 0.5,
                'max': 2,
            },
        }
    },
}

normal_early_start_mins = 50
normal_late_start_mins = 50
absence_rate = (1 - 0.9)

general_shifts = {
    'morning': {
        'start': 8,
        'end': 16,
    },
    'afternoon': {
        'start': 16,
        'end': 0,
    },
    'night': {
        'start': 0,
        'end': 8,
    },
    'standard': {
        'start': 8,
        'end': 17,
    },
}  #
role_shift_varieties = {
    # role_shift_varieties = {
    #     role:{
    #         shift: ({start, end}, population)
    #     },
    # }
    'Admin': {
        'day': (general_shifts['standard'], 0.9),
        'night': ({
                      'start': 17,
                      'end': 8,
                  }, 0.1),
    },
    'Support Day': {
        'day': (general_shifts['standard'], 1),
    },
    'Support Shift': {
        'morning': (general_shifts['morning'], 0.33333),
        'afternoon': (general_shifts['afternoon'], 0.33333),
        'night': (general_shifts['night'], 0.33334),
    },
    'Regular Shift': {
        'morning': (general_shifts['morning'], 0.33333),
        'afternoon': (general_shifts['afternoon'], 0.33333),
        'night': (general_shifts['night'], 0.33334),
    },
    'Regular Day': {
        'day': (general_shifts['standard'], 1),
    }
}  #
min_inter_login_mins = 10

devices_distribution = {
    'workstation': 0.93,
    'normal server': 0.055,
    'sensitive server': 0.015,
}
total_number_of_devices = 200

num_groups = 10
total_employees = 150
roles = ['Regular Day', 'Regular Shift', 'Support Shift', 'Support Day', 'Admin', ]
all_shifts = ['morning', 'afternoon', 'night']
min_groups_for_roles = {
    'Admin': 1,
    'Support Day': 1,
    'Support Shift': 1,
    'Regular Shift': 2,
    'Regular Day': 2
}
role_distribution = {
    'Admin': 0.03,
    'Support Day': 0.05,
    'Support Shift': 0.05,
    'Regular Shift': 0.30,
    'Regular Day': 0.57
}
role_distribution_tolerance = 0.05
