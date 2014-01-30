#!/usr/bin/env python

import sys
import os

def isFileThere(fileName, path):
  existents = os.listdir(path)
  try:
    existents.index(fileName)
  except:
    return False
  else:
    return True

def generateGoodName(fileName, path):
  if isFileThere(fileName, path):
    fileName += '1'
    return generateGoodName(fileName, path)
  else:
    return fileName

class Leaf():
  _dataPath = './data'
  def __init__(self, name=' ', text=''):
    self.name = name
    self.desc = ''
    self._path = self._dataPath + '/' + generateGoodName(name, self._dataPath)
    self.write(text) 
  def read(self):
    fd = open(self._path, 'rb')
    return fd.read()
  def write(self, text):
    fd = open(self._path, 'wb')
    try:
      fd.write(text)
      self.desc = text[:15]
    finally:  
      fd.close()
  def prepare_del(self):
    os.remove(self._path)
  def __str__(self):
    return 'Leaf:\n  name: %s\n  desc: %s' % (self.name, self.desc)


if __name__ == '__main__':
  test_str = 'leaf1_text'
  print 'Test for creating and reading:'
  leaf1 = Leaf('leaf1', test_str)
  leaf2 = Leaf('leaf2')
  if leaf1.read() == 'leaf1_text':
    print 'PASS'
  if leaf2.read() == ' ':
    print 'PASS'

  test_str2 = 'New text'
  print 'Test for rewritting:'
  leaf1.write(test_str2)
  if leaf1.read() == test_str2:
    print 'PASS'

  leaf1.prepare_del()
  leaf2.prepare_del()


