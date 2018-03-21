from Service.Service import Node, Metrics
from Service.Collection import Error
from Service import __service__
import graphene
from .mailing import send_error_report, send_metric_report


class MetricsReport(graphene.Mutation):
    class Arguments:
        node_id = graphene.String()
        report = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, node_id, report):
        m = Metrics(node_id=node_id, report=report)
        node = __service__.find_node(node_id)
        send_metric_report("ksula0155@gmail.com", "Scraping Metric report", m, node)
        send_metric_report("vincnttan@gmail.com", "Scraping Metric report", m, node)
        return MetricsReport(ok=True)


class NewNode(graphene.Mutation):
    class Arguments:
        node_name = graphene.NonNull(graphene.String)
        program_name = graphene.NonNull(graphene.String)
        version = graphene.NonNull(graphene.String)

    ok = graphene.Boolean()
    id = graphene.String()

    def mutate(self, info, node_name, program_name, version):
        node = Node(node_name=node_name, program_name=program_name, version=version)
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
            send_error_report("ksula0155@gmail.com", "Error in Scraping", error, node)
            send_error_report("vincnttan@gmail.com", "Error in Scraping", error, node)
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
    new_report = MetricsReport.Field()
