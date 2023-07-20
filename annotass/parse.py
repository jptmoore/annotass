import sys
import requests_cache
from iiif_prezi3 import (
    Manifest,
    ManifestRef,
    CollectionRef,
    Collection,
    Canvas,
    Annotation,
    AnnotationPage,
)
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
            self.pp_error("failed to fetch json")
        if response.status_code != 200:
            self.pp_error("failed to get a 200 response code")
        else:
            result = response.json()
            return result

    def __get_annotation_page_content(self, url):
        json = self.__get_json(url)
        ap = AnnotationPage(**json)
        return ap

    def __match_w3c_annotation_item(self, x):
        match x:
            case Annotation(
                id=id, body=body, motivation=motivation
            ) if motivation == "commenting" or motivation == "supplementing":
                self.data.write_data(id=id, content=body.value)
                self.store.write(uri=id, annotation=x.json())
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

    def __match_manifest_item(self, x):
        match x:
            case Canvas(annotations=annotations):
                self.__match_annotations(annotations)
            case _:
                self.pp_error("failed to find canvas annotations")

    def __get_collection_content(self, url):
        json = self.__get_json(url)
        collection = Collection(**json)
        return collection

    def __get_manifest_content(self, url):
        json = self.__get_json(url)
        manifest = Manifest(**json)
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
        collection = Collection(**json)
        self.store.open()
        self.store.create_table()
        self.__match_collection(collection)
        self.store.commit()

    def __run_manifest(self, json):
        self.pp_info("processing manifest...")
        manifest = Manifest(**json)
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
