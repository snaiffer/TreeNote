#!/usr/bin/env python
" A module is for working with text note "

from general import *

class Leaf():
  """
  A class is for storaging text note in utf-8
  general module is necessary for working
  """
  def __init__(self, name=' ', text='', desc='', path=' '):
    self.name = unicode(name)
    self.desc = ''
    if not os.path.isdir(dataPath):
      os.makedirs(dataPath)
    if path == ' ':  
      self._path = dataPath + '/' + generate_UniqueName(name, dataPath)
    else:
      self._path = path
    if not os.path.exists(self._path):
      self.write(text) 
  def read(self):
    " Read the note "
    fd = open(self._path, 'rb')
    return fd.read().decode('utf-8', 'xmlcharrefreplace')
  def write(self, text):
    " Save to the note "
    fd = open(self._path, 'wb')
    try:
      fd.write(text.encode('utf-8', 'xmlcharrefreplace'))
      self.desc = text[:15]
    finally:  
      fd.close()
  def prepare_del(self):
    " Prepare to remove the note "
    os.remove(self._path)
  def __str__(self):
    return (self.name + '\t desc: "' + self.desc + '"\n\t____text____:\n' + self.read()).encode('utf8')


if __name__ == '__main__':
  test_str = 'leaf1_text'
  print 'Test for creating and reading:'
  leaf1 = Leaf('leaf1', test_str)
  leaf2 = Leaf('leaf2')
  if leaf1.read() == 'leaf1_text':
    print 'PASS'
  if leaf2.read() == '':
    print 'PASS'

  test_str2 = 'New text'
  print 'Test for rewritting:'
  leaf1.write(test_str2)
  if leaf1.read() == test_str2:
    print 'PASS'
  print leaf1  

  leaf1.prepare_del()
  leaf2.prepare_del()


