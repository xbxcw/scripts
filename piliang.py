import maya.cmds as mc
import os
import shenqi1
PATH = mc.workspace(fn=True)+'/'

Names = ['sofa03','table01', 'kettle', 'tea', 'stone', 'sofa02', 'table02', 'wall01', 'cabinet01', 'altar01', 'wall02', 'wall03', 'table03', 'cabinet02', 'decoration01', 'decoration02', 'altar02', 'decoration03', 'decoration04', 'decoration05', 'decoration06', 'decoration07', 'decoration08', 'decoration09', 'candle01', 'candle02', 'tableware', 'door01', 'cabinet03', 'decoration10', 'decoration11']
textures = mc.getFileList(folder=PATH, filespec='*.png')
geometry = mc.ls(sl=True)
# geometry = shenqi1.renamemodel(geometry, name)


def fenli(args, path=None, img=False, mesh=False):
    a = []
    b = []
    c = []
    d = []

    if img is True:
        for i in args:
            b.append(path+i)
            a.append(path+i)
            if len(a)==3:
                c.append(a)
                a = []
            if len(c)==3:
                d.append(c)
                c =[]
        return b, d

    if mesh is True:
        for i in args:
            a.append(i)
            if len(a)==3:
                b.append(a)
                a = []
        b.sort()
        return b

def renamePuls(args, args1, suffix=None, start=None):
    new_geometry = []
    for mesh, name in zip(args, args1):
        print mesh, name
        for i in mesh:
            new_geometry.append(mc.rename(i, start+name+suffix))
    return new_geometry

def renametexturesPuls(args, args1, suffix=None, start=None, path=mc.workspace(fn=True)):

    for texture, name in zip(args, args1):
        for tex in texture:
            for i in tex:
                newName = path + '/' + start + name + suffix + '%d_' %texture.index(tex) + i.split('_', 2)[2]
                os.rename(i, newName)

geometry = fenli(geometry, mesh=True)
texs, textures = fenli(textures, PATH, img=True)
new_geometry = renamePuls(geometry, Names, '_LOD0', 'S_')
renametexturesPuls(textures, Names, 'LOD0', 'T_')