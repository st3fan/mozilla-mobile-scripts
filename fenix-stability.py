#!/usr/bin/env python3


import os
import requests


if __name__ == "__main__":

    # Collect available releases

    r = requests.get("https://product-details.mozilla.org/1.0/mobile_android.json")
    r.raise_for_status()
    products = r.json()

    versions = ""
    for key, release in products['releases'].items():
        if key.startswith("fenix-"):
            if len(versions) != 0:
                versions += ","
            versions += f"STRUCT('{release['version']}' AS version, DATE '{release['date']}' AS release_date)"

    # Update the query

    if (api_key := os.getenv("REDASH_API_KEY")) is None:
        println("This script needs REDASH_API_KEY to be set")
        os.exit(1)

    if (query_id := os.getenv("REDASH_QUERY_ID")) is None:
        println("This script needs REDASH_QUERY_ID to be set")
        os.exit(1)

    query = open("fenix-stability.sql").read()
    query = query.replace('__VERSIONS__', versions)

    r = requests.post(f"https://sql.telemetry.mozilla.org/api/queries/{query_id}",
                      headers={"Authorization": f"Key {api_key}"},
                      json={"query": query})
    r.raise_for_status()

