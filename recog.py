#######          Imports     #################

import speech_recognition as sr
import json
import pyaudio
import wave
from wit import Wit
import playsound
import serial
import time
import os
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from record import record_audio
from record import read_audio
from pydub import AudioSegment



################################################

#######         Variables       ################

rec = sr.Recognizer

port = "COM5"
speed = 9600

wit_access_token = 'I74NFKU4GZJ72MHATBITSMZWPU4M6YH6'
clientwit = Wit(wit_access_token)

connection = serial.Serial("COM5", 9600)
time.sleep(2)

clientgoogle = speech.SpeechClient()

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='en-US')





#################################################

########## Say the program ######################


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


#################################################

########### Arduino Function ####################


def onLIGTH():
    connection.write(str.encode('A'))
    sayLIGHTON()


def offLIGTH():
    connection.write(str.encode('B'))
    sayLIGHTOFF()



def onFAN():
    connection.write(str.encode('C'))
    sayFANON()


def offFAN():
    connection.write(str.encode('D'))
    sayFANOFF()

##################################################


################## Speech Recog #################

def RecognizeText(TEXT_VALUE):
        result = clientwit.message(TEXT_VALUE)
        print(result)
        jsondump = json.dumps(result)
        jsonloads = json.loads(jsondump)
        entities = jsonloads['entities']
        intent = entities['intent']
        value = json.dumps(intent[0])
        value = json.loads(value)
        value = value['value']
        return value

def RecognizeSpeechGoogle(AUDIO_FILE):
    with io.open(AUDIO_FILE, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    response  = clientgoogle.recognize(config, audio)
    for result in response.results:
        return(format(result.alternatives[0].transcript))


####################################################

############# Code #################################


while True:
    repeat = True
    print('I am hear you...')
    #audio = record_audio(2,'speack.wav')
    #recog = RecognizeSpeechGoogle('speack.wav')
    rec = sr.Recognizer()
    with sr.Microphone() as audio:
        frase = rec.listen(audio)

    try:
        recog = rec.recognize_sphinx(frase)
        print(recog)
        if (recog == 'hello machine'):
            print(recog)
            sayHNIGGA()
            time.sleep(0.7)
            while repeat:
                sayIAMHEAR()
                record_audio(3, 'choice.wav')
                recog = RecognizeSpeechGoogle('choice.wav')
                print(recog)
                action = RecognizeText(recog)
                os.remove('choice.wav')
                if (action == 'turn on lamp'):
                    print('Ligou a lampada')
                    onLIGTH()
                    repeat = False;
                elif (action == 'turn off lamp'):
                    print('Desligou a lampada')
                    offLIGTH()
                    repeat = False
                elif (action == 'turn on fan'):
                    onFAN()
                    repeat = False
                elif (action == 'turn off fan'):
                    print('Desligou o ventilador')
                    offFAN()
                    repeat = False

    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))



######################################################