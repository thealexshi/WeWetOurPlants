import subprocess
import os
import time

class Camera(object):
	def __init__(self, img_dir):
		self.image_dir = img_dir

	def snap(self, file_name):
		print(self.image_dir + file_name)
		full_file_name = os.getcwd() + "/" + self.image_dir + file_name
		iterations = 0
		while not os.path.isfile(full_file_name):
			subprocess.check_call(['fswebcam', full_file_name],
					stdout=subprocess.PIPE,
					stderr=subprocess.STDOUT)
			iterations += 1
			time.sleep(2)
			if iterations > 10:
				print("Failed to read from camera driver")
				return
		print("We took a picture with " + str(iterations) + " iterations")
		
		
	def clear_pics(self):
		folder = os.getcwd() + "/" + self.image_dir
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print(e)
