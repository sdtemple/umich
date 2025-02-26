import argparse
from random import randint

# Set up the argument parser
parser = argparse.ArgumentParser(description='Write parameters file for popgen simulations.')

# Define required arguments with named options
parser.add_argument('--output_file', 
                    type=str, 
                    required=True, 
                    help='File name for output')
parser.add_argument('--num_sims', 
                    type=int, 
                    required=True, 
                    help='Number of simulations')
parser.add_argument('--sample_size', 
                    type=int, 
                    required=True, 
                    help='Sample size')
parser.add_argument('--chromosome_size', 
                    type=int, 
                    required=True, 
                    help='Base pair length')
parser.add_argument('--ploidy', 
                    type=int, 
                    default=2, 
                    help='Ploidy number')
parser.add_argument('--demography', 
                    type=str, 
                    default="nan", 
                    help='Demographic model')
parser.add_argument('--Ne', 
                    type=float, 
                    default=10000, 
                    help='Effective population size')
parser.add_argument('--mutation_rate', 
                    type=float, 
                    default=1e-8, 
                    help='Genome-wide mutation rate')
parser.add_argument('--recombination_rate', 
                    type=float, 
                    default=1e-8, 
                    help='Genome-wide recombination rate')
parser.add_argument('--gene_conversion_rate', 
                    type=float, 
                    default=0., 
                    help='Input simulation method file output')
parser.add_argument('--mean_gene_conversion_tract', 
                    type=float, 
                    default=450, 
                    help='Average base pair length of gene conversion')
parser.add_argument('--genetic_map', 
                    type=str, 
                    default="nan", 
                    help='Genetic recombination map')
parser.add_argument('--sim_id_start', 
                    type=float, 
                    default=0, 
                    help='Iterator to start at for IDs')
parser.add_argument('--header', 
                    type=float, 
                    default=1, 
                    help='There is a header if not 0')

# Parse the arguments
args = parser.parse_args()
output_file = args.output_file
num_sims = args.num_sims
sample_size = args.sample_size
ploidy = args.ploidy
chromosome_size = args.chromosome_size
recombination_rate = args.recombination_rate
mutation_rate = args.mutation_rate
gene_conversion_rate = args.gene_conversion_rate
genetic_map = args.genetic_map
demography = args.demography
Ne = args.Ne
Ne = int(Ne)
mean_gene_conversion_tract = args.mean_gene_conversion_tract
mean_gene_conversion_tract = int(mean_gene_conversion_tract)
sim_id_start = args.sim_id_start
sim_id_start = int(sim_id_start)
header = int(args.header)

f = open(output_file,'w')

if abs(header) > 0:
    f.write('sim_id\t')
    f.write('sample_size\t')
    f.write('ploidy\t')
    f.write('chromosome_size\t')
    f.write('Ne\t')
    f.write('demography\t')
    f.write('recombination_rate\t')
    f.write('genetic_map\t')
    f.write('mutation_rate\t')
    f.write('gene_conversion_rate\t')
    f.write('mean_gene_conversion_tract\t')
    f.write('ancestry_random_seed\t')
    f.write('mutation_random_seed\n')

for n in range(sim_id_start, num_sims + sim_id_start):
    f.write(str(n)); f.write('\t')
    f.write(str(sample_size)); f.write('\t')
    f.write(str(ploidy)); f.write('\t')
    f.write(str(chromosome_size)); f.write('\t')
    f.write(str(Ne)); f.write('\t')
    f.write(str(demography)); f.write('\t')
    f.write(str(recombination_rate)); f.write('\t')
    f.write(str(genetic_map)); f.write('\t')
    f.write(str(mutation_rate)); f.write('\t')
    f.write(str(gene_conversion_rate)); f.write('\t')
    f.write(str(mean_gene_conversion_tract)); f.write('\t')
    # these are hard coded upper limits on random number generation
    # the highest possible with msprime
    f.write(str(randint(1,int(2**32-1)))); f.write('\t')
    f.write(str(randint(1,int(2**32-1)))); f.write('\n')

f.close()