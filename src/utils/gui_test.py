from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPoint, QSize
import sys

class DraggableLabel(QLabel):
    def __init__(self, gif_path):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Load and resize GIF
        movie = QMovie(gif_path)
        movie.setScaledSize(QSize(200, 185))  # Adjust GIF size as needed
        self.setMovie(movie)
        movie.start()

        # Resize window
        self.resize(200, 155)  # Match the resized GIF dimensions

        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

app = QApplication(sys.argv)
label = DraggableLabel("ai.gif")
label.show()
sys.exit(app.exec_())
