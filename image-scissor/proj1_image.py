import cv2 
import cost
import node
import min_cost_path
from PyQt5.QtWidgets import QLabel


class Image(QLabel):
	def __init__(self,fileName):
		super(Image, self).__init__()	
		self.fileName = fileName
		self.min_path = []
		self.node_mat = []
		self.iScissorReady = False
		return

	def start(self):

		img = cv2.imread(self.fileName,cv2.IMREAD_COLOR)

		#edges = cv2.Canny(img,100,200)
		#aplacian = cv2.Laplacian(img,cv2.CV_64F)

		self.node_mat = self.create_nodes(img)
		print('nodes created')
		#cv2.imshow('image',img)
		#cv2.waitKey()
		#cv2.destroyAllWindows()

		self.iScissorReady = True
		return

	def getiScissorReady(self):
		return self.iScissorReady

	def create_nodes(self,img):
		height, width, depth  = img.shape
		#print ('Dimension: ',height, width, depth)
		cost_mat = cost.get_rgb_cost_mat(img)
		Node_mat = []
		for i in range(height):
			node_mat_row = []
			for j in range(width):
				n = node.Node(i,j,cost_mat[i][j])
				node_mat_row.append(n)
			cost_mat.append(node_mat_row)
		
		return Node_mat


	def mousePressCallback(self,x,y):

		print('Image Press At',x,y)
		self.min_path.append([x,y])
		min_cost_path.compute_min_cost_path(x,y, self.node_mat)
		#return array of contour point for drawing the line
		return self.min_path 

	def mouseMoveCallback(self,x,y):
		print('Move Move To',x,y)
		self.min_path.append([x,y])
		return self.min_path 

	def undo(self):

		return
