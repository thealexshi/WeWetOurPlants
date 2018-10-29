from mongo_driver import MongoDriver
import os

mongo_driver = MongoDriver(os.environ['MONGOCLIENT'])
mongo_driver.delete_all()

