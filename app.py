from kivy.app import App
from kivy.core.window import Window
from screens.control_screen import ControlScreen
from util.json_loader import JsonLoader
from util.config import Config
from util.control_connection import ControlConnection

Window.size = (Config.config['windowWidth'], Config.config['windowHeight'])
Window.borderless = Config.config['borderless']


class Main(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.controlScreen = ControlScreen()
		self.macroConnection = ControlConnection(self.cbConnectionStateChanged)
	
	def build(self):
		print('Drawing ControlScreen')
		return self.controlScreen
	
	def cbConnectionStateChanged(self):
		self.controlScreen.macroConnected = True
		self.controlScreen.updateConnectedLabel()


if __name__ == '__main__':
	main = Main()
	main.run()
