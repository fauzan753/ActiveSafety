import socket
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)

# create a socket and bind socket to the host

Host = '192.168.0.102'
Port = 2005
s = socket(AF_INET, SOCK_STREAM)
s.connect((Host, Port))

# Setup RPi GPIO pins for HC-SR04
Trig = 18
Echo = 16
gpio.setmode(gpio.BOARD)
gpio.setup(Trig, gpio.OUT)
gpio.output(Trig, 0)
gpio.setup(Echo, gpio.IN)
time.sleep(0.1)

def distance():
	
	# Trigger high for 10 microseconds
	gpio.output(Trig, 1)
	time.sleep(0.00001)
	gpio.output(Trig,0)
	while gpio.input(Echo) ==0:
        start =time.time()
	
	# Listen to Echo
	while gpio.input(Echo) == 1:
		stop = time.time()
	
	# Calculate Distance
	d= ((stop-start) * 17000) #in cms

	return (d)

try:
    while True:
        d = distance()
        print "Distance : %.1f cm" % distance
        
        # send data to the host every 0.2 sec
        s.send(str(d))
        time.sleep(0.2)
finally:
    s.close()
    GPIO.cleanup()
