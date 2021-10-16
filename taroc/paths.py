from pathlib import Path

from xdg import BaseDirectory

CONFIG_DIR = 'taroc'
CONFIG_FILE = 'taroc.yaml'
SSH_HOSTS = 'ssh.hosts'
DEFAULT_THEME = 'turtles.theme'


def lookup_config_file():
    return lookup_file_in_config_path(CONFIG_FILE)


def lookup_default_theme_file():
    return lookup_file_in_config_path(DEFAULT_THEME)


def lookup_file_in_config_path(file) -> Path:
    """Returns config found in the search path
    :return: config file path
    :raise FileNotFoundError: when config lookup failed
    """
    cwd_path = Path.cwd() / file
    if cwd_path.exists():
        return cwd_path

    cfg_path = BaseDirectory.load_first_config(CONFIG_DIR, file)
    if not cfg_path:
        raise FileNotFoundError(f'Config file {file} not found in the search path: '
                                + ", ".join([str(dir_) for dir_ in [Path.cwd()] + _xdg_taro_config_paths()]))

    return Path(cfg_path)


def _xdg_taro_config_paths():
    return [Path(xdg_dir) / CONFIG_DIR for xdg_dir in BaseDirectory.xdg_config_dirs]
