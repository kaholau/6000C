
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
		self.min_path=[]
		return

	def initialize(self,fileName):
		self.cvImg = cv2.imread(fileName,cv2.IMREAD_COLOR)
		self.qImage = self.widget().pixmap()
		self.qImageSize =self.widget().pixmap().size()
		self.paintBoard = self.cvImg.copy()
		print(self.qImageSize)
		return

	def resize(self, factor):
		self.widget().resize(factor * self.qImage.size())
		return

	def normalSize(self):
		self.widget().adjustSize()
		return

	def setiScissorStarted(self,status):
		self.iScissorStarted = status
		return

	def mousePressEvent(self, event):
		if self.iScissorStarted:
			self.mousePressed = True
			self.min_path = self.widget().mousePressCallback(event.pos().x(),event.pos().y())
			self.drawPoint(event.pos().x(),event.pos().y())
			#print(event.pos().x(),event.pos().y())
		return 

	def mouseMoveEvent(self, event):
		if self.iScissorStarted and self.mousePressed:
			self.widget().mouseMoveCallback(event.pos().x(),event.pos().y())
		return      
	def mouseReleaseEvent(self, event):
		if self.iScissorStarted and self.mousePressed:
			self.mousePressed = False

	def drawPoint(self,x,y):
		mp = self.min_path
		if len(mp)>1:
			for i in range(len(mp)-1):
				cv2.line(self.paintBoard,(mp[i][0],mp[i][1]),(mp[i+1][0],mp[i+1][1]),(255,0,0),2)
		else:
			cv2.circle(self.paintBoard,(mp[0][0],mp[0][1]), 2, (0,0,255), -1)
		self.qImage = self.get_qimage(self.paintBoard)
		self.widget().setPixmap(self.qImage)
		return

	def get_qimage(self, image: np.ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

		image = image.rgbSwapped()
		return QPixmap.fromImage(image)


	def isModified(self):
		return self.modified
