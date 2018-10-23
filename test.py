import speech_recognition as sr
from wit import Wit
import pyaudio
import json
import pyaudio
import wave


def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    # --------- SETTING PARAMS FOR OUR AUDIO FILE ------------#
    FORMAT = pyaudio.paInt16  # format of wave
    CHANNELS = 2  # no. of audio channels
    RATE = 44100  # frame rate
    CHUNK = 1024  # frames per audio sample
    # --------------------------------------------------------#

    # creating PyAudio object
    audio = pyaudio.PyAudio()

    # open a new stream for microphone
    # It creates a PortAudio Stream Wrapper class object
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    # ----------------- start of recording -------------------#
    print("Listening...")

    # list to save all audio frames
    frames = []

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        # read audio stream from microphone
        data = stream.read(CHUNK)
        # append audio data to frames list
        frames.append(data)

    # ------------------ end of recording --------------------#
    print("Finished recording.")

    stream.stop_stream()  # stop the stream object
    stream.close()  # close the stream object
    audio.terminate()  # terminate PortAudio

    # ------------------ saving audio ------------------------#

    # create wave file object
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

    # settings for wave file object
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))

    # closing the wave file object
    waveFile.close()


def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio



from wit import Wit
wit_access_token = 'AVOW4L6WX24RHWYPY3ME5OD34P42RMT4'

client = Wit(wit_access_token)

# Wit.ai api access token


record_audio(5,'myname.wav')

result = None
with open('myname.wav', 'rb') as f:
    result = client.speech(f,None,{'Content-Type':'audio/wav'})

dumps = json.dumps(result)
data = json.loads(dumps)
text = data['_text']
print(text)
