"""Search entries in WGA catalog

See also:
- https://github.com/escorciav/europeana-data-parser#121-query-syntax
"""

from pathlib import Path

import pandas as pd

from search import search, SearchParams, SEARCH_URL, SESSION


def escape_space(s: str) -> str:
    s = s.replace(',', '').replace(';', '')
    s = s.lower()
    return s.replace(' ', '+AND+')


def grab_city(s: str) -> str:
    s_list = s.split(',')
    city = s
    if len(s_list) > 1:
        city = s_list[-1]
    return city


wga_dir = Path('../../data/wga')
wga_csv = wga_dir / 'main.csv'
wga_df = pd.read_csv(wga_csv)
print(wga_df.columns)

wga_df['city'] = wga_df['LOCATION'].apply(grab_city)
ind = wga_df['LOCATION'].str.contains(
    'Private collection|New York|Washington|Los Angeles|Boston|Chicago|'
    'Detroit|Cleveland|Philadelphia|Brazil|São Paulo|San Francisco|Seattle'
    'Houston|Metropolitan Museum of Art|Cincinnati|Providence|Buenos Aires'
    'Ohio'
)
import pdb; pdb.set_trace()

wga_df = wga_df.sample(n=5)
print(wga_df)

row = wga_df.iloc[0]
query_i = f'{row["TITLE"].lower()} by {row["AUTHOR"].lower()}'
print('Human query:', query_i)
query_api = (
    f'({escape_space(row["TITLE"])})+AND+'
    f'who:({escape_space(row["AUTHOR"])})'
)
print('Europeana query:', query_api)
# TODO: let this running for 1k queries
# response = search(query=query_i)
