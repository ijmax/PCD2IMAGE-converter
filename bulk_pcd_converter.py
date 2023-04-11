#############################################################
#
# Author: Isuru Jayarathne
# Date: 10/04/2023
# Usage: Convert bulk of PCD files as a JPG image
# Terminal command: python bulk_pcd_converter.py <path_to_folder> <path_to_target_folder>      
#
#############################################################

import open3d as o3d
import numpy as np
import cv2
import sys
import os

def convert2img(pcd_path, folder_path, target_folder="./", x_pixels=500):
	pcd_x = 0
	pcd_y = 1
	
	pcd = o3d.io.read_point_cloud(folder_path + "/" + pcd_path)
	point_array = np.asarray(pcd.points)

	max_x = np.max(point_array[:,pcd_x])
	max_y = np.max(point_array[:,pcd_y])
	min_x = np.min(point_array[:,pcd_x])
	min_y = np.min(point_array[:,pcd_y])

	x_range = max_x - min_x
	y_range = max_y - min_y

	y_pixels = int(x_pixels*(y_range/x_range))

	img_array = np.ones(shape=(x_pixels, y_pixels)) * 255

	for val in point_array[:,0:3]:
		x = int(((val[pcd_x]-min_x)/x_range)*x_pixels)
		y = int(((val[pcd_y]-min_y)/y_range)*y_pixels)
		if (x < x_pixels and y < y_pixels):
			img_array[x, y] = 0

	cv2.imwrite(target_folder + pcd_path.split(".")[0] + ".jpg", img_array)


if __name__ == "__main__":
	path = sys.argv[1]
	target_folder = sys.argv[2]
	files = os.listdir(path) 
	x_pixels = 500
	
	for f in files:
		convert2img(f, path, target_folder=target_folder, x_pixels=x_pixels)
	
