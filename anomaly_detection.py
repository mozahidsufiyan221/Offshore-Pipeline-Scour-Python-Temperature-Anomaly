# Import Libraries
import os
import glob
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Initialize the GPIO Pins

GPIO.setup(24, GPIO.OUT) #Blue Light
GPIO.setup(18, GPIO.OUT) #RED Light
GPIO.setup(22, GPIO.OUT) #buzzer


os.system("modprobe w1-gpio") # Turns on the GPIO module
os.system("modprobe w1-therm") # Turns on the Temperature module

# Find the correct Device file that holds the temperature data
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"

# A function that reads the sensors data

def read_temp_raw():
	f = open(device_file, "r") # opens the temperature device file
	lines = f.readlines() # Returns the text
	f.close()
	return lines

# Convert the value of the sensor into a temperature

def read_temp():
	lines = read_temp_raw() # Read the temperature "device file"

	# While the first line does not contain "YES", wait for 0.2s
	# and then read the device file again.
	while lines[0].strip()[-3:] != "YES":
		time.sleep(0.2)
		lines = read_temp_raw()

	# Look for the position of the "=" in the second line of the evice file.

	equals_pos = lines[1].find("t=")

	# If the "=" is found, convert the rest of the line after the 
	# "=" into degrees Celsius, then degrees Fahrenheit

	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0/ 5.0 + 32.0
		return temp_c, temp_f

# Print out the temperature until the program is stopped
while True:
	temp_c, tempf = read_temp()
	print(temp_c)
	time.sleep(1)
	if temp_c > 28.0:
		
		print ("above 28")		
		GPIO.output(18, GPIO.HIGH) # Red Lights on
		GPIO.output(22, GPIO.HIGH) # Buzzer On
		time.sleep(0.5)
		GPIO.output(18, GPIO.LOW)  
		GPIO.output(22, GPIO.LOW)
	else:
		print ("below 28")
		GPIO.output(24, GPIO.HIGH) # Blue Lights On
		time.sleep(0.5)
		GPIO.output(24, GPIO.LOW)

GPIO.cleanup()
