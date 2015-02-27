#!/usr/bin/env python
# -*- coding: utf8 -*-
# Soubor:  create_dev_users.py
# Datum:   22.02.2015 18:41
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL
# Úloha:   Vytvoří několik málo testovacích uřivatelů
############################################################################
from __future__ import division, print_function, unicode_literals


from crypt import crypt
from wtdb import Student, Ucitel
from pony.orm import (sql_debug, db_session)
############################################################################

sql_debug(True)
with db_session:
    Student(login="karel",
            jmeno="Karel Učenlivý",
            hash=crypt('karel', '$1$qda8YAO9'))

    Student(login="jan",
            jmeno="Jan Helemese",
            hash=crypt('jan',   '$1$8DAwyao9'))

    Ucitel(login="bob",
           jmeno="Bob Zadavatel",
           hash=crypt('bob',    '$1$3da8Yoo9'))

    Ucitel(login="emil",
           jmeno="Emil Přísný",
           hash=crypt('emil',   '$1$q118YAOg'))
