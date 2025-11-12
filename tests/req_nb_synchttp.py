import random

import httpx
import asyncio
import time
import requests
from nb_aiopool import NbAioPool
from nb_aiohttp import NbAioHttpClient,NbSyncHttpClient
from threadpool_executor_shrink_able import ThreadPoolExecutorShrinkAble

from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil


nb_sync_http = NbSyncHttpClient(connector_limit=200,).run_forever(daemon=True)
pool = ThreadPoolExecutorShrinkAble(200)


requests_ss = requests.Session()

def main():
    for i in range(200001):
        if i%1000==0:
            print(i)
        url = random.choice(urls)
        pool.submit(nb_sync_http.get,url)
        # pool.submit(requests.get, url)

if __name__ == '__main__':
    main()





