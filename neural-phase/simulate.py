### packages

# statistics
import numpy as np

# population genetics
import tskit
import msprime

# i/o

import argparse

# Argument parser
parser = argparse.ArgumentParser(description="Simulate genetic data using msprime.")
parser.add_argument("--n", type=int, help="Sample size")
parser.add_argument("--N", type=int, help="Constant population size)")
parser.add_argument("--ploidy", type=int, help="Ploidy level")
parser.add_argument("--rho", type=float, help="Recombination rate")
parser.add_argument("--mu", type=float, help="Mutation rate")
parser.add_argument("--L", type=int, help="Sequence length")
parser.add_argument("--num_sim", type=int, help="Simulations to run")
parser.add_argument("--output", type=str, help="Output file prefix")

args = parser.parse_args()

n = args.n
N = args.N
ploidy = args.ploidy
rho = args.rho
mu = args.mu
L = args.L
m = ploidy * n

K = args.num_sim
output = args.output

for k in range(K):

    # simulate the tree
    trees = msprime.sim_ancestry(samples=n,
                                 population_size=N,
                                 ploidy=ploidy,
                                 recombination_rate=rho,
                                 sequence_length=L, 
                                 )
    trees = msprime.sim_mutations(trees, rate=mu)

    # genotype matrix
    genotype_matrix = trees.genotype_matrix()

    # get the biallelic variant positions
    # and biallelic variants
    variant_positions = np.zeros(genotype_matrix.shape[0])
    biallelic = np.ones(genotype_matrix.shape[0],dtype=bool)
    itr = 0
    for variant in trees.variants():
        variant_positions[itr] = variant.position
        # check if biallelic
        if len(variant.alleles) > 2:
            biallelic[itr] = 0
        itr += 1

    # standardize the positions
    # and frequencies
    # to be between 0 and 1
    biallelic_matrix = genotype_matrix[biallelic]
    biallelic_positions = variant_positions[biallelic]
    biallelic_positions -= biallelic_positions.min()
    biallelic_positions /= biallelic_positions.max()

    # compute allele frequencies
    biallelic_frequencies = biallelic_matrix.mean(axis=1)

    # save genotype matrix
    np.savetxt(output + "_genotypes_" + str(k) + ".csv", biallelic_matrix, delimiter=",", fmt="%d")

    # save biallelic positions
    np.savetxt(output+"_positions_" + str(k) + ".csv", biallelic_positions, delimiter=",", fmt="%.8f")

    # save biallelic frequencies
    np.savetxt(output + "_frequencies_" + str(k) + ".csv", biallelic_frequencies, delimiter=",", fmt="%.8f")
