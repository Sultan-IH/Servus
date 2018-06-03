from flask_graphql import GraphQLView
from Service.Collection import Collection, Node, Resource
from flask import Flask
import graphene, atexit, logging
import Service.storage as storage


class Service(graphene.ObjectType):
    name = graphene.NonNull(graphene.String)
    collections = graphene.List(Collection)
    # this is for keeping track of properly registered nodes
    node_registry = graphene.List(Node)

    def __init__(self, name, collections=[], node_registry=[]):
        # resurrect
        self.db_path = "./dbs/" + name + ".db"
        collections = storage.ressurect(db_path=self.db_path, collections=collections)

        super().__init__(name=name, collections=collections, node_registry=node_registry)

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

    def alloc_resources(self, id: str, collection: str, n: int):
        coll = self.find_collection(collection)
        resources = coll.allocate_resources(id, n)
        node = self.find_node(id)
        if node is None:
            logging.warning("Node" + id + "hasn't been registered with a proper request")
            return []
        return resources

    def find_node(self, _id) -> Node:
        node = next((x for x in self.node_registry if x.id == _id), None)
        return node

    def remove_node(self, _id):
        for coll in self.collections: coll.remove_node(_id)
        self.node_registry = [node for node in self.node_registry if node.id != _id]


    def save(self):
        storage.save(self.db_path, self.collections)

    def run(self, schema, port):
        atexit.register(self.save)
        app = Flask('service_' + self.name)
        app.add_url_rule("/graphql", view_func=GraphQLView.as_view(
            'graphql',
            schema=schema
        ))
        logging.info("running on port %d", port)

        app.run(port=port, host='0.0.0.0')


class Metrics(graphene.ObjectType):
    node_id = graphene.NonNull(graphene.String)
    report = graphene.NonNull(graphene.String)
