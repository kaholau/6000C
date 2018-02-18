import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math 
import cost
import UI


class Node:
	def __init__(self,x,y,links):
		self.linkCost = links
		self.state ='INITIAL' #INITIAL, ACTIVE, EXPANDED 
		self.totalCost = math.inf #the minimum total cost from this node to the seed node.  
		self.prevNode = None #points to its predecessor along the minimum cost path from the seed to that node. 
		self.row = x
		self.column = y
		return
	def __repr__(self):
		return x,y

def randomMat(min,max,h,w):
	return np.random.randint(min,max,(h,w))


def create_node(img):
	height, width, depth  = img.shape
	cost_mat = cost.get_rgb_cost_mat(img)
	Node_mat = []
	for i in range(height):
		node_mat_row = []
		for j in range(width):
			node = Node(i,j,cost_mat[i][j])
			node_mat_row.append(node)
		cost_mat.append(node_mat_row)
	
	return Node_mat


path = 'ferry.bmp'
img = cv2.imread(path,cv2.IMREAD_COLOR)




#edges = cv2.Canny(img,100,200)
#aplacian = cv2.Laplacian(img,cv2.CV_64F)

mat = create_node(img)

cv2.imshow('image',img)
cv2.waitKey()
cv2.destroyAllWindows()
'''
plt.imshow(img)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()'''

