from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class ControlScreen(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.orientation = 'vertical'
		self.spacing = 5
		
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
		
		buttons = []
		i = 0
		while i < 8:
			buttons.append(Button(text='test' + str(i)))
			i += 1
		
		for button in buttons:
			self.iconGrid.add_widget(button)
		
		self.iconWrapper.add_widget(self.btPrev)
		self.iconWrapper.add_widget(self.iconGrid)
		self.iconWrapper.add_widget(self.btNext)
		
		self.add_widget(self.iconWrapper)

