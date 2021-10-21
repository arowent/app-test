import random
from time import sleep
import asyncio
import time
from termcolor import colored


def task(pid):
    """
    Synchronous non-deterministic task.
    """
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


async def task_coro(pid):
    """
    Coroutine non-deterministic task
    """
    await asyncio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


async def asynchronous():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = time.perf_counter()
    print('Synchronous:')
    synchronous()

    loop = asyncio.get_event_loop()
    print('\nAsynchronous:')
    loop.run_until_complete(asynchronous())
    loop.close()
    print(colored(f'FINISH: {time.perf_counter() - start_time}', 'yellow', attrs=['bold']))