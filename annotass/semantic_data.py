import chromadb

class Data:
    def __init__(self, ctx: object) -> None:
        self.annotation_limit = ctx.annotation_limit
        self.distance_threshold = ctx.distance_threshold
        client = chromadb.Client()
        self.collection = client.create_collection("collection.chromadb")

    def write_data(self, id: str, content: str) -> None:
        self.collection.add(documents=[content], ids=[id])

    def __filter_distance(self, data):
        uris = data['ids'][0]
        distances = data['distances'][0]
        #print(distances)
        result = []
        for uri,distance in zip(uris,distances):
            if float(distance) <= self.distance_threshold:
                result.append(uri)
        return result


    def search_data(self, term: str, page: int) -> tuple[int, list[str]]:
        if page < 0:
            return (0, [])
        results = self.collection.query(
            query_texts=[term],
            n_results=self.annotation_limit,
        )
        #print(results)
        uris = self.__filter_distance(results)
        results_len = len(uris)
        result = (results_len, uris)
        return result

# class Context:
#     pass
# ctx = Context()
# ctx.annotation_limit = 200
# ctx.distance_threshold = 1.0
# data = Data(ctx)
# data.write_data(id="foo", content="the cat sat on the mat")
# data.write_data(id="bar", content="the tabby has grey and white stripes")
# result = data.search_data("a cat", 1)
# print(result)