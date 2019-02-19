# _*_encoding=utf-8_*_
from PyQt5.QtWidgets import QDialog, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt5.QtGui import QTextOption
import numpy as np

class ShowBlcDataDlg(QDialog):
    def __init__(self, parent, data:tuple):
        super().__init__(parent)
        self.initUI(data)
        
    def initUI(self, data:tuple):
        mainLayout = QVBoxLayout()
        self.dataShowArea = QTextEdit(self)
        self.dataShowArea.setWordWrapMode(QTextOption.NoWrap)
        mainLayout.addWidget(self.dataShowArea)
        bottomLayout = QHBoxLayout()
        closeBtn = QPushButton('close', self)
        bottomLayout.addStretch(1)
        precisionLabel = QLabel('precision:')
        precisionBox = QComboBox()
        precisionBox.setEditable(False)
        precisionStrList = ['0', '1', '2', '3']
        precisionBox.addItems(precisionStrList)
        bottomLayout.addWidget(precisionLabel)
        bottomLayout.addWidget(precisionBox)
        bottomLayout.addStretch(1)
        bottomLayout.addWidget(closeBtn)
        closeBtn.clicked.connect(self.onCloseBtn)
        precisionBox.currentIndexChanged[str].connect(self.onPrecisionChanged)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
        self.resize(400, 800)
        self.setWindowTitle('blc data')
        
        (height, width) = data[0].shape
        self.r_1x1 = np.mean(data[0])
        self.gr_1x1 = np.mean(data[1])
        self.gb_1x1 = np.mean(data[2])
        self.b_1x1 = np.mean(data[3])
        
        width_unit = width/4
        height_unit = height/4
        self.r_5x5 = np.zeros((5, 5), np.float)
        self.gr_5x5 = np.zeros((5, 5), np.float)
        self.gb_5x5 = np.zeros((5, 5), np.float)
        self.b_5x5 = np.zeros((5, 5), np.float)
        for row in range(5):
            for col in range(5):
                y = int(row*height_unit+0.5)
                y = height-1 if y>=height else y
                x = int(col*width_unit+0.5)
                x = width-1 if x>=width else x
                self.r_5x5[row, col]=data[0][y, x]
                self.gr_5x5[row, col]=data[1][y, x]
                self.gb_5x5[row, col]=data[2][y, x]
                self.b_5x5[row, col]=data[3][y, x]
                
        width_unit = width/10
        height_unit = height/10
        self.r_11x11 = np.zeros((11, 11), np.float)
        self.gr_11x11 = np.zeros((11, 11), np.float)
        self.gb_11x11 = np.zeros((11, 11), np.float)
        self.b_11x11 = np.zeros((11, 11), np.float)
        for row in range(11):
            for col in range(11):
                y = int(row*height_unit+0.5)
                y = height-1 if y>=height else y
                x = int(col*width_unit+0.5)
                x = width-1 if x>=width else x
                self.r_11x11[row, col]=data[0][y, x]
                self.gr_11x11[row, col]=data[1][y, x]
                self.gb_11x11[row, col]=data[2][y, x]
                self.b_11x11[row, col]=data[3][y, x]
                
        prec_str = precisionBox.currentText()
        self.__flushTextEdit(prec_str)
    
    def onCloseBtn(self):
        self.accept()
    
    def __flushTextEdit(self, prec_str:str):
        if prec_str=='0':
            r_1x1 = self.r_1x1+0.5
            gr_1x1 = self.gr_1x1+0.5
            gb_1x1 = self.gb_1x1+0.5
            b_1x1 = self.b_1x1+0.5
            format_str_1x1 = 'R: %d, Gr: %d, Gb: %d, B: %d'
            r_5x5 = self.r_5x5+0.5
            gr_5x5 = self.gr_5x5+0.5
            gb_5x5 = self.gb_5x5+0.5
            b_5x5 = self.b_5x5+0.5
            format_str_5x5 = '%d, %d, %d, %d, %d,'
            r_11x11 = self.r_11x11+0.5
            gr_11x11 = self.gr_11x11+0.5
            gb_11x11 = self.gb_11x11+0.5
            b_11x11 = self.b_11x11+0.5
            format_str_11x11 = '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,'
        elif prec_str=='1':
            r_1x1 = self.r_1x1+0.05
            gr_1x1 = self.gr_1x1+0.05
            gb_1x1 = self.gb_1x1+0.05
            b_1x1 = self.b_1x1+0.05
            format_str_1x1 = 'R: %.1f, Gr: %.1f, Gb: %.1f, B: %.1f'
            r_5x5 = self.r_5x5+0.05
            gr_5x5 = self.gr_5x5+0.05
            gb_5x5 = self.gb_5x5+0.05
            b_5x5 = self.b_5x5+0.05
            format_str_5x5 = '%.1f, %.1f, %.1f, %.1f, %.1f,'
            r_11x11 = self.r_11x11+0.05
            gr_11x11 = self.gr_11x11+0.05
            gb_11x11 = self.gb_11x11+0.05
            b_11x11 = self.b_11x11+0.05
            format_str_11x11 = '%.1f, %.1f, %.1f, %.1f, %.1f, %.1f, %.1f, %.1f, %.1f, %.1f, %.1f'
        elif prec_str=='2':
            r_1x1 = self.r_1x1+0.005
            gr_1x1 = self.gr_1x1+0.005
            gb_1x1 = self.gb_1x1+0.005
            b_1x1 = self.b_1x1+0.005
            format_str_1x1 = 'R: %.2f, Gr: %.2f, Gb: %.2f, B: %.2f'
            r_5x5 = self.r_5x5+0.005
            gr_5x5 = self.gr_5x5+0.005
            gb_5x5 = self.gb_5x5+0.005
            b_5x5 = self.b_5x5+0.005
            format_str_5x5 = '%.2f, %.2f, %.2f, %.2f, %.2f,'
            r_11x11 = self.r_11x11+0.005
            gr_11x11 = self.gr_11x11+0.005
            gb_11x11 = self.gb_11x11+0.005
            b_11x11 = self.b_11x11+0.005
            format_str_11x11 = '%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f'
        elif prec_str=='3':
            r_1x1 = self.r_1x1+0.0005
            gr_1x1 = self.gr_1x1+0.0005
            gb_1x1 = self.gb_1x1+0.0005
            b_1x1 = self.b_1x1+0.0005
            format_str_1x1 = 'R: %.3f, Gr: %.3f, Gb: %.3f, B: %.3f'
            r_5x5 = self.r_5x5+0.0005
            gr_5x5 = self.gr_5x5+0.0005
            gb_5x5 = self.gb_5x5+0.0005
            b_5x5 = self.b_5x5+0.0005
            format_str_5x5 = '%.3f, %.3f, %.3f, %.3f, %.3f,'
            r_11x11 = self.r_11x11+0.005
            gr_11x11 = self.gr_11x11+0.005
            gb_11x11 = self.gb_11x11+0.005
            b_11x11 = self.b_11x11+0.005
            format_str_11x11 = '%.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f'
        else:
            r_1x1 = self.r_1x1+0.5
            gr_1x1 = self.gr_1x1+0.5
            gb_1x1 = self.gb_1x1+0.5
            b_1x1 = self.b_1x1+0.5
            format_str_1x1 = 'R: %d, Gr: %d, Gb: %d, B: %d'
            r_5x5 = self.r_5x5+0.5
            gr_5x5 = self.gr_5x5+0.5
            gb_5x5 = self.gb_5x5+0.5
            b_5x5 = self.b_5x5+0.5
            format_str_5x5 = '%d, %d, %d, %d, %d,'
            r_11x11 = self.r_11x11+0.5
            gr_11x11 = self.gr_11x11+0.5
            gb_11x11 = self.gb_11x11+0.5
            b_11x11 = self.b_11x11+0.5
            format_str_11x11 = '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,'
            
        self.dataShowArea.append('1x1:')
        self.dataShowArea.append(format_str_1x1%(r_1x1, gr_1x1, gb_1x1, b_1x1))
        self.dataShowArea.append('5x5 R:')
        for row in range(5):
            self.dataShowArea.append(format_str_5x5%(r_5x5[row, 0], r_5x5[row, 1], r_5x5[row, 2], r_5x5[row, 3], r_5x5[row, 4]))
        self.dataShowArea.append('5x5 Gr:')
        for row in range(5):
            self.dataShowArea.append(format_str_5x5%(gr_5x5[row, 0], gr_5x5[row, 1], gr_5x5[row, 2], gr_5x5[row, 3], gr_5x5[row, 4]))
        self.dataShowArea.append('5x5 Gb:')
        for row in range(5):
            self.dataShowArea.append(format_str_5x5%(gb_5x5[row, 0], gb_5x5[row, 1], gb_5x5[row, 2], gb_5x5[row, 3], gb_5x5[row, 4]))
        self.dataShowArea.append('5x5 B:')
        for row in range(5):
            self.dataShowArea.append(format_str_5x5%(b_5x5[row, 0], b_5x5[row, 1], b_5x5[row, 2], b_5x5[row, 3], b_5x5[row, 4]))
            
        self.dataShowArea.append('11x11 R:')
        for row in range(11):
            self.dataShowArea.append(format_str_11x11%(r_11x11[row, 0], r_11x11[row, 1], r_11x11[row, 2], r_11x11[row, 3], r_11x11[row, 4],\
            r_11x11[row, 5], r_11x11[row, 6], r_11x11[row, 7], r_11x11[row, 8], r_11x11[row, 9], r_11x11[row, 10]))
        self.dataShowArea.append('11x11 Gr:')
        for row in range(11):
            self.dataShowArea.append(format_str_11x11%(gr_11x11[row, 0], gr_11x11[row, 1], gr_11x11[row, 2], gr_11x11[row, 3], gr_11x11[row, 4],\
            gr_11x11[row, 5], gr_11x11[row, 6], gr_11x11[row, 7], gr_11x11[row, 8], gr_11x11[row, 9], gr_11x11[row, 10]))
        self.dataShowArea.append('11x11 Gb:')
        for row in range(11):
            self.dataShowArea.append(format_str_11x11%(gb_11x11[row, 0], gb_11x11[row, 1], gb_11x11[row, 2], gb_11x11[row, 3], gb_11x11[row, 4],\
            gb_11x11[row, 5], gb_11x11[row, 6], gb_11x11[row, 7], gb_11x11[row, 8], gb_11x11[row, 9], gb_11x11[row, 10]))
        self.dataShowArea.append('11x11 B:')
        for row in range(11):
            self.dataShowArea.append(format_str_11x11%(b_11x11[row, 0], b_11x11[row, 1], b_11x11[row, 2], b_11x11[row, 3], b_11x11[row, 4],\
            b_11x11[row, 5], b_11x11[row, 6], b_11x11[row, 7], b_11x11[row, 8], b_11x11[row, 9], b_11x11[row, 10]))
            
    def onPrecisionChanged(self, precisionStr:str):
        self.dataShowArea.clear()
        self.__flushTextEdit(precisionStr)
