import cv2
import dlib
import time
from machine import Ping

# pin intialization
led_pin1 = machine.Pin(4, Pin.OUT)

# To install dlib, run:
# pip install cmake
# pip install dlib
# dlib takes awhile to install

# Set up the video capture object to use your laptop's built-in camera
cap = cv2.VideoCapture(0)

# Load the face and eye detection classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load the facial landmark predictor
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
detector = dlib.get_frontal_face_detector()

# Initialize variables for measuring FPS
prev_time = 0
fps = 0

# turn inital led on
led_pin1.value(1)

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    print(faces)
    if(len(faces) == 0):
        print("No faces")
        # turn led on
        led_pin2.value(1)
        time.sleep(1)
    else:
        # turn led off
        led_pin1.value(1)
        time.sleep(0.1)
        led_pin1.value(0)
        time.sleep(0.1)
        led_pin1.value(1)
        time.sleep(0.1)
        led_pine1.value(0)
        time.sleep(1)
        # Draw a rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Extract the face region of interest
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            text = f"Face Width: {w} | Face Height: {h}"
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Detect eyes in the face region of interest
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

            # Draw a rectangle around each detected eye
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

            # Use facial landmarks detection to check the position of the eyes
            dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
            landmarks = predictor(gray, dlib_rect)

            left_eye_pos = (landmarks.part(36).x, landmarks.part(36).y)
            right_eye_pos = (landmarks.part(45).x, landmarks.part(45).y)

            cv2.circle(frame, left_eye_pos, 2, (255, 0, 0), 2)
            cv2.circle(frame, right_eye_pos, 2, (255, 0, 0), 2)

            # If the eyes are too far apart or too close together, remove the face detection
            eye_dist = right_eye_pos[0] - left_eye_pos[0]
            if eye_dist > 2 * w or eye_dist < 0.5 * w:
                faces = []
     # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Add FPS counter to the frame
    fps_text = f"FPS: {int(fps)}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Check for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
# turn off leds
led_pin1.value(0)
time.sleep(2)
