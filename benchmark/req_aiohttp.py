

import asyncio
import time
import aiohttp
import random

from nb_aiopool import NbAioPool

# 显示当前进程cpu使用率性能的
from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage 


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil



async def aio_req_test(n,aiohttp_cleint):
    url = random.choice(urls)
    async with aiohttp_cleint.get(url) as response: 
        text =  await response.text()
    if n % 1000 == 0:
        print(f'第 {n} 次','响应时间：',time.strftime("%H:%M:%S"), text)


pool = NbAioPool(100,max_queue_size=10)
async def main():
    async with  aiohttp.ClientSession() as aiohttp_cleint:
        for i in range(100001):
            await pool.submit(aio_req_test( i,aiohttp_cleint))

if __name__ == '__main__':
    thread_show_process_cpu_usage()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()



