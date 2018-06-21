import json
import graphene
import uuid
import logging


class Resource(graphene.ObjectType):
    mined = graphene.NonNull(graphene.Int)
    name = graphene.NonNull(graphene.String)


class Error(graphene.ObjectType):
    error_message = graphene.String()
    date = graphene.String()
    node_id = graphene.String()
    node_name = graphene.String()

    def __str__(self):
        s = f"""
        Error report:
            message: {self.error_message}
            date: {self.date}
            Node:
                id: {self.node_id}
                name: {self.node_name}
        """
        return s


class Node(graphene.ObjectType):
    node_name = graphene.NonNull(graphene.String)
    mining = graphene.List(Resource)
    id = graphene.String()
    errors = graphene.List(Error)
    program_name = graphene.NonNull(graphene.String)
    version = graphene.NonNull(graphene.String)

    def __init__(self, node_name, program_name, version, _id=None, mining=[], errors=[]):
        if _id is None:
            _id = uuid.uuid4().hex
        super().__init__(node_name=node_name, id=_id, mining=mining, errors=errors, program_name=program_name,
                         version=version)

    def node_html(self):
        return f"""
        <div>
            <p>program name: {self.program_name} </p>
            <p>version: {self.version} </p>
            <p>node: {self.node_name}</p>
        </div>
        """

    def add_error(self, error: Error):
        self.errors.append(error)


class Collection(graphene.ObjectType):
    name = graphene.String()
    resources = graphene.List(Resource)
    node_registry = {}

    def remove_node(self, _id):
        if self.node_registry[_id] is None:
            return None
        unwated_resources = self.node_registry[_id]

        def decrement(x):
            if x in unwated_resources:
                x.mined -= 1
            return x

        self.resources = [decrement(resource) for resource in self.resources]
        self.resources.sort(key=lambda x: x.mined)

    def allocate_resources(self, id: str, n: int):  # always allocates n least mined resources
        resources = []
        if n > len(self.resources):
            logging.info("Node requested more than possible, capping at len.")
            n = len(self.resources)

        for i in range(n):
            resources.append(self.resources[i])
            self.resources[i].mined += 1

        self.node_registry[id] = resources
        self.resources.sort(key=lambda x: x.mined)
        return resources

    def parse_json(self, s: str):
        resources = json.loads(s)
        self.add_resources(resources)

    def remove_resources(self, old_resources):
        self.resources = [d for d in self.resources if d.name not in old_resources]
        self.resources.sort(key=lambda x: x.mined)
        return self.resources

    def add_resources(self, l):
        for name in l:
            resource = Resource(name=name, mined=0)
            self.resources.append(resource)

        self.resources.sort(key=lambda x: x.mined)
