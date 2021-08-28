import argparse

ACTION_PS = 'ps'


def parse_args(args):
    # TODO destination required
    parser = argparse.ArgumentParser(description='Manage all your jobs remotely with Taro CLI client')
    common = argparse.ArgumentParser()  # parent parser for subparsers in case they need to share common options
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
    ps_parser.add_argument('-i', '--inst', '--instance', type=str, help='instance filter')
