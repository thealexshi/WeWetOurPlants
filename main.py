from motor import MotorDriver 
from color import ColorSensor 
from camera import Camera
from mongo_driver import MongoDriver
import RPi.GPIO as GPIO
import Adafruit_TCS34725
import smbus
import time
import os

mongo_driver = MongoDriver(os.environ['MONGOCLIENT'])
motor_driver = MotorDriver(GPIO)
sensor = ColorSensor(Adafruit_TCS34725)
camera = Camera("pics/")

def initial_scan():
	for i in range(4):
		move_until_black_line(motor_driver, sensor, time)
		time.sleep(1)
		camera.snap("plant" + str(i))
	motor_driver.motor_move("3")
	time.sleep(0.7)
	motor_driver.motor_stop("3")
	mongo_driver.upload_images(['./pics/plant0', './pics/plant1', './pics/plant2', './pics/plant3'])

def move_back():
	for i in range(5):
		move_until_black_line(motor_driver, sensor, time, "other way")
		time.sleep(1)
	
def get_results_and_water():
	for i in range(0, 4):
		result = mongo_driver.get_plant(i)
		print(result)
		if result:
			move_until_black_line(motor_driver, sensor, time)
			if 'water' in result and result['water'] == True:
				dispense_liquid(motor_driver, "water", time)
			if 'fertilizer' in result and result['fertilizer'] == True:
				dispense_liquid(motor_driver, "fertilizer", time)

def move_until_black_line(motor_driver, sensor, time_obj, direction="clockwise"):
	motor_driver.set_direction("3", direction)
	motor_driver.motor_move("3")
	time_obj.sleep(0.3)
	while (sensor.get_lux() >= 5): 
		continue
	motor_driver.motor_stop("3")

def dispense_liquid(motor_driver, liq_type, time_obj):
	motor_num = "1" if liq_type == "fertilizer" else "2"
	print("Dispensing " + liq_type + "\n")
	motor_driver.set_direction(motor_num, "clockwise")
	motor_driver.motor_move(motor_num)
	time_obj.sleep(3)
	motor_driver.motor_stop(motor_num)
	time_obj.sleep(3)


while True:
	initial_scan()
	move_back()
	while not mongo_driver.contains_results(): 
		time.sleep(5)
		continue	
	get_results_and_water()
	move_back()
	mongo_driver.delete_all()
	camera.clear_pics()
	time.sleep(120)
