import json
import graphene
import uuid


class Resource(graphene.ObjectType):
    mined = graphene.NonNull(graphene.Int)
    name = graphene.NonNull(graphene.String)


class Error(graphene.ObjectType):
    error_message = graphene.String()
    date = graphene.String()
    node_id = graphene.String()

    def __str__(self):
        s = f"""
        Error report:
            message: {self.error_message}
            date: {self.date}
            node id: {self.node_id}
        """
        return s


class Node(graphene.ObjectType):
    name = graphene.NonNull(graphene.String)
    mining = graphene.List(Resource)
    id = graphene.String()
    errors = graphene.List(Error)

    def __init__(self, name, _id=None, mining=[], errors=[]):
        if _id is None:
            _id = uuid.uuid4().hex
        super().__init__(name=name, id=_id, mining=mining, errors=errors)

    def add_error(self, error: Error):
        self.errors.append(error)


class Collection(graphene.ObjectType):
    name = graphene.String()
    resources = graphene.List(Resource)

    def remove_node(self, resources):
        for resource in resources:
            if resource in self.resources:
                resource.mined -= 1

        self.resources.sort(key=lambda x: x.mined)

    def allocate_resources(self, n: int):  # always allocates n least mined resources
        resources = []
        if n > len(self.resources):
            print("Node requested more than possible, capping at len.")
            n = len(self.resources)

        for i in range(n):
            resources.append(self.resources[i])
            self.resources[i].mined += 1

        self.resources.sort(key=lambda x: x.mined)
        return resources

    def parse_json(self, s: str):
        print(s, type(s))
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
