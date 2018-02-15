import cv2 
import numpy as np
from matplotlib import pyplot as plt


def randomMat(min,max,h,w):

	return np.random.randint(min,max,(h,w))

##This function calculate the cost to 8 neighbour
#* link is the 8 neighours
def cost_func(link):
	cost = [0]*8
	for i in link:
		if i%2==0:	#even index
			cost[i] = cost[i-1]+cost[i-2]

	return

def create_node(img):
	height, width  =img.shape
	cost_mat = np.zero((height,width))
	links = [0]*8
	for i in range(1,height):
		for j in range(1,width):
			links[0] = img[i+1,j]
			links[1] = img[i+1,j-1]
			links[2] = img[i,j-1]
			links[3] = img[i-1,j-1]
			links[4] = img[i-1,j]
			links[5] = img[i-1,j+1]
			links[6] = img[i,j+1]
			links[7] = img[i+1,j+1]

			cost_mat[i,j] = create_node()

	return cost_mat
#run under python3
class Node:

	def __init__(self):
		linkCost = []
		state = 0;
		totalCost = 0
		prevNode = Node()
		column = 0
		row = 0
		return

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
