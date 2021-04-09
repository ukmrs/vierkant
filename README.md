# Carrothko
## Text Encoding/Decoding FastAPI server :snake::zap:
Encodes to colorful squares or to hex gibberish.

Supports all valid unicode characters including whitespace ones.
Based on RC stream cipher, Carrothko cipher aims to be hedonistic more than utilitarian.
Encoded Images are enlarged for aesthetics purposes as serving 2x2 pixel pngs is not very thrilling.



## In Browser
### /img

Presents form that allows to encode to/decode from weird pixel art

<img src="./assets/slashimg.png">

### /str
Similar to /img but encodes to plain text

### /secret
Behind Basic Auth

### /encode/*key*/*secret*
quick encoding for simple secrets

## Installing
### with poetry


```
git clone https://github.com/ukmrs/carrothko && cd carrothko

# Install the required dependencies
poetry install

# run tests
poetry run pytest

# Start the server
poetry run uvicorn src.html:app --reload
```

## In Terminal
### encode through /encode/str or /encode/img
  
```
curl -d "key=key&secret=msg" http://localhost:8000/encode/img --output example.png
# or
curl http://localhost:8000/encode/key/msg --output example.png
```
  
### decode image through /decode/str /decode/img
```
# basic usage
curl -F "file=@example.png -F "key=klucz" http://localhost:8000/decode/img -s

# to file
curl -F "file=@example.png" -F "key=klucz" http://localhost:8000/decode/img -s > example.txt
# change to actual newlines
sed -i 's/\\r\\n/\n/g' example.txt
```
