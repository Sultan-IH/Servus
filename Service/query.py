import graphene
from Service.Collection import Resource, Node
from Service import __service__


class RootQuery(graphene.ObjectType):
    get_resources = graphene.Field(graphene.List(Resource), n=graphene.Int(), collection=graphene.String(),
                                   id=graphene.String())
    test_query = graphene.String()

    read_resources = graphene.Field(graphene.List(Resource), collection=graphene.String())

    collection_nodes = graphene.Field(graphene.List(Node), collection=graphene.String())

    def resolve_get_resources(self, info, **kwargs):
        id = kwargs.get('id')
        n = kwargs.get('n')
        collection = kwargs.get('collection')

        resources = __service__.alloc_resources(id=id, resource=collection, n=n)
        return resources

    def resolve_read_resources(self, info, **kwargs):
        collection_name = kwargs.get('collection')
        collection = __service__.find_collection(collection_name)

        return collection.resources

    def resolve_test_query(self, info, **kwargs):
        return "resolved"