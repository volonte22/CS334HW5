import serial
import time
import faceRec as FR

# on startup, light up 1 led
def startup():
    # get serial port from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

    # turn on LED
    ser.write(b'1')

# if face is shown, send 2 light up
def ifFace():
    if FR.faceShown

