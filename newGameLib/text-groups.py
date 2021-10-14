obj = bpy.context.object
x=[vert for vert in obj.data.vertices if len(vert.groups)>4]

all_obj = bpy.context.scene.objects
x=[vert.index for obj in all_obj if (obj.type == 'MESH') for vert in obj.data.vertices if len(vert.groups)>4]

x=[{obj.name:{vert.index:len(vert.groups)}} for obj in all_obj if (obj.type == 'MESH') for vert in obj.data.vertices if len(vert.groups)>4]


matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flatten_matrix = [val for sublist in matrix for val in sublist]
print(flatten_matrix)





bpy.context.edit_object.data.vertices[0].selected





import bpy
import bmesh
me = bpy.context.edit_object.data
bm=bmesh.from_edit_mesh(me)
bm.select_history.add(bm.verts[5])
bmesh.update_edit_mesh(me)
bm=bmesh.update_edit_mesh(me)




import bpy
import bmesh
me = bpy.context.object.data
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh
bm.select_history.add(bm.verts[5])
bm.to_mesh(me)
bm.free()

