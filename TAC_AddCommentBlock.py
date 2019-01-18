# Objective
# 1. Read script xml files within folder recursively, avoid batch file
# 2. Check if file is in write mode else stop further operation
# 3. Open the single script file, add the comment block
# 4. Write the additions to the script file.

# will read line by line 
#import os
from xml.etree import ElementTree as ET				# Used to convert XML into Tree Structure
import os
from os import walk
filePath = 'C:\\UserArea\\1_Automation_Tools\\7_GitHub\\WorkRelated\\1_TestFiles\\'
arr_filenames = os.listdir(filePath)  # get all filenames within the given folder into list

# for each filename that matches .Rq.xml, read the file, insert the required data at the required place and write into the same file. 
def AddComment(descText, scriptFile):
	with open(scriptFile, 'r') as xmlScript_file:
		fileLine_List = xmlScript_file.readlines()  # List to hold all lines within the XML

		# Find the required string within each line and capture the index value of the list.
		for lin_num, lin in enumerate(fileLine_List):
			if lin.find("<ItemCollection>") > 0:
				cap_lin_num = lin_num + 1
				break
	
		fileLine_List.insert(cap_lin_num, 
			"""      <Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308">
				  <Caption>Test Comment</Caption>
				  <Comments>""" + descText + """</Comments>
				  <OutputComment>true</OutputComment>
			   </Comment>\n""")
	
		xmlScript_file.close()
	WriteScript(fileLine_List, scriptFile)
		
def WriteScript(scriptLinebyLine, scriptFilePath):
	with open(scriptFilePath, 'w') as xmlScript_file:		
		xmlScript_file.write(''.join(scriptLinebyLine))  
		xmlScript_file.close()
		
def fetchDescriptionValue(inputFile):
	"This function is used to take a filename, parse for Description tag and fetch its value"
	tree = ET.parse(inputFile)  

	root = tree.getroot()
	
	for description in root.iter('Description'):
		return description.text
	

# -- -- Main Program is here ---
folderPath = 'C:\\UserArea\\1_Automation_Tools\\7_GitHub\\WorkRelated\\1_TestFiles\\'
# get all filenames within the given folder into list
for (dirpath, dirnames, filenames) in walk(folderPath):
	for name in filenames:
		if name.find(".xml") > 0:						 # Work only with xml files in a directory
			FullFilePath = os.path.join(dirpath, name)   # Join the path with filename
			print(dirpath)
			#parseTACxml(dirpath, FullFilePath)
			ScriptDescription = fetchDescriptionValue(FullFilePath)
			AddComment(ScriptDescription, FullFilePath)
			#WriteCommentIntoScript(ScriptDescription, whereToAdd, FullFilePath)