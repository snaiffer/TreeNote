#!/usr/bin/env python
" A module is for stack realisation "

class Stack():
  " A class is for stack realisation "
  def __init__(self):
    self.__stack = []
  def push(self, item):
    self.__stack.append(item)
  def pop(self):
    return self.__stack.pop()
  def top(self):
    return self.__stack[-1]
  def isEmpty(self):
    if self.__stack == []:
      return True
    else:
      return False
  def size(self):
    return len(self.__stack)
  def getAll(self):
    " get all items of the stack "
    return self.__stack
  def __str__(self):
    if self.__stack == []:
      return '/'
      #return 'Stack is empty'
    else:
      return '/' + ''.join([str(cur) + '/' for cur in self.__stack])
      #return 'Stack: top-> ' + str(self.__stack) + ' <-end' 

if __name__ == '__main__':
  testStack = Stack()
  testStack.push(1)
  testStack.push(3)
  testStack.push(2)

  print testStack.getAll()

  print testStack
  while not testStack.isEmpty():
    print testStack.pop()
    print testStack
