#!/usr/bin/env python3
" A module is for general settings "

import os

progDir = os.path.dirname(os.path.realpath(__file__))
dataPath = progDir + '/../TreeNote_data'
if not os.path.exists(dataPath):
  os.makedirs(dataPath)
structureFile = dataPath + '/structure.xml'

def generate_UniqueName(fileName, path):
  if os.path.exists(path + '/' + fileName):
    fileName += '1'
    return generate_UniqueName(fileName, path)
  else:
    return fileName


if __name__ == '__main__':
  print( 'progDir = ' + progDir )
  print( 'dataPath = ' + dataPath )
  print( 'structureFile = ' + structureFile )
