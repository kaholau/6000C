import sys
import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math 
import cost
from PyQt5.QtWidgets import QLabel


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


class Image(QLabel):
	def __init__(self,fileName):
		super(Image, self).__init__()	
		self.fileName = fileName
		self.min_path=[]
		return

	def start(self):

		img = cv2.imread(self.fileName,cv2.IMREAD_COLOR)

		#edges = cv2.Canny(img,100,200)
		#aplacian = cv2.Laplacian(img,cv2.CV_64F)

		mat = self.create_node(img)
		print('nodes created')
		#cv2.imshow('image',img)
		#cv2.waitKey()
		#cv2.destroyAllWindows()
		return

	def create_node(self,img):
		height, width, depth  = img.shape
		print (height, width, depth)
		cost_mat = cost.get_rgb_cost_mat(img)
		Node_mat = []
		for i in range(height):
			node_mat_row = []
			for j in range(width):
				node = Node(i,j,cost_mat[i][j])
				node_mat_row.append(node)
			cost_mat.append(node_mat_row)
	
		return Node_mat

	def mousePressCallback(self,x,y):

		print('Image Press At',x,y)
		self.min_path.append([x,y])
		#return array of contour point for drawing the line
		return self.min_path 

	def mouseMoveCallback(self,x,y):
		print('Move Move To',x,y)
		min_path=[]
		return min_path 

	def undo(self):

		return
