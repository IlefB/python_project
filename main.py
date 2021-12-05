import numpy as np
import cv2
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import pywhatkit
import wikipedia
import smtplib
import winsound


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def time():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(date)
    speak(month)
    speak(year)

def wishme():
    hour = datetime.datetime.now().hour
    if hour >=1 and hour < 12:
        speak("bonjour madame ilef!")
    elif hour >=12 and hour <18:
        speak("bonsoir madame ilef")
    elif hour>=18 and hour <24:
        speak("bonne soirée madame ilef!")
    speak("comment je peux vous-aidez madame?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ecoute...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Reconnaitre")
        command = r.recognize_google(audio, language='fr-fr')
        command = command.lower()
        print(f"vous me dites: {command}")
    except Exception as e:
        print(e)
        speak("S'il vous plait répeter ce que vous dites!")
        return "None"
    command = command.lower()
    return command

def objectDetection():
    protxt_path = 'MobileNetSSD_deploy.prototxt'
    model_path = 'MobileNetSSD_deploy.caffemodel'
    min_confidence = 0.2
    classes = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat','chair',
               'cow', 'dinigtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

    np.random.seed(64321098)  # to give different color of rectangles
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    net = cv2.dnn.readNetFromCaffe(protxt_path, model_path)
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        height, width = img.shape[0], img.shape[1]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007, (300, 300), 130)
        net.setInput(blob)
        detected_object = net.forward()
        for i in range(detected_object.shape[2]):
            confidence = detected_object[0][0][i][2]
            if confidence > min_confidence:
                class_index = int(detected_object[0, 0, i, 1])
                upper_left_x = int(detected_object[0, 0, i, 3] * width)
                upper_left_y = int(detected_object[0, 0, i, 4] * height)
                lower_right_x = int(detected_object[0, 0, i, 5] * width)
                lower_right_y = int(detected_object[0, 0, i, 6] * height)

                predection_text = f"{classes[class_index]}: {confidence:.2f}%"
                cv2.rectangle(img, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
                cv2.putText(img, predection_text,(upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15),cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)
                speak(classes[class_index])
                cv2.imshow("object_detection", img)

        if cv2.waitKey(10) == ord("q"):
            break



def SendEmail():
    email = 'ilefbelaid33@gmail.com'
    password = 'ilef19belaid..'
    sendEmail = 'ilefbelaid33@gmail.com'
    speak("qu'est ce que vous veulez envoyer?")
    command2= takeCommand().lower()
    message = command2
    speak(message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, sendEmail, message)
    server.quit()
    speak("l'email envoyait")


if __name__ =="__main__":
    speak("Ton personnelle assistante dans ton service. S'il vous plaît dites-moi comment peux-je vous aider?")
    while True:
        command = takeCommand()
        if ("salut" in command):
            wishme()
        elif ("temps" in command):
            speak("Le temps maintenant est")
            time()
        elif ("date" in command):
            speak("La date d'aujourd'hui est")
            date()
        elif ("youtube" in command):
            speak("d'accord madame")
            pywhatkit.playonyt(command)
        elif ("chercher" in command):
            definition = command.replace("chercher", " ")
            info = wikipedia.summary(definition, sentences=1)
            print(info)
            speak(info)
        elif ("aller" in command):
            speak("i'm ready madame")
            objectDetection()
        elif ("aide" in command):
            winsound.PlaySound('alert.wav', winsound.SND_FILENAME)
            SendEmail()
        elif ("au revoir" in command):
            speak("aurevoir madame, je suis là quand vous avez besoin de moi.")
            break




