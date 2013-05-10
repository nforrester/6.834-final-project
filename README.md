6.834-final-project
===================

Final project for 6.834 @troyastorino and @nforrester.


## Dependencies

* python3
* mysql-python (from pip)

## Training on Wikipedia

We trained our algorithm using data from Wikipedia. As Wikipedia has quite a bit
of data, all these operations take a long time.  In other words, be very patient.

### Downloading Wikipedia data

Wikipedia data can be
downloaded from the [Wikimedia dumps](http://dumps.wikimedia.org/enwiki/). There
you can see this list of available dumps and choose which you want to download.
For our training data we used `20130403`. The data can be downloaded as `.sql`
dumps from the MySQL database that WikiMedia sites use internally. For the
training we performed, 4 of the tables must be downloaded.  Replace `<datestr>`
with the label for the data to download, e.g., `20130403`.

* The [page table](http://www.mediawiki.org/wiki/Manual:Page_table): `http://dumps.wikimedia.org/enwiki/<datestr>/enwiki-<datestr>-page.sql.gz`
* The [pagelinks table](http://www.mediawiki.org/wiki/Manual:Pagelinks_table): `http://dumps.wikimedia.org/enwiki/<datestr>/enwiki-<datestr>-pagelinks.sql.gz`
* The [category table](http://www.mediawiki.org/wiki/Manual:Category_table): `http://dumps.wikimedia.org/enwiki/<datestr>/enwiki-<datestr>-category.sql.gz`
* The [categorylinks table](http://www.mediawiki.org/wiki/Manual:Category_table): `http://dumps.wikimedia.org/enwiki/<datestr>/enwiki-<datestr>-categorylinks.sql.gz`

Downloading all these files will take some time.

### Loading the data into a MySQL database

The `.sql` dumps must be extracted.  Move all the files into their own folder,
and run:

```
$ gunzip *.sql
```

You also need to create a MySQL database to store the data in. We called ours
`wikipedia`. Assuming you've successfully installed MySQL, do the following:

```
$ mysqld_safe & 
$ mysql -u root 
mysql> create database wikipedia;
mysql> exit
```

Now you can import the data into the MySQL database. The MySQL instance started
with `$ mysqld_safe` should still be running.  (Whenever you do want to stop it,
run `$ mysqladmin -u root shutdown`.) Go to the folder with all the `.sql` files
and run:

```
$ for f in `find . -name '*.sql'`; do mysql -v -u root wikipedia $f; done
```

The verbose option is included in the command because it takes an _incredibly_
long time, and you don't want to feel like nothing is happening for that long.
