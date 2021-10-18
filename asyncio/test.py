# import asyncio
# import time
#
# from logger import logger
#
#
# async def first():
#    while True:
#        print(f'Прошла 1 секунда')
#        await asyncio.sleep(1)
#
#
# async def second():
#     print(f'Прошло 5 секунд')
#     await asyncio.sleep(1)
#
#
#
#
# if __name__ == '__main__':
#     start_time = time.perf_counter()
#     loop = asyncio.get_event_loop()
#     tasks = [loop.create_task(first()), loop.create_task(second())]
#     wait_tasks = asyncio.wait(tasks)
#     loop.run_until_complete(wait_tasks)
#     loop.close()
#     logger.info(f'FINISH: {time.perf_counter() - start_time}')
#     asyncio.run(main)

import asyncio


async def hello():
    print('Hello ...')
    await asyncio.sleep(5)
    print('... World!')


async def main():
    await asyncio.gather(hello(), hello())


asyncio.run(main())