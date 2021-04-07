#!/usr/bin/env python3
from src.ciphers.rothko import Rothko
from fastapi import FastAPI, File, UploadFile, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from starlette.background import BackgroundTasks
from io import BytesIO
from uuid import uuid4
import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = os.sep.join((MAIN_DIR, "tmpimgs"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates/')


@app.get("/")
def index():
    return RedirectResponse(url='/img')


def read_bytes(file):
    return BytesIO(file)


def remove_file(path):
    os.unlink(path)


@app.get('/img')
def get_image(request: Request):
    result = ''
    return templates.TemplateResponse('img.html',
                                      context={
                                          'request': request,
                                          'result': result
                                      })


@app.post("/img")
async def post_image(request: Request,
                     key: str = Form(...),
                     secret: str = Form(None),
                     file: UploadFile = File(None),
                     btn: str = Form(...)):
    if btn == "encode":
        if secret:
            name = uuid4().hex
            path = os.sep.join((TMP, name)) + ".png"
            _ = Rothko(key).encode_to_img(secret, scale=True, save_path=path)
            return RedirectResponse(url=f"/encoded/{name}",
                                    status_code=status.HTTP_303_SEE_OTHER)
        else:
            result = "Secret field was not filled but is required for encoding"

    try:
        img = read_bytes(await file.read())
        result = Rothko(key).decode_from_img(img)
    except SyntaxError:  # file was not supplied or is not valid png
        result = "Image was not supplied but is required by decode method"

    return templates.TemplateResponse('img.html',
                                      context={
                                          'request': request,
                                          'result': result,
                                      })

    # # image = read_bytes(await file.read())
    # return Rothko(key).decode_from_img(image)


@app.get('/encoded/{image_id}')
def image_response(background_tasks: BackgroundTasks, image_id: str):
    """Serves the encoded img and deletes it shortly after"""
    path = os.sep.join((TMP, image_id)) + ".png"
    if os.path.isfile(path):
        background_tasks.add_task(remove_file, path)
        return FileResponse(path)
    return "Encoded pictures are avaible only once"


# ============  encode/decode from string  ============


@app.get('/string')
def get_result(request: Request):
    result = ''
    return templates.TemplateResponse('serve.html',
                                      context={
                                          'request': request,
                                          'result': result
                                      })


@app.post('/string')
def post_req(request: Request,
             key: str = Form(...),
             secret: str = Form(...),
             btn: str = Form(...)):
    if btn == "encode":
        result = Rothko(key).encode_to_string(secret)
    else:
        result = Rothko(key).decode_from_string(secret)
    return templates.TemplateResponse('serve.html',
                                      context={
                                          'request': request,
                                          'result': result,
                                          'key': key,
                                      })


@app.get('/encode/{key}/{msg}')
def encode(key, msg):
    Rothko(key).encode_to_img(msg, scale=True)
    return FileResponse("picture.png")
