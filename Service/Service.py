import requests
from flask import jsonify, Flask, Response, request


class Node:
    compute_power = 0

    def __init__(self, compute_power, id):
        self.compute_power = compute_power
        self.id = id


class Service:

    def __init__(self, resource, name, port, host="localhost"):
        self.resource = resource
        self.name = name
        self.port = port
        self.host = host

    def new_node(self):
        name = request.headers.get('node_name')
        power = request.headers.get('node_compute_power')
        n = Node(compute_power=int(power), id=name)
        resources = self.resource.allocate_resources(n)
        return jsonify(resources)

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
        app.add_url_rule('/', 'new_node', self.new_node)
        app.add_url_rule('/', 'remove_node', self.remove_node)

        app.run(port=self.port)
