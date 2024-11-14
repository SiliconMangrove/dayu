import os

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse, FileResponse
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from core.lib.network import NetworkAPIPath, NetworkAPIMethod
from core.lib.common import FileOps
from .distributor import Distributor


class DistributorServer:
    def __init__(self):
        self.distributor = Distributor()

        self.app = FastAPI(routes=[
            APIRoute(NetworkAPIPath.DISTRIBUTOR_DISTRIBUTE,
                     self.distribute_data,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_DISTRIBUTE]
                     ),
            APIRoute(NetworkAPIPath.DISTRIBUTOR_RESULT,
                     self.query_result,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_RESULT]
                     ),
            APIRoute(NetworkAPIPath.DISTRIBUTOR_FILE,
                     self.download_file,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_FILE]
                     ),
            # query all results：return as json
            APIRoute(NetworkAPIPath.DISTRIBUTOR_ALL_RESULT,
                     self.query_all_result,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_ALL_RESULT]
                     ),
            # clear database
            APIRoute(NetworkAPIPath.DISTRIBUTOR_CLEAR_DATABASE,
                     self.clear_database,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_CLEAR_DATABASE]
                     ),
            # query database is empty
            APIRoute(NetworkAPIPath.DISTRIBUTOR_IS_DATABASE_EMPTY,
                     self.is_database_empty,
                     response_class=JSONResponse,
                     methods=[NetworkAPIMethod.DISTRIBUTOR_IS_DATABASE_EMPTY]
                     ),
        ], log_level='trace', timeout=6000)

        self.app.add_middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True,
            allow_methods=["*"], allow_headers=["*"],
        )

    async def distribute_data(self, backtask: BackgroundTasks, file: UploadFile = File(...), data: str = Form(...)):
        file_data = await file.read()
        backtask.add_task(self.distribute_data_background, data, file_data)

    def distribute_data_background(self, data, file_data):
        self.distributor.set_current_task(data)
        FileOps.save_data_file(self.distributor.cur_task, file_data)
        self.distributor.record_transmit_ts()
        self.distributor.distribute_data()

    async def query_result(self, request: Request):
        data = await request.json()
        size = data['size']
        time_ticket = data['time_ticket']
        return self.distributor.query_result(time_ticket, size)

    async def download_file(self, request: Request, backtask: BackgroundTasks):
        data = await request.json()
        file_path = data['file']
        if not os.path.exists(file_path):
            return b''
        return FileResponse(
            path=file_path,
            filename=file_path,
            background=backtask.add_task(FileOps.remove_file, file_path))

    async def query_all_result(self):
        return self.distributor.query_all_result()

    async def clear_database(self):
        self.distributor.clear_database()

    async def is_database_empty(self):
        return self.distributor.is_database_empty()
