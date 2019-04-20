import numpy
import sys
import random
import operator
import pandas
import time


class City:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def calc_distance(self, city):
        distancex = abs(self.x - city.x)
        distancey = abs(self.y - city.y)
        return numpy.sqrt((distancex ** 2) + (distancey **2))


class Heuristic:

	def __init__(self, path):
		self.path = path
		self.distance = 0
		self.heuristic = 0.0

	def pathDistance(self):
		if (self.distance == 0):
			pathDistance = 0
			for i in range(0, len(self.path)):
				fromCity = self.path[i]
				toCity = None
				if (i + 1 < len(self.path)):
					toCity = self.path[i + 1]
				else:
					toCity = self.path[0]
				pathDistance += fromCity.calc_distance(toCity)
			self.path = pathDistance
		return self.path

	def pathHeuristic(self):
		if self.heuristic == 0:
			self.heuristic = 1 / float(self.pathDistance())
		return self.heuristic


def main():
	input_filename = sys.argv[1]
	output_filename = sys.argv[2]
	target_time = sys.argv[3]

	nodes = create_node_list(input_filename)
	cityList = []
	for node in nodes:
		cit = City(node[1], node[2])
		cityList.append(cit)
	bestroute, initialdistance, finaldistance = geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=1000)
	write_to_file(output_filename, bestroute, initialdistance, finaldistance)


def write_to_file(output_filename, bestroute, initial, final):
	# open file for reading
	try:
		fh = open(output_filename, 'r')
		fh.write(str(bestroute) + '\n')
		fh.write(str(final) + '\n')
	except:
		# if file does not exist, create it
		fh = open(output_filename, 'w')
		fh.write(str(bestroute) + '\n')
		fh.write(str(final) + '\n')


def create_node_list(input_filename):
	file = open(input_filename, "r")
	lines = file.read().split('\n')
	nodes = []
	for line in lines:
		node = []
		line.strip()
		if len(line) > 4:
			for elem in line.split(' '):
				if '.' in elem:
					elem = float(elem)
				node.append(int(elem))
			nodes.append(node)
	return nodes


def createPath(cityList):
	#creates a random path based on all cities
	path = random.sample(cityList, len(cityList))
	return path


def initialPopulation(popSize, cityList):
	#creates the 1st generation of routes
	#will create popSize number of routes in the population
	pop = []
	for i in range(0, popSize):
		pop.append(createPath(cityList))
	return pop


def rankPaths(population):
	heuristic_results = {}
	for i in range(len(population)):
		heuristic_results[i] = Heuristic(population[i]).pathHeuristic()
	return sorted(heuristic_results.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop, top_n):
	selected_paths = []

	current_total_cost = 0
	ids_to_selection_prob = {}
	for path_id in range(len(pop)):
		current_total_cost += pop[path_id][1]
		ids_to_selection_prob[path_id] = pop[path_id][1]/current_total_cost

	# top 20 paths auto pass
	for i in range(top_n):
		selected_paths += [pop[i][0]]

	# 0 - 80
	for j in range(len(pop) - top_n):
		pick = random.random()

		# 0 - 100
		for i in range(len(pop)):
			if pick <= ids_to_selection_prob[i]:
				selected_paths += [pop[i][0]]
				break

	return selected_paths


def matingPool(population, selected_paths):
	pool = []
	for i in range(len(selected_paths)):
		pool += [population[selected_paths[i]]]
	return pool


def crossover(parent1, parent2):
	left_half_child = []
	for i in range(random.randint(0, len(parent1)), random.randint(0, len(parent1))):
		left_half_child += [parent1[i]]

	right_half_child = []
	for item in parent2:
		if item not in left_half_child:
			right_half_child += [item]

	return left_half_child + right_half_child


def breedPopulation(matingpool, eliteSize):
	children = []
	length = len(matingpool) - eliteSize
	pool = random.sample(matingpool, len(matingpool))

	for i in range(0,eliteSize):
		children.append(matingpool[i])
	
	for i in range(0, length):
		child = crossover(pool[i], pool[len(matingpool)-i-1])
		children.append(child)
	return children


def mutate(individual, mutationRate):
	for swapped in range(len(individual)):
		if(random.random() < mutationRate):
			swapWith = int(random.random() * len(individual))
			
			city1 = individual[swapped]
			city2 = individual[swapWith]
			
			individual[swapped] = city2
			individual[swapWith] = city1
	return individual


def mutatePopulation(population, mutationRate):
	mutatedPop = []
	
	for ind in range(0, len(population)):
		mutatedInd = mutate(population[ind], mutationRate)
		mutatedPop.append(mutatedInd)
	return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate):
	popRanked = rankPaths(currentGen)
	selectionResults = selection(popRanked, eliteSize)
	matingpool = matingPool(currentGen, selectionResults)
	children = breedPopulation(matingpool, eliteSize)
	nextGeneration = mutatePopulation(children, mutationRate)
	return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
	pop = initialPopulation(popSize, population)
	print("Initial distance: " + str(1 / rankPaths(pop)[0][1]))
	initialDistance = 1 / rankPaths(pop)[0][1]
	
	for i in range(0, generations):
		pop = nextGeneration(pop, eliteSize, mutationRate)
	
	print("Final distance: " + str(1 / rankPaths(pop)[0][1]))
	bestRouteIndex = rankPaths(pop)[0][0]
	bestRoute = pop[bestRouteIndex]
	finalDistance = 1 / rankPaths(pop)[0][1]
	return bestRoute, initialDistance, finalDistance


if __name__ == "__main__":
	main()
