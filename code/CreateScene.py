# Create Custom Mesh for Ground surface

# Author: Chahat Deep Singh
# Modified By: Nitesh Jha, Mayank Joshi
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

SURFACE_SIZE = 10



def add_bluerov(model_path,bluerov_location=(0,0,0)):
    bpy.ops.wm.collada_import(filepath=model_path)
    model_name = "BlueROV"

    obj=bpy.context.scene.objects["Untitled_282"]
    obj.name=model_name
    # Initial position at origin
    obj.location.x=0
    obj.location.y=0
    obj.location.z=0
    obj.rotation_euler.x=1.57 # Orientation of DAE 

    # camera facing downwards
    roll=-1.57                # same as obj.rotation_euler.z
    pitch=0
    yaw=0
    bottom_cam, cam_obj = set_camera(0,0,0,roll, pitch, yaw)
    cam_obj.parent = bpy.data.objects[model_name]

    # camera (lidar/sonar) facing front
    roll=3.14                
    pitch=0
    yaw=0
    front_cam, cam_obj2 = set_camera(0,0,0,roll, pitch, yaw)
    cam_obj2.parent = bpy.data.objects[model_name]
    
    # Move to x,y,z
    obj=bpy.context.scene.objects[model_name]
    obj.location.x=bluerov_location[0]
    obj.location.y=bluerov_location[1]
    obj.location.z=bluerov_location[2]

    obj=bpy.context.scene.objects["BlueROV"]
    obj.location=bluerov_location

    return front_cam, bottom_cam

def set_light(x=0,y=0,z=60,energy=50000):
    bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(x,y,z), scale=(1, 1, 1))
    # bpy.context.space_data.context = 'DATA'
    bpy.context.object.data.energy = energy



def set_camera(x=0, y=0, z=2, roll=0, pitch=0, yaw=0):
    # creates a new camera object at x,y,z, roll, pitch, yaw
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x, y, z),\
     rotation=(roll, pitch, yaw), scale=(1, 1, 1))
    
    return bpy.context.object.name, bpy.context.object



# Delete all the current meshes
def delete_objs():
    # Select all the Meshes:
    bpy.ops.object.select_by_type(type='MESH')
    
    # Delete all the objects
    bpy.ops.object.delete()

     # selects previously generated camera 
    bpy.ops.object.select_by_type(type='CAMERA')
    
    # # deletes previously generated camera
    bpy.ops.object.delete()
    
    # Deselect all (if required):
    bpy.ops.object.select_all(action='DESELECT')
  

def apply_texture(PassiveObject, mat):
    if PassiveObject.data.materials:
        PassiveObject.data.materials[0] = mat
    else:
        PassiveObject.data.materials.append(mat)
        


def create_landscape(FloorNoise=1.2, texture_dir_path=None):
    # Create a plane of Size X, Y, Z
    [mesh_size_x, mesh_size_y, mesh_size_z] = [SURFACE_SIZE, SURFACE_SIZE, 0] # in m
    
    # list of acceptable noise type for terrain generation
    noise=['multi_fractal', 'hybrid_multi_fractal',\
     'hetero_terrain', 'fractal', 'shattered_hterrain',\
      'strata_hterrain', 'vl_hTerrain', 'distorted_heteroTerrain', \
      'double_multiFractal', 'rocks_noise', 'slick_rock', 'planet_noise']
      
    noise_type=random.choice(noise)
    noise_val=random.randint(0,100)
    
    bpy.ops.mesh.landscape_add(ant_terrain_name="Landscape", land_material="", water_material="", texture_block="", at_cursor=False, smooth_mesh=True, \
        tri_face=False, sphere_mesh=False, subdivision_x=256, subdivision_y=256, mesh_size=2, mesh_size_x=mesh_size_x, mesh_size_y=mesh_size_y, random_seed=noise_val, \
        noise_offset_x=0, noise_offset_y=0, noise_offset_z=1, noise_size_x=1, noise_size_y=1, noise_size_z=2, noise_size=3, noise_type=noise_type, \
        basis_type='BLENDER', vl_basis_type='VORONOI_F1', distortion=1.5, hard_noise='1', noise_depth=8, amplitude=1.47, frequency=1.71, dimension=FloorNoise,\
        lacunarity=2, offset=1, gain=1, marble_bias='1', marble_sharp='5', marble_shape='3', height=1, height_invert=False, height_offset=0, fx_mixfactor=0, \
        fx_mix_mode='0', fx_type='0', fx_bias='0', fx_turb=0, fx_depth=0, fx_amplitude=0.5, fx_frequency=1.5, fx_size=1, fx_loc_x=0, fx_loc_y=0, fx_height=0.5,\
        fx_invert=False, fx_offset=0, edge_falloff='0', falloff_x=4, falloff_y=4, edge_level=0, maximum=5, minimum=-0.5, vert_group="", strata=5, strata_type='0',\
        water_plane=False, water_level=0.01, remove_double=False, show_main_settings=True, show_noise_settings=True, show_displace_settings=True, refresh=True, auto_refresh=True)
    bpy.context.active_object.name = 'Landscape'
    PassiveObject = bpy.context.view_layer.objects.active
    mat = bpy.data.materials.new(name='Texture')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    
    if texture_dir_path is not None \
    and os.path.exists(texture_dir_path) \
    and len(os.listdir(texture_dir_path)):
        # randomly select a texture from texture dir
        texture_path = texture_dir_path + "//" + random.choice(os.listdir(texture_dir_path))
        if not os.path.exists(texture_path):
            print("CHECK RELATIVE PATH AGAIN")
            return True
        print(texture_path)
        texImage.image = bpy.data.images.load(filepath=texture_path) 
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        apply_texture(PassiveObject, mat)
        bpy.ops.object.editmode_toggle()

        bpy.ops.uv.smart_project()

    # set terrain rigidbody to Passive
    bpy.ops.rigidbody.object_add(type='PASSIVE')
                
    # Low Poly
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.ops.object.modifier_set_active(modifier="Decimate")
    bpy.context.object.modifiers["Decimate"].ratio =1
    bpy.context.object.rigid_body.collision_shape = 'MESH'


        
