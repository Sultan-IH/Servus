import graphene
from .query import RootQuery
from .mutations import Mutations
from .service import scraping_service

schema = graphene.Schema(query=RootQuery, mutation=Mutations, auto_camelcase=True)

scraping_service.run(schema=schema, port=4555)
