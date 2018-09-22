import xml.dom.minidom	as MINI	
from xml.dom.minidom import Node		
import os
from os import walk

# ---- What am I doing here? --
# > This script is written to parse the TAC xml scripts and find and replace those instances where dynamic Wait statement has the time set to less than 5000 ms.

def parseTACxml(inputFile):
	"This function is used to take a filename, parse for WaitTime less than 5000ms and change to 5000ms"
	DOMTree = MINI.parse(inputFile)  
	
	cnt = 0
	WaitCollection = DOMTree.getElementsByTagName('Wait')   # Find <Wait> nodes in entire document
	for totWait, WC in enumerate(WaitCollection):           # Loop through all Wait blocks found
		foundFlag = False				# Initialize every loop with False flag.
		for children in WC.childNodes:	                # Loop through all sub-nodes within the <Wait> ... </Wait> block
			if (children.nodeType == Node.ELEMENT_NODE):	
				if(children.tagName == 'ActionKeyword' and children.firstChild.data != "StaticWait"): 						foundFlag = True	# To identify Dynamic Wait block
				if(children.tagName == 'WaitTime' and int(children.firstChild.data) < 5000 and foundFlag == True):
					print(children.nodeName, children.firstChild.data)
					children.firstChild.replaceWholeText("5000")	# Replacing with 5000 				
					cnt = cnt + 1
		
	print("Total Wait:-", totWait, "\nWait < 5sec:-", cnt )	
	
	f = open("/home/tom/Documents/DuckWork/sampleOutput.xml", "w+")	
	DOMTree.writexml(f)	
	f.close()

# -- -- Main Program is here ---
folderPath = '/home/tom/Documents/DuckWork/AT081_TAC_Changed.xml'
# get all filenames within the given folder into list and pass it to the parsing function.
# for (dirpath, dirnames, filenames) in walk(folderPath):
	# for name in filenames:
		# if name.find(".xml") > 0:						 # Work only with xml files in a directory
			# FullFilePath = os.path.join(dirpath, name)   # Join the path with filename
			# print("Fetching files from :", dirpath)
			# parseTACxml(dirpath, FullFilePath)
parseTACxml(folderPath)
			
print("------------ All DONE ------------------")	
