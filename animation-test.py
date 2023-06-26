import sys
from PyQt5.QtCore import QEasingCurve, QRect, QPropertyAnimation, QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class ButtonAnimator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Button Animator")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton("Click Me")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.animate_button)

    def animate_button(self):
        animation = QPropertyAnimation(self.button, b"geometry")
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)

        start_rect = self.button.geometry()
        end_rect = QRect(start_rect.x() + 100, start_rect.y(), start_rect.width(), start_rect.height())

        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)

        animation.start(QPropertyAnimation.DeleteWhenStopped)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    animator = ButtonAnimator()
    animator.show()
    sys.exit(app.exec_())
