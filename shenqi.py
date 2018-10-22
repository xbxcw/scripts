import os
from maya import cmds as mc
import time

myFolder = 'D:/myFolder/'
folders = os.listdir(myFolder)
bb = len(folders)
name = '神器'
if mc.window(name, query=True, exists=True):
    mc.deleteUI(name)

window = mc.window(name)
column = mc.columnLayout()


mc.frameLayout(label='神器进度条')
progress = mc.progressBar(width=300, step=1)
mc.showWindow()


textures = []
i = 1
for folder in folders:
    
    name = '神器'
    if mc.window(name, query=True, exists=True):
        mc.deleteUI(name)
    
    window = mc.window(name)
    column = mc.columnLayout()
    
    
    mc.frameLayout(label='神器进度条: 正在生成%d/%d' % (i,len(folders)))
    progress = mc.progressBar(width=300, step=1)
    mc.showWindow()


    # 贴图
    textures = os.listdir(myFolder + folder +'/Textures/')
    textures.sort()
    print textures
    diffuse = myFolder + folder + '/Textures/' + textures[1]  # 颜色
    normal = myFolder + folder + '/Textures/' + textures[2]  # 法线
    print diffuse, normal
    
    
    
    # 材质球部分
    shader = mc.shadingNode('blinn', asShader=True)  # 材质球
    nodeColor = mc.shadingNode('file', asTexture=True)  # 颜色贴图
    nodeNormal = mc.shadingNode('file', asTexture=True)  # 法线贴图
    nodeBump = mc.shadingNode('bump2d', asTexture=True)
    mc.setAttr(nodeColor+'.fileTextureName', diffuse, type="string")  # 添加颜色贴图
    mc.setAttr(nodeNormal+'.fileTextureName', normal, type="string")  # 添加法线贴图
    mc.setAttr(nodeNormal+'.colorSpace', 'Raw', type='string')
    mc.setAttr(nodeBump+'.bumpInterp', 1)
    mc.connectAttr('%s.outAlpha' %nodeNormal, '%s.bumpValue' %nodeBump)  # 将法线输出给bump
    mc.connectAttr('%s.outNormal' %nodeBump, '%s.normalCamera' %shader)  # 将bump输出给材质球
    mc.connectAttr('%s.outColor' %nodeColor, '%s.color' %shader)  # 将图片输出给材质球
    
    
    # 模型部分
    obj = myFolder + folder +'/'+ mc.getFileList(folder=myFolder+folder, filespec='*.obj')[0]  # 获取模型文件
    mc.file(obj, i=True, ns='wang%02d' % i)  # 导入模型
    geometry = mc.ls(geometry=True)  # 选择模型
    mc.select(geometry[0])
    print geometry
    mc.hyperShade(a=shader, assign=True)  # 赋予材质
    
    mc.select(mc.listRelatives(mc.ls(geometry=True), p=True, path=True), r=True)
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
        mc.progressBar(progress, edit=True, step=1, maxValue=len(edges))        
    mc.select(b)
    mc.SewUVs()

    mc.FBXExport('-file', 'C:/Users/Intime/Desktop/aa/a%d' %i)  # 导出模型



    mc.file(new=True, force=True)  # 刷新场景
    
    i += 1
    bb -= 1