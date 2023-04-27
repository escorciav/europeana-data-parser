import hashlib
import json
import requests
from dataclasses import dataclass, asdict
from pathlib import Path

import config

SESSION = requests.Session()
SEARCH_URL = 'https://www.europeana.eu/api/v2/search.json'

@dataclass
class SearchParams:
    "Refer to details here, https://pro.europeana.eu/page/search#get-started"
    wskey: str = config.API_KEY
    query: str = 'art of sculpture'
    theme: str = 'art'
    media: bool = True
    reusability: str = 'open'
    profile: str = 'rich'
    rows: int = 100
    cursor: str = None


def md5_hash(string: str) -> str:
    "Get md5 hash of a given string"
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def search(query: str, cursor=None) -> dict:
    "Search a given query in Europeana search API"
    params = SearchParams()
    params.query = query
    params.cursor = cursor
    params_dict = asdict(params)

    response = SESSION.get(SEARCH_URL, params=params_dict)

    if response.status_code == 200:
        response = response.json()
        del response['apikey']
    elif response.status_code == 401:
        raise ValueError('Error: authentication failed')
    elif response.status_code == 429:
        raise NotImplementedError('Error 429: application has reached its usage limit.')
    elif response.status_code == 500:
        raise NotImplementedError(
            'Error 500: error has occorred in the server which has not been '
            'properly handled. If you receive this error it means that '
            'something has gone really wrong, so please report them to Europeana!'
        )
    else:
        raise ValueError(
            f'Error API request failed, status code {response.status_code}\n{response.text}'
        )
    return response


def get_all(query):
    "Get all responses of a given query"
    all_responses = []

    response = search(query, cursor='*')
    if response.get('itemsCount', 0) > 0:
        all_responses.append(response)

    next_cursor = response.get('nextCursor', None)
    while next_cursor:
        response = search(query, cursor=next_cursor)
        if response.get('itemsCount', 0) > 0:
            all_responses.append(response)
        next_cursor = response.get('nextCursor', None)

    return responses


# responses = get_all_pages(query='art of sculpture')
# with open('raw_art-of-sculpture.json', 'w') as fid:
#     json.dump(responses, fid)

with open('raw_search-art-of-sculpture.json', 'r') as fid:
    responses = json.load(fid)

items = []
for response in responses:
    if response['itemsCount'] <= 0:
        continue

    for item in response['items']:
        if item.get('type') != 'IMAGE':
            continue

        # items.append(item)
        # Consider retaining
        # id
        # dcCreator : array String
        # dcDescription
        # title
        # guid
        # link (relevant, but it exposes API key!)

        id2 = md5_hash(item['id'])
        record_file = Path(f'data/{id2}.json')
        if record_file.exists():
            continue

        record = requests.get(item['link'])
        if record.status_code == 200:
            record = record.json()['object']
            with open(record_file, 'w') as fid:
                json.dump(record, fid)
        else:
            # raise ValueError(f'Error: API request failed, status code {record.status_code}')
            print(f'API request failed, status code {record.status_code}')
            import pdb; pdb.set_trace()

# import pprint
# item_i = items[-1]
# import random
# item_i = random.choice(items)
# pprint.pprint(item_i)

# print(f'Found {len(items)} items')
# import pdb; pdb.set_trace()
