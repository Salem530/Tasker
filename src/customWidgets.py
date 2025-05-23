"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMouseEvent
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton, 
    QSizePolicy,
    QVBoxLayout,
    QWidget
)
# Locals importations
from themes import applyCTheme

class AppLogo(QFrame):
    """ 
    Custom widget that represents the application's title for
    custom titlte bar, it allows the user to move the main window by 
    dragging it.
    
    Attributes:
        title (QLabel): The app title
        _old_pos (QPoint | None): Stores the last known mouse position 
                                  for window movement.
    """

    def __init__(self, parent: QMainWindow, title : str) -> None:
        """
        Initializes the title widget with an image and enables window dragging.

        Args:
            parent (QMainWindow): The main application window.
            title (str): The app title text.
        """
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("CAppLogo")
        self.setFixedHeight(50)
        self.layout = QHBoxLayout(self)
        self.title = QLabel(f"<h1>{title}</h1>", self) # Create the title label
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter) # Add the to the layout
        # Store the last known position of the mouse (None when idle)
        self._old_pos: QPoint | None = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Captures the mouse position when the user presses the left button.

        Args:
            event (QMouseEvent): The mouse event containing position data.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPos()  # Store initial position

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Moves the application window when the user drags the logo.

        Args:
            event (QMouseEvent): The mouse movement event.
        """
        if self._old_pos is not None:
            # Calculate the movement delta (difference between old and new position)
            delta: QPoint = event.globalPos() - self._old_pos
            
            # Move the main window to the new position
            self.window().move(self.window().pos() + delta)
            
            # Update the stored position for smooth movement
            self._old_pos = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Resets the stored position when the user releases the mouse button.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        self._old_pos = None  # Reset the stored position

class CustomTitleBar(QFrame):
    """ 
    Custom title bar for the application.
    
    Attributes:
        appLogo (AppLogo) : The dragable zone widget. 
        minimizeBtn (QPushButton) : The button to minimize the window.
        toogleMaximizeBtn (QPushButton) : The button to maximize or set the window normal.
        closeBtn (QPushButton) : The button to close the window.

        resizeIcon (QIcon) : The toogleMaximizeBtn icon.
        maximizeIcon (QIcon) : The toogleMaximizeBtn icon.
        layout (QHBoxLayout) : The layout to place buttons.
    """
    def __init__(self, parent : QMainWindow, title : str) -> None:
        """
        Create a instance of the CustomTitleBar for the given parent window.

        Args:
            parent (QMainWindow): The object window parent.
            title (str): The title for the app logo. 
        """
        super().__init__(parent)
        parent.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.setObjectName("CTitleBar")
        self.setStyleSheet(applyCTheme())
        self.layout = QHBoxLayout(self)

        # Create the dragable zone
        self.appLogo = AppLogo(self, title)
        self.appLogo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding) # Expland this
        self.layout.addWidget(self.appLogo)
        # Create the dragable zone
        self.btnFrame = QFrame(self)
        self.layout.addWidget(self.btnFrame)
        # Create minimize button
        self.minimizeBtn = QPushButton("", self.btnFrame)
        self.minimizeBtn.setIcon(QIcon("ressources\\icons\\minimize.png"))
        self.minimizeBtn.setFixedSize(35, 35)
        self.minimizeBtn.clicked.connect(self.window().showMinimized)
        self.minimizeBtn.setToolTip("Minimize window")
        # Create toogle minisize and maximize button
        self.toogleMaximizeBtn = QPushButton("", self.btnFrame)
        self.resizeIcon = QIcon("ressources\\icons\\resize.png")
        self.maximizeIcon = QIcon("ressources\\icons\\maximize.png")
        self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
        self.toogleMaximizeBtn.setFixedSize(35, 35)
        self.toogleMaximizeBtn.setToolTip("Toogle maximize")
        self.toogleMaximizeBtn.clicked.connect(self.toogleMaximize)
        # Create close button
        self.closeBtn = QPushButton("", self.btnFrame)
        self.closeBtn.setIcon(QIcon("ressources\\icons\\cross.png"))
        self.closeBtn.setObjectName("CloseBtn")
        self.closeBtn.setFixedSize(35, 35)
        self.closeBtn.clicked.connect(self.window().close)
        self.closeBtn.setToolTip("Close app")
        # Add buttons to the layout
        for btn in [self.minimizeBtn, self.toogleMaximizeBtn, self.closeBtn]:
            self.layout.addWidget(btn)        

    # Toogle maximize command
    def toogleMaximize(self) -> None:
        """
        Toogle parent window maximed or normal.

        Args: No args
        """
        if self.window().isMaximized():
            self.toogleMaximizeBtn.setToolTip("Toogle maximize")
            self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
            self.window().showNormal()
        else:
            self.toogleMaximizeBtn.setToolTip("Toogle minimize")
            self.toogleMaximizeBtn.setIcon(self.resizeIcon)
            self.window().showMaximized()

class SideBar(QFrame):
    """
    Sidebar widget with navigation buttons and sliding animation.
    """

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setFixedWidth(60)
        self.setMaximumWidth(60)
        self.setMinimumWidth(0)

        self.setObjectName("CSideBar")
        self.setStyleSheet(applyCTheme())
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        buttons = {
            "Close side bar": ["ressources\\icons\\left.png", "ctrl+shift+t"],
            "Show task lists": ["ressources\\icons\\tasklists.png", "ctrl+shift+e"],
            "Add task list": ["ressources\\icons\\new_tasklist.png", "ctrl+shift+n"],
            "Settings": ["ressources\\icons\\settings.png", "ctrl+shift+s"],
        }
        self.buttons : dict[str, QPushButton] = dict()

        for name, value in buttons.items():
            btn = QPushButton("", self)
            btn.setIcon(QIcon(value[0]))
            btn.setFixedSize(50, 50)
            btn.setShortcut(value[1])
            btn.setToolTip(f"{name} ({btn.shortcut().toString()})")

            if name == "Close side bar":
                btn.clicked.connect(self.toggleSidebar)
                

            self.layout.addWidget(btn)
            self.buttons[name] = btn

        # Animation for sidebar
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 300ms animation speed

    def toggleSidebar(self) -> None:
        """
        Slide the sidebar in or out using width animation (layout-friendly).
        """
        target_width = 0 if self.width() > 30 else 60
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.start()

class SectionTitle(QWidget):
    def __init__(self, text: str):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setObjectName("SectionTitle")
        self.setStyleSheet(applyCTheme())
        label = QLabel(text.upper())
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedSize(90, 8)
        line.setObjectName("line")
        layout.addWidget(label)
        layout.addWidget(line)