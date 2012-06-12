__author__ = 'Justin Swanson'
__version__ = '0.1'

import os								# For running system commands & getting directory contents.
from subprocess import Popen, PIPE		# For piping system command output to the background.
import zipfile							# For creating the zip archive file.
#import zlib							# For compressing the files while zipping them up.

# Global Variables
fileName = "tweakzip"
filesToRemove = []
# Debug Variables
#filesToRemove = ["/system/app/CarHomeGoogle.apk","/system/app/Email.apk","/system/app/Exchange.apk"] #debug

### Clear screen function... clears the command prompt window.
def cls():
	os.system(['clear','cls'][os.name == 'nt'])

### List Directory function... returns a list of all the files inside a given directory.
def lsDir(dir = "."):
	list = []
	for dirname, dirnames, filenames in os.walk(dir):
		for filename in filenames:
			list.append(str(os.path.join(dirname, filename)).replace('\\','/'))
			# Runs a string replace that replaces any backslashes with forward slashes. For correct output on Windows hosts.
	return list

### Make Zip File function... creates a zip file containing all files designated in fileList[].
# TODO: Add exception catching code to this function and an exit code return.
def makeZipFile(filename, fileList = []):
	zf = zipfile.ZipFile(filename, mode='w')
	for file in fileList:
		# If the current item in fileList is a directory, scan it recursively and add each item.
		if os.path.isdir(file):
			dirContents = lsDir(file)
			for dirFile in dirContents:
				zf.write(dirFile, compress_type=zipfile.ZIP_DEFLATED)
		# If the current item in fileList is not a directory, add it as normal.
		else:
			zf.write(file, compress_type=zipfile.ZIP_DEFLATED)
	zf.close()

### Dependency Check function...
# TODO: Better exception checking code...
def depCheck():
	# Check for the directories, and create them as needed!
	dirCheck = ['configs','data/app','system/app','system/media','META-INF/com/google/android/']
	for dirName in dirCheck:
		if not os.path.isdir(dirName):
			os.makedirs(dirName)
	# Check for signapk.jar and related files.
	requiredFiles = []
	if not os.path.isfile('signapk.jar') or not os.path.isfile('certificate.pem') or not os.path.isfile('key.pk8'):
		requiredFiles.append('signapk.zip')
	if not os.path.isfile('META-INF/com/google/android/update-binary'):
		requiredFiles.append('update-binary')
	if len(requiredFiles) > 0:
		cls()
		print\
		"-------------------------------------------------\n",\
		"                 TweakZip v" + __version__ + "\n",\
		"-------------------------------------------------\n\n",\
		" Certain required files are not found.\n",\
		" Would you like to automatically download them?\n",\
		" If you choose not to, the program wil exit.\n"
		choice = raw_input("Download required files? Y/N [Y]: ")
		if choice in ('n','N'):
			return False
		else:
			from urllib import urlretrieve	# To use to download the file.
			for file in requiredFiles:
				if file == 'signapk.zip':
					urlretrieve('http://beta.h4xful.net/files/tweakZip/signapk.zip','./signapk.zip')
					if os.path.isfile('signapk.zip'):
						zf = zipfile.ZipFile('signapk.zip','r')
						zf.extractall()
						zf.close()
					else:
						print "Error: The file could not be downloaded successfully.\n"
						return False
				elif file == 'update-binary':
					urlretrieve('http://beta.h4xful.net/files/tweakZip/update-binary','./META-INF/com/google/android/update-binary')

	return True

### Resets all configuration variables to be blank.
def resetConfig():
	global filesToRemove
	del filesToRemove[:]
	print "Your configuration has been reset!"

### Loads configuration variables into memory from saved config files.
def loadConfig():
	global filesToRemove, fileName
	reprint = True
	message = ''
	while True:
		if reprint == True:
			cls()
			print\
			"-------------------------------------------------\n",\
			"                   Load Config\n",\
			"-------------------------------------------------\n"
			cfgFiles = lsDir("configs")
			if len(cfgFiles) > 0:
				i = 1
				for file in cfgFiles:
					print " " + str(i) + ". " + file
					i += 1
			else:
				i = 0
				print " There are currently no configuration files saved."
			print\
			"\n-------------------------------------------------\n",\
			"\n Please enter the corresponding number for the",\
			"\n    configuration file you'd like to load.",\
			"\n To go back to the main menu, enter 'Q'.\n"
		if message != '':
			print message + '\n'
		entry = raw_input("Please make your entry: ")
		reprint = True
		if entry.isdigit() == True:
			if int(entry) in range(1,len(cfgFiles)+1):
				fh = open(cfgFiles[int(entry)-1],'r')
				input = fh.read()
				cfg = input.split(':')
				filesToRemove = cfg[0].split(',')
				fileName = cfgFiles[int(entry)-1].replace('configs/','')
				fh.close()
				message = "Configuration loaded from " + cfgFiles[int(entry)-1] + "!"
			else:
				reprint = False
				print "That is not a valid number in the list."
		elif entry in ('q','Q'):
			return True
		else:
			reprint = False
			print "Invalid selection!"

