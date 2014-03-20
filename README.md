TreeNote
========
TreeNote is a note manager with tree-like hierarchy.

The app is written on kivy library -- Open source Python library that is cross platform. 
But target of this app is android devices.


========
for compilation to android:
Note: you need setup python-for-android

) start emulator:
android avd
) package to .apk
cd ~/temp/py/kivy/python-for-android/dist/default
./build.py --dir /home/snaiffer/temp/TreeNote --name "TreeNote" --package snaif.kivy.TreeNote --orientation "sensor" --version 1.1.22 debug installd
