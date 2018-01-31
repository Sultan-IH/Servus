import json
import math
import requests
from typing import Union, List, Tuple
from Service.Service import Node


class Resource:
    collection = []  # collection of tuples; resources to be mined.

    def __init__(self, file: str = None, sjson: str = None, link: str = None):
        if file:
            with open(file, "r") as f:
                self.parse_json(f.read())
        if sjson:
            self.parse_json(sjson)
        if link:
            r = requests.get(link)
            self.collection = r.json()

    def allocate_resources(self, node: Node):
        arr, remainder = self.find_sum_from_array(node.compute_power)
        resources = []
        for i in arr[:-1]:
            resources.append(self.collection[i][:])
        last_r = self.collection[arr[-1]][:]
        if remainder < 0:
            last_r[1] += remainder
        resources.append(last_r)
        self.adjust_resources(arr, remainder)
        return resources

    def adjust_resources(self, indexes, remainder):
        for i in indexes[:-1]:
            self.collection[i][1] = 0
        i = indexes[-1]

        if remainder < 0:
            self.collection[i][1] = -remainder  # what if its positive
        else:
            self.collection[i][1] = 0
        self.collection.sort(key=lambda x: x[1])

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

    def parse_json(self, s: str):
        d = json.loads(s)
        c = [list(t) for t in d.items()]
        self.collection = self.collection + c
        self.collection.sort(key=lambda x: x[1])
