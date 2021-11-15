import bpy
def set_motion(object_name,points):
    # points is of type : {frame: (x,y,z)}
    obj=bpy.context.scene.objects[object_name]
    for frame in points:
        obj.location=points[frame][0]
        obj.rotation_euler=points[frame][1]
        obj.keyframe_insert(data_path="location",frame=frame)
        obj.keyframe_insert("rotation_euler", frame = frame)

