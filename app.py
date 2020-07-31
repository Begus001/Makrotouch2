from kivy.app import App
from kivy.core.window import Window
from screens.control_screen import ControlScreen
from util.json_loader import JsonLoader
from util.config import Config
from util.control_connection import ControlConnection

# Fetch data from config file
Window.size = (Config.config['windowWidth'], Config.config['windowHeight'])
Window.borderless = Config.config['borderless']


class Main(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.controlScreen = ControlScreen()
		self.macroConnection = ControlConnection(self.cbConnectionStateChanged)  # Create new connection with callback function
	
	def build(self):
		return self.controlScreen
	
	# Set connection to control application to true and update label
	def cbConnectionStateChanged(self):
		self.controlScreen.macro_connected = True
		self.controlScreen.update_connected_label()


if __name__ == '__main__':
	main = Main()
	main.run()
