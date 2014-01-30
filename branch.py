#!/usr/bin/env python

class Branch():
  def __init__(self, name='branch'):
    self.name=name
    self._issue=[]
  def add(self, item):
    self._issue.append(item)
  def get(self, index=-1):
    if index == -1:
      return self._issue
    else:
      return self._issue[index]
  def remove(self, index):
    del self._issue[index]
  def __str__(self):
    res = '%s:\n' % self.name
    for i_cur in self._issue:
      res += '  %s\n' % i_cur.name
    return res

if __name__ == '__main__':
  branch = Branch(name='branch')
  branch1 = Branch(name='branch1')
  branch1.add(Branch(name='branch2'))
  branch1.add(Branch(name='branch3'))
  branch.add(branch1)
  branch.add(Branch(name='branch4'))

  print branch
  print '==================\n'

  if branch.get(0).get(0).name == 'branch2':
    print 'PASS'
  branch.remove(0)  
  if branch.get(0).name == 'branch4':
    print 'PASS'

