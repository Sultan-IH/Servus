from Service import Service, Resource

jsons = """
[
    "altcoin",
    "cryptomarkets",
    "ethtrader",
    "Cryptocurrency",
    "iota",
    "altcoin"

]
"""

reddit_resource = Resource(name="subreddits", sjson=jsons)
reddit_service = Service(name="scraping", port=4446, resources=[reddit_resource])
reddit_service.run()
