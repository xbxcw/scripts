from maya import cmds as mc
import time

# time_start=time.time()
# nodes = mc.ls(sl=True)
# edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)

# window = cmds.window('王大锤')
# cmds.columnLayout()
# progressControl = cmds.progressBar(maxValue=len(edges), width=300)

# cmds.showWindow( window )
# print len(edges)
# a = []
# b = []
# for edge in edges:
#     mc.select(edge)
#     uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
#     for uv in uvs:
#         p = mc.polyEditUV(uv, query=True)
#         a.append(p)
#     if len(a) == 4:

#         if a[0] == a[1] and a[2] == a[3]:
#             b.append(edge)
#         elif a[0] == a[2] and a[1] == a[3]:
#             b.append(edge)
#         elif a[0] == a[3] and a[1] == a[2]:
#             b.append(edge)
#     a = []
#     cmds.progressBar(progressControl, edit=True, step=1)
# print b

# mc.select(b)
# mc.SewUVs()
# cmds.progressBar(progressControl, edit=True, step=1)
# cmds.deleteUI('王大锤')
# mc.select(b)
# mc.select(nodes)
# time_end=time.time()

# print '%.2fs' % (time_end - time_start)
# # mc.ConvertSelectionToContainedEdges()


class HanScript(object):

    def __init__(self):
       
        name = '减面'
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name)
        
        window = cmds.window(name)
        self.buildUI()
        cmds.showWindow()
        cmds.window(window, e=True, resizeToFitChildren=True)
    
    def buildUI(self):
        column = cmds.columnLayout()
        cmds.frameLayout(label='等待完成……')
        progressControl = cmds.progressBar(maxValue=1, width=300)
        createIconButton(label='缝合')
    
    def hSewUvs(self):
        nodes = mc.ls(sl=True)
        edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)
        a = []
        b = []
        for edge in edges:
            mc.select(edge)
            uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
            for uv in uvs:
                p = mc.polyEditUV(uv, query=True)
                a.append(p)
            if len(a) == 4:

                if a[0] == a[1] and a[2] == a[3]:
                    b.append(edge)
                elif a[0] == a[2] and a[1] == a[3]:
                    b.append(edge)
                elif a[0] == a[3] and a[1] == a[2]:
                    b.append(edge)
            a = []
            cmds.progressBar(progressControl, edit=True, step=1/len(edges))
        mc.select(b)
        mc.SewUVs()
        cmds.progressBar(progressControl, edit=True, step=-1)
        mc.select(nodes)