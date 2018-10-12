from maya import cmds as mc

def test():
    uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
    # xPositions = sorted([mc.polyEditUV(i, query=True)[0] for i in uvs])
    # yPositions = sorted([mc.polyEditUV(i, query=True)[1] for i in uvs])
    a = []
    c = []
    b = {}
    e = {}
    f = 0
    for uv in uvs:
        print uv
        p = mc.polyEditUV(uv, query=True)
        if p not in a:
            b[uv] = 1
            a.append(p)
        else:
            b[uv] = 0
            b[uv] = 1 + b[uv] 

    print b
    for (key, value) in b.items():
        if value > 1:
            print key, value


