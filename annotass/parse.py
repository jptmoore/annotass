from iiif_prezi3 import *
from jsonpath_ng import parse
from data import Data

class Parse:
    def __init__(self, ctx):
        self.ctx = ctx
        self.data = Data(ctx)
        self.index = None
    
    def basic_headers(self):
        dict = {}
        return dict

    def get_json(self, url):
        headers = self.basic_headers()
        try:
            response = self.ctx.session.get(url, verify=False, headers=headers)
        except Exception as e:
            print(f"failed to get annotation: {repr(e)}")
            return None
        if response.status_code != 200:
            print(f"failed to get annotation")
            return None
        else:
            result = response.json()
            return result

    
    def get_annotation_page_content(self, url):
        json = self.get_json(url)
        return json  

    def match_annotation_page_body_value(self, content):
        jsonpath_expression = parse("items[*].body.value")
        result = [match.value for match in jsonpath_expression.find(content)]
        return result
    
    def match_annotation_page_target(self, content):
        jsonpath_expression = parse("items[*].target")
        result = [match.value for match in jsonpath_expression.find(content)]
        return result

    def write_data(self, target, commenting):
        match target, commenting:
            case [id], [text]:
                self.data.write_data(id, text)
            case _:
                raise "ouch"


    def match_annotation_content_item(self, x):
        match x:
            case AnnotationPage(id=id, type='AnnotationPage'):
                content = self.get_annotation_page_content(id)
                commenting = self.match_annotation_page_body_value(content)
                target = self.match_annotation_page_target(content)
                self.write_data(target,commenting)
            case _:
                raise('ouch')


    def match_annotations(self, x):
        match x:
            case []:
                print('empty')
            case [*xs]:
                for x in xs:
                    self.match_annotation_content_item(x)
            case _:
                raise('oppps')

    def match_manifest_item(self, x):
        match x:
            case Canvas(items=items, annotations=annotations):
                self.match_annotations(annotations)
            case _:
                raise('ouch')
        

    def get_manifest_content(self, url):
        json = self.get_json(url)
        manifest = Manifest(**json)
        return manifest


    def get_manifest_ref(self, id):
        manifest = self.get_manifest_content(id)
        match manifest:
            case Manifest(items=items):
                for item in items:
                    self.match_manifest_item(item)
            case _:
                raise('ouch')



    def match_collection_item(self, x):
        match x:
            case ManifestRef(id=id):
                self.get_manifest_ref(id)
            case CollectionRef():
                print('CollectionRef')
            case Collection():
                print('Collection')
            case _:
                raise('ouch')
        

    def get_collection(self, url):
        json = self.get_json(url)
        collection = Collection(**json)
        return collection


    def process_collection(self, x):
        match x:
            case Collection(items=items):
                for item in items:
                    self.match_collection_item(item)
            case _:
                raise('ouch')
            

    def run(self, url):
        self.index = self.data.create_index()
        obj = self.get_collection(url)
        self.process_collection(obj)
        



        
        