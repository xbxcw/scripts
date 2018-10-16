from maya import cmds as mc
import time
import os


class HanScript(object):

    def __init__(self):
       
        name = 'aa'
        if mc.window(name, query=True, exists=True):
            mc.deleteUI(name)
        
        window = mc.window(name)
        self.buildUI()
        mc.showWindow()
        mc.window(window, e=True, resizeToFitChildren=True)
    
    def buildUI(self):
        column = mc.columnLayout()
        mc.frameLayout(label='ss')
        self.progress = mc.progressBar(width=300, step=1)
        mc.button(label='dd', command=self.hSewUvs)
    
    def hSewUvs(self, *args):
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
            mc.progressBar(self.progress, edit=True, step=1, maxValue=len(edges))
        mc.select(b)
        mc.SewUVs()
        mc.select(nodes)


myFolder = 'D:/myFolder/'
folders = os.listdir(myFolder)
textures = []
for folder in folders:
    i = 0
    transforms = []
    obj = myFolder + folder +'/'+ mc.getFileList(folder=myFolder+folder, filespec='*.obj')[0]
    mc.file(obj, i=True, ns='wang%02d' % i)
    geometry = mc.ls(geometry=True)
    mc.hyperShade(a=shader, assign=True)
    shader = mc.shadingNode('blinn', asShader=True)
    file_node=mc.shadingNode('file', asTexture=True)
    mc.setAttr(file_node+'.fileTextureName', 'D:\HKW\danrenzuoyi\sourceimages\Hanjiangfu\T_Cabinet01_B.png', type="string")
    mc.connectAttr('%s.outColor' %file_node, '%s.color' %shader)
    mc.FBXExport('-file', 'C:/Users/HYC/Desktop/aa/'+geometry[0])
    mc.file(new=True, force=True)


shader = mc.shadingNode('blinn', asShader=True)
file_node=mc.shadingNode('file', asTexture=True)
mc.setAttr(file_node+'.fileTextureName', 'D:\HKW\danrenzuoyi\sourceimages\Hanjiangfu\T_Cabinet01_B.png', type="string")
shading_group= mc.sets(renderable=True,noSurfaceShader=True,empty=True)
mc.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)
mc.connectAttr('%s.outColor' %file_node, '%s.color' %shader)