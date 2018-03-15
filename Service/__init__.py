import logging
import yaml
from datetime import datetime

date = datetime.now().strftime("%Y-%m-%d.%H:%M:%S")


def get_version():
    with open('config.yaml') as file:
        try:
            config = yaml.load(file)
        except yaml.YAMLError as exc:
            print(exc)

    return config['version']


logfile = "./logs/" + date + "." + get_version() + ".servus.log"

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
