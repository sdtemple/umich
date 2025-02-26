## This repository provides a workflow to simulate data for tree-based machine learning

Current status
---

- Simulate tree with some flexibility
    - Sample and sequence length
    - rho, mu, GC rates
    - Constant Ne
    - To do: general Ne(t) and genetic map
- To improve: tsinfer and vcf 
    - Using CLI for tsinfer with .zarr / .vcz files is broke

Analysis steps
---

1. Modify a CSV file with parameter combinations (see `example.tsv`)
2. Run `scripts/write-make-experiments-sh.py`
3. Run the output shell script to populate simulation settings data
4. Update the YAML configuration file
5. Dry run `snakemake -c1 --configfile data.yaml -n`
6. Actual run `snakemake -c1 --configfile data.yaml`

Example
---

I use a conda environment specified here: `github.com/sdtemple/umich/hood-river.yaml`.

2. `python scripts/write-make-experiments-sh.py` with 
    - `--input-file example.csv` 
    - `--output-file simulated.data.tsv` 
    - `--shell_file make-experiments.sh`
    - Use `-h` for other settings 
3. `bash make-experiments.sh`
4. Update the `data.yaml` file with `vim`
5. Dry run `snakemake -c1 --configfile data.yaml -n`
6. Actual run `snakemake -c1 --configfile data.yaml`

To do
---

- Calculate various summary statistics
- Concatenate into NN features
- Learn how to run this on Great Lakes

Old status
---

Code to
- Sliding windows with left, center, right tree

Author
---

Seth Temple
sethtem@umich.edu