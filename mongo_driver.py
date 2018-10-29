from pymongo import MongoClient
from bson import Binary, BSON

class MongoDriver(object):
	def __init__(self, client_string):
		self.mongo = MongoClient(client_string)
		self.db = self.mongo['plant_data']
		self.plant_images = self.db['plant_images']
		self.plant_results = self.db['plant_results']
	
	def upload_images(self, image_file_names):
		for idx, file_name in enumerate(image_file_names):
			image = open(file_name, "r")
			image_data = image.read()
			post = { "plant_number": idx, "data" : Binary(image_data) }
			post_id = self.plant_images.insert_one(post).inserted_id

	def get_plant(self, plant_number):
		result = self.plant_results.find_one({"plant_number" : plant_number})
		return result

	def contains_results(self):
		print("Waiting for database to be populated")
		result_set = set()
		for i in range(4):
			if self.get_plant(i):
				result_set.add(i)
		return len(result_set) >= 4

	def delete_all(self):
		print("Deleting everything!")
		self.plant_images.delete_many({})
		self.plant_results.delete_many({})
		

