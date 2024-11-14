from collections import defaultdict, deque
import heapq
import numpy as np
from numpy.typing import NDArray
import random

# I wrote this function
def format_topology(tree: list) -> list:
    '''Reorder and sort the tree\'s topology'''
    reordered_tree = [(min(x),max(x)) for x in tree]
    sorted_tree = sorted(reordered_tree, key = lambda x: x[0])
    return sorted_tree

# From UMich GPT service
def topology_to_prufer(tree: list) -> NDArray[np.int_]:
    '''Convert tree topology to Pruefer sequence'''

    # Create adjacency list representation of the tree
    adj_list = defaultdict(list)
    for u, v in tree:
        adj_list[u].append(v)
        adj_list[v].append(u)

    # Min-heap to keep track of smallest leaves
    leaf_heap = []
    for node in adj_list:
        if len(adj_list[node]) == 1:
            heapq.heappush(leaf_heap, node)

    prufer_sequence = []
    while len(adj_list) > 2:
        # Get the smallest leaf
        leaf = heapq.heappop(leaf_heap)
        
        # The only neighbor of this leaf
        neighbor = adj_list[leaf].pop()

        # Remove the leaf from the neighbor's adjacency list
        adj_list[neighbor].remove(leaf)
        if len(adj_list[neighbor]) == 1:
            heapq.heappush(leaf_heap, neighbor)

        # Append the neighbor to the Prufer sequence
        prufer_sequence.append(neighbor)
        
        # Remove the leaf from the adjacency list
        del adj_list[leaf]

    return np.array(prufer_sequence)

# From UMich GPT service
def prufer_to_topology(prufer_sequence: NDArray[np.int_]) -> list:
    '''Convert Pruefer sequence to tree topology'''

    n = len(prufer_sequence) + 2
    degree = [1] * n
    
    # Degrees calculation
    for node in prufer_sequence:
        degree[node - 1] += 1
    
    # Priority queue to find the smallest node with degree 1
    leaf_nodes = deque(node for node in range(n) if degree[node] == 1)

    tree = []

    for node in prufer_sequence:
        leaf = leaf_nodes.popleft()
        tree.append((leaf + 1, node))
        
        degree[leaf] -= 1
        degree[node - 1] -= 1
        
        if degree[node - 1] == 1:
            leaf_nodes.append(node - 1)
    
    # Connecting the last two remaining nodes
    leaf_nodes = [x + 1 for x in leaf_nodes]
    tree.append((leaf_nodes[0], leaf_nodes[1]))

    return format_topology(tree)

# From UMich GPT service
def simulate_coalescent(n):
    """
    Simulate a coalescent tree for a sample of size n.

    Returns:
        edges: List of tuples representing the edges of the tree.
        ancestral_times: List of times at which coalescent events occur.
    """
    nodes = list(range(1, n + 1))  # Initial sample nodes
    edges = []
    ancestral_times = []
    
    current_time = 0
    node_counter = n + 1  # New node index for internal nodes

    while len(nodes) > 1:
        k = len(nodes)
        # Time until next coalescent event
        t = np.random.exponential(2 / (k * (k - 1)))
        current_time += t
        
        # Choose 2 nodes to coalesce
        i, j = random.sample(nodes, 2)
        
        # Add edge (new node, child node)
        edges.append((i, node_counter))
        edges.append((j, node_counter))
        
        # Record the time of this coalescence event
        ancestral_times.append(current_time)
        
        # Update nodes: remove i and j, add new node
        nodes.remove(i)
        nodes.remove(j)
        nodes.append(node_counter)
        
        node_counter += 1

    return format_topology(edges), ancestral_times

# def simulate_prufer(n: int) -> NDArray[np.int_]:
#     '''Simulate a Pruefer sequence for coalescent tree topology'''

