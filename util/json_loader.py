import json
import os


class JsonLoader:
	# Loads json file
	@staticmethod
	def load_file(file):
		assert os.path.exists(file)
		with open(file) as f:
			json_file = json.load(f)
		
		return json_file
