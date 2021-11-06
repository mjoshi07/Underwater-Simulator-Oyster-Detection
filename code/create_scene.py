# Create Custom Mesh for Ground surface

# Author: Chahat Deep Singh
# University of Maryland. College Park
# MIT License (c) 2021

# Import Libraries
import bpy
import bmesh
import ant_landscape
import math
import numpy as np
import random
import os


# Force Enter the Object Mode
try:
    bpy.ops.object.mode_set(mode = 'OBJECT')
except:
    pass


# List of Flags:

START_FRAME = 1
END_FRAME = 400

SURFACE_SIZE = 40


def SetCamera(x=0, y=0, z=2, roll=0, pitch=0, yaw=0):
    # selects previously generated camera 
    bpy.ops.object.select_by_type(type='CAMERA')
    
    # deletes previously generated camera
    bpy.ops.object.delete()
    
    # creates a new camera object at x,y,z, roll, pitch, yaw
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x, y, z),\
     rotation=(roll, pitch, yaw), scale=(1, 1, 1))



# Delete all the current meshes
def DeleteAllObjects():
    # Select all the Meshes:
    bpy.ops.object.select_by_type(type='MESH')
    
    # Select all the objects including the camera and light sources:
    # bpy.ops.object.select_all(action='SELECT')
    
    # Delete all the objects
    bpy.ops.object.delete()
    
    # Deselect all (if required):
    bpy.ops.object.select_all(action='DESELECT')
  



def CreateLandscape(FloorNoise=1.2, noise_type=None):
    # Create a plane of Size X, Y, Z
    [mesh_size_x, mesh_size_y, mesh_size_z] = [SURFACE_SIZE, SURFACE_SIZE, 0] # in m
    
    # list of acceptable noise type for terrain generation
    noise=['multi_fractal', 'hybrid_multi_fractal', 'hetero_terrain', 'fractal', 'shattered_hterrain', 'strata_hterrain', 'vl_hTerrain', 'distorted_heteroTerrain', 'double_multiFractal', 'rocks_noise', 'slick_rock', 'planet_noise']
    noise_type=random.choice(noise)
    bpy.ops.mesh.landscape_add(ant_terrain_name="Landscape", land_material="", water_material="", texture_block="", at_cursor=False, smooth_mesh=True, \
        tri_face=False, sphere_mesh=False, subdivision_x=256, subdivision_y=256, mesh_size=2, mesh_size_x=mesh_size_x, mesh_size_y=mesh_size_y, random_seed=1, \
        noise_offset_x=0, noise_offset_y=0, noise_offset_z=1, noise_size_x=1, noise_size_y=1, noise_size_z=2, noise_size=3, noise_type=noise_type, \
        basis_type='BLENDER', vl_basis_type='VORONOI_F1', distortion=1.5, hard_noise='1', noise_depth=8, amplitude=1.47, frequency=1.71, dimension=FloorNoise,\
        lacunarity=2, offset=1, gain=1, marble_bias='1', marble_sharp='5', marble_shape='3', height=1, height_invert=False, height_offset=0, fx_mixfactor=0, \
        fx_mix_mode='0', fx_type='0', fx_bias='0', fx_turb=0, fx_depth=0, fx_amplitude=0.5, fx_frequency=1.5, fx_size=1, fx_loc_x=0, fx_loc_y=0, fx_height=0.5,\
        fx_invert=False, fx_offset=0, edge_falloff='0', falloff_x=4, falloff_y=4, edge_level=0, maximum=5, minimum=-0.5, vert_group="", strata=5, strata_type='0',\
        water_plane=False, water_level=0.01, remove_double=False, show_main_settings=True, show_noise_settings=True, show_displace_settings=True, refresh=True, auto_refresh=True)
    bpy.context.active_object.name = 'Landscape'
    
    # Adding texture 
