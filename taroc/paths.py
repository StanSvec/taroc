from pathlib import Path

from xdg import BaseDirectory

CONFIG_FILE = 'taroc.yaml'


def lookup_config_file():
    return lookup_file_in_config_path(CONFIG_FILE)


def lookup_file_in_config_path(file) -> Path:
    """Returns config found in the search path
    :return: config file path
    :raise FileNotFoundError: when config lookup failed
    """
    cwd_path = Path.cwd() / file
    if cwd_path.exists():
        return cwd_path

    cfg_path = BaseDirectory.load_first_config('taro', file)
    if not cfg_path:
        raise FileNotFoundError(f'Config file {file} not found in the search path: '
                                + ", ".join([str(dir_) for dir_ in [Path.cwd()] + BaseDirectory.xdg_config_dirs]))

    return Path(cfg_path)
