import numpy
import operator
import sys
import random
import time


class Heuristic:
	def __init__(self, path):
		self.path = path
		self.distance = 0
		self.heuristic = 0.0

	def calculate_path_distance(self):
		if self.distance == 0:

			total_dist = 0
			for i in range(len(self.path) - 1):
				total_dist += self.path[i].calc_distance(self.path[i + 1])

			total_dist += self.path[len(self.path) - 1].calc_distance(self.path[0])
			self.distance = total_dist
		return self.distance

	def calculate_path_heuristic(self):
		if self.heuristic == 0:
			self.heuristic = 1/float(self.calculate_path_distance())
		return self.heuristic


class City:
    def __init__(self, x, y, city_id):
        self.x = x
        self.y = y
        self.id = city_id
        self.numpy_array = numpy.array((x, y))

    def calc_distance(self, city):
        return int(numpy.linalg.norm(self.numpy_array - numpy.array((city.x, city.y))))


def main():
	input_filename = sys.argv[1]
	output_filename = sys.argv[2]
	target_time = int(sys.argv[3])
	start_time = time.time()

	# create the City objects from the txt file
	cities = []
	for city_id, x, y in create_node_list(input_filename):
		city = City(x, y, city_id)
		cities += [city]

	# set genetic algorithm hyperparameters
	init_pop_size = 100
	elite_size = 20
	mutation_rate = 0.01

	# randomly shuffle the cities and create initial population
	pop = []
	for i in range(init_pop_size):
		random.shuffle(cities)
		pop += [cities]

	# continuously create new generations until timer runs out
	while (time.time() - start_time) < target_time:
		pop = next_gen(pop, elite_size, mutation_rate)

	final_path_id = rank_paths(pop)[0][0]
	final_cycle = pop[final_path_id]

	final_heuristic = rank_paths(pop)[0][1]
	final_dist = 1/final_heuristic

	write_to_file(output_filename, final_cycle, final_dist)


def write_to_file(output_filename, bestroute, final):
	# open file for reading
	try:
		fh = open(output_filename, 'r')
		print(int(final))
		fh.write(str(int(final)) + '\n')
		bestroute += [bestroute[0]]
		for node in bestroute:
			fh.write(str(node.id) + ' ')
		fh.write('\n')
	except:
		# if file does not exist, create it
		fh = open(output_filename, 'w')
		fh.write(str(int(final)) + '\n')
		bestroute += [bestroute[0]]
		for node in bestroute:
			fh.write(str(node.id) + ' ')
		fh.write('\n')


# returns a list of lists of integers as [[node ID, x coord, y coord], ...]
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
				node += [int(elem)]
			nodes += [node]
	return nodes


# produce the next generation of paths
def next_gen(curr_generation, elite_size, mutation_rate):
	ranked_pops = rank_paths(curr_generation)

	selected_paths = select_fittest(ranked_pops, elite_size)

	# create mating pool of superior paths
	mating_pool = []
	for i in range(len(selected_paths)):
		mating_pool += [curr_generation[selected_paths[i]]]

	# breed the mating pool to create children
	children = []
	random.shuffle(mating_pool)
	for i in range(elite_size):
		children += [mating_pool[i]]

	for i in range(len(mating_pool) - elite_size):
		child = crossover(mating_pool[i], mating_pool[len(mating_pool) - i - 1])
		children += [child]

	# mutate the children based on mutation_rate
	mutated = []
	for ind in range(len(children)):
		index = mutate(children[ind], mutation_rate)
		mutated += [index]

	return mutated


# ranks the paths based on their heuristics (1/total_dist) in desc order
def rank_paths(paths):
	pathid_to_heuristic = {}
	for pathid in range(len(paths)):
		pathid_to_heuristic[pathid] = Heuristic(paths[pathid]).calculate_path_heuristic()
	return sorted(pathid_to_heuristic.items(), key=operator.itemgetter(1), reverse=True)


# selects which paths proceed
def select_fittest(pop, top_n):
	selected_paths = []

	# suitably adjusts the likelihood of each path's survival based on its heuristic
	current_total_cost = 0
	ids_to_selection_prob = {}
	for path_id in range(len(pop)):
		current_total_cost += pop[path_id][1]
		ids_to_selection_prob[path_id] = pop[path_id][1] / current_total_cost

	# top 20 paths auto pass
	for i in range(top_n):
		selected_paths += [pop[i][0]]

	# remaining 80 paths
	for j in range(len(pop) - top_n):
		pick = random.random()

		for i in range(len(pop)):
			if pick <= ids_to_selection_prob[i]:
				selected_paths += [pop[i][0]]
				break

	return selected_paths


# takes random size substring of parent1 and fills remaining child space with parent2
def crossover(parent1, parent2):
	left_half_child = []
	for i in range(random.randint(0, len(parent1)), random.randint(0, len(parent1))):
		left_half_child += [parent1[i]]

	right_half_child = []
	for item in parent2:
		if item not in left_half_child:
			right_half_child += [item]

	return left_half_child + right_half_child


# prevents getting stuck in local optima by randomly mutating cities in our path
def mutate(path, mutation_rate):
	for city in range(len(path)):
		r = random.random()
		if r < mutation_rate:
			path[city], path[int(r * len(path))] = path[int(r * len(path))], path[city]
	return path


if __name__ == "__main__":
	main()
