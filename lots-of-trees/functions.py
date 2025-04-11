# Utility function for tree sequence projects
# Seth Temple, sethtem@umich.edu

import tskit
import msprime
import numpy as np
import scipy.sparse as sp
import networkx as nx

def make_adjacency_matrix_from_tree(tree, 
                                    upper=True, 
                                    sparse=False):
    '''Make an adjacency matrix from a bifurcating tree
    
    Parameters
    ----------
    tree : tskit.Tree
    upper : bool
        Only upper triangular if True
    sparse : bool
        Make sparse matrix if True

    Returns
    -------
    numpy.array(dtype=np.int32)
     (# of nodes) x (# of nodes) adjacency matrix
    '''
    sample_number = tree.num_samples()
    node_number = 2 * sample_number - 1
    if sparse:
        adjacency_matrix = sp.eye(node_number, dtype=np.int32, format='lil')
    else:
        adjacency_matrix = np.eye(node_number, dtype=np.int32)
    node_ids = np.sort(np.array([n for n in tree.nodes()]))
    rows_ids = dict((node_ids[i],i) for i in range(node_number))
    for child in node_ids:
        parent = tree.parent(child)
        if parent >= sample_number:
            child_row = rows_ids[child]
            parent_row = rows_ids[parent]  
            adjacency_matrix[child_row,parent_row] = 1
            if not upper:
                adjacency_matrix[parent_row,child_row] = 1
    return adjacency_matrix

def branch_grafted_onto(sample_id, tree):
    '''Determine edge that sample is grafted onto

    Parameters
    ----------
    sample_id : int
    tree : tskit.Tree
    
    Returns
    -------
    tuple
        (node ID, node ID)
    '''
    elder = tree.parent(sample_id)
    grand_elder = tree.parent(elder)
    sibs = tree.children(elder)
    sib = sibs[0] if sibs[0] != sample_id else sibs[1]
    return((sib,grand_elder))


def down_to_mrca(node_id, tree, trees, max_itr=100):
    '''Find first children that are not recombinant nodes

    Parameters
    ----------
    node_id : int
    tree : tskit.Tree
    trees : tskit.TreeSequence
    max_itr : int
        Addresses while loop

    Returns
    -------
    tuple
        Node IDs (two if the parent of leaves)
    '''
    
    condition = True
    elder = node_id
    itr = 1
    
    while condition:

        # worry about while loop dev
        if itr > max_itr:
            raise(TimeoutError,"Too many iterations")
        itr += 1 

        kids = tree.children(elder)
        if len(kids) > 1:
            kid0 = kids[0]
            kid1 = kids[1]
            # worried about this
            return((kid0,kid1))
        
        # scan for non recombinant / common ancestor node
        else:
            kid0 = kids[0]
            if trees.node(kid0).flags <= 1:
                condition = False
        elder = kid0

    return (kid0,)

def up_to_mrca(node_id, tree, trees, max_itr=100):
    '''Find first parent that is not recombinant nodes

    Parameters
    ----------
    node_id : int
    tree : tskit.Tree
    trees : tskit.TreeSequence
    max_itr : int
        Addresses while loop

    Returns
    -------
    int
        Node ID
    '''

    condition = True
    kid = node_id
    itr = 1

    while condition:

        # worry about while loop dev
        if itr > max_itr:
            raise(TimeoutError,"Too many iterations")
        itr += 1 

        # scan for non recombinant / common ancestor node
        elder = tree.parent(kid)
        if trees.node(elder).flags <= 0:
            condition = False
        kid = elder

    return elder