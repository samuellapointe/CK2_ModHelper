### START CONFIG ####
modPath = "C:/Users/Sam/Desktop/modmaker/northquebec"
### END CONFIG ###

# Imports
import errno
import os
import struct

# Functions

# Print for debug
def log(status, message):
	statusString = "[INFO] "
	if (status == 1):
		statusString = "[ERROR] "
	elif (status == 2):
		statusString = "[WARNING] "
	print(statusString + message)
	
# This function checks if file needed to generate the mod is present.
def checkFiles():
	log(0, "Making sure all necessary files are there")
	try:
		os.chdir(modPath)
	except:
		log(1, "Invalid path, check modPath in modmaker.py")
		print("=====")
		print(sys.exc_info()[0])
		
	files = [
		"heatmap.bmp",
		"map/provinces.bmp",
		"map/rivers.bmp",
		"map/terrain.bmp",
		"map/topology.bmp",
		"map/trees.bmp",
		"map/world_normal_height.bmp"
	]
	
	for file in files:
		fileExists = os.path.isfile(file)
		if fileExists:
			log(0, "OK: " + file)
		else:
			log(1, "File missing: " + file)
			print ("=====")
			raise IOError(errno.ENOENT, os.strerror(errno.ENOENT), file)
			
	print ('------------------------------')
			
def readProvinces():
	log(0, "Parsing provinces")
	mapPath = "map/provinces.bmp"
	with open(mapPath, 'rb') as f:
		data = bytearray(f.read())
		
		# Get location of pixels data
		offset = struct.unpack_from('<L', data, 10)[0]
		imageWidth = struct.unpack_from('<L', data, 18)[0]
		imageHeight = struct.unpack_from('<L', data, 22)[0]
		
		if (imageWidth != 3072 or imageHeight != 2048):
			log(2, "Your map size might not be valid. ")
			log(2, "Recommended is 3072x2048 and yours is " + 
			str(imageWidth) + "x" + str(imageHeight))
		else:
			log(0, "OK: Map size is valid")
		
		bitsPerPixel = struct.unpack_from('<L', data, 28)[0]
		if (bitsPerPixel != 24):
			log(1, "Invalid BMP format")
			errorMsg = "24-bit required, found " + str(bitsPerPixel) + "-bit"
			log(1, errorMsg)
			print("=====")
			raise ValueError(errorMsg)
		else:
			log(0, "OK: BMP is 24-bit")
			
	print ('------------------------------')
	
# Main function
def main():
	# Check files
	checkFiles()
	
	# Get provinces
	readProvinces()

	# End
	log(0, "Finished")
	input()
	
# Call main

main()