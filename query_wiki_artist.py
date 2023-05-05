import json
from pathlib import Path

import utils

# Given a Category in Wikimedia ontology (graph := tree?), e.g.,
# "Category:Sculptures by artist"
# https://commons.wikimedia.org/wiki/Category:Sculptures_by_artist
# we load all the categories connected to that node.
parent_json = Path("data/sculptures_by_artist.json")

parent_dir = parent_json.with_suffix('')
if not parent_dir.exists():
    raise ValueError(f'Type folder with nodes connected to {parent_json=}')

node_exist_fn = lambda x: (parent_dir / f'{x}.json').exists()
with open(parent_json, 'r') as fid:
    records = json.load(fid)
    categories = {
        i.get("pageid"): node_exist_fn(i.get("pageid"))
        for i in records
        if i.get("pageid")
    }

found = sum(i for i in categories.values())
print(f'Parsing node: {parent_json.stem}')
print(f'Crawled nodes: {found}/{len(categories)}')
for i, (node_id, downloaded) in enumerate(categories.items()):
    # sanity check. It assumes Python >= 3.5 (dicts are sorted)
    assert node_id == records[i].get("pageid")

    node = records[i]
    node['downloaded'] = downloaded
    if not downloaded:
         continue
    title_i = node.get('title')


    node_json = parent_dir / f'{node_id}.json'
    with open(node_json, 'r') as fid:
         node_metadata = json.load(fid)
    node['sculptor'] = utils.grab_sculptor(node['title'])

    import random, pprint
    # TODO: augment node dict with relevant info
    if random.random() < 0.01 and len(node_metadata['files']) < 10:
        print(f'====> {i}')
        pprint.pprint(node)
        pprint.pprint(node_metadata)
        import ipdb; ipdb.set_trace()
        node['files'] = node_metadata.get('files')
        node['cats'] = node_metadata.get('cats')

# Do I need to traverse the subnodes? No. Thanks Jay!

print(f"{len(categories)=}")
import random
# sample a random key from categories
categories = categories.key()
random.choice(list(categories.items()))

# request.head(query=query)

subcategories = {
    file_res.get("pageid")
    for json_file in Path("data/sculptures_by_artist").glob("*.json")
    for file_res in json.load(json_file.open()).get("cats")
}

print(f"{len(subcategories)=}")

# NOTE: this verifies that for Category:Sculptures by Ruth Abernethy
# that all categories are searched and the correct quantity of images received.
# This also tests/validates that cat is correct.
test_cat = json.load(Path("data/sculptures_by_artist/10295765.json").open())
subcats = test_cat.get("cats")
files = test_cat.get("files")

sc1 = [i for i in files if i.get("cat") == "Category:Glenn Gould statue, Toronto"]
sc2 = [i for i in files if i.get("cat") == "Category:Imagine (Ruth Abernathy)"]
sc3 = [i for i in files if i.get("cat") == "Category:Statue of Oscar Peterson"]

assert len(sc1) == 5
assert len(sc2) == 4
assert len(sc3) == 13
assert len(subcats) == 3
assert len(files) == 29
print(len(files))
