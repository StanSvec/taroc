import asyncio
from queue import Queue
from threading import Thread

import aiohttp

q = Queue()


def read_queue(queue):
    i = iter(lambda: queue.get(), None)
    for item in i:
        print(item)
    print('Finished')


t = Thread(target=read_queue, args=(q,))


async def read_instances():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(0, 3):
            tasks.append(fetch(session))
        await asyncio.gather(*tasks)


async def fetch(session):
    async with session.get('http://localhost:8080/instances') as resp:
        q.put(resp.status)
        resp_body = await resp.json()
        print(resp_body)


if __name__ == '__main__':
    t.start()
    loop = asyncio.get_event_loop()
    coroutine = read_instances()
    # main = Thread(target=loop.run_until_complete, args=(coroutine,))
    # main.start()
    await loop.run_in_executor(None, coroutine)
    # main.join()
    print('Konec')
    q.put(None)
