from distutils import command
import maya.cmds as mc
import maya.mel as mel
import subprocess
import math
import os

from uistates import UiStates

#Define globals
version = '1.1.0'
mult = 1

#################
###UI SETTINGS###
#################

uis = UiStates.pickleLoad()
red =    [0.808,0.365,0.306] #[0.8, 0.3, 0.3]
green =  [0.455,0.753,0.295] #[0.3, 0.8, 0.3]
blue =   [0.240,0.616,0.820]
yellow = [0.820,0.671,0.230]

#####################
###END UI SETTINGS###
#####################

#*****************#
#    MAKE WINDOW  #    
#*****************#    
def createUI(*args):
    if mc.window('UVDeluxe', exists=True):
        #remove when not in dev mode
        mc.deleteUI('UVDeluxe')
    
    mc.window('UVDeluxe',s=True,width=440,title='UV Deluxe %s' % version, toolbox=False)
    
    #Create Scriptjobs
    jobNumber1 = mc.scriptJob(parent='UVDeluxe',event=['linearUnitChanged',lambda *args:updateUI('units_text')])

    ### Define texture panel ###
    # Figure out percentage
    pnSize = (220/float(uis.widthHeight[0]))*100
    
    try:
        #swp flag only available in 2011 and beyond
        pane = mc.paneLayout('textureEditorPanel', paneSize=[1,pnSize,1], cn='vertical2', swp=1)
    except:    
        pane = mc.paneLayout('textureEditorPanel', paneSize=[1,pnSize,1], cn='vertical2')
    
    uvTextureViews = mc.getPanel(scriptType='polyTexturePlacementPanel')
    if len(uvTextureViews):
        mc.scriptedPanel(uvTextureViews[0], e=True, unParent=True)
        
    #Load main ui elements#
    mc.columnLayout ('MainColumn', columnWidth=220)
    ui_Settings(0)
    ui_Mover()
    ui_Scaler()
    ui_Ratio()
    ui_MatchUV()
    ui_Straighten()
    ui_Align()
    #ui_SelectionSet()
    ui_QuickSnap()
    
    #Add texture panel to window
    mc.scriptedPanel(uvTextureViews[0], e=True, parent=pane)    
    
    # SHOW WINDOW #    
    mc.showWindow('UVDeluxe')
    mc.window('UVDeluxe',edit=True,mnb=True,widthHeight=uis.widthHeight)
    
#-----------------#    
#    UPDATE UI    #    
#-----------------#    
def updateUI(command,*args):
    if command=='units_text':
        #'Maya Units' text in settings.
        mc.text('unitText',edit=True,label='Working Units: %s' % mc.currentUnit(q=True,f=True))    
        mc.text('ratio_unit',edit=True,label='Pixels per %s:' % mc.currentUnit(q=True))
        command = 'ratio_value'
    elif 'angle' in command:
        # Straighten Edges Angle dials
        if command.split(':')[1] == 'field':
            aValue = mc.floatField('angleField',q=True,value=True)
            mc.floatSlider('angleSlider',edit=True,value=aValue)        
        if command.split(':')[1] == 'slider':
            aValue = mc.floatSlider('angleSlider',q=True,value=True)
            mc.floatField('angleField',edit=True,value=aValue)
    elif 'match' in command:
        aValue = mc.floatSlider('matchSlider', q=True, value=True)
        mc.floatField('MatchUVDistance',edit=True,value=aValue)
    elif command == 'scale_pivot':
        #Check if scaling pivot is based on selection
        if mc.radioButton('PivSel',q=True,sl = True):
            mc.floatField('scalePivotFieldU',edit=True,enable=False)
            mc.floatField('scalePivotFieldV',edit=True,enable=False)
            mc.text('spu',edit=True,enable=False)
            mc.text('spv',edit=True,enable=False)            
            mc.button('samplePivotButton',edit=True,enable=False)    
        else:
            mc.floatField('scalePivotFieldU',edit=True,enable=True)
            mc.floatField('scalePivotFieldV',edit=True,enable=True)
            mc.text('spu',edit=True,enable=True)
            mc.text('spv',edit=True,enable=True)
            mc.button('samplePivotButton',edit=True,enable=True)    
    if 'ratio_value' in command:
        #Updates the floatField containing the value that gets queried by unfold.
        mult = setRatioMultiplier()
        unfold=0.0009765625*(mc.intField('densityField',q=True,value=True))
        mc.floatField('ratioField',edit=True,v=unfold*mult)
    return

