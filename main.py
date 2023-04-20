from os.path import isfile
from pathlib import Path
import datetime
import uvicorn
from fastapi import FastAPI, Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_utils.tasks import repeat_every
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from config import *
from web_app.edit_pdf import create_pdf
import os

APP = FastAPI()
limiter = Limiter(key_func=get_remote_address)
APP.state.limiter = limiter
APP.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "*",
]


APP.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def remove_all_files_in_path(path: str, end=12):
    now = datetime.datetime.now()
    time_threshold = datetime.timedelta(hours=end)
    for file in Path(path).glob('*'):
        if file.is_file():
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file))
            time_difference = now - modification_time
            if time_difference > time_threshold:
                try:
                    os.unlink(file.absolute())
                    print("deleted file: ", file.absolute())
                except Exception:
                    print(f"can't delete file {file.absolute()}")

@APP.on_event("startup")
@repeat_every(seconds=60 * 60)
def remove_files():
    Path(os.path.join(os.getcwd(), "static_download")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(os.getcwd(), "web_app", "tmp")).mkdir(parents=True, exist_ok=True)
    files_static_download_path = os.path.join(os.getcwd(), "static_download")
    files_path_tmp = os.path.join(os.getcwd(), "web_app", "tmp")
    remove_all_files_in_path(files_static_download_path)
    remove_all_files_in_path(files_path_tmp)



@APP.post("/api/create-pdf")
async def pdf(request: Request):
    if not BLOCK_ALL_THEY_DIDNT_PAY_US:
        data = await request.json()
        value = "files/" + create_pdf(data)
        return value



@APP.get("/api/files/{filename}")
async def file(request: Request, filename):
    if not BLOCK_ALL_THEY_DIDNT_PAY_US:
        path_to_file = os.path.join(os.getcwd(), "static_download", filename)

        if not isfile(path_to_file):
            return Response(status_code=404)

        response = FileResponse(path_to_file, media_type='application/octet-stream', filename=filename)
        return response





if __name__ == "__main__":
    uvicorn.run(APP, host="localhost", port=8638)

