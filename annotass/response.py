import urllib.parse

class Response:
    def __init__(self, ctx):
        self.search_url = ctx.search_url
        self.annotation_limit = ctx.annotation_limit

    def simple_template(self, q, ignored, distance, items):
        escaped_q = urllib.parse.quote(q)
        dict = {
            "@context": "http://iiif.io/api/search/2/context.json",
            "id": f"{self.search_url}?q={escaped_q}&distance={distance}",
            "type": "AnnotationPage",
            "ignored": ignored,
            "items": items,
        }
        return dict

    def build(self, q, ignored, distance, items):
        return self.simple_template(q, ignored, distance, items)
