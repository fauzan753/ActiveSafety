import sys
import pygame
from pygame.locals import *
import socket
from serial import Serial
import serial

pygame.init()
screen = pygame.display.set_mode((600,400))

ser = serial.Serial("/dev/rfcomm1", 115200, timeout = 1)
print(ser.name)


loop_label = True

while loop_label:
    #sending moving command to Arduino
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                print("Forward Left")
                ser.write(chr(5).encode())
               
            elif key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                print("Forward Right")
                ser.write(chr(6).encode())
               
            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                print("Reverse Left")
                ser.write(chr(7).encode())
                
            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                print("Reverse Right")
                ser.write(chr(8).encode())
               
            elif key_input[pygame.K_UP]:
                print("Forward")
                ser.write(chr(1).encode())
                
            elif key_input[pygame.K_DOWN]:
                print("Reverse")
                ser.write(chr(2).encode())
               
            elif key_input[pygame.K_LEFT]:
                print("Left")
                ser.write(chr(3).encode())
                
            elif key_input[pygame.K_RIGHT]:
                print("Right")
                ser.write(chr(4).encode())
               
            elif key_input[pygame.K_q]:
                print("Quit system")
                ser.write(chr(0).encode())
               
                loop_label = False
                ser.close()
               
                break
        elif (event.type == pygame.KEYUP):
            ser.write(str(0).encode())
          
