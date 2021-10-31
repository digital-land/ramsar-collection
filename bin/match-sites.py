#!/usr/bin/env python3

import os
import csv
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

debug = True

title_map = {
    "Blackwater Estuary": "Blackwater Estuary (Mid-Essex Coast Phase 4)",
    "Chesil Beach and The Fleet": "Chesil Beach & the Fleet",
    "Chichester Harbour": "Chichester and Langstone Harbours",
    "Chippenham Fen and Snailwell Poor's Fen": "Chippenham Fen",
    "Colne Estuary": "Colne Estuary (Mid-Essex Coast Phase 2)",
    "Crouch and Roach Estuaries": "Crouch & Roach Estuaries (Mid-Essex Coast Phase 3)",
    "Dee Estuary": "The Dee Estuary",
    "Dengie SPA": "Dengie (Mid-Essex Coast Phase 1)",
    "Foulness": "Foulness (Mid-Essex Coast Phase 5)",
    "Holburn Lake and Moss": "Holburn Lake & Moss",
    "Humber": "Humber Estuary",
    "Lea Valley": "Lee Valley",
    "Leighton Moss RSPB reserve": "Leighton Moss",
    "Minsmere-Walberswick Heaths and Marshes": "Minsmere-Walberswick",
    "Norfolk Broads": "Broadland",
    "Norfolk Coast AONB": "North Norfolk Coast",
    "Redgrave and South Lopham Fens": "Redgrave & South Lopham Fens",
    "Ribble and Alt Estuaries": "Ribble & Alt Estuaries",
    "River Alde": "Alde-Ore Estuary",
    "River Avon (Hampshire)": "Avon Valley",
    "River Derwent, Yorkshire": "Lower Derwent Valley",
    "River Medway": "Medway Estuary & Marshes",
    "River Ore": "Alde-Ore Estuary",
    "Somerset Levels and Moors": "Somerset Levels & Moors",
    "Southampton Water": "Solent & Southampton Water",
    "Stodmarsh NNR": "Stodmarsh",
    "Stour Estuary": "Stour and Orwell Estuaries",
    "Thames Estuary": "Thames Estuary & Marshes",
    "Thanet Coast": "Thanet Coast & Sandwich Bay",
    "The New Forest": "New Forest",
    "Thursley and Ockley Bog": "Thursley & Ockley Bogs",
    "Upper Solway Flats and Marshes": "Upper Solway Flats & Marshes",
}


def api(params):
    response = requests.get("https://en.wikipedia.org/w/api.php", params)
    if debug:
        print("get:", response.request.url)
        print("json:", response.json())
    return response.json()


def links(titles=""):
    j = api(
        {
            "action": "query",
            "titles": titles,
            "prop": "links",
            "pllimit": "500",
            "redirects": "max",
            "format": "json",
        }
    )
    for page, p in j["query"]["pages"].items():
        for link in p["links"]:
            yield link


def wikidata(titles=""):
    j = api(
        {
            "action": "query",
            "titles": titles,
            "prop": "pageprops",
            "ppprop": "wikibase_item",
            "redirects": "max",
            "format": "json",
        }
    )
    for page, p in j["query"]["pages"].items():
        if "missing" in p:
            return ""
        return p["pageprops"]["wikibase_item"]


def extlinks(titles=""):
    j = api(
        {
            "action": "query",
            "titles": titles,
            "prop": "extlinks",
            "ellimit": "500",
            "redirects": "max",
            "format": "json",
        }
    )
    for page, p in j["query"]["pages"].items():
        for link in p["extlinks"]:
            yield link["*"]


w = csv.DictWriter(
    open("x.csv", "w"),
    fieldnames=[
        "entity",
        "ramsar-site",
        "natural-england-site",
        "wikidata",
        "name",
        "wikipedia-en",
        "notes",
    ],
    extrasaction="ignore",
)
w.writeheader()

ramsar_site_names = {}
for row in csv.DictReader(open("data/ramsar-site.csv")):
    ramsar_site_names[row["name"]] = row

for link in links("List_of_Ramsar_sites_in_England"):
    title = link["title"]
    name = title_map.get(title, title)

    if debug:
        print(title, name)

    if name not in ramsar_site_names:
        if debug:
            print("skipping")
        continue
    row = ramsar_site_names[name]

    if not row["wikidata"]:
        row["wikidata"] = wikidata(title)

    if not row.get("wikipedia-en", ""):
        row["wikipedia-en"] = title.replace(" ", "_")

    if not row["wikidata"]:
        if debug:
            print("missing")
        continue

    if not row.get("ramsar-site", "") or not row.get("natural-england-site", ""):
        for url in extlinks(title):
            url = url.replace("http:", "https:")
            if url.startswith("https://rsis.ramsar.org/ris/"):
                row["ramsar-site"] = os.path.basename(urlparse(url).path)
            elif url.startswith("https://jncc.gov.uk/jncc-assets/") or url.startswith("https://jncc.defra.gov.uk/pdf/SPA/"):
                row["natural-england-site"] = row.get("natural-england-site", "") or Path(urlparse(url).path).stem

    w.writerow(row)
