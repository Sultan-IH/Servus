import json
import math


class Resource:
    collection = []  # collection of tuples; resources to be mined.

    def __init__(self, file: str = None, sjson: str = None):
        if file:
            with open(file, "r") as f:
                self.parse_json(f.read())
        if sjson:
            self.parse_json(sjson)

    def allocate_resources(self, node):
        arr = self.find_sum_from_array(node.compute_power)
        return arr

    def find_sum_from_array(self, x) -> list:
        arr = [x[1] for x in self.collection]
        elms = []  # contains indexes of elements that are selected
        s = 0  # contains the sum of elements
        current_error = x - s
        first_element_error = math.fabs(x - (s + arr[0])) <= math.fabs(current_error)

        while current_error and first_element_error and sum(arr) > 0:

            for i, j in enumerate(arr):
                if len(arr) - 1 >= i + 1:  # check to see if next element exists
                    next_error = x - (s + arr[i + 1])
                    if next_error < 0:
                        s += j
                        elms.append(i)
                        del arr[i]
                        break
                else:  # we've found the element with the least possible error
                    s += j
                    elms.append(i)
                    del arr[i]
                    break

            if len(arr) == 0:  # check if we've exhausted all resources
                break
            else:
                current_error = x - s
                first_element_error = x - (s + arr[0])
        return elms

    def parse_json(self, s: str):
        d = json.loads(s)
        c = list(d.items())
        self.collection = self.collection + c
        self.collection.sort(key=lambda x: x[1])