#----------------#    
#    Settings    #    
#----------------#
def ui_Settings(flag,*args):
    def retainCompSpace():
        if mc.checkBox ('SCR',q=True,value=True):
            mc.texMoveContext('texMoveContext',e=True,scr=True)            
        else: mc.texMoveContext('texMoveContext',e=True,scr=False)
        uis.setUiState()
    def openPrefs(*args):
        #Open preference window
        mel.eval('preferencesWnd "general";')
        #Change tab
        mel.eval('textScrollList -edit -selectItem (uiRes("m_preferencesWnd.kSettingsTab")) prefIndex;')
        mel.eval('switchPrefTabs 0;')
        return    
    def setResolution(*args):
        # IMPORTANT! SetRatio: multiplier = ((multiplier*(8192/textureResW))/8)
        iterations = 8
        resMin = 32
        maxRes = 32*(2**iterations)
        
        #mel. Create a local var "sliderValue" to whatever textureSliderW is set to.
        sliderValueW = mc.intSlider('textureSliderW', query=True, value=True)
        sliderValueH = mc.intSlider('textureSliderH', query=True, value=True)
        
        #Width
        p2 = resMin
        for i in range(0,iterations+1,1):
            if sliderValueW == i:
                textureResW = p2
                mc.text('resTextW',edit=True,label=str(p2))
            p2*=2
            
        #Height
        p2 = resMin
        for i in range(0,iterations+1,1):
            if sliderValueH == i:
                textureResW = p2
                mc.text('resTextH',edit=True,label=str(p2))
            p2*=2            
        
        if mc.window('UVDeluxe',visible=True,query=True) and not uis.textureSize == (sliderValueW,sliderValueH):
            if mc.checkBox('STR',q=True,v=False):uis.setUiState()
        return
        
    def callSetResAndUpdateUI():
        setResolution()
        updateUI('ratio_value')
        uis.setUiState()
        return

    mc.frameLayout('layout_Settings',label='Settings',width=220,
        cll=True,
        cl=uis.collapseFrame0,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
        
    ## Units and Preferences button
    mc.columnLayout()
    mc.rowLayout(numberOfColumns=2,cw2=(146,60))
    mc.text('unitText',label='Working Units: %s' % mc.currentUnit(q=True,f=True))
    mc.button(label='Maya Prefs',w=68,c=openPrefs)
    mc.setParent('..')
    
    ##
    mc.rowLayout()
    mc.text(label='Your resolution:')
    mc.setParent('..')
    
    ## Width controller
    mc.rowLayout(numberOfColumns=3,cw3=(40,30,140))
    mc.text(label='Size W:')
    mc.text('resTextW',label='')
    mc.intSlider('textureSliderW',w=140,min=0,max=8,value=uis.textureSize[0],step=1,cc=lambda *args:callSetResAndUpdateUI())
    mc.setParent('..')
    
    ## Height controller
    mc.rowLayout(numberOfColumns=3,cw3=(40,30,140))
    mc.text(label='Size H:')
    mc.text('resTextH',label='')
    mc.intSlider('textureSliderH',w=140,min=0,max=8,value=uis.textureSize[1],step=1,cc=lambda *args:callSetResAndUpdateUI())    
    mc.setParent('..')
    
    ## Create Checkboxes
    mc.checkBox ('STR',label="Don't save texture resolution",h=20,
            value=uis.forgetTextureSize,
            cc=lambda *args:uis.setUiState())
    mc.checkBox ('SCR',label='Retain component spacing (Move tool)',h=20,
            value=uis.retainCS,cc=lambda *args:retainCompSpace())
            
    ## Set parent for frameLayout & columnLayout
    mc.setParent('..')
    mc.setParent('..')
    
    setResolution()
    
#--------------#
#    MOVER     #
#--------------#    
def ui_Mover():
    def move(dTuple,*args):
        if not mc.polyListComponentConversion(fuv=True):
            mel.eval('warning "Please select some UVs"')
        else:
            steps = mc.floatField('steps',q=True,v=True)
            sel = mc.ls(sl = True)
            mel.eval('polySelectBorderShell 0')
            mc.polyEditUV(u=(steps*dTuple[0]),v=(steps*dTuple[1]))
            #Refocus selection
            mc.select(sel,r=True)
        return

    mc.frameLayout('layout_Mover',label='Mover',width=220,cll=True,cl=uis.collapseFrame1,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(107,107))
    mc.text(label='Move by steps of:')
    mc.floatField('steps',precision=2,width=107,value=1.0)
    mc.setParent('..')
    ##
    mc.rowLayout(numberOfColumns=4,cw4=(52,52,52,52))
    mc.button(label='Up',w=52, c=lambda *args:move((0,1)))
    mc.button(label='Down',w=52, c=lambda *args:move((0,-1)))
    mc.button(label='Left',w=52, c=lambda *args:move((-1,0)))
    mc.button(label='Right',w=52, c=lambda *args:move((1,0)))
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')

#-----------------------#
#    SCALE AND ROTATE   #
#-----------------------#
def ui_Scaler():
    def getPivot(method):
        ## Methods
        ## 1 = Updates UI with sampled position
        ## 2 = Return Custom UV
        ## None = return selection center
        
        try:
            pivot = mc.polyEvaluate(mc.ls(sl = True), bc2=True)
            pivotU=((pivot[0][0] + pivot[0][1]) * 0.5)
            pivotV=((pivot[1][0] + pivot[1][1]) * 0.5)
        except:
            mel.eval("warning (\"You do not have any UVs selected!\")")
            
        if method == 1:
            mc.floatField('scalePivotFieldU', edit=True, value=pivotU)
            mc.floatField('scalePivotFieldV', edit=True, value=pivotV)
            return
        elif method == 2:
            pivotU = mc.floatField('scalePivotFieldU', query=True, value=True)
            pivotV = mc.floatField('scalePivotFieldV', query=True, value=True)

        return (pivotU, pivotV)
            
    def scale(button_info, *args):
        button_data = button_info.split(':')
        if button_data[0] == 'custom': 
            if button_data[1] == 'u':
                button_data[0] = float(mc.floatField('scaleCustomU', query=True, v=True))
            else:
                button_data[0] = float(mc.floatField('scaleCustomV', query=True, v=True))
        else:
            button_data[0] = float(button_data[0])
        
        #Get pivot from preset or selection
        if mc.radioButton('CustomPivot', query=True, sl = True): pivotUV = getPivot(2)
        else: pivotUV = getPivot(None)
        
        if button_data[1] == 'u':
            mc.polyEditUV(pu=pivotUV[0], pv=pivotUV[1], su=button_data[0], sv=0)
        if button_data[1] == 'v':
            mc.polyEditUV(pu=pivotUV[0], pv=pivotUV[1], su=0, sv=button_data[0])
        return
        
    def smartRotate(dir):
        if not mc.ls(sl = True):
            mel.eval("print 'Could not rotate UVs: Nothing selected'")
            return
        
        resW = float(mc.text('resTextW', query=True, l=True))
        resH = float(mc.text('resTextH', query=True, l=True))

        #Get some uvs
        selection = mc.ls(sl = True)
        # mel.eval('polySelectBorderShell 0;')
        selection = mc.polyListComponentConversion(tuv=True)
        
        selCenter = getPivot(None)
        #Get pivot from preset or selection
        if mc.radioButton('CustomPivot', query=True, sl = True): pivotUV = getPivot(2)
        else: pivotUV = selCenter
        
        #Correct texture/scaling ratio before rotating.
        scaleV = resH/resW
        mc.polyEditUV(pu=selCenter[0], pv=selCenter[1], su=0, sv=scaleV)
        
        #Perform rotate
        mc.polyEditUV(pu=pivotUV[0], pv=pivotUV[1], angle=mc.intField('rot_deg', query=True, v=True)*dir)
        
        #Reverse correction
        selCenter = getPivot(None) #Update position after potential move
        scaleV = resW/resH
        mc.polyEditUV(pu=selCenter[0], pv=selCenter[1], su=0, sv=scaleV)
        return
    
    mc.frameLayout('layout_Scaler',label='Scaling and Rotation',width=220,cll=True,cl=uis.collapseFrame2,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
        
    mc.columnLayout()
    #mc.text(label='Set scaling pivot to selection or custom cords',height=20)
    mc.text(label='Pivot for scaling and roation:',height=20)
    mc.radioCollection('SP_RC')
    ##
    mc.rowLayout(numberOfColumns=4,cw4=(65,75,34,34))
    mc.radioButton('PivSel',w=65,label='Selection',cl='SP_RC',onc=lambda *args:updateUI('scale_pivot'),h=14)
    mc.setParent('..')
    ##    
    mc.rowLayout(numberOfColumns=3,cw3=(115,33,110))
    mc.radioButton('CustomPivot', h=18, w=80,label='Custom UV',cl='SP_RC',onc=lambda *args:updateUI('scale_pivot'))
    mc.text('spu',l='Pos U:',align="left",w=33,enable=False)
    mc.floatField('scalePivotFieldU',pre=7,w=60,v=0.0,h=18)
    mc.setParent('..')
    ##    
    mc.rowLayout(numberOfColumns=3,cw3=(115,33,110))
    mc.button('samplePivotButton',l='Sample selection', c=lambda *args:getPivot(1),h=18,w=108)
    mc.text('spv',l='Pos V:',align="left",w=33,enable=False)
    mc.floatField('scalePivotFieldV',pre=7,w=60,v=0.0,h=18)
    mc.setParent('..')
    ##

    ##
    mc.radioCollection('SP_RC',edit=True,select='PivSel') #Set default selection pivot mode
    mc.text(label='Scale by:',height=20)
    ##
    mc.rowLayout(numberOfColumns=6,cw6=(35,25,25,30,42,47))
    mc.text(l='Width:',h=18)
    mc.button(l='0.5',w=25, c=lambda *args:scale('0.5:u'),h=20, bgc=red)
    mc.button(l='2.0',w=25, c=lambda *args:scale('2.0:u'),h=20, bgc=red)
    mc.button(l='-1.0',w=27, c=lambda *args:scale('-1.0:u'),h=20, bgc=red)
    mc.floatField('scaleCustomU',pre=3, v=0.001 ,w=42,h=20)
    mc.button(l='Custom',w=47, c=lambda *args:scale('custom:u'),h=20, bgc=red)
    mc.setParent('..')
    ###
    mc.rowLayout(numberOfColumns=6,cw6=(35,25,25,30,42,47))
    mc.text(l='Height:',h=18)
    mc.button(l='0.5',w=25, c=lambda *args:scale('0.5:v'),h=20,bgc=green)
    mc.button(l='2.0',w=25, c=lambda *args:scale('2.0:v'),h=20,bgc=green)
    mc.button(l='-1.0',w=27, c=lambda *args:scale('-1.0:v'),h=20,bgc=green)
    mc.floatField('scaleCustomV',pre=3, v=0.001, w=42,h=20)
    mc.button(l='Custom',w=47, c=lambda *args:scale('custom:v'),h=20,bgc=green)
    mc.setParent('..')
    ##
    
        
    
    ##
    mc.text('')
    mc.text(label='Smart Rotate: Maintain width/height ratio')
    mc.rowLayout(numberOfColumns=3,cw3=(34,89,88))
    mc.intField('rot_deg',min=0,max=360,v=90,w=34)
    mc.button('CW_BTN',  label='Rotate CW',w=87, c=lambda *args:(smartRotate(-1)))
    mc.button('CCW_BTN',label='Rotate CCW',w=88, c=lambda *args:(smartRotate(1)))
    mc.setParent('..')
    #mc.text(align='left',label=' (Rotates with width/height ratio correction)')
    ##
    mc.setParent('..')
    mc.setParent('..')
    return
    
#----------------#
#    RATIO UI    #
#----------------#
def ui_Ratio():
    global mult
    
    def ratioHelp(*args):
        help =['This tool will scale your selected shells as close as possible to \nthe desired pixel density. Accuracy will vary depending on the \namount of distortion to your UVs. A new or unmodifed polyCube \nwill have no distortion and be scaled perfectly.',
                "Shells are scaled using the Unfold tool's -scale flag. \nThe output value is simply the number parsed to the \nUnfold tool, and all other options turned off"]
        mc.confirmDialog(title='Set Ratio',button='Ok, whatever',message=str(help[0])+'\n\n'+str(help[1]));
        return
    
    def setRatio(*args):
        resW = float(mc.text('resTextW',q=True,l=True))
        resH = float(mc.text('resTextH',q=True,l=True))
        
        #mult
        mult = setRatioMultiplier()
        
        #Define selection and convert it to uvs
        selection = mc.ls(sl = True)
        selection = mc.polyListComponentConversion(selection, tuv=True)
        
        #Find center of selection
        pivot = mc.polyEvaluate(selection,bc2=True)
        pu=((pivot[0][0] + pivot[0][1]) * 0.5)
        pv=((pivot[1][0] + pivot[1][1]) * 0.5)

        #Correct texture/scaling ratio before rotating.
        if resH != resW:
            scaleV = resH/resW
            mc.polyEditUV(pu=pu,pv=pv,su=0,sv=scaleV)
            
            mc.unfold(i=0,us=True,s=mc.floatField('ratioField',q=True,v=True))

            #Reverse correction
            scaleV = resW/resH
            mc.polyEditUV(pu=pu,pv=pv,su=0,sv=scaleV)
        else:            
            mc.unfold(i=0,us=True,s=mc.floatField('ratioField',q=True,v=True))
            
        mc.select(selection,replace=True)        
        return        

    mc.frameLayout('layout_Ratio',label='Ratio (Pixel density)',width=220,cll=True,cl=uis.collapseFrame3,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(170,42))
    mc.text(label='Scale shells to desired pixel density',w=170)
    mc.button(w=42,label='Info',align='right', command=ratioHelp)
    mc.setParent('..')
    ##//Pixel Density Controls//
    mc.rowLayout(numberOfColumns=3,cw3=(72,35,104))
    mc.text('ratio_unit',label='Pixels per %s:' % mc.currentUnit(q=True))
    mc.intField('densityField',v=256,min=0,max=8192,w=35,cc=lambda *args:updateUI('ratio_value'))
    mc.button(width=104,label='Set Ratio',command=setRatio)
    mc.setParent('..')
    ##    
    mc.rowLayout(numberOfColumns=2,cw2=(108,106))
    mc.text(label='Output value: (ignore)',w=108)
    mc.floatField('ratioField',pre=5,enable=False,w=106,v=0.0009765625*(mc.intField('densityField',q=True,v=True)))
    mc.setParent('..')
    ##
    mc.setParent('..')
    mc.setParent('..')
    updateUI('ratio_value')
    
#-------------------#
#     MatchUV UI        #
#-------------------#
def ui_MatchUV():
    def matchUVS(maxDist):
        def sortDist(tuple):
            return tuple[1]
        
        def getOtherUVS(allSelected,suvs):
            objects = [i.split('.')[0] for i in allSelected]
            objects = [i for i in set(objects)]
            uvs = mc.ls(mc.polyListComponentConversion(objects,tuv=True),fl=True)
            return sorted(set.difference(set(uvs)-set(suvs)))

        ### SETUP ###
        allSelected = mc.ls(sl = True)
        # Create list of uvs
        suvs = mc.ls(mc.polyListComponentConversion(tuv=True),sl = True,fl=True)
        ouvs= getOtherUVS(allSelected,suvs)
        
        # Create list of positions
        spos = [mc.polyEditUV(i,query=True) for i in suvs]
        opos = [mc.polyEditUV(i,query=True) for i in ouvs]

        ### PERFORM ###
        for i in range(len(suvs)):
            withinRange = []
            for j in range(len(ouvs)):
                x = spos[i][0]-opos[j][0]
                y = spos[i][1]-opos[j][1]
                dist =  math.sqrt((x**2) + (y**2)) 
                if dist < maxDist:
                    withinRange.append((opos[j],dist))
                                    
            withinRange = sorted(withinRange,key=sortDist)
            if len(withinRange):
                mc.polyEditUV(suvs[i],u=withinRange[0][0][0],v=withinRange[0][0][1],relative=False)

        uis.setUiState()
        return
    
    mc.frameLayout('layout_MatchUV',label='Match UVs',width=220,cll=True,cl=uis.collapseFrame7,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    
    mc.columnLayout()
    ##
    mc.text(label='Move UVs to closest unselected neighbour')
    mc.rowLayout(numberOfColumns=4,cw4=(45,50,49,65))
    mc.text(label='Distance:', w=45)
    mc.floatField('MatchUVDistance',pre=5,v=uis.matchDist,w=50)
    mc.floatSlider('matchSlider',min=0.0,max=1.0,value=uis.matchDist,w=49,dc=lambda *args:updateUI('match'))
    mc.button(width=65,label='Match UVs', command=lambda* args:matchUVS(mc.floatField('MatchUVDistance',q=True,v=True)))
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')
    return
    
#-------------------#
#    Straighten UI    #
#-------------------#

def ui_Straighten():
    def help(*args):
        help =['This script will flatten edges based on the initial angle of each edge.\nWhat that means is, if an edge is closer to being more vertical than \nhorizontal it can only be flattened vertically.',
                'So before the script flattens anything, it sorts all edges into two lists\nof horizontal and vertical and then decides which lists to flatten\nif the angle is within the range you set.']
        mc.confirmDialog(title='Straighten Edges',button='Got it!',message=help[0]+'\n\n'+help[1])
        return
    ## UI ##

    mc.frameLayout('layout_Straighten',label='Straighten Edges',width=220,cll=True,cl=uis.collapseFrame4,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(170,43))
    mc.text(label='Straighten based on UV selection')
    mc.button(w=43,label='Info',align='right',c=help)
    mc.setParent('..')
    ##
    mc.rowLayout(numberOfColumns=3,cw3=(82,35,100))
    mc.text(label='Angle tolerance:',align='left',w=82)
    mc.floatField('angleField',min=0,max=45,value=30,pre=1,w=35,cc=lambda *args:updateUI('angle:field'))
    mc.floatSlider('angleSlider',min=0,max=45,value=30,w=82,dc=lambda *args:updateUI('angle:slider'))
    mc.setParent('..')
    ##
    mc.rowLayout(numberOfColumns=3,cw3=(71,71,71))
    mc.button(label='Horizontal',w=71, h=20, c=lambda *args:(straightenEdges('hori')), bgc=green)
    mc.button(label='Vertical',w=71, h=20, c=lambda *args:(straightenEdges('vert')), bgc=red)
    mc.button(label='Both',w=71, h=20, c=lambda *args:(straightenEdges('both')), bgc=yellow)
    mc.setParent('..')
    ##
    mc.setParent('..')
    mc.setParent('..')

#-------------------#
#    Align Tools UI    #
#-------------------#

def ui_Align():

    mc.frameLayout('layout_Align',label='Align Tools',width=220,cll=True,cl=uis.collapseFrame5,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(137,77))
    mc.text(align='left',label='Straighten shells by rotation:',w=137)
    mc.button(label='Rotate Align',w=77, c=lambda *args:(align('--shell')))
    mc.setParent('..')
    ##
    ##
    mc.text(label='Align shells:')
    mc.rowLayout(numberOfColumns=4,cw4=(52,52,52,52))
    mc.button(label='Top',    w=52, c=lambda *args:alignShells("up"),    h=20,  bgc=green)
    mc.button(label='Bottom', w=52, c=lambda *args:alignShells("down"),  h=20,  bgc=green)
    mc.button(label='Left',   w=52, c=lambda *args:alignShells("left"),  h=20,  bgc=red)
    mc.button(label='Right',  w=52, c=lambda *args:alignShells("right"), h=20,  bgc=red)
    mc.setParent('..')
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(106,106))
    mc.button(label='Center Vertical',   w=106, c=lambda *args:alignShells("centerV"), h=20, bgc=green)
    mc.button(label='Center Horizontal', w=106, c=lambda *args:alignShells("centerH"), h=20, bgc=red)
    mc.setParent('..')
    ##
    mc.setParent('..')
    mc.setParent('..')
    return

#-----------------------#
#    SELECTION SETS     #
#-----------------------#

def ui_SelectionSet():
    selectionSlots = ['none','none','none','none','none','none']
    
    colorBlank = [0.3,0.3,0.3]
    uColor = [0.584314,0.772549,0.0]
    vColor = [0.913725,0.878431,0.0]
    eColor = [0.870588,0.643137,0.117647]
    oColor = [0.152941,0.729412,0.447059]
    fColor = [0.478431,0.227451,0.227451]

    mc.frameLayout('layout_SelectionSets',label='Selection Sets',width=220,cll=True,cl=uis.collapseFrame8,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    mc.rowLayout(numberOfColumns=6)
    mc.button("slotButton1", label='', w=49, c=lambda *args: storeLoadSelection(1), bgc=colorBlank)
    mc.iconTextButton("slotTrash1",style="iconOnly", ann="Clear Slot 1", image="SP_TrashIcon.png", c=lambda *args: clearSlot(1))
    mc.button("slotButton2", label='', w=49, c=lambda *args: storeLoadSelection(2), bgc=colorBlank)
    mc.iconTextButton("slotTrash2",style="iconOnly", ann="Clear Slot 2", image="SP_TrashIcon.png", c=lambda *args: clearSlot(2))
    mc.button("slotButton3", label='', w=49, c=lambda *args: storeLoadSelection(3), bgc=colorBlank)
    mc.iconTextButton("slotTrash3",style="iconOnly", ann="Clear Slot 3", image="SP_TrashIcon.png", c=lambda *args: clearSlot(3))
    mc.setParent('..')
    mc.rowLayout(numberOfColumns=6)
    mc.button("slotButton4", label='', w=49, c=lambda *args: storeLoadSelection(4), bgc=colorBlank)
    mc.iconTextButton("slotTrash4",style="iconOnly", ann="Clear Slot 4", image="SP_TrashIcon.png", c=lambda *args: clearSlot(4))
    mc.button("slotButton5" ,label='', w=49, c=lambda *args: storeLoadSelection(5), bgc=colorBlank)
    mc.iconTextButton("slotTrash5",style="iconOnly", ann="Clear Slot 5", image="SP_TrashIcon.png", c=lambda *args: clearSlot(5))
    mc.button("slotButton6",label='', w=49, c=lambda *args: storeLoadSelection(6), bgc=colorBlank)
    mc.iconTextButton("slotTrash6",style="iconOnly", ann="Clear Slot 6", image="SP_TrashIcon.png", c=lambda *args: clearSlot(6))
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')
    
#--------------------#
# Quck UvSnapshot UI #
#--------------------#
def ui_QuickSnap():
    #path = os.path.expanduser('~')
    #path = os.getenv('USERPROFILE') or os.getenv('HOME')
    path = uis.snapPath
    
    def performQuicksnap():
        # options #
        width = int(mc.text('resTextW',query=True,label=True))
        height = int(mc.text('resTextH',query=True,label=True))
        if mc.checkBox ('doubleRes', query=True, value=True):
            width *= 2
            height *= 2
        autoLoad = mc.checkBox ('autoLoad', query=True, value=True)
        antiAlias = mc.checkBox ('antiAliasing', query=True, value=True)
        
        fileName = 'outUV'
        format = mc.optionMenuGrp('fileFormat', query=True, value=True) 
        filePath = mc.textField('pathField',query=True,text=True) + '/' + fileName + '.' + format
        uis.setUiState()
        
        # # # Perform # # #
        mc.uvSnapshot(name=filePath,xr=width,yr=height,o=True,aa=antiAlias,ff=format)
        
        if autoLoad:
            os.startfile(filePath)
    
    mc.frameLayout('layout_QuickSnap',label='Quick UV Snapshot',width=220,cll=True,cl=uis.collapseFrame6,
        cc=lambda *args:uis.setUiState(),
        ec=lambda *args:uis.setUiState())
    mc.columnLayout()
    ##
    mc.text(align='left',label='Create UV Snapshot for selected objects')
    ##
    mc.rowLayout(numberOfColumns=3,cw3=(65,65,70))
    mc.checkBox ('autoLoad',label='Open file',value=True)
    mc.checkBox ('antiAliasing',label='Anti Alias',value=True)
    mc.checkBox ('doubleRes',label='Double Size',value=False)
    mc.setParent('..')
    ##
    #mc.text(label="Output directory:")
    mc.textField("pathField",text=path,width=214)
    ##
    mc.rowLayout(numberOfColumns=2,cw2=(89,122))
    mc.optionMenuGrp('fileFormat',label="Format:",cat=[1,'left',0],cw2=[40,48]) 
    mc.button(label='Save snapshot',w=119, c=lambda *args:performQuicksnap())
    mc.menuItem(label='tga')             
    mc.menuItem(label='tif')
    mc.menuItem(label='png')
    mc.setParent('..')
    ##
    mc.setParent('..')
    mc.setParent('..')

#####////////////////////////////////#####
#####                                #####
#####            CLASSES             #####
#####                                #####
#####////////////////////////////////#####

class UVClass:
    def __init__(self, uvs = "selection"):
        #Set self.uvs from a list of uvs or automatically
        if uvs == "selection": #No list was sent
            self.uvs = mc.ls(mc.polyListComponentConversion(tuv=True),fl=True)
        else: self.uvs = uvs

        self.type = "standard"
        self.shells = []

    def setMinMax(self):
        xPositions = sorted([mc.polyEditUV(i, query=True)[0] for i in self.uvs])
        yPositions = sorted([mc.polyEditUV(i, query=True)[1] for i in self.uvs])

        self.minMax = (xPositions[0],xPositions[-1]),(yPositions[0],yPositions[-1])
        self.xMin = self.minMax[0][0]
        self.xMax = self.minMax[0][1]
        self.yMin = self.minMax[1][0]
        self.yMax = self.minMax[1][1]

    def getPivot(self):
        pivot = mc.polyEvaluate(self.uvs,bc2=True)
        pivU = ((pivot[0][0] + pivot[0][1]) * 0.5)
        pivV = ((pivot[1][0] + pivot[1][1]) * 0.5)
        return pivU,pivV

    def getShells(self):
        """ This creates a list object (shells) within the class containing a UVClass per shell found"""
        if len(self.shells): #No need to do this twice
            if self.type == "shell":
                print "Class is already of shell type. This function call is redundant"
            return

        currentSelection = mc.ls(sl = True)
        self.shells = []
        for uv in self.uvs:
            found = False
            for shell in self.shells:
                if uv in shell.uvs:
                    found = True
            if not found:
                mc.select(uv)
                mel.eval('polySelectBorderShell 0;')
                thisShell = UVClass()
                thisShell.type = "shell"
                thisShell.setMinMax()

                self.shells.append(thisShell)

        mc.select(currentSelection)

#####///////////////////////////////////////#####
#####                                       #####
#####            SHARED PROCEDURES          #####
#####                                       #####
#####///////////////////////////////////////#####


def alignShells(dir):
    selected = UVClass()
    selected.getShells()

    shellsUVs = []
    for shell in selected.shells:
        for uv in shell.uvs:
            shellsUVs.append(uv)

    allUVs = UVClass(shellsUVs)
    allUVs.setMinMax()

    #Move shells
    for shell in selected.shells:
        if dir == "right":
            mc.polyEditUV(shell.uvs, u= allUVs.xMax - shell.xMax)
        elif dir == "left":
            mc.polyEditUV(shell.uvs, u= allUVs.xMin - shell.xMin)
        elif dir == "centerH":
            mc.polyEditUV(shell.uvs, u = (allUVs.xMin+allUVs.xMax)/2 - (shell.xMax + shell.xMin)/2)
        elif dir == "up":
            mc.polyEditUV(shell.uvs, v= allUVs.yMax - shell.yMax)
        elif dir == "down":
            mc.polyEditUV(shell.uvs, v= allUVs.yMin - shell.yMin)
        elif dir == "centerV":
            mc.polyEditUV(shell.uvs, v = (allUVs.yMin+allUVs.yMax)/2 - (shell.yMax + shell.yMin)/2)
        
def align(flag,*args): #Rotate align shell(s)
    orgSel = UVClass()
    orgSel.getShells()

    alignPoints = []
    if len(orgSel.uvs) < 2:
        mel.eval('warning("Select at least two uvs!")')
        return

    for shell in orgSel.shells:
        #Rotations can be unexpected if more than two uvs per shell were selected
        #This is often because orgSel is not in the same order as uvs were selected
        uvPositions = {}
        for uv in orgSel.uvs:
            if uv in shell.uvs and uv not in uvPositions.keys():
                uvPositions[len(uvPositions.items())] = uv

        if len(uvPositions) >= 2:
            angle = findAngle(( uvPositions.get(0), uvPositions.get(1) ))
            pivot = shell.getPivot()
            pu = pivot[0]
            pv = pivot[1]

            #Align to hoizontal
            if angle >-45 and angle < 45:
                mc.polyEditUV (shell.uvs, pu=pu,pv=pv,angle=(0 - angle))
            elif angle >135 and angle < 180:
                mc.polyEditUV (shell.uvs, pu=pu,pv=pv,angle=(180 - angle))
            elif angle >-180 and angle <-135:
                mc.polyEditUV (shell.uvs, pu=pu,pv=pv,angle=(180 - angle))

            #Align to vertical
            if angle >45 and angle <135:
                mc.polyEditUV (shell.uvs, pu=pu,pv=pv,angle=(90 - angle))
            elif angle <-45 and angle >-135:
                mc.polyEditUV (shell.uvs, pu=pu,pv=pv,angle=(270 - angle))
    return
    
def findAngle(tuple):
    #Returns angle of two UV points
    uv0 = tuple[0]
    uv1 = tuple[1]
    p1 = mc.polyEditUV(uv0,q=True)
    p2 = mc.polyEditUV(uv1,q=True)
    X = (p2[0] - p1[0])
    Y = (p2[1] - p1[1])
    
    radians = math.atan2(Y,X)
    angle = radians*57.2957795
    
    return angle

def findBox2D(uvs):
    xMin = mc.polyEditUV(uvs[0],query=True)[0]
    xMax = mc.polyEditUV(uvs[0],query=True)[0]
    yMin = mc.polyEditUV(uvs[0],query=True)[1]
    yMax = mc.polyEditUV(uvs[0],query=True)[1]
    
    for u in uvs:
        posX = mc.polyEditUV(u,query=True)[0]
        posY = mc.polyEditUV(u,query=True)[1]
        
        if   posX > xMax: xMax = posX
        elif posX < xMin: xMin = posX
        if   posY > yMax: yMax = posY
        elif posY < yMin: yMin = posY    
    
    return (xMin,xMax), (yMin,yMax)

def setRatioMultiplier():
    resW = float(mc.text('resTextW',q=True,l=True))
    resH = float(mc.text('resTextH',q=True,l=True))
    
    unit = mc.currentUnit(query=True,f=True)
    global mult 
    mult = 1
    if not unit == 'centimeter':
        if unit == 'meter':
            mult = 0.01
        elif unit == 'millimeter':
            mult = 10
        else:
            mc.confirmDialog(title='Sorry!',button='ok',message='UVDeluxe\'s Set Ratio does work with unit type: %s\nPlease work in meters, centimeters or millimeters' % unit);
            #mc.error('Script not configured for unit %s' % unit)
    
    mult = (mult*(8192/resW))/8
    return mult

def straightenEdges(flag):
    def findAdjacentEdges(gotEdges):
        ## Accepts list of tuples size 2 ##
        adjacentEdges = {}

        ##STEP ONE##
        #Create list of all UVs in gotEdges
        everyUV = []
        for e in range(0,len(gotEdges),1):
            for u in range(0,len(gotEdges[e]),1):
                if not gotEdges[e][u] in everyUV:
                    everyUV.append(gotEdges[e][u])

        #Check which uvs are in more than one edge, and store those edge connections.
        pairs = []
        loneEdges = []
        for u in range(0,len(everyUV),1):
            #Clear list of found edges for this uv
            foundE = []
            for e in range(0,len(gotEdges),1):
                if everyUV[u] in gotEdges[e]:
                    foundE.append(gotEdges[e])

                #Put edges into appropriate list, right before the loop iteration ends.
                if e==len(gotEdges)-1:
                    if len(foundE) == 2 and not foundE in pairs: pairs.append(foundE)
                    elif len(foundE) == 1 and not foundE in loneEdges:
                        loneEdges.append(foundE)

        #Remove pair-ends that got put into loneEdges
        for l in range(len(loneEdges)-1,-1,-1):
            found = []
            for p in range(0,len(pairs),1):
                if loneEdges[l][0] in pairs[p]:
                    found.append(l)
            for f in range(0,len(found),1):
                loneEdges.pop(found[f])

        ## STEP TWO ##
        incomplete = True
        addNewPair = False
        unsortedPairs = pairs[:]
        keysComplete = []

        if len(pairs):
            while incomplete:
                keysSkipped = 0

                if len(unsortedPairs):
                    ### print "\nAdding new key!"
                    adjacentEdges[len(adjacentEdges)] = unsortedPairs[0]

                for key in adjacentEdges.keys():
                    ### print "\nNow checking Key %d" % key
                    if key not in keysComplete:
                        #Pop first pair key from unsortet.
                        popPairs = []
                        deletePair = []
                        for p in unsortedPairs:
                            if p == adjacentEdges[key]:
                                deletePair.append(p)
                        for p in deletePair:
                            unsortedPairs.remove(p)

                        addingToKey = True
                        while addingToKey:
                            uvs_inKey = []
                            for pair in adjacentEdges.get(key):
                                for uv in pair:
                                    uvs_inKey.append(uv)

                            popPairs = []
                            pairsToAdd = []
                            for p in range(0,len(unsortedPairs),1):
                                for uv in uvs_inKey:
                                    #Check if either edge of pair contains key-uv
                                    if uv in unsortedPairs[p][0] or uv in unsortedPairs[p][1]:
                                        pairsToAdd.append(unsortedPairs[p])

                            #Add pairs to key and remove from list of unsorted pairs
                            for pair in pairsToAdd:
                                adjacentEdges[key] += pair
                                adjacentEdges[key] = sorted(list(set(adjacentEdges[key])))
                                if pair in unsortedPairs:
                                    unsortedPairs.remove(pair)

                            #Break loop when nothing more to add
                            if not len(pairsToAdd):
                                addingToKey = False
                                keysComplete.append(key)

                    else:
                        #Break loop when all keys are complete
                        keysSkipped += 1
                        if keysSkipped == len(adjacentEdges):
                            incomplete = False

        #Assign key to every single edge left
        for e in loneEdges:
            adjacentEdges[len(adjacentEdges)] = e

        #Restructure keys from list of tuples to list of uvs
        for key in adjacentEdges.keys():
            uvs_inKey = []
            for tuple in adjacentEdges[key]:
                uvs_inKey.append(tuple[0])
                uvs_inKey.append(tuple[1])

            #Replace list with new list
            adjacentEdges[key] = sorted(list(set(uvs_inKey)))

        return adjacentEdges

    max_angle = mc.floatField('angleField', query=True, value=True)

    orgSel = mc.ls(sl = True)
    edges = createEdgeList()

    #Sort edges by horizontal and vertical
    sortedEdges = sortEdges(edges,max_angle)

    #Determin method of straightening
    ## Horizontal
    if not flag == 'vert':
        hz_edges = findAdjacentEdges(sortedEdges[0])

        for key in hz_edges.keys():
            box = findBox2D(hz_edges[key])
            centerV=((box[1][0] + box [1][1]) * 0.5)
            mc.polyEditUV(hz_edges[key],v=centerV,relative=False)

    ## Vertical
    if not flag == 'hori':
        vt_edges = findAdjacentEdges(sortedEdges[1])

        for key in vt_edges.keys():
            box = findBox2D(vt_edges[key])
            centerU=((box[0][0] + box[0][1]) * 0.5)
            mc.polyEditUV(vt_edges[key],u=centerU,relative=False)
    return

def createEdgeList():
    def addToEdges(uv0, uv1):
        uvTup1 = (uv0,uv1)
        uvTup2 = (uv1,uv0)
        if not uvTup1 in edges.values() and not uvTup2 in edges.values():
            edges[len(edges)] = uvTup1
        return
    
    edges = { }    
    orgSel = mc.ls(sl = True, fl=True)

    #####################
    #Build list of edges
    if len(orgSel):
        for u in range(0,len(orgSel),1):
            uv1 = orgSel[u]
            uvToEdge = mc.ls(mc.polyListComponentConversion(orgSel[u], fuv=True, te=True), fl=True)
            
            #Get uvs in convertToFace selection
            faces = mc.ls(mc.polyListComponentConversion(orgSel[u], fuv=True, tf=True), fl=True)
            uvGrowSel = []
            for f in faces:
                uv = mc.ls(mc.polyListComponentConversion(f, ff=True, tuv=True), fl=True)
                for point in uv:
                    if not point in uvGrowSel:
                        uvGrowSel.append(point)
            
            #Check if there is a connection between point 1 and points in grow selection.
            for g in uvGrowSel:
                e1 = mc.ls(mc.polyListComponentConversion(uv1, fuv=True, te=True), fl=True)
                e2 = mc.ls(mc.polyListComponentConversion(g, fuv=True, te=True), fl=True)
                se = list(set(e1) & set(e2))
                if len(se):
                    #There is
                    ed = mc.ls(mc.polyListComponentConversion(se[0], fe=True, tuv=True), fl=True)                    
                    keepUVs = []
                    for e in range(len(ed)):
                        if ed[e] in uvGrowSel and ed[e] in orgSel:
                            keepUVs.append(ed[e])
                        if len(keepUVs) == 2:
                            addToEdges(keepUVs[0], keepUVs[1])                

    return edges

def sortEdges(edges, max_angle):
    hz_edges = {}
    vt_edges = {}        
    for e in edges:
        if not e in hz_edges.values() and not e in vt_edges.values():
            angle = findAngle(edges[e])
            #if not uvTup1 in edges.values() and not uvTup2 in edges.values(): edges[len(edges)] = uvTup1
            if angle < 0:
                angle = angle*-1        
            #hoizontal
            if angle < 45 and angle >= 0:
                if angle < max_angle:
                    hz_edges[len(hz_edges)] = edges[e]
            elif angle >= 135 and angle < 180:
                if angle > 180-max_angle:
                    hz_edges[len(hz_edges)] = edges[e]
            #vertical
            elif angle < 135 and angle >= 45:
                if angle < 90 and angle > 90-max_angle:
                    vt_edges[len(vt_edges)] = edges[e]
                elif angle > 90 and angle < 90+max_angle:
                    vt_edges[len(vt_edges)] = edges[e]        
    return hz_edges,vt_edges
