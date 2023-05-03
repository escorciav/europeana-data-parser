import builtins
import requests
from pathlib import Path
from datetime import datetime

import pandas as pd
from PIL import Image, JpegImagePlugin

from search import md5_hash

SESSION = requests.Session()


def which_suffix(s: str, image_suffix=['.jpg', '.png', '.jpeg', '.tiff']) -> str:
    "Return the images suffix present in s"
    s = s.lower()
    return [suffix for suffix in image_suffix if suffix in s][0]


def download_image(url: str, image_path: Path) -> bool:
    "Download image from a given url"
    status = False
    try:
        response = requests.get(url)
    except requests.exceptions.ProxyError:
        print(
            'Error: ProxyError, 👏 Kudos to IT/ISP/Government for awesome '
            f'security protocols 🙃 {url}'
        )
        return status

    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        status = True
    else:
        print(f'Error: {response.status_code} {url}')

    return status


def print(*args, **kwargs):
    builtins.print(*args, flush=True, **kwargs)


def parse_datetime(iso_string: str) -> datetime:
    return datetime.fromisoformat(iso_string)


if __name__ == '__main__':
    records_df = pd.read_csv('main.csv', )
    image_dir = Path('images')
    check_if_downloaded = True
    check_if_corrupted = False

    records_df['images'] = records_df['images'].apply(eval)
    if isinstance(records_df.loc[0, 'images'], list):
        records_df['images'] = records_df['images'].apply(
            lambda x: {url: False for url in x},
        )
    else:
        raise NotImplementedError
    records_df['downloaded'] = 0

    def update_records(df, index, url):
        df.loc[index, 'downloaded'] += 1
        df.loc[index, 'images'][url] = True

    image_dir.mkdir(exist_ok=True, parents=True)
    print(f'{datetime.now().isoformat()} Downloading...')
    for i, item in records_df.iterrows():
        if i % int(len(records_df) * 0.05) == 0:
            progress = i * 100 /len(records_df)
            print(
                f'{datetime.now().isoformat()} Progress: {progress:.1f}%',
            )

        record_id = item['id']
        image_dir_i = image_dir / f'{md5_hash(record_id)}'
        image_dir_i.mkdir(exist_ok=True)

        for url, is_downloaded in item['images'].items():
            image_path = image_dir_i / f'{md5_hash(url)}{which_suffix(url)}'

            if check_if_downloaded:
                is_downloaded = image_path.exists()

            # Check if image is corrupted
            if is_downloaded and not check_if_corrupted:
                update_records(records_df, i, url)
            elif is_downloaded and check_if_corrupted:
                try:
                    if image_path.suffix.lower() in {'.jpg', '.jpeg'}:
                        with open(image_path, 'rb') as f:
                            img = JpegImagePlugin.JpegImageFile(f)
                    else:
                        img = Image.open(image_path)
                    is_downloaded = True
                except:
                    is_downloaded = False

            if is_downloaded:
                update_records(records_df, i, url)

            success = download_image(url, image_path)
            if success:
                update_records(records_df, i, url)
            else:
                print(f'Failed on: {record_id}')

        # item = records_df.loc[i]
        # import pprint; pprint.pprint(item)
        # import pprint; pprint.pprint(item['images'])
        # import pdb; pdb.set_trace()
    progress = (records_df["downloaded"] > 0).sum()
    print(f'{progress}/{i + 1} records downloaded')
    progress = records_df["downloaded"].sum()
    print(f'{progress}/{records_df["num_images"].sum()} images downloaded')
    print(f'{datetime.now().isoformat()} Done')
    records_df.to_csv('main_d1.csv', index=False)
