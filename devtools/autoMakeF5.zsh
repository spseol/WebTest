#!/bin/zsh
# File:    autoMake.zsh 
# Date:    13.10.2014 22:01
# Author:  Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL 
# Task:    Automatic lunch sass procesing when file change.
############################################################
setopt extendedglob # **/*.txt
setopt re_match_pcre 

if [[ $1 == '-h' ]]; then
    cat <<EOF 
    
    $(basename $0) [XID]

        Skript sleduje pracovní adresář a pokud v něm dojde ke změně 
        nějakého souboru, sputí kompilaci SCSS a pošle do okna 
        prohlížeče stisk F5.

        Pokud není zadáno XID je nuté po spuštění kliknou na okno 
        prohlížeče aby skript věděl, do kterého okna se má 
        stisk F5 posílat.

EOF
    exit 0
fi

# načtu XID okna jako parametr z příkazové řádky
if [ $1 ] && [ $1 != 'x' ]; then 
    if [[ $1 =~ '^[\da-fA-F]+$' ]]; then
        winID="0x$1"
    elif [[ $1 =~ '^0x[\da-fA-F]+$' ]]; then
        winID="$1"
    else 
        echo "Toto nevypadá jako window XID" >/dev/stderr
        exit 1
    fi
else
    winID=$(xwininfo | egrep -i 'window id' | awk '{print $4}')
    echo $winID
fi


radek=0
while true; do
    radek=$[ $radek + 1 ]
    inotifywait -r -e modify . --exclude '^\..+\.swp$'
    scss --compass styles.scss static/styles.css
    sleep 1s
    if [ $winID ]; then
        xdotool key --window $winID F5  
    fi
    printf "%03d: " ${radek}; 
    date
    
done

