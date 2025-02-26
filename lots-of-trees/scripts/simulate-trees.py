import msprime
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(description='Simulate trees with msprime.')

# Define required arguments with named options
parser.add_argument('--input_file', 
                    type=str, 
                    required=True, 
                    help='File name for input')
parser.add_argument('--output_file', 
                    type=str, 
                    required=True, 
                    help='File name for output')



# Parse the arguments
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file

# Read in parameters
f = open(input_file, 'r')
line = f.readline()
line = f.readline().strip().split('\t')
sample_size = int(line[1])
line = f.readline().strip().split('\t')
ploidy = int(line[1])
line = f.readline().strip().split('\t')
chromosome_size = int(line[1])
line = f.readline().strip().split('\t')
Ne = int(line[1])
line = f.readline().strip().split('\t')
demography = line[1]
line = f.readline().strip().split('\t')
recombination_rate = float(line[1])
line = f.readline().strip().split('\t')
genetic_map = line[1]
line = f.readline().strip().split('\t')
mutation_rate = line[1] 
line = f.readline().strip().split('\t')
gene_conversion_rate = float(line[1])
line = f.readline().strip().split('\t')
mean_gene_conversion_tract = int(line[1])
line = f.readline().strip().split('\t')
seed1 = int(float(line[1]))
line = f.readline().strip().split('\t')
seed2 = int(float(line[1]))

# genetic map flexibility not implemented
# demography flexibility not implemented

# Simulate a tree sequence
ts = msprime.sim_ancestry(
  samples = sample_size,
  ploidy=int(ploidy),
  population_size = Ne,
  # demography = demography,
  model=[
    msprime.StandardCoalescent(),
  ],
  recombination_rate=recombination_rate,
  # genetic_map=genetic_map,
  sequence_length=chromosome_size,
  gene_conversion_rate=gene_conversion_rate,
  gene_conversion_tract_length=mean_gene_conversion_tract,
  random_seed=seed1,
)

# root check
roots = max(tree.num_roots for tree in ts.trees())
if roots > 1:
    raise ValueError('More than 1 root')

# add neutral mutations
mut_ts = msprime.sim_mutations(ts, 
                               rate=mutation_rate, 
                               keep=True,
                               random_seed=seed2,
                               )

mut_ts.dump(output_file)