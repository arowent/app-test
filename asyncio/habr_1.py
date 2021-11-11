import asyncio
import time


async def foo():
    print('Running in foo')
    await asyncio.sleep(0)
    print('Explicit context switch to foo again')


async def bar():
    print('Explicit context to bar')
    await asyncio.sleep(0)
    print('Implicit context switch back to bar')


if __name__ == '__main__':
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(foo()), loop.create_task(bar())]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()
    print(f'FINISH: {time.perf_counter() - start_time}')
