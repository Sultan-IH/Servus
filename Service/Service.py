import requests
import json
from flask import jsonify, Flask, Response, request


class Node:
    def __init__(self, _id, resources):  # resources = [{resource:reddit, n: 2}]
        self.id = _id
        self.resources = resources


class Service:
    resources = []

    def __init__(self, resources, name, port, host="localhost"):
        self.resources += resources
        self.name = name
        self.port = port
        self.host = host

    def new_node(self):
        name = request.headers.get('node_name')
        rs = json.loads(request.headers.get('resources'))
        ns = json.loads(request.headers.get('how_many'))
        resources = {rs[i]: ns[i] for i in range(len(rs))}
        n = Node(name, resources)

        alloc = self.allocate_resources(n)
        return jsonify(alloc)

    def allocate_resources(self, n: Node):
        alloc = {}
        for k, i in n.resources.items():
            res = next((x for x in self.resources if x.name == k), None)
            resources = res.new_node(n)
            alloc[k] = resources
        return alloc

    def remove_node(self, node: Node):
        self.resource.deallocate_resources(node)
        res = Response()
        res.status_code = 200
        return res

    def run(self):  # app has to be provided
        headers = {
            "service_name": self.name,
            "service_port": str(self.port),
            "service_host": self.host

        }
        r = requests.get("http://localhost:4444/new_service", headers=headers)

        assert r.status_code == 200
        app = Flask('service_' + self.name)
        app.add_url_rule('/new_node', 'new_node', self.new_node)
        app.add_url_rule('/remove_node', 'remove_node', self.remove_node)

        app.run(port=self.port)
