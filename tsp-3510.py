import sys
import numpy

def main():
	input_filename = sys.argv[1]
	output_filename = sys.argv[2]
	target_time = sys.argv[3]

	nodes = create_node_list(input_filename)

	dist_array = create_dist_array(nodes)

	optimal_cycle, dist = find_optimal_cycle(dist_array)

	write_to_file(output_filename, optimal_cycle, dist)


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
			if node.index(sorted(node)[i]) not in visited_nodes:
				visited_nodes += [node.index(sorted(node)[i])]

	dist = 0
	for i in range(len(visited_nodes) - 1):
		dist += dist_array[i][i + 1]

	# increment by 1 to translate from index -> node ID
	visited_nodes = [str(x + 1) for x in visited_nodes]
	visited_nodes += visited_nodes[0]
	return visited_nodes, dist


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
