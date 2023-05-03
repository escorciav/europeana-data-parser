"""2nd round of clean out, it yielded 2nd golden set with over 1k entries."""
import json
import pprint
import random
import requests
from pathlib import Path

import pandas as pd

from search import md5_hash

metadata_dir = Path('data')
with open('raw_search-art-of-sculpture.json', 'r') as fid:
    entries = []
    for i in json.load(fid):
        if i['itemsCount'] <= 0:
            continue
        entries.extend(i['items'])

record_files, records = [], []
ind_entries = []
for i, item in enumerate(entries):
    id2 = md5_hash(item['id'])
    file = metadata_dir / f'{id2}.json'
    if not file.exists():
        continue

    ind_entries.append(i)
    with open(file) as fid:
        entry = json.load(fid)
    record_files.append(file)
    # records.append(entry)

    concepts = entry.get('concepts', None)
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

    records.append({
        'guid': item['guid'],
        'id': item['id'],
        'title': ';'.join(item['title']),
        'dcCreator': ';'.join(item.get('dcCreator', '')),
        'concepts': concepts,
    }
    )

entries = [entries[i] for i in ind_entries]

print(f'Found {len(records)}')
ind = random.choice(range(len(records)))
parent = entries[ind]
metadata = records[ind]
pprint.pprint(metadata)
print(f'Sample entry: {record_files[ind]}')

records_df = pd.DataFrame(records)
ind = records_df['concepts'].str.contains(
    'image|photo*|print*|drawing|postcards|prints|portrait*|'
    'handwriting|daguerreotype|mixed media work of art|park|'
    'paper|fragment|castle|tooth|music|postcard|negative|'
    'public transport|palace|motor car|painting|building|'
    'architecture|garden|villa|stairs'
)
print('Filtering:', ind.sum(), 'entries')
records_df = records_df.loc[~ind, :]

ind = records_df['dcCreator'].str.contains('_person|_Fotograf|#Unbekannt')
print('Filtering:', ind.sum(), 'entries')
records_df = records_df.loc[~ind, :]

ind = records_df['title'].str.contains('Servi*|foto*|Foto*')
print('Filtering:', ind.sum(), 'entries')
records_df = records_df.loc[~ind, :]

ind = records_df["dcCreator"].str.len() == 0
print('Filtering:', ind.sum(), 'entries')
records_df = records_df.loc[~ind, :]
print(records_df.shape)

records_df['cat'] = records_df.apply(
    lambda row: row['dcCreator'] + '-' + row['title'], axis=1)
records_df.drop_duplicates(subset=['cat'], keep='first', inplace=True)
records_df.drop(columns=['cat'], inplace=True)
print(records_df.shape)

records_df['id'].to_csv('golden-set_2.csv',index=None)
