"""
    The app module for manage application, for make basic app functions such as : 
    - adding task
    - create task list
    - load and set stylesheets for widgets

    This an opensource code made by [SalemMalola](https://github.com/SalemMalola)
"""
# Depencies importations
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)
# Locals importations
from customWidgets import CustomTitleBar, loadStyleSheet

class Tasker(QMainWindow):
    """The app manager"""
    def __init__(self):
        self.qtApplication = QApplication([])
        super().__init__()
        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle("Tasker")
        self.setStyleSheet(loadStyleSheet("style"))
        # Central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # Main layout
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Title bar
        self.titleBar = CustomTitleBar(self)
        self.layout.addWidget(self.titleBar, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

    def mainLoop(self) -> None:
        self.show()
        self.qtApplication.exec_()