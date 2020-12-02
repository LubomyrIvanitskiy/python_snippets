#https://nbviewer.jupyter.org/gist/BenLangmead/6665861
#http://www.cs.jhu.edu/~langmea/resources/lecture_notes/suffix_trees.pdf
# Each node stores a dictionary of children where key is the first letter, and the value is the node with lable and count

class WordSuffixTree(object):
    class Node(object):
        def __init__(self, lab):
            self.lab = lab  # label on path leading to this node
            self.out = {}  # outgoing edges; maps characters to nodes
            self.count = 0  # how many times given child was selected



    def __init__(self):
        """ Make suffix tree, without suffix links, from s in quadratic time
            and linear space """
        self.root = self.Node(None)
        self.node_count = 0
        # add the rest of the suffixes, from longest to shortest
        
    def add_word(self, s):
      s = ''.join([ch if (ch!='^' and ch!="$") else '_' for ch in s])
      s = f"^{s}$"
      for i in range(0, len(s)):
            cur = self.root
            j = i
            while j < len(s):
                if s[j] in cur.out:
                  #Go deeply
                    child = cur.out[s[j]]
                    lab = child.lab
                    k = j + 1
                    while k - j < len(lab) and s[k] == lab[k - j]:
                        k += 1
                    if k - j == len(lab):
                        cur = child
                        # Go deeply node by node
                        child.count += 1
                        # print("child.count", child.lab, child.count)
                        j = k
                    else:
                        cExist, cNew = lab[k - j], s[k]
                        mid = self.Node(lab[:k - j])
                        mid.count = child.count
                        mid.out[cNew] = self.Node(s[k:])
                        mid.out[cNew].count += 1
                        # print("mid.out[cNew]", mid.out[cNew].lab, mid.out[cNew].count)
                        mid.out[cExist] = child
                        # We already increased this node count in the if k - j scope lets decrease it such as we don't follow this pass and this node was cloned from above
                        mid.out[cExist].count -= 1
                        child.lab = lab[k - j:]
                        cur.out[s[j]] = mid
                else:
                    # Go through all leters and ensure there we have all children initialised. Not we don't change j so the next time we'll go in the top scope with the same j
                    cur.out[s[j]] = self.Node(s[j:])

    def followPath(self, s):
        """ Follow path given by s.  If we fall off tree, return None.  If we
            finish mid-edge, return (node, offset) where 'node' is child and
            'offset' is label offset.  If we finish on a node, return (node,
            None). """
        cur = self.root
        i = 0
        while i < len(s):
            c = s[i]
            if c not in cur.out:
                return (None, None)  # fell off at a node
            child = cur.out[s[i]]
            lab = child.lab
            j = i + 1
            while j - i < len(lab) and j < len(s) and s[j] == lab[j - i]:
                j += 1
            if j - i == len(lab):
                cur = child  # exhausted edge
                i = j
            elif j == len(s):
                return (child, j - i)  # exhausted query string in middle of edge
            else:
                return (None, None)  # fell off in the middle of the edge
        return (cur, None)  # exhausted query string at internal node

    def hasSubstring(self, s):
        """ Return true iff s appears as a substring """
        node, off = self.followPath(s)
        return node is not None

    def hasWord(self, s):
        s = f"^{s}"
        node, off = self.followPath(s)
        if node is None:
            return False  # fell off the tree
        if off is None:
            # finished on top of a node
            return '$' in node.out
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return node.lab[off] == '$'

    def hasSuffix(self, s):
        """ Return true iff s is a suffix """
        node, off = self.followPath(s)
        if node is None:
            return False  # fell off the tree
        if off is None:
            # finished on top of a node
            return '$' in node.out
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return node.lab[off] == '$'

    def countSubstring(self, s):
        node, off = WordSuffixTree.followPath(self, s)
        return node.count if node is not None else -1
      
    def countWord(self, s):
        s = f"^{s}"
        node, off = self.followPath(s)
        if node is None:
            return -1  # fell off the tree
        if off is None:
            # finished on top of a node
            return node.out['$'].count if '$' in node.out else -1
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return node.lab[off].count if node.lab[off] == '$' else -1


# https://github.com/LubomyrIvanitskiy/python_snippets/tree/main
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





if __name__=='__main__':
  test = """
    Gaudeamus igitur,
    Juvenes dum sumus! (bis)
    Post jucundam juventutem,
    Post molestam senectutem
    Nos habebit humus!
  """
  test_stree = WordSuffixTree()
  test_words = test.split()
  for word in test_words:
    test_stree.add_word(word)
  #method from snippets
  pprint_tree(test_stree.root, childrenattr='out', labelattr='lab')
  print(test_stree.countSubstring("ма"))
  print(test_stree.countSubstring("мама"))
