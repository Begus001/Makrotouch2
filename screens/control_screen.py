from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from util.json_loader import JsonLoader
from util.config import Config
from functools import partial
import math
import os


class ControlScreen(BoxLayout):
	img_location = 'img/'
	macro_cfg_Location = 'macros.json'
	macros = JsonLoader.loadFile(macro_cfg_Location)
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.orientation = 'vertical'
		self.spacing = 5
		
		self.macro_page = 0
		self.num_macros = len(self.macros)
		self.macro_cols = Config.config['macroCols']
		self.macro_rows = Config.config['macroRows']
		self.macro_page_size = self.macro_cols * self.macro_rows
		self.num_macro_pages = math.ceil(self.num_macros / self.macro_page_size)
		self.macro_connected = False
		
		self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.icon_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.icon_grid = GridLayout(cols=self.macro_cols, size_hint=(0.8, 1))
		
		self.bt_switch_mode = Button(text='Mode', size_hint=(0.1, 1))
		self.lb_page = Label(size_hint=(0.4, 1))
		self.update_page_label()
		self.lb_connected = Label(size_hint=(0.4, 1))
		self.update_connected_label()
		self.bt_settings = Button(text='Settings', size_hint=(0.1, 1))
		
		self.top_bar.add_widget(self.bt_switch_mode)
		self.top_bar.add_widget(self.lb_page)
		self.top_bar.add_widget(self.lb_connected)
		self.top_bar.add_widget(self.bt_settings)
		
		self.add_widget(self.top_bar)
		
		self.bt_prev = Button(text='<', size_hint=(0.1, 1), on_press=self.prev_page)
		self.bt_next = Button(text='>', size_hint=(0.1, 1), on_press=self.next_page)
		
		self.icon_wrapper.add_widget(self.bt_prev)
		self.icon_wrapper.add_widget(self.icon_grid)
		self.icon_wrapper.add_widget(self.bt_next)
		
		self.add_widget(self.icon_wrapper)
		
		self.init_makros()
	
	def update_page_label(self):
		print('Updating page label')
		self.lb_page.text = 'Page: ' + str(self.macro_page + 1) + '/' + str(self.num_macro_pages)
	
	def update_connected_label(self):
		print('Updating connected label')
		self.lb_connected.text = 'Connected to control: ' + ('Yes' if self.macro_connected else 'No')
	
	def next_page(self, sender):
		print('\nTrying to switch to next page ' + str(self.macro_page + 1))
		
		if (self.macro_page + 1) >= self.num_macro_pages:
			print('Wrapping around')
			self.macro_page = 0
		else:
			self.macro_page += 1
		
		self.update_page_label()
		self.init_makros()
		
		print('Switched to page ' + str(self.macro_page))
	
	def prev_page(self, sender):
		print('\nTrying to switch to previous page ' + str(self.macro_page - 1))
		
		if (self.macro_page - 1) < 0:
			print('Wrapping around')
			self.macro_page = self.num_macro_pages - 1
		else:
			self.macro_page -= 1
		
		self.update_page_label()
		self.init_makros()
		
		print('Switched to page ' + str(self.macro_page))
	
	def init_makros(self):
		print('Initializing macros')
		
		self.icon_grid.clear_widgets()
		i = self.macro_page * self.macro_page_size
		while i < (self.macro_page * self.macro_page_size) + self.macro_page_size:
			if i >= self.num_macros:
				currentBtn = Button()
			else:
				# TODO: Optimize macro button creation
				current = self.macros[i]
				currentName = current['name']
				currentImage = current['image']
				if currentName != '' and currentImage != '':
					assert os.path.exists(self.img_location + currentImage)
					currentBtn = Button(text=currentName, background_normal='img/' + currentImage, outline_color=(0, 0, 0), outline_width=2)
					currentBtn.bind(on_press=partial(self.exec_macro, i), on_release=self.reset_border)
					currentBtn.border = (0, 0, 0, 0)
				elif currentImage == '':
					currentBtn = Button(text=currentName)
				elif currentName == '':
					currentBtn = Button(background_normal='img/' + currentImage)
					currentBtn.bind(on_press=partial(self.exec_macro, i), on_release=self.reset_border)
					currentBtn.border = (0, 0, 0, 0)
			
			self.icon_grid.add_widget(currentBtn)
			i += 1
	
	def update_makros(self):
		print('Reloading macros')
		self.macros = JsonLoader.loadFile(self.macrocfg_location)
		self.init_makros()
	
	def reset_border(self, sender):
		sender.border = (0, 0, 0, 0)
	
	def exec_macro(self, macroId, sender):
		
		# TODO: Implement macro execution command sending after control_conntion is finished
		
		sender.border = (16, 16, 16, 16)
		print('exec ' + str(macroId))
