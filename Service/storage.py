import logging, simplejson
from os import path
from Service.Collection import Collection, Resource


def ressurect(db_path: str, collections):
    if path.isfile(db_path):
        logging.info("Found old state, resurrecting...")

        with open(db_path, "r") as f:
            state = simplejson.load(f)
        # collections from __init__
        collection_names = [collection.name for collection in collections]
        logging.info("resurrecting from state: ", state)
        for collection in state['collections']:

            resources = []
            for resource in collection['resources']:
                r = Resource(mined=0, name=resource['name'])
                resources.append(r)
            c = Collection(name=collection["name"], resources=resources)

            # check if the collection has been passed in already
            if collection['name'] in collection_names:
                # find the index and replace
                index = collection_names.index(collection["name"])
                collections[index] = c
            else:
                collections.append(c)
    else:
        logging.info("No old db found.")
    return collections


def save(db_path: str, collections):
    logging.info("Saving current state")
    state = {}
    with open(db_path, 'w') as file:
        state['collections'] = []
        for c in collections:
            resources = [{'name': r.name, 'mined': r.mined} for r in c.resources]
            state['collections'].append({'name': c.name, 'resources': resources})
        logging.info(state)
        simplejson.dump(state, file)
