import bpy
import numpy as np
import random
import os
import time

import sys
path=r"..//code//"

if path not in sys.path:
    sys.path.append(path)

from create_scene import CreateLandscape, import_bluerov, AddOysters,DeleteAllObjects,ApplyTexture
from motion_record_IMU import get_position


START_FRAME = 1
END_FRAME = 400

SURFACE_SIZE = 10



#TODO:
def calculate_ideal_imu():
    return

#TODO:
def calculate_sim_imu():
    return


def render_img(img_dir,keyframe): 
    # Use for HQ render:
#        bpy.data.cameras['Camera'].dof.use_dof = False
    save_path = img_dir+keyframe+'.jpg'
    bpy.context.scene.render.filepath = save_path
    bpy.ops.render.render(write_still = False)




def pipeline(floor_noise,landscape_texture_dir,bluerov_path,bluerov_location,oysters_model_dir,oysters_texture_dir,\
             n_clusters, min_oyster, max_oyster,renders_save_dir):
    
    CreateLandscape(floor_noise,landscape_texture_dir)
    
    
    import_bluerov(bluerov_path,bluerov_location)
    
    
    AddOysters(oysters_model_dir,oysters_texture_dir, n_clusters, min_oyster, max_oyster)
    
    # TODO: Play the animation
    
    # Time delay for oysters drop
#   time.sleep(10)

    
    for i in range(20):
        bpy.context.scene.frame_set(i)
        
        x,y,z,rot_x,rot_y,rot_z=get_position('BlueROV')
        
#       TODO
#       vx_i,vy_i,vz_i,wx_i,wy_i,wz_i=calculate_ideal_imu()

#       TODO
#        vx,vy,vz,wx,wy,wz=calculate_sim_imu()

#       TODO
#        plot_imu(vx,vy,vz,wx,wy,wz)

#        render_img(renders_save_dir,i)


    
if __name__=="__main__":
    DeleteAllObjects()
    
    floor_noise=3.5
#    landscape_texture_dir = r"..//data//blender_data//landscape//textures//"
    landscape_texture_dir="D:\\Programming\\Underwater-Robotics\\data\\blender_data\\landscape\\textures"
    
    
    bluerov_path="D:\\Programming\\Blender\\assets\\BlueRov2.dae"
    bluerov_location=(10,0,10)
    
    
    oysters_model_dir=r"D:\\Programming\\Underwater-Robotics\\data\\blender_data\\oysters\\model\\"
    oysters_texture_dir=r"D:\\Programming\\Underwater-Robotics\\data\\blender_data\\oysters\\textures\\"
    n_clusters=1
    min_oyster=5
    max_oyster=None
    
    
    renders_save_dir="D:\\Programming\\Underwater-Robotics\\data\\renders\\"
    
    pipeline(floor_noise,landscape_texture_dir,bluerov_path,bluerov_location,oysters_model_dir,oysters_texture_dir,\
             n_clusters, min_oyster, max_oyster,renders_save_dir)
