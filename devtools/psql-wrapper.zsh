#!/bin/zsh
# Soubor:  psql.zsh
# Datum:   18.11.2014 23:28
# Autor:   Marek Nožka, marek <@T> tlapicka <dot> net
# Licence: GNU/GPL 
############################################################
#######           HELP           ##########
printHelp() {
cat <<EOF

Vytvoří uživatele a založí mu databázy

    create-psql.user.db user password [database]


Odstraní uživatele a všechny jeho databáze

    drop-psql.user.db user 

EOF
}
# pokud existuje parametr -h vytiskne help
for param in $@; do
    if [[ $param == "-h" ]] || [[ $param == "--help" ]]; then
        printHelp
        exit 0;
    fi
done

############################################################
if [ -z $1 ]; then
    printHelp
    exit 1
fi

############################################################
user=$1

if [[ $0 =~ "create" ]]; then
    if [ $2 ]; then
        pass=$2
    else
        printHelp
        echo
        echo "Zadej nejen uživatele, ale také heslo."
        exit 1
    fi
    if [ $3 ]; then
        db=$3
    else
        db=$1
    fi
    psql -a -c "CREATE USER $user WITH ENCRYPTED PASSWORD '$pass';"
    createdb -e -E UTF8 -l cs_CZ.UTF-8 -T template0 -O $user $db
elif [[ $0 =~ "drop" ]]; then
    databases=$(psql -l | awk -F '|' '$3~"'$user'" {print $2 } ' | awk '{print $1}')
    for d in $(echo $databases); do
        dropdb -e $d
    done
    dropuser -e $user
fi


