# Vierkant
## Text Encoding/Decoding FastAPI server :snake::zap:
Silly server that encodes to colorful squares or to hex gibberish.
Supports all valid unicode characters including whitespace ones.
Encoded Images are enlarged for aesthetics purposes as serving 2x2 pixel pngs is not very thrilling.
Made for fun and to explore ciphers and fastapi a lil bit, not meant to be practical.


## In Browser
### /img

Presents form that allows to encode to/decode from weird pixel art

<img src="./assets/slashimg.png">

### /str
Similar to /img but encodes to plain text

### /encode/*key*/*secret*
Quick encoding for simple secrets

### /docs
FastAPI auto-generated docs, nice to poke around


## Installing
Requires python ^3.9


```
git clone https://github.com/ukmrs/carrothko && cd carrothko

# Install the required dependencies
pip install -r requirements.txt

# run tests
pytest

# Start the server
uvicorn src.main:app --reload
```

## Terminal examples
### images
  
```
# encode
curl -d "key=key&secret=SecretMessage" http://localhost:8000/encode/img --output example.png
# or
curl http://localhost:8000/encode/key/SecretMessage --output example.png

# decode
curl -F "file=@example.png" -F "key=key" http://localhost:8000/decode/img -s
```
### Strings

```
# encode
curl -d "key=key&secret=SecretMessage" http://localhost:8000/encode/str
# decode
curl -d "key=key&secret=2c62ebfcb63a5fbf3b98e83b2bda2b1e6166a1a5242ff345163edf" http://localhost:8000/decode/str
```
