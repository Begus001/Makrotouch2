import json


class JsonLoader:
	@staticmethod
	def loadIcons():
		with open("macros.json") as f:
			macros = json.load(f)
		
		return macros
