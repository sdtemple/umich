import tskit
# import msprime
import numpy as np
import sys
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(description='Fill matrices for genotype data and rank order topology.')

# Define required arguments with named options
parser.add_argument('--input_file', 
                    type=str, 
                    required=True, 
                    help='File name for input')
parser.add_argument('--output_prefix', 
                    type=str, 
                    required=True, 
                    help='Folder name for output')
parser.add_argument('--num_markers', 
                    type=int, 
                    required=True, 
                    help='How markers after tree right end to capture')
# parser.add_argument('--rounding_number', 
#                     type=int,
#                     default=4,  
#                     help='How many decimal places for the coalescent times')

# Parse the arguments
args = parser.parse_args()
input_file = args.input_file
output_prefix = args.output_prefix
num_markers = args.num_markers

trees = tskit.load(input_file)
full_matrix = trees.genotype_matrix()

# nodes in tree sequence should already be rank ordered
assert np.all(np.diff(trees.tables.nodes.time) >= 0)

# code to get the genotype matrices
sites = trees.tables.sites.position
num_trees = trees.num_trees
num_nodes = trees.num_nodes
itr = 0

### SAVE THE CURRENT AND NEXT TREES AND THE NEXT XX MARKERS

### THIS CREATES SOME REDUNDANT DATA STORAGE
### BUT MAY BE MORE USER FRIENDLY

for i in range(num_trees-1):

    current_tree = trees.at_index(i)
    next_tree = trees.at_index(i+1)

    # initialize the topology
    current_rank_topology = np.zeros((num_nodes,num_nodes))
    next_rank_topology = np.zeros((num_nodes,num_nodes))

    itr += 1
    if itr < num_trees:

        # capture the marker data
        right = current_tree.interval.right
        mask = sites > right
        try:
            first_index = np.nonzero(mask)[0][0]
        # happens at the last tree
        except Exception as e:
            sys.exit(0)
        sites = sites[first_index:,]
        sub_matrix = full_matrix[first_index:(first_index+num_markers)]
        np.savetxt(output_prefix + '/genotypes' + str(itr) + '.csv', 
                   sub_matrix, 
                   delimiter=',',
                   fmt='%.0f')

        # for single tree get the topology
        root = current_tree.get_root()
        nodes = [n for n in current_tree.nodes() if n != root]
        parents = [current_tree.get_parent(n) for n in nodes]
        times = [trees.get_time(p) for p in parents]
        current_rank_topology[nodes,parents] = times
        np.save(output_prefix + '/topology' + str(itr) + '.current.npy', 
                current_rank_topology)
        # for single tree get the topology
        root = next_tree.get_root()
        nodes = [n for n in next_tree.nodes() if n != root]
        parents = [next_tree.get_parent(n) for n in nodes]
        times = [trees.get_time(p) for p in parents]
        next_rank_topology[nodes,parents] = times
        np.save(output_prefix + '/topology' + str(itr) + '.next.npy', 
                current_rank_topology)
    else:
        pass


### SAVE ONLY THE CURRENT TREE AND NEXT XX MARKERS DATA

# for tree in trees.trees():

#     # initialize the topology
#     sparse_rank_topology = np.zeros((num_nodes,num_nodes))
#     sparse_rank_topology.shape

#     itr += 1
#     if itr < num_trees:

#         # capture the marker data
#         right = tree.interval.right
#         mask = sites > right
#         try:
#             first_index = np.nonzero(mask)[0][0]
#         # happens at the last tree
#         except Exception as e:
#             sys.exit(0)
#         sites = sites[first_index:,]
#         sub_matrix = full_matrix[first_index:(first_index+num_markers)]
#         np.savetxt(output_prefix + '/genotypes' + str(itr) + '.csv', 
#                    sub_matrix, 
#                    delimiter=',',
#                    fmt='%.0f')
#         # np.save(output_prefix + '/genotypes' + str(itr) + '.npy', 
#         #         sub_matrix)

#         # for single tree get the topology
#         root = tree.get_root()
#         nodes = [n for n in tree.nodes() if n != root]
#         parents = [tree.get_parent(n) for n in nodes]
#         times = [trees.get_time(p) for p in parents]
#         sparse_rank_topology[nodes,parents] = times
#         # np.savetxt(output_prefix + '/topology' + str(itr) + '.csv', 
#         #            sparse_rank_topology, 
#         #            delimiter=','
#         #            )
#         np.save(output_prefix + '/topology' + str(itr) + '.npy', 
#                 sparse_rank_topology)
#     else:
#         pass
