'''
Alexandre Jum - chokram@gmail.com
braid_1.0.0
'''

import os
import UtilsQT
try:
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
import random
import maya.cmds as cmds


location = os.path.dirname(__file__)


class espiral(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self, UtilsQT.wrapWidget())
        UtilsQT.reloadWidget('makeBraidWin', self)
        self.ui = UtilsQT.loadUI(location + "/braid.ui", location, self)
        self.setFixedSize(300, 310)
        self.setWindowTitle("braid 1.0")

        self.__radius = 0.0
        self.__side = 6
        self.__variation = 0
        self.__circle = ''
        self.__pt_position_A = []
        self.__pt_position_B = []
        self.__pt_position_C = []
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

    def __makeEight(self):
        side = 16
        offset = self.ui.spin_offset.value()

        eight = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), degree=3, sections=side)
        cmds.select(eight[0])
        lattice = cmds.lattice(dv = (3, 2, 3), objectCentered  = True )
        cmds.setAttr(lattice[0]+'.local', 0)


        cmds.select(lattice[1]+'.pt[2][0:1][0]',lattice[1]+'.pt[2][0:1][1]',lattice[1]+'.pt[2][0:1][2]')
        cmds.scale(1, 1, -1, pivot = (1.108194, 0 , 0), relative = True)
        cmds.select(lattice[1]+'.pt[1][0:1][0]',lattice[1]+'.pt[1][0:1][1]',lattice[1]+'.pt[1][0:1][2]')
        cmds.scale(0, 0, 0, pivot = (0, 0 , 0), relative = True)
        cmds.select(lattice[1]+'.pt[0][0:1][0]',lattice[1]+'.pt[2][0:1][2]',lattice[1]+'.pt[2][0:1][0]',lattice[1]+'.pt[0][0:1][2]')

        cmds.scale(1, 1, 1.455556, pivot = (0, 0 , 0), relative = True)
        cmds.scale(0.929167, 1, 1, pivot = (0, 0 , 0), relative = True)

        cmds.select(eight[0])
        cmds.delete(ch = True)


        cmds.rotate(0,offset,0,eight[0])
        cmds.makeIdentity(eight[0],apply = True, t = True, r = True, s = True, n = 0, pn = True)
        return eight

    def __next(self, porcentagem,eight,scale):
        #print porcentagem
        curva = self.ui.ln_path.text()

        position = cmds.pointOnCurve(curva, top=True, pr=porcentagem, position=True)
        tangent  = cmds.pointOnCurve(curva, top=True, pr=porcentagem, tangent=True)
        angle    = cmds.angleBetween(er=True, v1=(0.0, 1.0, 0.0), v2=tangent)

        cmds.scale((scale * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   (scale * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   (scale * random.uniform((1-self.ui.spin_random.value()), 1.0)),
                   eight[0])
        cmds.move(position[0],
                  position[1],
                  position[2],
                  eight[0])
        cmds.rotate(angle[0],
                    angle[1],
                    angle[2],
                    eight[0])


    def __voltas(self):
        steps = 16 * float(self.ui.spin_loops.value())
        porcent = 1.0 / steps
        return int(steps), porcent

    def __makeMesh(self,curva):
        scale_0 = self.ui.spin_radius.value()
        scale_1 = self.ui.spin_radius_1.value()
        scale = self.ui.spin_radius.value()
        if (scale_0 >= scale_1):
            tempMaior = scale_0
            tempMenor = scale_1
        else:
            tempMaior = scale_1
            tempMenor = scale_0

        scale_extrude = tempMenor/tempMaior

        position = cmds.pointOnCurve(curva, top=True, pr=0, position=True)
        tangent  = cmds.pointOnCurve(curva, top=True, pr=0, normalizedTangent=True)
        angle    = cmds.angleBetween(er=True, v1=(0.0, 1.0, 0.0), v2=tangent)

        circle = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), degree=3, sections=16, r = 0.5)
        cmds.scale(tempMaior,
                   tempMaior,
                   tempMaior,
                   circle[0])
        cmds.move(position[0],
                  position[1],
                  position[2],
                  circle[0])
        cmds.rotate(angle[0],
                    angle[1],
                    angle[2],
                    circle[0])


        extrude = cmds.extrude(circle[0],
                                curva,
                                constructionHistory = True,
                                range = True,
                                polygon = 0,
                                extrudeType = 2,
                                useComponentPivot = 0,
                                fixedPath = 0,
                                useProfileNormal = 1,
                                rotation = 0,
                                scale = scale_extrude,
                                reverseSurfaceIfPathReversed = 1)


        poly = cmds.nurbsToPoly(extrude[0], matchNormalDir = True, constructionHistory = False, format = 2, polygonType = 1, uType = 3, uNumber = 1, vType = 3, vNumber = 3)

        cmds.delete(circle, extrude[0])
        print poly
        return poly

    def __curve(self):
        curve_A = cmds.curve(p=self.__pt_position_A)
        curve_B = cmds.curve(p=self.__pt_position_B)
        curve_C = cmds.curve(p=self.__pt_position_C)

        if (self.ui.btn_makeMesh.isChecked()):
            mesh_A = self.__makeMesh(curve_A)
            mesh_B = self.__makeMesh(curve_B)
            mesh_C = self.__makeMesh(curve_C)
            cmds.delete(curve_A, curve_B, curve_C)
            cmds.select(mesh_A,mesh_B,mesh_C)
        else:
            cmds.select(curve_A,curve_B,curve_C)

    def __braid(self):
        steps, porcent = self.__voltas()
        increment = porcent

        eight = self.__makeEight()

        list = range(int(steps))
        offset = self.ui.spin_offset.value()
        offset_normalize = offset/360.0
        self.ui.progress_Create.setRange(0,len(list))

        scale_0 = self.ui.spin_radius.value()
        scale_1 = self.ui.spin_radius_1.value()
        if (scale_0 >= scale_1):
            scale_maior = scale_0
            scale_menor = scale_1
        else:
            scale_maior = scale_1
            scale_menor = scale_0

        diference = scale_maior-scale_menor
        percent = diference/steps
        scale = scale_maior

        if (self.ui.btn_reverse.isChecked()):
            curva = self.ui.ln_path.text()
            cmds.reverseCurve(curva,ch = False, replaceOriginal = True)


        for i in list:
            self.ui.progress_Create.setValue(i)
            self.__next(porcent,eight,scale)

            porcent += increment

            _pos_A = (i*0.0625)%1.0 + offset_normalize
            _pos_B = (i*0.0625+0.333333)%1.0 + offset_normalize
            _pos_C = (i*0.0625+0.666666666)%1.0 + offset_normalize

            self.__pt_position_A.append(cmds.pointOnCurve( eight[0],top = True, pr= _pos_A, p=True ))
            self.__pt_position_B.append(cmds.pointOnCurve( eight[0],top = True, pr= _pos_B, p=True ))
            self.__pt_position_C.append(cmds.pointOnCurve( eight[0],top = True, pr= _pos_C, p=True ))
            scale -= percent


        self.ui.progress_Create.reset()
        #cmds.delete(self.__circle[0])
        # return self.__pt_position
        self.__curve()
        cmds.delete(eight[0])

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

        self.__braid()

        self.__pt_position_A = []
        self.__pt_position_B = []
        self.__pt_position_C = []


def run():
    espira = espiral()
    espira.show()

