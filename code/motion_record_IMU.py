import bpy
import time
import csv

            
def get_position(object_name):
    
    # Mention which object to track
    obj=bpy.context.scene.objects[object_name]
    x=obj.location.x
    y=obj.location.y
    z=obj.location.z
    
    # Specify rotation rep
    rot_z=obj.rotation_euler.z
    rot_y=obj.rotation_euler.y
    rot_x=obj.rotation_euler.x
    return x,y,z,rot_x,rot_y,rot_z

if __name__=="__main__":
    get_position()
#    bpy.ops.screen.animation_play()