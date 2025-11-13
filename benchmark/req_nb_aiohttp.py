import random

import httpx
import asyncio
import time
from nb_aiopool import NbAioPool
from nb_aiohttp import NbAioHttpClient

# 显示当前进程cpu使用率性能的
from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage # 显示当前进程性能的


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil

nbhttp = NbAioHttpClient(connector_limit=100)
pool = NbAioPool(100,)

async def aio_req_test(n):
    url = random.choice(urls)
    text =  (await nbhttp.get(url)).text
    if n % 1000 == 0:
        print(f'第 {n} 次','响应时间：',time.strftime("%H:%M:%S"), text)


async def main():
    for i in range(100001):
        await pool.submit(aio_req_test(i))

if __name__ == '__main__':
    thread_show_process_cpu_usage()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

