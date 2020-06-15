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
		
		self.topBar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.iconWrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.iconGrid = GridLayout(cols=self.macroCols, size_hint=(0.8, 1))
		
		self.btSwitchMode = Button(text='Mode', size_hint=(0.1, 1))
		self.lbPage = Label(text=str(self.macroPage + 1), size_hint=(0.8, 1))
		self.btSettings = Button(text='Settings', size_hint=(0.1, 1))
		
		self.topBar.add_widget(self.btSwitchMode)
		self.topBar.add_widget(self.lbPage)
		self.topBar.add_widget(self.btSettings)
		
		self.add_widget(self.topBar)
		
		self.btPrev = Button(text='<', size_hint=(0.1, 1), on_press=self.prevPage)
		self.btNext = Button(text='>', size_hint=(0.1, 1), on_press=self.nextPage)
		
		self.iconWrapper.add_widget(self.btPrev)
		self.iconWrapper.add_widget(self.iconGrid)
		self.iconWrapper.add_widget(self.btNext)
		
		self.add_widget(self.iconWrapper)
		
		self.initMakros()
	
	def nextPage(self, ign):
		if (self.macroPage + 1) >= self.numMacroPages:
			self.macroPage = 0
		else:
			self.macroPage += 1
		
		self.lbPage.text = str(self.macroPage + 1)
		self.initMakros()
	
	def prevPage(self, ign):
		if (self.macroPage - 1) < 0:
			self.macroPage = self.numMacroPages - 1
		else:
			self.macroPage -= 1
		
		self.lbPage.text = str(self.macroPage + 1)
		self.initMakros()
	
	def initMakros(self):
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
					currentBtn.bind(on_press=partial(self.resetBorder, currentBtn), on_release=partial(self.setBorder, currentBtn))
					self.setBorder(None, currentBtn)
				elif currentImage == '':
					currentBtn = Button(text=currentName)
				elif currentName == '':
					currentBtn = Button(background_normal='img/' + currentImage)
					currentBtn.bind(on_press=partial(self.resetBorder, currentBtn), on_release=partial(self.setBorder, currentBtn))
					self.setBorder(None, currentBtn)
			
			self.iconGrid.add_widget(currentBtn)
			i += 1
	
	def updateMakros(self):
		self.macros = JsonLoader.loadFile(self.macrocfg_location)
		self.initMakros()
	
	def resetBorder(self, ign, sender):
		sender.border = (16, 16, 16, 16)
	
	def setBorder(self, ign, sender):
		sender.border = (0, 0, 0, 0)
