# memory maneuver
from typing import List, NamedTuple, Deque
from itertools import accumulate
from collections import deque

# load sample data, list of ints
with open('data/data-day8.txt') as f:
    data = [int(i) for i in f.read().strip().split(' ')]

st = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
smp = [int(i) for i in st.split(' ')]

def get_header(data):
    n_children = data.popleft()
    meta_len = data.popleft()    
    return n_children, meta_len, data

def build_tree(data: List):
    smpl = deque(data)
    meta, stack = [],[]
    n_children, meta_len, data = get_header(smpl)
    stack.append((n_children,meta_len))
    while len(smpl) > 0:
        if n_children==0:
            meta += [smpl.popleft() for i in range(meta_len)]
            new_header = stack.pop()
            n_children = new_header[0]-1
            meta_len = new_header[1]
        else:
            stack.append((n_children,meta_len))
            n_children, meta_len, data = get_header(smpl)
            
    return meta

# print(build_tree(smp))
# print(sum(build_tree(data)))

# part 2: track meta
class Node():
    def __init__(self, n_children, n_meta, data):
        self.n_children = n_children
        self.child_count = n_children
        self.n_meta = n_meta
        self.children = []
        self.meta = []

    def print_header(self):
        print(f'n children: {self.n_children}, n meta: {self.n_meta}')

    def get_meta_sum(self):
        return sum(self.meta)

def build_tree(data):
    smpl = deque(data)
    stack = []
    full = []

    n = Node(*get_header(smpl))

    while smpl:

        if n.child_count == 0:
            n.meta +=  [smpl.popleft() for i in range (n.n_meta)]

            # get parend from stack
            try:
                n_ = stack.pop()
                n_.children.append(n)
                n = n_
            except:
                IndexError
            
        else:
            n.child_count -= 1
            stack.append(n)
            n = Node(*get_header(smpl)) 
        
    return n

tree = build_tree(smp) 

# implementaiton from @joelgrus
def get_value(node):
    if node.n_children == 0:
        return node.get_meta_sum()
    else:
        child_values = {i: get_value(child) for i, child in enumerate(node.children)}
        return sum(child_values.get(i - 1, 0) for i in node.meta)
    
# bad implementation

# def recurse_get_value(tree, i, value=0):
#     if i > len(tree.children):
#         return value
#     else:
#         i = i-1
#         sub = tree.children[i]
#         if sub.n_children == 0:
#             value = sub.get_meta_sum()
#         else:
#             for it in sub.meta:
#                 value = recurse_get_item(sub, it, value)
#         return value

# for i in tree.meta:
#     values.append(recurse_get_item(tree,i))
# print(sum(values))

t2 = build_tree(data)
print( get_value(t2) )