from maya import cmds as mc

import time
import threading
 
b = []
NumberTime = 0  
b1 = True
b2 = True

def ThreadJob1(edges):
    a = []
    print len(edges)
    for edge in edges:
        mc.select(edge)
        uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
        for uv in uvs:
           p = mc.polyEditUV(uv, query=True)
           a.append(p)

def ThreadJob2(edges):
    b = []
    print len(edges)
    for edge in edges:
        mc.select(edge)
        uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
        for uv in uvs:
            p = mc.polyEditUV(uv, query=True)
            b.append(p)

def test():
    time_start=time.time()
    # edges All edges
    edges = mc.ls(mc.polyListComponentConversion(te=True),fl=True)
    print len(edges)

   
    EdgesNumber = len(edges)
    t1 = threading.Thread(target=ThreadJob1(edges[0:EdgesNumber/2]))
    t1.start()
    t1.join()

    t2 = threading.Thread(target=ThreadJob2(edges[EdgesNumber/2:]))
    t2.start()
    t2.join()


    time_end=time.time()
    print '%.2fs' % (time_end - time_start)

    # print 'Now select edges'
    # print len(b)

    # while(b1 and b2):
    #     time.sleep(1)
    #     print"WATI" 
    #     print 'Now select edges'
    #     print len(b)

    # mc.select(b)
    # mc.polyMapSewMove()
    # time_end=time.time()
    # print '%.2fs' % (time_end - time_start)
    # # mc.ConvertSelectionToContainedEdges()