#     # set up labels
#     arr1 = np.arange(n+1,2*n-1,1)
#     arr2 = np.arange(n+1,2*n-1,1)
#     arr = np.sort(
#         np.concatenate((arr1,
#                         arr2,
#                         np.array([2*n-1]))
#                         )
#         )
#     print(arr.shape)
    
#     # # initial labels fully random
#     # idxs = np.random.choice(np.arange(n),
#     #                         n-2,
#     #                         replace=False)
#     # seq = arr[idxs]
#     # arr = np.delete(arr,idxs)

#     idx = np.random.choice(np.arange(arr.shape[0]),1)
#     seq = np.array(arr[idx])
#     arr = np.delete(arr,idx)
#     print(seq)
#     print(arr)

#     # enforce coalescent tree conditions
#     for i in np.arange(2*n-3):
#         try:
#             j = i + 2
#             sm = (seq <= (j + 0.5)).sum()
#             if sm > 1:
#                 seq = np.concatenate((seq,[j,j]))
#                 arr = np.delete(arr,[0])
#                 arr = np.delete(arr,[0])
#             elif sm > 0:
#                 seq = np.concatenate((seq,[j]))
#                 arr = np.delete(arr,[0])
#             else:
#                 idx = np.random.choice(np.arange(arr.shape[0]),1)
#                 seq = arr[idx]
#                 arr = np.delete(arr,idx)
#         except ValueError:
#             pass
#     return seq



    # for must in range(n+1,2*n):

    #     if arr.shape[0] <= 1:
    #         print(seq,arr)
    #         seq = np.concatenate((seq,arr))
    #         break

    #     print(seq,arr)

    #     sm = ((seq > must - 1) & ((seq < must + 1))).sum()
    #     if sm <= 0:
    #         # must choose two specific nodes 
    #         seq = np.concatenate((seq,[must,must]))
    #         arr = np.delete(arr,[0,1])

    #     elif sm >= 2:
    #         # can choose two nodes randomly
    #         idx = np.random.choice(np.arange(arr.shape[0]),2,replace=False)
    #         seq = np.concatenate((seq,arr[idx]))
    #         arr = np.delete(arr,idx)

    #     else:
    #         # choose one node randomly
    #         seq = np.concatenate((seq,[must]))
    #         arr = np.delete(arr,0)
    #         idx = np.random.choice(np.arange(arr.shape[0]),1)
    #         seq = np.concatenate((seq,arr[idx]))
    #         arr = np.delete(arr,idx)
    #         # sm = ((seq > must - 1) & ((seq < must + 1))).sum()
    #         # if sm >= 2:
    #         #     # can choose node randomly
    #         #     idx = np.random.choice(np.arange(arr.shape[0]),1)
    #         #     seq = np.concatenate((seq,arr[idx]))
    #         #     arr = np.delete(arr,idx)
    #         # else:
    #         #     # must choose specific node
    #         #     seq = np.concatenate((seq,[must]))
    #         #     arr = np.delete(arr,0)

    # return seq

# I wrote this function
def simulate_prufer(n: int) -> NDArray[np.int_]:
    '''Simulate a coalescent tree topology'''
    topology, _ = simulate_coalescent(n)
    return topology_to_prufer(topology)

# I wrote this function
def prufer_there_and_back_again(prufer: list) -> float:
    '''Check conversion between tree and Pruefer sequence'''
    tree = prufer_to_topology(prufer)
    inverse_prufer = topology_to_prufer(tree)
    return (inverse_prufer - prufer).sum()

# I wrote this function
def valid_prufer(prufer: list) -> bool:
    '''Valid coalescent Prufer sequence has
    two of each interior node except
    one of the most recent common ancestor
    '''
    ids, counts = np.unique(prufer, return_counts=True)
    sorts = np.argsort(ids)
    ids_revised = ids[sorts]
    counts_revised = counts[sorts]
    interiors = counts_revised[:-1]
    assert counts_revised[-1] == 1
    two, _ = np.unique(interiors, return_counts = True)
    assert two.shape == (1,)
    assert two[0] == 2
    return None