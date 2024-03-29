"""
https://rich.readthedocs.io/en/stable/appendix/colors.html
"""

from taroc.ref import RefValue, StaticRefValueSupport


class Theme(metaclass=StaticRefValueSupport):
    value = RefValue('white')
    label = RefValue('bright_white')
    greyed_out = RefValue('bright_black')
    warning = RefValue('red')
    error = RefValue('bright_red')

    progress_bar_complete = 'bar.complete'
    progress_bar_finished = 'spring_green1'

    spinner = RefValue('bold white')
    spinner_text = RefValue(spinner)

    panel_border = RefValue('bright_cyan')

    state_running = RefValue('bright_cyan')

    hosts_panel_title = RefValue(panel_border)
    hosts_panel_border = RefValue(panel_border)
    hosts_panel_progress_label = RefValue(label)
    hosts_panel_progress_status = RefValue(value)
    hosts_panel_progress_elapsed = RefValue(value)
    hosts_panel_successful_name = RefValue(label)
    hosts_panel_successful_value = RefValue(value)
    hosts_panel_failed_name = RefValue(greyed_out)
    hosts_panel_failed_value = RefValue(greyed_out)
    hosts_panel_failed_positive_name = RefValue(error)
    hosts_panel_failed_positive_value = RefValue(error)

    jobs_panel_title = RefValue(panel_border)
    jobs_panel_border = RefValue(panel_border)
    jobs_panel_instances_name = RefValue(label)
    jobs_panel_instances_value = RefValue(value)
    jobs_panel_warning_name = RefValue(greyed_out)
    jobs_panel_warning_value = RefValue(greyed_out)
    jobs_panel_warning_positive_name = RefValue(warning)
    jobs_panel_warning_positive_value = RefValue(warning)

    jobs_table_header = 'table.header'
    jobs_table_host = 'white'
    jobs_table_job = 'bold white'
    jobs_table_instance = 'bright_black'
    jobs_table_created = 'white'
    jobs_table_time = 'white'
    jobs_table_state_running = RefValue(state_running)
    jobs_table_warns = RefValue(warning)
    jobs_table_status = 'bright_white'
    jobs_table_border = 'bright_cyan'

    @staticmethod
    def hosts_panel_failed(failed_count):
        if failed_count:
            return Theme.hosts_panel_failed_positive_name, Theme.hosts_panel_failed_positive_value
        else:
            return Theme.hosts_panel_failed_name, Theme.hosts_panel_failed_value

    @staticmethod
    def jobs_panel_warning(warning_count):
        if warning_count:
            return Theme.jobs_panel_warning_positive_name, Theme.jobs_panel_warning_positive_value
        else:
            return Theme.jobs_panel_warning_name, Theme.jobs_panel_warning_value

    @classmethod
    def set_variables(cls, **kwargs):
        for name, val in kwargs.items():
            if not name[0].isalpha():
                raise ValueError(f"Invalid theme variable: {name}")
            if not hasattr(cls, name):
                raise ValueError(f"Unknown theme variable: {name}")

            setattr(cls, name, val)
