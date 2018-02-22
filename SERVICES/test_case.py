from Service.Resource import Resource
from Service.Service import Node

sjson = """
[
  "wired.com",
  "hackernoon.com",
  "news.com",
  "something.net"
]
"""

r = Resource("sources", sjson=sjson)
n = Node("sultan",
         {"sources": 2})
j = Node("vince",
         {"sources": 2})

print(r.new_node(n))
print(r.collection, '\n')
print(r.remove_node(n))
print(r.collection, '\n')
print(r.new_node(j))
print(r.collection, '\n')
print(r.nodes)
