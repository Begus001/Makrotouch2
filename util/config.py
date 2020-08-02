from util.json_loader import JsonLoader


class Config:
	config_location = 'config.json'
	config = JsonLoader.load_file(config_location)
