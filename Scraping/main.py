import Service

subreddits = Service.Collection(name="subreddits", resources=[])
sources = Service.Collection(name="sources", resources=[])
searches = Service.Collection(name="searches", resources=[])

scraping_service = Service.Service(name="scraping", collections=[subreddits, sources, searches], node_registry=[])
schema = Service.init(scraping_service)

scraping_service.run(schema=schema, port=4555)
