# These rules handle tree sequence files

rule simulate_trees:
    input:
        file = '{folder}/{sim_id}/parameters.tsv'
    output:
        file = '{folder}/{sim_id}/simulated.trees'
    shell:
        '''
        python scripts/simulate-trees.py \
            --input_file {input.file} \
            --output_file {output.file}
        '''

rule format_trees_data:
    input:
        file = '{folder}/{sim_id}/simulated.trees'
    output:
        # gt = '{folder}/{sim_id}/genotypes1.csv',
        # tp = '{folder}/{sim_id}/topology1.npy',
        gtn = '{folder}/{sim_id}/genotypes1.next.csv',
        tpn = '{folder}/{sim_id}/topology1.next.npy',
        tpc = '{folder}/{sim_id}/topology1.current.npy',
    params:
        num_markers = num_markers,
    shell:
        '''
        python scripts/format-trees-data.py \
            --input_file {input.file} \
            --output_prefix {wildcards.folder}/{wildcards.sim_id} \
            --num_markers {params.num_markers}
        '''

rule access_trees:
    input:
        tree_sequence = '{folder}/{sim_id}/simulated.trees',
        files = '{folder}/{sim_id}/{tree_id}/init.txt'
    output:
        center = '{folder}/{sim_id}/{tree_id}/center.tree.pkl',
        left = '{folder}/{sim_id}/{tree_id}/left.tree.pkl',
        right = '{folder}/{sim_id}/{tree_id}/right.tree.pkl',
        lcr = '{folder}/{sim_id}/{tree_id}/lcr.trees',
        intervals = '{folder}/{sim_id}/{tree_id}/intervals.tsv',
    params:
        trim_trees = trim_trees,
    shell:
        '''
        python scripts/access-trees.py \
            --input_file {input.tree_sequence} \
            --output_folder {wildcards.folder}/{wildcards.sim_id}/{wildcards.tree_id} \
            --index_tree {wildcards.tree_id} \
            --trim_trees {params.trim_trees}
        '''

rule tsinfer:
    input:
        file = '{folder}/{sim_id}/simulated.trees',
    output:
        file = '{folder}/{sim_id}/inferred.trees',
    shell:
        '''
        python scripts/tsinfer-trees.py \
            --input_file {input.file} \
            --output_file {output.file}
        '''

# eventually do a command line
# cli documentation buggy
# rule tsinfer:
#     input:
#     output:
#     params:
#     shell:
#         '''
        
        
#         '''