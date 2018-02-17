import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math

##	This function calculate the cost to 8 neighbors
#@	link is the 8 neighours pixel value
Max_D_link = 0
def D_link(link):
	global Max_D_link
	d_link = [0]*8
	for i in range(len(link)):
		if i%2==0:	#even index
			if i == 6:
				d_link[i] = abs((link[i-1]+link[i-2])/2-(link[i+1]+link[0])/2)/2	
			else:
				d_link[i] = abs((link[i-1]+link[i-2])/2-(link[i+1]+link[i+2])/2)/2
		else:
			if i == 7 :
				d_link[i] = abs(link[i-1]+link[0])/math.sqrt(2)
			else:
				d_link[i] = abs(link[i-1]+link[i+1])/math.sqrt(2)
	Max_D_link = max(d_link) if max(d_link)>Max_D_link else Max_D_link
	return d_link

##	Calculate the cost using Max_D_link 
#@	d_links  is the list of links to 8 neighbors 
def link_cost(d_links):
	#print(d_links)
	for i,d in enumerate(d_links):
		if i%2==0:
			d = (Max_D_link-d)*1
		else:
			d = (Max_D_link-d)*math.sqrt(2)
	#print(d_links,"\n")
	
	return d_links

##	Adding boarder to the image for the convinient of link calculation
##	shape of img will be increae to (width+2,height+2), 0 is black, 255 is white
#@  img is the original image
def add_egde_pixel(img):
	h,w = img.shape
	new_img = np.full((h+2,w+2),0,dtype=np.uint8)
	for i in range(h):
		for j in range(w):
			new_img[i+1,j+1]= img[i][j]
			#print(new_img[i,j])
	return new_img

def invert_pixel_value(img):
	h,w = img.shape
	inverted_img = np.zeros((h,w))
	for i in range(h):
		for j in range(w):
			if img[i,j]==0:
				inverted_img[i][j]=255
			else:
				inverted_img[i][j]=1

	return inverted_img

def get_cost_mat(img):
	larger_img = add_egde_pixel(invert_pixel_value(img))
	height, width  =larger_img.shape
	#print(img.shape,"vs",larger_img.shape)
	cost_mat = []
	links = [0]*8
	#if shape is 10*8, range() return (0..9)*(0..7)
	#if larger_img has shape 10*8, then just (1..8)*(1..6) are needed 
	for i in range(1,height-1):
		cost_mat_row = []
		for j in range(1,width-1):
			#print('(',i,',',j,')',end='')
			links[0] = larger_img[i+1,j]
			links[1] = larger_img[i+1,j-1]
			links[2] = larger_img[i,j-1]
			links[3] = larger_img[i-1,j-1]
			links[4] = larger_img[i-1,j]
			links[5] = larger_img[i-1,j+1]
			links[6] = larger_img[i,j+1]
			links[7] = larger_img[i+1,j+1]
			cost_mat_row.append(D_link(links))
		cost_mat.append(cost_mat_row)
	print("Max_D_link: ",Max_D_link)
	for i in range(height-2):
		for j in range(width-2):
			cost_mat[i][j] = link_cost(cost_mat[i][j])
			#print(cost_mat[i][j],end='')
	return cost_mat

