import json

import asyncssh


async def fetch(command, queue):
    async with asyncssh.connect('ciserver') as conn:
        result = await conn.run(f"python3 -m taroapp {command} -f json", check=True)
        result_str = result.stdout
        result_list = json.loads(result_str)
        for item in result_list:
            queue.put(('ciserver', item))
