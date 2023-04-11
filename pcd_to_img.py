#############################################################
#
# Author: Isuru Jayarathne
# Date: 10/04/2023
# Usage: Convert PCD file as a JPG image
# Terminal command: python pcd_to_img.py <path_to_PCD_file>       
#
#############################################################

import open3d as o3d
import numpy as np
import cv2
import sys

def covert2img(file_path, x_pixels):
	
	# define x, y axes of the given PCD
	pcd_x = 0
	pcd_y = 1
	
	# open point cloud file
	pcd = o3d.io.read_point_cloud(file_path)
	# extract x,y,z (point data) from PCD file as a 3D array
	point_array = np.asarray(pcd.points)
	
	# get max and min of x and y axes
	max_x = np.max(point_array[:,pcd_x])
	max_y = np.max(point_array[:,pcd_y])
	min_x = np.min(point_array[:,pcd_x])
	min_y = np.min(point_array[:,pcd_y])
	
	# calculate ranges from x,y data points
	x_range = max_x - min_x
	y_range = max_y - min_y
	
	# calculate number of pixels for y axis for the image
	y_pixels = int(x_pixels*(y_range/x_range))
	
	# create 2D array with calculated number of pixel for x and y axes
	img_array = np.ones(shape=(x_pixels, y_pixels)) * 255

	# loop through all points in the PCD
	for val in point_array[:,0:3]:
		# calculate x index using x value and x range
		x = int(((val[pcd_x]-min_x)/x_range)*x_pixels)
		# calculate y index using y value and y range
		y = int(((val[pcd_y]-min_y)/y_range)*y_pixels)
		
		if (x < x_pixels and y < y_pixels):
			# set pixel values to 0 for the given indices
			img_array[x, y] = 0
	
	# save 2D array as an image 
	cv2.imwrite("image_from_pcd.jpg", img_array)


if __name__ == "__main__":
	# get file path from terminal argument
	file_path = sys.argv[1]
	# set number of pixels for x axis
	x_pixels = 1000
	# call for the convert function
	covert2img(file_path, x_pixels)
