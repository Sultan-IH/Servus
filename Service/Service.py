

class Node:
    compute_power = 0

    def __init__(self, compute_power):
        self.compute_power = compute_power


class Service:
    def __init__(self, resource):
        self.resource = resource

    def new_node(self, node: Node):
        resources = self.resource.allocate_resources(node)
        return resources
