import sys
import requests_cache
from iiif_prezi3 import (
    Manifest,
    ManifestRef,
    CollectionRef,
    Collection,
    Canvas,
    CanvasRef,
    Annotation,
    AnnotationPage,
    AnnotationPageRef,
)
from pydantic import Extra, ValidationError
Annotation.Config.extra = Extra.allow

from sqlite3 import IntegrityError

from search_data import Data
from annotation_store import Store
from date import Date
from response import Response
from context import Context


class Parse:
    def __init__(self, ctx: Context) -> None:
        self.data = Data(ctx)
        self.store = Store(ctx)
        self.date = Date(ctx)
        self.response = Response(ctx)
        self.cache = requests_cache.CachedSession(ctx.cache_fname)

    def pp_info(self, msg: str) -> None:
        print(f"\U0001F680 {msg}")

    def pp_warn(self, msg: str) -> None:
        print(f"\U000026A0 {msg}")

    def pp_error(self, msg: str) -> None:
        print(f"\U0001F4A5 {msg}", file=sys.stderr)
        sys.exit(1)

    def __basic_headers(self):
        dict = {}
        return dict

    def __get_json(self, url):
        headers = self.__basic_headers()
        try:
            response = self.cache.get(url, headers=headers)
        except Exception as e:
            self.pp_error(f"failed to fetch json: {repr(e)}")
        if response.status_code != 200:
            self.pp_error("failed to get a 200 response code")
        else:
            try:
                result = response.json()
            except Exception as e:
                self.pp_error(f"failed to parse json: {repr(e)}")
            else:
                return result

    def __get_annotation_page_content(self, url):
        json = self.__get_json(url)
        try:
            ap = AnnotationPage(**json)
        except ValidationError:
            self.pp_error("Could not validate AnnotationPage")
        return ap
    
    def __write_data(self, id, annotation, content):
        data = annotation.json()
        self.data.write_data(id=id, content=content)
        try:
            self.store.write(uri=id, annotation=data)
        except IntegrityError:
            self.pp_error("failed as annotations id's are not unique")        

    def __handle_body_as_list(self, id, annotation, body):
        for index, item in enumerate(body):
            unique_id = f"{id}_{index}"
            if "value" in item:
                self.__write_data(id=unique_id, annotation=annotation, content=item["value"])

    def __handle_body_as_object(self, id, annotation, body):
        self.__write_data(id, annotation, content=body.value)

    def __match_w3c_annotation_item(self, x):
        match x:
            case Annotation(id=id, body=body, motivation=motivation) if motivation in [
                "commenting",
                "supplementing",
                "tagging",
            ]:
                if type(body) is list:
                    self.__handle_body_as_list(id, x, body)
                else:
                    self.__handle_body_as_object(id, x, body)
            case _:
                self.pp_error("failed to find annotation")

    def __match_wc3_annotations(self, x):
        match x:
            case []:
                self.pp_error("no W3C annotations to process")
            case [*xs]:
                for x in xs:
                    self.__match_w3c_annotation_item(x)

    def __match_annotation_content_item(self, x):
        match x:
            case AnnotationPage(id=id, type="AnnotationPage", items=items):
                match items:
                    case []:
                        ap = self.__get_annotation_page_content(id)
                        self.__match_annotation_content_item(ap)
                    case [*xs]:
                        self.__match_wc3_annotations(xs)
            case AnnotationPageRef(id=id):
                ap = self.__get_annotation_page_content(id)
                self.__match_annotation_content_item(ap)
            case _:
                self.pp_error("failed to find annotation page")

    def __match_annotations(self, x):
        match x:
            case []:
                self.pp_warn("found an empty annotation list")
                pass
            case [*xs]:
                for x in xs:
                    self.__match_annotation_content_item(x)
            case _:
                self.pp_error("failed to find annotations")

    def __get_canvas_content(self, url):
        json = self.__get_json(url)
        try:
            cc = Canvas(**json)
        except ValidationError:
            self.pp_error("Could not validate the canvas")
        return cc

    def __match_manifest_item(self, x):
        match x:
            case Canvas(annotations=annotations):
                self.__match_annotations(annotations)
            case CanvasRef(id=id):
                cc = self.__get_canvas_content(id)
                self.__match_manifest_item(cc)                
            case _:
                self.pp_error("failed to find canvas annotations")

    def __get_collection_content(self, url):
        json = self.__get_json(url)
        try:
            collection = Collection(**json)
        except ValidationError:
            self.pp_error("Could not validate the collection")
        return collection

    def __get_manifest_content(self, url):
        json = self.__get_json(url)
        try:
            manifest = Manifest(**json)
        except ValidationError:
            self.pp_error("Could not validate the manifest")
        return manifest

    def __match_collection_item(self, x):
        match x:
            case ManifestRef(id=id):
                manifest = self.__get_manifest_content(id)
                self.__match_collection_item(manifest)
            case Manifest(id=id):
                self.__match_manifest(x)
            case CollectionRef(id=id):
                collection = self.__get_collection_content(id)
                self.__match_collection_item(collection)
            case Collection(id=id):
                self.__match_collection(x)
            case _:
                self.pp_error(
                    "only supports Manifest, ManifestRef", "CollectionRef", "Collection"
                )

    def __match_manifest(self, x):
        match x:
            case Manifest(items=items):
                for item in items:
                    self.__match_manifest_item(item)
            case _:
                self.pp_error("failed to find manifest items")

    def __match_collection(self, x):
        match x:
            case Collection(items=items):
                for item in items:
                    self.__match_collection_item(item)
            case _:
                self.pp_error("failed to find collection items")

    def __run_collection(self, json):
        self.pp_info("processing collection...")
        try:
            collection = Collection(**json)
        except ValidationError:
            self.pp_error("Could not validate the collection")
        self.store.open()
        self.store.create_table()
        self.__match_collection(collection)
        self.store.commit()

    def __run_manifest(self, json):
        self.pp_info("processing manifest...")
        try:        
            manifest = Manifest(**json)
        except ValidationError:
            self.pp_error("Could not validate the manifest")        
        self.store.open()
        self.store.create_table()
        self.__match_manifest(manifest)
        self.store.commit()

    def run(self, url: str) -> None:
        self.data.create_index()
        json = self.__get_json(url)
        match json["type"]:
            case "Collection":
                self.__run_collection(json)
            case "Manifest":
                self.__run_manifest(json)
            case _:
                self.pp_error("failed to find collection or manifest")
 

    def __has_motivation(self, item, motivation):
        annotation = Annotation(**item)
        match motivation:
            case []:
                return True
            case [x]:
                motivations = x.split(" ")
                return annotation.motivation in motivations

    # not using as prezi not supporting created item
    def __date_in_range(self, item, date):
        annotation = Annotation(**item)
        result = self.date.in_range(check=annotation.created, ranges=date)
        return result

    # to be implemented later
    def __handle_ignored(self, date, user):
        ignored = []
        if date != None:
            ignored.append("date")
        if user != None:
            ignored.append("user")
        return ignored

    def search(
        self, q: str, motivation: str, date: str, user: str, page: int
    ) -> dict[str, object]:
        (total, uris) = self.data.search_data(q, page)
        items = []
        for uri in uris:
            item = self.store.read(uri)
            if self.__has_motivation(item, motivation):
                items.append(item)
        ignored = self.__handle_ignored(date, user)
        result = self.response.build(q, ignored, page, total, items)
        return result

    def shutdown(self) -> None:
        self.store.close()
