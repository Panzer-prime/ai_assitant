import speech_recognition as sr


r = sr.Recognizer()

def get_mic():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mic_list):
            print(f"{index}: {name}")  
        return sr.Microphone(device_index=3) 
    except Exception as e:
        print(f"Error detecting microphones: {e}")
        return None

def listen():
    mic = get_mic()
    if not mic:
        print("No microphone detected!")
        return None
    
    with mic as source:
        print("Listening... (Start speaking)")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing audio...")

            # Recognizing speech
            transpiled_text = r.recognize_google(audio)
            print(f"You said: {transpiled_text}")
            return transpiled_text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Request error: {e}")


