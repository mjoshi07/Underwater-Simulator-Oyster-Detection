import bpy
import numpy as np
import random
import os
import time

import sys
path=r"..//code//"

if path not in sys.path:
    sys.path.append(path)

from CreateScene import delete_objs, create_landscape, add_bluerov, add_oyster
from Utils import get_position, render_img
from ImuUtils import  cal_linear_acc, cal_angular_vel, acc_gen, gyro_gen, accel_high_accuracy, gyro_high_accuracy, vib_from_env
from RangeScanner import run_scanner, tupleToArray
import range_scanner


START_FRAME = 1
END_FRAME = 400

SURFACE_SIZE = 10

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
             n_clusters, min_oyster, max_oyster,render_out_dir):
    
    # Create a random lanscape everytime
    create_landscape(floor_noise,landscape_texture_dir)
    
    # import blueROV 3d model 
    front_cam, down_cam = add_bluerov(bluerov_path,bluerov_location)

    # bpy context object
    context = bpy.context

    # scanner object for the rotating LiDAR
    scanner_object = context.scene.objects[front_cam]
    
    # import oysters at some random location according to cluster size
    add_oyster(oysters_model_dir,oysters_texture_dir, n_clusters, min_oyster, max_oyster)
    
    # TODO: Play the animation
    
    # Time delay for oysters drop
#   time.sleep(10)

    frame_skip = FRAME_SKIP
    
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
        
        frame_count += 1

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

        # plot simulated accelerometer and simulated gyro for each point of time

        
        if frame_count % frame_skip == 0:
            scan_values = run_scanner(context, scanner_object)
            mappedData = np.array(list(map(lambda hit: tupleToArray(hit), scan_values))).transpose()
            
            x_coordinates = mappedData[2]
            y_coordinates = mappedData[3]
            z_coordinates = mappedData[4]
            distances     = mappedData[5]
            intensities   = mappedData[6]

        # plot the coordinates, distances and intensities for each point of time
        

        img = render_img(render_out_dir, frame_count, down_cam)

        # [OPTIONAL] - display the image continously with opencv
        # [OPTIONAL] - run yolo-oyster detection on the rendered img


    
if __name__=="__main__":
    
    # register range_scanner module
    range_scanner.register()

    try:
        # delete all previously created objects from the scene
        delete_objs()
        
        # landscape parameters
        floor_noise=3.5
        landscape_texture_dir = r"..//data//blender_data//landscape//textures//"
        
        # blueRov parameters
        bluerov_model_path = r"..//data//blender_data//blueROV//BlueRov2.dae"
        bluerov_location=(10,0,10)
        
        # oysters paramteres
        oysters_model_dir = r"..//data//blender_data//oysters//model//"
        oysters_texture_dir = r"..//data//blender_data//oysters//textures//"
        n_clusters=1
        min_oyster=5
        max_oyster=None
        

        render_out_dir="..//data//blender_data//render_output//"
        
        start_pipeline(floor_noise,landscape_texture_dir, \
            bluerov_model_path,bluerov_location,oysters_model_dir, \
                oysters_texture_dir, n_clusters, min_oyster, \
                    max_oyster,render_out_dir)


    except Exception as e:
        print(e)

    # unregister range_scanner module
    range_scanner.unregister()
