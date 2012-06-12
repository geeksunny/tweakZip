tweakZip
=========
tweakZip is a cross-platform program written in Python that creates a customized `update.zip` file for flashing to your Android device.

Using tweakZip
---------------
Creating your custom zip file is a very simple process.

1. Place any files you want your zip file to ADD into the 'data' or 'system' directories.
2. Create the list of files you want your zip to REMOVE in the tweakZip program (menu option #1)
3. Generate your zip file by selecting menu option #3 in tweakZip

You can compile a `tweakZip.exe` file for Windows with py2exe using the included `setup.py` file.

Files in this project
----------------------
tweakZip.py
	- The main source file for tweakZip.
setup.py
	- A setup script for compiling this project with py2exe.
README
	- This readme file.

Requirements
-------------
To use tweakZip, You must have...

On Linux / OSX:
1. Java
2. Python 2.7 (Most likely will be included with your OS)

On Windows:
1. Java
2. Python 2.7 (Not required if running a pre-compiled .exe file)

If you would like to compile a standalone executable version, you must be using Windows and install py2exe, found here:
	- http://www.py2exe.org/

Compiling a standalone exe (Windows Required)
----------------------------------------------
To compile a standalone executable version of tweakZip, simply run this command:
	- python setup.py py2exe
The resulting tweakZip.exe file may be used on systems that do not have Python installed.