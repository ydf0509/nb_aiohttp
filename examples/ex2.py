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


    async def f1():
        """演示通过session属性任然使用aiohttp.ClientSession的request等原生方法"""
        async with nbhttp.session.request('GET', 'https://www.baidu.com') as response:
            text = await response.text()
        print(text[:10])


    # async def f3():
    #     """
    #     NbAioHttpClient 既能用封装，又能用原生
    #
    #     演示使用 NbAioHttpClient 中没定义的方法，自动使用 aiohttp.ClientSession 中的方法
    #     注意此处没使用 nbhttp.session.put，而是直接使用 nbhttp.put，
    #     """
    #     async with nbhttp.put('https://www.baidu.com') as response:
    #         text = await response.text()
    #     print(text[:10])


    async def main():
        await nbhttp.ensure_session()
        await f1()

        await f2()

        # await f3()

        await nbhttp.close()


    asyncio.run(main())
