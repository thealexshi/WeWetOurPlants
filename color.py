import smbus

class ColorSensor(object):
	def __init__(self, sensor_library):
		self.sensor_lib = sensor_library
		self.sensor = self.sensor_lib.TCS34725()
		self.sensor.set_interrupt(False)
	
	def get_rgb(self):
		return self.sensor.get_raw_data()

	def get_color_temp(self):
		r, g, b, c = self.sensor.get_raw_data()
		return self.sensor_lib.calculate_color_temperature(r, g, b)

	def get_lux(self):
		r, g, b, c = self.sensor.get_raw_data()
		return self.sensor_lib.calculate_lux(r, g, b)
	
	def clean_up(self):
		self.sensor.set_interrupt(True)
		self.sensor.disable()
		
