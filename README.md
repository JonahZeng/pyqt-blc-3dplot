# pyqt5-blc-3dplot
------------------------
## user guide
* 启动程序，主界面打开：

![main window](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/1.PNG?raw=true)

* 打开准备好的遮黑状态下拍摄的raw文件，可以打开单张，也可以多张，多张情况下，工具内部将会把多张raw累加起来平均；
**注意**，raw文件名必须带有`_ISO_200_`的部分，否则报错；多张raw情况下，文件名中的ISO和文件大小必须一致，否则不能通过内部检查；
点击打开菜单：

![open raw](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/2.png?raw=true)

在弹出的文件对话框中选择raw文件：

![open multi-raw](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/3.jpg?raw=true)

* 选择的raw通过内部条件检查以后，会弹出raw info对话框：

![rawinfo](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/4.png?raw=true)

需手动完成bayer模式，raw长宽，bit位宽等输入，然后点击ok按钮；
**对于2个字节为单位，且长宽比例为4:3的raw，工具将自动计算出长宽**

* 工具开始进行计算，稍等片刻后显示3d图示：

![result](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/5_downscale.jpg?raw=true)

用户可按住鼠标左键拖动3d图，调整视角，点击底部工具栏上的按钮进行保存，放大，间距设置等等操作不一而足；
tips:**底部工具栏是python绘图库matplotlib的标准工具条**

* 获取标定数据：
点击上一步中的***show blc data***按钮，即可弹出数据对话框：

![blc data](https://github.com/JonahZeng/pyqt-blc-3dplot/blob/master/tutorial_img/6.png?raw=true)

用户可自由调整精度，鼠标右键复制出来即可
