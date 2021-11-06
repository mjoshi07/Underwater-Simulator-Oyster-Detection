import bpy
import time
import csv

            
def record_data():
    counter=0
    with open('imu_data_test.csv','w') as file:
        csvwriter=csv.writer(file)
#        while True:
#                      Keyframes/(fps*sleep)
        while counter<100:
#            try:
                
                # Mention which object to track
                obj=bpy.context.scene.objects['BlueRov']
                x=obj.location.x
                y=obj.location.y
                z=obj.location.z
                
                # Specify rotation rep
                rot_z=obj.rotation_euler.z
                rot_y=obj.rotation_euler.y
                rot_x=obj.rotation_euler.x
                
                row=[counter,x,y,z,rot_x,rot_y,rot_z]
                csvwriter.writerow(row)
                # Time delay b/w steps in s
                time.sleep(0.1)
                counter+=1
#            except (KeyboardInterrupt):
#                break
            

if __name__=="__main__":
    record_data()
#    bpy.ops.screen.animation_play()