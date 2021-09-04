from taroc import cfgfile, paths, cfg, sshclient


def load_defaults(**kwargs):
    cfgfile.load_default()
    setup(**kwargs)


def load_config(config=None, **kwargs):
    cfgfile.load(config)
    setup(**kwargs)


def setup(**kwargs):
    cfg.set_variables(**kwargs)


def ps(*hosts):
    return sshclient.execute('ps -f json', *hosts)
