import maya.cmds as mc
def tichu():
    edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)
    print edges[0]