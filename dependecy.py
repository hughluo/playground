from collections import namedtuple


class Node:
    def __init__(self, name, children=None):
        self.name = name
        if children is None:
            self.children = []
        else:
            self.children = children


class Solution:
    def __init__(self, root, dependency):
        self.node_dict = dict()

        for pair in dependency:
            origin, target = pair
            if origin not in self.node_dict:
                self.node_dict[origin] = Node(origin)
            if target not in self.node_dict:
                self.node_dict[target] = Node(target)

            origin_node = self.node_dict[origin]
            target_node = self.node_dict[target]

            if origin_node.children is None:
                origin_node.children = []

            origin_node.children.append(target_node)

        self.root_node = self.node_dict[root]

    def get_sequence(self):

        res = []
        stack = []
        visited = set()
        stack.append(self.root_node)
        while stack:
            curr = stack.pop()

            if curr in visited:
                res.append(curr)
                continue

            stack.append(curr)

            for child in curr.children:
                if child not in visited:
                    stack.append(child)

            visited.add(curr)

        return res


if __name__ == "__main__":
    dependency = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c')]
    s = Solution('a', dependency)
    seq = s.get_sequence()
    res = map(lambda n: n.name, seq)
    print(list(res))
