#  _*_ encoding=utf-8 _*_
import sys
from PyQt5.QtWidgets import QDialog,  QGroupBox,  QHBoxLayout,  QVBoxLayout,  QGridLayout,  QRadioButton,  \
QApplication,  QLabel,  QLineEdit,  QSizePolicy
from PyQt5.QtCore import Qt
class RawinfoDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        bayerGroup = QGroupBox('bayer')
        bayerLayout = QGridLayout()
        rg = QRadioButton('RG',  bayerGroup)
        gr = QRadioButton('GR',  bayerGroup)
        gb = QRadioButton('GB',  bayerGroup)
        bg = QRadioButton('BG',  bayerGroup)
        bayerLayout.addWidget(rg,  0,  0,  1,  1)
        bayerLayout.addWidget(gr,  0,  1,  1,  1)
        bayerLayout.addWidget(gb,  1,  0,  1,  1)
        bayerLayout.addWidget(bg,  1,  1,  1,  1)
        bayerGroup.setLayout(bayerLayout)
        
        hlayout_1 = QHBoxLayout()
        width_label = QLabel('width:')
        width_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        width_textEdit = QLineEdit()
        width_textEdit.setSizePolicy(QSizePolicy.Preferred,  QSizePolicy.Fixed)
        hlayout_1.addWidget(width_label,  1)
        hlayout_1.addWidget(width_textEdit,  1)
        
        hlayout_2 = QHBoxLayout()
        height_label = QLabel('height:')
        height_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        height_textEdit = QLineEdit()

        hlayout_2.addWidget(height_label,  1)
        hlayout_2.addWidget(height_textEdit,  1)
        
        hlayout_3 = QHBoxLayout()
        bitDepth_label = QLabel('bit depth:')
        bitDepth_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bitDepth_textEdit = QLineEdit()

        hlayout_3.addWidget(bitDepth_label,  1)
        hlayout_3.addWidget(bitDepth_textEdit,  1)
        
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(bayerGroup)
        verticalLayout.addLayout(hlayout_1)
        verticalLayout.addLayout(hlayout_2)
        verticalLayout.addLayout(hlayout_3)
        self.setLayout(verticalLayout)
#        self.resize(400,  300)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = RawinfoDlg()
    dlg.show()
    sys.exit(app.exec_())
