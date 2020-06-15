from kivy.app import App
from kivy.core.window import Window
from screens.control_screen import ControlScreen
from util.json_loader import JsonLoader
from util.config import Config

Window.size = (Config.config['windowWidth'], Config.config['windowHeight'])
Window.borderless = Config.config['borderless']


class Main(App):
	def build(self):
		return ControlScreen()


if __name__ == '__main__':
	Main().run()
