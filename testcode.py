from maya import cmds as mc
import time
import threading

def test():
<<<<<<< Updated upstream
    time_start=time.time()
    edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)
    a = []
    b = []
    for edge in edges:
        mc.select(edge)
        uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
        for uv in uvs:
            p = mc.polyEditUV(uv, query=True)
            a.append(p)
            print a
        if a[0] == a[1] and a[2] == a[3]:
            b.append(edge)
        elif a[0] == a[2] and a[1] == a[3]:
            b.append(edge)
        elif a[0] == a[3] and a[1] == a[2]:
            b.append(edge)
        a = []
    print b
    


    mc.select(b)
    mc.polyMapSewMove()
    time_end=time.time()
    print '%.2fs' % (time_end - time_start)
    # mc.ConvertSelectionToContainedEdges()

def test1():
    time_start=time.time()
    edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)
    print len(edges)
    a = []
    b = []
    for edge in edges:
        mc.select(edge)
        uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
        for uv in uvs:
            p = mc.polyEditUV(uv, query=True)
            a.append(p)
            print a

        if (a[0] == a[1] and a[2] == a[3]) or (a[0] == a[2] and 
            a[1] == a[3]) or (a[0] == a[3] and a[1] == a[2]):
            b.append(edge)

        a = []
    print b
    


    mc.select(b)
    mc.polyMapSewMove()
    time_end=time.time()
    print '%.2fs' % (time_end - time_start)
    # mc.ConvertSelectionToContainedEdges()
=======
    uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
    a = []
    b = {}
    c = []
    print len(uvs)

    num = 0
    listnum = [] 
    
    for uv in uvs:
        p = mc.polyEditUV(uv, query=True)
        num += 1
        listnum.append(p)

        if num == 4:
            if listnum[0] == listnum[1] or listnum[0] == listnum[2] or listnum[0] == listnum[3]:
                num = 0
                for temp in listnum:
                    c.append(temp)
                listnum = []
                
        
        
    







    # for (key, value) in b.items():
    #     wang = 0

    #     for i in b.values():
>>>>>>> Stashed changes

    #         if i == value:
    #             wang += 1
    #         if wang == 2:
    #             a.append(key)
    #             break
    # # for (key, value) in b.items():
    # #     temp = value
    # #     print temp
    # #     if value in c:
    # #         a.append(key)
    # # print c
    mc.select(c)
    # mc.ConvertSelectionToContainedEdges()
    # # mc.SewUVs()
    # # mc.ConvertSelectionToUVs()