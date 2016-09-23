### START CONFIG ####
modPath = "C:/Users/Sam/Desktop/modmaker/northquebec"
### END CONFIG ###

# Imports
import errno
import os
import struct
import utils

from province import Province
from sets import Set

# Functions

# Print for debug
def log(status, message):
	statusString = "[INFO] "
	if (status == 1):
		statusString = "[WARNING] "
	elif (status == 2):
		statusString = "[ERROR] "
	print(statusString + message)
	
# This function checks if file needed to generate the mod is present.
def checkFiles():
	log(0, "Making sure all necessary files are there")
	try:
		os.chdir(modPath)
	except:
		log(2, "Invalid path, check modPath in modmaker.py")
		print("=====")
		print(sys.exc_info()[0])
		
	files = [
		"heatmap.bmp",
		"map/provinces.bmp",
		"map/rivers.bmp",
		"map/terrain.bmp",
		"map/topology.bmp",
		"map/trees.bmp",
		"map/world_normal_height.bmp",
		"map/terrain/colormap.dds",
		"map/terrain/colormap_water.dds"
	]
	
	for file in files:
		fileExists = os.path.isfile(file)
		if fileExists:
			log(0, "OK: " + file)
		else:
			log(2, "File missing: " + file)
			print ("=====")
			raise IOError(errno.ENOENT, os.strerror(errno.ENOENT), file)
			
	print ('------------------------------')

# Parse the provinces.bmp file, find every different province
def parseProvinces():
	log(0, "Parsing provinces")
	mapPath = "map/provinces.bmp"
	with open(mapPath, 'rb') as f:
		data = bytearray(f.read())
		
		# Get location of pixels data
		offset = struct.unpack_from('<L', data, 10)[0]
		imageWidth = struct.unpack_from('<L', data, 18)[0]
		imageHeight = struct.unpack_from('<L', data, 22)[0]
		
		if (imageWidth != 3072 or imageHeight != 2048):
			log(1, "Your map size might not be valid. ")
			log(1, "Recommended is 3072x2048 and yours is " + 
			str(imageWidth) + "x" + str(imageHeight))
		else:
			log(0, "OK: Map size is valid")
		
		bitsPerPixel = struct.unpack_from('<L', data, 28)[0]
		if (bitsPerPixel != 24):
			log(2, "Invalid BMP format")
			errorMsg = "24-bit required, found " + str(bitsPerPixel) + "-bit"
			log(2, errorMsg)
			print("=====")
			raise ValueError(errorMsg)
		else:
			log(0, "OK: BMP is 24-bit")
		
		nbPixels = imageWidth*imageHeight
		lastPixel = offset+nbPixels
		colorSet = Set()
		
		while (offset < lastPixel):
			color = (data[offset+2], data[offset+1], data[offset])
			colorSet.add(color)
			offset+=3
			
	print ('------------------------------')
	return colorSet

# Assign an ID and name to every province
def generateProvinces(colorSet):
	log(0, "Generating province data")
	provinces = []
	cpt = 1
	
	for color in colorSet:
		province = Province(cpt, color)
		
		if (province.type != "wasteland"):
			provinces.append(province)
			cpt+=1
	
	log (0, "Provinces generated")
	print ('------------------------------')
	return provinces

def generateDefinitionFile(provinces):
	definition = "province;red;green;blue;x;x\n"
	for province in provinces:
		definition += province.getDefinition() + "\n"
	
	definitionFile = open("map/definition.csv", "w")
	definitionFile.write(definition)
	definitionFile.close()
	log(0, "OK: definition.csv")

def generatePositionsFile():
	# For now, positions.txt will be empty
	positionsFile = open("map/positions.txt", "w")
	positionsFile.close()

	log(0, "OK: positions.txt")

def generateTerrainFile():
	# For now, terrain.txt will be empty
	terrainFile = open("map/terrain.txt", "w")
	terrainFile.close()

	log(0, "OK: terrain.txt")

def generateContinentFile():
	# For now, continent.txt will be empty
	continentFile = open("map/continent.txt", "w")
	continentFile.close()
	
	log(0, "OK: continent.txt")

def generateAdjacenciesFile():
	# Nothing important for now
	adjacenciesFile = open("map/adjacencies.csv", "w")
	adjacenciesFile.write("From;To;Type;Through;-1;-1;-1;-1;Comment")
	adjacenciesFile.close()

	log(0, "OK: adjacencies.csv")

def generateClimateFile():
	# For now, climate.txt will be empty
	climateFile = open("map/climate.txt", "w")
	climateFile.close()
	
	log(0, "OK: climate.txt")
	
def generateIslandRegionFile():
	# For now, island_regions.txt will be empty
	islandRegionFile = open("map/island_regions.txt", "w")
	islandRegionFile.close()
	
	log(0, "OK: island_regions.txt")

def generateGeographicalRegionFile():
	# For now, geographical_region.txt will be empty
	geographicalRegionFile = open("map/geographical_region.txt", "w")
	geographicalRegionFile.close()
	
	log(0, "OK: geographical_region.txt")

