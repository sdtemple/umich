# global parameters for all python
# in yaml file you should update your file name
filename=train.tsv
samplesize=50
chrsize=1000000
numsims=2

# remove if existing
rm -f $filename

# initiate the file
touch $filename
itr=0

# first simulation
python make-experiments.py \
    --output_file $filename.temp \
    --num_sims $numsims \
    --sample_size $samplesize \
    --chromosome_size $chrsize \
    --header 1 \
    --sim_id_start $itr \
    --ploidy 2 \
    --Ne 10000 \
    --demography null \
    --mutation_rate 1e-8 \
    --recombination_rate 1e-8 \
    --gene_conversion_rate 0. \
    --mean_gene_conversion_tract 450 \
    --genetic_map null \

cat $filename.temp >> $filename
itr=$(($itr + $numsims))

# second simulation
# change some parameters
python make-experiments.py \
    --output_file $filename.temp \
    --num_sims $numsims \
    --sample_size $samplesize \
    --chromosome_size $chrsize \
    --header 0 \
    --sim_id_start $itr \
    --ploidy 2 \
    --Ne 20000 \
    --demography null \
    --mutation_rate 1e-8 \
    --recombination_rate 1e-8 \
    --gene_conversion_rate 0. \
    --mean_gene_conversion_tract 450 \
    --genetic_map null \

cat $filename.temp >> $filename
itr=$(($itr + $numsims))

# copy, paste, and modify second simulation
# to fill in with more simulation settings



#
#
#


# last commands
rm -f $filename.temp






