# Import arcpy and other modules
import arcpy
from arcpy import env
import sys, string, os, time, datetime
import csv

# SET TO OVERWRITE
arcpy.env.overwriteOutput = True

#Create Directory file path
root = "C:/Users/bgoggin/Dropbox/SF_Planning/Tim_Updates/"

# Logging script
myStartDate = str(datetime.date.today())
myStartTime = time.clock()
theStartTime = time.ctime()
print theStartTime
file = open(root + "Logs/" + myStartDate + "keywalkingstreets"+ ".txt", "w")
file.write(theStartTime + "\n")
when =datetime.date.today()
theDate = when.strftime("%d")
theDay=when.strftime("%A")
print theDay

try:
	#NOTE: raw data was downloaded via email from Paul Chasan on June 20, 2017.
	raw_layer = root + "Raw_Data/KeyWalkingStreets.shp"
	dissolve_layer = root + "Staging_Data/Ped_Network.gdb/key_walking_streets_dissolve"
	projected_layer = root + "Staging_Data/Ped_Network.gdb/key_walking_streets_proj"
	buffer_layer = root + "Staging_Data/Ped_Network.gdb/key_walking_streets_buff"
	
	
	#Dissolve
	print("\n")
	print "Dissolving "
	arcpy.Dissolve_management(raw_layer, dissolve_layer, "STREETNAME", "", "MULTI_PART", "DISSOLVE_LINES")
	print "Dissolved"
	file.write("Dissolved" + "\n")
	
	#Project
	print("\n")
	print "Projecting "
	webmercator = arcpy.SpatialReference(3857)
	arcpy.Project_management(dissolve_layer, projected_layer, webmercator)
	print "Projected"
	file.write("Projected" + "\n")
	
	#Buffer
	print("\n")
	print "Buffering "
	arcpy.Buffer_analysis(projected_layer, buffer_layer, "250 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
	print "Buffered"
	file.write("Buffered" + "\n")
		
	file.write(str(time.ctime()) +": Time Ended")
	file.close()
	
except Exception,e:
	print "Ended badly"
	print str(e)
	print arcpy.GetMessages()
	file.write(str(e) + "\n")
	#file.write(arcpy.GetMessages() + "\n") I don't totally understand what arcpy.GetMessages() does
	file.write(str(time.ctime()) +": Ended badly")
	file.close()
