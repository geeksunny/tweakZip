__author__ = 'Justin Swanson'
__version__ = '0.1'

import os								# for running system commands & getting directory contents
from subprocess import Popen, PIPE		# For piping system command output to the background.

# Global Variables
fileName = "tweakzip"
filesToRemove = []
commandsToRun = []
#filesToRemove = ["/system/app/CarHomeGoogle.apk","/system/app/Email.apk","/system/app/Exchange.apk"] #debug
#commandsToRun = ["zram enable"] #debug

def cls():
	os.system(['clear','cls'][os.name == 'nt'])

def lsDir(dir = "."):
	list = []
	for dirname, dirnames, filenames in os.walk(dir):
		for filename in filenames:
			list.append(str(os.path.join(dirname, filename)).replace('\\','/'))
			# Runs a string replace that replaces any backslashes with forward slashes. For correct output on Windows hosts.
	return list

def resetConfig():
	global filesToRemove, commandsToRun
	del filesToRemove[:]
	del commandsToRun[:]
	print "Your configuration has been reset!"

def loadConfig():
	global filesToRemove, commandsToRun, fileName
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
				commandsToRun = cfg[1].split(',')
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
					for file in commandsToRun:
						outputStr = outputStr + file + ','
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
				for file in commandsToRun:
					outputStr = outputStr + file + ','
				fh.write(outputStr[:-1])
				fh.close()
				message = "Configuration saved as " + entry + "!"
			except IOError as e:
				print "There was an error saving your configuration!"
				print "  " + str(e)

def buildZip():
	# Scan directories for the file that will be installed
	sysFiles = lsDir("system")
	dataFiles = lsDir("data")
	# If there are no files to install and other instructions for the zip, abort the build proces
	if len(sysFiles) == 0 and len(dataFiles) == 0 and len(filesToRemove) == 0 and len(commandsToRun) == 0:
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
#	if len(commandsToRun) > 0:
#		fh.write('ui_print("Mounting rootfs...");\n')
#		fh.write('run_program("/sbin/busybox", "mount", "/");\n')
	if len(commandsToRun) > 0 or len(sysFiles) > 0:
		fh.write('ui_print("Mounting system...");\n')
		fh.write('run_program("/sbin/busybox", "mount", "/system");\n')
	if len(commandsToRun) > 0 or len(dataFiles) > 0:
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
#	if len(commandsToRun) > 0:
#		fh.write('ui_print("Running custom commands...");\n')
#		fh.write('package_extract_file("commands.sh", "/tmp/commands.sh");\n')
#		fh.write('set_perm(0, 0777, 0777, "/tmp/install.sh");\n')
#		fh.write('run_program("/tmp/install.sh");\n')
	if len(commandsToRun) > 0 or len(dataFiles) > 0:
		fh.write('ui_print("Unmounting data...");\n')
		fh.write('run_program("/sbin/busybox", "umount", "/data");\n')
	if len(commandsToRun) > 0 or len(sysFiles) > 0:
		fh.write('ui_print("Unmounting system...");\n')
		fh.write('run_program("/sbin/busybox", "umount", "/system");\n')
#	if len(commandsToRun) > 0:
#		fh.write('ui_print("Unmounting rootfs...");\n')
#		fh.write('run_program("/sbin/busybox", "umount", "/");\n')
	fh.write('ui_print("----------");\n')
	fh.write('ui_print("Installation complete!");\n')
	fh.close()
	print "New updater-script has been written!"
	# Command script creation
#	fh = open('commands.sh','wb')
#	fh.write('#!/sbin/sh\n')
#	for file in commandsToRun:
#		fh.write(file + '\n')
#	fh.close()
#	print "New commands.sh has been written!"
	# Open the log file to save the output of the commands piped below.
	fh = open('log.txt','a+b')
	# TODO: Add error catching down here. Also logging.
	# Create the zip file!
	pipe = Popen(['7za', 'a', '-r', fileName+'.zip', 'commands.sh', 'data/', 'META-INF/', 'system/'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = pipe.stdout.read()
	pipe.wait()
	fh.write(str(output))
	print "Zip file created!"
	pipe = Popen(['java', '-jar', 'signapk.jar', 'certificate.pem', 'key.pk8', fileName+'.zip', fileName+'_signed.zip'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = pipe.stdout.read()
	pipe.wait()
	fh.write(output)	# TODO: Try to figure out why the java output isn't logging properly...
	print "Zip file signed!"
	fh.close()

def runCommands():
	global filesToRemove, commandsToRun
	reprint = True
	while True:
		if reprint == True:
			cls()
			print \
				"-------------------------------------------------\n",\
				"                 Commands to run\n",\
				"-------------------------------------------------\n"
			if len(commandsToRun) > 0:
				i = 1
				for file in commandsToRun:
					print " " + str(i) + ". " + file
					i += 1
			else:
				i = 0
				print " There are currently no commands in this list."
			print \
				"\n-------------------------------------------------\n",\
				"\n Please enter a command to add it to your list.",\
				"\n To remove a command from the list, enter the",\
				"\n    number next to it.",\
				"\n To go back to the main menu, enter 'Q'.\n"
		entry = raw_input("Please make your entry: ")
		reprint = True
		if entry.isdigit() == True:
			if int(entry) in range(1,len(commandsToRun)+1):
				commandsToRun.pop(int(entry)-1)
			else:
				reprint = False
				print "That is not a valid number in the list."
		elif entry in ('q','Q'):
			return True
		else:
			commandsToRun.append(entry)

def removeFiles():
	global filesToRemove, commandsToRun
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
				" 2. Commands to be run at first boot [Disabled]\n",\
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
		elif entry == '2':
			#runCommands()	# Disabled... Subject for removal if no working method for this is found.
			reprint = False
			print "This is currently not available!"
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
		elif entry == '9':
			return True
		else:
			reprint = False
			print "Invalid selection!"

mainMenu()

# TODO: Add checks for command line arguments. If opened with a config name passed, automatically load that particular configuration!