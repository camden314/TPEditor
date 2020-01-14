kv_script = """#:kivy 1.11.1
#:import expanduser os.path.expanduser
#:import C kivy.utils.get_color_from_hex
<RoundTextinput@TextInput>:
	font_size: '40dp'
	background_color: 0,0,0,0
	font_name: 'assets/Pusab.ttf'
	cursor_color: 1,1,1,1
	canvas.before:
		Color:
			rgb: 0, 39/255, 98/255 #C('#0f192e')
		RoundedRectangle:
			#angle_start: 180
			#angle_end: 360
			pos: (self.pos[0], self.pos[1]+5)
			size: self.size
		Color:
			rgb: 1,1,1
<GDTexture>:
	size_hint: None, None
	size: 128,128
	spacing: 0
	background_color: 0,0,0,0
	Image:
		size_hint: [1.4,1.4]
		center_x: root.center_x
		center_y: root.center_y
		source: "assets/smoothborder.png"
	Image:
		center_x: root.center_x
		center_y: root.center_y
		id: textureIMG
		source: ""
<FileChoosePopup>:
	title: "Choose a Texture File"
	size_hint: 1, 1
	auto_dismiss: False

	BoxLayout:
		orientation: "vertical"
		FileChooserListView:
			path: "/Users/jakrillis/Projects/texturepackgui/tests/"
			filters: [self.parent.parent.parent.parent.is_png]
			id: filechooser

		BoxLayout:
			size_hint: (1, 0.1)
			pos_hint: {'center_x': .5, 'center_y': .5}
			spacing: 20
			Button:
				text: "Cancel"
				on_release: root.dismiss()
			Button:
				text: "Load"
				on_release: root.load(filechooser.selection)
				id: ldbtn
				disabled: True if filechooser.selection==[] else False
<FileSavePopup>:
	title: "Choose a Save Location"
	size_hint: 1, 1
	auto_dismiss: False

	BoxLayout:
		orientation: "vertical"
		FileChooserListView:
			path: expanduser("~")
			id: filechooser
			on_selection: text_input.text = self.selection and self.selection[0] or ''

		TextInput:
			id: savetext_input
			size_hint_y: None
			height: 30
			multiline: False
		BoxLayout:
			size_hint: (1, 0.1)
			pos_hint: {'center_x': .5, 'center_y': .5}
			spacing: 20
			Button:
				text: "Cancel"
				on_release: root.dismiss()
			Button:
				text: "Save"
				on_release: root.save(filechooser.path+'/'+savetext_input.text)
				id: ldbtn
				disabled: False if savetext_input.text else True

<ImageButton@ButtonBehavior+Image>:


<TPScreen>:
	orientation: 'vertical'
	canvas.before:
		Rectangle:
			source: 'assets/background.png'
			size: self.size
			pos: self.pos
	Image:
		source: 'assets/title.png'
		pos_hint: {'top':1.43}
	Button:
		on_press: self.parent.openFileChoose()
		pos_hint: {'right':0.08,'top':0.98}
		size_hint: [None,None]
		size: 60,57
		background_color: 0, 0, 0, 0
		Image:
			source: 'assets/fileopen.png'
			center_x: self.parent.center_x
			center_y: self.parent.center_y
			size_hint: [None,None]
			size: 60, 57
			allow_stretch: True
	Button:
		on_press: self.parent.exportFile()
		pos_hint: {'right':0.98,'top':0.98}
		size_hint: [None,None]
		size: 60,57
		background_color: 0, 0, 0, 0
		Image:
			source: 'assets/save.png'
			center_x: self.parent.center_x
			center_y: self.parent.center_y
			size_hint: [None,None]
			size: 60, 57
			allow_stretch: True
	RoundTextInput:
		id: searchinp
		size_hint: [None,None]
		size: 300,50
		pos_hint: {'right':0.8,'top':0.86}
		foreground_color: 1,1,1,1
	Button:
		background_color: 0,0,0,0
		size_hint: [None,None]
		size: 153,50
		pos_hint: {'right':0.97,'top':0.87}
		on_press: tp_box.filter(searchinp.text)
		Image:
			source: 'assets/search.png'
			center_x: self.parent.center_x
			center_y: self.parent.center_y
			size_hint: [None,None]
			size: 153,50
			allow_stretch: True
	BoxLayout:
		size_hint: 1,0.8
		pos_hint: {"top":0.75}
		ScrollView:
			scroll_distance: 1
			TextureBox:
				#  for debugging
				id: tp_box
				size_hint_y: None
				height: self.minimum_height
				canvas.before:
					Color:
						rgba: 0.75,0.43,0.24,1
					Rectangle:
						size: self.size
					Line:
						width:2
						rectangle: (self.x, self.y, self.width, self.height)
TPScreen:

"""




import kivy
kivy.require('1.11.1')
from kivy.app import App

from kivy.config import Config
Config.set('graphics', 'width', '1024')
from kivy.core.image import Image as CoreImage

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooser
from kivy.properties import ObjectProperty, StringProperty
import time
from kivy.lang import Builder

import plistlib
from PIL import Image as PilImage
import io
import orjson
import platform
import os
import sys, traceback


class RoundTextInput(TextInput):
	pass
