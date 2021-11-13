import bpy
import numpy as np
import os
import sys

path = r"..//code//"

if path not in sys.path:
    sys.path.append(path)

from CreateScene import delete_objs, create_landscape, add_bluerov, add_oyster, set_camera
from Utils import get_position, render_img
from ImuUtils import  cal_linear_acc, cal_angular_vel, acc_gen, gyro_gen, accel_high_accuracy, gyro_high_accuracy, vib_from_env
from RangeScanner import run_scanner, tupleToArray
import range_scanner


START_FRAME = 1
END_FRAME = 400

SURFACE_SIZE = 10

TIME_TO_WAIT = 50  # [EXPERIMENTAL VALUE] wait for 50 frames for oysters to settle down properly

IMU_RATE = 30
FRAME_RATE = 30
FRAME_SKIP = 3  # range scanner will run only on every 3rd frame

ACC_ERROR = accel_high_accuracy
GYRO_ERROR = gyro_high_accuracy

# sets random vibration to accel with RMS for x/y/z axis - 1/2/3 m/s^2, can be zero or changed to other values
ACC_ENV = '[0.03 0.001 0.01]-random'
ACC_VIB = vib_from_env(ACC_ENV, IMU_RATE)


# sets sinusoidal vibration to gyro with frequency being 0.5 Hz and amp for x/y/z axis being 6/5/4 deg/s
GYRO_ENV = '[6 5 4]d-0.5Hz-sinusoidal'
GYRO_VIB = vib_from_env(GYRO_ENV, IMU_RATE)


