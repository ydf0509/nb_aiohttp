import random


import time
import requests

from nb_aiohttp import NbSyncHttpClient
from threadpool_executor_shrink_able import ThreadPoolExecutorShrinkAble

# 显示当前进程cpu使用率性能的
from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil


nb_sync_http = NbSyncHttpClient(connector_limit=100,)
pool = ThreadPoolExecutorShrinkAble(100,)

def sync_req_test(n):
    url = random.choice(urls)
    text =   nb_sync_http.get(url).text
    if n % 1000 == 0:
        print(f'第 {n} 次','响应时间：',time.strftime("%H:%M:%S"), text)

def main():
    for i in range(100001):
        pool.submit(sync_req_test,i)


if __name__ == '__main__':
    thread_show_process_cpu_usage()
    main()





