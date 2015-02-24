#!/bin/zsh
# Soubor:  db-drop_create_insert.zsh
# Datum:   24.02.2015 14:11
# Autor:   Marek Nožka, marek <@T> tlapicka <dot> net
# Licence: GNU/GPL 
# Úloha:   Pomocníček který
#            * zduší vývojovou lokální databázi
#            * vytvoří vývojovou lokální databázi
#            * vloží do ní vstupní data
############################################################

DBNAME=webtest

cd $(dirname $0)

dropdb $DBNAME
createdb -e -E UTF8 -l cs_CZ.UTF-8 -T template0 -O $DBNAME $DBNAME
./db-insert_dev_data.py
