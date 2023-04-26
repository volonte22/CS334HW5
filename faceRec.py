import cv2
import sys
import serial
import time

# serial ports connected to arduino
# com4/com5 corresponding to placements on arduino
ser1 = serial.Serial('COM4', 9800, timeout=1)
ser2 = serial.Serial('COM5', 9800, timeout=1)

# create a face cascade
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
# initalize video_capture
video_capture = cv2.VideoCapture(0)
# intialize boolean variable for output
outputBool = False

def getFace():
    # turn led 1 on
    ser1.writelines(b'H')
    
    # while we want to read in data, read it in
    while True:
        # get frame by frame data
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        
        if ( faces == null ) {
            ser2.writelines(b'L')
        } else {
            ser2.writelines(b'H')
        }

        # draw rect
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # visualize frame
        cv2.imshow('Video', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        

