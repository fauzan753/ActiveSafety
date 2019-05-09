# ActiveSafety
## Integration of Active Safety and ADAS in a 1/14th scale vehicle
![TestVehicle](https://user-images.githubusercontent.com/41763883/57440113-68d24080-7215-11e9-89b9-d99da377ed81.png)

![IMG_20190508_181845](https://user-images.githubusercontent.com/41763883/57440294-bfd81580-7215-11e9-8fae-067927ddc313.jpg)

![IMG_20190508_181710](https://user-images.githubusercontent.com/41763883/57440304-c36b9c80-7215-11e9-962d-af2e0a342387.jpg)

### Introduction:
This project aims at integration of advanced driver assistance and active safety features in a 1/14th scale RWD vehicle. The project is developed in Python 3.7 programming environment. All the test conditions can be observed in the brief video below:


### Trying it yourself:
For building the project, there are three stages. First is to assemble the hardware, second is to write and compile the programs, servers, clients and arduino and third is testing. Hardware used for the project is explained below:

### Hardware:
1. Raspberry Pi (preferably the latest model)
2. Arduino Uno (suitable for this application)
3. L298 H-Bridge circuit to control the drive and steer motors
4. HC-05 Bluetooth Module for serial communication
5. Pi Camera for Computer Vision
6. An RC Vehicle (1/14th scale or smaller)
7. Powerbank for Raspberry Pi
8. HC-SR04 Ultrasonic distance sensor
9. A laptop computer

Complete the hardware setup as per the image shown below:
![Schematic Diagram](https://user-images.githubusercontent.com/41763883/57438424-ded4a880-7211-11e9-8014-297d041e9ec8.png)

### Setting up the communication:
#### Bluetooth Serial:
For Linux, setup the bluetooth serial by first pairing with the HC-05 module and then binding the module to an available channel using:
`$ sudo rfcomm release 0` followed by 
`$ sudo rfcomm bind 0 <mac address of HC-05>`
Once the Bluetooth is setup, flash the Arduino with the VehicleDynamics.ino
#### Laptop Computer:
Copy all the files in the Supervisory controls folder in the same place on the Laptop Computer.
Run the MainDriver_withSensor.py on the laptop computer after making sure the bluetooth serial is working.
### Raspberry Pi:
Copy the two clients for the video and the sensor clients. Once the main server is active on the laptop computer, run the Distance_Pi_Client.py followed by the VideoStream_Pi_Client.py on separate terminals

Soon as the video stream starts, the vehicle will start following the track in lane keeping assist mode and detecting the stop signs, traffic signals and cars coming in the camera's FOV. 

### Lane Departure Warning System (LDWS):
To test LDWS, the vehicle has to be driven manually and the program will now throw warnings on the terminal window of the main server. The serial port needs to be deactivated to prevent automatic driving. 
To drive the vehicle manually, open Keyboard_Pygame.py on a separate terminal or a separate computer (preferable).

