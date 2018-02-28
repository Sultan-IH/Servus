import graphene

from SERVICES.Scraping.query import RootQuery
from SERVICES.Scraping.mutations import Mutations
from SERVICES.Scraping.service import scraping_service

schema = graphene.Schema(query=RootQuery, mutation=Mutations, auto_camelcase=True)

scraping_service.run(schema, port=4555)
