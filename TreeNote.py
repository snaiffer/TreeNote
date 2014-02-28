#!/usr/bin/env python

timeOut_forContextMenu = 0.4
color = {
    'btnLeaf':      [0.25,1,0.25,0.8], #[1,1,0,1], 
    'btnBranch':    [1,0.4,0.3,0.9],  #[1,0.4,0.3,1], 
    'readLeaf':     [0.4,1,0.4,1],
    'lblPath':      [0.2,0,0,1],
    'editLeaf':        [1,1,1,1],
    'brown':        [1,0.5,0.1,1],
    'green':        [0.5,1,0.2,1]
    }

systemBtnBack = 8
from kivy.utils import platform
if platform() == 'android':
  import android
  android.map_key(android.KEYCODE_BACK, 1001)
  systemBtnBack = 1001

from tree import *
tree = Tree()

"""
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '700')
#Config.set('kivy', 'window_icon', './icon.png')
"""

from kivy.app import App
from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, FadeTransition , SlideTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class ButtonTreeItem(Button):
  def __init__(self, num, outward, **kwargs):
    super(ButtonTreeItem, self).__init__(**kwargs)
    self.size_hint_y = None
    self.num = num
    self.context = False
    self.outward = outward

  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
      self.create_clock()
    return super(ButtonTreeItem, self).on_touch_down(touch) 
  def on_touch_up(self, touch):
    if self.collide_point(*touch.pos):
      self.delete_clock()
      if self.context :
        self.context = False
        return True 
    return super(ButtonTreeItem, self).on_touch_up(touch) 

  def create_clock(self, *args):
    Clock.schedule_once(self.openContextMenu, timeOut_forContextMenu)
  def delete_clock(self, *args):
    Clock.unschedule(self.openContextMenu)

  def openContextMenu(self, *args):
    self.context = True
    self.contextMenu = ModalView(size_hint=(0.5, 0.5))
    self.contextMenu.bind(on_dismiss=self.outward.showTree())
    contextLayout = BoxLayout(
        padding = 10,
        spacing = 10,
        pos_hint = {'center_x': 0.5, 'center_y': 0.5}, 
        size_hint = (0.7, 0.8), 
        orientation = 'vertical')
    contextLayout.add_widget(Label(text=self.text))
    btnDelete = Button(text='delete')
    btnDelete.bind(on_press=self.delete)
    contextLayout.add_widget(btnDelete)
    close = Button(text='close')
    close.bind(on_release=self.contextMenu.dismiss)
    contextLayout.add_widget(close)
    self.contextMenu.add_widget(contextLayout)
    self.contextMenu.open()
  def delete(self, *args):
    tree.curItem().remove(self.num)
    self.contextMenu.dismiss()
    self.outward.showTree()

class ButtonBranch(ButtonTreeItem):
  def __init__(self, **kwargs):
    super(ButtonBranch, self).__init__(**kwargs)
    self.background_color = color['btnBranch']
  def goHere(self, *args):  
    tree.upTo(self.num)

class ButtonLeaf(ButtonTreeItem):
  def __init__(self, **kwargs):
    super(ButtonLeaf, self).__init__(**kwargs)
    self.background_color = color['btnLeaf']
  def on_release(self):
    tree.upTo(self.num)
    sm.transition = SlideTransition(direction='left')
    sm.current = 'leafScreen'

