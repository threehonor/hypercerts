import json
import sys
import urllib.parse
import os
import json

from utils import datify


METADATA_DIR = "metadata"
OUT_FILENAME = 'minting_urls.txt'


def safe_url_attr(name, value):
    return urllib.parse.quote(name, safe='') + '=' + urllib.parse.quote(value, safe='') + '&'


def create_url(metadata):
    url = 'https://hypercerts.vercel.app/hypercerts/create?'

    url += safe_url_attr('description', metadata['description'])
    url += safe_url_attr('name', metadata['name'])

    work_time_start = datify(metadata['properties']['work_timeframe']['value'][0])
    url += safe_url_attr('workTimeStart', work_time_start)

    work_time_end = datify(metadata['properties']['work_timeframe']['value'][1])
    url += safe_url_attr('workTimeEnd', work_time_end)

    impact_time_start = datify(metadata['properties']['impact_timeframe']['value'][0])
    url += safe_url_attr('impactTimeStart', impact_time_start)

    impact_time_end = datify(metadata['properties']['impact_timeframe']['value'][1]).lower()
    url += safe_url_attr('impactTimeEnd', impact_time_end)

    for idx, right in enumerate(metadata['properties']['rights']['value']):
        url += safe_url_attr(f"rights[{idx}]", right)
    
    for idx, work_scope in enumerate(metadata['properties']['work_scope']['value']):
        url += safe_url_attr(f"workScopes[{idx}]", work_scope)

    for idx, impact_scope in enumerate(metadata['properties']['impact_scope']['value']):
        url += safe_url_attr(f"impactScopes[{idx}]", impact_scope)
    
    contributors = metadata['properties']['contributors']['value']
    url += safe_url_attr('contributors', contributors)

    allowlist_url = metadata['hidden_properties']['allowlist']
    url += safe_url_attr('allowlistUrl', allowlist_url)
    
    url += safe_url_attr('fractions', "10000")

    return url


def create_urls(metadata_dir, out_filename):
    grants_metadata = []
    for file in os.scandir(metadata_dir):
        with open(file, 'r') as f:
            grants_metadata.append(json.loads(f.read()))

    urls = []
    for metadata in grants_metadata:
        url = create_url(metadata)
        urls.append(url) 

    with open(out_filename, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

    

if __name__ == "__main__":
    metadata_dir = sys.argv[1] if len(sys.argv) == 2 else METADATA_DIR
    out_filename = sys.argv[2] if len(sys.argv) == 3 else OUT_FILENAME

    create_urls(metadata_dir, out_filename)