#!/usr/bin/env python

class Stack():
  _stack = []
  def push(self, item):
    self._stack.append(item)
  def pop(self):
    return self._stack.pop()
  def top(self):
    return self._stack[-1]
  def isEmpty(self):
    if self._stack == []:
      return True
    else:
      return False
  def size(self):
    return len(self._stack)
  def __str__(self):
    if self._stack == []:
      return 'Stack is empty'
    else:
      return 'Stack: top-> ' + str(self._stack) + ' <-end' 

if __name__ == '__main__':
  testStack = Stack()
  testStack.push(1)
  testStack.push(3)
  testStack.push(2)
  print testStack

  while not testStack.isEmpty():
    print testStack.pop()
    print testStack
