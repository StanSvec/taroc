import json

import asyncssh

from taroc import cfg


def create_tasks(command, *hosts):
    return {host: _exec(host, command) for host in hosts}


async def _exec(host, command):
    async with asyncssh.connect(host, login_timeout=cfg.ssh_con_timeout) as conn:
        result = await conn.run(f"python3 -m taroapp {command}", check=True, timeout=cfg.ssh_run_timeout)
        result_str = result.stdout
        result_json = json.loads(result_str)
        return host, result_json
