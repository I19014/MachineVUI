import wave
from io import BytesIO
from picotts import PicoTTS
import simpleaudio as sa

picotts = PicoTTS()
wavs = picotts.synth_wav('Happy Birthday to You Happy. Birthday to You. Happy Birthday. Happy Birthday.')
wav = wave.open(BytesIO(wavs))
print (wav.getnchannels(), wav.getframerate(), wav.getnframes())

wave_object = sa.WaveObject.from_wave_read(wav)
play_obj = wave_object.play()
play_obj.wait_done() 