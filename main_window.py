# _*_ encoding=utf-8 _*_
import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox, QFileDialog, QVBoxLayout, QDialog
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont
from aboutDlg import aboutDlg
import rawHandle
import rawinfoDlg

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#from mpl_toolkits.mplot3d.axes3d import get_test_data
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm

 
class jonahWidget(QMainWindow):
     
    def __init__(self):
        super().__init__()         
        self.initUI()
                  
    def initUI(self):          
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('&File')
        openAction = fileMenu.addAction('open file')
        aboutMenu = self.menuBar.addMenu('&About')
        aboutQtAction = aboutMenu.addAction('about Qt')
        aboutThisAction = aboutMenu.addAction('about ...')
        openAction.triggered.connect(self.onOpenFileAction)
        aboutQtAction.triggered.connect(self.onAboutQtAction)
        aboutThisAction.triggered.connect(self.onAboutThisAction)
        self._main = QWidget(self)
        self.setCentralWidget(self._main)
        vlayout = QVBoxLayout()
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.addToolBar(Qt.BottomToolBarArea, NavigationToolbar(self.static_canvas, self))
        vlayout.addWidget(self.static_canvas,  1)
        self._main.setLayout(vlayout)
        self._static_ax = self.static_canvas.figure.add_subplot(1, 1, 1,  projection='3d')
        
        screenInfo = QApplication.desktop()
        screenIdx = screenInfo.screenNumber()#current screen index
        screenRect = screenInfo.screenGeometry(screenIdx)
        self.setGeometry((screenRect.width()-900)/2, (screenRect.height()-600)/2, 900, 600)
        self.setWindowTitle('blc savgol filter 3d plot')   
        
    def closeEvent(self,  event):
        replay = QMessageBox.question(self,  'quit',  'are you really wanna quit?')
        if replay == QMessageBox.Yes:
            super().closeEvent(event)
        else:
            event.ignore()
    
    def onAboutQtAction(self):
        QApplication.instance().aboutQt()
        
    def onAboutThisAction(self):
        about = aboutDlg(self)
        about.exec_()
    
    def onOpenFileAction(self):
        '''
        type open_files: tuple
        '''
        current_dir = QDir.currentPath()
        open_files = QFileDialog.getOpenFileNames(self,  'open raw',  current_dir,  'raw file(*.raw);;all file(*.*)')
        if len(open_files[0])<=0 :
            return 
        if open_files[1]!='raw file(*.raw)':
            QMessageBox.information(self,  'error',  'only raw file can be selected!',  QMessageBox.Ok)
            return
        iso_fixed = 50
        for idx,  fileName in enumerate(open_files[0]):
            str_list = fileName.split('_')
            if str_list.count('ISO')==0:
                QMessageBox.information(self,  'error',  'no ISO info in {0}'.format(fileName),  QMessageBox.Ok)
                return
            iso = int(str_list[str_list.index('ISO')+1])
            if idx==0:
                iso_fixed = iso
            else:
                if iso!=iso_fixed:
                    QMessageBox.information(self,  'error',  'ISO in your selected raws are not same',  QMessageBox.Ok)
                    return
        infoDlg = rawinfoDlg.RawinfoDlg(self)
        reply = infoDlg.exec_()
        if reply == QDialog.Accepted:
            try:
                data = rawHandle.handle(open_files[0],  infoDlg.bayer,  infoDlg.rawWidth,  infoDlg.rawHeight,  infoDlg.bitDepth)
                if data==None:
                    QMessageBox.information(self,  'error',  'raw handle result error',  QMessageBox.Ok)
                    return

                h,  w = data[0].shape
                h = np.arange(0,  h)
                w = np.arange(0,  w)
                h,  w = np.meshgrid(w, h)
                self._static_ax.clear()
                z_max = np.max(data[0])
                z_min = np.min(data[0])
                self._static_ax.set_zlim([z_min-10,  z_max+10])
                #self._static_ax.set_xlim([0,  160])
                self._static_ax.set_ylim([h.shape[0],  0])
                self.surface = self._static_ax.plot_surface(h,  w,  data[0],  cmap=cm.coolwarm, linewidth=1, antialiased=True)
                self.static_canvas.figure.colorbar(self.surface,  pad=0.15,  shrink=0.5,  aspect=10)
                self._static_ax.figure.canvas.draw()
                self.repaint()
            except ValueError as ve:
                print(ve)

if __name__ == '__main__':     
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 10))
    ex = jonahWidget()
    ex.show()
    sys.exit(app.exec_())
