from Service.Service import Node
from Service.Collection import Error
from Service import __service__
import graphene
from .mailing import send_email


class NewNode(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    id = graphene.String()

    def mutate(self, info, name):
        node = Node(name=name)
        __service__.new_node(node)
        return NewNode(ok=True, id=node.id)


class NewError(graphene.Mutation):
    class Arguments:
        error_message = graphene.String()
        date = graphene.String()
        node_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, error_message, date, node_id):
        node = __service__.find_node(node_id)

        error = Error(error_message=error_message, date=date, node_id=node.id, node_name=node.name)

        if node is None:
            return NewError(ok=False)
        else:
            node.add_error(error)
            send_email("ksula0155@gmail.com", "Error in Scraping", error)
            send_email("vincnttan@gmail.com", "Error in Scraping", error)
            return NewError(ok=True)


class RemoveNode(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    id = graphene.String()

    def mutate(self, info, id):
        __service__.remove_node(id)
        return RemoveNode(ok=True, id=id)


class AddResources(graphene.Mutation):

    class Arguments:
        collection = graphene.String()
        new_resources = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info, new_resources, collection):
        __service__.add_resources(collection, new_resources)
        return AddResources(ok=True)


class RemoveResources(graphene.Mutation):
    class Arguments:
        collection = graphene.String()
        old_resources = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info, old_resources, collection):
        __service__.remove_resources(collection, old_resources)
        return RemoveResources(ok=True)


class Mutations(graphene.ObjectType):
    new_node = NewNode.Field()
    add_resources = AddResources.Field()
    remove_resources = RemoveResources.Field()
    remove_node = RemoveNode.Field()
    report_error = NewError.Field()
