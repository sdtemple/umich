import argparse
import msprime
import tskit
import pickle
from math import floor

# Set up the argument parser
parser = argparse.ArgumentParser(description='Access tree from tree sequence.')

# Define required arguments with named options
parser.add_argument('--input_file', 
                    type=str, 
                    required=True, 
                    help='File name for input')
parser.add_argument('--output_folder', 
                    type=str, 
                    required=True, 
                    help='Folder name for output')
parser.add_argument('--index_tree', 
                    type=int, 
                    required=True, 
                    help='Index of trees in tree sequence')
parser.add_argument('--trim_trees', 
                    type=int, 
                    required=True, 
                    help='How many trees to skip at start of tree sequence')

# Parse the arguments
args = parser.parse_args()
input_file = args.input_file
output_folder = args.output_folder
index_tree = args.index_tree + args.trim_trees

# process the trees
# into left, center, and right trees
ts = tskit.load(input_file)
center_tree = ts.at_index(index_tree)
left_tree = ts.at_index(index_tree-1)
right_tree = ts.at_index(index_tree+1)
center_dd = center_tree.as_dict_of_dicts()
left_dd = left_tree.as_dict_of_dicts()
right_dd = right_tree.as_dict_of_dicts()

# store the base pair positions of the trees
left_start = floor(left_tree.interval.left)
center_start = floor(center_tree.interval.left)
right_start = floor(right_tree.interval.left)
left_end = floor(left_tree.interval.right)
center_end = floor(center_tree.interval.right)
right_end = floor(right_tree.interval.right)
with open(output_folder + '/intervals.tsv','w') as f:
    f.write('\tleft_tree\tcenter_tree\tright_tree\n')
    f.write('bp_start\t')
    f.write(str(left_start)); f.write('\t')
    f.write(str(center_start)); f.write('\t')
    f.write(str(right_start)); f.write('\n')
    f.write('bp_end\t')
    f.write(str(left_end)); f.write('\t')
    f.write(str(center_end)); f.write('\t')
    f.write(str(right_end)); f.write('\n')


# Open a file in binary write mode
# Save the left, center, right trees as dicts of dict
# Save using pickle native python object
with open(output_folder + '/center.tree.pkl', 'wb') as f:
    # Use pickle.dump() to serialize the data
    pickle.dump(center_dd, f)
with open(output_folder + '/left.tree.pkl', 'wb') as f:
    pickle.dump(left_dd, f)
with open(output_folder + '/right.tree.pkl', 'wb') as f:
    pickle.dump(right_dd, f)

# store a left, center, right tree sequence
# to later make a vcf
start = int(left_tree.interval.left)
end = int(right_tree.interval.right)
lcr_tree_sequence = ts.keep_intervals([(start,end)])
lcr_tree_sequence.dump(output_folder + '/lcr.trees')



