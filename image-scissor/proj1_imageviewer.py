
import sys
from PyQt5.QtCore import (Qt,QPoint,QSize,QDir,QObject,QFileInfo,pyqtSignal)
from PyQt5.QtGui import (QImage,QPainter,QPixmap,QPalette,QKeySequence,QIcon,qRgb)
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QAction, QActionGroup, QApplication, QFileDialog, QFrame,
		QLabel, QMainWindow, QMenu, QMessageBox,QScrollArea, QSizePolicy, QVBoxLayout,
		QWidget)
import numpy as np
import cv2 
		



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
		#self.imageOriginalSize = (0,0)
		self.min_path=[]
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
			self.widget().start()
		return

	def getiScissorReady(self):
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
			print(x,y)
		return isGoal,x,y

	def mousePressEvent(self, event):
		if self.getiScissorReady() and (self.seedNum>0):
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.mousePressed = True
				self.min_path = self.widget().mouseMoveCallback(y,x)
				self.drawPoint(False,self.min_path)
				print('mousePressEvent')
		return 

	def mouseMoveEvent(self, event):
		if self.mousePressed and self.getiScissorReady() and (self.seedNum>0):
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.min_path = self.widget().mouseMoveCallback(y,x)
				self.drawPoint(False,self.min_path)
				print('mouseMoveEvent')

		return      

	def mouseReleaseEvent(self, event):
		self.mousePressed = False
		if self.getiScissorReady():
			isGoal,x,y = self.getOriginalCoordinate(event)
			if isGoal:
				self.min_path = self.widget().mouseReleaseCallback(y,x)
				self.drawPoint(True,self.min_path)
				self.seedNum += 1
				#print(event.pos().x(),event.pos().y())

	def drawPoint(self,isConfirm,mp):
		self.modified = True
		if isConfirm:
			#it is confirmed when user release the mouse
			img = self.paintBoard 
			isConfirm = False
		else:
			img = self.paintBoard.copy()

		if len(mp)>1:
			for i in range(len(mp)-1):
				cv2.line(img,(mp[i][0],mp[i][1]),(mp[i+1][0],mp[i+1][1]),(255,0,0),2)
		else:
			cv2.circle(img,(mp[0][0],mp[0][1]), 2, (0,0,255), -1)
		self.qImage = self.get_qimage(img)
		self.widget().setPixmap(self.qImage)
		return

	def get_qimage(self, image: np.ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

		image = image.rgbSwapped()
		return QPixmap.fromImage(image)

	def getMaskedImage(self):
		if True:
			min_path = np.array(self.min_path)
			mask = np.zeros((self.qImageHieght,self.qImageWidth),np.uint8)
			cv2.fillConvexPoly(mask,min_path,255)
			cv2.imshow('mask',mask)
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
		
	def getImageWithContour(self):
		src = self.cvImg.copy()
		for i in range(len(mp)-1):
				cv2.line(src,(mp[i][0],mp[i][1]),(mp[i+1][0],mp[i+1][1]),(255,0,0),2)
		return self.get_qimage(src)

	def isModified(self):
		return self.modified
