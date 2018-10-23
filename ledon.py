import speech_recognition as sr
import pyaudio
import time
import serial
from gtts import gTTS
import playsound
import os

def sayHNIGGA():
    playsound.playsound('hinigga.mp3')

def sayIAMHEAR():
    playsound.playsound('hearyou.mp3')

def sayLIGHTON():
    playsound.playsound('lighton.mp3')

def sayLIGHTOFF():
    playsound.playsound('lightoff.mp3')

def sayFANON():
    playsound.playsound('faon.mp3')

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


port = "COM5";
speed = 9600;

def onLIGTH():
    conection = serial.Serial(port, speed)
    sayLIGHTON()
    conection.write(str.encode('A'))
    conection.close()

def offLIGTH():
    conection = serial.Serial(port, speed)
    sayLIGHTOFF()
    conection.write('B')
    conection.close()

def onFAN():
    conection = serial.Serial(port, speed)
    sayFANON()
    conection.write('C')
    conection.close()

def offFAN():
    conection = serial.Serial(port, speed)
    sayFANOFF()
    conection.write('D')
    conection.close()





rec = sr.Recognizer()
while True:
    repeat = True
    print("Hear you")
    with sr.Microphone() as fala:
        voice = rec.listen(fala)
        choice = rec.recognize_sphinx(voice)
        if(choice == "hello"):
            print(choice)
            sayHNIGGA();
            time.sleep(2)
            while repeat:
                sayIAMHEAR()
                with sr.Microphone() as fala:
                    print("Speack")
                    voice = rec.listen(fala)
                    choice = rec.recognize_sphinx(voice)
                    choice = rec.recognize_sphinx(voice)
                    print(choice)
                    if("on" in choice):
                        onLIGTH()
                        print(choice)
                        repeat = False
                    elif( "off" in choice):
                        offLIGTH()
                        repeat = False
                    elif ("on fan" in choice):
                        onFAN()
                        repeat = False
                    elif ("off fan" in choice):
                        offFAN()
                        repeat = False
                print(choice)