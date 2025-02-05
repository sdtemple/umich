import numpy as np
from scipy.special import kv, gamma

def spherical_family(matrix,phi):
    '''Correlation function for spherical family'''
    long_distance = matrix < phi
    init_vario = 1 - 1.5 * matrix / phi + 0.5 * ((matrix / phi) ** 3)
    return init_vario * long_distance

def matern_family(matrix,phi,kappa):
    '''Correlation function for Matern family'''
    transformed = matrix / phi
    gammakappa = gamma(kappa)
    tk = transformed ** kappa
    bessel = kv(kappa,transformed)
    off_diag = (2 ** (1-kappa)) / gammakappa * bessel * tk
    off_diag[np.isnan(off_diag)] = 1
    return off_diag
    # nrow, ncol = matrix.shape
    # return off_diag + np.eye(nrow, ncol)

def powered_exponential_family(matrix, phi, kappa):
    '''Correlation function for powered exponential family'''
    return np.exp( - ((matrix / phi) ** kappa))