import configparser

from taroc import paths
from taroc.theme import Theme


def load_default():
    load_theme(paths.DEFAULT_THEME)


def load_theme(theme_file):
    obj_to_vars = read_file(paths.lookup_file_in_config_path(theme_file))
    all_vars = _flatten(obj_to_vars)
    Theme.set_variables(**all_vars)


def read_file(theme_file) -> dict[str, dict[str, str]]:
    """Returns dictionary of {name to value} for theme variables
    :param theme_file: ini file with sections representing themed objects
    :return: theme name to value dict
    :raise FileNotFoundError: when theme file cannot be found
    """
    theme_file_path = paths.lookup_file_in_config_path(theme_file)
    config = configparser.ConfigParser(allow_no_value=False)
    config.read(theme_file_path)

    return {obj_section.lower(): dict(config[obj_section]) for obj_section in config}


def _flatten(obj_to_vars):
    """
    Object section is prefixed to variable names except the `general` section
    [general]
    warning = red
        >> translates to: warning = red

    [panel]
    title = white
        >> translates to: panel_title = white
    """

    all_vars = dict()
    for obj, vars_ in obj_to_vars.items():
        if obj == 'general':
            all_vars.update(vars_)
        else:
            all_vars.update({f"{obj}_{k}": v for k, v in vars_.items()})
    return all_vars
