from kivy.app import App
from kivy.core.window import Window
from screens.control_screen import ControlScreen
from util.json_loader import JsonLoader
from util.config import Config
from util.control_connection import ControlConnection

# Fetch data from config file
Window.size = (Config.config['windowWidth'], Config.config['windowHeight'])
Window.fullscreen = Config.config['fullscreen']
Window.borderless = Config.config['borderless']


class Main(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.control_screen = ControlScreen()
		self.connection = ControlConnection(self.control_screen)
		self.control_screen.connection = self.connection
	
	def build(self):
		return self.control_screen


if __name__ == '__main__':
	main = Main()
	main.run()
	main.connection.close()
