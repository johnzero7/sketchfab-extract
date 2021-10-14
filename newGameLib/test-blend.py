import bpy
import os
from mathutils import Matrix



def showbone(bone):
	print(b.matrix)
	#print('ARMATURESPACE')
	#print(b.matrix['ARMATURESPACE'])
	#print('BONESPACE')
	#print(b.matrix['BONESPACE'])


os.system('cls')
print('-------')

#print(obj.getData.edit.getCurrent())



#print(blenddat.faceUV)
#print(blendMesh.vertexUV)
print(bpy.context.object.data.edit_bones.active.name)
b=bpy.context.object.data.edit_bones['UniqueID_149']
showbone(b)
b=bpy.context.object.data.edit_bones['UniqueID_151']
showbone(b)
b=bpy.context.object.data.edit_bones['UniqueID_161']
showbone(b)

print(b.matrix.decompose())

if(1):
    b.matrix= Matrix((
            [0.990812, 0.105891, 0.084131, -0.538684],
            [-0.050080, 0.865113, -0.499070, 0.2473],
            [-0.125630, 0.490271, 0.862468, 0.680248],
            [0, 0, 0, 0]
        )).to_4x4()

