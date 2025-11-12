import random

import httpx
import asyncio
import time
from nb_aiopool import NbAioPool
from nb_aiohttp import NbAioHttpClient

from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage # 显示当前进程性能的


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil

nbhttp = NbAioHttpClient(connector_limit=200)
pool = NbAioPool(200,)

httpx_client= httpx.AsyncClient(limits=httpx.Limits(max_connections=200,))

async def main():
    for i in range(200000):
        if i%1000==0:
            print(i)
        url = random.choice(urls)
        await pool.submit(nbhttp.get(url))
        # await pool.submit(httpx_client.get(url))

if __name__ == '__main__':
    thread_show_process_cpu_usage()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

