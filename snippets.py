
def pprint_tree(node, file=None, _prefix="", _last=True, childrenattr='children', labelattr='label'):

    '''
    From https://vallentin.dev/2016/11/29/pretty-print-tree modified for cases when children is a dictionary
    Example: Node has a structure: 
    class Node(object):
        def __init__(self, lab):
            self.lab = lab  # label on path leading to this node
            self.out = {}  # outgoing edges; maps characters to nodes
    Usage:
    pprint_tree(node, childrenattr='out', labelattr='lab')
    '''
 
    label = str(getattr(node, labelattr))
    children = getattr(node, childrenattr)
    print(_prefix, "`- " if _last else "|- ", label, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(children)
    for i, child in enumerate(children):
        _last = i == (child_count - 1)
        pprint_tree(children[child], file, _prefix, _last, childrenattr=childrenattr, labelattr=labelattr)

        
        
 def file_line_count(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
