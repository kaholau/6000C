
import sys
from PyQt5.QtCore import (Qt,QPoint,QSize,QDir,QObject,QFileInfo,pyqtSignal)
from PyQt5.QtGui import (QImage,QPainter,QPixmap,QPalette,QKeySequence,QIcon,qRgb)
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QAction, QActionGroup, QApplication, QFileDialog, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox,QScrollArea, QSizePolicy, QVBoxLayout,
        QWidget)

        



class ImageViewer(QScrollArea):

    def __init__(self,parent=None):
        super(ImageViewer, self).__init__(parent)
        # Image is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
        self.modified = False
        self.iScissorStarted = False
        self.mousePressed = False

        return

    def initialize(self):
        self.image = self.widget().pixmap()
        self.imageSize =self.widget().pixmap().size()
        print(self.imageSize)
        return


    def setiScissorStarted(self,status):
        self.iScissorStarted = status
        return

    def mousePressEvent(self, event):
        if self.iScissorStarted:
            self.mousePressed = True
            self.widget().mousePressCallback(event.pos().x(),event.pos().y())
            #print(event.pos().x(),event.pos().y())
        return 

    def mouseMoveEvent(self, event):
        if self.iScissorStarted and self.mousePressed:
            self.widget().mouseMoveCallback(event.pos().x(),event.pos().y())
        return      
    def mouseReleaseEvent(self, event):
        if self.iScissorStarted and self.mousePressed:
            self.mousePressed = False


    def isModified(self):
        return self.modified
