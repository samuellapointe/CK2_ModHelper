class Province:
	def __init__(self, id, color):
		self.id = id
		self.color = color
		
		# Detect province type (wasteland, ocean, land)
		if (color[2] == 255):
			self.type = "ocean"
		elif (color[0] + color[1] + color[2] <= 32):
			self.type = "wasteland"
		else:
			self.type = "land"
			
		self.name = str(self.id) + "_" + self.type
	
	def getDefinition(self):
		return (
			str(self.id) + ";" +
			str(self.color[0]) + ";" +
			str(self.color[1]) + ";" +
			str(self.color[2]) + ";" +
			"x;x"
		)