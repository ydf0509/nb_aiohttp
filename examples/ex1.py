import asyncio
from nb_aiohttp import NbAioHttpClient, NbHttpResp


if __name__ == '__main__':
    # nbhttp 使得可以模块级全局变量直接实例化， aiohttp.ClientSession不能在全局变量实例化
    nbhttp = NbAioHttpClient(timeout=5,  # 可以直接入参数字，降低传 ClientTimeout 难度
                             connector_limit=200,  # 直接把连接池最关键的的limit入参提升到一级，降低传 aiohttp.TCPConnector 难度
                             )  #


    async def f2():
        """演示使用NbAioHttpClient的request_text方法，
        少了一次 async with
        和 少了一次await response.text()，更简洁"""
        nb_resp = await nbhttp.get('https://www.baidu.com')
        print(nb_resp.text[:100])

        nb_resp2 = await nbhttp.get('https://www.sina.com')
        print(nb_resp2.text[:100])

        await nbhttp.close()
        await asyncio.sleep(0)




    asyncio.run(f2())
