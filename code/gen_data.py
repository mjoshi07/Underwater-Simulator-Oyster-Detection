import bpy
from mathutils import Vector
import random
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
        return (0, 0, 0, 0)
    print('reached herer')
    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )


def write_bounds_2d(filepath, scene, cam_ob, me_ob, frame_start, frame_end):

    with open(filepath, "w") as file: 
        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)
            for ob in me_ob:
                print(camera_view_bounds_2d(scene, cam_ob, ob))
                x,y,w,h=camera_view_bounds_2d(scene,cam_ob,ob)
                if(w!=0 and h!=0):
                    file.write("%i %i %i %i\n" % camera_view_bounds_2d(scene, cam_ob, ob))
            

if __name__ == "__main__":
    N_FRAMES=10
    for i in range(N_FRAMES):
        data = bpy.data
        filepath = 'C:/UMD/Fall2021/PRG/Blender/gen_bbox_YOLO/'+str(i)+'.txt'  
        cam_ob = data.objects['Camera']
        mesh_names = ['Cube', 'Cube.001', 'Cube.002']
        me_ob = [data.objects[name] for name in mesh_names]
        disp_factor_x=4.5
        disp_factor_y=4.5
        for mesh in mesh_names:
            obj=bpy.context.scene.objects[mesh]
            rn=2*random.random()-1
            obj.location.x=rn*disp_factor_x
            rn=2*random.random()-1
            obj.location.y=rn*disp_factor_y
            obj.rotation_euler.z=rn*2*3.14
        scene = bpy.context.scene
        frame_current = scene.frame_current
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        save_path='C:/UMD/Fall2021/PRG/Blender/gen_images_YOLO/'+str(i)+'.png'
        bpy.context.scene.render.filepath = save_path
        bpy.ops.render.render(write_still = True)
        write_bounds_2d(filepath, scene, cam_ob, me_ob, frame_start, 1)
    
