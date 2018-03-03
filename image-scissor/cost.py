import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math

##	This function calculate the cost to 8 neighbors
#@	pixels is the 8 neighours pixel value
Max_D_link = 0
def D_link(pixels):
	global Max_D_link
	#print(link)
	d_link = [0]*8
	for i in range(len(pixels)):
		if i%2==0:	#even index
			if i == 6:
				d_link[i] = abs((pixels[i-1]+pixels[i-2])/2-(pixels[i+1]+pixels[0])/2)/2	
			else:
				d_link[i] = abs((pixels[i-1]+pixels[i-2])/2-(pixels[i+1]+pixels[i+2])/2)/2
		else:
			if i == 7 :
				d_link[i] = abs(pixels[i-1]-pixels[0])/math.sqrt(2)
			else:
				d_link[i] = abs(pixels[i-1]-pixels[i+1])/math.sqrt(2)
	#print(d_link)
	Max_D_link = max(d_link) if max(d_link)>Max_D_link else Max_D_link

	return d_link

##	Calculate the cost using Max_D_link 
#@	d_links  is the list of links to 8 neighbors 
def link_cost(d_links):
	#print(d_links)
	for i,d in enumerate(d_links):
		#print(i,d)
		if i%2==0:
			d_links[i] = (Max_D_link-d)*1
		else:
			d_links[i] = (Max_D_link-d)*math.sqrt(2)
		#print(i,d)
	#print(d_links,"\n")
	#input("Press Enter to continue...")
	return d_links


def get_dlink_mat(img):
	global Max_D_link
	Max_D_link = 0
	##	Adding boarder to the image for the convinient of link calculation
	##	shape of img will be increae to (width+2,height+2), 0 is black, 255 is white
	bordered_img= cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT,value=128)
	if len(bordered_img.shape) > 2:
		height, width, depth  =bordered_img.shape
	else:
		height, width  =bordered_img.shape
	#print(img.shape,"vs",bordered_img.shape)
	dlink_mat = []
	pixels = [0]*8
	#if shape is 10*8, range() return (0..9)*(0..7)
	#if bordered_img has shape 10*8, then just (1..8)*(1..6) are needed 
	for i in range(1,height-1):
		dlink_mat_row = []
		for j in range(1,width-1):
			pixels[0] = int(bordered_img[i+1,j])
			pixels[1] = int(bordered_img[i+1,j-1])
			pixels[2] = int(bordered_img[i,j-1])
			pixels[3] = int(bordered_img[i-1,j-1])
			pixels[4] = int(bordered_img[i-1,j])
			pixels[5] = int(bordered_img[i-1,j+1])
			pixels[6] = int(bordered_img[i,j+1])
			pixels[7] = int(bordered_img[i+1,j+1])
			dlink_mat_row.append(D_link(pixels))

		dlink_mat.append(dlink_mat_row)

	#print("Max_D_link: ",Max_D_link)
	'''for i in range(height-2):
		for j in range(width-2):
			dlink_mat[i][j] = link_cost(dlink_mat[i][j])
			#print(dlink_mat[i][j],end='')'''

	return Max_D_link, dlink_mat

def get_rgb_cost_mat(img):
	height, width, depth  = img.shape
 
	#blur = cv2.GaussianBlur(img,(5,5),0)
	#blur = cv2.blur(img,(5,5))
	blur = cv2.medianBlur(img,5)

	b,g,r = cv2.split(blur)
	'''print(img[0,0])
	print(b[0,0],g[0,0],r[0,0])
	plt.subplot(131),plt.imshow(r,'gray'),plt.title('r')
	plt.subplot(132),plt.imshow(g,'gray'),plt.title('g')
	plt.subplot(133),plt.imshow(b,'gray'),plt.title('b')
	plt.show()
	exit()
	'''
	b_max_D_link, b_dlink_mat = get_dlink_mat(b)
	g_max_D_link, g_dlink_mat = get_dlink_mat(g)
	r_max_D_link, r_dlink_mat = get_dlink_mat(r)
	Max_D_link = max(b_max_D_link,g_max_D_link,r_max_D_link)
	cost_mat = []
	for i in range(height): 
		cost_mat_row = []
		for j in range(width):
			DB=np.square( b_dlink_mat[i][j])
			DG=np.square( g_dlink_mat[i][j])
			DR=np.square( r_dlink_mat[i][j])
			D_link = np.sqrt((DB+DG+DR)/3.0)
			cost_mat_row.append(link_cost(D_link.tolist()))
		cost_mat.append(cost_mat_row)
	'''for i in range(height):
		for j in range(width):
			print(cost_mat[i][j])'''
	return Max_D_link,cost_mat