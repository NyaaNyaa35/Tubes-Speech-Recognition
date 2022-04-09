from importlib.resources import path
import speech_recognition as sr
import webbrowser as web


def main():

    pathChrome = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Say Something")

        audio = r.listen(source)

        print("Recognizing Now")

        try:
            dest = r.recognize_google(audio)
            print("U Said ===> "+dest)
            web.get(pathChrome).open(dest)
        except Exception as e:
            print("Error : " + str(e))

if __name__ == "__main__":
    main()
