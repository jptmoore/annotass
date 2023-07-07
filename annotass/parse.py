from iiif_prezi3 import *
import sys
import requests_cache
from data import Data
from store import Store
from response import Response

class Parse:
    def __init__(self, ctx):
        self.data = Data(ctx)
        self.index = None
        self.store = Store(ctx)
        self.response = Response(ctx)
        self.cache = requests_cache.CachedSession(ctx.cache_fname)

    def pp(self, msg):
        print(f"\U0001F680 {msg}")

    def pp_exit(self, msg):
        print(f"\n\U0001F4A5 {msg}", file=sys.stderr)
        sys.exit(1)

    def basic_headers(self):
        dict = {}
        return dict

    def get_json(self, url):
        headers = self.basic_headers()
        try:
            response = self.cache.get(url, verify=False, headers=headers)
        except Exception as e:
            self.pp_exit('failed to fetch json')
        if response.status_code != 200:
            self.pp_exit('failed to get a 200 response code')
        else:
            result = response.json()
            return result

    
    def get_annotation_page_content(self, url):
        json = self.get_json(url)
        ap = AnnotationPage(**json)
        return ap  
                    

    def match_w3c_annotation_item(self, x):
        match x:
            case Annotation(id=id, body=body):
                self.data.write_data(id=id, content=body.value)
                self.store.write(uri=id, annotation=x.json())
            case _:
                self.pp_exit('failed to find annotation')


    def match_wc3_annotations(self, x):
        match x:
            case []:
                self.pp_exit('no W3C annotations to process')
            case [*xs]:
                for x in xs:
                    self.match_w3c_annotation_item(x)


    def match_annotation_content_item(self, x):
        match x:
            case AnnotationPage(id=id, type='AnnotationPage', items=items):
                match items:
                    case []:
                        ap = self.get_annotation_page_content(id)
                        self.match_annotation_content_item(ap)
                    case [*xs]:
                        self.match_wc3_annotations(xs)
            case _:
                self.pp_exit('failed to find annotation page')


    def match_annotations(self, x):
        match x:
            case []:
                self.pp_exit('no annotations to process')
            case [*xs]:
                for x in xs:
                    self.match_annotation_content_item(x)

    def match_manifest_item(self, x):
        match x:
            case Canvas(items=items, annotations=annotations):
                self.match_annotations(annotations)
            case _:
                self.pp_exit('failed to find canvas items')
        

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
                self.pp_exit('failed to find manifest items')



    def match_collection_item(self, x):
        match x:
            case ManifestRef(id=id):
                self.get_manifest_ref(id)
            case Manifest(id=id):
                print('Manifest')
            case CollectionRef():
                print('CollectionRef')
            case Collection():
                print('Collection')
            case _:
                self.pp_exit('only supports Manifest, ManifestRef', 'CollectionRef',  'Collection')
        

    def process_collection(self, x):
        match x:
            case Collection(items=items):
                for item in items:
                    self.match_collection_item(item)
            case _:
                self.pp_exit('failed to find collection items')


    def run_collection(self, json):
        self.pp("processing collection...")
        collection = Collection(**json)
        self.store.open()
        self.store.create_table()
        self.process_collection(collection)
        self.store.commit()        


    def process_manifest(self, x):
        match x:
            case Manifest(items=items):
                for item in items:
                    self.match_manifest_item(item)
            case _:
                self.pp_exit('failed to find manifest items')        

    def run_manifest(self, json):
        self.pp("processing manifest...")
        manifest = Manifest(**json)
        self.store.open()
        self.store.create_table()
        self.process_manifest(manifest)
        self.store.commit()          


    def run(self, url):
        self.index = self.data.create_index()
        json = self.get_json(url)
        match json['type']:
            case 'Collection':
                self.run_collection(json)
            case 'Manifest':
                self.run_manifest(json)            
            case _:
                self.pp_exit('failed to find collection or manifest')


    def search(self, q, page):
        (total, uris) = self.data.search_data(q, page)
        items = []
        for uri in uris:
            item = self.store.read(uri)
            items.append(item)
        result = self.response.build(q, page, total, items)
        return result
    
    def shutdown(self):
        self.store.close()

        



        
        