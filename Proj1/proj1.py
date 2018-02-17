import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math 
import cost


class Node:
	def __init__(self,x,y,links):
		self.linkCost = links
		self.state = 0
		self.totalCost = 0 #the minimum total cost from this node to the seed node.  
		self.prevNode = None #points to its predecessor along the minimum cost path from the seed to that node. 
		self.row = x
		self.column = y
		return
	def __repr__(self):
		return x,y

def randomMat(min,max,h,w):
	return np.random.randint(min,max,(h,w))


def create_node(img):
	height, width  = img.shape
	#print(img.shape,"vs",larger_img.shape)
	import cost
	cost_mat = cost.get_cost_mat(img)
	Node_mat = []
	for i in range(height):
		node_mat_row = []
		for j in range(width):
			node = Node(i,j,cost_mat[i][j])
			node_mat_row.append(node)
		cost_mat.append(node_mat_row)

	return Node_mat


path = 'ferry.bmp'
print(dir(cost))
img = cv2.imread(path,0)
print(img.shape)
edges = cv2.Canny(img,100,200)
#aplacian = cv2.Laplacian(img,cv2.CV_64F)

mat = create_node(edges)

print(img.shape)

plt.imshow(edges, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
