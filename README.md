## Next

1. Clean up `raw_art-of-sculpture.json`

- Describe steps in `search.py`

2. Create `art-of-sculpture.json`

## [Search](https://pro.europeana.eu/page/search)

The Search API provides a way to search for metadata records and media on the Europeana repository, for instance give me all results for the word "Vermeer".
It interacts with Europeana's data in much the same way as the Europeana website does.
You can search for keywords, and the API will return all records that match that keyword.

### [pagination](https://pro.europeana.eu/page/search#pagination)

The Search API offers two ways of paginating through the result set: basic and cursor-based pagination.

- Basic pagination is suitable for smaller or user-facing browsing applications.

- Cursor-based pagination allows for a quick iteration over the entire result set, for larger and/or harvesting applications.

## Playground

- [Search "art of sculpture", open resuability](https://api.europeana.eu/api/v2/search.json?wskey=corthawo&query=art+of+sculpture&theme=art&media=True&reusability=open&profile=rich&rows=100&cursor=*&qf=TYPE:%22IMAGE%22)

- As before via [web](https://api.europeana.eu/record/search.json?wskey=nLbaXYaiH&page=1&qf=collection:art&qf=RIGHTS:*/publicdomain/zero/*&qf=RIGHTS:*/licenses/by-sa/*&qf=RIGHTS:*/publicdomain/mark/*&qf=RIGHTS:*/licenses/by/*&qf=TYPE:"IMAGE"&qf=contentTier:(2 OR 3 OR 4)&query="Art of sculpture"&view=grid&profile=minimal&rows=24&start=1)

## Misc

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
