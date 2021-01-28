#!/usr/bin/env python3


import requests


if __name__ == "__main__":

    r = requests.get("https://product-details.mozilla.org/1.0/mobile_android.json")
    r.raise_for_status()

    products = r.json()

    print("Use the following for https://sql.telemetry.mozilla.org/queries/75521/source")
    for key, release in products['releases'].items():
        if key.startswith("fenix-"):
            print(f"STRUCT('{release['version']}' AS version, DATE '{release['date']}' AS release_date),")
