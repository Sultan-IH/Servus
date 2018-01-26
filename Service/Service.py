

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


"""
links.json is [
    "wired.com": 1,
    "hackernoon.com": 2,
    "/r/altcoin": 120, // refresh rate per hour,
]
res = Resource("links.json")
service = Service(res)

def add_new_node(req):
    compute = req.headers["compute_power"]
    resources = service.add_new_node(compute)
    return resources
    
def remove_node():
    
    

"""
