"""
     ssh(1) obtains configuration data from the following sources in the
     following order:

           1.   command-line options
           2.   user's configuration file (~/.ssh/config)
           3.   system-wide configuration file (/etc/ssh/ssh_config)

     For each parameter, the first obtained value will be used.  The
     configuration files contain sections separated by Host
     specifications, and that section is only applied for hosts that
     match one of the patterns given in the specification.  The matched
     host name is usually the one given on the command line (see the
     CanonicalizeHostname option for exceptions).

     Since the first obtained value for each parameter is used, more
     host-specific declarations should be given near the beginning of
     the file, and general defaults at the end.
"""

from os.path import expanduser

from sshconf import read_ssh_config

from sshhost import SshHost


def get_hosts() -> SshHost:
    config = read_ssh_config(expanduser("~/.ssh/config"))
    hosts = []
    for host in config.hosts():
        params = config.host(host)
        ssh_host = SshHost(host, params['hostname'], params.get('identityfile'))
        hosts.append(ssh_host)

    return hosts
