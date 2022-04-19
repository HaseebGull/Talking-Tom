import speech_recognition as sr
from translate import Translator
from pydub import AudioSegment
from playsound import playsound
import pyttsx3

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening.....")
    audio = r.listen(source, timeout=2)
    r.pause_threshold = 1
    r.energy_threshold = 300

    query = r.recognize_google(audio, language="en-US")
    translator = Translator(to_lang="Urdu")
    translation = translator.translate(query)
    print(f"you said: {query}\n")
    print("Done......")
    with open('speed.wav', 'wb') as f:
        f.write(audio.get_wav_data())

sound = AudioSegment.from_file('speed.wav', format="wav")
sound = sound + 25
octaves = 0.4

new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
hipitch_sound = hipitch_sound.set_frame_rate(44100)
hipitch_sound.export("output_pitch.wav", format="wav")
try:
    print(translation)
    engine = pyttsx3.init()
    engine.say(translation)
    engine.runAndWait()

    playsound(r"output_pitch.wav")`
except Exception as e:
    print("sorry cannot play")
