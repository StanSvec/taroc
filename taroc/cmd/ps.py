import asyncio
from queue import Queue
from threading import Thread

from taroc import ps, sshclient
from taroc.view import instance

_POISON = None


def run(args):
    q = Queue()
    _start_print(q)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sshclient.fetch('ps', q))
    q.put(_POISON)


def _start_print(queue):
    t = Thread(target=_print, args=(queue,))
    t.start()


def _print(queue):
    ps.print_table(iter(lambda: queue.get(), _POISON), instance.DEFAULT_COLUMNS, show_header=True, pager=False)
