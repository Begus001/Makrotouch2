from kivy.app import App
from kivy.core.window import Window
from screens.control_screen import ControlScreen

Window.size = (1024, 600)
Window.borderless = True


class Main(App):
	def build(self):
		return ControlScreen()


if __name__ == '__main__':
	Main().run()
