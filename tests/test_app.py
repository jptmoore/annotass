import unittest
import json
from iiif_prezi3 import Manifest, AnnotationPage
from unittest import TestCase
import requests



url = 'http://localhost:5555'

class IntegrationTests(TestCase):


    @classmethod
    def setUpClass(self):
        manifest_json = json.load(open("tests/web/embedded-manifest.json"))
        self.manifest = Manifest(**manifest_json)

    def test_status_code_200(self):
        ret = requests.get(f"{url}/search?q=foo")
        self.assertEqual(ret.status_code, 200, "endpoint found")

    def test_status_code_404(self):
        ret = requests.get(f"{url}/does_not_exist")
        self.assertEqual(ret.status_code, 404, "test endpoint not found")

    def test_received_annotation_page_type(self):
        ret = requests.get(f"{url}/search?q=mit")
        json = ret.json()
        ap = AnnotationPage(**json)
        self.assertEqual(type(ap), AnnotationPage, "test for annotation page type")

    def test_received_annotation_items_length(self):
        ret = requests.get(f"{url}/search?q=mit")
        json = ret.json()
        ap = AnnotationPage(**json)
        items = ap.items
        self.assertEqual(len(items), 1, "test for annotation items length")


if __name__ == "__main__":
    unittest.main()