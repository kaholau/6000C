import sys
from PyQt5.QtCore import (Qt,QPoint,QSize,QDir,QObject,QFileInfo,pyqtSignal)
from PyQt5.QtGui import (QImage,QPainter,QPixmap,QPalette,QKeySequence,QIcon,qRgb)
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QAction, QActionGroup, QApplication, QFileDialog, QFrame,
		QLabel, QMainWindow, QMenu, QMessageBox,QScrollArea, QSizePolicy, QVBoxLayout,
		QWidget)
import proj1_imageviewer
import proj1_image
		

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.root = QFileInfo(__file__).absolutePath()
		self.curFile = ''

		'''self.imageLabel = Image()#QLabel()
		self.imageLabel.setBackgroundRole(QPalette.Base)
		self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		self.imageLabel.setScaledContents(True)'''

		self.graphicsView = proj1_imageviewer.ImageViewer()#QScrollArea()
		self.graphicsView.setMouseTracking(False)
		self.graphicsView.setBackgroundRole(QPalette.Dark)
		#self.graphicsView.setWidget(self.imageLabel)
		self.setCentralWidget(self.graphicsView)

		self.setWindowTitle("iScissor")
		self.setGeometry(100, 100, 480, 300)
		self.setMinimumSize(480,320)
		self.setWindowIcon(QIcon(self.root+'iScissor.png'))
		self.curFile = ''
		self.isModified = False

		self.createActions()
		self.createMenus()
		self.createToolBars()
		self.createStatusBar()

		return

	def eventFilter(self, obj, event):
		print(event.type())
		return False

		
	def createStatusBar(self):
		self.statusBar().showMessage("Ready")
		return
	#===========================Menu>File Action Funtion===================================#
	def open(self):
		if self.maybeSave():
			fileName, _ = QFileDialog.getOpenFileName(self, "Open Image",
					QDir.currentPath())
			if fileName:
				image = QImage(fileName)
				if image.isNull():
					QMessageBox.information(self, "iScissor",
							"Cannot load %s." % fileName)
					return

				imageLabel = proj1_image.Image(fileName)#QLabel()
				imageLabel.setBackgroundRole(QPalette.Base)
				imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
				imageLabel.setScaledContents(True)
				imageLabel.setPixmap(QPixmap.fromImage(image))

				self.graphicsView.setWidget(imageLabel)
				self.graphicsView.initialize()
				self.scaleFactor = 1.0
				self.normalSize()
			
		return

	def maybeSave(self):
		if self.graphicsView.isModified():
			ret = QMessageBox.warning(self, "iScissor",
						"The image has been modified.\n"
						"Do you want to save your changes?",
						QMessageBox.Save | QMessageBox.Discard |
						QMessageBox.Cancel)
			if ret == QMessageBox.Save:
				return self.save()
			elif ret == QMessageBox.Cancel:
				return False

		return True

	def save(self):
		if not self.getCurrentFile():
			return

		fileFormat ='png'
		initialPath = QDir.currentPath() + self.getCurrentFile()+'*.' + fileFormat
		fileName, _ = QFileDialog.getSaveFileName(self, "Save As", initialPath,
				"%s Files (*.%s);;All Files (*)" % (fileFormat.upper(), fileFormat))
		if fileName:
			if not self.graphicsView.widget.pixmap().save(fileName):
				QMessageBox.warning(self, self.tr("Save Image"),self.tr("Failed to save file at the specified location."))
				return
			self.statusBar().showMessage("File saved", 2000)
		
		return


	def exit(self):
		print('exit')
		return

	#===========================Menu>Edit Action Function================================#
	def reset(self):
		print('reset')
		self.graphicsView.clear()
		return

	def undo(self):
		print('undo')
		self.graphicsView.undo()
		return
	
	def copy(self):
		print('copy')
		return
	
	def paste(self):
		print('paste')
		return

	#==========================Menu>View Action Function===========================#

	def zoomIn(self):
		self.scaleImage(1.25)
		return
	def zoomOut(self):
		self.scaleImage(0.8)
		return

	def normalSize(self):
		#self.imageLabel.adjustSize()
		self.scaleFactor = 1.0
		return
			
	def orignalImg(self):
		print('orignalImg')
		return
	def gradientMap(self):
		print('gradientMap')
		return
	
	#=========================Menu>Action Action Function================================#

	def iScissorStart(self):
		print('iScissorStart')
		self.graphicsView.widget().start()
		self.graphicsView.setMouseTracking(True)
		self.graphicsView.setiScissorStarted(True)
		return
	def iScissorDone(self):
		print('iScissorDone')
		self.graphicsView.setMouseTracking(False)
		self.graphicsView.setiScissorStarted(False)
		return

	#========================Menu>About Action Function===================================#
	def about(self):
		print('about')
		return

	def updateActions(self):
		print('updateActions')
		return

	def scaleImage(self, factor):
		#self.scaleFactor *= factor
		#self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

		#self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
		#self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

		#self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
		#self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
		return

	def adjustScrollBar(self, scrollBar, factor):
		scrollBar.setValue(int(factor * scrollBar.value()
								+ ((factor - 1) * scrollBar.pageStep()/2)))

	def getCurrentFile(self):
		return self.curFile

	def setCurrentFile(self, fileName):
		self.curFile = fileName
		self.setModified(False)
		self.setWindowTitle("%s[*] - iScissor" % fileName)
		#self.setWindowTitle("%s[*] - iScissor" % QFileInfo(fileName).fileName())
		return
	def setModified(self,modified):
		self.isModified = modified
		return

	#==============================GUI Set Up=====================================================#
	def createActions(self):
		
		#===============================File===================================#
		self.openAct = QAction(QIcon(self.root + '/icon/open.png'),"&Open...", self, shortcut="Ctrl+O",
				statusTip="Open an existing Image", triggered=self.open)

		self.saveAct = QAction(QIcon(self.root + '/icon/save.png'),"&Save", self, shortcut="Ctrl+S",
				statusTip="Save the Image to disk", triggered=self.save)

		self.exitAct = QAction(QIcon(self.root + '/icon/exit.png'),"&Exit", self, shortcut="Ctrl+Q",
				statusTip="Exit the application", triggered=self.exit)


		#================================Edit================================#

		self.resetAct = QAction(QIcon(self.root + '/icon/reset.png'),"&Reset", self,
				statusTip="Reset the operation", triggered=self.reset)


		self.undoAct = QAction(QIcon(self.root + '/icon/undo.png'),"&Undo", self, shortcut="Ctrl+Z",
				statusTip="Undo the last operation", triggered=self.undo)


		self.copyAct = QAction(QIcon(self.root + '/icon/copy.png'),"&Copy", self, shortcut="Ctrl+C",
				statusTip="Copy the current selection's contents to the clipboard",
				triggered=self.copy)

		self.pasteAct = QAction(QIcon(self.root + '/icon/paste.png'),"&Paste", self, shortcut="Ctrl+V",
				statusTip="Paste the clipboard's contents into the current selection",
				triggered=self.paste)

		#================================View================================#

		self.zoomInAct = QAction(QIcon(self.root + '/icon/zoomIn.png'),"&Zoom In", self, shortcut="Ctrl++",
				statusTip="Zoom In",
				triggered=self.zoomIn)

		self.zoomOutAct = QAction(QIcon(self.root + '/icon/zoomOut.png'),"&Zoom Out", self, shortcut="Ctrl+-",
				statusTip="Zoom Out",
				triggered=self.zoomOut)

		self.normalSizeAct = QAction(QIcon(self.root + '/icon/normalSize.png'),"&Normal Size", self, shortcut="Ctrl+N",
				statusTip="Normal Size",
				triggered=self.normalSize)

		self.orignalImgAct = QAction("&Orignal Imgage", self,
				statusTip="Display the orignal Image",
				triggered=self.orignalImg)


		self.gradientMapAct = QAction("&Gradient Map", self,
				statusTip="Display the Gradient Map",
				triggered=self.gradientMap)

		#================================Action================================#

		self.iScissorStartAct = QAction(QIcon(self.root + '/icon/start.png'),"&iScissorStart", self, shortcut="1",
		statusTip="iScissorStart",triggered=self.iScissorStart)

		self.iScissorDoneAct = QAction(QIcon(self.root + '/icon/done.png'),"&iScissorDone", self, shortcut="2",
		statusTip="iScissorDone",triggered=self.iScissorDone)

		#===============================About===================================#
		self.aboutAct = QAction("&About", self,
				statusTip="Show the application's About box",
				triggered=self.about)

		return

	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.saveAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.editMenu = self.menuBar().addMenu("&Edit")
		self.editMenu.addAction(self.resetAct)
		self.editMenu.addAction(self.undoAct)
		self.editMenu.addSeparator()
		self.editMenu.addAction(self.copyAct)
		self.editMenu.addAction(self.pasteAct)

		self.editMenu = self.menuBar().addMenu("&View")
		self.editMenu.addAction(self.normalSizeAct)
		self.editMenu.addAction(self.zoomInAct)
		self.editMenu.addAction(self.zoomOutAct)
		self.editMenu.addSeparator()
		self.editMenu.addAction(self.orignalImgAct)
		self.editMenu.addAction(self.gradientMapAct)

		self.editMenu = self.menuBar().addMenu("&Action")
		self.editMenu.addAction(self.iScissorStartAct)
		self.editMenu.addAction(self.iScissorDoneAct)

		self.helpMenu = self.menuBar().addMenu("&Help")
		self.helpMenu.addAction(self.aboutAct)
		return

	def createToolBars(self):
		self.fileToolBar = self.addToolBar("File")
		self.fileToolBar.addAction(self.openAct)
		self.fileToolBar.addAction(self.saveAct)

		self.editToolBar = self.addToolBar("Edit")
		self.editToolBar.addAction(self.resetAct)
		self.editToolBar.addAction(self.undoAct)
		self.editToolBar.addAction(self.copyAct)
		self.editToolBar.addAction(self.pasteAct)


		self.editToolBar = self.addToolBar("View")
		self.editToolBar.addAction(self.normalSizeAct)
		self.editToolBar.addAction(self.zoomInAct)
		self.editToolBar.addAction(self.zoomOutAct)


		self.editToolBar = self.addToolBar("Edit")
		self.editToolBar.addAction(self.iScissorStartAct)
		self.editToolBar.addAction(self.iScissorDoneAct)  

