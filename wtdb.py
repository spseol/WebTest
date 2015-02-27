# -*- coding: utf8 -*-
# Soubor:  wtdb.py
# Datum:   22.02.2015 18:42
# Autor:   Marek Nožka, nozka <@t> spseol <d.t> cz
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL
# Úloha:   Knihovna s definicí databáze:
#          https://editor.ponyorm.com/user/tlapicka/WebTest
############################################################################
from datetime import datetime
from pony.orm import (Database, PrimaryKey, Required, Optional, Set,
                      sql_debug)
import wtconf

db = Database("postgres", **wtconf.DB)


class Student(db.Entity):
    """Každý jeden student, který se může účastnit testů."""
    _table_ = "student"
    id = PrimaryKey(int, column="id_student", auto=True)
    login = Required(str, 20)
    jmeno = Required(unicode, 40)
    hash = Required(str, 196)
    akcee = Set("Akce")
    vysledky_testu = Set("Vysledek_testu")


class Akce(db.Entity):
    """evidence toho, co student v aplikací dělá:
    * logIn
    * logOut"""
    _table_ = "akce"
    id = PrimaryKey(int, column="id_akce", auto=True)
    cas = Required(datetime)
    student = Required(Student)
    typ_akce = Required(str, 10)


class Vysledek_testu(db.Entity):
    _table_ = "vysledek_testu"
    id = PrimaryKey(int, column="id_vysledek_testu", auto=True)
    student = Required(Student)
    test = Required("Test")
    cas_zahajeni = Required(datetime)
    cas_ukonceni = Optional(datetime)
    odpovedi = Set("Odpoved")


class Test(db.Entity):
    """Jeden konkrétní test. """
    _table_ = "test"
    id = PrimaryKey(int, column="id_test", auto=True)
    jmeno = Required(unicode, 80)
    ucitel = Required("Ucitel")
    otazky_testu = Set("Otazka_testu")
    vysledky_testu = Set(Vysledek_testu)
    zobrazeno_od = Optional(datetime)
    zobrazeno_do = Optional(datetime)


class Otazka(db.Entity):
    """Obecná otázka:
    * V obecne_zadani se dá specifikovat rozsah náhodného čísla.
    * typ_otazky: Otevřená, Uzavřená, Hodnota, Vzorec"""
    _table_ = "otazka"
    id = PrimaryKey(int, column="id_otazka", auto=True)
    ucitel = Required("Ucitel")
    jmeno = Required(unicode, 80)
    typ_otazky = Required(str, 1, sql_type="char")
    obecne_zadani = Required(unicode)
    spravna_odpoved = Optional(unicode, 512)
    spatna_odpoved1 = Optional(unicode, 512)
    spatna_odpoved2 = Optional(unicode, 512)
    spatna_odpoved3 = Optional(unicode, 512)
    spatna_odpoved4 = Optional(unicode, 512)
    spatna_odpoved5 = Optional(unicode, 512)
    spatna_odpoved6 = Optional(unicode, 512)
    otazky_testuu = Set("Otazka_testu")


class Odpoved(db.Entity):
    """Vazební tabulka mezi výsledkem testu a otázkami testu.

    Obsahuje znovu (redundantně) zadání a odpověď. Je to proto, že otázku
    může učitel editovat a není možné hodnotit odpověď na změněnou otázku.
    Dále se řeší problém, kdy je v otázce náhodné číslo: je nutno uchovat
    konkretní zadání i očekávaný výsledek """
    _table_ = "odpoved"
    id = PrimaryKey(int, column="id_odpoved", auto=True)
    konkretni_zadani = Required(unicode)
    ocekavana_odpoved = Required(unicode, 512)
    konkretni_odpoved = Required(unicode, 512)
    vysledek_testu = Required(Vysledek_testu)
    otazka_testu = Required("Otazka_testu")


class Otazka_testu(db.Entity):
    """Vazební tabulka: každý test, lze vytvořit kombinací libovolných otázek.
    """
    _table_ = "otazka_testu"
    id = PrimaryKey(int, column="id_otazka_testu", auto=True)
    poradi = Required(int)
    test = Required(Test)
    otazka = Required(Otazka)
    odpovedi = Set(Odpoved)


class Ucitel(db.Entity):
    """Každý jeden učitel, který tvoří testy."""
    id = PrimaryKey(int, column="id_ucitel", auto=True)
    login = Required(str, 20)
    jmeno = Required(unicode, 40)
    hash = Required(str, 196)
    testy = Set(Test)
    otazky = Set(Otazka)


sql_debug(True)
db.generate_mapping(create_tables=True)
