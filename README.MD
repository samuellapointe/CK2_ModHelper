This script creates a Crusader Kings 2 mod from bitmap files. It is not 
functional yet. Some guidelines apply.

## Configuration

TODO, for now put values in the first lines of modmaker.py

## Guidelines for image files

#### provinces.bmp

The program can't guess from the outline of your map which provinces will be 
water and which ones will be land. To deal with this, follow the following 
guidelines when creating your provinces.bmp file:

 * Provinces with the Blue value set to 255 are considered to be ocean (65 536 possible values). 
   
  Examples: [21, 35, 255], [0, 0, 255], [128, 255, 255]

 * Provinces where the sum of color values is equal or below 32 are considered to be wastelands (32 768 possible values)
 
  Examples: [0, 0, 32], [16, 0, 8], [0, 0, 0]

 * Other provinces will be land provinces. (16 678 912 possible values)
