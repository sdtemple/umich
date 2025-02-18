## This repository provides a workflow to simulate data for tree-based machine learning

Current status
---

- Simulate tree with some flexibility
    - Sample and sequence length
    - rho, mu, GC rates
    - Constant Ne
    - To do: general Ne(t) and genetic map
- Sliding windows with left, center, right tree
- tsinfer and vcf
    - Using CLI for tsinfer with .zarr / .vcz files is broke

To do
---

- Calculate various summary statistics
- Concatenate into NN features
- Python environment (pip update is buggy)
- Learn how to run this on Great Lakes

Example analysis
---

1. Modify the `make-experiments.sh` file
2. Update the `data.yaml` file
3. Dry run `snakemake -c1 --configfile data.yaml -n`
4. Actual run `snakemake -c1 --configfile data.yaml`

Author
---

Seth Temple
sethtem@umich.edu