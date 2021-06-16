import asyncio
from queue import Queue
from threading import Thread

import asyncssh as asyncssh

q = Queue()


def read_queue(queue):
    i = iter(lambda: queue.get(), None)
    for item in i:
        print(item)
    print('Finished')


t = Thread(target=read_queue, args=(q,))


async def fetch():
    async with asyncssh.connect('ciserver') as conn:
        result = await conn.run('taro ps -f json', check=True)
        # result = await conn.run('python3 -m taroapp ps -f json', check=True)
        print(result.stdout, end='')


if __name__ == '__main__':
    # t.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch())
    print('Konec')
    # q.put(None)
