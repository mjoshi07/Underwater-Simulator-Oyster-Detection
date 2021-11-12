import bpy
from mathutils import Vector
import random
import os
import uuid
import shutil

"""
TODO - cite the main source of the code
"""

class Box:

    dim_x = 1
    dim_y = 1

    def __init__(self, min_x, min_y, max_x, max_y, dim_x=dim_x, dim_y=dim_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.dim_x = dim_x
        self.dim_y = dim_y

    @property
    def x(self):
        return round(self.min_x * self.dim_x)

    @property
    def y(self):
        return round(self.dim_y - self.max_y * self.dim_y)

    @property
    def width(self):
        return round((self.max_x - self.min_x) * self.dim_x)

    @property
    def height(self):
        return round((self.max_y - self.min_y) * self.dim_y)

    def __str__(self):
        return "<Box, x=%i, y=%i, width=%i, height=%i>" % \
               (self.x, self.y, self.width, self.height)

    def to_tuple(self):
        if self.width == 0 or self.height == 0:
            return (0, 0, 0, 0)
        return (self.x, self.y, self.width, self.height)


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            if z <= 0.0:
                continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return 0, 0, 0, 0
    return round(min_x * dim_x), round(dim_y - max_y * dim_y), round((max_x - min_x) * dim_x), round((max_y - min_y) * dim_y)
    


def write_bounds_2d(filepath, scene, cam_object, mesh_objects):
    with open(filepath, "w") as file: 
        for object in mesh_objects:
            x,y,w,h=camera_view_bounds_2d(scene, cam_object, object)
            x_c = x + w/2
            y_c = y + h/2
            if w != 0 and h != 0:
                file.write("0 {} {} {} {}\n".format((x_c)/640.0, (y_c)/480.0, w/640.0, h/480.0))           


if __name__ == "__main__":

    data = bpy.data
    scene = bpy.context.scene
    cam_object = data.objects['Camera']
    
    # object names whose bbox you want to save
    # if object is totally outside FOV, its bbox will be ignored
    mesh_names = [ 'Mesh_0.001', 'Mesh_0.002','Mesh_0.003','Mesh_0.004'
    , 'Mesh_0.005', 'Mesh_0.006','Mesh_0.007','Mesh_0.008', 'Mesh_0.009', 'Mesh_0.010'
    ,'Mesh_0.011','Mesh_0.012', 'Mesh_0.013', 'Mesh_0.014','Mesh_0.015','Mesh_0.016', 'Mesh_0.017', 
    'Mesh_0.018'    ,'Mesh_0.019','Mesh_0.020','Mesh_0.021']
    
    # Objects randomly varying in three regions- small (in around 1/4th FOV), camera (around full camera FOV), large (some objects might go outside FOV)
    mesh_names_small_region=[ 'Mesh_0.001', 'Mesh_0.002','Mesh_0.003','Mesh_0.004']
    mesh_names_camera_region=['Mesh_0.005', 'Mesh_0.006','Mesh_0.007','Mesh_0.008', 'Mesh_0.009', 'Mesh_0.010'
    ,'Mesh_0.011','Mesh_0.012', 'Mesh_0.013', 'Mesh_0.014','Mesh_0.015']
    mesh_names_large_region=['Landscape.001','Landscape.002','Landscape.003','Landscape.004','Landscape.005'
    ,'Landscape.006','Landscape.007','Landscape.008','Landscape.009','Landscape.010','Landscape.011'
    ,'Landscape.012','Landscape.013','Landscape.014','Landscape.015','Landscape.016','Mesh_0.016', 'Mesh_0.017', 'Mesh_0.018','Mesh_0.019','Mesh_0.020','Mesh_0.021']
    
    mesh_objects = [data.objects[name] for name in mesh_names]
    
    # Consts for respective x,y variation
    small_reg_x=1.3
    small_reg_y=0.8
    cam_reg_x=1.3
    cam_reg_y=0.8
    large_reg_x=1.5
    large_reg_y=1.1
    
    # No. of images to generate
    N_FRAMES=5000
    
    
    # for writing text file relative path is fine
    # for rendering images, blender might save it relative to its location
    path = "..//data//yolo_data//"
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
        

    for i in range(N_FRAMES):
        data = bpy.data
        filename = str(uuid.uuid1())
        filepath = path+filename+'.txt'  

        for mesh in mesh_names_small_region:
            obj=bpy.context.scene.objects[mesh]
            rn=-random.random()
            obj.location.x=rn*small_reg_x
            rn=-random.random()
            obj.location.y=rn*small_reg_y
#            
            
        for mesh in mesh_names_camera_region:
            obj=bpy.context.scene.objects[mesh]
            rn=2*random.random()-1
            obj.location.x=rn*cam_reg_x
            rn=2*random.random()-1
            obj.location.y=rn*cam_reg_y
#            
#            
        for mesh in mesh_names_large_region:
            obj=bpy.context.scene.objects[mesh]
            rn=2*random.random()-1
            obj.location.x=rn*large_reg_x
            rn=2*random.random()-1
            obj.location.y=rn*large_reg_y
         
        # Use for HQ render:
        bpy.data.cameras['Camera'].dof.use_dof = False
        save_path = path+filename+'.png'
        bpy.context.scene.render.filepath = save_path
        bpy.ops.render.render(write_still = False)
        write_bounds_2d(filepath, scene, cam_object, mesh_objects)
#       