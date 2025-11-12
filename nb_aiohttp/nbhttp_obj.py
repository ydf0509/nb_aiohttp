

from .nb_aiohttp_m import NbAioHttpClient
from .nb_synchttp import NbSyncHttpClient


# 直接全局内置，如果用户不需要专门定制实例化入参和区分多实例，可以简单直接使用这两个对象
nbhttp = NbAioHttpClient()
nb_sync_http = NbSyncHttpClient()