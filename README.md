# Automatic query construction evaluation data

This repository contains data for the development and evaluation of queries generated automatically from a text paragraph in order to retrieve resources relevant to that paragraph. The data was collected by means of a user study in the beginning of 2016. 

Probably the most interesting files are `query_sequences.json` and `best_queries_full_features.json` in the [compiled_data  folder](compiled_data). Both are described in detail subsequently. The raw data collected via log files and questionnaires is available in [raw_data](raw_data). Results were obtained from the search APIs of [Mendeley](http://mendeley.com) and [Europeana](http://europeana.eu) during the study. To ease comparability, we ran the evaluation on a custom index, whose setup is described in the section [custom index](#custom-index)

If you have questions regarding the dataset, feel free to open an issue or contact me via E-mail (joerg.schloettere@uni-passau.de).

## query_sequences.json
This file contains all the paragraphs and corresponding queries issued during the study. It is structured as an array of the paragraphs, where each entry has the following structure:
```javascript
{
  "search_intention":"...", // the user's search intention, obtained via questionnaire
  "task" : "<task identifier>",
  "uuid" : "<user identifier>",
  "paragraph_id" : "<paragraph identifier>",
  "text" : "...", // the textual content of the paragraph
  "stopping criterion" : "...", // criterion, why the user stopped query reformulation, one of "perfect results", "no results" or "timeout"
  "page" : "http://example.org", // URL of the page containing the paragraph
  "queries" : [] // the queries, see detailed description below
}
```
The `queries` attribute in each entry is an array of corresponding queries, starting with an initial automatic query, which is possibly followed by reformulations by the user. Each entry has the following structure:
```javascript
{
  "resultsMEN" : [], // the array of results received from the Mendeley-API in response to the query
  "resultsEU" : {}, // the JSON-object received from the Europeana-API in response to the query
  "ratings" : {
    "<result identifier>" : "<rating score>" // possible values are: 0 (not relevant), 1 (cannot judge), 2 (relevant), 3 (perfect match)
    // ...
  },
  "keywords":[ // this is the query
    {
      "text" : "<the keyword>", // in case of automatically extracted keywords, represented by named entities, this is the label of the entity
      "type" : "<Person|Location|Organisation|Misc>", // type of the entity, only present if keyword is an automatically extracted entity
      "uri" : "http://example.org", // URI of the entity, only present if keyword is an automatically extracted entity
      "isMainTopic":false // determines whether the keyword is the main topic of the corresponding paragraph, either false or true
    }
    // ...
  ], 
}
```


## best_queries_full_features.json
This file is similar to the previous one, but does not contain user generated queries. Instead, it contains the keywords of the initial automatic queries and the best queries, that can be achieved, given the main topic and named entities automatically extracted from the paragraph. Compared to the previous file, it contains additional features for each extracted named entity, like its frequency and position in the text. In this file, the paragraphs are grouped per page, hence the general structure is as follows:
```javascript
{
  "<page>":{
    "<paragraph identifier>": {
      "main_topic" : {
        "text" : "<entity label>",
        "type" : "<Person|Location|Organisation|Misc>",
        "uri" : "<entity uri>",
        "isMainTopic" : true
      },
      "original_keywords":[ // the keywords from the initial query
        {
          "isMainTopic" : false,
          "text" : "<entity label>",
          "type" : "<Person|Location|Organisation|Misc>",
          "uri" : "<entity uri>",
          "freq" : 1, // frequency of occurences of this entity in the paragraph text
          "offset": [], // position(s) of the entity in the paragraph, normalized by paragraph length in terms of characters. The size of the array is equal to the maximum frequency of the keywords in original_keywords. If an entity occurs less often in the paragraph, the remaining entries are set to -1
          "sim" : 0.5322319759211719, // cosine similarity between the Doc2Vec representation of the entity and the Doc2Vec representation of the main topic in the range of 0 to 1
          "sim_avg" : 0.576498727317405 // cosine similarity between the Doc2Vec representation of the entity and the average Doc2Vec representation of the remaining entities in the range of 0 to 1
        }
        // ...
      ],
      "best_keywords" : [
        // same structure as original_keywords, but containing only keywords that form the optimal query
      ]
      
    }
  }
  // ...
}
```

## custom index
For the creation of the custom index, we used [Elasticsearch](https://www.elastic.co/products/elasticsearch) in [Version 2.2.0](https://www.elastic.co/downloads/past-releases/elasticsearch-2-2-0). The index for Europeana was created with the Snowball Analyzer and the index for Mendeley with the default settings. The necessary meta data to populate the index are available in [europeana.json](custom_index/europeana.json) and [mendeley.json](custom_index/mendeley.json). Those are the meta data of results obtained during the study. A python script to create and populate the index with the mentioned settings is available in [custom_index/es_setup.py](custom_index/es_setup.py). This script assumes the files with the meta data to be in the same folder.

## Prototype used to collect the data
The source code of the prototype is available in [chrome-extension.zip](chrome-extension.zip). However, some of the contained server calls are only accessible from within our university network. If you're looking for a quickly installable version to get an intuition of the appearance and interaction possibilities, take a look at the [EEXCESS extension in the chrome webstore](https://chrome.google.com/webstore/detail/eexcess/mnicfonfoiffhekefgjlaihcpnbchdbc), it provides similar capabilities.
