from unittest import TestCase
from Service.Resource import Resource
from Service.Service import Node


class TestResource(TestCase):
    def test_find_sum_from_array(self):
        r = Resource("./Service/test_links.json")
        n = Node(123)
        elms = r.allocate_resources(n)
        self.assertEqual(elms, [4, 2])
