import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math

##	This function calculate the cost to 8 neighbors
#@	link is the 8 neighours pixel value
Max_D_link = 0
def D_link(link):
	global Max_D_link
	#print(link)
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
	#print(d_link)
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


def get_cost_mat(img):
	global Max_D_link
	Max_D_link = 0
	##	Adding boarder to the image for the convinient of link calculation
	##	shape of img will be increae to (width+2,height+2), 0 is black, 255 is white
	larger_img= cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT,value=128)
	height, width  =larger_img.shape
	#print(img.shape,"vs",larger_img.shape)
	cost_mat = []
	links = [0]*8
	#if shape is 10*8, range() return (0..9)*(0..7)
	#if larger_img has shape 10*8, then just (1..8)*(1..6) are needed 
	'''for i in range(0,3):
		for j in range(0,10):
			print(img[i][j])'''

	for i in range(1,height-1):
		cost_mat_row = []
		for j in range(1,width-1):
			#print('(',i,',',j,')',end='')
			links[0] = int(larger_img[i+1,j])
			links[1] = int(larger_img[i+1,j-1])
			links[2] = int(larger_img[i,j-1])
			links[3] = int(larger_img[i-1,j-1])
			links[4] = int(larger_img[i-1,j])
			links[5] = int(larger_img[i-1,j+1])
			links[6] = int(larger_img[i,j+1])
			links[7] = int(larger_img[i+1,j+1])
			cost_mat_row.append(D_link(links))

		cost_mat.append(cost_mat_row)
	'''for i in range(100,105):
		for j in range(100,105):
			print(cost_mat[i][j])'''

	#print("Max_D_link: ",Max_D_link)
	for i in range(height-2):
		for j in range(width-2):
			cost_mat[i][j] = link_cost(cost_mat[i][j])
			#print(cost_mat[i][j],end='')

	return Max_D_link, cost_mat

def get_rgb_cost_mat(img):
	height, width, depth  = img.shape
 
	#blur = cv2.GaussianBlur(img,(5,5),0)
	#blur = cv2.blur(img,(5,5))
	blur = cv2.medianBlur(img,5)

	b,g,r = cv2.split(img)
	'''print(img[0,0])
	print(b[0,0],g[0,0],r[0,0])
	plt.subplot(131),plt.imshow(r,'gray'),plt.title('r')
	plt.subplot(132),plt.imshow(g,'gray'),plt.title('g')
	plt.subplot(133),plt.imshow(b,'gray'),plt.title('b')
	plt.show()
	exit()
	'''
	b_max_D_link, b_cost_mat = get_cost_mat(b)
	g_max_D_link, g_cost_mat = get_cost_mat(g)
	r_max_D_link, r_cost_mat = get_cost_mat(r)
	Max_D_link = max(b_max_D_link,g_max_D_link,r_max_D_link)
	cost_mat = []
	for i in range(height): 
		cost_mat_row = []
		for j in range(width):
			DB=np.square( b_cost_mat[i][j])
			DG=np.square( g_cost_mat[i][j])
			DR=np.square( r_cost_mat[i][j])
			D_link = np.sqrt((DB+DG+DR)/3.0)
			cost_mat_row.append(link_cost(D_link.tolist()))
		cost_mat.append(cost_mat_row)
	'''for i in range(height):
		for j in range(width):
			print(cost_mat[i][j])'''
	return cost_mat