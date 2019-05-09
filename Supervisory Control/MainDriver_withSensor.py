import SocketServer as socketserver
import sys
import threading
import cv2
import numpy as np
import socket
import time
from Dynamics import *
from ImageProcessing import *


class SensorHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		 global distance
		 global previous_distance
		 distance = 100
		 while True:
			 self.raw_distance = self.request.recv(1024)
			 previous_distance = distance
			 distance = round(float(self.raw_distance),1)
			 print("Distance Ahead: ", distance)
			  
    
class VideoStreamHandler(socketserver.StreamRequestHandler):
	command = Dynamics()
	identify_features= features()
	print("Video Server Active")
	
	
	
	def handle(self):
		global command
		global distance
		global previous_distance
		stream_bytes = b''
		AEB = 0;
		try:
			while True:
	
				stream_bytes += self.rfile.read(1024)
				first = stream_bytes.find(b'\xff\xd8')
				last = stream_bytes.find(b'\xff\xd9')
				if first != -1 and last != -1:
					jpg = stream_bytes[first:last + 2]
					stream_bytes = stream_bytes[last + 2:]
					
					#read images in stream
					img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
					
					#Perspective Transform
					src = np.float32([[00,100],[320,100],[-10,150],[330,150]]) 
					dst = np.float32([[0,0],[320,0],[0,240],[320,240]])
					M = cv2.getPerspectiveTransform(src,dst)
					image = cv2.warpPerspective(img,M,(320,240))
					
					#Image Processing -Identify Features
					img, image, stop, average_heading, sigFlag, carFlag = self.identify_features.haar(img, image)
					
					#Display Processed Images and views
					cv2.imshow('Feild Of View', img )
					cv2.imshow('Birds Eye', image ) #img
					
					#HC-SR04 distance data
					a = (previous_distance + distance)/2
					b = previous_distance - distance
					
					
					if distance<25: #Object under threshold distance
						AEB = 1; #Emergency Brakes Flag
					else:
						AEB = 0;
					
					if cv2.waitKey(3) & 0xFF == ord('q'):
						break
					
					if sigFlag == 0: # Signal is Green
						
						#Set Lane Departure limits
						if ((average_heading <150) and (stop ==0)) and AEB == 0:
							print("Turn left")
							self.command.fleft();
						elif ((average_heading >170) and (stop==0))and AEB == 0:
							print("Turn right")
							self.command.fright();
						elif ((170>= average_heading >=150) and (stop ==0)) and AEB == 0:
							print("In lane")
							self.command.forward();
						elif stop==1:
							print("BRAKES ACTIVE due to Stop sign")
							self.command.brake();
						elif AEB == 1:
							self.command.brake()
							if carFlag == 1: #If car spotted
								print("Car Ahead at "+ str(distance)+ " cm")
							else:
								print("Obstacle Ahead!, Emergency Brakes Active")
						else:
							pass
					elif sigFlag ==1: # Signal is Red
						pass
						print("Signal Red, waiting to turn Green...")
						self.command.brake();
		finally:
			cv2.destroyAllWindows()
			self.command.halt()
			self.command.closeconn()
			sys.exit()

class Server(object):
    def __init__(self, host, vid_port, sensor_port):
        self.host = host
        self.port1 = vid_port
        self.port2 = sensor_port

    def video_stream(self, host, port):
        s = socketserver.TCPServer((host, port), VideoStreamHandler)
        s.serve_forever()

    def sensor_stream(self, host, port):
        s = socketserver.TCPServer((host, port), SensorHandler)
        s.serve_forever()

    def start(self):
        sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port2))
        sensor_thread.daemon = True
        sensor_thread.start()
        print('Sensor Server Active')
        self.video_stream(self.host, self.port1)


if __name__ == '__main__':
    host = '141.219.226.5'
    vid_port = 8000
    sensor_port = 8008
    print('Starting All Servers')
    servers = Server(host, vid_port, sensor_port)
    servers.start()
