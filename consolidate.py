"2nd round of clean out, it yielded 2nd golden set with over 1k entries."
import json
import pprint
import random
from pathlib import Path
from types import FunctionType

import pandas as pd

from search import md5_hash

METADATA_DIR = Path('data')
IMAGE_SUFFIX = {'.jpg', '.jpeg', '.png', '.tiff'}


def fizz_buried_gems(data: [dict, list], str_gem: FunctionType):
    "Traverse dict/list bubbling up any string triggering `str_gem` filter"
    if isinstance(data, str) and str_gem(data):
        yield data
    elif isinstance(data, (int, float, str, type(None))):
        pass
    elif isinstance(data, dict):
        for key, value in data.items():
            yield from fizz_buried_gems(value, str_gem)
    elif isinstance(data, (list, tuple)):
        for item in data:
            yield from fizz_buried_gems(item, str_gem)
    else:
        print(f'Ignoring {type(data)=} {data=}')


def get_metadata(record_id: str, dirname: Path = METADATA_DIR) -> dict:
    id2 = md5_hash(record_id)
    file = dirname / f'{id2}.json'
    if not file.exists():
        metadata = None
    else:
        with open(file) as fid:
            metadata = json.load(fid)
    return metadata


def grab_concepts(metadata: dict) -> str:
    "Return string with concepts associate to a given metadata record"
    concepts = metadata.get('concepts', None)
    if concepts:
        all_concepts = []
        for concept_i in concepts:
            preflabel_i = concept_i.get('prefLabel', None)
            if preflabel_i:
                preflabel_i_en = preflabel_i.get('en', [])
                if isinstance(preflabel_i_en, list):
                    preflabel_i_en = ','.join(preflabel_i_en)
                all_concepts.append(preflabel_i_en)
        concepts = ','.join(all_concepts).lower()
    else:
        concepts = ''


def grab_year(metadata: dict) -> str:
    "Return string with year associated to a given metadata record"
    year = metadata.get('year', None)
    if year:
        year = ','.join(year)
    else:
        year = ''
    return year


def grab_images(metadata1: dict, metadata2: dict, return_list=False) -> dict:
    urls = metadata1.get('edmIsShownBy', None)
    if urls:
        urls = [urls] if isinstance(urls, str) else urls
        image_urls = {i: None for i in urls}
    else:
        image_urls = {}

    for url in fizz_buried_gems(metadata2, image_filter):
        if url in image_urls:
            continue
        image_urls[url] = None

    if return_list:
        image_urls = list(image_urls.keys())

    if len(image_urls) == 0:
        raise ValueError('No images found 😱, call 111 (aka Victor or Jay)!')
    return image_urls


def image_filter(s: str, img_keywords: [list, set, dict] = IMAGE_SUFFIX):
    """Return True if string trigger any string in image_keyword

    Arguments:
        s (str) :
        img_keywords (set) :
    """
    s = s.lower()
    return any(suffix in s for suffix in img_keywords)


with open('raw_search-art-of-sculpture.json', 'r') as fid:
    entries = []
    for i in json.load(fid):
        if i['itemsCount'] <= 0:
            continue
        entries.extend(i['items'])

golden_set_df = pd.read_csv('golden-set_2.csv')
golden_set = {i for i in golden_set_df['id'].values}

full_records, minimal_records = {}, []
for i, metadata1_i in enumerate(entries):
    record_id = metadata1_i['id']

    if record_id not in golden_set:
        continue

    metadata2_i = get_metadata(record_id)
    if metadata2_i is None:
        raise ValueError(
            f'Metadata for {record_id=} not downloaded. If it is a relevant'
            'download metadata. NO clue how? check check "search.py". Good luck!'
        )

    full_records[record_id] = {
        'search_json': metadata1_i,
        'metadata_json': metadata2_i,
    }

    minimal_records.append(
        {
            'id': metadata1_i['id'],
            'title': ';'.join(metadata1_i['title']),
            'dcCreator': ';'.join(metadata1_i.get('dcCreator', '')),
            'year': grab_year(metadata1_i),
            'concepts': grab_concepts(metadata2_i),
            'guid': metadata1_i['guid'].split('?')[0],
            'images': grab_images(metadata1_i, metadata2_i, return_list=True),
        }
    )

    # if len(minimal_records) == 1:
    #     sentinel, lucky_rabbit = True, random.choice(range(len(golden_set)))
    # if len(minimal_records) >= lucky_rabbit:
    #     if image_filter(minimal_records[-1]['images'][-1]):
    #         sentinel = False
    #     if not sentinel:
    #         pprint.pprint(metadata1_i); print(md5_hash(metadata1_i['id']))
    #         print(image_filter(metadata2_i['europeanaAggregation']['edmPreview']))
    #         import pdb; pdb.set_trace()
    #         aja = list(fizz_buried_gems(metadata2_i['europeanaAggregation'], image_filter))

# print(f'Found {len(full_records)}')
# ind = random.choice(range(len(full_records)))
# metadata_i = full_records[record_id]
# record_i = minimal_records[ind]
# record_id = record_i['id']
# print(f'Sample of search & record metadata:')
# pprint.pprint(metadata_i)
# print(f'Sample of minimal record:')
# pprint.pprint(record_i)
# print(f'Sample entry json: {md5_hash(record_id)}')

records_df = pd.DataFrame(minimal_records)

# Cross-check that for some entries, we get multiple (image) URLs
num_images = records_df['images'].apply(len)
# num_images.value_counts()
print(f'Num potential sculptures: {len(records_df["title"])}')
print(f'Num potential sculptors: {len(records_df["dcCreator"])}')
print(f'Num images: {num_images.sum()}')
# records_df.sample(n=100).to_csv('aja.csv', index=None)

# records_df.to_csv('main.csv', index=None)
