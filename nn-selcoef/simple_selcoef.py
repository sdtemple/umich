# These are the essential simulation functions from isweep
# github.com/sdtemple/isweep 

import numpy as np
from scipy.stats import binom
from math import floor, ceil, sqrt

def read_Ne(file):
    '''Read *.ne file

    Parameters
    ----------
    file : string
        Input file name

    Returns
    -------
    dict
        dict[generation] = size
    '''

    Ne = {}
    f = open(file, 'r')
    f.readline() # header
    for line in f:
        g, size = line.split('\t')[:2]
        Ne[int(g)] = int(float(size))
    f.close()

    return Ne

def make_constant_Ne(file, size, maxg):
    '''Create *.ne file for constant size population

    Parameters
    ----------
    file: str
        Output file name
    size : float
        Effective population size
    maxg : int
        Maximum generation

    Returns
    -------
    NoneType
        Writes a *.ne file
    '''

    size = floor(size)
    maxg = floor(maxg)
    with open(file, 'w') as f:
        f.write('GEN\tNE\n')
        f.write(str(0)); f.write('\t'); f.write(str(size)); f.write('\n')
        for i in range(1, int(maxg) + 1):
            f.write(str(i)); f.write('\t'); f.write(str(size)); f.write('\n')

    return None

def walk_variant_backward(s, p0, Ne, random_walk = False, one_step_model = 'a', tau0 = 0, sv=-0.01, ploidy = 2):
    '''Variant frequencies backward in time

    Parameters
    ----------
    s : float
        Selection coefficient
    p0 : float
        Variant frequency at generation 0
    Ne : dict
        Effective population sizes
    random_walk : bool
        True for random walk
    one_step_model : str
        'm', 'a', 'd', or 'r'
    tau0 : int
        Generation when neutrality begins
    sv: float
        Allele frequency of standing variation
        (Default -0.01 will assume de novo sweep)
    ploidy : int
        1 for haploid or 2 for diploid


    Returns
    -------
    tuple
        NumPy arrays for frequencies and sizes
    '''

    # local functions
    assert ploidy in [1,2]
    assert one_step_model in ['m','a','r','d']
    assert p0 <= 1
    assert p0 >= 0
    assert sv < 1
    def haploid_bwd(p, s): # haploid is same as multiplicative (Felsenstein, 2017)
        return p / (1 + s - s * p)
    def multiplicative_bwd(p, s):
        num = 1
        dnm = 1 + (1 - p) * s
        return p * num / dnm
    def dominant_bwd(p, s):
        if s <= 0:
            return p
        a = p * s
        b = 1 + s - 2 * p * s
        c = - p
        qf = - b + sqrt((b ** 2) - 4 * a * c)
        qf = qf / 2 / a
        return qf
    def additive_bwd(p, s):
        if s <= 0:
            return p
        a = s
        b = 1 + s - 2 * p * s
        c = - p
        qf = - b + sqrt((b ** 2) - 4 * a * c)
        qf = qf / 2 / a
        return qf
    def recessive_bwd(p, s):
        if s <= 0:
            return p
        a = (1 - p) * s
        b = 1
        c = - p
        qf = - b + sqrt((b ** 2) - 4 * a * c)
        qf = qf / 2 / a
        return qf

    # one step calculation
    if ploidy == 1:
        one_step = haploid_bwd
    else:
        if one_step_model == 'a':
            one_step = additive_bwd
        elif one_step_model == 'r':
            one_step = recessive_bwd
        elif one_step_model == 'd':
            one_step = dominant_bwd
        else:
            one_step = multiplicative_bwd

    # initialize
    ps = [] # frequencies
    xs = [] # variants
    Ns = [] # sizes
    t = floor(tau0)
    p = p0
    N = Ne[0]
    x = floor(p * ploidy * N)
    Ns.append(N)
    xs.append(x)
    ps.append(p)

    if random_walk: # random walk

        for G in range(1, max(Ne.keys())+1):
            try: # population size change
                N = Ne[G]
            except KeyError:
                pass
            if G > t:
                p = one_step(p, s)
            x = int(binom.rvs(int(ploidy * N), p))
            p = x / ploidy / N
            if x < 1:
                break
            if p >= 1:
                break
            if p <= sv:
                s = 0
            ps.append(p)
            xs.append(x)
            Ns.append(N)

        return np.array([ps, Ns, xs], dtype=float) # numpy-ify

    else: # deterministic

        for G in range(1, max(Ne.keys())+1):
            try: # population size change
                N = Ne[G]
            except KeyError:
                pass
            if G > t:
                p = one_step(p, s)
            x = floor(p * ploidy * N)
            if x < 1:
                break
            if p >= 1:
                break
            if p <= sv:
                s = 0
            Ns.append(N)
            xs.append(x)
            ps.append(p)

        return np.array([np.array(ps), np.array(Ns), np.array(xs)]) # numpy-ify