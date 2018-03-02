import cv2 
import cost
import node
import min_cost_path
from PyQt5.QtWidgets import QLabel
import numpy as np

class Image(QLabel):
	def __init__(self,fileName):
		super(Image, self).__init__()	
		self.fileName = fileName
		self.min_path = []
		self.temp_min_path = []
		self.last_min_path_len = []
		self.node_mat = []
		self.height = 0
		self.width = 0 
		self.depth = 0
		self.maxCost = 0
		self.iScissorReady = False
		self.first_seed_coord = None
		self.seeds = []
		return

	def start(self):
		print("waiting for initialization....")
		img = cv2.imread(self.fileName,cv2.IMREAD_COLOR)

		self.node_mat = self.create_nodes(img)
		print('nodes created')
		graph = self.getCostGraph()

		#cv2.imshow('image',img)
		#cv2.waitKey()
		#cv2.destroyAllWindows()

		self.iScissorReady = True
		return	graph

	def getiScissorReady(self):
		return self.iScissorReady

	def create_nodes(self,img):
		height, width, depth  = img.shape
		self.height = height
		self.width = width
		self.depth = depth
		#print ('Dimension: ',height, width, depth)
		#edges = cv2.Canny(img,100,200)
		#aplacian = cv2.Laplacian(img,cv2.CV_64F)

		self.maxCost, cost_mat = cost.get_rgb_cost_mat(img)
		#self.maxCost, cost_mat = cost.get_cost_mat(img)
		Node_mat = []
		for i in range(height):
			node_mat_row = []
			for j in range(width):
				n = node.Node(i,j,img[i,j],cost_mat[i][j])
				node_mat_row.append(n)
			Node_mat.append(node_mat_row)
		
		return Node_mat


	def mouseReleaseCallback(self,x,y):
		self.iScissorReady = False
		print('Image Press At',x,y)
		if self.first_seed_coord == None:
		   self.first_seed_coord = [x,y]
		   self.min_path.append([y,x])
		   self.last_min_path_len.append(1)
		else:
			self.min_path +=self.temp_min_path		
			#temp_min_path contain previous seed, points among path and last seed
			self.last_min_path_len.append(len(self.temp_min_path))
		self.seeds.append([x,y])
		self.temp_min_path = []
		min_cost_path.reset_node_matrix(self.node_mat)
		min_cost_path.compute_min_cost_path(x, y, self.node_mat)
		#return array of contour point for drawing the line
		self.iScissorReady = True
		return self.min_path 

	def mouseMoveCallback(self,x,y):
		return self.get_entire_min_path(x,y)
	     
	def getClosedCoutour(self):
		#return min_path from last seed to the first seed
		if self.first_seed_coord == None:
		   return
		print('closed contour')
		return self.get_entire_min_path(self.first_seed_coord[0],self.first_seed_coord[1])

	def get_entire_min_path(self,x,y):
		return self.min_path+self.get_min_path_coordinates(x,y)
		
	def get_min_path_coordinates(self,x,y):
		self.iScissorReady = False
		node_list = min_cost_path.get_min_path_from_seed(x, y, self.node_mat)
		self.temp_min_path = self.convertNodeToPoints(node_list)
		self.iScissorReady = True
		return self.temp_min_path
    
	def convertNodeToPoints(self,nodes):
		temp_min_path = []
		#index of point drawn on image is the revert of matrix index
		for n in reversed(nodes):
			temp_min_path.append([n.get_column_index(),n.get_row_index()])
		return temp_min_path

	def getCostGraph(self):
		m = 3
		mh = self.height*m
		mw = self.width*m
		#print(self.height,self.width,'>>',mh,mw)
		graph = np.zeros((mh,mw,self.depth),np.uint8)
		row_cnt = 0
		col_cnt = 0
		maxC = self.maxCost
		#print('max cost link:',maxC)

		for i in range(1,mh,m):
			for j in range(1,mw,m):
				#print(i,j,row_cnt,col_cnt)
				node = self.node_mat[row_cnt][col_cnt]
				links = np.array([[l,0,0] for l in node.get_links_cost()])
				links = np.uint8(links/maxC*255)
				graph[i,j] = node.get_pixel()

				graph[i+1,j] 	= links[0]
				graph[i+1,j-1] 	= links[1]
				graph[i,j-1] 	= links[2]
				graph[i-1,j-1] 	= links[3]
				graph[i-1,j] 	= links[4]
				graph[i-1,j+1] 	= links[5]
				graph[i,j+1] 	= links[6]
				graph[i+1,j+1] 	= links[7] 

				#print(graph[i,j],end='')
				col_cnt+=1
			col_cnt=0
			row_cnt+=1


		#cv2.imshow('Cost Graph',graph)

		return graph


	def undo(self):

		#TODO remove the min_path generated by last seed
		if len(self.min_path) ==1:
			self.min_path = []
			self.seeds.pop(-1)
			self.first_seed_coord = None
			min_cost_path.reset_node_matrix(self.node_mat)
		elif len(self.min_path)>1:
			self.min_path = self.min_path[:-self.last_min_path_len.pop(-1)]
			self.seeds.pop(-1)
			min_cost_path.reset_node_matrix(self.node_mat)
			min_cost_path.compute_min_cost_path(self.seeds[-1][0],self.seeds[-1][1], self.node_mat)
		return self.min_path
