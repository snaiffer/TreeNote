#!/usr/bin/env python

import pickle

class Data():
  def __init__(self, db, dbfile_name='dbfile.dat'):
    self.dbfile_name = dbfile_name
    self.db = db
  def load(self):
    try:
      with open(self.dbfile_name, 'rb') as dbfile:
        self.db = pickle.load(dbfile)
        dbfile.close()
    except IOError:
      pass
  def save(self):
    dbfile = open(self.dbfile_name, 'wb')
    pickle.dump(self.db, dbfile)
    dbfile.close()


if __name__ == '__main__':
  """
  l = [1,2,3,4,5]
  print '\n\tFor save:\n'
  print l
  data = Data(db=l)
  data.save()

  l2 = []
  data2 = Data(l2)
  data2.load()
  print '\n\tWhat we have loaded:'
  print l2
  print data2.db
  """

  from tree import * 
  """
  tree = Tree()
  tree.curItem().add(Branch('branch1'))
  tree.curItem().add(Branch('branch2'))
  tree.curItem().add(Leaf('leaf1'))
  print '\n\tFor save:\n'
  print_all(tree.curItem())
  data = Data(db=tree)
  data.save()
  """

  treeLoaded = Tree()
  data2 = Data(db=treeLoaded)
  data2.load()
  print '\n\tWhat we have loaded:'
  print_all(treeLoaded.curItem())
  print_all(data2.db.curItem())
  data2.db.upTo(0)
  print data2.db.curItem()


