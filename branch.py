#!/usr/bin/env python
" A module is for realising tree structure "

from leaf import *

class Branch():
  """
  A class realises tree structure with unlimited nesting 
  leaf module is necessary for working
  """
  def __init__(self, name='branch'):
    self.name = unicode(name)
    self._children = []
  def add(self, item):
    self._children.append(item)
    return self._children[-1]
  def get(self, index=-1):
    if index == -1:
      return self._children
    else:
      return self._children[index]
  def _cleaner(self, item):
    if isinstance(item, Branch):
      if item.get() == []:
        return
      else:
        for b_cur in item.get():
          self._cleaner(b_cur)
    if isinstance(item, Leaf):
      item.prepare_del()
      return
  def remove(self, index):
    self._cleaner(self._children[index])
    del self._children[index]
  def __str__(self):
    return self.name.encode('utf8')
    #return self.name + ': (with ' + str(len(self._children)) + ' children)'

if __name__ == '__main__':
  branch = Branch(name='branch')
  branch1 = Branch(name='branch1')
  branch1.add(Branch(name='branch2'))
  branch1.add(Branch(name='branch3'))
  branch.add(branch1)
  addedB = branch.add(Branch(name='branch4'))

  print branch
  print '==================\n'

  if branch.get(0).get(0).name == 'branch2':
    print 'PASS'
  branch.remove(0)  
  if branch.get(0).name == 'branch4':
    print 'PASS'
  if addedB.name == 'branch4':
    print 'PASS'

