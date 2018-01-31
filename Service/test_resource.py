from unittest import TestCase
from Service.Resource import Resource
from Service.Service import Node


class TestResource(TestCase):
    def test_find_sum_from_array1(self):
        r = Resource("./Service/test_links.json")
        n = Node(123)
        elms, remainder = r.allocate_resources(n)

        self.assertEqual(elms, [4, 2])
        self.assertEqual(remainder, 0)
        n = Node(127)

        elms, remainder = r.allocate_resources(n)

        self.assertEqual(elms, [4, 2, 1, 0])
        self.assertEqual(remainder, 1)
