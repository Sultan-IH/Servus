from flask_graphql import GraphQLView
from Service.Collection import Collection, Node
from flask import jsonify, Flask
import graphene


class Service(graphene.ObjectType):
    name = graphene.NonNull(graphene.String)
    collections = graphene.List(Collection)
    node_registry = graphene.List(Node)

    def new_node(self, n: Node):
        self.node_registry.append(n)

    def add_resources(self, name, new_resources):
        collection = self.find_collection(name)
        collection.add_resources(new_resources)

    def remove_resources(self, name, new_resources):
        collection = self.find_collection(name)
        new_resources = collection.remove_resources(new_resources)
        return new_resources

    def find_collection(self, name):
        collection = next((x for x in self.collections if x.name == name), None)
        return collection

    def alloc_resources(self, id: str, resource: str, n: int):
        res = self.find_collection(resource)
        node = self.find_node(id)
        if node is None:
            print("hasnt been registered with a proper request")
            return []
        resources = res.allocate_resources(n)
        return resources

    def find_node(self, id):
        node = next((x for x in self.node_registry if x.id == id), None)
        return node

    def remove_node(self, _id):
        self.node_registry = [node for node in self.node_registry if node.id != _id]

    def run(self, schema, port):
        app = Flask('service_' + self.name)
        app.add_url_rule("/graphql", view_func=GraphQLView.as_view(
            'graphql',
            schema=schema
        ))

        app.run(port=port)