### Saves configuration variables to an config file.
def saveConfig():
	global fileName
	reprint = True
	message = ''
	while True:
		if reprint == True:
			cls()
			print\
			"-------------------------------------------------\n",\
			"                   Save Config\n",\
			"-------------------------------------------------\n"
			cfgFiles = lsDir("configs")
			if len(cfgFiles) > 0:
				i = 1
				for file in cfgFiles:
					print " " + str(i) + ". " + file
					i += 1
			else:
				i = 0
				print " There are currently no configuration files saved."
			print\
			"\n-------------------------------------------------\n",\
			"\n Please enter a name for your configuration.",\
			"\n If you'd like to replace an existing configuration,",\
			"\n    enter the number next to it.",\
			"\n To go back to the main menu, enter 'Q'.\n"
		if message != '':
			print message + '\n'
		entry = raw_input("Please make your entry [" + fileName + "]: ")
		reprint = True
		if entry.isdigit() == True:
			if int(entry) in range(1,len(cfgFiles)+1):
				try:
					fileName = cfgFiles[int(entry)-1].replace('configs/','')
					fh = open(cfgFiles[int(entry)-1],'wb')
					outputStr = ''
					for file in filesToRemove:
						outputStr = outputStr + file + ','
					fh.write(outputStr[:-1] + ':')
					outputStr = ''
					fh.write(outputStr[:-1])
					fh.close()
					message = "Configuration saved as " + cfgFiles[int(entry)-1] + "!"
				except IOError as e:
					print "There was an error saving your configuration!"
					print "  " + str(e)
			else:
				reprint = False
				print "That is not a valid number in the list."
		elif entry in ('q','Q'):
			return True
		else:
			try:
				if len(entry) == 0:
					entry = fileName
				else:
					fileName = entry
				fh = open('configs/' + entry,'wb')
				outputStr = ''
				for file in filesToRemove:
					outputStr = outputStr + file + ','
				fh.write(outputStr[:-1] + ':')
				outputStr = ''
				fh.write(outputStr[:-1])
				fh.close()
				message = "Configuration saved as " + entry + "!"
			except IOError as e:
				print "There was an error saving your configuration!"
				print "  " + str(e)

