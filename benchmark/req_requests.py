import random


import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from threadpool_executor_shrink_able import ThreadPoolExecutorShrinkAble

# 显示当前进程cpu使用率性能的
from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage


urls = ["http://127.0.0.1:8006/aio2","http://127.0.0.1:8007/aio2"] # 防止抱怨是服务端性能不行，两个进程端口，消灭服务端gil
# 创建一个 Session 对象
session = requests.Session()

# 设置最大连接数和每个主机的最大连接数
adapter = HTTPAdapter(
    pool_connections=100,   # 连接池总大小（连接的 host 数量）
    pool_maxsize=100,       # 每个 host 最大连接数
    max_retries=Retry(total=3, backoff_factor=0.2),  # 可选：自动重试
)

# 为所有 HTTP/HTTPS 协议挂载 adapter
session.mount("http://", adapter)
session.mount("https://", adapter)

pool = ThreadPoolExecutorShrinkAble(100,)
def sync_req_test(n):
    url = random.choice(urls)
    text = session.get(url).text
    if n % 1000 == 0:
        print(f'第 {n} 次','响应时间：',time.strftime("%H:%M:%S"), text)

def main():
    for i in range(100001):
        pool.submit(sync_req_test,i)


if __name__ == '__main__':
    thread_show_process_cpu_usage()
    main()








