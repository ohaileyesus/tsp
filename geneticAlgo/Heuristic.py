class Heuristic:
	def _init_(self, path):
		self.path = path;
		self.distance = 0;
		self.heuristic = 0.0;

	def pathDistance(self):
		if (self.distance == 0):
			pathDistance = 0
			for i in range(0, len(self.path)):
				fromCity = path[i]
				toCity = None
				if (i + 1 < len(self.path)):
					toCity = self.path[i + 1]
				else:
					toCity = self.path[0]
				pathDistance += fromCity.distance(toCity)
			self.path = pathDistance
		return self.path

	def pathHeuristic(self):
		if (self.heuristic == 0):
			self.heuristic = 1 / float(self.pathDistance())
		return self.heuristic
