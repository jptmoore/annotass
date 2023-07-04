
class Response:
    def __init__(self, ctx):
        self.search_url = ctx.search_url
        self.annotation_limit = ctx.annotation_limit

    def simple_template(self, q, page, items):
        dict = {
            "@context": "http://iiif.io/api/search/2/context.json",
            "id": f"{self.search_url}?q={q}&page={page}",
            "type": "AnnotationPage",
            "items": items,
        }
        return dict

    def part_of(self, q, total, total_pages):
        first = f"{self.search_url}?q={q}&page=0"
        last = f"{self.search_url}?q={q}&page={total_pages}"
        dict = {
            "partOf": {
                "id": f"{self.search_url}?q={q}",
                "type": "AnnotationCollection",
                "total": total,
                "first": {"id": first, "type": "AnnotationPage"},
                "last": {"id": last, "type": "AnnotationPage"}
            }
        }
        return dict

    def paged_template(self, q, page, total, items):
        start_index = page * self.annotation_limit
        total_pages = int(total / self.annotation_limit)
        dict = self.simple_template(q, page, items)
        dict.update(self.part_of(q, total, total_pages))
        if page > 0:
            dict["prev"] = f"{self.search_url}?q={q}&page={page-1}"
        if page < total_pages:
            dict["next"] = f"{self.search_url}?q={q}&page={page+1}"
        dict["start_index"] = start_index
        return dict

    def build(self, q, page, total, items):
        if total > self.annotation_limit:  # if paged response
            return self.paged_template(q, page, total, items)
        else:
            return self.simple_template(q, page, items)
