from flask_graphql import GraphQLView
from Service.Collection import Collection, Node, Resource
from flask import jsonify, Flask
import graphene
import os.path as path
import simplejson
import atexit


class Service(graphene.ObjectType):
    name = graphene.NonNull(graphene.String)
    collections = graphene.List(Collection)
    node_registry = graphene.List(Node)

    def __init__(self, name, collections=[], node_registry=[]):
        # resurrect
        self.db_path = "./dbs/" + name + ".db"
        if path.isfile(self.db_path):
            print("Found old state, resurrecting...")
            with open(self.db_path, "r") as f:
                state = simplejson.load(f)
            collection_names = [collection.name for collection in collections]
            print("resurrecting from state: ", state)
            for collection in state['collections']:
                # check if the collection has been passed in already

                resources = []
                for resource in collection['resources']:
                    r = Resource(mined=0, name=resource['name'])
                    resources.append(r)
                c = Collection(name=collection["name"], resources=resources)

                if collection['name'] in collection_names:
                    # find the index and replace
                    index = collection_names.index(collection["name"])
                    collections[index] = c
                else:
                    collections.append(c)

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

    def save(self, ):
        print("saving current state")
        state = {}
        with open(self.db_path, 'w') as file:
            state['collections'] = []
            for c in self.collections:
                resources = [{'name': r.name, 'mined': r.mined} for r in c.resources]
                state['collections'].append({'name': c.name, 'resources': resources})
            print(state)
            simplejson.dump(state, file)

    def run(self, schema, port):
        atexit.register(self.save)
        app = Flask('service_' + self.name)
        app.add_url_rule("/graphql", view_func=GraphQLView.as_view(
            'graphql',
            schema=schema
        ))

        app.run(port=port, host='0.0.0.0')
