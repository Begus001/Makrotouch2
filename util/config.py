from util.json_loader import JsonLoader


class Config:
	configLocation = 'config.json'
	config = JsonLoader.loadFile(configLocation)
