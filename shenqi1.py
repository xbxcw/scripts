import os
from maya import cmds as mc
import time

path = mc.workspace(fn=True) + '/'

def createPBS(name='a', num=1, textures=None):
    name = 'M_' + name + '_LOD%d' %num
    for i in range(num):
        shader = mc.shadingNode('StingrayPBS', asShader=True, name=name)
        mc.shaderfx(sfxnode=shader, initShaderAttributes=True)
        shading_group= mc.sets(renderable=True,noSurfaceShader=True,empty=True,name=name+'SG')
        mc.connectAttr(shader+'.outColor', shading_group+'.surfaceShader')

        ao = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_AO')
        mc.setAttr(ao+'.fileTextureName', textures[i][0], type='string')

        cm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_B')
        mc.setAttr(cm+'.fileTextureName', textures[i][1], type='string')

        nm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_N')
        mc.setAttr(nm+'.fileTextureName', textures[i][2], type='string')

        # mm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_M')
        # mc.setAttr(mm+'.fileTextureName', textures[3][i], type='string')

        # rm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_R')
        # mc.setAttr(rm+'.fileTextureName', textures[4][i], type='string')

        # em = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_E')
        # mc.setAttr(em+'.fileTextureName', textures[5][i], type='string')


        mc.setAttr(shader+'.use_color_map', 1)
        mc.setAttr(shader+'.use_normal_map', 1)
        # mc.setAttr(shader+'.use_metallic_map', 1)
        # mc.setAttr(shader+'.use_roughness_map', 1)
        # mc.setAttr(shader+'.use_emissive_map', 1)
        mc.setAttr(shader+'.use_ao_map', 1)

        mc.connectAttr(cm+'.outColor', shader+'.TEX_color_map')
        mc.connectAttr(nm+'.outColor', shader+'.TEX_normal_map')
        # mc.connectAttr(mm+'.outColor', shader+'.TEX_metallic_map')
        # mc.connectAttr(rm+'.outColor', shader+'.TEX_roughness_map')
        # mc.connectAttr(em+'.outColor', shader+'.TEX_emissive_map')
        mc.connectAttr(ao+'.outColor', shader+'.TEX_ao_map')


geometry = mc.ls(sl=True)

def renamemodel(geometry, name='a'):
    
    for i in geometry:

        mc.rename(i, name+'_LOD0')

def renametextures(name='a'):
    
    textures = mc.getFileList(folder=path, filespec='*.png')
    num = 0
    tex = []
    for i in textures:
        if textures.index(i) % 3 == 0 and textures.index(i) != 0:
            num += 1
        a = path + i

        b = path + 'T_' + name + '_LOD%d' %num + '_' + a.split('_', 2)[2]

        tex.append(b)
        
        os.rename(a, b)




if __name__ == '__main__':
    path = mc.workspace(fn=True) + '/'
    name = 'sofa'
    # renamemodel(geometry, name)
    # renametextures(name)
    textures = mc.getFileList(folder=path, filespec='*.png')
    num = 0
    a = []
    tex = []
    for i in textures:            
        b = path + i
        print b
        
        a.append(b)
        if len(a)%3 == 0 and len(a) != 0:
            tex.append(a)
            
            a = []
    createPBS('a', 1, tex)