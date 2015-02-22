# -*- coding: utf8 -*-
# Soubor:  webtest.py
# Datum:   22.02.2015 16:35
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL
# Úloha:   Hlavní soubor aplikace WebTest
from __future__ import division, print_function, unicode_literals
############################################################################

from flask import (Flask, render_template, Markup, request,
                   url_for, redirect, session, )
from werkzeug.routing import BaseConverter
from typogrify.filters import typogrify
from pony.orm import (sql_debug, get, select, db_session)
from markdown import markdown
from datetime import datetime
import os
import functools
from crypt import crypt
from wtdb import Student, Ucitel
from pony.orm import db_session

import sys
reload(sys)  # to enable `setdefaultencoding` again
sys.setdefaultencoding("UTF-8")
app = Flask(__name__)
app.secret_key = os.urandom(24)


############################################################################
class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login', url=request.path))
    return wrapper


def pswd_check(pswd, encript):
    """Kontroluje heslo a hash hesla v DB.

    pswd: heslo od uživatele
    encript: šífrované heslo uložené v DB
    """
    i = encript.rfind('$')
    salt = encript[:i]
    return encript == crypt(pswd, salt)


############################################################################


@app.route('/')
def index():
    if 'student' in session:
        return render_template('student.html')
    elif 'ucitel' in session:
        return render_template('ucitel.html')
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
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
############################################################################


if __name__ == '__main__':
    sql_debug(True)
    app.run(host='127.0.0.1', port=8080, debug=True)
