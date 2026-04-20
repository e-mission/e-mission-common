from __future__ import annotations  # __: skip


def memoize(fn: function) -> function:
    '''
    Simple memoization decorator
    '''
    _cache = {}

    # __pragma__('kwargs')
    def wrapper(*args, **kwargs):
        if (str(args), str(kwargs)) not in _cache:
            _cache[(str(args), str(kwargs))] = fn(*args, **kwargs)
        return _cache[(str(args), str(kwargs))]
    # __pragma__('nokwargs')
    return wrapper


# e-mission-phone www/js/diary/timelineHelper.ts unpackServerData()
def flatten_db_entry(entry: dict) -> dict:
    '''
    DB entries retrieved from the server have '_id', 'metadata', and 'data' fields.
    This function returns a shallow copy of the obj, which flattens the 'data' field into the top
    level, while also including '_id', 'user_id', 'metadata.key', and 'metadata.origin_key'.
    '''
    # JS implementation
    '''?
    __pragma__('js', '{}', """
      return {
          ...entry.data,
          _id: entry._id,
          'user_id': entry.user_id,
          key: entry.metadata.key,
          origin_key: entry.metadata.origin_key
      }
    """)
    ?'''
    # Python implementation
    # __pragma__('skip')
    return {
        **entry['data'],
        '_id': entry['_id'],
        'user_id': entry['user_id'],
        'key': entry['metadata']['key'],
        'origin_key': entry['metadata']['origin_key'] if 'origin_key' in entry['metadata'] else None
    }
    # __pragma__('noskip')


resources = {}


async def read_json_resource(filename: str) -> dict:
    """
    Read a JSON file from '/resources' and return the contents as a dict
    """
    global resources
    if filename in resources:
        return resources[filename]

    '''?
    __pragma__('js', '{}', """
    const __resourcesMap = {
      'egrid2018_intensities.json': () => import('../src/emcommon/resources/egrid2018_intensities.json'),
      'egrid2018_subregions_5pct.json': () => import('../src/emcommon/resources/egrid2018_subregions_5pct.json'),
      'egrid2019_intensities.json': () => import('../src/emcommon/resources/egrid2019_intensities.json'),
      'egrid2019_subregions_5pct.json': () => import('../src/emcommon/resources/egrid2019_subregions_5pct.json'),
      'egrid2020_intensities.json': () => import('../src/emcommon/resources/egrid2020_intensities.json'),
      'egrid2020_subregions_5pct.json': () => import('../src/emcommon/resources/egrid2020_subregions_5pct.json'),
      'egrid2021_intensities.json': () => import('../src/emcommon/resources/egrid2021_intensities.json'),
      'egrid2021_subregions_5pct.json': () => import('../src/emcommon/resources/egrid2021_subregions_5pct.json'),
      'egrid2022_intensities.json': () => import('../src/emcommon/resources/egrid2022_intensities.json'),
      'egrid2022_subregions_5pct.json': () => import('../src/emcommon/resources/egrid2022_subregions_5pct.json'),
      'label-options.default.json': () => import('../src/emcommon/resources/label-options.default.json'),
      'ntd2018_intensities.json': () => import('../src/emcommon/resources/ntd2018_intensities.json'),
      'ntd2019_intensities.json': () => import('../src/emcommon/resources/ntd2019_intensities.json'),
      'ntd2020_intensities.json': () => import('../src/emcommon/resources/ntd2020_intensities.json'),
      'ntd2021_intensities.json': () => import('../src/emcommon/resources/ntd2021_intensities.json'),
      'ntd2022_intensities.json': () => import('../src/emcommon/resources/ntd2022_intensities.json')
    };
    const r = await __resourcesMap[filename]();
    resources[filename] = r.default;
    return resources[filename];
    """)
    ?'''

    # __pragma__('skip')
    import os
    import json
    currdir = os.path.dirname(__file__)
    filepath = os.path.join(currdir, f"resources/{filename}")
    with open(filepath) as f:
        resources[filename] = json.load(f)
        return resources[filename]
    # __pragma__('noskip')


async def fetch_url(url: str) -> dict:
    """
    Fetch a URL and return the response as a dict
    """

    '''?
    response = await fetch(url)
    if (not response.ok):
        raise Exception(f"Failed to fetch {url}: {response.text()}")
    return await response.json()
    ?'''

    # __pragma__('skip')
    import requests
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}: {response.text}")
    return response.json()
    # __pragma__('noskip')
