import serial
from serial import Serial
import time

class Dynamics(object):
    """docstring for Dynamics."""
    def __init__(self):
        global ser
        ser = serial.Serial("/dev/rfcomm1", 115200, timeout = 1)
        print("Dynamics Object Created")
        ser.write(chr(0).encode())
        
    def forward(self):
        ser.write(chr(1).encode())
                
    def fright(self):
        ser.write(chr(6).encode())
        
    def fleft(self):
        ser.write(chr(5).encode())
		
    def brake(self):
        ser.write(chr(9).encode())
        
    def halt(self):
        ser.write(chr(0).encode())
        
    def closeconn(self):
		ser.close()
