
from .nb_aiohttp_m import NbAioHttpClient, NbHttpResp, asyncio
import threading


class NbSyncHttpClient:
    _lock = threading.Lock()
    def __init__(self, **kwargs):
        self._nbaiohttp = NbAioHttpClient(**kwargs)
        self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)
        self._has_run_forever = False

    def run_forever(self):
        if self._has_run_forever:
            return self
        with self._lock:
            if not self._has_run_forever:
                threading.Thread(target=self.loop.run_forever).start()
                self._has_run_forever = True
        return self

    def request(self, method: str, url: str, **kwargs) -> NbHttpResp:
        future = asyncio.run_coroutine_threadsafe(self._nbaiohttp.request(method, url, **kwargs), self.loop)
        return future.result()

    def get(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('POST', url, **kwargs)

    def delete(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('DELETE', url, **kwargs)

    def head(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('HEAD', url, **kwargs)

    def options(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('OPTIONS', url, **kwargs)

    def patch(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('PATCH', url, **kwargs)

    def trace(self, url: str, **kwargs) -> NbHttpResp:
        return self.request('TRACE', url, **kwargs)
