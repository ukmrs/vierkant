#!/usr/bin/env python3
from ciphers.rothko import Rothko
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from io import BytesIO

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates/')


@app.get("/")
def index():
    return RedirectResponse(url='/docs')


@app.get('/encode/{key}/{msg}')
def encode(key, msg):
    Rothko(key).encode_to_img(msg, scale=True)
    return FileResponse("picture.png")


def read_bytes(file):
    return BytesIO(file)


@app.post("/decode")
async def decode_image(key: str,
                       file: UploadFile = File(..., media_type="image/png")):
    image = read_bytes(await file.read())
    return Rothko(key).decode_from_img(image)


# ============  encode/decode from image  =============


@app.get('/encodeimg')
def get_result_img(request: Request):
    result = ''
    return templates.TemplateResponse('serve.html',
                                      context={
                                          'request': request,
                                          'result': result
                                      })


@app.post('/encodeimg')
def post_request_img(request: Request,
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


# ============  encode/decode from string  ============


@app.get('/encodestr')
def get_result(request: Request):
    result = ''
    return templates.TemplateResponse('serve.html',
                                      context={
                                          'request': request,
                                          'result': result
                                      })


@app.post('/encodestr')
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
