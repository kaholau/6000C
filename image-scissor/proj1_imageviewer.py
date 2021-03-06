
import sys
from PyQt5.QtCore import (Qt,QPoint,QSize,QDir,QObject,QFileInfo,pyqtSignal)
from PyQt5.QtGui import (QImage,QPainter,QPixmap,QPalette,QKeySequence,QIcon,qRgb)
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QAction, QActionGroup, QApplication, QFileDialog, QFrame,
		QLabel, QMainWindow, QMenu, QMessageBox,QScrollArea, QSizePolicy, QVBoxLayout,
		QWidget)
import numpy as np
import cv2 
from matplotlib import pyplot as plt



class ImageViewer(QScrollArea):

	def __init__(self,parent=None):
		super(ImageViewer, self).__init__(parent)
		# Image is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
		self.modified = False
		self.iScissorStarted = False
		self.mousePressed = False
		self.qImageHieght = 0
		self.qImageWidth = 0
		self.hieghtbound = 0
		self.widthbound = 0
		self.imageScaleFactor = 1
		self.seedNum = 0
		self.qImage = None
		self.costGraph =None
		#self.imageOriginalSize = (0,0)
		self.min_path=[]
		self.cur_seed = None
		return

	def initForImage(self,fileName):
		self.cvImg = cv2.imread(fileName,cv2.IMREAD_COLOR)
		self.qImage = self.widget().pixmap()
		self.qImageSize = self.widget().pixmap().size()
		self.qImageHieght = self.widget().pixmap().size().height()
		self.qImageWidth= self.widget().pixmap().size().width()
		self.hieghtbound = self.qImageHieght
		self.widthbound = self.qImageWidth
		self.imageScaleFactor = 1
		#self.imageOriginalSize = (,)   
		self.paintBoard = self.cvImg.copy()
		print(self.qImageSize,self.hieghtbound,self.widthbound )
		return

	def displayOriginalImg(self):
		self.qImage = self.get_qimage(self.cvImg)
		self.widget().setPixmap(self.qImage)		

		return
	def displayImgWithContour(self):
		self.drawPoint(self.cvImg,self.min_path)
		return


	def displayMaskedImg(self):
		self.getMaskedImage()
		return

	def displayCostGraph(self):
		print('Creating Cost Graph, please wait......')
		'''cv2.namedWindow('Cost Graph',cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Cost Graph', 640,480)
		cv2.imshow('Cost Graph',self.costGraph)
		'''
		plt.imshow(self.costGraph)
		plt.suptitle('Cost Graph')
		plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
		plt.show()
		print('Cost Graph Done')
		return
	
	def displayPathTreeGraph(self):
		if self.seedNum>0:
			print('Creating Path Tree, please wait......')
			img = self.getPathTreeGraph()
		return

	def resize(self, factor):
		self.imageScaleFactor = factor		
		self.hieghtbound = self.qImageHieght * factor
		self.widthbound = self.qImageWidth * factor
		self.widget().resize(factor  * self.qImage.size())
		return

	def normalSize(self):
		self.widget().adjustSize()
		return

	def setiScissorStarted(self, isStart):
		self.iScissorStarted = isStart
		if isStart : 
			self.costGraph = self.widget().start()
			print('iScissor Ready')
		return
	def setiScissorDone(self):
		print(len(self.min_path) )
		if len(self.min_path) >2:
			self.getMaskedImage()
			return True
		return False
	def getiScissorReady(self):
		if not self.qImage:
			return
		#print(self.widget().getiScissorReady())
		return self.widget().getiScissorReady()

	def getOriginalCoordinate(self, event):
		x = event.pos().x()
		y = event.pos().y()
		isGoal = False
		if  x < self.widthbound and y < self.hieghtbound:
			isGoal = True
			x = int(x/self.imageScaleFactor)
			y = int(y/self.imageScaleFactor)

		return isGoal,x,y

	def mousePressEvent(self, event):
		if self.getiScissorReady() and (self.seedNum>0):
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.mousePressed = True
				self.min_path = self.widget().mouseMoveCallback(y,x)
				self.drawPath(False,self.min_path)
		return 

	def mouseMoveEvent(self, event):
		if self.mousePressed and self.getiScissorReady() and (self.seedNum>0):
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.min_path = self.widget().mouseMoveCallback(y,x)
				self.drawPath(False,self.min_path)

		return      

	def mouseReleaseEvent(self, event):
		self.mousePressed = False
		if self.getiScissorReady():
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.min_path = self.widget().mouseReleaseCallback(y,x)
				self.cur_seed = [x,y]
				self.drawPath(True,self.min_path)
				self.seedNum += 1
		return  

	def drawPoint(self,img,mp):
		#print('drawPoint: ', mp)
		if len(mp)>1:
			for i in range(len(mp)-1):
				cv2.line(img,(mp[i][0],mp[i][1]),(mp[i+1][0],mp[i+1][1]),(255,0,0),2)
		elif len(mp) == 1:
			cv2.circle(img,(mp[0][0],mp[0][1]), 2, (0,0,255), -1)
		self.qImage = self.get_qimage(img)
		self.widget().setPixmap(self.qImage)
		return

	def drawPath(self,isConfirm,mp):
		self.modified = True
		if isConfirm:
			#it is confirmed when user release the mouse
			img = self.paintBoard 
			isConfirm = False
		else:
			img = self.paintBoard.copy()
		self.drawPoint(img,mp)
		return

	def get_qimage(self, image: np.ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

		image = image.rgbSwapped()
		return QPixmap.fromImage(image)

	def getMaskedImage(self):
		self.min_path = np.array(self.widget().getClosedCoutour())
		coutour_img = np.zeros((self.qImageHieght,self.qImageWidth),np.uint8)
		mp = self.min_path
		for i in range(len(mp)-1):
				cv2.line(coutour_img,(mp[i][0],mp[i][1]),(mp[i+1][0],mp[i+1][1]),255,1)

		mask = np.zeros((self.qImageHieght+2,self.qImageWidth+2), np.uint8)
 
		# Floodfill from point (0, 0)
		cv2.floodFill(coutour_img, mask, (0,0), 255);
		 
		# Invert floodfilled image
		mask = cv2.bitwise_not(coutour_img)
		#cv2.imshow('mask',mask)
		#cv2.waitKey()
		#cv2.fillConvexPoly(mask,min_path,255)

		#cv2.imshow('mask',mask)
		#cv2.waitKey()
		src = self.cvImg.copy()
		dst = cv2.bitwise_and(src,src,mask = mask)
		#cv2.imshow('dst',dst)
		mask2 = cv2.bitwise_not(mask)
		#cv2.imshow('res',mask2)
		white_background = np.full((self.qImageHieght,self.qImageWidth,3),255,np.uint8)
		#cv2.imshow('res2',white_background)
		white_background = cv2.bitwise_and(white_background,white_background,mask = mask2)

		
		result = dst+white_background
		self.qImage = self.get_qimage(result)
		self.widget().setPixmap(self.qImage)
		return
		

	def getPathTreeGraph(self):
		m = 3
		graph = np.zeros((self.qImageHieght*m,self.qImageWidth*m,3),np.uint8)
		cv2.circle(graph,(int(self.cur_seed[0]*m),int(self.cur_seed[1]*m)), 4, (255,255,255), -1)
		print(self.cur_seed)
		'''start_h = self.cur_seed[0] -int(self.cur_seed[0]*0.2)
		end_h = int((self.qImageHieght - self.cur_seed[0])*0.2)+self.cur_seed[0]
		start_w = self.cur_seed[1] - int(self.cur_seed[1]*0.2)
		end_w = int((self.qImageWidth - self.cur_seed[1])*0.2)+self.cur_seed[1]
		print(start_h,end_h,start_w,end_w)

		for i in range(start_h,end_h):
			for j in range(start_w,end_w):
		'''

		for i in range(5,self.qImageHieght-5):
			for j in range(5,self.qImageWidth-5):		
				mp = np.array(self.widget().get_min_path_coordinates(i,j))
				mp *= m
				for k in range(int(mp.size/2)-1):
					if (graph[mp[k+1,1],mp[k+1,0]].all() == 0):
						cv2.line(graph,(mp[k,0],mp[k,1]),(mp[k+1,0],mp[k+1,1]),(255,0,0),1)

		print('Path Tree Done')
		plt.imshow(graph)
		plt.suptitle('Path Tree')
		plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
		plt.show()


		return 

	def undo(self):
		if len(self.min_path) > 0:
			self.min_path = self.widget().undo()
			self.paintBoard = self.cvImg.copy()
			self.drawPath(True,self.min_path)
		return
	def isModified(self):
		return self.modified
