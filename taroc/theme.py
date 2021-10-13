DEF_VALUE = 'white'
DEF_LABEL = 'bright_green'
DEF_GREYED_OUT = 'bright_black'
DEF_WARNING = 'bright_red'
DEF_ERROR = 'bright_red'
DEF_PANEL_BORDER = 'bright_cyan'

DEF_SPINNER = 'bold green'
DEF_SPINNER_TEXT = 'bold green'

DEF_HOSTS_PANEL_TITLE = DEF_PANEL_BORDER
DEF_HOSTS_PANEL_BORDER = DEF_PANEL_BORDER
DEF_HOSTS_PANEL_NAMES = DEF_LABEL
DEF_HOSTS_PANEL_VALUES = DEF_VALUE

DEF_JOBS_PANEL_TITLE = DEF_PANEL_BORDER
DEF_JOBS_PANEL_BORDER = DEF_PANEL_BORDER
DEF_JOBS_PANEL_NAMES = DEF_LABEL
DEF_JOBS_PANEL_VALUES = DEF_VALUE

greyed_out = DEF_GREYED_OUT

spinner = DEF_SPINNER
spinner_text = DEF_SPINNER_TEXT

progress_status = DEF_VALUE

hosts_panel_title = DEF_HOSTS_PANEL_TITLE
hosts_panel_border = DEF_HOSTS_PANEL_BORDER
hosts_panel_successful_name = DEF_HOSTS_PANEL_NAMES
hosts_panel_successful_value = DEF_HOSTS_PANEL_VALUES
hosts_panel_failed_name = DEF_GREYED_OUT
hosts_panel_failed_value = DEF_GREYED_OUT
hosts_panel_failed_positive_name = DEF_ERROR
hosts_panel_failed_positive_value = DEF_ERROR

jobs_panel_title = DEF_JOBS_PANEL_TITLE
jobs_panel_border = DEF_JOBS_PANEL_BORDER
jobs_panel_instances_name = DEF_JOBS_PANEL_NAMES
jobs_panel_instances_value = DEF_JOBS_PANEL_VALUES
jobs_panel_warning_name = DEF_GREYED_OUT
jobs_panel_warning_value = DEF_GREYED_OUT
jobs_panel_warning_positive_name = DEF_WARNING
jobs_panel_warning_positive_value = DEF_WARNING


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
