#!/usr/bin/env python3

import csv

csv.field_size_limit(1000000000)
# entity=612000

names = {}
sites = {}


def _name(s):
    return (
        s.lower()
        .replace(" ", "")
        .replace("&", "and")
        .replace("themersey", "mersey")
        .replace("-phase1", "")
    )


for row in csv.DictReader(open("data/ramsar-site.csv")):
    entity = row["entity"]
    sites[entity] = row
    names[_name(row["name"])] = entity


for row in csv.DictReader(
    open(
        "var/converted/78c85817600ce7ddd2666b14cd1d7ccd042a91715d7e05c57a0ae19f41953964.csv"
    )
):
    name = _name(row["NAME"])
    entity = names[name]
    sites[entity]["ramsar"] = row["CODE"]

w = csv.DictWriter(
    open("data/ramsar-site.csv", "w", newline=""),
    fieldnames=[
        "entity",
        "ramsar",
        "ramsar-site",
        "special-protection-area",
        "wikidata",
        "name",
        "wikipedia",
        "documentation-url",
        "start-date",
        "end-date",
        "entry-date",
    ],
    extrasaction="ignore",
)
w.writeheader()
for entity, row in sorted(sites.items()):
    w.writerow(row)

w = csv.DictWriter(
    open("pipeline/lookup.csv", "w", newline=""),
    fieldnames=["prefix", "resource", "organisation", "reference", "entity"],
    extrasaction="ignore",
)
w.writeheader()
for entity, row in sorted(sites.items()):
    row["prefix"] = "ramsar"
    row["reference"] = row["ramsar"]
    w.writerow(row)

    if row["ramsar-site"]:
        row["prefix"] = "ramsar-site"
        row["reference"] = row["ramsar-site"]
        w.writerow(row)

    if row["wikidata"]:
        row["prefix"] = "wikidata"
        row["reference"] = row["wikidata"]
        w.writerow(row)
