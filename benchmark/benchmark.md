
## 20 各种三方包的http客户端每请求 10000次 http的 耗时

[![pZCRiPe.png](https://s21.ax1x.com/2025/11/13/pZCRiPe.png)](https://imgchr.com/i/pZCRiPe)

### 20.1 实测对比依赖的三方包说明

- pip install nb_libs   
thread_show_process_cpu_usage 需要用这个函数监控当前进程的cpu，通过当前进程cpu使用率的打印，让你清清楚楚到底是服务端性能不行还是客户端性能不行？让你清清楚楚知道是客户端cpu达到100%了，所以请求次数无法往上突破

- pip install  nb_aiopool
 异步并发池，比无脑 asyncio.create_task 10万任务 + asyncio.Semaphore(100) 限制并发， 内存和cpu好太多

- pip install  threadpool_executor_shrink_able
 同步并发池，主要是有界队列，也可以用 concurrent.futures.ThreadPoolExecutor ，但是它是无界队列，。

### 20.2 通过代码实测 benchmark

通过控制台的 日志观察得到

例如：
```
第 20000 次 响应时间：  10:29:20 {"message":"欢迎来到aio1 示例 API!"} 
第 30000 次 响应时间：  10:29:35 {"message":"欢迎来到aio1 示例 API!"}
```

#### 20.2.1 aiohttp.ClientSession()
- 耗时15秒   
第 1000 次 响应时间：  10:37:07 {"message":"欢迎来到aio1 示例 API!"}  
第 11000 次 响应时间：  10:37:22 {"message":"欢迎来到aio1 示例 API!"}  

#### 20.2.2 httpx.AsyncClient()
- 耗时50秒   
第 1000 次 响应时间：  10:44:17 {"message":"欢迎来到aio1 示例 API!"}
第 11000 次 响应时间：  10:45:07 {"message":"欢迎来到aio1 示例 API!"}

#### 20.2.3 nb_aiohttp.NbAioHttpClient
- 耗时13秒  
第 1000 次 响应时间： 10:58:32 {"message":"欢迎来到aio1 示例 API!"}
第 11000 次 响应时间： 10:58:45 {"message":"欢迎来到aio1 示例 API!"} 

### 20.2.4 requests.Session()  
- 耗时40秒  
第 2000 次 响应时间：  10:34:25 {"message":"欢迎来到aio1 示例 API!"}
第 12000 次 响应时间：  10:35:05 {"message":"欢迎来到aio1 示例 API!"} 

#### 20.2.5 nb_aiohttp.NbSyncHttpClient
- 耗时 15秒   
第 20000 次 响应时间：  10:29:20 {"message":"欢迎来到aio1 示例 API!"}   
第 30000 次 响应时间：  10:29:35 {"message":"欢迎来到aio1 示例 API!"}  

#### 20.2.6 nb_http_client.ObjectPool
- 耗时4秒   
第 11000 次 响应时间： 11:07:49 {"message":"欢迎来到aio1 示例 API!"} 
第 21000 次 响应时间： 11:07:53 {"message":"欢迎来到aio1 示例 API!"}


### 20.10 小结

#### 20.10.1 nb_http_client：

nb_http_client 和 nb_aiohttp 是同一个作者。

nb_http_client 性能吊打python同步和异步编程世界的 任何http客户端请求三方包，是真正的 **王中王，神中神**。  
nb_http_client 性能强悍是因为基于我的 万能对象池 universal_object_pool  + python 内置的非常底层的 http 模块 打造的 http连接池。  

- `nb_http_client` 是 ydf0509的 python万能对象池的 `universal_object_pool` 演示的一个附属品而已。   
`nb_http_client` 是用来显示 `universal_object_pool` 这个万能对象池如何神通广大的万能，可以实现任何连接池，包括**数据库连接池**和**http连接池**以及**python对象池**

- `nb_http_client`没有过于精心打磨成人性化好用,难用是难用了一点。   
但是用在公司内部的http服务间调用足够了，你可以再对他二次封装成一个你自己的请求函数 utils/my_request ，性能吊打requests 10倍，给你的服务器节约大量cpu

- **优点**：
   - 性能好，在同步包里面 nb_http_client.ObjectPool 是神中神级别，python 有史以来的http请求包，性能的王中王。
   - 连接池绑定了host和port，以及发送请求相对于封装完善的requests 和 aiohttp httpx们，不够人性化
- **缺点**：
   - 不太好用，连接池绑定了host和port，不能张冠李戴对别的域名发请求；
   - 不够人性化，发送请求相对于封装完善的高级包，requests 和 aiohttp httpx们，使用没那么方便，但你可以二次封装成你的 utils/my_request 函数。

#### 20.10.2  nb_aiohttp

- nb_aiohttp 有 NbAioHttpClient 和 NbSyncHttpClient 两个类， 如同httpx.AsyncClient() 和 httpx.Client() 一样，两个类分别用于同步编程和异步编程。

- `nb_aiohttp` 的好处是 使用方便程度和 `httpx/requests` 一样， 性能程度和`aiohttp`一样。
- httpx使用比aiohttp方便
- aiohttp 性能吊打 httpx
  

