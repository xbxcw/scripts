import maya.cmds as cmds

# Create a custom progressBar in a windows ...

window = cmds.window()
cmds.columnLayout()

progressControl = cmds.progressBar(maxValue=10, width=300)
cmds.button( label='Make Progress!', command='cmds.progressBar(progressControl, edit=True, step=1)' )

cmds.showWindow( window )