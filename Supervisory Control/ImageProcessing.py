import numpy as np
import cv2
import time 

#Load Haar Cascades
stop_cascade = cv2.CascadeClassifier('Stopsign_HAAR.xml')
car_cascade = cv2.CascadeClassifier('Cars_HAAR2.xml')
tsignal= cv2.CascadeClassifier('TrafficSignal_HAAR.xml')

class features(object):
	
	def __init__(self):
		self.stop= 0
		self.sigFlag = 0
		self.first_detect=1
		self.red_detect=0
		self.carSig = 0
			
	def haar(self, img, image):
		self.image =img
		self.gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# Region of Interest
		graycopy = self.gray[:150, : ]
		self.Pers = image
		gray_cars= self.gray[10:160,50:270]
		
		self.stops = stop_cascade.detectMultiScale(self.gray, 1.2, 3)
		self.cars = car_cascade.detectMultiScale(gray_cars, scaleFactor=1.1, minNeighbors=3, minSize=(40,40))
		self.TSig = tsignal.detectMultiScale(graycopy, scaleFactor= 1.1,minNeighbors=9, maxSize=(30,80) )	
					
		# Color Segmentation
		hsv_img = cv2.cvtColor(self.Pers, cv2.COLOR_BGR2GRAY)
		mask_white = cv2.inRange(hsv_img, 100, 255)
		canny_image = cv2.Canny(mask_white, 50, 150)
		blur= cv2.GaussianBlur(canny_image,(5,5),0)
		black= np.zeros_like(blur)
		centre=[]
		
		# Sliding Window 
		for i in range(3,11):
			p = (20*i)+15
			q = p-5
			roi_l = blur[q:p, 0:160]
			roi_r = blur[q:p, 160:320]
			(minVal, maxVal, minLoc, maxLoc_l) = cv2.minMaxLoc(roi_l)
			(minVal, maxVal, minLoc, maxLoc_r) = cv2.minMaxLoc(roi_r)

			cv2.circle(self.Pers,(80+int((maxLoc_l[0]+maxLoc_r[0])/2),p),5,(255,0,0),2)
			centre.extend((80+int((maxLoc_l[0]+maxLoc_r[0])/2),p))
		
		# Average Heading Direction	
		self.average_heading =	int((centre[0] +centre[2] +centre[4])/3)

		
		# Identify stops
		try:
			for (x,y,w,h) in self.stops:
				cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),2)
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(self.image,'STOP',(x+3,y+h-3),font,0.3,(0,0,255),1)
				print("stop detected ", w)
				if  (w>35) and (self.first_detect==1): #Stop width threshold
					self.stop =1
					self.stop_start = cv2.getTickCount() #Start Counter
					self.first_detect=0
					
				self.stop_now=  cv2.getTickCount()
				self.stop_time = (self.stop_now -self.stop_start)/ cv2.getTickFrequency() # Time spent
				print("elapsed time at stop= ",self.stop_time)
				
				# if waited for 5 seconds true	
				if self.first_detect==0 and self.stop_time > 5:
					print("Waited for 5 seconds")
					self.stop = 0
					self.sigFlag=0
		except:
			pass
		
		# Identify traffic signals
		try:
			for (x,y,w,h) in self.TSig:
				
				#rgion of Interest
				roi2= self.gray[y:y+20 ,x:x+w]
				roi = img[y:y+30, x:x+w]
				img_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
				
				mask1 = cv2.inRange(img_hsv, (0,40,70), (20,255,255))
				mask2 = cv2.inRange(img_hsv, (170,40,70), (180,255,255))

				mask = cv2.bitwise_or(mask1, mask2 )
				red= np.sum(mask ==255) 
				
				mask3 = cv2.inRange(img_hsv, (60,50,50), (120,255,255))
				green=np.sum(mask3==255)
				
				circles = cv2.HoughCircles(roi2, cv2.HOUGH_GRADIENT, 1, 10,
				  param1=100,
				  param2=12,
				  minRadius=4,
				  maxRadius=15)
				
				circles = np.uint16(np.around(circles))[0][0]
				radius = circles[2]
				
				signal_distance= float(round((304*0.5)/(2*radius),1))
				Signal_distance =str(signal_distance) + str(" in")
				
				
				if red >= 50:
					signal = "RED"
					if signal_distance <= 16:# if Red signal within threshold, raise flag
						self.sigFlag = 1
						red_detect=1
						
				else:
					signal = "GREEN"
					self.sigFlag = 0
				
				cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),2)
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(self.image,signal,(x+3,y+h-5),font,0.3,(0,0,255),1)
				cv2.putText(self.image,Signal_distance,(x, y+h+10),font,0.3,(0,0,255),1)
		except:
			if self.red_detect==1:
				self.sigFlag=1
			pass 
					
		# identify cars
		try:
			for (x2,y2,w2,h2) in self.cars:
				
				#detection in ROI
				cv2.rectangle(self.image,(50+x2,10+y2),(50+x2+w2,10+y2+h2),(255,200,50),2)
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(self.image,'CAR',(x2+3,y2+h2-3),font,0.3,(255,200,50),1)
				self.carSig = 1;
		except:
			self.carSig = 0;
			
		return (self.image, self.Pers, self.stop, self.average_heading, self.sigFlag, self.carSig)
