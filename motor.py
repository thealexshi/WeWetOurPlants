class MotorDriver(object):
	def __init__(self, gpio_object):
		self.gpio = gpio_object
		self.gpio.setmode(self.gpio.BOARD)
		# Motor 1 setup.
		self.gpio.setup(7, self.gpio.OUT)
		self.gpio.setup(11, self.gpio.OUT)
		self.gpio.setup(12, self.gpio.OUT)
		# Motor 2 setup.
		self.gpio.setup(15, self.gpio.OUT)
		self.gpio.setup(16, self.gpio.OUT)
		self.gpio.setup(18, self.gpio.OUT)
		# Motor 3 setup.
		self.gpio.setup(31, self.gpio.OUT)
		self.gpio.setup(33, self.gpio.OUT)
		self.gpio.setup(35, self.gpio.OUT)
		# Set stand by pins.
		self.gpio.setup(29, self.gpio.OUT)
		self.gpio.setup(13, self.gpio.OUT)
	
	def set_direction(self, motor_name, direction):
		is_clockwise = (direction == "clockwise")

		first = self.gpio.HIGH if is_clockwise else self.gpio.LOW
		second = self.gpio.LOW if is_clockwise else self.gpio.HIGH

		print("clockwise", is_clockwise, "first", first, "second", second)

		if motor_name == "1":
			print("Fertilizer motor")
			self.gpio.output(12, first) # Set AIN1
			self.gpio.output(11, second) # Set AIN2
		elif motor_name == "2":
			print("Water motor")
			self.gpio.output(15, first) # Set BIN1
			self.gpio.output(16, second) # Set BIN2
		elif motor_name == "3":
			self.gpio.output(31, first) # Set BIN1
			self.gpio.output(33, second) # Set BIN2

	def motor_move(self, motor_name):
		self._stand_by()
		if motor_name == "1":
			self.gpio.output(7, self.gpio.HIGH) # Set PWMA
		elif motor_name == "2":
			self.gpio.output(18, self.gpio.HIGH) # Set PWMB
		elif motor_name == "3":
			self.gpio.output(35, self.gpio.HIGH) # Set PWMB
		self._stand_by()

	def motor_stop(self, motor_name):
		if motor_name == "1":
			self.gpio.output(7, self.gpio.LOW) # Set PWMA
		elif motor_name == "2":
			self.gpio.output(18, self.gpio.LOW) # Set PWMB
		elif motor_name == "3":
			self.gpio.output(35, self.gpio.LOW) # Set PWMB
		self._un_stand_by()

	def _stand_by(self):
		self.gpio.output(13, self.gpio.HIGH)
		self.gpio.output(29, self.gpio.HIGH)

	def _un_stand_by(self):
		self.gpio.output(13, self.gpio.LOW)
		self.gpio.output(29, self.gpio.LOW)

	def clean_up(self):
		self.gpio.output(12, self.gpio.LOW) # Set AIN1
		self.gpio.output(11, self.gpio.LOW) # Set AIN2
		self.gpio.output(7, self.gpio.LOW) # Set PWMA
		self.gpio.output(13, self.gpio.LOW) # Set STBY
		self.gpio.output(15, self.gpio.LOW) # Set BIN1
		self.gpio.output(16, self.gpio.LOW) # Set BIN2
		self.gpio.output(18, self.gpio.LOW) # Set PWMB
		self.gpio.output(29, self.gpio.LOW)
		self.gpio.output(31, self.gpio.LOW)
		self.gpio.output(33, self.gpio.LOW)
		self.gpio.output(35, self.gpio.LOW)

		
	
