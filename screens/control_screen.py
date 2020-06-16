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
	imgLocation = 'img/'
	macrocfgLocation = 'macros.json'
	macros = JsonLoader.loadFile(macrocfgLocation)
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.orientation = 'vertical'
		self.spacing = 5
		
		self.macroPage = 0
		self.numMacros = len(self.macros)
		self.macroCols = Config.config['macroCols']
		self.macroRows = Config.config['macroRows']
		self.macroPageSize = self.macroCols * self.macroRows
		self.numMacroPages = math.ceil(self.numMacros / self.macroPageSize)
		self.macroConnected = False
		
		self.topBar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.iconWrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.iconGrid = GridLayout(cols=self.macroCols, size_hint=(0.8, 1))
		
		self.btSwitchMode = Button(text='Mode', size_hint=(0.1, 1))
		self.lbPage = Label(size_hint=(0.4, 1))
		self.updatePageLabel()
		self.lbConnected = Label(size_hint=(0.4, 1))
		self.updateConnectedLabel()
		self.btSettings = Button(text='Settings', size_hint=(0.1, 1))
		
		self.topBar.add_widget(self.btSwitchMode)
		self.topBar.add_widget(self.lbPage)
		self.topBar.add_widget(self.lbConnected)
		self.topBar.add_widget(self.btSettings)
		
		self.add_widget(self.topBar)
		
		self.btPrev = Button(text='<', size_hint=(0.1, 1), on_press=self.prevPage)
		self.btNext = Button(text='>', size_hint=(0.1, 1), on_press=self.nextPage)
		
		self.iconWrapper.add_widget(self.btPrev)
		self.iconWrapper.add_widget(self.iconGrid)
		self.iconWrapper.add_widget(self.btNext)
		
		self.add_widget(self.iconWrapper)
		
		print('ControlScreen built')
		
		self.initMakros()
		
	def updatePageLabel(self):
		print('Updating page label')
		self.lbPage.text = 'Page: ' + str(self.macroPage + 1) + '/' + str(self.numMacroPages)
		
	def updateConnectedLabel(self):
		print('Updating connected label')
		self.lbConnected.text = 'Connected to control: ' + ('Yes' if self.macroConnected else 'No')
	
	def nextPage(self, sender):
		print('Trying to switch to next page ' + str(self.macroPage + 1))
		
		if (self.macroPage + 1) >= self.numMacroPages:
			print('Wrapping around')
			self.macroPage = 0
		else:
			self.macroPage += 1
		
		self.updatePageLabel()
		self.initMakros()
		
		print('Switched to page ' + str(self.macroPage))
	
	def prevPage(self, sender):
		print('Trying to switch to previous page ' + str(self.macroPage - 1))
		
		if (self.macroPage - 1) < 0:
			print('Wrapping around')
			self.macroPage = self.numMacroPages - 1
		else:
			self.macroPage -= 1
		
		self.updatePageLabel()
		self.initMakros()
		
		print('Switched to page ' + str(self.macroPage))
	
	def initMakros(self):
		print('Initializing macros')
		
		self.iconGrid.clear_widgets()
		i = self.macroPage * self.macroPageSize
		while i < (self.macroPage * self.macroPageSize) + self.macroPageSize:
			if i >= self.numMacros:
				currentBtn = Button()
			else:
				current = self.macros[i]
				currentName = current['name']
				currentImage = current['image']
				if currentName != '' and currentImage != '':
					assert os.path.exists(self.imgLocation + currentImage)
					currentBtn = Button(text=currentName, background_normal='img/' + currentImage)
					currentBtn.bind(on_press=partial(self.execMacro, i), on_release=self.resetBorder)
					currentBtn.border = (0, 0, 0, 0)
				elif currentImage == '':
					currentBtn = Button(text=currentName)
				elif currentName == '':
					currentBtn = Button(background_normal='img/' + currentImage)
					currentBtn.bind(on_press=partial(self.execMacro, i), on_release=self.resetBorder)
					currentBtn.border = (0, 0, 0, 0)
			
			self.iconGrid.add_widget(currentBtn)
			i += 1
	
	def updateMakros(self):
		print('Reloading macros')
		self.macros = JsonLoader.loadFile(self.macrocfg_location)
		self.initMakros()
	
	def resetBorder(self, sender):
		sender.border = (0, 0, 0, 0)
	
	def execMacro(self, macroId, sender):
		sender.border = (16, 16, 16, 16)
		print('exec ' + str(macroId))
