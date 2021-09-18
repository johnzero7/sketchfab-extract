import os
import importlib
import newGameLib.starter
importlib.reload(newGameLib.starter)

os.system('cls')

newGameLib.starter.test()