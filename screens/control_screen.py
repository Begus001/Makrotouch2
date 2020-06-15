from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from util.json_loader import JsonLoader


class ControlScreen(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.orientation = 'vertical'
		self.spacing = 5
		
		self.macros = JsonLoader.loadIcons()
		
		self.topBar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=3)
		self.iconWrapper = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), spacing=3)
		self.iconGrid = GridLayout(cols=4, size_hint=(0.8, 1))
		
		self.btSwitchMode = Button(text='Mode', size_hint=(0.1, 1))
		self.lbPage = Label(text='PAGE', size_hint=(0.8, 1))
		self.btSettings = Button(text='Settings', size_hint=(0.1, 1))
		
		self.topBar.add_widget(self.btSwitchMode)
		self.topBar.add_widget(self.lbPage)
		self.topBar.add_widget(self.btSettings)
		
		self.add_widget(self.topBar)
		
		self.btPrev = Button(text='<', size_hint=(0.1, 1))
		self.btNext = Button(text='>', size_hint=(0.1, 1))
		
		self.iconWrapper.add_widget(self.btPrev)
		self.iconWrapper.add_widget(self.iconGrid)
		self.iconWrapper.add_widget(self.btNext)
		
		self.add_widget(self.iconWrapper)
		
		self.initMakros()
		
	def initMakros(self):
		for macro in self.macros:
			current = Button(text=macro['name'])
			self.iconGrid.add_widget(current)
			
	def updateMakros(self):
		self.macros = JsonLoader.loadIcons()
		self.initMakros()
