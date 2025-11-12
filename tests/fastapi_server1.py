# from auto_run_on_remote import run_current_script_on_remote
# run_current_script_on_remote()


from nb_libs.system_monitoring import start_all_monitoring_threads,thread_show_process_cpu_usage

import nb_log


import os



import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from fastapi import FastAPI
import uvicorn
import starlette

from contextlib import asynccontextmanager
import anyio
from anyio import to_thread

import logging
nb_log.get_logger('uvicorn',log_level_int=logging.WARNING)




app = FastAPI()

@app.get("/", tags=["Root"])
def read_root():
    # 这个 time.sleep(1) 会在上面创建的线程池中的某个线程里执行
    time.sleep(1)
    return {"message": "欢迎来到 fastapi-d1 示例 API!"}


@app.get("/aio2", tags=["Root"])
async def aio_api():
    # await asyncio.sleep(1)
    return {"message": "欢迎来到aio1 示例 API!"}


def start(port):
     # 使用 uvicorn 启动应用
    # start_all_monitoring_threads(10)
    thread_show_process_cpu_usage(1)
    uvicorn.run(app, host="0.0.0.0", port=port,
    log_config={"version": 1,
    'disable_existing_loggers':False
    }
    )

if __name__ == "__main__":
   start(8006)