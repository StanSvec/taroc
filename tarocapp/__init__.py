import taroc
from taroc import util
from tarocapp import cmd, cli


def main_cli():
    main(None)


def main(args):
    """Taro CLI app main function.

    Note: Configuration is setup before execution of all commands although not all commands require it.
          This practice increases safety (in regards with future extensions) and consistency.
          Performance impact is expected to be negligible.

    :param args: CLI arguments
    """
    args_ns = cli.parse_args(args)
    init_taroc(args_ns)
    cmd.run(args_ns)


def init_taroc(args):
    """Initialize taroc according to provided CLI arguments

    :param args: CLI arguments
    """
    config_vars = util.split_params(args.set) if args.set else {}  # Config variables and override values

    if getattr(args, 'config', None):
        taroc.load_config(args.config, **config_vars)
    elif getattr(args, 'def_config', False):
        taroc.load_defaults(**config_vars)
    elif getattr(args, 'min_config', False):
        taroc.setup(**config_vars)
    else:
        taroc.load_config(**config_vars)
