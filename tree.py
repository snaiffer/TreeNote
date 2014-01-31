#!/usr/bin/env python

import sys
import os
from stack import *
from branch import *
from leaf import *

def print_all(item, iterNum=0):
  indent='  '*iterNum
  print str(indent) + str(item)
  if isinstance(item, Branch):
    if item.get() == []:
      return
    else:
      iterNum += 1
      for b_cur in item.get():
        print_all(b_cur, iterNum)

class Tree():
  def __init__(self, root=Branch(name='root')):
    self.__root = root
    self.__path = Stack()
    self.__path.push(root)
  def reachRoot(self):
    if self.__path.size() == 1:
      return True
    else:
      return False
  def upTo(self, branchNum):
    self.__path.push(self.__path.top().get(branchNum))
  def down(self):
    if not self.reachRoot():
      self.__path.pop()
    else:
      raise AchiveRoot
  def curItem(self):
    return self.__path.top()

class TreeException(Exception):
  pass
class AchiveRoot(TreeException):
  pass

if __name__ == '__main__':
  tree = Tree()
  tree.curItem().add(Branch('branch1'))
  tree.curItem().add(Branch('branch2'))
  tree.curItem().add(Leaf('leaf1'))
  print_all(tree.curItem())

  print '\n\t Go up to branch1\n'
  tree.upTo(0)
  tree.curItem().add(Leaf('leaf2'))
  tree.curItem().add(Leaf('leaf3'))
  tree.curItem().add(Branch('branch3'))
  print_all(tree.curItem())

  print '\n\t Go down\n'
  tree.down()
  print_all(tree.curItem())

  print '\n\t Fill in leaf1\n'
  tree.upTo(2)
  tree.curItem().write('Hello! Im here!')
  tree.down()
  print_all(tree.curItem())

  print '\n\t Remove leaf2\n'
  tree.upTo(0)
  tree.curItem().remove(0)
  tree.down()
  print_all(tree.curItem())

  print '\n\t Remove branch1\n'
  tree.curItem().remove(0)
  print_all(tree.curItem())


