# These rules handle VCF files

rule trees_to_vcf:
    input:
        file = '{folder}/{sim_id}/simulated.trees'
    output:
        file = '{folder}/{sim_id}/simulated.vcf'
    shell:
        '''
        tskit vcf {input.file} > {output.file}
        '''

rule gzip_vcf:
    input:
        file = '{folder}/{sim_id}/simulated.vcf'
    output:
        file = '{folder}/{sim_id}/simulated.vcf.gz'
    shell:
        '''
        bgzip {input.file}
        '''

rule tabix_vcf:
    input:
        file = '{folder}/{sim_id}/simulated.vcf.gz'
    output:
        file = '{folder}/{sim_id}/simulated.vcf.gz.tbi'
    shell:
        '''
        tabix -fp vcf {input.file}
        '''

# rule vcf_to_zarr:
#     input:
#         file = '{folder}/{sim_id}/simulated.vcf.gz',        
#         tbi = '{folder}/{sim_id}/simulated.vcf.gz.tbi',
#     output:
#         directory('{folder}/{sim_id}/simulated.zarr')
#     shell:
#         '''
#         python -m bio2zarr vcf2zarr convert {input.file} {output}
#         '''

rule vcf_to_zarr:
    input:
        file = '{folder}/{sim_id}/simulated.vcf.gz',        
        tbi = '{folder}/{sim_id}/simulated.vcf.gz.tbi',
    output:
        directory('{folder}/{sim_id}/simulated.vcz'),
        # directory('{folder}/{sim_id}/simulated.zarr')
    shell:
        '''
        python -m bio2zarr vcf2zarr explode \
            {input.file} \
            {wildcards.folder}/{wildcards.sim_id}/simulated.exploded
        python -m bio2zarr vcf2zarr encode \
            {wildcards.folder}/{wildcards.sim_id}/simulated.exploded \
            {output}
        '''


rule tree_to_vcf:
    input:
        file = '{folder}/{sim_id}/{tree_id}/lcr.trees'
    output:
        file = '{folder}/{sim_id}/{tree_id}/lcr.vcf'
    shell:
        '''
        tskit vcf {input.file} > {output.file}
        '''

rule gzip_tree_vcf:
    input:
        file = '{folder}/{sim_id}/{tree_id}/lcr.vcf'
    output:
        file = '{folder}/{sim_id}/{tree_id}/lcr.vcf.gz'
    shell:
        '''
        bgzip {input.file}
        '''

rule tabix_tree_vcf:
    input:
        file = '{folder}/{sim_id}/{tree_id}/lcr.vcf.gz'
    output:
        file = '{folder}/{sim_id}/{tree_id}/lcr.vcf.gz.tbi'
    shell:
        '''
        tabix -fp vcf {input.file}
        '''

rule subset_lcr_vcf:
    input:
        lcr = '{folder}/{sim_id}/{tree_id}/lcr.vcf.gz',
        intervals = '{folder}/{sim_id}/{tree_id}/intervals.tsv',
        tbi = '{folder}/{sim_id}/{tree_id}/lcr.vcf.gz.tbi',
    output:
        left = '{folder}/{sim_id}/{tree_id}/left.vcf.gz',
        center = '{folder}/{sim_id}/{tree_id}/center.vcf.gz',
        right = '{folder}/{sim_id}/{tree_id}/right.vcf.gz',
    shell:
        '''
        left_start=$(cut -f 2 {input.intervals} | head -n 2 | tail -n 1)
        center_start=$(cut -f 3 {input.intervals} | head -n 2 | tail -n 1)
        right_start=$(cut -f 4 {input.intervals} | head -n 2 | tail -n 1)
        left_end=$(cut -f 2 {input.intervals} | tail -n 1)
        center_end=$(cut -f 3 {input.intervals} | tail -n 1)
        right_end=$(cut -f 4 {input.intervals} | tail -n 1)
        bcftools view -Oz -o {output.left} \
            -r 1:$left_start-$left_end {input.lcr}
        bcftools view -Oz -o {output.center} \
            -r 1:$center_start-$center_end {input.lcr}
        bcftools view -Oz -o {output.right} \
            -r 1:$right_start-$right_end {input.lcr}
        '''