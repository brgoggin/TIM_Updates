# Import arcpy and other modules
import arcpy
from arcpy import env
import sys, string, os, time, datetime
import csv

# SET TO OVERWRITE
arcpy.env.overwriteOutput = True

#NOTE: Before running the below code, I manually create a geodatabase and "Commitments" point feature class
#with the below column names.

try:

	# Logging script
	myStartDate = str(datetime.date.today())
	myStartTime = time.clock()
	theStartTime = time.ctime()
	print theStartTime

	myStartDate = str(datetime.date.today())
	myStartTime = time.clock()
	theStartTime = time.ctime()
	file = open("C:/Users/bgoggin/Dropbox/SF Planning/Tim Updates/Logs/" + myStartDate + "test"+ ".txt", "w")
	file.write(theStartTime + "\n")
	when =datetime.date.today()
	theDate = when.strftime("%d")
	theDay=when.strftime("%A")
	print theDay
	
	mitigation_layer = "C:/Users/bgoggin/Dropbox/SF Planning/Tim Updates/Staging_Data/sfmta_commitments.gdb/Commitments"
	mitigation_projected = "C:/Users/bgoggin/Dropbox/SF Planning/Tim Updates/Staging_Data/sfmta_commitments.gdb/Commitments_proj"
	mitigation_buffer = "C:/Users/bgoggin/Dropbox/SF Planning/Tim Updates/Staging_Data/sfmta_commitments.gdb/Commitments_buffer"
	arcpy.TruncateTable_management(mitigation_layer)
	file.write("Deleted old feature class table" + "\n")
	cursor = arcpy.da.InsertCursor(mitigation_layer, ['Title', 'Description', 'SHAPE@XY'])
	
	with open('Raw_Data/mitigation.csv', 'rb') as f:
		reader = csv.DictReader(f)
		#reader = [('Title1', 'The project is the construction of a 36-story 262', (-122.4248302, 37.7856142)),
		#('Title2', 'The proposed project would demolish the existing', (-122.4248302, 37.7856142))]

		for row in reader:
			cursor.insertRow((row['Title'], row['Short Description'],(float(row['Longitude']), float(row['Latitude'])))) 
			
	#clean up
	del cursor
			
	theEndTime = time.ctime()
	file.write("End time" + theEndTime + "\n")
	
	#Project feature class
	webmercator = arcpy.SpatialReference(3857)
	arcpy.Project_management(mitigation_layer, mitigation_projected, webmercator)
	print "Projected measures"
	file.write("Projected Measures" + "\n")
	
	#Buffer feature class
	print("\n")
	print "Buffering "
	arcpy.Buffer_analysis(mitigation_projected, mitigation_buffer, "0.25 Miles", "FULL", "ROUND", "NONE", "", "PLANAR")
	print "Projected measures"
	file.write("Buffered Measures" + "\n")
		
	file.write(str(time.ctime()) +": Time Ended")
	file.close()
	
except Exception,e:
	print "Ended badly"
	print str(e)
	print arcpy.GetMessages()
	file.write(str(e))
	file.write(arcpy.GetMessages())
	file.write(str(time.ctime()) +": Ended badly")
	file.close()
	

