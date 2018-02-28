from Service.Service import Node
from Service.Collection import Error
import graphene
from SERVICES.Scraping.service import scraping_service
from SERVICES.Scraping.mailing import send_email


class NewNode(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    id = graphene.String()

    def mutate(self, info, name):
        node = Node(name=name)
        scraping_service.new_node(node)
        return NewNode(ok=True, id=node.id)


class NewError(graphene.Mutation):
    class Arguments:
        error_message = graphene.String()
        date = graphene.String()
        node_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, error_message, date, node_id):
        print(error_message, date, node_id)
        error = Error(error_message=error_message, date=date, node_id=node_id)
        node = scraping_service.find_node(node_id)

        if node is None:
            return NewError(ok=False)
        else:
            node.add_error(error)
            send_email("ksula0155@gmail.com", "Error in Scraping", error)
            return NewError(ok=True)


class RemoveNode(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    id = graphene.String()

    def mutate(self, info, id):
        print("removing node with id: ", id)
        scraping_service.remove_node(id)
        return RemoveNode(ok=True, id=id)


class AddResources(graphene.Mutation):
    class Arguments:
        collection = graphene.String()
        new_resources = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info, new_resources, collection):
        scraping_service.add_resources(collection, new_resources)
        return AddResources(ok=True)


class RemoveResources(graphene.Mutation):
    class Arguments:
        collection = graphene.String()
        old_resources = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info, old_resources, collection):
        scraping_service.remove_resources(collection, old_resources)
        return RemoveResources(ok=True)


class Mutations(graphene.ObjectType):
    new_node = NewNode.Field()
    add_resources = AddResources.Field()
    remove_resources = RemoveResources.Field()
    remove_node = RemoveNode.Field()
    report_error = NewError.Field()