def generateStatics():
	# Statics folder
	if not os.path.exists("map/statics"):
		os.mkdir("map/statics")
	
	# Static file, we use the same setting as the ones paradox uses
	staticFile = open("map/statics/00_static.txt", "w")
	staticFileContent = (
		'	object = {\n' +
		'		type = "frame3072"\n' +
		'		position = { 3.000 -8.000 3.000 }\n' +
		'		rotation = { 0.000 0.000 0.000 }\n' +
		'		scale = 100.00\n' +
		'	}'
	)
	staticFile.write(staticFileContent)
	staticFile.close()
	
	log(0, "OK: statics/00_static.txt")

def generateSeasons():
	# For now, use the same file as paradox
	seasonsFile = open("map/seasons.txt", "w")
	seasonsFileContent = (
"""winter = {
	start_date=00.12.01
	end_date=00.02.31
}

spring = {
	start_date=00.04.01
	end_date=00.05.1
}

summer = {
	start_date=00.06.01
	end_date=00.09.10
}

autumn = {
	start_date=00.10.10
	end_date=00.10.31
}

tree_winter = {
	start_date=00.11.15
	end_date=00.12.01
}
tree_winter2 = {
	start_date=00.12.20
	end_date=00.01.20
}
tree_spring = {
	start_date=00.02.20
	end_date=00.03.01
}
tree_spring2 = {
	start_date=00.03.20
	end_date=00.04.20
}
tree_summer = {
	start_date=00.05.20
	end_date=00.06.01
}
tree_summer2 = {
	start_date=00.06.20
	end_date=00.09.10
}
tree_autumn = {
	start_date=00.10.01
	end_date=00.10.10
}
tree_autumn2 = {
	start_date=00.10.25
	end_date=00.11.01
}""")
	seasonsFile.write(seasonsFileContent)
	seasonsFile.close()
	
	log(0, "OK: seasons.txt")

def generateSeaZones(provinces):
	seaZones = "\n"
	nbSeaZones = 0
	for province in provinces:
		if province.type == "ocean":
			nbSeaZones+=1
			seaZones += (
			    "sea_zones = {" + 
				str(province.id) + " " + 
				str(province.id) + "}\n"
			)
	
	seaZones += "\nocean_region = {\n"
	seaZones += "    sea_zones = { "
	
	for i in range(1, nbSeaZones + 1):
		seaZones += str(i) + " "
	
	seaZones += "}\n"
	seaZones += "}"
	return seaZones

# Here, we generate various files related to the map
def generateMapFiles(provinces):
	log (0, "Generating map files")
	defaultMap = ""
	
	# Number of provinces is actual number + 1
	nbProvinces = len(provinces) + 1
	
	defaultMap += "max_provinces = " + str(nbProvinces) + "\n"
	
	# Generate definitions.csv
	generateDefinitionFile(provinces)
	
	# Generate positions.txt
	generatePositionsFile()
	
	# Generate terrain.txt
	generateTerrainFile()
	
	# Generate continent.txt
	generateContinentFile()
	
	# Generate adjacencies.csv
	generateAdjacenciesFile()
	
	# Generate climate.txt
	generateClimateFile()
	
	# Generate island_region.txt
	generateIslandRegionFile()
	
	# Generate geographical_region.txt
	generateGeographicalRegionFile()
	
	# Generate statics
	generateStatics()
	
	# Generate seasons.txt
	generateSeasons()
	
	seaZones = generateSeaZones(provinces)
	
	defaultMap += 'definitions = "definition.csv"\n'
	defaultMap += 'provinces = "provinces.bmp"\n'
	defaultMap += 'positions = "positions.txt"\n'
	defaultMap += 'terrain = "terrain.bmp"\n'
	defaultMap += 'rivers = "rivers.bmp"\n'
	defaultMap += 'terrain_definition = "terrain.txt"\n'
	defaultMap += 'heightmap = "topology.bmp"\n'
	defaultMap += 'tree_definition = "trees.bmp"\n'
	defaultMap += 'continent = "continent.txt"\n'
	defaultMap += 'adjacencies = "adjacencies.csv"\n'
	defaultMap += 'climate = "climate.txt"\n'
	defaultMap += 'region = "island_region.txt"\n'
	defaultMap += 'geographical_region = "geographical_region.txt"\n'
	defaultMap += 'static = "statics"\n'
	defaultMap += 'seasons = "seasons.txt"\n'
	defaultMap += seaZones
	
	defaultMap += '\n'
	
	defaultMapFile = open("map/default.map", "w")
	defaultMapFile.write(defaultMap)
	defaultMapFile.close()

	log(0, "OK: default.map")
	
	print ('------------------------------')

# Main function
def main():
	# Check files
	checkFiles()
	
	# Get provinces
	colorSet = parseProvinces()
	
	# Generate province data
	provinces = generateProvinces(colorSet)
	
	# Generate default.map and other files
	generateMapFiles(provinces)

	# End
	log(0, "Finished")
	input()
	
# Call main

main()