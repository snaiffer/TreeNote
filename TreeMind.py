#!/usr/bin/env python

timeOut_forContextMenu = 0.4

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
    contextLayout = BoxLayout(orientation='vertical')
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
    self.background_color=[1,0,0,1]
  def goHere(self, *args):  
    tree.upTo(self.num)

class ButtonLeaf(ButtonTreeItem):
  def __init__(self, **kwargs):
    super(ButtonLeaf, self).__init__(**kwargs)
    self.background_color=[1,1,0,1]
  def on_release(self):
    tree.upTo(self.num)
    sm.transition = SlideTransition(direction='left')
    sm.current = 'leafScreen'

class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)

    mainLayout = GridLayout(cols=1)
    # top
    buttonBack = Button(text='Back', size_hint_x=0.1)
    buttonAdd = Button(text='+', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(buttonBack)
    topLayout.add_widget(buttonAdd)
    mainLayout.add_widget(topLayout) 
    buttonAdd.bind(on_press=self.goTo_addLayout)
    # Content
    scroll = ScrollView(size_hint=(1,1), do_scroll_x=False)
    self.contentLayout = GridLayout(cols = 1, padding = 10, spacing = 10, size_hint_y = None)
    self.contentLayout.bind(minimum_height=self.contentLayout.setter('height'))  # for scrolling
    scroll.add_widget(self.contentLayout)
    mainLayout.add_widget(scroll)
    buttonBack.bind(on_press=self.goBack)

    self.add_widget(mainLayout)
    self.showTree()

  def on_pre_enter(self, *args):
    self.showTree()
    
  def showTree(self, *args):  
    self.contentLayout.clear_widgets()
    counter = 0
    for cur in tree.curItem().get():
      if isinstance(cur, Branch):
        buttonBranch = ButtonBranch(text=cur.name, num=counter, outward=self)
        buttonBranch.bind(on_release=buttonBranch.goHere)
        buttonBranch.bind(on_release=self.showTree)
        self.contentLayout.add_widget(buttonBranch)
      if isinstance(cur, Leaf):
        self.contentLayout.add_widget(ButtonLeaf(text=cur.name, num=counter, outward=self))
      counter += 1  

  def goBack(self, *args):
    if not tree.reachRoot():
      tree.down()
      self.showTree()

  def goTo_addLayout(self, *args):
    sm.transition = FadeTransition() #duration=0.8)
    sm.current = 'addScreen'

class LeafScreen(Screen):
  def on_pre_enter(self):
    self.clear_widgets()
    
    leafLayout = BoxLayout(orientation = 'vertical')

    # top
    buttonBack = Button(text='Back', size_hint_x=0.1)
    capture = Label(text=tree.curItem().name, size_hint_x=0.9)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(buttonBack)
    topLayout.add_widget(capture)
    leafLayout.add_widget(topLayout) 
    buttonBack.bind(on_press=self.back)
    
    # Content
    self.textField = TextInput(text=tree.curItem().read())
    leafLayout.add_widget(self.textField) 

    self.add_widget(leafLayout)

  def back(self, *args):
    tree.curItem().write(self.textField.text)
    if not tree.reachRoot():
      tree.down()
      sm.transition = SlideTransition(direction='right')
      sm.current = 'mainScreen'

class AddLayout(FloatLayout):
  def __init__(self, **kwargs):
    super(AddLayout, self).__init__(**kwargs)
    buttonBack = Button(text='back', pos_hint={'y': 0.9},  size_hint=(0.2,0.1))
    self.add_widget(buttonBack)
    buttonBack.bind(on_press=self.back)

    mainLayout = BoxLayout(
        padding = 10,
        spacing = 10,
        pos_hint = {'center_x': 0.5, 'center_y': 0.5}, 
        size_hint = (0.7, 0.8), 
        orientation = 'vertical')
    mainLayout.add_widget(Label(text='Add:'))
    inputField = BoxLayout()
    inputField.add_widget(Label(text='name: ', size_hint_x=0.1))
    self.textField = TextInput(multiline=False)
    inputField.add_widget(self.textField)
    mainLayout.add_widget(inputField)
    buttonAddBranch = Button(text='Add Branch')
    buttonAddLeaf = Button(text='Add Leaf')
    mainLayout.add_widget(buttonAddBranch)
    mainLayout.add_widget(buttonAddLeaf)
    buttonAddBranch.bind(on_press=self.addBranch)
    buttonAddLeaf.bind(on_press=self.addLeaf)

    self.add_widget(mainLayout)
    
  def addBranch(self, *args):
    if self.textField.text != '':
      tree.curItem().add(Branch(name=self.textField.text))
      self.textField.text = ''
      self.back()  

  def addLeaf(self, *args):
    if self.textField.text != '':
      tree.curItem().add(Leaf(name=self.textField.text))
      self.textField.text = ''
      self.back()  

  def back(self, *args):
    sm.transition = FadeTransition()
    sm.current = 'mainScreen'

sm = ScreenManager() 

class TreeNoteApp(App):
  def build(self):
    try:
      tree.restore()
    except XMLfileNotfound:
      pass

    mainScreen = MainScreen(name="mainScreen")
    leafScreen = LeafScreen(name="leafScreen")
    addScreen = Screen(name='addScreen')
    addScreen.add_widget(AddLayout())

    sm.add_widget(mainScreen)
    sm.add_widget(leafScreen)
    sm.add_widget(addScreen)
    return sm

  def on_stop(self):
    tree.save()
    pass

if __name__ == '__main__':
    TreeNoteApp().run()

