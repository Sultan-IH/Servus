import json
import math
import requests
from typing import Union, List, Tuple
from Service.Service import Node


class Resource:
    collection = []  # resources to be mined.
    nodes = {}

    def __init__(self, name: str, file: str = None, sjson: str = None, link: str = None):
        self.name = name
        if file:
            with open(file, "r") as f:
                self.parse_json(f.read())
        if sjson:
            self.parse_json(sjson)
        if link:
            r = requests.get(link)
            self.collection = r.json()

    def new_node(self, node: Node):
        n = node.resources[self.name]
        resources = self.allocate_resources(n)
        # should store indexes of resources
        if node.id in self.nodes:
            self.nodes[node.id] += resources
        else:
            self.nodes[node.id] = resources
        resources = [r["name"] for r in resources]
        return resources

    def remove_node(self, node: Node):
        resources = self.nodes[node.id]
        for r in resources:
            i = self.collection.index(r)
            self.collection[i]["mined"] -= 1
        self.nodes[node.id] = []

    def allocate_resources(self, n: int):  # always allocates n least mined resources
        resources = []
        for i in range(n):
            resources.append(self.collection[i])
            self.collection[i]["mined"] += 1
        self.collection.sort(key=lambda x: x["mined"])
        return resources

    def parse_json(self, s: str):
        resources = json.loads(s)
        for item in resources:
            d = {
                "name": item,
                "mined": 0,
            }
            self.collection.append(d)

        self.collection.sort(key=lambda x: x["mined"])


"""
IN MEMORY OF THE USELESS ALGORITHM I WROTE:

    def find_sum_from_array(self, x) -> Tuple[List, Union[int, any]]:
        arr = [x[1] for x in self.collection]
        elms = []  # contains indexes of elements that are selected
        s = 0  # contains the sum of elements
        current_error = x - s
        first_element_error = math.fabs(x - (s + arr[0])) <= math.fabs(current_error)

        while current_error and first_element_error and sum(arr) > 0:
            # print("iter started.")
            for i in range(len(arr)):
                if len(arr) - 1 >= i + 1:  # check to see if next element exists
                    cee = math.fabs(x - (s + arr[i]))  # current element error
                    nee = x - (s + arr[i + 1])  # next element error
                    if nee < 0:
                        # print(cee, nee, arr[i])
                        if cee > math.fabs(nee):  # what if they are equal?
                            i += 1
                            # print("adding: ", arr[i])
                        s += arr[i]
                        elms.append(i)
                        arr = arr[:i]
                        break
                else:  # we've found the element with the least possible error
                    s += arr[i]
                    elms.append(i)
                    arr = arr[:i]
                    break
            # print("middle of the loop!")
            current_error = x - s
            if len(arr) == 0:  # check if we've exhausted all resources
                break
            else:
                first_element_error = math.fabs(x - (s + arr[0])) <= math.fabs(current_error)
                # print("ce: ", current_error, "fee: ", first_element_error)

            # print("Iter finished", arr, s)
        return elms, current_error
"""
