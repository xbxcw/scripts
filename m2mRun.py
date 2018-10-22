import sys
import os
from os import path
scriptPath = os.path.expanduser("~/maya/scripts/MaxToMaya/MaxToMaya.py")
scriptPathPyc = os.path.expanduser("~/maya/scripts/MaxToMaya/MaxToMaya.pyc")
if os.path.exists(scriptPathPyc): scriptPath = scriptPathPyc
if os.path.exists(scriptPath): scriptPath = scriptPath
def psource(module):
    file = os.path.basename( module )
    dir = os.path.dirname( module )
    toks = file.split( '.' )
    modname = toks[0]
    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
        if not pathfound:
            sys.path.append( dir )
    exec ('import ' + modname) in globals()
    exec( 'reload( ' + modname + ' )' ) in globals()
    return modname
def start():
    # When you import a file you must give it the full path
    print "m2mRun: " + scriptPath
    psource( scriptPath )