import pickle
import os

import maya.cmds as mc
version = 100

class UiStates():
	filename = 'config.uvd'
	path = __file__.split('\\')[0]+'/'
	
	def __init__(self):
		self.version = version
		#Window
		self.widthHeight = (1150,700)
		self.collapseFrame0 = False
		self.collapseFrame1 = True
		self.collapseFrame2 = True
		self.collapseFrame3 = True
		self.collapseFrame4 = True
		self.collapseFrame5 = True
		self.collapseFrame6 = True
		self.collapseFrame7 = True
		#self.collapseFrame8 = True
		
		#Settings
		self.textureSize = (5,5)
		self.forgetTextureSize = False
		self.retainCS = mc.texMoveContext('texMoveContext',q=True,scr=True)
		self.matchDist = 0.05
		
		#Quicksnap
		self.snapPath = mc.workspace(q=True,rd=True)			
		
	@staticmethod
	def pickleDump(uis):
		datafile = open(UiStates.path+UiStates.filename,'w')		
		pickle.dump(uis,datafile)
		datafile.close()
		
	@staticmethod
	def pickleLoad():
		#Delete settings file from parent folder
		if os.path.exists(UiStates.path+UiStates.filename):
			print "%s found, loading settings." % UiStates.filename
			datafile = open(UiStates.path+UiStates.filename,'r')
			uis = pickle.load(datafile)
			datafile.close()
			try: 
				pickledVer = uis.version
				if pickledVer < version:
					os.remove(UiStates.path+UiStates.filename)
					return UiStates()
			except:
				os.remove(UiStates.path+UiStates.filename)
				return UiStates()
			return uis
		else:
			return UiStates()
		
	def setUiState(self):
		#Window
		self.widthHeight = mc.window('UVDeluxe',query=True,wh=True)
		self.collapseFrame0 = mc.frameLayout('layout_Settings',query=True,cl=True)
		self.collapseFrame1 = mc.frameLayout('layout_Mover',query=True,cl=True)
		self.collapseFrame2 = mc.frameLayout('layout_Scaler',query=True,cl=True)
		self.collapseFrame3 = mc.frameLayout('layout_Ratio',query=True,cl=True)
		self.collapseFrame4 = mc.frameLayout('layout_Straighten',query=True,cl=True)
		self.collapseFrame5 = mc.frameLayout('layout_Align',query=True,cl=True)
		self.collapseFrame6 = mc.frameLayout('layout_QuickSnap',query=True,cl=True)
		self.collapseFrame7 = mc.frameLayout('layout_MatchUV',query=True,cl=True)
		#self.collapseFrame8 = mc.frameLayout('layout_SelectionSets',query=True,cl=True)
		
		self.forgetTextureSize = mc.checkBox ('STR',q=True,value=True)
		self.matchDist = mc.floatField('MatchUVDistance',q=True,v=True)
		
		#Settings
		if mc.checkBox('STR',q=True,v=True) == False:
			print "box is false"
			self.textureSize = (mc.intSlider('textureSliderW',query=True,value=True),mc.intSlider('textureSliderH',query=True,value=True))
		else:
			print "box is true"
			self.textureSize = (5,5)
			
		self.retainCS = mc.texMoveContext('texMoveContext',q=True,scr=True)
		#Qucksnap
		self.snapPath = mc.textField("pathField",query=True,text=True)
		''' Dump '''
		UiStates.pickleDump(self)