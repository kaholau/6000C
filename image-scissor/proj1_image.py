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
		self.temp_min_path = []
		self.node_mat = []
		self.iScissorReady = False
		return

	def start(self):
		print("waiting for initialization....")
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
			Node_mat.append(node_mat_row)
		
		return Node_mat


	def mouseReleaseCallback(self,x,y):
		self.iScissorReady = False
		print('Image Press At',x,y)
		self.min_path +=self.temp_min_path
		#index of point drawn on image is the revert of matrix index
		self.min_path.append([y,x])
		self.temp_min_path = []
		'''print("Update min_path:")
		for n in self.min_path:
			print(n,end=',')'''
		min_cost_path.reset_node_matrix(self.node_mat)
		min_cost_path.compute_min_cost_path(x, y, self.node_mat)
		#return array of contour point for drawing the line
		self.iScissorReady = True
		return self.min_path 

	def mouseMoveCallback(self,x,y):
		self.iScissorReady = False
		print('Image Move To',x,y)
		#node_list contain all points from last seed to [x,y], 
		node_list = min_cost_path.get_min_path_from_seed(x, y, self.node_mat)
		#print(len(node_list))
		self.temp_min_path = []
		for n in reversed(node_list):
			self.temp_min_path.append([n.get_column_index(),n.get_row_index()])
		'''print("Moving min_path:")
		for n in self.temp_min_path:
			print(n,end=',')'''
		self.iScissorReady = True
		return self.min_path+self.temp_min_path

	def undo(self):

		return
