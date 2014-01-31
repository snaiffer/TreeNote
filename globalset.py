#!/usr/bin/env python

import os

progDir = os.path.dirname(os.path.realpath(__file__))
dataPath = progDir + '/data'


if __name__ == '__main__':
  print 'progDir = ' + progDir
  print 'dataPath = ' + dataPath
