import json
import os


class JsonLoader:
	@staticmethod
	def loadFile(file):
		assert os.path.exists(file)
		with open(file) as f:
			macros = json.load(f)
		
		return macros