class FileChoosePopup(Popup):
	def has_plist(self,directory,file):
		if file.endswith('.png'):
			if os.path.exists(file.replace('.png','.plist')):
				return True
			else:
				return False
		else:
			return False
	def is_png(self,directory,file):
		if file.endswith('.png'):
			return True 
		else:
			return False
	load = ObjectProperty()
class FileSavePopup(Popup):
	def is_png(self,directory,file):
		if file.endswith('.png'):
			return True 
		else:
			return False
	save = ObjectProperty()
class GDTexture(Button):

	def fileOpenCallback(self,sel):
		print(self.imageName)
		self.filepopup.dismiss()
		oldSize = self.imageData.size
		print(oldSize)
		self.imageData = PilImage.open(sel[0]).resize(oldSize,PilImage.ANTIALIAS)
		self.reloadImage()
		self.parent.textures[self.imageName][0] = self.imageData
	def changeTexture(self):
		self.filepopup = FileChoosePopup(load=self.fileOpenCallback)
		self.filepopup.open()
	
	def reloadImage(self):
		imageobject = io.BytesIO()

		imgdata2 = self.imageData.copy()
		imgdata2.thumbnail((80,80),PilImage.ANTIALIAS)
		imgdata2.save(imageobject,format='png')
		imageobject.seek(0)
		self.ids.textureIMG.texture = CoreImage(imageobject, ext='png').texture
	
	def loadTexture(self,imgName,imgData):
		self.imageName = imgName
		self.imageData = imgData
		self.reloadImage()
	def on_press(self):
		self.changeTexture()
class TextureBox(StackLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.textures = {}
		self.tpSize = (0,0)
	def addImage(self,imgName,imgData,rotated,pos,new=True):
		if new:
			self.textures[imgName] = [imgData,rotated,pos]
		texture = GDTexture()
		texture.loadTexture(imgName,imgData)
		texture.reloadImage()

		#texture.size = (60,60)
		self.add_widget(texture)
	def filter(self,textFilter):
		self.clear_widgets()
		for key in self.textures:
			if textFilter.lower() in key.lower():
				obj = self.textures[key]
				self.addImage(key,obj[0],obj[1],obj[2],new=False)
	def generateTPPng(self):
		base = PilImage.new('RGBA',self.tpSize)
		for key in self.textures:
			obj = self.textures[key]
			textureImage = obj[0]
			if obj[1]:
				textureImage = textureImage.rotate(-90,expand=True)
			base.paste(textureImage,obj[2])
		return base
class TPScreen(FloatLayout):
	def getTextures(self):
		png = PilImage.open(self.pngLocation)
		pngWidth, pngHeight = self.ids.tp_box.tpSize = png.size

		plist = open(self.plistLocation,'r').read().replace('{','[').replace('}',']').encode()
		plist = plistlib.loads(plist)['frames']

		self.ids.tp_box.clear_widgets()
		self.ids.tp_box.textures = {}

		# for speed
		_loads = orjson.loads
		_addImage = self.ids.tp_box.addImage
		_crop = png.crop
		for key in plist:
			obj = plist[key]
			lists = _loads(obj['textureRect'])

			pos_left, pos_top = lists[0]
			width, height = lists[1]

			if obj['textureRotated']:
				objectPng = _crop((pos_left,pos_top,pos_left+height,pos_top+width))
				objectPng = objectPng.rotate(90,expand=True)
			else:
				objectPng = _crop((pos_left,pos_top,pos_left+width,pos_top+height))

			_addImage(key,objectPng,obj['textureRotated'],(pos_left,pos_top))
	def fileOpenCallback(self,sel):
		print(sel)
		self.pngLocation = sel[0]
		self.plistLocation = sel[0].replace('png','plist')
		self.filepopup.dismiss()
		self.getTextures()
		self.choosePath = os.path.dirname(sel[0])
	def openFileChoose(self):
		self.filepopup = FileChoosePopup(load=self.fileOpenCallback)
		self.filepopup.ids.filechooser.path = self.choosePath
		self.filepopup.ids.filechooser.filters = [self.filepopup.has_plist]
		self.filepopup.open()
	def saveFileCallback(self,sel):
		self.savepopup.dismiss()
		if not sel.endswith('.png'):
			sel+='.png'
		print(sel)
		self.ids.tp_box.generateTPPng().save(sel,'PNG')
	def exportFile(self):
		if self.pngLocation:
			print("TODO: Add Export")
			self.savepopup = FileSavePopup(save=self.saveFileCallback)
			self.savepopup.open()
		else:
			print("ERR")
	def __init__(self, **kwargs):
		super().__init__()
		self.choosePath = os.path.expanduser("~")
		self.plistLocation = self.pngLocation = None
		"""title = Label(text="Texture Pack Creator")
		title.size_hint=[None, None]
		title.pos_hint = {'top':0.8}
		title.size = title.texture_size
		self.add_widget(title)"""

class TPEditorApp(App):
	def build(self):
		root = Builder.load_string(kv_script)
		return root
try:
	app = TPEditorApp()
	app.run()
except Exception as e:
	with open(os.path.expanduser('~')+"/tplog.txt",'w') as f:
		f.write(traceback.format_exc())
		f.write(str(e))
	raise