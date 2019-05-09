# ActiveSafety
## Integration of Active Safety and ADAS in a 1/14th scale vehicle
### Introduction:
This project aims at integration of advanced driver assistance and active safety features in a 1/14th scale RWD vehicle. The project is developed in Python 3.7 programming environment. All the test conditions can be observed in the brief video below:


### Trying it yourself:
For building the project, there are four stages. First is be to assemble the hardware, second is designing the test track, third is to write and compile the programs, servers, clients and arduino and fourth is testing. Hardware used for the project is explained below:

### Hardware:
1. Raspberry Pi (preferably the latest model)
2. Arduino Uno (suitable for this application)
3. L298 H-Bridge circuit to control the drive and steer motors
4. HC-05 Bluetooth Module for serial communication
5. Pi Camera for Computer Vision and image processing
6. An RC Vehicle (1/14th scale or smaller)
7. Powerbank for Raspberry Pi
8. HC-SR04 Ultrasonic distance sensor
9. A laptop computer

Complete the hardware setup as per the image shown below:
![Schematic Diagram](https://user-images.githubusercontent.com/41763883/57438424-ded4a880-7211-11e9-8014-297d041e9ec8.png)

### Setting up the communication:
#### Bluetooth Serial:
Connect the HC-05 Rx and Tx to Arduino Rx and Tx, hold down on the key and power on the module to go in the AT mode. On the serial bus monitor, use the AT commands to override the default baud rate of the HC-05 module with 115200 Mbps Baud Rate. For Linux, setup the bluetooth serial by first pairing with the HC-05 module and then binding the module to an available channel using:
`$ sudo rfcomm release 0` followed by 
`$ sudo rfcomm bind 0 <mac address of HC-05>`
Once the Bluetooth is setup, flash the Arduino with the VehicleDynamics.ino
#### 
