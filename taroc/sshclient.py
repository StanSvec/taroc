import json

import asyncssh


def create_tasks(command, *hosts):
    return {host: _exec(host, command) for host in hosts}


async def _exec(host, command):
    async with asyncssh.connect(host) as conn:
        result = await conn.run(f"python3 -m taroapp {command}", check=True)
        result_str = result.stdout
        result_json = json.loads(result_str)
        return host, result_json
