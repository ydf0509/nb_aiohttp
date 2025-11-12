
"""
NbAioHttpClient 懒加载实例化 aiohttp.ClientSession
使得可以模块级全局变量直接实例化，
因为aiohttp.ClientSession不能在全局变量实例化，不好用。
"""
import time

import nb_log
import json
import copy
import aiohttp
import asyncio
from aiohttp import BaseConnector
from typing import Optional, Any, Union, Coroutine
from aiohttp.client import StrOrURL, LooseCookies, LooseHeaders, ClientTimeout, sentinel


class _Unset:
    pass


unset = _Unset()


class NbHttpResp:
    def __init__(self, text, status, headers, url):
        self.text = text
        self.status = status
        self.headers = headers
        self.url = url

    @property
    def dict(self):
        try:
            return json.loads(self.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"response text is not valid JSON: {e}") from e

    def __repr__(self):
        return f"<NbHttpResp [{self.status}] {self.url}>"

    @property
    def ok(self):
        """类似 requests 的 ok 属性"""
        return 200 <= self.status < 300


class NbAioHttpClient():
    logger = nb_log.get_logger(__name__)

    def __init__(self, *, connector: Optional[BaseConnector] = None,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 cookies: Optional[LooseCookies] = None,
                 headers: Optional[LooseHeaders] = None,
                 timeout: Union[object, ClientTimeout] = sentinel,

                 connector_limit: Union[int,] = 100,

                 max_retries: int = 3,
                 is_raise_for_status: bool = True,
                 log_timeout_seconds: Union[int, float, _Unset] = unset,
                 is_log_error: bool = True,

                 **kwargs
                 ):

        if isinstance(timeout, (int, float)):
            timeout = ClientTimeout(total=timeout)

        self._client_params = {'connector': connector,
                               'loop': loop,
                               'cookies': cookies,
                               'headers': headers,
                               'timeout': timeout, }

        self._client_kwargs = kwargs

        self._connector_limit = connector_limit

        self._max_retries = max_retries
        self._is_raise_for_status = is_raise_for_status

        self._log_timeout_seconds = log_timeout_seconds
        self._is_log_error = is_log_error

        self.session: aiohttp.ClientSession = None
        self._create_lock: Optional[asyncio.Lock] = None
        self._has_create = False

    async def _ensure_lock(self):
        if self._create_lock is None:
            self._create_lock = asyncio.Lock()

    async def ensure_session(self):
        if self._has_create:
            return
        await self._ensure_lock()
        async with self._create_lock:
            if not self._has_create:
                if self._client_params['connector'] is None:
                    self._client_params['connector'] = aiohttp.TCPConnector(limit=self._connector_limit)
                self.session = aiohttp.ClientSession(**self._client_params, **self._client_kwargs)
                self._has_create = True

    # async def ensure_session(self):
    #     if self._has_create:
    #         return
    #     self._has_create = True
    #     if self._client_params['connector'] is None:
    #         self._client_params['connector'] = aiohttp.TCPConnector(limit=self._connector_limit)
    #     self.session = aiohttp.ClientSession(**self._client_params, **self._client_kwargs)

    async def request(self, method: str, url: StrOrURL,

                         max_retries: Union[int, _Unset] = unset,
                         is_raise_for_status: Union[bool, _Unset] = unset,

                         **kwargs: Any) -> Optional[NbHttpResp]:
        await self.ensure_session()

        if isinstance(max_retries, _Unset):
            max_retries = self._max_retries
        if isinstance(is_raise_for_status, _Unset):
            is_raise_for_status = self._is_raise_for_status
        timeout = kwargs.get('timeout', self._client_params['timeout'])
        if isinstance(timeout, (int, float)):
            kwargs['timeout'] = ClientTimeout(total=timeout)

        req_params = {
            'method': method,
            'url': url,
            'max_retries': max_retries,
            'is_raise_for_status': is_raise_for_status,
            'data': kwargs.get('data', None),
            'json': kwargs.get('json', None),
            'params': kwargs.get('params', None),
        }

        req_params_str = json.dumps(req_params, ensure_ascii=False)

        for attempt in range(max_retries):
            try:
                t1 = time.time()
                async with self.session.request(method, url, **kwargs) as response:
                    if is_raise_for_status:
                        if self._is_log_error and not response.ok:
                            self.logger.error(
                                f"response status is {response.status}, url is {response.url}, log_params is {req_params_str}")

                    text = await response.text()
                    if isinstance(self._log_timeout_seconds, (int, float)):
                        cost_time = time.time() - t1
                        if cost_time > self._log_timeout_seconds:
                            self.logger.warning(
                                f"response timeout {cost_time} seconds, url is {response.url}, log_params is {req_params_str}")
                    return NbHttpResp(text, response.status, response.headers, response.url)
            except Exception as e:
                if self._is_log_error:
                    self.logger.error(
                        f"request attempt {attempt + 1} failed: {e} , url is {url}, req_params is {req_params_str}")
                if attempt == max_retries - 1:
                    raise e
                # await asyncio.sleep(2 ** attempt)  # 指数退避

    async def get(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('GET', url, **kwargs)

    async def post(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('POST', url, **kwargs)

    async def put(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('PUT', url, **kwargs)

    async def delete(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('DELETE', url, **kwargs)

    async def head(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('HEAD', url, **kwargs)

    async def options(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('OPTIONS', url, **kwargs)

    async def patch(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('PATCH', url, **kwargs)

    async def trace(self, url: StrOrURL, **kwargs) -> Optional[NbHttpResp]:
        return await self.request('TRACE', url, **kwargs)



    # def __getattr__(self, name: str) -> Any:
    #     """
    #     代理原生方法，既能用封装，又能用原生
    #     代理对底层 aiohttp.ClientSession 实例的属性访问。
    #     这使得你可以直接调用 session.get, session.post 等方法。
    #     """
    #     if not self._has_create:
    #         raise RuntimeError(
    #             f"Session未初始化,请先调用 await ensure_session() 或使用 async with"
    #         )
    #     return getattr(self.session, name)

    async def close(self):
        if self._has_create and self.session and not self.session.closed:
            await self.session.close()
            await asyncio.sleep(0.25)


    async def __aenter__(self) -> 'NbAioHttpClient':
        # 确保 session 在进入 'async with' 块时已经创建
        await self.ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
        self._has_create = False









