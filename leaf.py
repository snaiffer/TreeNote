#!/usr/bin/env python

import sys
import os
import globalset

def generate_UniqueName(fileName, path):
  if os.path.exists(path + '/' + fileName):
    fileName += '1'
    return generate_UniqueName(fileName, path)
  else:
    return fileName

class Leaf():
  def __init__(self, name=' ', text=''):
    self.name = name
    self.desc = ''
    if not os.path.isdir(globalset.dataPath):
      os.makedirs(globalset.dataPath)
    self._path = globalset.dataPath + '/' + generate_UniqueName(name, globalset.dataPath)
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
    return self.name + '\t desc: "' + self.desc + '"\n\t____text____:\n' + self.read()


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
  print leaf1  

  leaf1.prepare_del()
  leaf2.prepare_del()


