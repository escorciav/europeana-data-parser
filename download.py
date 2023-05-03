import requests
from pathlib import Path

import pandas as pd

from search import md5_hash

SESSION = requests.Session()


def which_suffix(s: str, image_suffix=['.jpg', '.png', '.jpeg', '.tiff']) -> str:
    "Return the images suffix present in s"
    s = s.lower()
    return [suffix for suffix in image_suffix if suffix in s][0]


def download_image(url: str, image_path: Path) -> bool:
    "Download image from a given url"
    response, status = requests.get(url), False
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        status = True
    else:
        print(f'Error: {response.status_code} {url}')

    return status


if __name__ == '__main__':
    records_df = pd.read_csv('main.csv', )
    image_dir = Path('images')

    records_df['images'] = records_df['images'].apply(eval)
    if isinstance(records_df.loc[0, 'images'], list):
        records_df['images'] = records_df['images'].apply(
            lambda x: {url: False for url in x},
        )
    else:
        raise NotImplementedError
    records_df['downloaded'] = 0

    image_dir.mkdir(exist_ok=True, parents=True)
    for i, item in records_df.iterrows():
        record_id = item['id']
        image_dir_i = image_dir / f'{md5_hash(record_id)}'
        image_dir_i.mkdir(exist_ok=True)

        for url, is_downloaded in item['images'].items():
            image_path = image_dir_i / f'{md5_hash(url)}{which_suffix(url)}'
            if is_downloaded:
                raise NotImplementedError

            success = download_image(url, image_path)
            if success:
                records_df.loc[i, 'downloaded'] += 1
                records_df.loc[i, 'images'][url] = True
            else:
                print(f'Failed on: {record_id}')

        # item = records_df.loc[i]
        # import pprint; pprint.pprint(item)
        # import pprint; pprint.pprint(item['images'])
        # import pdb; pdb.set_trace()

        if (i + 1) % 200 == 0:
            print(f'{i * 100 /len(records_df):.1f}% done')
    print(f'{(records_df["downloaded"] > 0).sum()}/{i + 1} images downloaded')
    print('Done')
    records_df.to_csv('main_d1.csv', index=False)
