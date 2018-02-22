from unittest import TestCase
from Service.Resource import Resource
from Service.Service import Node


class TestResource(TestCase):
    def allocate_resource(self):
        r = Resource("reddit", "./Service/test_links.json")
        n = Node("Test1", {"reddit": 2})
        resources = r.new_node(n)
