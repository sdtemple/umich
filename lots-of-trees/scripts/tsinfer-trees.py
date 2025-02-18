import tsinfer
import tskit
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(description='Infer trees from simulated tree.')

# Define required arguments with named options
parser.add_argument('--input_file', 
                    type=str, 
                    required=True, 
                    help='File name for input')
parser.add_argument('--output_file', 
                    type=str, 
                    required=True, 
                    help='File name for output')

# infer the tree sequence
args = parser.parse_args()
ts = tskit.load(args.input_file)
sample_data = tsinfer.SampleData.from_tree_sequence(ts)
inferred_ts = tsinfer.infer(sample_data)
inferred_ts.dump(args.output_file)
