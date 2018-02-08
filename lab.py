from Service import Service, Node
from Resource import Resource
from pprint import pprint

r = Resource("./Service/test_links.json")

n = Node(250)
pprint(r.collection)
resource = r.allocate_resources(n)
print('\n')
pprint(resource)
print('\n')

pprint(r.collection)

pprint(type(locals()['n']) == Node)