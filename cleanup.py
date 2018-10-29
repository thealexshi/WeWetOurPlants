import RPi.GPIO as GPIO
from motor import MotorDriver
from color import ColorSensor
import Adafruit_TCS34725


motor_driver = MotorDriver(GPIO)
motor_driver.clean_up()
sensor = ColorSensor(Adafruit_TCS34725)
sensor.clean_up()
