import sys
from PyQt5.QtCore import (Qt,QFileInfo)
from PyQt5.QtGui import (QKeySequence,QIcon)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
		QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
		QWidget)


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.createActions()
		self.createMenus()
		self.createToolBars()
		self.createStatusBar()


		self.setWindowTitle("iScissor")
		self.setMinimumSize(480,320)
		self.curFile = ''

		return

	def createStatusBar(self):
		self.statusBar().showMessage("Ready")
		return
	#===========================Menu>File Action Funtion===================================#
	def open(self):
		print('open file')
		return

	def save(self):
		print('save')
		return

	def exit(self):
		print('exit')
		return

	#===========================Menu>Edit Action Function================================#
	def undo(self):
		print('undo')
		return
	
	def copy(self):
		print('copy')
		return
	
	def paste(self):
		print('paste')
		return

	#==========================Menu>View Action Function===========================#

	def zoomIn(self):
		print('zoomIn')
		return
	def zoomOut(self):
		print('zoomOut')
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
		return
	def iScissorDone(self):
		print('iScissorDone')
		return

	#========================Menu>About Action Function===================================#
	def about(self):
		print('about')
		return


	def createActions(self):
		root = QFileInfo(__file__).absolutePath()
		#===============================File===================================#
		self.openAct = QAction(QIcon(root + '/icon/open.png'),"&Open...", self, shortcut="Ctrl+O",
				statusTip="Open an existing Image", triggered=self.open)

		self.saveAct = QAction(QIcon(root + '/icon/save.png'),"&Save", self, shortcut="Ctrl+S",
				statusTip="Save the Image to disk", triggered=self.save)

		self.exitAct = QAction(QIcon(root + '/icon/exit.png'),"&Exit", self, shortcut="Ctrl+Q",
				statusTip="Exit the application", triggered=self.exit)


		#================================Edit================================#

		self.undoAct = QAction(QIcon(root + '/icon/undo.png'),"&Undo", self, shortcut="Ctrl+Z",
				statusTip="Undo the last operation", triggered=self.undo)


		self.copyAct = QAction(QIcon(root + '/icon/copy.png'),"&Copy", self, shortcut="Ctrl+C",
				statusTip="Copy the current selection's contents to the clipboard",
				triggered=self.copy)

		self.pasteAct = QAction(QIcon(root + '/icon/paste.png'),"&Paste", self, shortcut="Ctrl+V",
				statusTip="Paste the clipboard's contents into the current selection",
				triggered=self.paste)

		#================================View================================#

		self.zoomInAct = QAction(QIcon(root + '/icon/zoomIn.png'),"&Zoom In", self, shortcut="Ctrl++",
				statusTip="Zoom In",
				triggered=self.zoomIn)

		self.zoomOutAct = QAction(QIcon(root + '/icon/zoomOut.png'),"&Zoom Out", self, shortcut="Ctrl+-",
				statusTip="Zoom Out",
				triggered=self.zoomOut)


		self.orignalImgAct = QAction("&Orignal Imgage", self,
				statusTip="Display the orignal Image",
				triggered=self.orignalImg)


		self.gradientMapAct = QAction("&Gradient Map", self,
				statusTip="Display the Gradient Map",
				triggered=self.gradientMap)

		#================================Action================================#

		self.iScissorStartAct = QAction(QIcon(root + '/icon/start.png'),"&iScissorStart", self, shortcut="1",
		statusTip="iScissorStart",triggered=self.iScissorStart)

		self.iScissorDoneAct = QAction(QIcon(root + '/icon/done.png'),"&iScissorDone", self, shortcut="2",
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
		self.editMenu.addAction(self.undoAct)
		self.editMenu.addSeparator()
		self.editMenu.addAction(self.copyAct)
		self.editMenu.addAction(self.pasteAct)

		self.editMenu = self.menuBar().addMenu("&View")
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
		self.editToolBar.addAction(self.undoAct)
		self.editToolBar.addAction(self.copyAct)
		self.editToolBar.addAction(self.pasteAct)


		self.editToolBar = self.addToolBar("View")
		self.editToolBar.addAction(self.zoomInAct)
		self.editToolBar.addAction(self.zoomOutAct)


		self.editToolBar = self.addToolBar("Edit")
		self.editToolBar.addAction(self.iScissorStartAct)
		self.editToolBar.addAction(self.iScissorDoneAct)  



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())