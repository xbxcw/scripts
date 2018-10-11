UVDeluxe 1.1.1
By Erik Spellerberg - erik.spellerberg@gmail.com
Downloaded from: http://www.creativecrash.com/maya/downloads/scripts-plugins/texturing/c/uvdeluxe/


	New in version 1.1.1

	* Added buttons to center-align shells horizontally and vertically.
	* Colorized certain buttons to make it easier.
	* Restructured code a bit to allow shortcuts for

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
If you get a crash when trying to start UVDeluxe after updating it
from an older version, delete the old files and start fresh.
The settings file it creates does not like all older versions.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
	
		
		Installation

1) Place the UVDeluxe FOLDER in Maya's script folder 
  e.g "..\USER\Documents\maya\scripts\UVDeluxe"
	
2) Create a shelf button with the Python code:

from UVDeluxe import uvdeluxe
uvdeluxe.createUI()


		Creating hotkeys

Hotkeys have to be written in mel, don't ask me why, and since this script is in python 
Commands need to be called like this: python("SomeCommand");

Also, UVDeluxe needs to be started once (per instance of Maya) before you can access any commands.


/// Straighten Edges ///

Horizontal: python("uvdeluxe.straightenEdges('hori')");
Vertical:   python("uvdeluxe.straightenEdges('vert')");
Both:       python("uvdeluxe.straightenEdges('both')");

! Tolerance still has to be set in the UI

//Align Shells//

python("uvdeluxe.alignShells('left')");
python("uvdeluxe.alignShells('right')");
python("uvdeluxe.alignShells('up')");
python("uvdeluxe.alignShells('down')");
python("uvdeluxe.alignShells('centerV')");
python("uvdeluxe.alignShells('centerH')");
