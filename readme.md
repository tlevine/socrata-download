Download Socrata Portals
======
I download the contents of Socrata portals to a filesystem and then upload them
to S3.

## How to run (multiple portals)

Set the parameters.

    SOCRATA_URLS=( data.cityofnewyork.us 
    SOCRATA_S3_BUCKET=socrata.appgen.me

Then run the main script.

    ./run.sh

The result will be the following file structure, both locally and in the bucket.

    data.cityofnewyork.us/
      searches/
        1
        2
        ...
      views/
        abcd-efgh
        ijkl-mnop
        ...
      rows/
        abcd-efgh
        ijkl-mnop
    data.sfgov.org/
      searches/
        1
        2
        ...
      views/
        abcd-efgh
        ijkl-mnop
        ...
      rows/
        abcd-efgh
        ijkl-mnop
        ...

The different portals will be accessed in parallel, so this should only take as
long as the largest/slowest portal.

## How to run (one portal)

Set the parameters.

    SOCRATA_URL=data.cityofnewyork.us
    SOCRATA_S3_BUCKET=socrata.appgen.me

Then run the main script.

    ./run_one.sh

The result will be the following file structure, both locally and in the bucket.

    data.cityofnewyork.us/
      searches/
        1
        2
        ...
      views/
        abcd-efgh
        ijkl-mnop
        ...
      rows/
        abcd-efgh
        ijkl-mnop

## Components of the run script.
When you run `./run_all.sh`, the following things happen in order.

1. `./search.sh` searches/browses through all of the datasets/maps/views/&c.
    and saves all of the files as `$SOCRATA_URL/searches/$page_number`.
2. `./viewids.py` returns all of the 4x4 Socrata view id codes from the
    files in `$SOCRATA_URL/searches`.
3. `./views.sh` downloads the metadata files for each of the viewids and
    and saves all of the files as `$SOCRATA_URL/views/$viewid`.
4. `./rows.sh` downloads the data files for each of the viewids as CSV
    and saves all of the files as `$SOCRATA_URL/rows/$viewid`.
5. `./builddb.py` makes a SQLite3 database with one row per dataset, using
    features from the view and row files. It contains one table, called
    `datasets`. One of the columns is named `socrata.url`, so unioning it
    with databases from other portals will be easy. It is named
    `$SOCRATA_URL/features.db`.
6. `./upload.sh` uploads all of the downloaded files to an S3 bucket.