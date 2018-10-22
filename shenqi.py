import os
from maya import cmds as mc
import time

myFolder = 'D:/myFolder/'
folders = os.listdir(myFolder)
bb = len(folders)
name = '����'
if mc.window(name, query=True, exists=True):
    mc.deleteUI(name)

window = mc.window(name)
column = mc.columnLayout()


mc.frameLayout(label='����������')
progress = mc.progressBar(width=300, step=1)
mc.showWindow()


textures = []
i = 1
for folder in folders:
    
    name = '����'
    if mc.window(name, query=True, exists=True):
        mc.deleteUI(name)
    
    window = mc.window(name)
    column = mc.columnLayout()
    
    
    mc.frameLayout(label='����������: ��������%d/%d' % (i,len(folders)))
    progress = mc.progressBar(width=300, step=1)
    mc.showWindow()


    # ��ͼ
    textures = os.listdir(myFolder + folder +'/Textures/')
    textures.sort()
    print textures
    diffuse = myFolder + folder + '/Textures/' + textures[1]  # ��ɫ
    normal = myFolder + folder + '/Textures/' + textures[2]  # ����
    print diffuse, normal
    
    
    
    # �����򲿷�
    shader = mc.shadingNode('blinn', asShader=True)  # ������
    nodeColor = mc.shadingNode('file', asTexture=True)  # ��ɫ��ͼ
    nodeNormal = mc.shadingNode('file', asTexture=True)  # ������ͼ
    nodeBump = mc.shadingNode('bump2d', asTexture=True)
    mc.setAttr(nodeColor+'.fileTextureName', diffuse, type="string")  # �����ɫ��ͼ
    mc.setAttr(nodeNormal+'.fileTextureName', normal, type="string")  # ��ӷ�����ͼ
    mc.setAttr(nodeNormal+'.colorSpace', 'Raw', type='string')
    mc.setAttr(nodeBump+'.bumpInterp', 1)
    mc.connectAttr('%s.outAlpha' %nodeNormal, '%s.bumpValue' %nodeBump)  # �����������bump
    mc.connectAttr('%s.outNormal' %nodeBump, '%s.normalCamera' %shader)  # ��bump�����������
    mc.connectAttr('%s.outColor' %nodeColor, '%s.color' %shader)  # ��ͼƬ�����������
    
    
    # ģ�Ͳ���
    obj = myFolder + folder +'/'+ mc.getFileList(folder=myFolder+folder, filespec='*.obj')[0]  # ��ȡģ���ļ�
    mc.file(obj, i=True, ns='wang%02d' % i)  # ����ģ��
    geometry = mc.ls(geometry=True)  # ѡ��ģ��
    mc.select(geometry[0])
    print geometry
    mc.hyperShade(a=shader, assign=True)  # �������
    
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

    mc.FBXExport('-file', 'C:/Users/Intime/Desktop/aa/a%d' %i)  # ����ģ��



    mc.file(new=True, force=True)  # ˢ�³���
    
    i += 1
    bb -= 1