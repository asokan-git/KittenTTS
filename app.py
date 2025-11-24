from fastapi import FastAPI
from pydantic import BaseModel
from kittentts import KittenTTS
import soundfile as sf
import io
import base64

app = FastAPI()

# Load model once at startup
model = KittenTTS("KittenML/kitten-tts-nano-0.2")

class TTSRequest(BaseModel):
    text: str
    voice: str = "expr-voice-2-f"

@app.post("/tts")
def tts(req: TTSRequest):
    audio = model.generate(req.text, voice=req.voice)

    # write wav to memory
    buf = io.BytesIO()
    sf.write(buf, audio, 24000, format="WAV")
    wav_bytes = buf.getvalue()

    # return base64 wav so it's easy to consume
    return {
        "voice": req.voice,
        "sample_rate": 24000,
        "wav_base64": base64.b64encode(wav_bytes).decode("utf-8")
    }
