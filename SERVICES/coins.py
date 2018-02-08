import requests as req
import pickle
from os.path import isfile
from Service import Service, Resource

if not isfile("./coins.pickle"):
    res = req.get("https://raw.githubusercontent.com/vincnt/Lambo/master/coinlist.json").json()
    GOOGLE_QUERY_COMP = 100  # 1/REFRESH_RATE where refresh rate is per second
    resource = [["google:" + val['Name'] + '+' + key, GOOGLE_QUERY_COMP] for key, val in res.items()]
    coins_resource = Resource()
    coins_resource.collection = resource
else:
    with open('./coins.pickle', 'rb') as f:
        coins_resource = pickle.load(f)

coins_service = Service(name="coins_service", port=4445, resource=coins_resource)
coins_service.run()
