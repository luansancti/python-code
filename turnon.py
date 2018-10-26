import speech_recognition as sr;
import json
import pyaudio
import wave
from wit import Wit
import playsound
import serial
import time
import os

###################### Variaveis do Codigo ########################

rec = sr.Recognizer

port = "COM5"
speed = 9600

wit_access_token = 'I74NFKU4GZJ72MHATBITSMZWPU4M6YH6'
client = Wit(wit_access_token)


###################### FALA DO PROGRAMA ############################

def sayHNIGGA():
    playsound.playsound('hinigga.mp3')

def sayIAMHEAR():
    playsound.playsound('hearyou.mp3')

def sayLIGHTON():
    playsound.playsound('lighton.mp3')

def sayLIGHTOFF():
    playsound.playsound('lightoff.mp3')

def sayFANON():
    playsound.playsound('fanon.mp3')

def sayFANOFF():
    playsound.playsound('fanoff.mp3')





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

def RecognizeSpeechValue(AUDIO_FILE):
    with open(AUDIO_FILE, 'rb') as audio:
        result = client.speech(audio,None,{'Content-Type':'audio/wav'})
        print(result)
        jsondump = json.dumps(result)
        jsonloads = json.loads(jsondump)
        entities = jsonloads['entities']
        intent = entities['intent']
        value = json.dumps(intent[0])
        value = json.loads(value)
        value = value['value']
        return value

def RecognizeSpeech(AUDIO_FILE):
    print('Iniciando o processo de speech')
    with open(AUDIO_FILE, 'rb') as f:
        result = client.speech(f,None,{'Content-Type':'audio/wav'})
    print('obtive a resposta')
    data = result
    print(data)
    jsondump = json.dumps(result)
    jsonloads = json.loads(jsondump)
    text = jsonloads['_text']
    return text





def onLIGTH():
    conection = serial.Serial(port, speed)
    time.sleep(2)
    conection.write(str.encode('A'))
    sayLIGHTON()


def offLIGTH():
    conection = serial.Serial(port, speed)
    time.sleep(2)
    conection.write(str.encode('B'))
    sayLIGHTOFF()


def onFAN():
    conection = serial.Serial(port, speed)
    time.sleep(2)
    conection.write(str.encode('C'))
    sayFANON()


def offFAN():
    conection = serial.Serial(port, speed)
    time.sleep(2)
    conection.write(str.encode('D'))
    sayFANOFF()




while True:
    repeat = True
    print('I am hear you...')
    audio = record_audio(2,'speack.wav')
    recog = RecognizeSpeech('speack.wav')
    os.remove('speack.wav')
    if(recog == 'hello'):
        print(recog)
        sayHNIGGA()
        time.sleep(0.7)
        while repeat:
            sayIAMHEAR()
            record_audio(3, 'choice.wav')
            recog = RecognizeSpeechValue('choice.wav')
            os.remove('choice.wav')
            if( recog == 'turn on lamp'):
                print('Ligou a lampada')
                onLIGTH()
                repeat = False;
            elif(recog == 'turn off lamp'):
                print('Desligou a lampada')
                offLIGTH()
                repeat = False
            elif (recog == 'turn on fan'):
                onFAN()
                repeat = False
            elif (recog == 'turn off fan'):
                print('Desligou o ventilador')
                offFAN()
                repeat = False


