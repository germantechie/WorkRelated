# Objective
# 1. Read script xml files within folder recursively, avoid batch file
# 2. Assuming file will be in Write mode, below program is developed, hence not Checking if file is in write mode else stop further operation
# 3. Open the single script file, capture the Description and then add the new comment block before any other operations.
# 4. Write the additions to the script file. If the Description has multiple lines, to show in html Duckcall, replace empty lines with <br>.
# 5. Avoid adding duplicate comment step to script file.
# 6. Code to remove the added comment for all files based on a flag.
# 7. logging of which all files were skipped, updated in a list so that it can be printed to a seperate file.

from xml.etree import ElementTree as ET				# Used to convert XML into Tree Structure
import os, html
from os import walk
 
def storeScriptFile(scriptFile):
	"""This function takes FullFilePath as input and will read the TAC script line by line as bytes, 
	    convert to Unicode text and store in a List object"""
	xmlScriptAsList = []
	with open(scriptFile, 'rb') as xmlScript_file:  # opens in binary mode to read bytes
		for eachLine in xmlScript_file:
			encodedLine = eachLine.decode('utf8')  # converts bytes to Unicode UTF-8 encoding
			encodedLine = encodedLine.rstrip()     # remove trailing whitespaces with CR and LF characters.
			updatedLine = encodedLine + "\n"
			xmlScriptAsList.append(updatedLine)  
	return xmlScriptAsList

def removeCommentFromXML(xmlList, scriptFile):
	""" This function has the logic to find if Comment step for Script Objective is present and then remove it from the xml file."""
	if 'Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308"' in str(xmlList):  # to check if already comment step is added to the script.
		startIndx = endIndx = None
		# Below logic is to find the start and end lines of added comment step, so that it can be removed from the file.
		for indx, line in enumerate(xmlList):
			if startIndx is not None and endIndx is not None:   # This line will control the loop execution to exit when it finds the start and end Comment Tags
				break
			if 'Comment id="96602b49-ea73' in str(line):        # This looks for the first occurence of the given search text
				startIndx = indx
			if "</Comment>" in str(line):                       # This looks for the first occurence of the given search text
				endIndx = indx
			
		strippedXML = xmlList[:startIndx] + xmlList[endIndx+1:] # List concatenation after slicing the required data
		WriteScript(strippedXML, scriptFile)                    # Call the Write function and update the xml file.
		return "Success"
	else:
		return "SKIP"
		#print("removeCommentFromXML::Comment not present in file-", scriptFile)
	
def AddComment(descText, xmlList):
	""" This function has the logic to insert the new comment step at the top section before anything else starts or skip if the file already has the comment step added."""
	if 'Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308"' not in str(xmlList):  # to check if already comment step is added to the script.
		# Find the required string within each line and capture the index value of the list.
		for lin_num, line in enumerate(xmlList):
			if "<ItemCollection>" in str(line):
				cap_lin_num = lin_num + 1
				break
		xmlList.insert(cap_lin_num, 
			""" <Comment id="96602b49-ea73-4a75-afdc-4de8b15a8308">
				  <Caption>Script Objective</Caption>
				  <Comments>""" + descText + """</Comments>
				  <OutputComment>true</OutputComment>
				</Comment>\n""")
		return xmlList # Updated List with new Comment Tag
	else:
		#print("Comment already present, hence, skipping.....")
		return "SKIP"
			
def WriteScript(scriptLinebyLine, scriptFilePath):
	"""This function opens the Script file and overwrites the entire script line by line based on List object passed as argument."""
	with open(scriptFilePath, 'w', encoding='utf-8') as xmlScript_file:		
		for eachLine in scriptLinebyLine:
			xmlScript_file.write(eachLine)
	#print("Write Success!")
	
def fetchDescriptionValue(inputFile):
	"""This function is used to take a filename, parse for Description tag and fetch its value"""
	tree = ET.parse(inputFile)  

	root = tree.getroot()
	
	for description in root.iter('Description'): 
		scriptIntent = description.text
		
		if scriptIntent is not None:  			              # To check if there is an empty Description block in Script XML
			originalDescription = html.escape(scriptIntent)   # Escaping the special characters in text using the html.escape module.
			htmlFriendlyText = originalDescription.replace("\n", "&lt;br&gt;")  # adding <br> for all the newline character found within description since, it will look better in Duckcall.
			return htmlFriendlyText
		else:
			return "Objective is BLANK!"
	
def returnTestScriptFirstLine(sFilePath):
	"""This function is used to read and return only the first line from the given FullFilePath"""
	with open(sFilePath, 'r') as evTestFH:
		Line1 = evTestFH.readline().strip()
		return Line1
		
# -- -- Main Program starts below ---
#addRemoveFlag = 0    # 0 = Add Comment step, don't remove. 
addRemoveFlag = 1   # 1 = Remove Comment step.

logAddComment = []
logSkipRemoveComment = []

folderPath = 'C:\\UserArea\\1_Automation_Tools\\7_GitHub\\WorkRelated\\1_TestFiles\\'
#folderPath = 'C:\\AFS.Claims\\Branches\\R10.7.1.x\\TestScripts\\Automated TestScripts\\US_Locale_Scripts\\Automated_Scripts\\Smoke_Testing'

for (dirpath, dirnames, filenames) in walk(folderPath):  # get all filenames within the given folder into list
	for name in filenames:
		if name.find(".xml") > 0:						 # Work only with xml files in a directory
			FullFilePath = os.path.join(dirpath, name)   # Join the path with filename

			xmlLine1 = returnTestScriptFirstLine(FullFilePath)			
			if "<TestScripts" in xmlLine1:   		# Evaluating if the Testscript is a BatchFile or a ScriptFile.
				#print("test:", FullFilePath)
				if addRemoveFlag == 0:        		# Evaluate if Comment Step has to be added or removed. if block is for Add. elif block is for Remove.
					ScriptDescription = fetchDescriptionValue(FullFilePath)
					scriptInList = storeScriptFile(FullFilePath)
					updatedScriptList = AddComment(ScriptDescription, scriptInList)
					if updatedScriptList != "SKIP":
						WriteScript(updatedScriptList, FullFilePath)
						logAddComment.append("AddSuccess::"+FullFilePath)
					elif updatedScriptList == "SKIP":
						logSkipRemoveComment.append("Skipped::"+FullFilePath)
				elif addRemoveFlag == 1:
					scriptInList = storeScriptFile(FullFilePath)
					status = removeCommentFromXML(scriptInList, FullFilePath)
					if status == "Success":
						logSkipRemoveComment.append("Removed::"+FullFilePath)
					elif status == "SKIP":
						logSkipRemoveComment.append("RemoveSkip::"+FullFilePath)
			else:
				#print("batch:" , FullFilePath)
				logSkipRemoveComment.append("Batch::"+FullFilePath)
print("-----")
print("Add:",logAddComment)
print("non-add:",logSkipRemoveComment)