class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)

    mainLayout = GridLayout(cols=1)
    # top
    btnBack = Button(text='Back', size_hint_x=0.1)
    
    self.lblPath = Label(size_hint_x=0.8, color = color['lblPath'])
    self.lblPath.anchors_x = 'left'
    btnAdd = Button(text='+', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(btnBack)
    topLayout.add_widget(self.lblPath)
    topLayout.add_widget(btnAdd)
    mainLayout.add_widget(topLayout) 
    btnAdd.bind(on_press=self.addMenu)
    # Content
    scroll = ScrollView(size_hint=(1,1), do_scroll_x=False)
    self.contentLayout = GridLayout(cols = 1, padding = 10, spacing = 10, size_hint_y = None)
    self.contentLayout.bind(minimum_height=self.contentLayout.setter('height'))  # for scrolling
    scroll.add_widget(self.contentLayout)
    mainLayout.add_widget(scroll)
    btnBack.bind(on_press=self.goBack)

    self.add_widget(mainLayout)
    self.showTree()

    mainLayout.bind(
          size=self._update_rect,
          pos=self._update_rect)
    with mainLayout.canvas.before:
      Color(0.5, 0.8, 1, 0.9) 
      self.rect = Rectangle(
                  size=mainLayout.size,
                  pos=mainLayout.pos)
  def _update_rect(self, instance, value):
    self.rect.pos = instance.pos
    self.rect.size = instance.size

  def on_pre_enter(self, *args):
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self.showTree()
    
  def showTree(self, *args):  
    self.contentLayout.clear_widgets()
    self.lblPath.text = tree.getPath()
    counter = 0
    for cur in tree.curItem().get():
      if isinstance(cur, Branch):
        btnBranch = ButtonBranch(text=cur.name, num=counter, outward=self)
        btnBranch.bind(on_release=btnBranch.goHere)
        btnBranch.bind(on_release=self.showTree)
        self.contentLayout.add_widget(btnBranch)
      if isinstance(cur, Leaf):
        self.contentLayout.add_widget(ButtonLeaf(text=cur.name, num=counter, outward=self))
      counter += 1  

  def goBack(self, *args):
    if not tree.reachRoot():
      tree.down()
      self.showTree()

  def addMenu(self, *args):
    self.contextMenu = ModalView(size_hint=(0.5, 0.5))
    mainLayout = BoxLayout(
        padding = 10,
        spacing = 10,
        pos_hint = {'center_x': 0.5, 'center_y': 0.5}, 
        size_hint = (0.7, 0.8), 
        orientation = 'vertical')
    mainLayout.add_widget(Label(text='Add:'))
    inputField = BoxLayout()
    inputField.add_widget(Label(text='name: ', size_hint_x=0.3))
    self.textField = TextInput(multiline=False, focus=True)
    inputField.add_widget(self.textField)
    mainLayout.add_widget(inputField)
    btnAddBranch = Button(text='Add Branch')
    btnAddLeaf = Button(text='Add Leaf')
    mainLayout.add_widget(btnAddBranch)
    mainLayout.add_widget(btnAddLeaf)
    btnAddBranch.bind(on_press=self.addBranch)
    btnAddLeaf.bind(on_press=self.addLeaf)
    close = Button(text='close')
    close.bind(on_release=self.contextMenu.dismiss)
    mainLayout.add_widget(close)

    self.contextMenu.add_widget(mainLayout)
    self.contextMenu.open()
    
  def addBranch(self, *args):
    if self.textField.text != '':
      tree.curItem().add(Branch(name=self.textField.text))
      self.textField.text = ''
      self.contextMenu.dismiss()
      self.showTree()

  def addLeaf(self, *args):
    if self.textField.text != '':
      tree.curItem().add(Leaf(name=self.textField.text))
      self.textField.text = ''
      self.contextMenu.dismiss()
      self.showTree()

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[0] == systemBtnBack:
      self.goBack()
      return True
    return False
  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

class TextInputForScroll(TextInput):
  def on_text(self, *args):
    actual_height = (len(self._lines)+1) * (self.line_height+self._line_spacing)*1.1
    self.height=actual_height

class LeafScreen(Screen):
  def on_pre_enter(self):
    self.clear_widgets()
    
    self.leafLayout = BoxLayout(orientation = 'vertical')
    
    self.readMode()
    #self.editMode()

    self.add_widget(self.leafLayout)

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)

    self.leafLayout.bind(
          size=self._update_rect,
          pos=self._update_rect)
    with self.leafLayout.canvas.before:
      Color(0.5, 0.8, 1, 0.9) 
      self.rect = Rectangle(
                  size=self.leafLayout.size,
                  pos=self.leafLayout.pos)
  def _update_rect(self, instance, value):
    self.rect.pos = instance.pos
    self.rect.size = instance.size

  def readMode(self, *args):
    self.leafLayout.clear_widgets()
    # top
    btnBack = Button(text='Back', size_hint_x=0.1)
    capture = Label(text=tree.curItem().name, size_hint_x=0.8, color = color['lblPath'])
    btnEdit = Button(text='Edit', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(btnBack)
    topLayout.add_widget(capture)
    topLayout.add_widget(btnEdit)
    self.leafLayout.add_widget(topLayout) 
    btnBack.bind(on_press=self.back)

    # Content
    self.textField = TextInputForScroll(
        size_hint_y=None,
        text=tree.curItem().read(), 
        background_color = color['readLeaf'],
        readonly = True,
        focus = True)
    self.textField.on_text()
    textFieldScroll = ScrollView( bar_width = 10)
    textFieldScroll.add_widget(self.textField)

    self.leafLayout.add_widget(textFieldScroll) 

    btnEdit.bind(on_release=self.editMode)

  def editMode(self, *args):
    self.leafLayout.clear_widgets()
    # top
    btnBack = Button(text='Back', size_hint_x=0.1)
    capture = Label(text=tree.curItem().name, size_hint_x=0.8, color = color['lblPath'])
    btnSave = Button(text='Save', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(btnBack)
    topLayout.add_widget(capture)
    topLayout.add_widget(btnSave)
    self.leafLayout.add_widget(topLayout) 
    btnBack.bind(on_press=self.back)

    # Content
    self.textField = TextInput(
        text=tree.curItem().read(), 
        background_color = color['editLeaf'],
        focus = True)
    self.leafLayout.add_widget(self.textField)

    btnSave.bind(on_release=self.readMode,
                on_press=self.save)

  def save(self, *args):  
    tree.curItem().write(self.textField.text)

  def back(self, *args):
    if sm.current == "leafScreen" :
      self.save()
      if not tree.reachRoot():
        tree.down()
        sm.transition = SlideTransition(direction='right')
        sm.current = 'mainScreen'

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[0] == systemBtnBack:
      self.back()
      return True
    return False
  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

sm = ScreenManager() 

class TreeNoteApp(App):
  def build(self):
    try:
      tree.restore()
    except XMLfileNotfound:
      pass

    mainScreen = MainScreen(name="mainScreen")
    leafScreen = LeafScreen(name="leafScreen")
    self.bind(on_stop=leafScreen.back)

    sm.add_widget(mainScreen)
    sm.add_widget(leafScreen)
    return sm

  def on_stop(self):
    tree.save()
    pass

if __name__ == '__main__':
    TreeNoteApp().run()

