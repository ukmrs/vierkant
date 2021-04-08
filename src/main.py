#!/usr/bin/env python3
from src.ciphers.rothko import Rothko
from fastapi import (FastAPI, File, UploadFile, Request, Form, status, Depends,
                     HTTPException)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from starlette.background import BackgroundTasks
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from io import BytesIO
from uuid import uuid4
import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = os.sep.join((MAIN_DIR, "tmpimgs"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates/')
security = HTTPBasic()


@app.get("/")
def index():
    return RedirectResponse(url='/img')


def read_bytes(file):
    return BytesIO(file)


def remove_file(path):
    os.unlink(path)


# ============  encode/decode from img  ============


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
            pxl = Rothko(key).encode_to_img(secret, scale=True)
            pxl.save(TMP)
            # redirect user to page when they can download image
            return RedirectResponse(url=f"/encoded/{pxl.id}",
                                    status_code=status.HTTP_303_SEE_OTHER)
        else:
            result = "Secret field was not filled but is required for encoding"

    else:
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


# ============  url based functions  ============


# TODO this is incorrect
@app.get('/encode/{key}/{msg}')
def encode(background_tasks: BackgroundTasks, key, msg):
    pxl = Rothko(key).encode_to_img(msg, scale=True)
    save_path = pxl.save(TMP)
    background_tasks.add_task(remove_file, save_path)
    return FileResponse(save_path)


# ============  Basic Auth Lock  ============


def get_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = secrets.compare_digest(credentials.password, "pass")
    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/secret")
def give_out_secret(request: Request, username: str = Depends(get_username)):
    result = f"I am sorry {username}, this page is pointless"
    return templates.TemplateResponse("secret.html",
                                      context={
                                          "request": request,
                                          "secret": result
                                      })
