import json
import sqlite3
from pathlib import Path

import flatdict as flatdict


if __name__ == '__main__':
    with open(Path('OTL_Navigatie_202239.json')) as file:
        nav_json = json.load(file)

    uri_list = [v for k, v in flatdict.FlatterDict(nav_json, delimiter='.').items() if "uri" in k]

    with sqlite3.connect(Path('OTL_Export_MetProductieUris.db')) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT uri FROM OSLOClass WHERE abstract = 0')
        rows = cursor.fetchall()
        missing_uris = [row[0] for row in rows if row[0] not in uri_list]

    print(missing_uris)
