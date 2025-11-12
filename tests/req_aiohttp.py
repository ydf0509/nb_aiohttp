

import asyncio
import time
import aiohttp

from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage
from nb_aiopool import NbAioPool


url = "http://127.0.0.1:8006/aio2"


async def aio_req_test(aiohttp_cleint, n):
    async with aiohttp_cleint.get(url) as response: 
        text =  await response.text()
    if n % 100 == 0:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), text)


pool = NbAioPool(100)
async def main():
    async with  aiohttp.ClientSession() as aiohttp_cleint:
        for i in range(500000):
            await pool.submit(aio_req_test(aiohttp_cleint, i))

    

if __name__ == '__main__':
    thread_show_process_cpu_usage()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

