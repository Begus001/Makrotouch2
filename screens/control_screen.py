from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from util.json_loader import JsonLoader
from util.config import Config
from functools import partial
import math
import os
import requests


# Main screen
class ControlScreen(BoxLayout):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		# region Wrapper config
		self.orientation = 'vertical'
		self.spacing = 5
		# endregion
		
		# region Macro page config
		self.macro_cfg_location: str = 'macros.json'
		self.macros = JsonLoader.load_file(self.macro_cfg_location)  # Load configuration
		self.img_location = 'img/'
		self.page: int = 0
		self.num_macros: int = len(self.macros)
		self.cols: int = Config.config['macroCols']
		self.rows: int = Config.config['macroRows']
		self.page_size: int = self.cols * self.rows
		self.num_pages: int = math.ceil(self.num_macros / self.page_size) if len(self.macros) > 0 else 1  # Calculate number of pages if macros not empty, else set page to 1
		self.connected: bool = False
		self.connection = None
		# endregion
		
		# region Layout config
		self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.icon_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.icon_grid = GridLayout(cols=self.cols, size_hint=(0.8, 1))
		
		self.bt_exit = Button(background_normal='internal_img/exit.png', background_down='internal_img/exit.png', size_hint=(0.1, 1), on_press=self.exit)
		self.lb_page = Label(size_hint=(0.4, 1), font_size='20dp')
		self.lb_connected = Label(size_hint=(0.4, 1), font_size='20dp')
		self.bt_settings = Button(background_normal='internal_img/settings.png', background_down='internal_img/settings.png', size_hint=(0.1, 1))
		
		self.bt_prev = Button(text='<', size_hint=(0.1, 1), on_press=self.prev_page)
		self.bt_next = Button(text='>', size_hint=(0.1, 1), on_press=self.next_page)
		
		self.top_bar.add_widget(self.bt_exit)
		self.top_bar.add_widget(self.lb_page)
		self.top_bar.add_widget(self.lb_connected)
		self.top_bar.add_widget(self.bt_settings)
		
		self.add_widget(self.top_bar)
		
		self.icon_wrapper.add_widget(self.bt_prev)
		self.icon_wrapper.add_widget(self.icon_grid)
		self.icon_wrapper.add_widget(self.bt_next)
		
		self.add_widget(self.icon_wrapper)
		# endregion
		
		# region Update labels
		self.update_page_label()
		self.update_connected_label()
		# endregion
		
		self.init_macros()
	
	# Updates label that displays page number
	def update_page_label(self):
		print('Updating page label')
		self.lb_page.text = 'Page: ' + str(self.page + 1) + '/' + str(self.num_pages)
	
	# Updates label that indicates the connection status
	def update_connected_label(self):
		print('Updating connected label')
		self.lb_connected.text = 'Connected' if self.connected else 'Not connected'
	
	# Tries to switch to next page, else loops
	def next_page(self, sender):
		print('\nTrying to switch to next page ' + str(self.page + 1))
		
		if (self.page + 1) >= self.num_pages:
			print('Wrapping around')
			self.page = 0
		else:
			self.page += 1
		
		self.update_page_label()
		self.init_macros()
		
		print('Switched to page ' + str(self.page))
	
	# Tries to switch to previous page, else loops
	def prev_page(self, sender):
		print('\nTrying to switch to previous page ' + str(self.page - 1))
		
		if (self.page - 1) < 0:
			print('Wrapping around')
			self.page = self.num_pages - 1
		else:
			self.page -= 1
		
		self.update_page_label()
		self.init_macros()
		
		print('Switched to page ' + str(self.page))
	
	# Opens popup, which allows rebooting, shutting down and closing the application
	def exit(self, sender):
		boxLayout = BoxLayout(orientation='vertical')
		popup = Popup(title='Exit', size_hint=(None, None), size=(800, 400))
		popup.add_widget(boxLayout)
		
		boxLayout.add_widget(Button(text='Exit Application', on_press=self.exit_app))
		boxLayout.add_widget(Button(text='Reboot Device', on_press=self.reboot))
		boxLayout.add_widget(Button(text='Shutdown Device', on_press=self.shutdown))
		
		popup.open()
	
	# Notifies connection to close and exits
	def exit_app(self, sender):
		self.connection.close()
		exit(0)
	
	# Reboots the device
	def reboot(self, sender):
		os.system('sudo reboot')
	
	# Shuts device down
	def shutdown(self, sender):
		os.system('sudo shutdown -hP now')
	
	# Clears macro icons and creates new icons from json file
	def init_macros(self):
		print('Initializing macros')
		
		self.icon_grid.clear_widgets()
		
		# Add label if macro.json is empty
		if len(self.macros) <= 0:
			self.icon_grid.add_widget(Label(text='Add macros via the control application'))
			return
		
		i = self.page * self.page_size
		
		while i < (self.page * self.page_size) + self.page_size:
			current_btn = Button(font_size='14dp')
			
			if i < self.num_macros:
				
				current = self.macros[i]
				
				# Check if item is spacer
				if current['type'] == 'spacer':
					self.icon_grid.add_widget(Button())
					i += 1
					continue
				
				current_name = current['name']
				current_image = current['image']
				
				# Checks if the current macro has an image, a name, or both
				if current_name != '' and current_image != '':
					
					current_btn.bind(on_release=self.reset_border)
					current_btn.text = current_name
					current_btn.outline_width = 2
					
					if os.path.exists('img/' + current_image):
						current_btn.background_down = 'img/' + current_image
						current_btn.background_normal = 'img/' + current_image
						current_btn.border = (0, 0, 0, 0)
				
				elif current_image == '':
					current_btn.text = current_name
				elif current_name == '':
					current_btn.bind(on_release=self.reset_border)
					if os.path.exists('img/' + current_image):
						current_btn.background_normal = 'img/' + current_image
						current_btn.border = (0, 0, 0, 0)
					else:
						current_btn.text = 'IMG_ERR'
				
				# Checks if current macro can be executed locally, or if it needs a connection to the control application
				if current['type'] == 'remote':
					current_btn.bind(on_press=partial(self.exec_remote, i))
				elif current['type'] == 'local':
					current_btn.bind(on_press=partial(self.exec_local, i))
			
			self.icon_grid.add_widget(current_btn)
			i += 1
	
	# Reloads macros.json and calls init_macros
	def update_macros(self):
		print('Reloading macros')
		self.macros = JsonLoader.load_file(self.macro_cfg_location)
		self.init_macros()
	
	# Resets border (weird button click glitch with images)
	def reset_border(self, sender):
		sender.border = (0, 0, 0, 0)
	
	# Executes the action of the pressed button even if not connected to control application
	def exec_local(self, macro_id, sender):
		sender.border = (16, 16, 16, 16)
		
		try:
			for current in self.macros[macro_id]['action']:
				if current['type'] == 'post-request':
					requests.post(current['url'], data=current['data'])
				elif current['type'] == 'get-request':
					requests.get(current['url'], data=current['data'])
				elif current['type'] == 'console-print':
					print(current['message'])
				else:
					return
		except KeyError:
			print('Invalid action')
			return
	
	# Executes the action of the pressed macro button if connected to control application
	def exec_remote(self, macro_id, sender):
		sender.border = (16, 16, 16, 16)
		
		msg = 'makrotouch exec {}'.format(str(macro_id))
		
		if self.connected:
			self.connection.send(msg)
		else:
			print('Couldn\'t send "{}" to control application, not connected'.format(msg))
