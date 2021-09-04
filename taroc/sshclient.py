import asyncio

import asyncssh


def execute(command, *hosts):
    return {host: _fetch(host, command) for host in hosts}


async def _fetch(host, command):
    async with asyncssh.connect(host) as conn:
        result = await conn.run(f"python3 -m taroapp {command}", check=True)
        result_str = result.stdout
        return host, result_str


async def print_results():
    coro = _fetch('prdextdata', 'ps -f json'), _fetch('ciserver', 'ps -f json')
    coro_tasks = [asyncio.create_task(c) for c in coro]
    print(coro)
    for task in asyncio.as_completed(coro_tasks):
        print(task)
        print(await task)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(print_results())
