# _*_ encoding=utf-8 _*_
import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QDialog, \
    QComboBox, QLabel, QGroupBox, QGridLayout, QRadioButton, QPushButton
from PyQt5.QtCore import QDir, QFileInfo #Qt
from PyQt5.QtGui import QFont
from aboutDlg import aboutDlg
import rawHandle
import rawinfoDlg
import showBlcDataDlg

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
        self.whichChannel = -1
        self.channelStr = ''     
        self.colorMap = ''
        self.iso_fixed = 50 
        self.file_size = 0
        self.initUI()
                  
    def initUI(self):          
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('&File')
        openAction = fileMenu.addAction('open raw')
        aboutMenu = self.menuBar.addMenu('&About')
        aboutQtAction = aboutMenu.addAction('about Qt')
        aboutThisAction = aboutMenu.addAction('about ...')
        openAction.triggered.connect(self.onOpenFileAction)
        aboutQtAction.triggered.connect(self.onAboutQtAction)
        aboutThisAction.triggered.connect(self.onAboutThisAction)
        
        mainLayout = QHBoxLayout()
        
        leftLayout = QVBoxLayout()
        self._main = QWidget(self)
        self.setCentralWidget(self._main)
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #self.addToolBar(Qt.BottomToolBarArea, NavigationToolbar(self.static_canvas, self))
        self._static_ax = self.static_canvas.figure.add_subplot(1, 1, 1,  projection='3d')
        leftLayout.addWidget(self.static_canvas,  1)
        leftLayout.addWidget(NavigationToolbar(self.static_canvas, self._main))
        mainLayout.addLayout(leftLayout)
        
        midLayout = QVBoxLayout()
        
        showBayerChannelGroup = QGroupBox('show which channel')
        channelLayout = QGridLayout()
        self.r_radioBtn = QRadioButton('r',  showBayerChannelGroup)
        self.gr_radioBtn = QRadioButton('gr',  showBayerChannelGroup)
        self.gb_radioBtn = QRadioButton('gb',  showBayerChannelGroup)
        self.b_radioBtn = QRadioButton('b',  showBayerChannelGroup)
        channelLayout.addWidget(self.r_radioBtn,  0,  0,  1,  1)
        channelLayout.addWidget(self.gr_radioBtn,  0,  1,  1,  1)
        channelLayout.addWidget(self.gb_radioBtn,  1,  0,  1,  1)
        channelLayout.addWidget(self.b_radioBtn,  1,  1,  1,  1)
        self.r_radioBtn.setChecked(True)
        self.channelStr = 'R'
        self.r_radioBtn.toggled.connect(self.onRchannelBtn)
        self.gr_radioBtn.toggled.connect(self.onGrchannelBtn)
        self.gb_radioBtn.toggled.connect(self.onGbchannelBtn)
        self.b_radioBtn.toggled.connect(self.onBchannelBtn)
        showBayerChannelGroup.setLayout(channelLayout)
        midLayout.addWidget(showBayerChannelGroup)
        
        colorThemeLayout = QHBoxLayout()
        colorThemeLabel = QLabel('color theme')
        self.colorThemeComBox = QComboBox()
        self.colorThemeComBox.setEditable(False)
        cmap= ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        self.colorThemeComBox.addItems(cmap)
        colorThemeLayout.addWidget(colorThemeLabel)
        colorThemeLayout.addWidget(self.colorThemeComBox)
        self.colorThemeComBox.currentIndexChanged[str].connect(self.changeColorMap)
        midLayout.addLayout(colorThemeLayout)
        
        showBlcNumberBtn = QPushButton('show blc data', self)
        midLayout.addStretch(1)
        midLayout.addWidget(showBlcNumberBtn)
        midLayout.addStretch(1)
        showBlcNumberBtn.clicked.connect(self.onShowBlcData)
        
        mainLayout.addLayout(midLayout)
        self._main.setLayout(mainLayout)
        
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
        
        for idx,  fileName in enumerate(open_files[0]):
            str_list = fileName.split('_')
            if str_list.count('ISO')==0:
                QMessageBox.information(self,  'error',  'no ISO info in {0}'.format(fileName),  QMessageBox.Ok)
                return
            iso = int(str_list[str_list.index('ISO')+1])
            file_size = QFileInfo(fileName).size()
            if idx==0:
                self.iso_fixed = iso
                self.file_size = file_size
            else:
                if iso!=self.iso_fixed:
                    QMessageBox.information(self,  'error',  'ISO in your selected raws are not same',  QMessageBox.Ok)
                    return
                if file_size!=self.file_size:
                    QMessageBox.information(self,  'error',  'Inconsistent file size !',  QMessageBox.Ok)
                    return
        infoDlg = rawinfoDlg.RawinfoDlg(self.file_size, self)
        reply = infoDlg.exec_()
        if reply == QDialog.Accepted:
            try:
                self.data = rawHandle.handle(open_files[0],  infoDlg.bayer,  infoDlg.rawWidth,  infoDlg.rawHeight,  infoDlg.bitDepth)
                if self.data==None:
                    QMessageBox.information(self,  'error',  'raw handle result error',  QMessageBox.Ok)
                    return

                if self.r_radioBtn.isChecked():
                    self.whichChannel = 0
                    self.channelStr = 'R'
                elif self.gr_radioBtn.isChecked():
                    self.whichChannel = 1
                    self.channelStr = 'Gr'
                elif self.gb_radioBtn.isChecked():
                    self.whichChannel = 2
                    self.channelStr = 'Gb'
                else:
                    self.whichChannel = 3
                    self.channelStr = 'B'
                self.colorMap = self.colorThemeComBox.currentText()
                h,  w = self.data[self.whichChannel].shape
                h = np.arange(0,  h)
                w = np.arange(0,  w)
                h,  w = np.meshgrid(w, h)
                self._static_ax.clear()
                if hasattr(self,  'colorBar'):
                    self.colorBar.remove()
                z_max = np.max(self.data[self.whichChannel])
                z_min = np.min(self.data[self.whichChannel])
                self._static_ax.set_zlim([z_min-10,  z_max+10])
                self._static_ax.set_ylim([h.shape[0],  0])
                self.surface = self._static_ax.plot_surface(h,  w, self.data[self.whichChannel],  cmap=cm.get_cmap(self.colorMap), linewidth=0, antialiased=True)
                self._static_ax.set_title('ISO '+str(self.iso_fixed)+' '+self.channelStr+' channel 3d plot')
                self.colorBar = self.static_canvas.figure.colorbar(self.surface,  pad=0.15,  shrink=0.5,  aspect=10)
                self._static_ax.figure.canvas.draw()
                self.repaint()
            except ValueError as ve:
                print(ve)
    
    def changeColorMap(self,  colorMap:str):
        self.colorMap = colorMap
        self._static_ax.clear()
        if hasattr(self,  'colorBar'):
            self.colorBar.remove()
        h,  w = self.data[self.whichChannel].shape
        h = np.arange(0,  h)
        w = np.arange(0,  w)
        h,  w = np.meshgrid(w, h)
        z_max = np.max(self.data[self.whichChannel])
        z_min = np.min(self.data[self.whichChannel])
        self._static_ax.set_zlim([z_min-10,  z_max+10])
        self._static_ax.set_ylim([h.shape[0],  0])
        self.surface = self._static_ax.plot_surface(h,  w, self.data[self.whichChannel],  cmap=cm.get_cmap(self.colorMap), linewidth=0, antialiased=True)
        self._static_ax.set_title('ISO '+str(self.iso_fixed)+' '+self.channelStr+' channel 3d plot')
        self.colorBar = self.static_canvas.figure.colorbar(self.surface,  pad=0.15,  shrink=0.5,  aspect=10)
        self._static_ax.figure.canvas.draw()
        self.repaint()
        
    def onRchannelBtn(self,  checked:bool):
        self.channelStr = 'R'
        self.whichChannel = 0
        self.__flushAxes()
        
    def onGrchannelBtn(self,  checked:bool):
        self.channelStr = 'Gr'
        self.whichChannel = 1
        self.__flushAxes()
        
    def onGbchannelBtn(self,  checked:bool):
        self.channelStr = 'Gb'
        self.whichChannel = 2
        self.__flushAxes()
        
    def onBchannelBtn(self,  checked:bool):
        self.channelStr = 'B'
        self.whichChannel = 3
        self.__flushAxes()

    def __flushAxes(self):
        self._static_ax.clear()
        if hasattr(self,  'colorBar'):
            self.colorBar.remove()
        h,  w = self.data[self.whichChannel].shape
        h = np.arange(0,  h)
        w = np.arange(0,  w)
        h,  w = np.meshgrid(w, h)
        z_max = np.max(self.data[self.whichChannel])
        z_min = np.min(self.data[self.whichChannel])
        self._static_ax.set_zlim([z_min-10,  z_max+10])
        self._static_ax.set_ylim([h.shape[0],  0])
        self.surface = self._static_ax.plot_surface(h,  w, self.data[self.whichChannel],  cmap=cm.get_cmap(self.colorMap), linewidth=0, antialiased=True)
        self._static_ax.set_title('ISO '+str(self.iso_fixed)+' '+self.channelStr+' channel 3d plot')
        self.colorBar = self.static_canvas.figure.colorbar(self.surface,  pad=0.15,  shrink=0.5,  aspect=10)
        self._static_ax.figure.canvas.draw()
        self.repaint()
    
    def onShowBlcData(self):
        if hasattr(self, 'data') and isinstance(self.data, tuple) and len(self.data)==4:
            dlg = showBlcDataDlg.ShowBlcDataDlg(self, self.data)
            dlg.exec_()
        else:
            QMessageBox.information(self, 'error', 'have no (enough) data to show', QMessageBox.Ok)

if __name__ == '__main__':     
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 10))
    ex = jonahWidget()
    ex.show()
    sys.exit(app.exec_())
