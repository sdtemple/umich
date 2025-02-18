import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_array

def spherical_taper(_matrix, _range):
    initial_matrix = _matrix / _range
    truncation_term = 1 - initial_matrix
    truncation_term = np.maximum(truncation_term, 0)
    truncation_term **= 2
    multiply_term = 1 + initial_matrix / 2
    return truncation_term * multiply_term

def wendland1_taper(_matrix, _range):
    initial_matrix = _matrix / _range
    truncation_term = 1 - initial_matrix
    truncation_term = np.maximum(truncation_term, 0)
    truncation_term **= 6
    multiply_term = 1 + 4 * initial_matrix
    return truncation_term * multiply_term

def wendland2_taper(_matrix, _range):
    initial_matrix = _matrix / _range
    truncation_term = 1 - initial_matrix
    truncation_term = np.maximum(truncation_term, 0)
    truncation_term **= 4
    multiply_term = 1 + 6 * initial_matrix \
        + 35 / 3 * np.power(initial_matrix, 2)
    return truncation_term * multiply_term

def rcm_reorder_sparse(_sparse_matrix):
    '''Apply Reverse Cuthill McKee to sparse matrix'''
    rcm_indices = reverse_cuthill_mckee(_sparse_matrix)
    reorder_matrix = _sparse_matrix[rcm_indices,:][:,rcm_indices]
    return reorder_matrix

def rcm_reorder_dense(_matrix):
    '''Apply Reverse Cuthill McKee to dense matrix'''
    _sparse_matrix = csr_array(_matrix)
    rcm_indices = reverse_cuthill_mckee(_sparse_matrix)
    return _sparse_matrix[rcm_indices,:][:,rcm_indices].toarray()

