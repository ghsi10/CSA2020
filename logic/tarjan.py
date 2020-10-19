import math
from tqdm import tqdm


with open('tree.txt', 'r') as f:
    data = f.read()

pairs = [
        [9459011, 9459014],
        [8834567, 8834570],
        [16484715, 16484718],
        [10536999, 10537002],
        [5360200, 5360202],
        [9219552, 9219554],
        [12180815, 12180822],
        [6840232, 6840234],
        [9045060, 9045061],
        [11177208, 11177209],
        [11759735, 11759737],
        [14370512, 14370514], 
        [5040815, 10081638],
        [14104364, 14104365],
        [5298400, 5298401],
        [520991, 520993],
        [4762656, 4762657],
        [3424404, 3424406],
        [1955787, 15646330],
        [15455827, 15455830],
        [16176083, 16176085],
        [16746452, 16746453],
        [5806147, 1451538], 
        [8531676, 8531678],
        [847235, 6777909],
        [13936711, 13936714],
        [4484468, 4484470],
        [1783775, 1783777],
        [1515704, 757854],
        [1362647, 1362650],
        [9927216, 9927217],
        [12178935, 12178938], 
        [15606523, 15606526],
        [8906755, 8906758],
        [3688248, 3688249],
        [13860120, 13860121], 
        [7669927, 7669929], 
        [11053915, 11053917],
        [10777908, 2694478], 
        [12786419, 3196605], 
        [13042600, 13042602], 
        [15378273, 7689137], 
        [15287808, 15287810], 
        [1187667, 1187670], 
        [5977260, 5977261], 
        [8324863, 8324866], 
        [1255851, 10046834], 
        [2811044, 2811046]
]

m = 0
for a, b in pairs:
    _m = max(a, b)
    m = max(m, _m)
max_layer = int(math.log(m, 2))

pbar = tqdm(range(m))

def get_layer(text, layer_idx):
    from_idx = sum_pow(layer_idx)
    return text[from_idx : from_idx + 2**layer_idx]


def sum_pow(n):
    return sum([ 2**i for i in range(n)])

class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None



def findPath( root, path, k): 
  
    if root is None: 
        return False
    path.append(root.key) 
    if root.key == k : 
        return True
    if ((root.left != None and findPath(root.left, path, k)) or
            (root.right!= None and findPath(root.right, path, k))): 
        return True 
    path.pop() 
    return False

def findLCA(root, n1, n2): 
    path1 = [] 
    path2 = []  
    if (not findPath(root, path1, n1) or not findPath(root, path2, n2)): 
        return -1 
    i = 0 
    while(i < len(path1) and i < len(path2)): 
        if path1[i] != path2[i]: 
            break
        i += 1
    return path1[i-1] 

def get_idx():
    i = 0
    while True:
        yield i
        i += 1


def build_tree(l):
    indexer = get_idx()
    root = Node(next(indexer))
    work = root
    curr = [work]
    for _ in range(l):
        _curr = []
        for node in curr:
            node.left = Node(next(indexer))
            node.right = Node(next(indexer))
            _curr.append(node.left)
            _curr.append(node.right)
            pbar.update(2)
        curr = _curr
    return root


root = build_tree(max_layer)
for a, b in pairs:
    n = findLCA(root, a, b)
    print(data[n], end='')