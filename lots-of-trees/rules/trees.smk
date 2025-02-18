# These rules handle tree sequence files

rule simulate_tree_sequence:
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

rule access_tree:
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
        python scripts/access-tree.py \
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
# rule tsinfer:
#     input:
#     output:
#     params:
#     shell:
#         '''
        
        
#         '''