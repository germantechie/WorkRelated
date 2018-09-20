from xml.etree import ElementTree as ET				# Used to convert XML into Tree Structure
import os
from os import walk

# ---- What am I doing here? --
# > This script is written to parse the TAC xml scripts and find and replace those instances where dynamic Wait statement has the time set to less than 5000 ms.
# > It is replaced to 5000ms so that performance of the script can be made better.

def parseTACxml(inputFile):
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
				print(WaitInt.attrib, ":", whichWaitStatement, ":", WaitTime)


	print("Total to be rectified:",cnt)

# -- -- Main Program is here ---
FullFilePath = 'C:\\Tom_DataFolder\\AT081_TAC_Changed.xml'
parseTACxml(FullFilePath)
	
print("------------ All DONE ------------------")	
