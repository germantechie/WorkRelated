# Objective
# 1. Read script xml files within folder recursively, avoid batch file
# 2. Check if file is in write mode else stop further operation
# 3. Open the single script file, capture the Description and then add the new comment block before any other operations.
# 4. Write the additions to the script file.
# 5. Avoid adding duplicate comment step to script file.
# 6. Code to remove the added comment for all files based on a flag.

# work on to know if Comment section is already added into the script.

from xml.etree import ElementTree as ET				# Used to convert XML into Tree Structure
import os, html
from os import walk
 
def AddComment(descText, scriptFile):
	"This function is used to read the script file line by line, parse for Description tag and fetch its value and then call the WriteScript() to add the description as a comment."
	
	with open(scriptFile, 'r') as xmlScript_file:
		fileLine_List = xmlScript_file.readlines()  # List to hold all lines within the XML

		if 'Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308"' not in str(fileLine_List):  # to check if already comment step is added to the script.
			# Find the required string within each line and capture the index value of the list.
			for lin_num, lin in enumerate(fileLine_List):
				if lin.find("<ItemCollection>") > 0:
					cap_lin_num = lin_num + 1
					break
			fileLine_List.insert(cap_lin_num, 
				""" <Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308">
					  <Caption>Script Objective</Caption>
					  <Comments>""" + descText + """</Comments>
					  <OutputComment>true</OutputComment>
					</Comment>\n""")
		
			xmlScript_file.close()  # this statement is not necessary as With statment is used for automatic file closure at the end of its block.
			WriteScript(fileLine_List, scriptFile)
		else:
			RemoveComment()
		

def RemoveComment():
	print("for now")
			
def WriteScript(scriptLinebyLine, scriptFilePath):
	"This function opens the Script file and overwrites the entire script line by line now including the added comment step."
	with open(scriptFilePath, 'w') as xmlScript_file:		
		for eachLine in scriptLinebyLine:
			xmlScript_file.writelines(eachLine)
		#xmlScript_file.write(''.join(scriptLinebyLine))  
		xmlScript_file.close()
		
def fetchDescriptionValue(inputFile):
	"This function is used to take a filename, parse for Description tag and fetch its value"
	tree = ET.parse(inputFile)  

	root = tree.getroot()
	
	for description in root.iter('Description'): 
		scriptIntent = description.text
		
		if scriptIntent is not None:  			 # To check if there is an empty Description block in Script XML
			return html.escape(scriptIntent)     # Escaping the special characters in text using the html.escape module.
		else:
			return "Objective is BLANK!"
	
def returnTestScriptFirstLine(sFilePath):
	with open(sFilePath, 'r') as evTestFH:
		Line1 = evTestFH.readline().strip()
		return Line1
		
# -- -- Main Program starts here ---
folderPath = 'C:\\UserArea\\1_Automation_Tools\\7_GitHub\\WorkRelated\\1_TestFiles\\'
#folderPath = 'C:\\AFS.Claims\\Branches\\R10.7.1.x\\TestScripts\\Automated TestScripts\\US_Locale_Scripts\\Automated_Scripts\\Smoke_Testing'
# get all filenames within the given folder into list
for (dirpath, dirnames, filenames) in walk(folderPath):
	for name in filenames:
		if name.find(".xml") > 0:						 # Work only with xml files in a directory
			FullFilePath = os.path.join(dirpath, name)   # Join the path with filename
			#print(FullFilePath)
			xmlLine1 = returnTestScriptFirstLine(FullFilePath)
			#print(xmlLine1)
			if "<TestScripts" in xmlLine1:   # Evaluating if the Testscript is a BatchFile or a ScriptFile.
				print("test:", FullFilePath)
				ScriptDescription = fetchDescriptionValue(FullFilePath)
				AddComment(ScriptDescription, FullFilePath)
			else:
				print("batch:" , FullFilePath)