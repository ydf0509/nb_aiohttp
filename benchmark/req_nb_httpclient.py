import random


import time
import typing
from http.client import HTTPConnection

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from nb_http_client import ObjectPool, HttpOperator
from threadpool_executor_shrink_able import BoundedThreadPoolExecutor,ThreadPoolExecutorShrinkAble

http_pool1 = ObjectPool(object_type=HttpOperator, object_pool_size=100, object_init_kwargs=dict(host='127.0.0.1', port=8006),
                       max_idle_seconds=30)
http_pool2 = ObjectPool(object_type=HttpOperator, object_pool_size=100, object_init_kwargs=dict(host='127.0.0.1', port=8007),
                       max_idle_seconds=30)

http_pool_list = [http_pool1, http_pool2]

# 显示当前进程cpu使用率性能的
from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil



pool = ThreadPoolExecutorShrinkAble(100,)
def sync_req_test(n):
    http_pool = random.choice(http_pool_list)
    with http_pool.get() as conn:  # type: typing.Union[HttpOperator,HTTPConnection]  # http对象池的请求速度暴击requests的session和直接requests.get
        r1 = conn.request_and_getresponse('GET', '/aio2')
        if n % 1000 == 0:
            print(f'第 {n} 次', '响应时间：', time.strftime("%H:%M:%S"), r1.text)

def main():
    for i in range(100001):
        pool.submit(sync_req_test,i)


if __name__ == '__main__':
    thread_show_process_cpu_usage()
    main()








