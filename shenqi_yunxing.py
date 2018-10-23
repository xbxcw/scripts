import shenqi1
import maya.cmds as mc

reload(shenqi1)



PATH = mc.workspace(fn=True) + '/'
UNITY_PATH = 'D:/Unity/tt/Assets/'

geometry = mc.ls(sl=True)
name = 'sofa'
geometry = shenqi1.renamemodel(geometry, name)
print geometry
shenqi1.renametextures(name)
textures = mc.getFileList(folder=PATH, filespec='*.png')
num = 0
a = []
tex = []
imgs = []
for i in textures:
    b = PATH + i
    imgs.append(b)    
    a.append(b)
    if len(a)%3 == 0 and len(a) != 0:
        tex.append(a)
        
        a = []
shenqi1.createPBS(name, 3, tex, geometry)
shenqi1.exportFbx(UNITY_PATH, name, geometry)
shenqi1.moveTextures(imgs,UNITY_PATH)