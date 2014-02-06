#!/usr/bin/env python

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ObjectProperty

from tree import *

tree = Tree()
"""
tree.curItem().add(Branch('branch1'))
tree.curItem().add(Branch('branch2'))
tree.curItem().add(Leaf('leaf1'))
tree.upTo(0)
tree.curItem().add(Leaf('leaf2'))
tree.curItem().add(Leaf('leaf3'))
tree.curItem().add(Branch('branch3'))
tree.down()
print_all(tree.curItem())
"""

class ButtonTreeItem(Button):
  def __init__(self, num, **kwargs):
    super(ButtonTreeItem, self).__init__(**kwargs)
    self.size_hint_y = None
    self.num = num

class ButtonBranch(ButtonTreeItem):
  def __init__(self, content, **kwargs):
    super(ButtonBranch, self).__init__(**kwargs)
    self.content = content
    self.background_color=[1,0,0,1]
  def on_press(self):
    global tree
    tree.upTo(self.num)
    self.content.showTree()
    return super(ButtonBranch, self).on_press()

class ButtonLeaf(ButtonTreeItem):
  def __init__(self, **kwargs):
    super(ButtonLeaf, self).__init__(**kwargs)
    self.background_color=[1,1,0,1]
  def on_press(self):
    global tree
    tree.upTo(self.num)
    sm.current = 'leafScreen'
    return super(ButtonLeaf, self).on_press()

class ContentScroll(ScrollView):
  def __init__(self, layout, **kwargs):
    super(ContentScroll, self).__init__(**kwargs)
    self.size_hint=(1,1)
    self.do_scroll_x=False
    self.add_widget(layout)

class ContentLayout(GridLayout):
  def __init__(self, textField, **kwargs):
    super(ContentLayout, self).__init__(**kwargs)
    self.textField = textField
    self.cols = 1
    self.padding = 10
    self.spacing = 10
    self.size_hint_y = None
    self.bind(minimum_height=self.setter('height'))  # for scrolling
    self.showTree()

  def showTree(self):  
    global tree
    self.clear_widgets()
    counter = 0
    for cur in tree.curItem().get():
      if isinstance(cur, Branch):
        self.add_widget(ButtonBranch(text=cur.name, num=counter, content = self))
      if isinstance(cur, Leaf):
        self.add_widget(ButtonLeaf(text=cur.name, num=counter))
      counter += 1  

  def add_newBranch(self, *args):
    global tree
    print 'Add NewBranch'
    if self.textField.text != '':
      tree.curItem().add(Branch(name=self.textField.text))
      self.textField.text = ''
      self.showTree()

  def add_newLeaf(self, *args):
    global tree
    print 'Add NewLeaf'
    if self.textField.text != '':
      tree.curItem().add(Leaf(name=self.textField.text))
      self.textField.text = ''
      self.showTree()

  def goBack(self, *args):
    global tree
    if not tree.reachRoot():
      tree.down()
      self.showTree()

class MainLayout(GridLayout):
  def __init__(self, **kwargs):
    super(MainLayout, self).__init__(**kwargs)
    self.cols=1

    # top
    buttonBack = Button(text='Back', size_hint_x=0.1)
    textField = TextInput(multiline=False, size_hint_x=0.7)
    buttonAddBranch = Button(text='AddBranch', size_hint_x=0.1)
    buttonAddLeaf = Button(text='AddLeaf', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(buttonBack)
    topLayout.add_widget(textField)
    topLayout.add_widget(buttonAddBranch)
    topLayout.add_widget(buttonAddLeaf)
    self.add_widget(topLayout) 
    
    # Content
    contentLayout = ContentLayout(textField)
    scroll = ContentScroll(contentLayout)
    self.add_widget(scroll)
    buttonAddBranch.bind(on_press=contentLayout.add_newBranch)
    buttonAddLeaf.bind(on_press=contentLayout.add_newLeaf)
    buttonBack.bind(on_press=contentLayout.goBack)
    #textField.bind(text=contentLayout.find)

class ButtonBack_fromLeaf(Button):
  def on_press(self):
    global tree
    print 'goBack_fromLeaf'
    if not tree.reachRoot():
      tree.down()
      sm.current = 'mainScreen'

class TextField(TextInput):
  def save(self, *args):
    global tree
    tree.curItem().write(self.text)
  
class LeafLayout(BoxLayout):
  def __init__(self, **kwargs):
    super(LeafLayout, self).__init__(**kwargs)
    self.orientation = 'vertical'

    global tree
    # top
    buttonBack = ButtonBack_fromLeaf(text='Back', size_hint_x=0.1)
    capture = Label(text=tree.curItem().name, size_hint_x=0.9)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(buttonBack)
    topLayout.add_widget(capture)
    self.add_widget(topLayout) 
    
    # Content
    textField = TextField(text=tree.curItem().read())
    self.add_widget(textField) 
    buttonBack.bind(on_press=textField.save)

class LeafScreen(Screen):
  def on_pre_enter(self):
    print 'pre_enter'
    self.clear_widgets()
    self.add_widget(LeafLayout())
    
    
sm = ScreenManager()

class ScrollViewApp(App):
  global tree
  def build(self):
    try:
      tree.restore()
    except XMLfileNotfound:
      pass

    mainScreen = Screen(name="mainScreen")
    mainScreen.add_widget(MainLayout())

    leafScreen = LeafScreen(name="leafScreen")

    sm.add_widget(mainScreen)
    sm.add_widget(leafScreen)
    return sm
  def on_stop(self):
    tree.save()
    pass

if __name__ == '__main__':
    ScrollViewApp().run()

