#!/bin/zsh
# Soubor:  devserver.zsh
# Autor:   Marek Nožka, marek <@T> tlapicka <dot> net
# Licence: GNU/GPL 
############################################################

cd $(dirname $0)/..

source ./venv/bin/activate
python ./webtest.py
deactivate
