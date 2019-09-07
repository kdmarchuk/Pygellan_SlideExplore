

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QHeaderView
from PyQt5.QtCore import pyqtSlot
from SlideROIs_ui import Ui_MainWindow

class ROIsMap(QMainWindow):
    def __init__(self,slide):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.slideROIs_graphicsView.ui.menuBtn.hide()
        self._ui.slideROIs_graphicsView.ui.histogram.hide()
        self._ui.slideROIs_graphicsView.ui.roiBtn.hide()
        self._ui.slideROIs_graphicsView.view.setAspectLocked()

        self._ui.close_pushButton.clicked.connect(self.close)

        self._ui.slideROIs_graphicsView.view.addItem(slide.slideBase)



