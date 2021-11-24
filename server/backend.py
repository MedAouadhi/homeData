import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import json

class MyDB:
	app = None
	ref: str
	url: str

	def __init__(self, url):
		self.url = url
		# connec to the db
		if self.connect("/home/pi/homeData/server/creds.json"):
			print("Successfully connected to the DB.")

	def connect(self, cred_path):
		cred_obj = credentials.Certificate(cred_path)
		try:
			self.app = firebase_admin.initialize_app(cred_obj, {
				'databaseURL': self.url
			})
			self.ref = db.reference("/")
			return True
		except Exception as e:
			print("Error: could not connect " + e.__str__())
			return False

	# data is a dict
	def add_measurement(self, location, sensorType, value):
		now = datetime.now()
		current_time = now.strftime("%d-%m-%y:%H:%M:%S")
		valDict = {current_time: value}
		ref = db.reference("/" + location + "/" + sensorType + "/")
		try:
			ref.update(valDict)
			print("{} added to DB".format(valDict))
		except Exception as e:
			print("Error: Update problem: " + e.__str__())

	def get_all_measurments(self):
		return self.ref.get()
