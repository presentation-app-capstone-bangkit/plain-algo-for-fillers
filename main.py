import speech_recognition as sr
import re

def count_words(text):
    return len(text.split())

def calculate_pace(word_count, duration):
    if duration == 0:
        return 0
    return (word_count / duration) * 60  # WPM


def detect_fillers(text):
    pattern = r'\b(?:aaaa|uhmm|mmm|ya|kayak apa ya|apasih namanya|em|e|jadi|so|then|uh|um|like)\b' # masih nyampur en id, vocab masih kurang
    filler_words = re.findall(pattern, text, re.IGNORECASE) # cari pattern pake regex
    return len(filler_words)


recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Waiting a sec, preparing the mic")

try:
    with mic as source:
        # Adjust ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        # Record audio
        print("Listening...")
        audio = recognizer.record(source, duration=10) #pake .record biar bisa set duration, kalau pake .listen() sering timeout

      
        text = recognizer.recognize_google(audio, language='id-ID') #api google
        print(f"Recognized Text: {text}")

        duration = len(audio.frame_data) / audio.sample_rate / audio.sample_width 

        word_count = count_words(text)
        filler_count = detect_fillers(text)
        pace = calculate_pace(word_count, duration)

       
        print(f"Word Count: {word_count}")
        print(f"Filler Words Count: {filler_count}")
        print(f"Speech Pace: {pace:.2f} words per minute")

except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
    print("Sorry, there was an error with the request.")
except Exception as e:
    print(f"An error occurred: {e}")