def add_oyster(model_dir_path=None,texture_dir_path=None, n_clusters=5, min_oyster=5, max_oyster=None):
    
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
    
    # list of mesh names in model_dir_path
    mesh_names=os.listdir(model_dir_path)


    # list of textures in texture_dir_path
    if texture_dir_path is None:
        texture_names = []
    else:
        texture_names=os.listdir(texture_dir_path)

    for i in range(n_clusters):
        
        if cal_n_oysters:
            n_oyster = random.choice(range(min_oyster, max_oyster))
        
        cluster_mesh_names = [random.choice(mesh_names) for i in range(n_oyster)]
        
        # Set center of cluster around which oysters will be dispersed
        cluster_center=[(random.random()*2-1)*SURFACE_SIZE*.50 + random.choice(signs)*cluster_offset_x,(random.random()*2-1)*SURFACE_SIZE*0.50+random.choice(signs)*cluster_offset_y]
        
        # Boundary condition in x axis
        if cluster_center[0] > SURFACE_SIZE*0.37:
            cluster_center[0]  = SURFACE_SIZE*0.37
        elif cluster_center[0] < -SURFACE_SIZE*0.37:
            cluster_center[0]  = -SURFACE_SIZE*0.37
        
        # Boundary condition in y axis
        if cluster_center[1] > SURFACE_SIZE*0.37:
            cluster_center[1]  = SURFACE_SIZE*0.37
        elif cluster_center[1] < -SURFACE_SIZE*0.37:
            cluster_center[1]  = -SURFACE_SIZE*0.37
        
        # Variation in coordinates within a cluster
        var_x=SURFACE_SIZE*0.10
        var_y=SURFACE_SIZE*0.10
        
        # Z is sequentially incremented for oyster within a cluster
        z_val=0

        for mesh_name in cluster_mesh_names:
            z_val+=1
            oyster_file_path=model_dir_path + "\\" + mesh_name
            bpy.ops.import_mesh.stl(filepath=oyster_file_path)
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            
            # Low Poly
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.ops.object.modifier_set_active(modifier="Decimate")
            bpy.context.object.modifiers["Decimate"].ratio = 0.008
            
            # Set oyster scales
            bpy.context.object.scale[0] = 0.005
            bpy.context.object.scale[1] = 0.005
            bpy.context.object.scale[2] = 0.005
            
            # Set oyster location in x and y randomly
            rn=random.random()
            bpy.context.object.location.x=rn*var_x+cluster_center[0]
            rn=random.random()
            bpy.context.object.location.y=rn*var_y+cluster_center[1]       
            bpy.context.object.location.z=z_val
            
            # Applying rigit body dynamics
            bpy.ops.rigidbody.object_add(type='ACTIVE')
            # Set mass
            bpy.context.object.rigid_body.mass = 10
            
            # Apply texture and Smart UV project
            current_Object = bpy.context.view_layer.objects.active
            mat = bpy.data.materials.new(name='Texture')
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            
            if len(texture_names):
                # randomly select one texture file and apply it
                texPath=texture_dir_path+'\\'+random.choice(texture_names)
                texImage.image = bpy.data.images.load(filepath=texPath) 
                mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
                apply_texture(current_Object, mat)
                bpy.ops.object.editmode_toggle()
                bpy.ops.uv.smart_project()
                bpy.ops.object.editmode_toggle()
            
            #Deselect all
            bpy.ops.object.select_all(action='DESELECT')

   
    


if __name__ == '__main__':
    
    pass

    # # delete all previously created objects in the scene
    # delete_objs()
    
    
    # # set arguments for landscape
    # floor_noise=3.5
    # landscape_texture_dir = r"..//data//blender_data//landscape//textures//"
    # create_landscape(floor_noise,landscape_texture_dir)
    
    # # set arguments for oysters
    # n_clusters=1
    # min_oyster=5
    # max_oyster=None
    # oyster_model_dir = r"..//data//blender_data//oysters//model//"
    # oyster_texture_dir = r"..//data//blender_data//oysters//textures//"
    # add_oyster(oyster_model_dir,oyster_texture_dir,n_clusters,min_oyster, max_oyster)
    
    # # Create camera
    # set_camera()
