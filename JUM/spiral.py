'''
Alexandre Jum - chokram@gmail.com
spiral_1.0.0
'''

import os
import random
import maya.cmds as cmds
try:
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
import UtilsQT


location = os.path.dirname(__file__)


class espiral(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self, parent=UtilsQT.wrapWidget())
        UtilsQT.reloadWidget('makeSpiralWin', self)
        self.ui = UtilsQT.loadUI(location + "/spiral.ui", location, self)
        self.setFixedSize(300, 310)
        self.setWindowTitle("spiral 1.0")

        self.__radius = 0.0
        self.__side = 6
        self.__variation = 0
        self.__circle = ''
        self.__pt_position = []
        self.__path = ''
        self.__quantidade = 0.0
        self.clock = True

    ##########################################################
    #                                                        #
    #                    UI elements                         #
    #                                                        #
    ##########################################################
        
        self.ui.btn_selectPath.clicked.connect(self.getPath)
        self.ui.btn_create.setDisabled(True)
        self.ui.btn_create.clicked.connect(self.create)

    def __makeCircle(self):
        side = self.ui.spin_smooth.value()
        offset = self.ui.spin_offset.value()

        circle = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), degree=1, sections=side)
        cmds.rotate(0,offset,0,circle[0])
        cmds.makeIdentity(circle[0],apply = True, t = True, r = True, s = True, n = 0, pn = True)
        return circle

    def __next(self, porcentagem,circle):
        position = cmds.pointOnCurve(self.ui.ln_path.text(), top=True, pr=porcentagem, position=True)
        tangent  = cmds.pointOnCurve(self.ui.ln_path.text(), top=True, pr=porcentagem, tangent=True)
        angle    = cmds.angleBetween(er=True, v1=(0.0, 1.0, 0.0), v2=tangent)

        cmds.scale((self.ui.spin_radius.value() * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   (self.ui.spin_radius.value() * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   (self.ui.spin_radius.value() * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   circle[0])
        cmds.move(position[0],
                  position[1],
                  position[2],
                  circle[0])
        cmds.rotate(angle[0],
                    angle[1],
                    angle[2],
                    circle[0])


    def __voltas(self):
        steps = self.ui.spin_smooth.value() * float(self.ui.spin_loops.value())
        porcent = 1.0 / steps
        return int(steps), porcent

    def __curve(self):
        cmds.curve(p=self.__pt_position)

    def __espiral(self):
        steps, porcent = self.__voltas()
        increment = porcent

        circle = self.__makeCircle()
        list = []
        if (self.ui.check_inverse.checkState()):
            list = reversed(range(int(steps)))
        else:
            list = range(int(steps))

            self.ui.progress_Create.setRange(0,len(list))
        for i in list:
            self.ui.progress_Create.setValue(i)
            self.__next(porcent,circle)
            porcent += increment
            self.__pt_position.append(cmds.xform(circle[0] + '.cv[' + str(i % self.ui.spin_smooth.value()) + ']',
                                                 q=True,
                                                 ws=True,
                                                 t=True))
        self.ui.progress_Create.reset()
        self.__curve()
        cmds.delete(circle)

    def getPath(self):
        path = cmds.ls(sl = True)
        if path == []:
            self.ui.ln_path.setText('Nothing selected')
            self.ui.btn_create.setDisabled(True)
            self.ui.ln_path.setStyleSheet("background-color: rgb(110, 90, 90);")
        else:
            shape_path = cmds.listRelatives(path[0])
            if (cmds.objectType(shape_path)== 'nurbsCurve'):
                self.ui.ln_path.setText(path[0])
                self.ui.btn_create.setEnabled(True)
                self.ui.ln_path.setStyleSheet("background-color: rgb(90, 150, 50);")
            else:
                self.ui.ln_path.setText('Path not valid')
                self.ui.btn_create.setDisabled(True)
                self.ui.ln_path.setStyleSheet("background-color: rgb(110, 90, 90);")

    def create(self):

        self.__espiral()
        self.__pt_position = []


def run():
    espira = espiral()
    espira.show()

