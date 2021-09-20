import os

from importlib import reload

import newGameLib.starter


reload(newGameLib.starter)
reload(newGameLib)


os.system('cls')

if __name__ == "__main__":
    newGameLib.starter.test()

