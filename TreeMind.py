#!/usr/bin/env python

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ObjectProperty

from tree import *

tree = Tree()
tree.curItem().add(Branch('branch1'))
tree.curItem().add(Branch('branch2'))
tree.curItem().add(Leaf('leaf1'))
tree.upTo(0)
tree.curItem().add(Leaf('leaf2'))
tree.curItem().add(Leaf('leaf3'))
tree.curItem().add(Branch('branch3'))
tree.down()
print_all(tree.curItem())

class ButtonTreeItem(Button):
  def __init__(self, num, **kwargs):
    super(ButtonTreeItem, self).__init__(**kwargs)
    self.size_hint_y = None
    self.num = num

class ButtonBranch(ButtonTreeItem):
  def __init__(self, content, **kwargs):
    super(ButtonBranch, self).__init__(**kwargs)
    self.content = content
  def on_press(self):
    global tree
    tree.upTo(self.num)
    self.content.showTree()
    return super(ButtonBranch, self).on_press()

class ButtonLeaf(ButtonTreeItem):
  def __init__(self, **kwargs):
    super(ButtonLeaf, self).__init__(**kwargs)
    self.background_color=[1,0,1,1]
  def on_press(self):
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

  def goUp(self):
    pass

  def goBack(self, *args):
    global tree
    if not tree.reachRoot():
      tree.down()
      self.showTree()

"""
  def add_newItem(self, *args):
    print 'Add NewItem'
    if self.textField.text != '':
      self.data.db.append(self.textField.text)
      self.add_widget(Item(self.textField.text))
      self.textField.text = ''

  def add_Item(self, text):
    print 'Add item'
    self.add_widget(Item(text))

  def find(self, instance, text):
    print 'Find ' + text
    if text == '':
      self.showData(self.data.db)      
    else:  
      foundData = []
      for cur in self.data.db:
        try:
          pos = cur.index(text)
        except ValueError:
          pass
        else:
          if pos == 0:
            foundData.append(cur)
      self.showData(foundData)      
      print foundData

  def showData(self, data):
    self.clear_widgets()
    for cur in data:
      self.add_Item(cur)
"""

class MainLayout(GridLayout):
  def __init__(self, **kwargs):
    super(MainLayout, self).__init__(**kwargs)
    self.cols=1

    # Top
    buttonBack = Button(text='Back', size_hint_x=0.1)
    textField = TextInput(multiline=False, size_hint_x=0.8)
    buttonAddItem = Button(text='AddBranch', size_hint_x=0.1)
    topLayout = BoxLayout(size_hint_y = 0.1)
    topLayout.add_widget(buttonBack)
    topLayout.add_widget(textField)
    topLayout.add_widget(buttonAddItem)
    self.add_widget(topLayout) 
    
    # Content
    contentLayout = ContentLayout(textField)
    scroll = ContentScroll(contentLayout)
    self.add_widget(scroll)
    buttonAddItem.bind(on_press=contentLayout.add_newBranch)
    buttonBack.bind(on_press=contentLayout.goBack)
    #textField.bind(text=contentLayout.find)


"""
class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)

class LeafScreen(Screen):
  pass

sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='WelcomeScreen'))
sm.add_widget(MainScreen(name='MainScreen'))
sm.add_widget(LeafScreen(name='LeafScreen'))
"""


class ScrollViewApp(App):
  def build(self):
    return MainLayout()
  def on_stop(self):
    pass

if __name__ == '__main__':
    ScrollViewApp().run()

