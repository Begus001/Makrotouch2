from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from util.json_loader import JsonLoader
from util.config import Config
from functools import partial
import math
import os


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
		self.macro_page: int = 0
		self.num_macros: int = len(self.macros)
		self.macro_cols: int = Config.config['macroCols']
		self.macro_rows: int = Config.config['macroRows']
		self.macro_page_size: int = self.macro_cols * self.macro_rows
		self.num_macro_pages: int = math.ceil(self.num_macros / self.macro_page_size)
		self.macro_connected: bool = False
		self.macro_connection = None
		# endregion
		
		# region Wrapper Layout config
		self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.icon_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.icon_grid = GridLayout(cols=self.macro_cols, size_hint=(0.8, 1))
		# endregion
		
		# region Create buttons
		self.bt_switch_mode = Button(text='Mode', size_hint=(0.1, 1))
		self.lb_page = Label(size_hint=(0.4, 1))
		self.lb_connected = Label(size_hint=(0.4, 1))
		self.bt_settings = Button(text='Settings', size_hint=(0.1, 1))
		
		self.bt_prev = Button(text='<', size_hint=(0.1, 1), on_press=self.prev_page)
		self.bt_next = Button(text='>', size_hint=(0.1, 1), on_press=self.next_page)
		# endregion
		
		# region Combine all widgets
		self.top_bar.add_widget(self.bt_switch_mode)
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
		self.lb_page.text = 'Page: ' + str(self.macro_page + 1) + '/' + str(self.num_macro_pages)
	
	# Updates label that indicates the connection status
	def update_connected_label(self):
		print('Updating connected label')
		self.lb_connected.text = 'Connected to control: ' + ('Yes' if self.macro_connected else 'No')
	
	# Tries to switch to next page, else loops
	def next_page(self, sender):
		print('\nTrying to switch to next page ' + str(self.macro_page + 1))
		
		if (self.macro_page + 1) >= self.num_macro_pages:
			print('Wrapping around')
			self.macro_page = 0
		else:
			self.macro_page += 1
		
		self.update_page_label()
		self.init_macros()
		
		print('Switched to page ' + str(self.macro_page))
	
	# Tries to switch to previous page, else loops
	def prev_page(self, sender):
		print('\nTrying to switch to previous page ' + str(self.macro_page - 1))
		
		if (self.macro_page - 1) < 0:
			print('Wrapping around')
			self.macro_page = self.num_macro_pages - 1
		else:
			self.macro_page -= 1
		
		self.update_page_label()
		self.init_macros()
		
		print('Switched to page ' + str(self.macro_page))
	
	# Clears macro icons and creates new icons form json file
	def init_macros(self):
		print('Initializing macros')
		
		self.icon_grid.clear_widgets()
		i = self.macro_page * self.macro_page_size
		
		while i < (self.macro_page * self.macro_page_size) + self.macro_page_size:
			current_btn = Button()
			
			if i < self.num_macros:
				
				current = self.macros[i]
				current_name = current['name']
				current_image = current['image']

				# Checks if the current macro has an image, a name, or both
				if current_name != '' and current_image != '':
					current_btn.bind(on_press=partial(self.exec_macro, i), on_release=self.reset_border)
					current_btn.text = current_name
					
					if os.path.exists('img/' + current_image):
						current_btn.background_normal = 'img/' + current_image
						current_btn.border = (0, 0, 0, 0)
				
				elif current_image == '':
					current_btn.text = current_name
					current_btn.bind(on_press=partial(self.exec_macro, i))
				elif current_name == '':
					current_btn.bind(on_press=partial(self.exec_macro, i), on_release=self.reset_border)
					if os.path.exists('img/' + current_image):
						current_btn.background_normal = 'img/' + current_image
						current_btn.border = (0, 0, 0, 0)
					else:
						current_btn.text = 'IMG_ERR'
				
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
	
	# Executes the action of the pressed macro button
	def exec_macro(self, macroId, sender):
		sender.border = (16, 16, 16, 16)
		
		msg = 'makrotouch exec{}'.format(str(macroId))
		
		if self.macro_connected:
			self.macro_connection.send(msg)
		else:
			print('Couldn\'t send "{}" to control application, not connected'.format(msg))
