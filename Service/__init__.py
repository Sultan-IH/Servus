from Service.Service import Service
from Service.Collection import Collection, Resource, Node

__service__ = None


def init(service):
    global __service__
    __service__ = service

    import graphene
    from .query import RootQuery
    from .mutations import Mutations

    return graphene.Schema(query=RootQuery, mutation=Mutations, auto_camelcase=True)
