import proj1_window
import sys
from PyQt5.QtWidgets import QApplication

def randomMat(min,max,h,w):
	return np.random.randint(min,max,(h,w))

app = QApplication(sys.argv)
window = proj1_window.MainWindow()
window.show()
sys.exit(app.exec_())