def start_pipeline(floor_noise,landscape_texture_dir,bluerov_path,bluerov_location,oysters_model_dir,oysters_texture_dir,\
             n_clusters, min_oyster, max_oyster,out_dir, save_imu=False, save_scanner=False):
    
    # if output dir not present, make one
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # if render output dir not present, make one
    render_out_dir = os.path.join(out_dir, "render_output")
    if not os.path.exists(render_out_dir):
        os.makedirs(render_out_dir)
    
    # if front camera render output dir not present, make one
    front_cam_dir = os.path.join(render_out_dir, "front_cam")
    if not os.path.exists(front_cam_dir):
        os.makedirs(front_cam_dir)
        
    # if third person camera render output dir not present, make one
    third_cam_dir = os.path.join(render_out_dir, "third_cam")
    if not os.path.exists(third_cam_dir):
        os.makedirs(third_cam_dir)
    
    # if bottom facing camera render output dir not present, make one
    bottom_cam_dir = os.path.join(render_out_dir, "bottom_cam")
    if not os.path.exists(bottom_cam_dir):
        os.makedirs(bottom_cam_dir)

    # if imu output dir not present, make one
    imu_dir = os.path.join(out_dir, "imu_dir")
    if not os.path.exists(imu_dir):
        os.makedirs(imu_dir)

    # if scanner output dir not present, make one
    scanner_dir = os.path.join(out_dir, "scanner_dir")
    if not os.path.exists(scanner_dir):
        os.makedirs(scanner_dir)
    
    # create a random lanscape everytime
    create_landscape(floor_noise,landscape_texture_dir)
    
    # import blueROV 3d model 
    front_cam, bottom_cam = add_bluerov(bluerov_path,bluerov_location)

    # bpy context object
    context = bpy.context

    # scanner object for the rotating LiDAR
    scanner_object = context.scene.objects[front_cam]
    
    # import oysters at some random location according to cluster size
    add_oyster(oysters_model_dir,oysters_texture_dir, n_clusters, min_oyster, max_oyster)

    # add third person view camera to the scene
    third_cam_x = 10
    third_cam_y = 10
    third_cam_z = 10
    third_cam_r = 0
    third_cam_p = 0
    third_cam_yaw = 0
    third_cam,_ = set_camera(third_cam_x, third_cam_y, third_cam_z, third_cam_r, third_cam_p, third_cam_yaw)
    
    # create variables to store values
    x_array     = []
    y_array     = []
    z_array     = []
    roll_array  = []
    pitch_array = []
    yaw_array   = []
    simulated_accel = None
    simulated_gyro = None

    x_coordinates = None
    y_coordinates = None
    z_coordinates = None
    distances     = None
    intensities   = None

    for frame_count in range(END_FRAME):
        context.scene.frame_set(frame_count)

        if frame_count >= TIME_TO_WAIT:  # assuming all objects settle down

            x,y,z,rot_x,rot_y,rot_z=get_position('BlueROV')
            x_array.append(x)
            y_array.append(y)
            z_array.append(z)
            roll_array.append(rot_x)
            pitch_array.append(rot_y)
            yaw_array.append(rot_z)
            
            if frame_count > 3:
                true_accel  = cal_linear_acc(x_array, y_array, z_array, IMU_RATE, FRAME_RATE)
                true_gyro  = cal_angular_vel(roll_array, pitch_array, yaw_array, IMU_RATE, FRAME_RATE)

                simulated_accel = acc_gen(IMU_RATE, true_accel, ACC_ERROR, ACC_VIB)
                simulated_gyro = gyro_gen(IMU_RATE, true_gyro, GYRO_ERROR, GYRO_VIB)

                x_array.pop(0)
                y_array.pop(0)
                z_array.pop(0)
                roll_array.pop(0)
                pitch_array.pop(0)
                yaw_array.pop(0)

                # save the simulated values in a text file
                # if save_imu:
                #   save_values(imu_dir, simulated_accel, simulated_gyro)

            # plot simulated accelerometer and simulated gyro for each point of time

            
            if frame_count % FRAME_SKIP == 0:
                scan_values = run_scanner(context, scanner_object)
                mappedData = np.array(list(map(lambda hit: tupleToArray(hit), scan_values))).transpose()
                
                x_coordinates = mappedData[2]
                y_coordinates = mappedData[3]
                z_coordinates = mappedData[4]
                distances     = mappedData[5]
                # intensities   = mappedData[6]

                # save the values in a text file 
                # if save_scanner:
                #   save_values(scanner_dir, x_coordinates, y_coordinates, z_coordinates, distances)

            # plot the coordinates, distances and intensities for each point of time
            

            render_img(bottom_cam_dir, frame_count, bottom_cam)
            render_img(front_cam_dir, frame_count, front_cam)
            render_img(third_cam_dir, frame_count, third_cam)

            # [OPTIONAL] - display the image continously with opencv
            # [OPTIONAL] - run yolo-oyster detection on the rendered img


    
if __name__=="__main__":
    
    # register range_scanner module
    range_scanner.register()

    # absolute path of the script
    script_path = os.path.dirname(os.path.abspath(__file__))

    # remove the last dir from path so that we are in base directory and can navigate further
    base_dir_path = script_path.split('code')[0]

    try:
        # delete all previously created objects from the scene
        delete_objs()
        
        # landscape parameters
        floor_noise=3.5
        landscape_texture_dir = base_dir_path + "//data//blender_data//landscape//textures//"
        
        # blueRov parameters
        bluerov_model_path = base_dir_path + "//data//blender_data//blueROV//BlueRov2.dae"
        bluerov_location=(10,0,10)
        
        # oysters paramteres
        oysters_model_dir = base_dir_path + "//data//blender_data//oysters//model//"
        oysters_texture_dir = base_dir_path + "//data//blender_data//oysters//textures//"
        n_clusters=1
        min_oyster=5
        max_oyster=None
    
        # dir where all the results will be saved
        out_dir = base_dir_path + "//data//output//"
        
        start_pipeline(floor_noise,landscape_texture_dir, \
            bluerov_model_path,bluerov_location,oysters_model_dir, \
                oysters_texture_dir, n_clusters, min_oyster, \
                    max_oyster,out_dir)


    except Exception as e:
        print(e)

    # unregister range_scanner module
    range_scanner.unregister()
