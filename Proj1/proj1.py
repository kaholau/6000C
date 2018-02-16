import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math 
class Node:

	def __init__(self,links):
		self.linkCost = links
		self.state = 0
		self.totalCost = 0
		#self.prevNode = Node()
		self.column = 0
		self.row = 0
		return

def randomMat(min,max,h,w):
	return np.random.randint(min,max,(h,w))

##This function calculate the cost to 8 neighbours
#* link is the 8 neighours
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
def link_cost(d_links):
	print(d_links)
	for i,d in enumerate(d_links):
		if i%2==0:
			d = (Max_D_link-d)*1
		else:
			d = (Max_D_link-d)*math.sqrt(2)
	print(d_links,"\n")
	
	return d_links

def create_node(img):
	height, width  =img.shape
	cost_mat = []
	links = [0]*8
	for i in range(1,height-1):
		cost_mat_row = []
		for j in range(1,width-1):
			links[0] = img[i+1,j]
			links[1] = img[i+1,j-1]
			links[2] = img[i,j-1]
			links[3] = img[i-1,j-1]
			links[4] = img[i-1,j]
			links[5] = img[i-1,j+1]
			links[6] = img[i,j+1]
			links[7] = img[i+1,j+1]
			cost_mat_row.append(Node(D_link(links)))
		cost_mat.append(cost_mat_row)
	print("Max_D_link: ",Max_D_link)
	for i in range(1,height-1):
		for j in range(1,width-1):
			cost_mat[i][j].linkCost = link_cost(cost_mat[i][j].linkCost)
	
	return cost_mat


path = 'ferry.bmp'

img = cv2.imread(path,0)
print(img.shape)
edges = cv2.Canny(img,100,200)

#aplacian = cv2.Laplacian(img,cv2.CV_64F)
#cost_mat = create_node(edges)

print(img.shape)

plt.imshow(edges, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
