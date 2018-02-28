from Service.Service import Service
from Service.Collection import Collection

subreddits = Collection(name="subreddits",  resources=[])
sources = Collection(name="sources",  resources=[])
searches = Collection(name="searches",  resources=[])

scraping_service = Service(name="scraping", collections=[subreddits, sources, searches], node_registry=[])
