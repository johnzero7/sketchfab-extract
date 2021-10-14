import os

from importlib import reload

import newGameLib.starter


reload(newGameLib.starter)
reload(newGameLib)


os.system('cls')

if __name__ == "__main__":
    path = r'C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Maria Naruse\file.osgjs'
    path = r'C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Marina (Off the Hook)\file.osgjs'
    path = r'C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\B&S Lyn (fanart)2\file.osgjs'
    path = r"C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Tanuko\file.osgjs"
    path = r"C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Ar tonelico\file.osgjs"
    path = r"C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Thiria\file.osgjs"
    #path = r"C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Kitsune Teen\file.osgjs"
    newGameLib.starter.test(path)

