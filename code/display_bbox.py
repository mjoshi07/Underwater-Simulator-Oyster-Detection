import cv2
import os

def draw_bbox(yolo_data_path):
	if not os.path.exists(yolo_data_path):
		print("PATH DOES NOT EXIST")
		return
	else:
		for root, dirs, files in os.walk(data_path):
			for file in files:
				if file.split('.')[1] == 'txt':
					txt_file = file
					img_file = file.split('.')[0] + '.png'
					if not os.path.exists(img_file):
						img_file = file.split('.')[0] + '.jpg'

					img = cv2.imread(os.path.join(root, img_file))
					img_h, img_w = img.shape[:2]

					with open(os.path.join(root, txt_file), 'r') as f:
						for line in f.readlines():
							x_center = float(line.split(" ")[1])*img_w
							y_center = float(line.split(" ")[2])*img_h
							w = float(line.split(" ")[3])*img_w
							h = float(line.split(" ")[4])*img_h

							x = int(x_center - w/2)
							y = int(y_center - h/2)
							w = int(w)
							h = int(h)
							
							cv2.rectangle(img, (x,y, w, h), (255, 120, 0), 2)

							cv2.imshow('img', img)
							c = cv2.waitKey()
							if c == ord('q'):
								EXIT

if __name__ == "__main__":
	# path to yolo format data
	data_path = "../data/sample_yolo_data/"

	# draws bbox on the images by reading annotation txt files
	draw_bbox(data_path)
