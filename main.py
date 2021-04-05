#!/usr/bin/env python3
from fastapi import FastAPI, File, UploadFile
from ciphers.rothko import Rothko
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from io import BytesIO

app = FastAPI()


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
