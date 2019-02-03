# _*_ encoding=utf-8 _*_
import sys
from PyQt5.QtWidgets import QMainWindow,  QWidget, QApplication,  QMessageBox,  QFileDialog,  QVBoxLayout
from PyQt5.QtCore import  QDir
from PyQt5.QtGui import QFont
from aboutDlg import aboutDlg
import rawHandle

from matplotlib.backends.backend_qt5agg import FigureCanvas
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
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        vlayout.addWidget(static_canvas,  1)
        self._main.setLayout(vlayout)
        self._static_ax = static_canvas.figure.add_subplot(1, 1, 1,  projection='3d')
#        t = np.linspace(0, 10, 501)
#        self._static_ax.plot(t, np.tan(t), ".")
        
        screenInfo = QApplication.desktop()
        screenIdx = screenInfo.screenNumber()#current screen index
        screenRect = screenInfo.screenGeometry(screenIdx)
        self.setGeometry((screenRect.width()-600)/2, (screenRect.height()-400)/2, 600, 400)
        self.setWindowTitle('blc savgol filter 3d plot')   
        self.show()
        
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
        #TODO: add rawinfo dlg
        data = rawHandle.handle(open_files[0],  'BG', 5120,  3840,  12)
        if data==None:
            QMessageBox.information(self,  'error',  'raw handle result error',  QMessageBox.Ok)
 
if __name__ == '__main__':     
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 10))
    ex = jonahWidget()
    sys.exit(app.exec_())