### Builds and signs the update.zip file.
def buildZip():
	# Scan directories for the file that will be installed
	sysFiles = lsDir("system")
	dataFiles = lsDir("data")
	# If there are no files to install and other instructions for the zip, abort the build proces
	if len(sysFiles) == 0 and len(dataFiles) == 0 and len(filesToRemove) == 0:
		print "There is nothing to go into your zip! Nothing will be built."
		return False
	# Prompt for the filename
	global fileName
	entry = raw_input("What do you want to name your file? [" + fileName + "]: ")
	if len(entry) > 0:	# Will default to the existing value if no input is presented
		fileName = entry
	# TODO: Add error checking/catching to this. Must try/catch the fh = open() statement!
	# Open the updater-script for writing. Any existing file will be completely replaced
	fh = open('META-INF/com/google/android/updater-script','wb')
	fh.write('ui_print("----------");\n')
	fh.write('ui_print(" TweakZip");\n')
	fh.write('ui_print("----------");\n')
	fh.write('show_progress(1, 10);\n')
	if len(sysFiles) > 0:
		fh.write('ui_print("Mounting system...");\n')
		fh.write('run_program("/sbin/busybox", "mount", "/system");\n')
	if len(dataFiles) > 0:
		fh.write('ui_print("Mounting data...");\n')
		fh.write('run_program("/sbin/busybox", "mount", "/data");\n')
	if len(filesToRemove) > 0:
		fh.write('ui_print("Deleting unwanted files...");\n')
		# Prepare the delete string from the list of filesToRemove
		deleteStr = ''
		for file in filesToRemove:
			deleteStr = deleteStr + '"' + file + '"' + ", "
		deleteStr = deleteStr[:-2]	# remove trailing comma and space
		fh.write('delete(' + deleteStr + ');\n')
	if len(sysFiles) > 0:
		fh.write('ui_print("Installing new system files...");\n')
		fh.write('package_extract_dir("system", "/system");\n')
		# Create a list of system files to accurately set file permissions in the script
		for file in sysFiles:
			fh.write('set_perm(0, 0, 0644, "/' + file + '");\n')
	if len(dataFiles) > 0:
		fh.write('ui_print("Copying new data files...");\n')
		fh.write('package_extract_dir("data", "/data");\n')
		for file in dataFiles:
			fh.write('set_perm(0, 0, 0644, "/' + file + '");\n')
	if len(dataFiles) > 0:
		fh.write('ui_print("Unmounting data...");\n')
		fh.write('run_program("/sbin/busybox", "umount", "/data");\n')
	if len(sysFiles) > 0:
		fh.write('ui_print("Unmounting system...");\n')
		fh.write('run_program("/sbin/busybox", "umount", "/system");\n')
	fh.write('ui_print("----------");\n')
	fh.write('ui_print("Installation complete!");\n')
	fh.close()
	print "New updater-script has been written!"
	# Open the log file to save the output of the commands piped below.
	fh = open('log.txt','a+b')
	# TODO: Add error catching down here. Also logging.
	# Create the zip file!
	makeZipFile(fileName+'.zip',['data','META-INF','system'])
	print "Zip file created!"
	pipe = Popen(['java', '-jar', 'signapk.jar', 'certificate.pem', 'key.pk8', fileName+'.zip', fileName+'_signed.zip'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = pipe.stdout.read()
	pipe.wait()
	fh.write(output)	# TODO: Try to figure out why the java output isn't logging properly...
	print "Zip file signed!"
	fh.close()

### Editor for the filesToRemove[] variable.
def removeFiles():
	global filesToRemove
	reprint = True
	while True:
		if reprint == True:
			cls()
			print\
			"-------------------------------------------------\n",\
			"                 Files to remove\n",\
			"-------------------------------------------------\n"
			if len(filesToRemove) > 0:
				i = 1
				for file in filesToRemove:
					print " " + str(i) + ". " + file
					i += 1
			else:
				i = 0
				print " There are currently no files in this list."
			print\
			"\n-------------------------------------------------\n",\
			"\n Please enter a filename to add it to your list.",\
			"\n    You must enter the full file path.",\
			"\n    Remember to include the leading slash!",\
			"\n To remove a filename from the list, enter the",\
			"\n    number next to it.",\
			"\n To go back to the main menu, enter 'Q'.\n"
		entry = raw_input("Please make your entry: ")
		reprint = True
		if entry.isdigit() == True:
			if int(entry) in range(1,len(filesToRemove)+1):
				filesToRemove.pop(int(entry)-1)
			else:
				reprint = False
				print "That is not a valid number in the list."
		elif entry.startswith('/'):
			filesToRemove.append(entry)
		elif entry in ('q','Q'):
			return True
		else:
			reprint = False
			print "Invalid selection!"

### Main menu of the program.
def mainMenu():
	reprint = True
	while True:
		# This will only clear screen and print the menu if reprint is equal to true.
		if reprint == True:
			cls()
			print\
				"-------------------------------------------------\n",\
				"                 TweakZip v" + __version__ + "\n",\
				"-------------------------------------------------\n\n",\
				" 1. Files to be removed\n",\
				"\n",\
				" 3. Build .zip file\n",\
				"\n",\
				" 5. Load configuration\n",\
				" 6. Save configuration\n",\
				" 7. Discard configuration\n",\
				"\n",\
				" 9. Exit program\n\n",\
				"-------------------------------------------------\n"
		entry = raw_input("Please enter a number: ")
		reprint = True	# reset's reprint to its default value
		if entry == '1':
			removeFiles()
		elif entry == '3':
			reprint = False
			buildZip()
		elif entry == '5':
			loadConfig()
		elif entry == '6':
			saveConfig()
		elif entry == '7':
			reprint = False
			resetConfig()
		elif entry in ('9','q','Q'):
			return True
		else:
			reprint = False
			print "Invalid selection!"

### Program initialization code.
if __name__ == "__main__":
	if depCheck():	# Check dependencies
		mainMenu()	# Run program
	else:
		raw_input("The program will now exit. Press Enter to continue.")

# TODO: Add checks for command line arguments. If opened with a config name passed, automatically load that particular configuration.