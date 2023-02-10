import multiprocessing as mp
import sys
from pathlib import Path
import pygame

import matplotlib
from PySide6.QtGui import QIcon
from PySide6.QtCore import QPropertyAnimation, QPointF, QEasingCurve, QParallelAnimationGroup
import random as rd

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGraphicsOpacityEffect,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLineEdit,
    QVBoxLayout,
)
import math

class EMGEpochDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("orbs number (1, n)")
        vbox = QVBoxLayout(self)
        grid = QGridLayout()
        self.n_orbs = QLineEdit()
        grid.addWidget(self.n_orbs, 0, 1)
        vbox.addLayout(grid)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vbox.addWidget(buttonbox)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        vbox.setSizeConstraint(QVBoxLayout.SetFixedSize)

    def orbs_number(self) -> int:
        n_orbs = self.n_orbs.text()
        try:
            return int(n_orbs) if n_orbs else None
        except Exception as e:
            print(e)
            return None
    def c_speed(self) -> float:
        speed = self.speed.text()
        try:
            return float(speed) if speed else None
        except Exception as e:
            print(e)
            return None
class QPropertyAnimation_(QPropertyAnimation):
    def __init__(self, obj, window, name=b"pos"):
        super().__init__(obj, name, window)
        self.obj = obj
        self.window = window
        self.name = name
        self.sval = QPointF(rd.uniform(100, 600), rd.uniform(100, 600))
        self.not_correct_location = True
        while (self.not_correct_location):
            for orb in self.window.orbs:
                if self.sval != orb.currentValue():
                    d = self.sval - orb.currentValue()
                    norm = math.sqrt(math.pow(d.x(), 2) + math.pow(d.y(), 2))
                    if norm <= 100:
                        self.sval = QPointF(rd.uniform(100, 600), rd.uniform(100, 600))
                        continue
            self.not_correct_location = False
        self.endval = QPointF(rd.uniform(100, 600), rd.uniform(100, 600))
        self.curval = self.sval
        self.d = self.endval - self.sval
        self.setDuration(1500)
        self.norm = math.sqrt(math.pow(self.d.x(), 2) + math.pow(self.d.y(), 2))
        self.norm2 = math.sqrt(math.pow(self.d.x(), 2) + math.pow(self.d.y(), 2))
        self.v = QPointF(self.d.x() / self.norm2, self.d.y() / self.norm2)
        self.setStartValue(self.sval)
        self.setEndValue(self.endval)
        self.setEasingCurve(QEasingCurve.Linear)
        self.curval = self.sval
        self.setLoopCount(100)
    def is_collided(self, left, right):
        x1 = left.currentValue().x()
        y1 = left.currentValue().y()
        x2 = right.currentValue().x()
        y2 = right.currentValue().y()
        d = math.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))
        return d < 100.0
    def currentValue(self) -> QPointF:
        return self.curval
    def setCurrentValue(self, value):
        self.curval = value
    def startValue(self) -> QPointF:
        return self.sval
    def endValue(self) -> QPointF:
        return self.endval
    def setStartValue(self, value) -> None:
        super().setStartValue(self.sval)
    def setEndValue(self, value) -> None:
        super().setEndValue(self.endval)
    def setCurrentValue(self, value):
        self.curval = value
    def move(self, value):
        self.curval += self.v * value
    def setCurrentV(self, value):
        self.v = value
    def currentV(self):
        return self.v
    def updateCurrentValue_p(self):
        super().updateCurrentValue(self.curval)
    def updateCurrentValue(self, value, reflect=None) -> None:
        if reflect:
            norm = math.sqrt(math.pow(reflect.x(), 2) + math.pow(reflect.y(), 2))
            self.v = QPointF(reflect.x() / norm, reflect.y() / norm)
            self.sval = self.currentValue()
            self.setStartValue(None)
            self.endval = self.sval + self.v * self.norm2
            self.setEndValue(None)
        self.curval += self.v * 2.0
        super().updateCurrentValue(self.curval)
        for left in self.window.orbs:
            for right in self.window.orbs:
                if left.currentValue() != right.currentValue():
                    c = right.currentValue() - left.currentValue()
                    norm = math.sqrt(math.pow(c.x(), 2) + math.pow(c.y(), 2))
                    v = QPointF(c.x() / norm, c.y() / norm)
                    if norm <= 100:
                        nv = pygame.math.Vector2(v.x(), v.y())
                        m1 = pygame.math.Vector2(left.currentV().x(), left.currentV().y()).reflect(nv)
                        m2 = pygame.math.Vector2(right.currentV().x(), right.currentV().y()).reflect(nv)
                        left.setCurrentV(QPointF(m1.x, m1.y))
                        right.setCurrentV(QPointF(m2.x, m2.y))
                        left.sval = left.currentValue()
                        left.move(5.0)
                        left.setStartValue(None)
                        left.endval = left.sval + left.v * left.norm2
                        left.setEndValue(None)
                        right.sval = right.currentValue()
                        right.move(5.0)
                        right.setStartValue(None)
                        right.endval = right.sval + right.v * right.norm2
                        right.setEndValue(None)
        if self.currentValue():
            self.c = self.endval - self.curval
            self.norm3 = math.sqrt(math.pow(self.c.x(), 2) + math.pow(self.c.y(), 2))
            if self.norm3 < 1 and self.norm3 != 0.0:
                self.sval = self.curval
                self.setStartValue(None)
                self.endval = self.sval + self.v * self.norm2
                self.setEndValue(None)
            elif self.currentValue() and self.endValue() and ((self.endValue().x() > 900 and self.currentValue().x() > 900) or (self.endValue().x() < 0 and self.currentValue().x() < 0) or (self.endValue().y() > 600 and self.currentValue().y() > 600) or (self.endValue().y() < 0 and self.currentValue().y() < 0)):
                if self.curval.x() > 900.0 or self.curval.x() < 0.0:
                    self.v.setX(-self.v.x())
                if self.curval.y() > 600.0 or self.curval.y() < 0.0:
                    self.v.setY(-self.v.y())
                self.sval = self.curval
                self.setStartValue(None)
                self.endval = self.sval + self.v * self.norm2
                self.setEndValue(None)
