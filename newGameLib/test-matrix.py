import bpy
import os
from datetime import datetime

from mathutils import Matrix
from math import radians,degrees



os.system('cls')

matR1 = Matrix.Rotation(radians(30), 4, 'X')
matR2 = Matrix.Rotation(radians(45), 4, 'Z')
matR = matR2 @ matR1
matT = Matrix.Translation((2,4,8))
mat = matT @ matR
mat = matT @ matR2 @ matR1

deco = mat.decompose()

print("now =", datetime.now())
print('-------')
print('parte location', deco[0])
print('-------')
print('parte rotation', deco[1].to_euler())
print('-------')
print('parte scale', deco[2])
print('-------mat')
print(mat)
print('-------OBJ matrix')
bpy.context.object.matrix_world=mat
print(bpy.context.object.matrix_world)
print('-------ROW0')
print(bpy.context.object.matrix_world[0])
