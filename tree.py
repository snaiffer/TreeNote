#!/usr/bin/env python3
" A module is for representating and working with tree structure "

from stack import *
from branch import *
from leaf import *
from xml.etree.ElementTree import *
from general import *

def print_all(item, iterNum=0):
  " print all tree structure "
  indent='  '*iterNum
  print( str(indent) + str(item) )
  if isinstance(item, Branch):
    if item.get() == []:
      return
    else:
      iterNum += 1
      for b_cur in item.get():
        print_all(b_cur, iterNum)

class Tree():
  " A class is for representating and working with tree structure "
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
  def getPath(self):
    return str(self.__path)[5:]
  def curItem(self):
    return self.__path.top()
  def save(self):
    " Save tree structure as xml format "
    def generate_XML(tree_curI, xml_curE):
      if isinstance(tree_curI, Branch):
        curE = Element('Branch', name=tree_curI.name)
        xml_curE.append(curE)
        if tree_curI.get() == []:
          return
        else:
          for curI in tree_curI.get():
            generate_XML(curI, curE)
      if isinstance(tree_curI, Leaf):
        curE = xml_curE.append(Element('Leaf', name=tree_curI.name, desc=tree_curI.desc, path=tree_curI._path))
        return
    xml_tree = Element("root")
    generate_XML(self.__root, xml_tree)
    ElementTree(xml_tree).write(structureFile)

  def restore(self):
    " Restore tree structure from xml file "
    def restore_fromXML(tree_curI, xml_curE):
      elements = [elem for elem in xml_curE]
      if xml_curE.tag == 'root':
        elements = [elem for elem in elements[0]]
      for curE in elements:
        if curE.tag == 'Branch':
          curI = tree_curI.add(Branch(name=curE.get('name')))
          restore_fromXML(curI, curE)
        if curE.tag == 'Leaf':
          curI = tree_curI.add(Leaf(name=curE.get('name'), desc=curE.get('desc'), path=curE.get('path')))
    try:
      xml_tree = ElementTree(file=structureFile)
      xml_root = xml_tree.getroot()
      tree = self.__root
      restore_fromXML(tree, xml_root)
    except IOError:
      raise XMLfileNotfound
      pass

class TreeException(Exception):
  pass
class AchiveRoot(TreeException):
  pass
class XMLfileNotfound(TreeException):
  pass

if __name__ == '__main__':
  tree = Tree()
  try:
    tree.restore()
    print( tree.getPath() )
    print_all(tree.curItem())
  except XMLfileNotfound:
    print( "Error: XML file isn't found" )

  """
  tree.curItem().add(Branch('branch1'))
  tree.curItem().add(Branch('branch2'))
  tree.curItem().add(Leaf('leaf1'))
  print_all(tree.curItem())

  print( '\n\t Go up to branch1\n' )
  tree.upTo(0)
  tree.curItem().add(Leaf('leaf2'))
  tree.curItem().add(Leaf('leaf3'))
  tree.curItem().add(Branch('branch3'))
  print_all(tree.curItem())

  print( '\n\t Go down\n' )
  tree.down()
  print_all(tree.curItem())

  print( '\n\t Fill in leaf1\n' )
  tree.upTo(2)
  tree.curItem().write('Hello! Im here!')
  tree.down()
  print_all(tree.curItem())

  print( '\n\t Remove leaf2\n' )
  tree.upTo(0)
  tree.curItem().remove(0)
  tree.down()
  print_all(tree.curItem())

  print( '\n\t Remove branch1\n' )
  tree.curItem().remove(0)
  print_all(tree.curItem())

  tree.save()
  """
