import os
import cv2
import serial
import time

# capture webcam as video
face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
cap = cv2.VideoCapture(0)
ser = ''

# on startup, light up 1 led
def startup():
    # get serial port from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

    # turn on 1 led to show working
    ser.write(b'1')
    time.sleep(2)
    ser.write(b'0')
    time.sleep(2)

def lookForFace():
    # loop of reading frame by frame from webcam
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # light if there is a face, no light if there isnt a face
        print(len(faces))
        if (len(faces) == 0 ):
            #ser.write(b'1')
            print('Face detected: led OFF')
        else:
            #ser.write(b'0')
            print('Face detected: led ON')

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('img', img)
        # stop on escape key
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

def run():
    #startup()
    lookForFace()
    cap.release()

run()
