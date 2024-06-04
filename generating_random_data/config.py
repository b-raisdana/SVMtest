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

normal_starters = 0.8  #
normal_starters_start_at_shift_start = 0.2  #
normal_starters_start_at_shift_start_late_start_tolerance_mins = 20  #
normal_early_start_mins = 30
normal_late_start_mins = 45
absence_rate = 0.1

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
    '''
    role_shift_varieties = {
        role:{
            shift: ({start, end}, population)
        },
    }
    '''
    'Admin': {
        'day': (general_shifts['standard'], 0.9),
        'night': ({
                      'start': 17,
                      'end': 8,
                  }, 0.1),
    },
    'Support Day': {
        'day': (general_shifts['standard'], 0.55),
    },
    'Support Shift': {
        'morning': (general_shifts['morning'], 0.15),
        'afternoon': (general_shifts['afternoon'], 0.15),
        'night': (general_shifts['night'], 0.15),
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

login_rates = {
    'Admin': {
        'other_workstation': 5,
        'normal_server': 4,
        'sensitive_server': 1,
        'min_inter_login_mins': min_inter_login_mins,
    },
    'Support Day': {
        'other_workstation': 5,
        'normal_server': 4,
        'sensitive_server': 0,
        'min_inter_login_mins': min_inter_login_mins,
    },
    'Support Shift': {
        'other_workstation': 5,
        'normal_server': 4,
        'sensitive_server': 0,
        'min_inter_login_mins': min_inter_login_mins,
    },
    'Regular Shift': {
        'other_workstation': 2,
        'normal_server': 2,
        'sensitive_server': 0,
        'min_inter_login_mins': 30,
    },
    'Regular Day': {
        'other_workstation': 2,
        'normal_server': 2,
        'sensitive_server': 0,
        'min_inter_login_mins': 30,
    }
}
login_normals = {
    'Admin': {
        'other_workstation': 0.10,
        'normal_server': 0.8,
        'sensitive_server': 0.5,
    },
    'Support Day': {
        'other_workstation': 0.5,
        'normal_server': 0.5,
        'sensitive_server': 0.5,
    },
    'Support Shift': {
        'other_workstation': 0.5,
        'normal_server': 0.5,
        'sensitive_server': 0.5,
    },
    'Regular Shift': {
        'other_workstation': 0.20,
        'normal_server': 0.8,
        'sensitive_server': 1,
    },
    'Regular Day': {
        'other_workstation': 0.10,
        'normal_server': 0.8,
        'sensitive_server': 0.5,
    }
}
devices_distribution = {
    'workstation': 0.93,
    'normal_server': 0.055,
    'sensitive_server': 0.015,
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
