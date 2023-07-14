import unittest
from iiif_prezi3 import AnnotationPage, Annotation
from unittest import TestCase
import requests

url = 'http://localhost:5555'

class IntegrationTest(TestCase):

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

    def test_received_annotation(self):
        ret = requests.get(f"{url}/search?q=mit")
        json = ret.json()
        ap = AnnotationPage(**json)
        anno = ap.items[0]
        self.assertEqual(type(anno), Annotation, "test for annotation")

    def test_received_annotation_motivation(self):
        ret = requests.get(f"{url}/search?q=mit&motivation=commenting")
        json = ret.json()
        ap = AnnotationPage(**json)
        items = ap.items
        self.assertGreater(len(items), 0, "test for annotation motivation")


    def test_received_annotation_motivation_not_matched(self):
        ret = requests.get(f"{url}/search?q=mit&motivation=foo")
        json = ret.json()
        ap = AnnotationPage(**json)
        items = ap.items
        self.assertEqual(len(items), 0, "test for annotation motivation not matched")


    def test_received_annotation_body_value(self):
        ret = requests.get(f"{url}/search?q=mit")
        json = ret.json()
        ap = AnnotationPage(**json)
        anno = ap.items[0]
        value = anno.body.value
        self.assertEqual(value, "Göttinger Marktplatz mit Gänseliesel Brunnen", "test for annotation body value")

    def test_received_annotation_empty_search_result(self):
        ret = requests.get(f"{url}/search?q=foo")
        json = ret.json()
        ap = AnnotationPage(**json)
        items = ap.items
        self.assertEqual(items, [], "test empty search result")

if __name__ == "__main__":
    unittest.main()