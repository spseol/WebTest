#!/bin/zsh
# Soubor:  devserver.zsh
# Autor:   Marek Nožka, marek <@T> tlapicka <dot> net
# Licence: GNU/GPL 
###########################################################

PORT=8888

cd $(dirname $0)/..

source ./venv/bin/activate
{ sleep 2; x-www-browser "http://localhost:$PORT" }&
python ./webtest.py $PORT 
deactivate
