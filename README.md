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

## Study Setup
### Procedure and Participants
The study took place in a university lab and participating users were recruited via an online system of the university. 
They were paid ten Euros for taking part in the study, which lasted approximately one hour. 
To collect quantitative data, we developed a browser extension (c.f. previous section) and defined tasks for participants to perform by using this extension. 
Log data was collected automatically via the browser extension and in addition, we collected qualitative data via a questionnaire.
In this questionnaire, users were asked to indicate the result quality per task, their search intention for each task and demographic data. 

77 university students from different disciplines took part in the study.
Among the most prominent fields of study were business administration and economics (19) and law (11), followed by teaching (8) and political science (8).
The average age was 23, ranging from 19 to 31. 46 of the users were female, 31 male. 
67 considered themselves as average computer users, 9 as experts and 1 did not provide this information. All of them use the internet on a daily basis, with 28 using it less than 2 hours per day and 49 using it more than 2 hours per day.

### Tasks and Test Material
The general procedure of the four tasks, users had to perform, was the same for each task: First, users had to navigate to a particular page and a predefined section within that page. 
For this section, the relevant paragraph was already pre-selected and highlighted by the prototype. If the selection did not fit, users were asked to adapt it.
Afterwards, a search query was generated automatically for the selected paragraph  and users had to rate the results. 
Finally, they were instructed to adapt the query (and rate the corresponding results), until one of the following criteria, indicating the result quality, was met: (i) the results are perfect, (ii) it is not possible to retrieve relevant results or (iii) the time is over. The timing bounds were determined in a pretest with a small user group and set to 8 minutes per task. 

Users could select a Wikipedia page from a predefined list in the first three tasks. To gather this list, a featured article from each category was chosen at random from the list of Wikipedia's [featured articles](https://en.wikipedia.org/w/index.php?title=Wikipedia:Featured_articles&oldid=699545245) (this URL refers to the page revision used to create the list). 
The resulting list contained 35 Wikipedia pages per task from which the users could choose. On the chosen page, users were asked to navigate to a particular section.
In the fourth task, the Wikipedia page was predefined and the same for all users.

The search results were retrieved from the REST-APIs of [Mendeley](http://dev.mendeley.com) and [Europeana](http://labs.europeana.eu/api). From both providers, we retrieved at most the top-10 results and interleaved them via Round-Robin. While the content in Mendeley comprises scientific documents, Europeana features cultural objects in a variety of formats, such as text, audio, video and 3D. 
Hence, with Mendeley we perform traditional document retrieval, while with Europeana, the search is performed over the meta data of cultural objects and therefore we cover different result representations in digital libraries.
Since the Mendeley API does not support boolean queries, the query terms were sent to the Mendeley API as a simple keyword list. 
For Europeana, a boolean query with main topic and keywords was constructed.

### Dataset Statistics and Data Cleansing
During the study, 661 queries (automatic and user generated) were issued in 271 tasks, resulting in 2.4 queries on average per task. 
8650 relevance ratings have been provided for the retrieved results. 
Details have been viewed for less than 4\% of the results (331), which indicates that the results have been rated based on the result surrogates, rather than the results itself. 

From the collected data, we removed all paragraphs and their associated queries that could not clearly be assigned to a task (i.e. queries executed on pages other than the predefined ones). 
Also we removed all paragraphs and their associated queries, in which the first rated query was an already adapted one and not the automatically generated query. Furthermore, we removed queries, were no rating has been provided for any of the results. 
The cleansing was performed in order to ensure that the query sequences associated to a paragraph start with an initial automatic query and all subsequent queries are modifications by the user. This is necessary to evaluate the performance of automatic queries against the performance of user queries. Also, the cleaned data contains only queries and corresponding results for which ratings have been provided, since those are required to determine the query performance.
The cleaned dataset consists of 251 paragraphs and 558 associated queries, executed by 69 users in 228 tasks. 
The reason why there are more paragraphs than tasks is that users could modify the automatic pre-selection of a paragraph in a task. 
Even though they were instructed to apply this modification before executing any query, some users seem to have modified it after they already executed queries and rated the results. 
6985 relevance ratings have been provided for the retrieved results.
All evaluations are carried out on the cleaned dataset.
