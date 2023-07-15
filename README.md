# annotation search service

### Turn a IIIF v3 manifest or collection containing annotations into a content search service

Start up the server:
```
❯ python app.py https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/manifest.json
🚀 processing manifest...
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5555
 * Running on http://192.168.1.95:5555
Press CTRL+C to quit
```

Query the service:
```
❯ curl -s 'localhost:5555/search?q=mit' | jq
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "http://localhost:5555/search?q=mit&page=0",
  "ignored": [],
  "items": [
    {
      "@context": "http://iiif.io/api/presentation/3/context.json",
      "body": {
        "format": "text/plain",
        "language": "de",
        "type": "TextualBody",
        "value": "Göttinger Marktplatz mit Gänseliesel Brunnen"
      },
      "id": "https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/canvas-1/annopage-2/anno-1",
      "motivation": "commenting",
      "target": "https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/canvas-1",
      "type": "Annotation"
    }
  ],
  "type": "AnnotationPage"
}
```

### Demo

The OCR content available here https://github.com/jptmoore/awesome-iiif-annotations is available to search:

```
❯ curl -s 'https://miiify.rocks/iiif/content/search?q=eastcote' | jq
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://miiify.rocks/iiif/content/search?q=eastcote&page=0",
  "ignored": [],
  "items": [
    {
      "@context": "http://iiif.io/api/presentation/3/context.json",
      "body": {
        "format": "text/plain",
        "type": "TextualBody",
        "value": "Harrow-on-the-Hill, crowned by church and school, is the capital of this Riding of Metro-land ; Ruislip and Northwood are its lake district; Eastcote and Ickenham, Harefield and Pinner are its rustic townships. London is at your very door, if you needs must keep in touch with London, but it is always pure country at the corner of the lane beyond your garden fence. The town has stained the country less here than in Essex, Kent or Surrey, at the same radius of ten or twenty miles from Charing Cross."
      },
      "id": "https://miiify.rocks/annotations/diamond_jubilee_of_the_metro/image_28_block_8",
      "motivation": "commenting",
      "target": "https://miiifystore.s3.eu-west-2.amazonaws.com/diamond_jubilee_of_the_metro/c/3/f88e6e3a-177b-4fec-a15d-7e3f8300c993#xywh=324,2125,1057,374",
      "type": "Annotation"
    }
  ],
  "type": "AnnotationPage"
}
```

### Todo

* Implement all Content Search API 2.0
* Handle all v3 manifest and collections gracefully