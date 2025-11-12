import asyncio
from nb_aiohttp.nb_aiohttp_m import NbAioHttpClient


if __name__ == '__main__':
    # nbhttp 使得可以模块级全局变量直接实例化， aiohttp.ClientSession不能在全局变量实例化
    nbhttp = NbAioHttpClient(timeout=5,  # 可以直接入参数字，降低传 ClientTimeout 难度
                             connector_limit=200,  # 直接把连接池最关键的的limit入参提升到一级，降低传 aiohttp.TCPConnector 难度
                             )  #

    async def f1():
        """演示通过session属性任然使用aiohttp.ClientSession的request等原生方法"""
        async with nbhttp.session.request('GET', 'https://www.baidu.com') as response:
            text = await response.text()
        print(text[:10])



    async def main():
        await nbhttp.ensure_session()
        await f1()
        await nbhttp.close()

        # await asyncio.sleep(1)



    asyncio.run(main())
