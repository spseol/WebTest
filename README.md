
WebTest
=========

WebTest je webové rozhraní pro testy a domácí úkoly žáků. Tento projekt se
zaměřuje hlavně na (elektro-)technické úlohy. Tento projekt nabízí:

* Zápis úloh pomocí jazyka [Markdown](https://cs.wikipedia.org/wiki/Markdown).
* Vkládání matematických vzorců 
  ala [LaTeX](https://cs.wikipedia.org/wiki/LaTeX)
  mocí knihovny [MathJax](https://cs.wikipedia.org/wiki/MathJax).
* Možnost vložit do zadání náhodné číslo a očekávaný výsledek
  zapsat jako vzorec. 


Příklad zápisu úlohy
--------------------

    ::task Dělič I.
    Vypočítejte výstupní napětí nezatíženého děliče 
    $R_1=4,2k\Omega$, $R_2=4,2k\Omega$, kde vstupní napětí $U_1=12V$.
    ::close
    :- 12V
    :- -12V
    :+ 6V
    :- 0V

    ::task Dělič II.
    Vypočítejte výstupní napětí nezatíženého děliče $R_1=4,2k\Omega$, 
    $R_2=4,2k\Omega$, kde vstupní napětí $U_1=12V$.
    ::number 6,000 0,010

    ::task Dělič III.
    Vypočítejte výstupní napětí nezatíženého děliče $R_1=4,2k\Omega$,
    $R_2=4,2k\Omega$, kde vstupní napětí $U_1=12V$.
    ::open


Závislosti
-----------

* [Flask](http://flask.pocoo.org/) --- Python web framework.
* [Python-Markdown](http://pythonhosted.org/Markdown/) --- Python implementace pro
  [Markdown](http://daringfireball.net/projects/markdown/) Johnyho Grubera.
* [psycopg](http://initd.org/psycopg/) --- 
  [PostgreSQL](http://www.postgresql.org/) adaptér
  pro [Python](https://www.python.org/).
* [Pony](http://ponyorm.com/) ---
  [ORM](http://cs.wikipedia.org/wiki/Objektově_relační_mapování) 
  pro [Python](https://www.python.org/).
* [Typogrify](https://github.com/mintchaos/typogrify) --- typografická
  vylepšení pro HTML.


Databáze
--------

* [ERD]() databáze: <https://editor.ponyorm.com/user/tlapicka/WebTest>.
* Definice databázových tabulek je v modulu `wtdb.py`.

Vzhled a CSS
------------

Pro tvorbu vzhledu je použit:
* [SASS](http://sass-lang.com/guide)
* [Semantic](http://semantic.gs/)
* [Compass](http://compass-style.org/)

Pomocný Skript `devtools/autoMakeF5.zsh` sleduje pomocí `inotify` adresář a pokud
se nějaký soubor změní, provede se kompilace `scss` a pomocí `xdotool`
se do prohlížeče odešle stisk F5.

devtools
-----------

V adresáři `devtools/` je několik pomocných skriptů, které mají usnadnit vývoj
a práci s lokální databází.

* `autoMakeF5.zsh`: při změně souborů automaticky odesílá 
   do prohlížeče stisk F5.
* `create-psql.usr.db`: vytvoří v PostgreSQL uživatele a založí mu 
   databázi.
* `drop-psql.usr.db`: zruší v PostgreSQL uživatele a všechny jeho 
   databáze.
* `db-insert_dev_data.py`: vloží do vývojové databáze počáteční data.
* `db-drop_create_insert.zsh`: vývojovou databázi zruší, znovu vytvoří
   a vloží do ní počáteční data.
* `devserver.zsh`: spustí vývojový server.


