# Europeana

<<<<<<< HEAD
## 1. Europeana relevant pointers

### 1.1 [Harvesting and Downloads](https://pro.europeana.eu/page/harvesting-and-downloads#downloads)

Given a "dataset number" name, we can retrieve the metadata, and content:

- `wget ftp://download.europeana.eu/dataset/XML/2021672.zip`, OR

- `curl -O ftp://download.europeana.eu/dataset/XML/2021672.zip`


### 1.2 [Search](https://pro.europeana.eu/page/search)
=======
- Describe steps in `search.py`

## [Search](https://pro.europeana.eu/page/search)
>>>>>>> 2b93e26 ([docs] Push relevant link)

The Search API provides a way to search for metadata records and media on the Europeana repository, for instance give me all results for the word "Vermeer".
It interacts with Europeana's data in much the same way as the Europeana website does.
You can search for keywords, and the API will return all records that match that keyword.

#### 1.2.1 [Query syntax](https://pro.europeana.eu/page/search#syntax)

Relevant to search for a given artpiece, artist, or combo.

Try out some queries in [this console](https://pro.europeana.eu/page/api-rest-console?function=search&query=%22Mona%20Lisa%22)

#### 1.2.2 [pagination](https://pro.europeana.eu/page/search#pagination)

The Search API offers two ways of paginating through the result set: basic and cursor-based pagination.

- Basic pagination is suitable for smaller or user-facing browsing applications.

- Cursor-based pagination allows for a quick iteration over the entire result set, for larger and/or harvesting applications.

### 1.3 Metadata meaning

Refer to:

- [Europeana metasets](https://pro.europeana.eu/page/search#metadata-sets)

- [EDM biz](https://pro.europeana.eu/page/intro#edm).

### Playground

- [Search "art of sculpture", open resuability](https://api.europeana.eu/api/v2/search.json?wskey=corthawo&query=art+of+sculpture&theme=art&media=True&reusability=open&profile=rich&rows=100&cursor=*&qf=TYPE:%22IMAGE%22)

- As before but via web:

    ```
    https://api.europeana.eu/record/search.json?wskey=nLbaXYaiH&page=1&qf=collection:art&qf=RIGHTS:*/publicdomain/zero/*&qf=RIGHTS:*/licenses/by-sa/*&qf=RIGHTS:*/publicdomain/mark/*&qf=RIGHTS:*/licenses/by/*&qf=TYPE:"IMAGE"&qf=contentTier:(2 OR 3 OR 4)&query="Art of sculpture"&view=grid&profile=minimal&rows=24&start=1
    ```

## 3. Misc

```python
first_request['success'], first_request['totalResults']
first_request['nextCursor']
# AoJ++fncg4YDPwkvMjAyMTAwNy9fU0xTQV8zNjdfU0xTQV8zNjdfYnJldl8xODc5XzE5
next_page['success'], next_page['totalResults']
next_page['nextCursor']
# AoJwgezD0IUDLy8yMDQ4MTI4LzU3NTIwOQ==

print(response.url)
# request gotten from web browser search
```

## Inbox

1. Explore metadata.

    - `edmLandingPage` := page in Europeana

    - `concepts`, refer to [links here](#metadata-meaning)

    - `dcTitle`, refer to [links here](#metadata-meaning)

    - proxies:

      - [dctermsMedium](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/medium)

1. Filter ideas

    - Check/Count `dcCreator`

        - "_Fotograf" in

    - Type of object? "Photography"; "Photography genre"; "teapots" ;"reliefs (sculptures)"

        - Print -> http://data.europeana.eu/concept/2538

    - Is part of: "Grafik- und Fotosammlung"

1. Merge catalogs

    - [Indexes 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/indexes/getting_started.html)

    - [Pandas DataFrame — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/dataframe.html)
    - [Directory Loader — 🦜🔗 ](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/directory_loader.html)
    - [MediaWikiDump — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/mediawikidump.html)
    - [Sitemap — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/sitemap.html)
    - [Getting Started — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/agents/getting_started.html)
    - [Wikipedia API — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/agents/tools/examples/wikipedia.html)
    - [SearxNG Search API — 🦜🔗 LangChain](https://python.langchain.com/en/latest/modules/agents/tools/examples/searx_search.html)
    - [Wikimedia — SearXNG Documentation (2023.5.3+e840c481)](https://docs.searxng.org/src/searx.engines.wikipedia.html#id2)
    - [Google Engines — SearXNG Documentation](https://docs.searxng.org/src/searx.engines.google.html#module-searx.engines.google_images)
    - [citiususc/pyplexity: Cleaning tool for web scraped text](https://github.com/citiususc/pyplexity)

1. Visualization tools

    - [Arize-ai/phoenix: ML Observability in a Notebook - Uncover Insights, Surface Problems, Monitor, and Fine Tune your Generative LLM, CV and Tabular Models](https://github.com/Arize-ai/phoenix)
