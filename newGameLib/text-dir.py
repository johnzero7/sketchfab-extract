import os
import json

os.getcwd()
path = r'C:\Users\Rodrigo\Downloads\sketchfab\PythonRipper\Models\Marina (Off the Hook)'
os.chdir(path)




f = open('file.osgjs',)
data = json.load(f)
f.close()




bone_matrix = Matrix(((-0.30297, -0.38529, -0.87164, 0), (-0.67395, -0.56004, 0.48181, 0), (-0.67379, 0.73342, -0.09, 0), (-1.07267, 1.97332, -0.16574, 1) ))
bone_max = Vector((1.10226, 2.18536, 1.46895))
bone_min = Vector((-1.00389, -0.782865, -1.59253))

bone_matrix @ bone_max
bone_matrix @ bone_min

bone_max @ bone_matrix
bone_min @ bone_matrix

bone_max - bone_min

