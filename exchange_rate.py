from collections import namedtuple
from functools import reduce


class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children


class Solution:
    def __init__(self, exchange_rates):

        ChildWithRate = namedtuple('ChildWithRate', ['node', 'rate'])

        self.node_dict = dict()

        for exchange_rate in exchange_rates:
            origin, target, rate = exchange_rate
            if origin not in self.node_dict:
                self.node_dict[origin] = Node(origin)
            if target not in self.node_dict:
                self.node_dict[target] = Node(target)

            origin_node = self.node_dict[origin]
            target_node = self.node_dict[target]

            if origin_node.children is None:
                origin_node.children = []
            if target_node.children is None:
                target_node.children = []

            origin_node.children.append(ChildWithRate(target_node, rate))
            target_node.children.append(ChildWithRate(origin_node, 1 / rate))

    def exchange(self, origin, target, amount):
        if origin not in self.node_dict or target not in self.node_dict:
            return -1

        origin_node = self.node_dict[origin]
        target_node = self.node_dict[target]

        path = self.dfs(origin_node, target_node)
        if path is None:
            return -1
        path_exchange = map(lambda p: p.rate, path)

        return reduce(lambda acc, x: acc * x, path_exchange) * amount

    def dfs(self, origin, target):
        stack = []
        visited = set()
        for childwithrate in origin.children:
            stack.append([childwithrate])
        while stack:
            curr_path = stack.pop()
            last_node, _ = curr_path[-1]
            visited.add(last_node)
            for childwithrate in last_node.children:
                if childwithrate.node in visited:
                    continue
                new_path = curr_path + [childwithrate]
                if childwithrate.node.name == target.name:
                    return new_path
                stack.append(new_path)
        return None


if __name__ == "__main__":
    exchange_rates = [('USD', 'EUR', 0.8),
                      ('USD', 'RMB', 6), ('EUR', 'BPD', 0.9)]
    s = Solution(exchange_rates)
    print(s.exchange('RMB', 'BPD', 10))
    print(s.exchange('RMB', 'RMB', 1))
    print(s.exchange('RMB', 'ABC', 1))
