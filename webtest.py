#!/usr/bin/env python
# -*- coding: utf8 -*-
# Soubor:  webtest.py
# Datum:   22.02.2015 16:35
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL
# Úloha:   Hlavní soubor aplikace WebTest
from __future__ import division, print_function, unicode_literals
############################################################################

from flask import (Flask, render_template, Markup,
                   request, url_for, redirect, session)
from werkzeug.routing import BaseConverter
from typogrify.filters import typogrify
from markdown import markdown
from pony.orm import (sql_debug, get, select, db_session)
import datetime
import time
import os
import functools
from crypt import crypt
from wtdb import(Student, Ucitel, Otazka, Test,
                 Otazka_testu, Odpoved, Vysledek_testu)
import random
import sys
reload(sys)  # to enable `setdefaultencoding` again
sys.setdefaultencoding("UTF-8")
app = Flask('WebTest')
app.secret_key = os.urandom(24)

############################################################################


class RegexConverter(BaseConverter):
    "Díky této funci je možné do routovat pomocí regulárních výrazů"
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter


def prihlasit(klic):
    """Dekoruje funkce, které vyžadují přihlášení

    @prihlasit(klic)
    klic: je klic ve slovniku session, který se kontroluje.
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if klic in session:
                return function(*args, **kwargs)
            else:
                return redirect(url_for('login', url=request.path))
        return wrapper
    return decorator


def pswd_check(pswd, encript):
    """Kontroluje heslo a hash hesla v DB.

    pswd: heslo od uživatele
    encript: šífrované heslo uložené v DB
    """
    i = encript.rfind('$')
    salt = encript[:i]
    return encript == crypt(pswd, salt)


def rendruj(m):
    return Markup(typogrify(markdown(m)))
############################################################################


@app.route('/')
def index():
    if 'student' in session:
        return redirect(url_for('student_testy'))
    elif 'ucitel' in session:
        return render_template('ucitel.html')
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        with db_session:
            if 'student' in session:
                student = get(s for s in Student
                              if s.login == session[b'student'])
                return render_template('login.html', jmeno=student.jmeno)
            elif 'ucitel' in session:
                ucitel = get(u for u in Ucitel
                             if u.login == session[b'ucitel'])
                return render_template('login.html', jmeno=ucitel.jmeno)
        if 'url' in request.args:
            return render_template('login.html', url=request.args['url'])
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        login = request.form['login']
        heslo = request.form['passwd']
        with db_session:
            student_hash = get(s.hash for s in Student if s.login == login)
            ucitel_hash = get(u.hash for u in Ucitel if u.login == login)
        if student_hash and pswd_check(heslo, student_hash):
            session['student'] = login
            if 'url' in request.form:
                return redirect(request.form['url'])
            else:
                return redirect(url_for('index'))
        elif ucitel_hash and pswd_check(heslo, ucitel_hash):
            session['ucitel'] = login
            if 'url' in request.form:
                return redirect(request.form['url'])
            else:
                return redirect(url_for('index'))
        else:  # špatně
            if 'url' in request.form:
                return render_template('login.html', spatne=True,
                                       url=request.form['url'])
            else:
                return render_template('login.html', spatne=True)


@app.route('/logout/', methods=['GET'])
def logout():
    if 'student' in session:
        session.pop('student', None)
    elif 'ucitel' in session:
        session.pop('ucitel', None)
    return redirect(url_for('login'))


@app.route('/vysledky/', methods=['GET', 'POST'])
@prihlasit('ucitel')
def vysledky():
    if request.method == 'GET':
        return render_template('vysledky.html')
    elif request.method == 'POST':
        return redirect(url_for('/'))


@app.route('/otazky/', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def otazky():
    #: Zobrazí všechny otázky a nabídne příslušné akce
    if request.method == 'GET':
        otazky = select((o.id, o.ucitel.login, o.ucitel.jmeno, o.jmeno,
                        o.obecne_zadani) for o in Otazka)
        return render_template('otazky.html',
                               otazky=otazky.order_by(1))
    elif request.method == 'POST':
        return redirect(url_for('/'))


@app.route('/otazky/ucitel/<login>', methods=['GET'])
@prihlasit('ucitel')
@db_session
def otazky_ucitel(login):
    #: Zobrazí všechny otázky jednoho zadávajícího učitele
    otazky = select((o.id, o.ucitel.login, o.ucitel.jmeno, o.jmeno,
                    o.obecne_zadani)for o in Otazka
                    if o.ucitel.login == login)
    return render_template('otazky.html', otazky=otazky)


@app.route('/otazky/zobrazit/<id>', methods=['GET'])
@prihlasit('ucitel')
@db_session
def otazka_zobrazit(id):
    otazka = Otazka[id]
    return render_template('otazka.html', otazka=otazka, rendruj=rendruj)


@app.route('/otazky/editovat/<id>', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def otazka_editovat(id):
    if request.method == 'GET':
        otazka = Otazka[id]
        return render_template('otazka_editovat.html',
                               otazka=otazka, rendruj=rendruj)
    if request.method == 'POST':
        r = request
        r.f = r.form
        if r.f['jmeno'] and r.f['typ_otazky'] and r.f['obecne_zadani']:
            if r.f['typ_otazky'] == 'O':
                otazka = Otazka[id]
                otazka.ucitel = get(u for u in Ucitel
                                    if u.login == session['ucitel'])
                otazka.jmeno = r.f['jmeno']
                otazka.typ_otazky = 'O'
                otazka.obecne_zadani = r.f['obecne_zadani']
                return redirect(url_for('otazky'))
            elif r.f['typ_otazky'] == 'C' and r.f['spravna_odpoved']:
                otazka = Otazka[id]
                otazka.ucitel = get(u for u in Ucitel
                                    if u.login == session['ucitel'])
                otazka.jmeno = r.f['jmeno']
                otazka.typ_otazky = 'C'
                otazka.obecne_zadani = r.f['obecne_zadani']
                otazka.spravna_odpoved = r.f['spravna_odpoved']
                return redirect(url_for('otazky'))
            # TODO!
        else:
            zprava = "Nebyla zadána všechna požadovaná data."
            otazka = Otazka[id]
            return render_template('otazka_editovat.html',
                                   chyba=zprava, otazka=otazka)


@app.route('/otazky/smazat/<id>', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def otazka_smazat(id):
    #: Zobrazí všechny otázky a nabídne příslušné akce
    if request.method == 'GET':
        otazka = Otazka[id]
        return render_template('otazka_smazat.html',
                               otazka=otazka, rendruj=rendruj)
    elif request.method == 'POST':
        if 'ano' in request.form and request.form['ano'] == 'Ano':
            Otazka[id].delete()
        return redirect(url_for('otazky'))


@app.route('/testy/', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def testy():
    """seznam testu
    """
    if request.method == 'GET':
        testy = select((u.id, u.jmeno) for u in Test)
        return render_template('testy.html', testy=testy)
    elif request.method == 'POST':
        return redirect(url_for('/'))


@app.route('/testy/<id_test>', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def uprav_test(id_test):
    """uprava vytvoreneho testu
    """
    if request.method == 'POST':
        if 'upravit' in request.form:
            nazev_testu = request.form['nazev_testu']
            platne_od = request.form['datum1'] + " " + request.form['cas_od']
            platne_do = request.form['datum2'] + " " + request.form['cas_do']
            datum_od = datetime.datetime.strptime(platne_od,
                                                  "%d.%m.%Y %H:%M")
            datum_do = datetime.datetime.strptime(platne_do,
                                                  "%d.%m.%Y %H:%M")
            checked = request.form.getlist('check')
            # smaz puvodni zaznam test-otazky
            get(u for u in Test if u.id is id_test).delete()
            # vytvor nove zaznamy
            Test(jmeno=nazev_testu,
                 ucitel=get(u for u in Ucitel if u.login == session['ucitel']),
                 zobrazeno_od=datum_od, zobrazeno_do=datum_do)
            for otazka in checked:
                Otazka_testu(poradi=0, test=get(u for u in Test
                                                if u.jmeno == nazev_testu),
                             otazka=get(o for o in Otazka
                                        if o.jmeno == otazka))
            zprava = 'Test "' + nazev_testu + '" byl úspěšně upraven'
            testy = select((u.id, u.jmeno) for u in Test)
            return render_template('testy.html', zprava=zprava, testy=testy)
        if 'smazat' in request.form:
            get(u for u in Test if u.id is id_test).delete()
            zprava = 'smazan test "' + request.form['nazev_testu'] + '"'
            testy = select((u.id, u.jmeno) for u in Test)
            return render_template('testy.html', zprava=zprava, testy=testy)
    elif request.method == 'GET':
        test = select((u.id, u.jmeno) for u in Test
                      if u.id is id_test)
        datum = select((u.zobrazeno_od, u.zobrazeno_do)
                       for u in Test if u.id is id_test).get()
        datum_od, cas_od = (datum[0]).strftime("%d.%m.%Y %H:%M").split()
        datum_do, cas_do = (datum[1]).strftime("%d.%m.%Y %H:%M").split()
        # vyber ucitelem zvolene testy
        testy = select((u.otazka.id, u.otazka.ucitel.login,
                        u.otazka.ucitel.jmeno, u.otazka.jmeno,
                        u.otazka.obecne_zadani)for u in Otazka_testu if
                       u.test.id is id_test)
        # vyber vsechny testy
        otazky_all = select((u.id, u.ucitel.login, u.ucitel.jmeno, u.jmeno,
                            u.obecne_zadani) for u in Otazka if u.id
                            not in select(ot.otazka.id for ot in Otazka_testu
                                          if ot.test.id is id_test))
        return render_template('upravit_test.html', test=test,
                               otazky=testy, cas_od=cas_od, cas_do=cas_do,
                               datum_od=datum_od, datum_do=datum_do,
                               otazku=otazky_all)


@app.route('/pridat/otazku/', methods=['GET', 'POST'])
@prihlasit('ucitel')
def pridat_otazku():
    r = request
    r.f = r.form
    if r.method == 'GET':
        if 'ok' in r.args:
            zprava = 'Proběhlo vložení otázky "' + r.args['ok'] + '".'
            return render_template('pridat_otazku.html', vlozeno=zprava)
        else:
            return render_template('pridat_otazku.html')
    elif r.method == 'POST':
        if r.f['jmeno'] and r.f['typ_otazky'] and r.f['obecne_zadani']:
            if r.f['typ_otazky'] == 'O':
                with db_session:
                    Otazka(ucitel=get(u for u in Ucitel
                                      if u.login == session['ucitel']),
                           jmeno=r.f['jmeno'],
                           typ_otazky='O',
                           obecne_zadani=r.f['obecne_zadani'])
                return redirect(url_for('pridat_otazku', ok=r.f['jmeno']))
            elif r.f['typ_otazky'] == 'C' and r.f['spravna_odpoved']:
                with db_session:
                    Otazka(ucitel=get(u for u in Ucitel
                                      if u.login == session['ucitel']),
                           jmeno=r.f['jmeno'],
                           typ_otazky='C',
                           obecne_zadani=r.f['obecne_zadani'],
                           spravna_odpoved=r.f['spravna_odpoved'])
                return redirect(url_for('pridat_otazku', ok=r.f['jmeno']))
            elif r.f['typ_otazky'] == 'U' and r.f['spravna_odpoved']:
                # Musím dát všechny špatné odpovědi těsně za sebe
                KLICE = ('spatna_odpoved1', 'spatna_odpoved2',
                         'spatna_odpoved3', 'spatna_odpoved4',
                         'spatna_odpoved5', 'spatna_odpoved6')
                odpovedi = []
                for klic in KLICE:
                    if r.f[klic]:
                        odpovedi.append(r.f[klic])
                parametry = {}
                i = 0
                for odpoved in odpovedi:
                    parametry[KLICE[i]] = odpoved
                    i += 1
                # Chce to alespoň jednu špatnou odpověď
                if len(parametry) < 1:
                    zprava = "... alespoň jednu špatnou odpověď!"
                    return render_template('pridat_otazku.html', chyba=zprava)
                with db_session:
                    Otazka(ucitel=get(u for u in Ucitel
                                      if u.login == session['ucitel']),
                           jmeno=r.f['jmeno'],
                           typ_otazky='U',
                           obecne_zadani=r.f['obecne_zadani'],
                           spravna_odpoved=r.f['spravna_odpoved'],
                           **parametry)
                return redirect(url_for('pridat_otazku', ok=r.f['jmeno']))
            else:
                zprava = "U číselné otázky musí být zadán správná odpověď."\
                         " U uzavrené otázky i špatná odpověď."
                return render_template('pridat_otazku.html', chyba=zprava)
        else:
            zprava = "Nebyla zadána všechna požadovaná data."
            return render_template('pridat_otazku.html', chyba=zprava)


@app.route('/pridat/test/', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def pridat_test():
    """pridat test z již vložených otázek a určit dobu platnosti testu
    """
    if request.method == 'GET':
        otazky = select((o.id, o.ucitel, o.ucitel.jmeno, o.jmeno,
                         o.obecne_zadani) for o in Otazka)
        return render_template('pridat_test.html',
                               otazky=otazky.order_by(1))
    elif request.method == 'POST':
        nazev_testu = request.form['nazev_testu']
        platne_od = request.form['datum1'] + " " + request.form['cas_od']
        platne_do = request.form['datum2'] + " " + request.form['cas_do']
        datum_od = datetime.datetime.strptime(platne_od,
                                              "%d.%m.%Y %H:%M")
        datum_do = datetime.datetime.strptime(platne_do,
                                              "%d.%m.%Y %H:%M")
        checked = request.form.getlist('check')
        Test(jmeno=nazev_testu, ucitel=get(u for u in Ucitel
                                           if u.login == session['ucitel']),
             zobrazeno_od=datum_od, zobrazeno_do=datum_do)
        for otazka in checked:
            Otazka_testu(poradi=0, test=get(u for u in Test
                                            if u.jmeno == nazev_testu),
                         otazka=get(o for o in Otazka
                                    if o.jmeno == otazka))
        zprava = 'Vytvořen test "' + nazev_testu + '"'
        otazky = select((o.id, o.ucitel, o.ucitel.jmeno, o.jmeno,
                         o.obecne_zadani) for o in Otazka)
        return render_template('pridat_test.html', zprava=zprava,
                               otazky=otazky.order_by(1))


@app.route('/upload/', methods=['GET', 'POST'])
@prihlasit('ucitel')
@db_session
def upload():
    """upload souboru se zadáním
    """
    def add(typ, nazev_otazky, cislo, otazka, spravna, spatna):
        """zapis do databaze
        """
        ucitel = get(u for u in Ucitel if u.login == session['ucitel'])
        while len(spatna) < 7:  # doplni hodnoty NULL do nevyuzitych mist
            spatna.append('Null')

        # prevede polozky seznamu na UNICODE
        spatna = [unicode(i) for i in spatna]
        Otazka(ucitel=ucitel, jmeno=nazev_otazky, typ_otazky=typ,
               obecne_zadani='10', spravna_odpoved=spravna,
               spatna_odpoved1=spatna[0],
               spatna_odpoved2=spatna[1],
               spatna_odpoved3=spatna[2],
               spatna_odpoved4=spatna[3],
               spatna_odpoved5=spatna[4],
               spatna_odpoved6=spatna[5])
        # Obecne_zadani nastaveno perma na 10

    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        if 'datafile' in request.files:
            fil = request.files['datafile']
            typ = cislo = nazev_otazky = otazka = spravna = ""
            spatna = []  # seznam spatnych odpovedi
            for line in fil:
                radek = line.strip().decode('UTF-8')
                if line != '\n':  # ignoruj prazdne radky
                    if radek.split()[0] == '::date':
                        #  datum = " ".join(radek.split()[1:])
                        pass
                    elif radek.split()[0] == '::number':
                        typ = 'C'
                        spravna = " ".join(radek.split()[1:])
                    elif radek.split()[0] == ':+':
                        spravna = " ".join(radek.split()[1:])
                    elif radek.split()[0] == ':-':
                        spatna.append(radek.split()[1:])
                    elif radek.split()[0] == '::task':
                        nazev_otazky = " ".join(radek.split()[1:])
                    elif radek.split()[0] == '::open':
                        typ = 'O'
                    elif radek.split()[0] == '::close':
                        typ = 'U'
                    else:
                        otazka = otazka + line
                else:  # kdyz je mezera(oddeleni otazek), udelej zapis do DB
                    # ignoruj 1.mezeru či  nekor. otazky
                    if nazev_otazky and otazka:
                        add(typ, nazev_otazky, cislo, otazka, spravna, spatna)
                    # vynuluj
                    typ = nazev_otazky = cislo = otazka = spravna = ""
                    spatna = []
        return redirect(url_for('upload'))


@app.route('/student/testy/', methods=['GET', 'POST'])
@prihlasit('student')
@db_session
def student_testy():
    if request.method == 'GET':
        pritomnost = datetime.datetime.strptime(
            time.strftime("%d.%m.%Y %H:%M"), "%d.%m.%Y %H:%M")
        testy = select((u.id, u.jmeno, u.zobrazeno_od, u.zobrazeno_do)
                       for u in Test if (pritomnost >= u.zobrazeno_od and
                                         pritomnost <= u.zobrazeno_do))
        return render_template('student.html', testy=testy)


@app.route('/student/testy/<id>', methods=['GET', 'POST'])
@prihlasit('student')
@db_session
def student_zobrazit(id):
    if request.method == 'GET':
        global zacatek_testu
        zacatek_testu = (datetime.datetime.now()).strftime("%d.%m.%Y %H:%M:%S")
        shluk_otazek = []
        otazky_testu = select((u.otazka.id,
                               u.otazka.typ_otazky,
                               u.otazka.obecne_zadani,
                               u.otazka.spravna_odpoved,
                               u.otazka.spatna_odpoved1,
                               u.otazka.spatna_odpoved2,
                               u.otazka.spatna_odpoved3,
                               u.otazka.spatna_odpoved4,
                               u.otazka.spatna_odpoved5,
                               u.otazka.spatna_odpoved6) for u
                              in Otazka_testu if u.test.id is
                              id)
        for ramec in otazky_testu:
            vysledek = []
            for clen in ramec[4:]:
                vysledek.append(clen)
            random.shuffle(vysledek)
            vysledek.insert(0, ramec[0])
            vysledek.insert(1, ramec[1])
            vysledek.insert(2, ramec[2])
            vysledek.insert(3, ramec[3])
            shluk_otazek.append(vysledek)
        random.shuffle(shluk_otazek)

        Vysledek_testu(student=get(s.id for s in Student
                                   if s.login == session[b'student']),
                       test=get(u.id for u in Test if u.id is id),
                       cas_zahajeni=zacatek_testu)
        return render_template('student_testy.html',
                               otazka_testu=shluk_otazek)
    elif request.method == 'POST':
        checked = request.form
        Vysledek_testu(student=get(s.id for s in Student
                                   if s.login == session[b'student']),
                       test=get(u.id for u in Test if u.id is id),
                       cas_zahajeni=zacatek_testu,
                       cas_ukonceni=datetime.datetime.now().strftime(
                           "%d.%m.%Y %H:%M:%S"))

        for ch in checked:
            zadani = select((u.obecne_zadani, u.spravna_odpoved)
                            for u in Otazka if u.id is ch).get()
            konk_odpoved = request.form.get("%s" % ch)
            if not konk_odpoved:
                konk_odpoved = "Nevyplneno"
            idcko = get(u.id for u in Otazka_testu if
                        u.otazka.id is ch and u.test.id is id)
            if not idcko:
                idcko = "Nevyplneno"
            id_vysledek = select(u.id for u in Vysledek_testu
                                 if u.student.login == session['student'] and
                                 u.test.id is id)[:]
            Odpoved(konkretni_zadani=zadani[0],
                    ocekavana_odpoved=zadani[1],
                    konkretni_odpoved=konk_odpoved,
                    vysledek_testu=id_vysledek[0],
                    otazka_testu=idcko)
        return redirect(url_for('student_testy'))


@app.route('/student/vysledky/')
@prihlasit('student')
@db_session
def student_vysledek():
    if request.method == 'GET':
        testy_uzivatele = select((u.test.jmeno, u.cas_ukonceni, u.id) for u in
                                 Vysledek_testu
                                 if u.student.login is session[b'student'])
    return render_template('student_vysledky.html',
                           testy_uzivatele=testy_uzivatele)


############################################################################
if __name__ == '__main__':
    sql_debug(True)
    OPT = {'debug': True}
    OPT['port'] = 5000
    if len(sys.argv) == 2:
        # jeden parametr určuje port
        OPT['port'] = int(sys.argv[1])
    elif len(sys.argv) > 2:
        # dva parametry určují adrasu aport, vypne se DebugMode
        OPT['host'] = sys.argv[1]
        OPT['port'] = int(sys.argv[2])
        OPT['debug'] = False
    app.run(**OPT)
