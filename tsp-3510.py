import sys
import numpy
import itertools
import datetime


def main():
	input_filename = sys.argv[1]
	output_filename = sys.argv[2]
	target_time = sys.argv[3]

	nodes = create_node_list(input_filename)

	dist_array = create_dist_array(nodes)

	initial_cycle, init_dist = find_optimal_cycle(dist_array)

	final_cycle, final_dist = optimize(initial_cycle, init_dist, dist_array)

	write_to_file(output_filename, final_cycle, final_dist)


# input_filename is the name of the file containing the node info
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


# nodes is a list of lists of [node ID, x coord, y coord]
# returns a 2d array of the distances between every any node1 to any other node2
def create_dist_array(nodes):
	dist_array = []
	for node1 in nodes:
		dist_from_node1 = []
		for node2 in nodes:
			one = numpy.array((node1[1], node1[2]))
			two = numpy.array((node2[1], node2[2]))
			dist_from_node1 += [int(numpy.linalg.norm(one - two))]
		dist_array += [dist_from_node1]
	return dist_array


# dist_array is the 2d distance array
# returns the optimal cycle as string list
# returns round-trip distance
def find_optimal_cycle(dist_array):
	visited_nodes = []
	for node in dist_array:
		for i in range(1, len(node)):
			if str(node.index(sorted(node)[i]) + 1) not in visited_nodes:
				visited_nodes += [str(node.index(sorted(node)[i]) + 1)]

	# make the list a cycle by appending first node to end
	visited_nodes += [visited_nodes[0]]

	total_dist = 0
	for i in range(len(visited_nodes) - 1):
		first = visited_nodes[i]
		second = visited_nodes[i + 1]
		total_dist += dist_array[int(first) - 1][int(second) - 1]

	return visited_nodes, total_dist


# calculates round trip distance of the given cycle
def calculate_dist(cycle, dist_array):
	total_dist = 0
	for i in range(len(cycle) - 1):
		first = cycle[i]
		second = cycle[i + 1]
		total_dist += dist_array[int(first) - 1][int(second) - 1]
	return total_dist


# optimizes the given initial_cycle
def optimize(initial_cycle, init_dist, dist_array):
	curr_dist = init_dist
	curr_cycle = initial_cycle[0:len(initial_cycle) - 1]
	start = datetime.datetime.now()

	# 2-opt
	# for i in range(len(curr_cycle)):
	# 	for j in range(len(curr_cycle)):
	# 		new_cycle = curr_cycle
	#
	# 		temp = new_cycle[i]
	# 		new_cycle[i] = new_cycle[j]
	# 		new_cycle[j] = temp
	#
	# 		new_dist = calculate_dist(new_cycle, dist_array)
	# 		if new_dist < curr_dist:
	# 			curr_cycle = new_cycle
	# 			curr_dist = new_dist
	#
	# 3-opt
	# for i in range(len(curr_cycle)):
	# 	for j in range(len(curr_cycle)):
	# 		for k in range(len(curr_cycle)):
	# 			new_cycle = curr_cycle
	# 			if i is not j and j is not k and i is not k:
	# 				for triplet in list(itertools.permutations([new_cycle[i], new_cycle[j], new_cycle[k]])):
	# 					new_cycle[i] = triplet[0]
	# 					new_cycle[j] = triplet[1]
	# 					new_cycle[k] = triplet[2]
	#
	# 					new_dist = calculate_dist(new_cycle, dist_array)
	# 					if new_dist < curr_dist:
	# 						curr_cycle = new_cycle
	# 						curr_dist = new_dist
	#
	# 4-opt
	for i in range(len(curr_cycle)):
		for j in range(len(curr_cycle)):
			for k in range(len(curr_cycle)):
				for l in range(len(curr_cycle)):
					new_cycle = curr_cycle
					if i is not j and i is not k and i is not l and j is not k and j is not l and k is not l:
						for quad in list(itertools.permutations([new_cycle[i], new_cycle[j], new_cycle[k], new_cycle[l]])):
							if curr_dist < 28000: break

							new_cycle[i] = quad[0]
							new_cycle[j] = quad[1]
							new_cycle[k] = quad[2]
							new_cycle[l] = quad[3]

							new_dist = calculate_dist(new_cycle, dist_array)
							if new_dist < curr_dist:
								curr_cycle = new_cycle
								curr_dist = new_dist
							# print(curr_dist)

	print(datetime.datetime.now() - start)
	print(curr_dist)
	return curr_cycle, curr_dist


# params are self-explanatory lol
def write_to_file(output_filename, optimal_cycle, dist):
	# open file for reading
	try:
		fh = open(output_filename, 'r')
		fh.write(str(dist) + '\n')
		fh.write(' '.join(optimal_cycle))
	except:
		# if file does not exist, create it
		fh = open(output_filename, 'w')
		fh.write(str(dist) + '\n')
		fh.write(' '.join(optimal_cycle))


if __name__ == "__main__":
	main()
