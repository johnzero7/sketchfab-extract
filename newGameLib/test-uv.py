import bpy
obj = bpy.context.active_object
poly = obj.data.polygons
uv_layer = obj.data.uv_layers.active.data

print('--------')
print(f'polygons {len(poly)}')
print(f'UVs {len(uv_layer)}')

for poly in obj.data.polygons:
    print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))

    # range is used here to show how the polygons reference loops,
    # for convenience 'poly.loop_indices' can be used instead.
    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
        print(f"    Vertex: {obj.data.loops[loop_index].vertex_index}")
        print(f"    UV: {uv_layer[loop_index].uv}")