#    bpy.context.area.type = 'NODE_EDITOR'
#    cont = bpy.context.area.type
#    print("context:",str(cont))
#    bpy.ops.node.nw_add_textures_for_principled(filepath="..//..\\..\\Blender\\assets\\Ground029_8K-JPG\\Ground029_8K_AmbientOcclusion.jpg",\
#     directory="D:\\Blender\\assets\\Ground029_8K-JPG\\",\
#      files=[{"name":"Ground029_8K_Roughness.jpg", "name":"Ground029_8K_Roughness.jpg"},\
#       {"name":"Ground029_8K_Displacement.jpg", "name":"Ground029_8K_Displacement.jpg"},\
#        {"name":"Ground029_8K_Color.jpg", "name":"Ground029_8K_Color.jpg"},\
#         {"name":"Ground029_8K_AmbientOcclusion.jpg",\
#          "name":"Ground029_8K_AmbientOcclusion.jpg"}])

#    bpy.ops.image.open(filepath="//..\\..\\Blender\\assets\\4.jpg", directory="D:\\Blender\\assets\\", files=[{"name":"4.jpg", "name":"4.jpg"}], show_multiview=False)

    # set terrain rigidbody to Passive
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.rigid_body.collision_shape = 'MESH'


def AddOysters(model_dir_path=None, n_clusters=5, min_oyster=5, max_oyster=None):
    
    if model_dir_path is None or not os.path.exists(model_dir_path):
        print("MODELS NOT FOUND")
        return 
    
        
    cal_n_oysters = True
    if max_oyster is None:
        n_oyster = min_oyster
        cal_n_oysters = False
    
    # calculate cluster offset values
    cluster_offset_x=SURFACE_SIZE*0.15
    cluster_offset_y=SURFACE_SIZE*0.15
    
    # list of -1 and 1 to choose sign for cluster offset 
    signs=[-1,1,1,-1,-1,1,-1]
    
    # list of mesh names available
    mesh_names=['oysterA','oysterB','oysterC','oysterD','oysterE','oysterF','oyster1','oysterG','oyster2',\
    'oyster3','oyster4','oyster5','oyster6']

    for i in range(n_clusters):
        
        if cal_n_oysters:
            n_oyster = random.choice(range(min_oyster, max_oyster))
            
        cluster_mesh_names = [random.choice(mesh_names) for i in range(n_oyster)]
        cluster_center=[(random.random()*2-1)*SURFACE_SIZE*.50 + random.choice(signs)*cluster_offset_x,(random.random()*2-1)*SURFACE_SIZE*0.50+random.choice(signs)*cluster_offset_y]
        
        if cluster_center[0] > SURFACE_SIZE*0.37:
            cluster_center[0]  = SURFACE_SIZE*0.37
        elif cluster_center[0] < -SURFACE_SIZE*0.37:
            cluster_center[0]  = -SURFACE_SIZE*0.37
            
        if cluster_center[1] > SURFACE_SIZE*0.37:
            cluster_center[1]  = SURFACE_SIZE*0.37
        elif cluster_center[1] < -SURFACE_SIZE*0.37:
            cluster_center[1]  = -SURFACE_SIZE*0.37
        
        var_x=SURFACE_SIZE*0.10
        var_y=SURFACE_SIZE*0.10
        z_val=0

        for mesh in cluster_mesh_names:
            z_val+=1
            file_path=model_dir_path + "//" + mesh + ".stl"
            bpy.ops.import_mesh.stl(filepath=file_path)
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.scale[0] = 0.005
            bpy.context.object.scale[1] = 0.005
            bpy.context.object.scale[2] = 0.005
            rn=random.random()
            bpy.context.object.location.x=rn*var_x+cluster_center[0]
            rn=random.random()
            bpy.context.object.location.y=rn*var_y+cluster_center[1]
#            bpy.context.object.location.z=5    
            # vary z also         
            bpy.context.object.location.z=z_val

            bpy.ops.rigidbody.object_add(type='ACTIVE')
            bpy.context.object.rigid_body.mass = 10
    bpy.ops.object.select_all(action='DESELECT')

   
    


if __name__ == '__main__':
    floor_noise=3.5
    n_clusters=3
    min_oyster=2
    max_oyster=5
    model_dir_path = "D:\\Programming\\Blender\\assets\\modified_oyster\\modified_oyster\\"
    
    DeleteAllObjects()
    CreateLandscape(floor_noise)
    AddOysters(model_dir_path,n_clusters,min_oyster, max_oyster)
    SetCamera()
