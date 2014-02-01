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

from tree import *

Builder.load_file('./TreeMind.kv')
tx = 'None'

class Branch(Button):
  def on_press(self):
    print 'on_press Branch'
    return super(Branch, self).on_press()

class Leaf(Button):
  def on_press(self):
    print 'on_press Leaf'
    return super(Leaf, self).on_press()


class MainLayout(GridLayout):
  def __init__(self, **kwargs):
    super(MainLayout, self).__init__(**kwargs)

class ContentLayout(GridLayout):
  pass

class MainScreen(Screen):
  pass

class LeafScreen(Screen):
  pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='MainScreen'))
sm.add_widget(LeafScreen(name='LeafScreen'))

class ScrollViewApp(App):
  def build(self):
    return sm
  def on_stop(self):
    pass

if __name__ == '__main__':
    ScrollViewApp().run()

