# annotation search service

### Turn a IIIF v3 manifest or collection into content search service.

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

### Todo

* Implement all IIIF Content Search API 2.0 API
* Handle all v3 manifest and collections