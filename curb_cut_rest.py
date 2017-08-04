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
file = open(root + "Logs/" + myStartDate + "curb_cut_rest"+ ".txt", "w")
file.write(theStartTime + "\n")
when =datetime.date.today()
theDate = when.strftime("%d")
theDay=when.strftime("%A")
print theDay

try:
	#NOTE: The street segment polygons layer ("ROWPolygons") is the layer already existing in TIM as of July 2017. I was originally plannning
	#on merging street segment polygons with curb cut restrictions in order to view street segments next to a parcel. However, it seems like
	#that is better to be consistent with how other streets layers currently operate in TIM for now. Commenting out code about merging with
	#streets polygons for now. That is, for now I am just doing a 250 foot buffer.
	raw_layer = root + "Raw_Data/ROWPolygons.shp"
	merge_layer = root + "Raw_Data/CurbCuts.gdb/CurbCutRestrictions"
	#arcpy.MakeFeatureLayer_management (root + "Raw_Data/ROWPolygons.shp", "base_layer")
	#arcpy.MakeFeatureLayer_management(root + "Raw_Data/CurbCuts.gdb/CurbCutRestrictions","merge_Layer") 
	#projected_layer = root + "Staging_Data/CurbCuts.gdb/ROW_CurbCuts_Proj"
	projected_layer = root + "Staging_Data/CurbCuts.gdb/CurbCuts_Proj"
	#buffer_layer = root + "Raw_Data/CurbCuts.gbd/CurbCutRestrictions_Buffer"
	buffer_layer = "C:\\Users\\bgoggin\\Dropbox\\SF_Planning\\TIM_Updates\\Staging_Data\\CurbCuts.gdb\\CurbCutRestrictions_Buffer"
	
	#Commenting out merging procedure below. Just buffering curb cuts layer for now.
	#print "Merging fields"
	#arcpy.JoinField_management(raw_layer, "CNNTEXT", merge_layer, "cnn", ["curbcutcode", "code_note"]) don't want to use this because it makes changes to raw input data
	#still not merging correctly, not sure why
	#arcpy.AddJoin_management("base_layer", "CNNTEXT", "merge_Layer", "cnn", "KEEP_COMMON")
	#file.write("Merged")

	print("\n")
	print "Projecting"
	webmercator = arcpy.SpatialReference(3857)
	arcpy.Project_management(merge_layer, projected_layer, webmercator)
	print "Projected"
	file.write("Projected" + "\n")
	
	#Buffer
	print("\n")
	print "Buffering "
	arcpy.Buffer_analysis(projected_layer, buffer_layer, "250 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
	
	#output from manual example below
	#arcpy.Buffer_analysis(CurbCuts_Proj, CurbCutRestrictions_Buffer, "250 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
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