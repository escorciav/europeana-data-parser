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
    suffix = [suffix for suffix in image_suffix if suffix in s]
    if len(suffix) <= 0:
        suffix = None
    else:
        suffix = suffix[0]
    return suffix


def download_image(url: str, image_path: Path, get_suffix=False) -> bool:
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
    except requests.exceptions.SSLError:
        print(f'Error: SSLError. Help/Google is needed {url}')
        return status
    except requests.exceptions.MissingSchema:
        print(f'Error: MissingSchema. Help/Google is needed {url}')
        return status

    if response.status_code == 200:
        if get_suffix and response.headers.get('content-type'):
            content_type, _ = requests.utils._parse_content_type_header(
                response.headers['content-type'])
            ext = content_type.split('/')[-1]

            if ext not in {'jpg', 'png', 'jpeg', 'tiff'}:
                print(f'Warning: unexpected image format {ext} for {url}')
                dump = False
            else:
                dump = True
                image_path = image_path.with_suffix(f'.{ext}')
        elif get_suffix:
            dump = False
            print(f'Error: GrabbingSuffix2. Could not get format from header {url}')

        if dump:
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
    # records_df, output_file = pd.read_csv('main.csv'), 'main_d1.csv'
    records_df, output_file = pd.read_csv('main_d2.csv'), 'main_d3.csv'
    image_dir = Path('images')
    check_if_downloaded = True
    check_if_corrupted = False
    download_all_images = True

    records_df['images'] = records_df['images'].apply(eval)
    if isinstance(records_df.loc[0, 'images'], list):
        records_df['images'] = records_df['images'].apply(
            lambda x: {url: False for url in x},
        )

    if 'downloaded' not in records_df.columns:
        records_df['downloaded'] = 0
    else:
        def count_files(record):
            record_dir = image_dir / f'{md5_hash(record["id"])}'
            return len([i.stem for i in record_dir.iterdir() if i.is_file()])

        records_df['downloaded'] = records_df.apply(count_files, axis=1)

    def update_records(df, index, url):
        df.loc[index, 'images'][url] = True
        df.loc[index, 'downloaded'] = sum(df.loc[index, 'images'].values())

    image_dir.mkdir(exist_ok=True, parents=True)
    print(f'{datetime.now().isoformat()} Downloading...')
    for i, item in records_df.iterrows():
        if i % int(len(records_df) * 0.05) == 0:
            progress = i * 100 /len(records_df)
            print(
                f'{datetime.now().isoformat()} Progress: {progress:.1f}%',
            )

        at_least_one = item['downloaded'] > 0
        if not download_all_images and at_least_one:
            continue

        record_id = item['id']
        image_dir_i = image_dir / f'{md5_hash(record_id)}'
        image_dir_i.mkdir(exist_ok=True)
        if check_if_downloaded:
            downloaded_files_noext = {
                image_dir_i / i.stem
                for i in image_dir_i.iterdir() if i.is_file()
            }

        for url, is_downloaded in item['images'].items():
            suffix = which_suffix(url)
            suffix_on_request = False
            if suffix is None:
                suffix = ''
                suffix_on_request = True
            image_path = image_dir_i / f'{md5_hash(url)}{suffix}'

            if check_if_downloaded and suffix != '':
                is_downloaded = image_path.exists()
            elif check_if_downloaded and suffix == '':
                is_downloaded = image_path in downloaded_files_noext

            if is_downloaded:
                update_records(records_df, i, url)
                if not download_all_images:
                    break
                else:
                    continue

            success = download_image(url, image_path, suffix_on_request)
            if success:
                update_records(records_df, i, url)
            else:
                print(f'Failed on: {record_id}')

            at_least_one = records_df.loc[i, 'downloaded'] > 0
            if not download_all_images and at_least_one:
                break

    progress = (records_df["downloaded"] > 0).sum()
    print(f'{progress}/{i + 1} records downloaded')
    progress = records_df["downloaded"].sum()
    print(f'{progress}/{records_df["num_images"].sum()} images downloaded')
    print(f'{datetime.now().isoformat()} Done')
    records_df.to_csv(output_file, index=False)
