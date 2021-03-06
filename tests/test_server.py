from src.main import app, TMP, read_bytes
from src.ciphers.rothko import Rothko
from fastapi.testclient import TestClient
import os

client = TestClient(app)
example_key = "żyrafowate"
example_secret = "rodzina dużych ssaków z podrzędu przeżuwaczy"


def test_main():
    response = client.get("/")
    assert 200 == response.status_code


def poke_post_image(mode, key="key", secret=None, file=None):
    return client.post("/img",
                       data={
                           "key": key,
                           "secret": secret,
                           "file": file,
                           "mode": mode,
                       })


def test_good_post_image():
    response = poke_post_image("encode", example_key, example_secret)

    # succesfully redirected
    assert response.status_code == 303

    next_url = response.next.url
    img_id = next_url.split("/")[-1]
    img_name = img_id + ".png"
    file_path = os.sep.join((TMP, img_name))

    # temporary file was created
    assert os.path.isfile(file_path)

    # serve image
    response_get = client.get(next_url)  # type: ignore pyright's drunk
    assert response_get.status_code == 200

    # temporary file should be deleted at this point
    assert not os.path.isfile(file_path)

    # check if it the response is valid png
    # PngImageFile(png) called by Rothko will raise SyntaxError otherwise
    # By the way check if the image is decoded into original message
    valid_png_hopefully = read_bytes(response_get.content)
    decoded = Rothko(example_key).decode_from_img(
        valid_png_hopefully)  # type: ignore
    assert decoded == example_secret


def test_post_image_missing_key():
    res_enc = poke_post_image("encode", None, "secret")
    res_dec = poke_post_image("decode", None, "secret")
    # 422 Unprocessable Entity - missing required field
    assert res_dec.status_code == 422
    assert res_enc.status_code == 422


def test_good_post_str():
    encode_response = client.post("/str",
                                  data={
                                      "key": example_key,
                                      "secret": example_secret,
                                      "mode": "encode",
                                  })

    assert encode_response.status_code == 200

    decode_response = client.post("/str",
                                  data={
                                      "key": example_key,
                                      "secret":
                                      encode_response.context["result"],
                                      "mode": "decode",
                                  })

    assert decode_response.status_code == 200
    assert decode_response.context["result"] == example_secret
