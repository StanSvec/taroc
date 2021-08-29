from importlib import resources

from taroc import util, cfg, paths

SSH_CONFIG_ENABLED = 'ssh_config.enabled'


def load_default():
    cns = util.read_yaml(resources.read_text('taroc.config', paths.CONFIG_FILE))
    _set_attributes(cns)


def load(config=None):
    config_path = util.expand_user(config) if config else paths.lookup_config_file()
    cns = util.read_yaml_file(config_path)
    _set_attributes(cns)


def _set_attributes(cns):
    cfg.ssh_config_enabled = cns.get(SSH_CONFIG_ENABLED, default=cfg.DEF_SSH_CONFIG_ENABLED, type_=bool)
