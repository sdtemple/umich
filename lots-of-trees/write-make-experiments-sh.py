import argparse
import pandas as pd
import numpy as np

# Set up the argument parser
parser = argparse.ArgumentParser(description='Metaprogram a shell script to write parameters for popgen simulations.')

# Define required arguments with named options
parser.add_argument('--input_file', 
                    type=str, 
                    required=True, 
                    help='File name for output')
parser.add_argument('--output_file', 
                    type=str, 
                    default="train.tsv", 
                    help='File name for eventual output')
parser.add_argument('--shell_file', 
                    type=str, 
                    default="make-experiments.sh", 
                    help='File name for the shell script')
parser.add_argument('--num_sims',
                    type=int,
                    required=True,
                    help='Simulate each parameter combo this many times'
                    )
parser.add_argument('--sample_size',
                    type=int,
                    required=True,
                    )
parser.add_argument('--ploidy',
                    type=int,
                    required=True,
                    )
parser.add_argument('--chromosome_size',
                    type=int,
                    required=True,
                    )


args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file
shell_file = args.shell_file
num_sims = args.num_sims
sample_size = args.sample_size
ploidy = args.ploidy
chromosome_size = args.chromosome_size

# Define a preset string with placeholders
preset_string = "python make-experiments.py \\\n"
preset_string += "\t--output_file "
preset_string += output_file
preset_string += ".temp \\\n"
preset_string += "\t--num_sims "
preset_string += str(num_sims)
preset_string += " \\\n"
preset_string += "\t--sample_size "
preset_string += str(sample_size)
preset_string += " \\\n"
preset_string += "\t--chromosome_size "
preset_string += str(chromosome_size)
preset_string += " \\\n"
preset_string += "\t--ploidy "
preset_string += str(ploidy)
preset_string += " \\\n"
preset_string += "\t--header {header} \\\n"
preset_string += "\t--sim_id_start {sim_id} \\\n"
preset_string += "\t--Ne {Ne} \\\n"
preset_string += "\t--demography {demography} \\\n"
preset_string += "\t--mutation_rate {mutation_rate} \\\n"
preset_string += "\t--recombination_rate {recombination_rate} \\\n"
preset_string += "\t--gene_conversion_rate {gene_conversion_rate} \\\n"
preset_string += "\t--mean_gene_conversion_tract {mean_gene_conversion_tract} \\\n"
preset_string += "\t--genetic_map {genetic_map} \n"
preset_string += "cat "
preset_string += output_file
preset_string += ".temp >> "
preset_string += output_file
preset_string += '\n\n'

df = pd.read_csv(input_file,index_col=None)
print(df.head())
df['sim_id'] = np.arange(0, df.shape[0]) * num_sims
df['sim_id'] = pd.to_numeric(df['sim_id'], errors='coerce', downcast='integer')
df['header'] = 0
df['header'][0] = 1
df['header'] = df['header'].astype(int)

# Fill in the row values into the preset string
df['filled_string'] = df.apply(lambda row: preset_string.format(**row), axis=1)

# Concatenate the filled preset string
concatenated_string = ''.join(df['filled_string'].tolist())

g = open(shell_file,'w')
g.write('#!/bin/bash\n\n')
g.write('rm -f ' + output_file + '\n')
g.write('touch ' + output_file + '\n\n')
g.write(concatenated_string)
g.write('\nrm -f ' + output_file + '.temp\n')
g.close()







