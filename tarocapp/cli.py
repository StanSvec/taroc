import argparse

ACTION_PS = 'ps'


def parse_args(args):
    # TODO destination required
    parser = argparse.ArgumentParser(description='Manage all your jobs remotely with Taro CLI client')

    common = argparse.ArgumentParser()  # parent parser for subparsers in case they need to share common options
    common.add_argument('--set', type=str, action='append', help='override value of configuration field')
    common.add_argument('-dc', '--def-config', action='store_true', help='ignore config files and use defaults')
    common.add_argument('-mc', '--min-config', action='store_true',
                        help='ignore config files and use minimum configuration')
    common.add_argument('-C', '--config', type=str, help='path to custom config file')

    subparsers = parser.add_subparsers(dest='action')  # command/action

    _init_ps_parser(common, subparsers)

    parsed = parser.parse_args(args)
    return parsed


def _init_ps_parser(common, subparsers):
    """
    Creates parsers for `ps` command

    :param common: parent parser
    :param subparsers: sub-parser for ps parser to be added to
    """

    ps_parser = subparsers.add_parser(ACTION_PS, parents=[common], description='Show running jobs', add_help=False)
    ps_parser.add_argument('-H', '--host', type=str, action='append', help='host to communicate with')
    ps_parser.add_argument('-G', '--group', type=str, action='append', help='group of hosts to communicate with')
