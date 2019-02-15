#  _*_ encoding=utf-8 _*_
import sys
from PyQt5.QtWidgets import QDialog,  QGroupBox,  QHBoxLayout,  QVBoxLayout,  QGridLayout,  QRadioButton,  \
QApplication,  QLabel,  QLineEdit,  QFrame,  QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

class RawinfoDlg(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.bayer = 'None'
        self.rawWidth = 0
        self.rawHeight = 0
        self.bitDepth = 0
        self.initUI()
        
    def initUI(self):
        bayerGroup = QGroupBox('bayer')
        bayerLayout = QGridLayout()
        self.rg = QRadioButton('RG',  bayerGroup)
        self.gr = QRadioButton('GR',  bayerGroup)
        self.gb = QRadioButton('GB',  bayerGroup)
        self.bg = QRadioButton('BG',  bayerGroup)
        bayerLayout.addWidget(self.rg,  0,  0,  1,  1)
        bayerLayout.addWidget(self.gr,  0,  1,  1,  1)
        bayerLayout.addWidget(self.gb,  1,  0,  1,  1)
        bayerLayout.addWidget(self.bg,  1,  1,  1,  1)
        bayerGroup.setLayout(bayerLayout)
        
        width_validator = QIntValidator(0,  10000)
        hlayout_1 = QHBoxLayout()
        width_label = QLabel('width:')
        width_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.width_textEdit = QLineEdit()
        self.width_textEdit.setValidator(width_validator)
        hlayout_1.addWidget(width_label,  1)
        hlayout_1.addWidget(self.width_textEdit,  1)
        
        height_validator = QIntValidator(0,  7500,)
        hlayout_2 = QHBoxLayout()
        height_label = QLabel('height:')
        height_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.height_textEdit = QLineEdit()
        self.height_textEdit.setValidator(height_validator)
        hlayout_2.addWidget(height_label,  1)
        hlayout_2.addWidget(self.height_textEdit,  1)
        
        bit_validator = QIntValidator(0,  16)
        hlayout_3 = QHBoxLayout()
        bitDepth_label = QLabel('bit depth:')
        bitDepth_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bitDepth_textEdit = QLineEdit()
        self.bitDepth_textEdit.setValidator(bit_validator)
        hlayout_3.addWidget(bitDepth_label,  1)
        hlayout_3.addWidget(self.bitDepth_textEdit,  1)
        
        hline = QFrame(self)
        hline.setFrameShape(QFrame.HLine)
        
        ok_btn = QPushButton('OK')
        cancel_btn = QPushButton('Cancel')
        hlayout_4 = QHBoxLayout()
        hlayout_4.addStretch(2)
        hlayout_4.addWidget(ok_btn,  1)
        hlayout_4.addWidget(cancel_btn,  1)
        
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(bayerGroup)
        verticalLayout.addLayout(hlayout_1)
        verticalLayout.addLayout(hlayout_2)
        verticalLayout.addLayout(hlayout_3)
        verticalLayout.addWidget(hline)
        verticalLayout.addLayout(hlayout_4)
        verticalLayout.setContentsMargins(50,  20,  50,  20)
        self.setLayout(verticalLayout)
        self.resize(400,  300)
        self.setWindowTitle('raw info')
        ok_btn.clicked.connect(self.on_OK_btn)
        cancel_btn.clicked.connect(self.on_Cancel_btn)
    
    def on_OK_btn(self):
        if self.rg.isChecked():
            self.bayer = 'RG'
        elif self.gr.isChecked():
            self.bayer = 'GR'
        elif self.gb.isChecked():
            self.bayer = 'GB'
        elif self.bg.isChecked():
            self.bayer = 'BG'
        else:
            pass
        self.rawWidth = int(self.width_textEdit.text())
        self.rawHeight = int(self.height_textEdit.text())
        self.bitDepth = int(self.bitDepth_textEdit.text())
        self.accept()
    def on_Cancel_btn(self):
        self.reject()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = RawinfoDlg()
    dlg.show()
    sys.exit(app.exec_())
