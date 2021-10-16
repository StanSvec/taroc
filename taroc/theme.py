import sys

DEF_VALUE = 'white'
DEF_LABEL = 'bright_green'
DEF_GREYED_OUT = 'bright_black'
DEF_WARNING = 'red'
DEF_ERROR = 'bright_red'
DEF_PANEL_BORDER = 'bright_cyan'

DEF_SPINNER = 'bold green'
DEF_SPINNER_TEXT = 'bold green'

DEF_JOBS_TABLE_HOST = 'white'
DEF_JOBS_TABLE_JOB = 'bold white'
DEF_JOBS_TABLE_INSTANCE = 'bright_black'
DEF_JOBS_TABLE_CREATED = 'green'
DEF_JOBS_TABLE_TIME = 'green'
DEF_JOBS_TABLE_STATE_RUNNING = 'bright_cyan'
DEF_JOBS_TABLE_WARNING = DEF_WARNING
DEF_JOBS_TABLE_STATUS = 'bright_white'

value = DEF_VALUE
label = DEF_LABEL
greyed_out = DEF_GREYED_OUT
warning = DEF_WARNING
error = DEF_ERROR

spinner = DEF_SPINNER
spinner_text = DEF_SPINNER_TEXT

progress_status = value

panel_border = DEF_PANEL_BORDER

hosts_panel_title = panel_border
hosts_panel_border = panel_border
hosts_panel_successful_name = label
hosts_panel_successful_value = value
hosts_panel_failed_name = greyed_out
hosts_panel_failed_value = greyed_out
hosts_panel_failed_positive_name = error
hosts_panel_failed_positive_value = error

jobs_panel_title = panel_border
jobs_panel_border = panel_border
jobs_panel_instances_name = label
jobs_panel_instances_value = value
jobs_panel_warning_name = greyed_out
jobs_panel_warning_value = greyed_out
jobs_panel_warning_positive_name = warning
jobs_panel_warning_positive_value = warning

jobs_table_host = DEF_JOBS_TABLE_HOST
jobs_table_job = DEF_JOBS_TABLE_JOB
jobs_table_instance = DEF_JOBS_TABLE_INSTANCE
jobs_table_created = DEF_JOBS_TABLE_CREATED
jobs_table_time = DEF_JOBS_TABLE_TIME
jobs_table_state_running = DEF_JOBS_TABLE_STATE_RUNNING
jobs_table_warns = DEF_JOBS_TABLE_WARNING
jobs_table_status = DEF_JOBS_TABLE_STATUS


def hosts_panel_failed(failed_count):
    if failed_count:
        return hosts_panel_failed_positive_name, hosts_panel_failed_positive_value
    else:
        return hosts_panel_failed_name, hosts_panel_failed_value


def jobs_panel_warning(warning_count):
    if warning_count:
        return jobs_panel_warning_positive_name, jobs_panel_warning_positive_value
    else:
        return jobs_panel_warning_name, jobs_panel_warning_value


def set_variables(**kwargs):
    module = sys.modules[__name__]
    for name, value in kwargs.items():
        if not name[0].isalpha():
            raise ValueError(f"Invalid theme variable: {name}")
        if not hasattr(module, name):
            raise ValueError(f"Unknown theme variable: {name}")

        setattr(module, name, value)
