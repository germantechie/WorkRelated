from xml.etree import ElementTree as ET				# Used to convert XML into Tree Structure
import os
from os import walk

# ---- What am I doing here? --
# > This script is written to parse the TAC xml scripts and find and replace those instances where dynamic Wait statement has the time set to less than 5000 ms.
# > It is replaced to 5000ms so that performance of the script can be made better.

def parseTACxml(DirNAME, inputFile):
	"This function is used to take a filename, parse for WaitTime less than 5000ms and change to 5000ms"
	tree = ET.parse(inputFile)  

	root = tree.getroot()
	cnt = 0
	for WaitInt in root.iter('Wait'):
		whichWaitStatement = WaitInt.find('ActionKeyword').text
		if(whichWaitStatement != "StaticWait"):                       # Find ActionKeyword that is not StaticWait
			WaitTime = int(WaitInt.find('WaitTime').text)			  # converting the time value text to int
			if(WaitTime < 5000):  									  # Work upon those values whose time is less than 5000ms
				cnt = cnt + 1
				WaitInt.find('WaitTime').text = str(5000)
				print(WaitInt.attrib, ":", whichWaitStatement, ":", WaitTime, ":", WaitInt.find('WaitTime').text)
				

	print("Total to be rectified:",cnt)
	outPutFile = DirNAME + "output.xml"
	tree.write(outPutFile)

# -- -- Main Program is here ---
folderPath = 'C:\\1_Automation_Tools\\3_Python\\2_Page_Manuscript_Parsing\\TAC\\'
# get all filenames within the given folder into list
for (dirpath, dirnames, filenames) in walk(folderPath):
	for name in filenames:
		if name.find(".xml") > 0:						 # Work only with xml files in a directory
			FullFilePath = os.path.join(dirpath, name)   # Join the path with filename
			print(dirpath)
			parseTACxml(dirpath, FullFilePath)
	
print("------------ All DONE ------------------")	
