from Adafruit_BNO055 import BNO055
import Adafruit_PCA9685
import picamera
import picamera.array
from threading import Thread

from outils import *
import time

class Axionaut():

	def __init__(self, pwm_freq=60, max_speed_rate=0.5, cam_resolution=(250,150),fps=60,curve_factor=0.5):
		"""Method to create a new Axionaut vehicle"""
		pwm = Adafruit_PCA9685.PCA9685()
		self.pwm = pwm.set_pwm_freq(pwm_freq)
		self.max_speed = max_speed_rate
		self.state = 'stopped'
		self.model_loaded = False
		self.curve_factor = curve_factor
	    cam = picamera.PiCamera(framerate=fps)
	    time.sleep(3)
    	cam.resolution = cam_resolution
    	cam_output = picamera.array.PiRGBArray(cam, size=cam_resolution)
    	self.camera = cam
    	self.cam_output = cam_output
    	print('Axionaut created. Hardware ready.')


    def set_commands(self, commands):
    	"""Set global PWM config parameters"""
    	self.commands = commands


    def autopilot(self, model):
    	"""Set car to autopilot mode. Won't start until calling """
    	# Wrap model
    	self.model = model
    	self.graph = graph
    	self.model_loaded = True

    	# Starting camera thread
    	camera_thread = Thread(target=autopilot_loop, 
    							args=(self))
		camera_thread.start()

	def start(self):
		self.state = 'started'
		

	def train(self):
		# starting camera thread
		camera_thread = Thread(target=training_loop, 
								args=(self))
		camera_thread.start()
		

	def close(self):
		""" Method to close the Axionaut ans stop the camera thread"""
		# Kill the thread 888!crtl
	    self.state = 'stopped'
    	camera_thread.join()
  		print('Axionaut stopped')

