import json
import elasticsearch

es = elasticsearch.Elasticsearch()
index1 = "europeana"
index2 = "mendeley"
ctn = 1

# create europeana index
index_settings_eu = {
    "settings":
        {
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "snowball"
                    }
                }
            }
        }
}
es.indices.create(index=index1, body=json.dumps(index_settings_eu))


# populate europeana index with metadata from file
with open('europeana.json', 'r') as f:
    data = json.load(f)
    for result in data:
        res = es.index(index=index1, doc_type='result', id=ctn, body=json.dumps(result))
        ctn += 1


ctn = 1
# populate mendeley index with metadata from file
with open('mendeley.json', 'r') as f:
    data = json.load(f)
    for result in data:
        res = es.index(index=index2, doc_type='result', id=ctn, body=json.dumps(result))
        ctn += 1