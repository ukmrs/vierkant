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

### /encode/*key*/*secret*
Quick encoding for simple secrets

### /secret
Behind Basic Auth

### /docs
FastAPI auto-generated docs, nice to poke around


## Installing
### with poetry


```
git clone https://github.com/ukmrs/carrothko && cd carrothko

# Install the required dependencies
poetry install

# run tests
poetry run pytest

# Start the server
poetry run uvicorn src.main:app --reload
```

## Terminal examples
### Strings

```
# encode
curl -d "key=key&secret=SecretMessage" http://localhost:8000/encode/str
# decode
curl -d "key=key&secret=2c62ebfcb63a5fbf3b98e83b2bda2b1e6166a1a5242ff345163edf" http://localhost:8000/decode/str
```
### images
  
```
# encode
curl -d "key=key&secret=SecretMessage" http://localhost:8000/encode/img --output example.png
# or
curl http://localhost:8000/encode/key/SecretMessage --output example.png

# decode
# basic usage
curl -F "file=@example.png" -F "key=key" http://localhost:8000/decode/img -s

# to file
curl -F "file=@example.png" -F "key=key" http://localhost:8000/decode/img -s > example.txt
# change to actual newlines
sed -i 's/\\r\\n/\n/g' example.txt
```