class Window(QWidget):
    def __init__(self):
        super().__init__()
        start_dialog = EMGEpochDialog(self)
        if start_dialog.exec():
            self.n_orbs = start_dialog.orbs_number()
        self.resize(1000, 700)
        self.orbs = []
        self.anim_group = QParallelAnimationGroup()
        for _ in range(self.n_orbs):
            self.child = QWidget(self)
            effect = QGraphicsOpacityEffect(self.child)
            self.child.setGraphicsEffect(effect)
            self.child.setStyleSheet("border: 3px solid blue;border-radius: 50px;")
            self.child.resize(100, 100)
            self.anim = QPropertyAnimation_(self.child, self)
            self.orbs.append(self.anim)
            self.anim_group.addAnimation(self.anim)
        self.anim_group.start()
    def anim_group(self):
        return self.anim_group


class Model:
    """Data model for MNELAB."""
    def __init__(self):
        self.view = None  # current view


__version__ = "0.9.0.dev0"


def main():
    mp.set_start_method("spawn", force=True)  # required for Linux
    app_name = "MNELAB"
    if sys.platform.startswith("darwin"):
        # set bundle name on macOS (app name shown in the menu bar)
        # this must be done before the app is created
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        info["CFBundleName"] = app_name

    matplotlib.use("QtAgg")
    app = QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setOrganizationName("cbrnr")
    if sys.platform.startswith("darwin"):
        app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
        app.setWindowIcon(QIcon(f"{Path(__file__).parent}/icons/mnelab-logo-macos.svg"))
    else:
        app.setWindowIcon(QIcon(f"{Path(__file__).parent}/icons/mnelab-logo.svg"))
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    model = Model()
    model.view = Window()
    if len(sys.argv) > 1:  # open files from command line arguments
        for f in sys.argv[1:]:
            model.load(f)
    model.view.show()
    sys.exit(app.exec())
