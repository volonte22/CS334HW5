import cv2
import sys

# create a face cascade
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
# initalize video_capture
video_capture = cv2.VideoCapture(0)
# intialize boolean variable for output
outputBool = False

def getFace():
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

        # draw rect
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # visualize frame
        cv2.imshow('Video', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

