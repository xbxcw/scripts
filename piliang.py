import maya.cmds as mc
import os
import shenqi1


def fenli(args, path=None, img=False, mesh=False):
    a = []
    b = []
    c = []
    d = []

    if img is True:
        for i in args:
            a.append(path + i)
            if len(a) == 3:
                c.append(a)
                a = []
            if len(c) == 3:
                d.append(c)
                c = []
        return d

    if mesh is True:
        for i in args:
            a.append(i)
            if len(a) == 3:
                b.append(a)
                a = []
        b.sort()
        return b


def renamePuls(args, args1, suffix=None, start=None):
    a = []
    b = []
    for mesh, name in zip(args, args1):
        for i in mesh:
            a.append(mc.rename(i, start + name + suffix))
        b.append(a)
        a = []
    return b


def renametexturesPuls(args, args1, suffix=None, start=None, path=mc.workspace(fn=True)):
    a = []
    b = []
    c = []
    d = []
    for texture, name in zip(args, args1):
        for tex in texture:
            for i in tex:
                newName = path + '/' + start + name + suffix + '%d_' % texture.index(tex) + i.split('_', 2)[2]
                os.rename(i, newName)
                a.append(newName)
                d.append(newName)
            b.append(a)
            a = []
        c.append(b)
        b = []
    return d, c


def createPBSPlus(args=None, args1=None, args2=None, ):
    for name, mesh, texture in zip(args, args1, args2):
        name = 'M_' + name + '_LOD0'
        for i in texture:
            num = texture.index(i)
            print i[0]
            print i[1]
            print i[2]
            shader = mc.shadingNode('StingrayPBS', asShader=True, name=name)
            mc.shaderfx(sfxnode=shader, initShaderAttributes=True)
            shading_group = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + 'SG')
            mc.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')

            ao = mc.shadingNode('file', at=True, name=name.replace('M', 'T') + '_AO')
            mc.setAttr(ao + '.fileTextureName', i[0], type='string')

            cm = mc.shadingNode('file', at=True, name=name.replace('M', 'T') + '_B')
            mc.setAttr(cm + '.fileTextureName', i[1], type='string')

            nm = mc.shadingNode('file', at=True, name=name.replace('M', 'T') + '_N')
            mc.setAttr(nm + '.fileTextureName', i[2], type='string')

            # mm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_M')
            # mc.setAttr(mm + '.fileTextureName', i[3], type='string')

            # rm = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_R')
            # mc.setAttr(rm + '.fileTextureName', i[4], type='string')

            # em = mc.shadingNode('file', at=True, name=name.replace('M', 'T')+'_E')
            # mc.setAttr(em + '.fileTextureName', i[5], type='string')
            #
            mc.setAttr(shader + '.use_color_map', 1)
            mc.setAttr(shader + '.use_normal_map', 1)
            # mc.setAttr(shader+'.use_metallic_map', 1)
            # mc.setAttr(shader+'.use_roughness_map', 1)
            # mc.setAttr(shader+'.use_emissive_map', 1)
            mc.setAttr(shader + '.use_ao_map', 1)
            #
            mc.connectAttr(cm + '.outColor', shader + '.TEX_color_map')
            mc.connectAttr(nm + '.outColor', shader + '.TEX_normal_map')
            # # mc.connectAttr(mm+'.outColor', shader+'.TEX_metallic_map')
            # # mc.connectAttr(rm+'.outColor', shader+'.TEX_roughness_map')
            # # mc.connectAttr(em+'.outColor', shader+'.TEX_emissive_map')
            mc.connectAttr(ao + '.outColor', shader + '.TEX_ao_map')
            #
            mc.sets('%s' % mesh[num], e=True, fe='%s' % shading_group)


def exportFbxPlus(args, args1, path=mc.workspace(fn=True) + '/'):
    dir = path + 'FBX'
    if os.path.exists(dir) is False:
        os.makedirs(dir)
    for name, mesh in zip(args, args1):
        mc.select(mesh)
        mc.FBXExport('-file', dir + '/%s' % name, '-s')


Names = ['sofa03', 'table01', 'kettle', 'tea', 'stone', 'sofa02', 'table02', 'wall01', 'cabinet01', 'altar01', 'wall02',
         'wall03', 'table03', 'cabinet02', 'decoration01', 'decoration02', 'altar02', 'decoration03', 'decoration04',
         'decoration05', 'decoration06', 'decoration07', 'decoration08', 'decoration09', 'candle01', 'candle02',
         'tableware', 'door01', 'cabinet03', 'decoration10', 'decoration11']

PATH = mc.workspace(fn=True) + '/'
UNITY_PATH = 'D:/Unity/tt/Assets/'

textures = mc.getFileList(folder=PATH, filespec='*.png')
textures = fenli(textures, PATH, img=True)
texs, textures = renametexturesPuls(textures, Names, 'LOD0', 'T_')
geometry = mc.ls(sl=True)
geometry = fenli(geometry, mesh=True)
geometry = renamePuls(geometry, Names, '_LOD0', 'S_')
createPBSPlus(Names, geometry, textures)
exportFbxPlus(Names, geometry, UNITY_PATH)
shenqi1.moveTextures(texs, UNITY_PATH)
