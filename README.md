# Underwater-Robotics
Development of an underwater simulator which will be used for oysters detection for the [project](https://isr.umd.edu/news/story/using-underwater-robots-to-detect-and-count-oysters). Simulator can generate random underwater landscape, randomize oysters location and oysters count and much more.
Using a range scanner installed on BlueROV for navigation.

## Preview of underwater scene
![image](https://github.com/mjoshi07/Underwater-Robotics/blob/main/data/render3.png)

## Tasks
- [x] 2D bounding Box of objects from Blender `2.93`
- [x] Integrate IMU with blender
- [x] Integrate LiDAR/SONAR with blender
- [x] Train yolo on the generated data from blender
- [x] Train UNet for semantic segmentation task 
- [ ] Train GAN to get realistic underwater images from renderd images
- [ ] Train  multi-task learning network to predict segmentation, 3D depth estimation, and realistic underwater images in a single forward pass


## Google Colab Notebook
* colab notebook used to train the yolov4-tiny, find it [here](https://colab.research.google.com/drive/1RePfSTb7c1tPAuh_D-ySLhrG78gxkF9D?usp=sharing)
* Modified the colab notebook provided [here](https://colab.research.google.com/drive/1_GdoqCJWXsChrOiY8sZMr_zbr_fH-0Fg)

## Models
* We trained a yoloV4-tiny on a dataset of around 5000 images
* Download the model best weights file from [here](https://drive.google.com/file/d/1ffx9uFeBLUgfymSTHV5pO_OoLnYB7EVT/view?usp=sharing) 
* Copy the model weights in [here](https://github.com/mjoshi07/Underwater-Robotics/tree/main/data/model)

## Blender model
* BlueROV model downlaod from [here](https://github.com/patrickelectric/bluerov_ros_playground)
* Oysters model download from [here](https://drive.google.com/drive/folders/1XY2yMnFDCiSR8H6S84OS8WX1tzu2OnCW?usp=sharing)  
