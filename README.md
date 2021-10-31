# Ramsar collection

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/ramsar-collection/blob/master/LICENSE)
[![Run pipeline](https://github.com/digital-land/ramsar-collection/actions/workflows/run.yml/badge.svg)](https://github.com/digital-land/ramsar-collection/actions/workflows/run.yml)

A collection of Ramsar sites and shapes collected from Natural England.

The national dataset is in a format consistent with other Digital Land datasets as defined by the
[ramsar](https://digital-land.github.io/specification/schema/ramsar/) and
[ramsar-site](https://digital-land.github.io/specification/schema/ramsar-site/) schemas.

Identifiers in the collection can be used in a number of different places, including:

* https://rsis.ramsar.org/ris/220
* https://jncc.gov.uk/jncc-assets/RIS/UK11056.pdf
* https://sac.jncc.gov.uk/site/UK0012890
* https://designatedsites.naturalengland.org.uk/SiteGeneralDetail.aspx?SiteCode=UK11013&SiteName=&countyCode=&responsiblePerson=&unitId=&SeaArea=&IFCAArea=
* https://magic.defra.gov.uk/MagicMap.aspx?startTopic=Designations&activelayer=sssiIndex&query=HYPERLINK%3D%271001904%27

# Collection

* [collection/source.csv](collection/source.csv) — the list of data sources by organisation, see [specification/source](https://digital-land.github.io/specification/schema/source/)
* [collection/endpoint.csv](collection/endpoint.csv) — the list of endpoint URLs for the collection, see [specification/endpoint](https://digital-land.github.io/specification/schema/endpoint)
* [collection/resource/](collection/resource/) — collected resources
* [collection/log/](collection/log/) — individual log JSON files, created by the collection process
* [collection/log.csv](collection/log.csv) — a collection log assembled from the individual log files, see [specification/log](https://digital-land.github.io/specification/schema/log)
* [collection/resource.csv](collection/resource.csv) — a list of collected resources, see [specification/resource](https://digital-land.github.io/specification/schema/resource)

# Updating the collection

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python [requirements](requirements.txt), [makerules](https://github.com/digital-land/makerules) and other dependencies. Requires Make v4.0 or above.

    $ make makerules
    $ make init
    $ make collect

# Nightly collection

The collection is [updated nightly](https://github.com/digital-land/ramsar-collection/actions) by the [GitHub Action](.github/workflows/run.yml).

# Building the national dataset

The collected files can then be converted into a national dataset:

    $ make

# Licence

The software in this project is open source and covered by the [LICENSE](LICENSE) file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
