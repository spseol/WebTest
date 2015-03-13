var datum=new Date();       //aktuální datum
  var d=datum.getDate();      //den
  var m=datum.getMonth()+1;   //měsíc
  var r=datum.getFullYear();  //rok
  
  function kalendar1(mesic,rok) {
    var dnes=new Date();      //aktuální datum
    var nazevMesice=new Array("","leden","únor","březen","duben","květen","červen","červenec","srpen","září","říjen","listopad","prosinec");
    var datum=new Date(rok,mesic-1,1);  //1. den v zadaném měsíci - v JavaScriptu se měsíce číslují od 0, proto musíme odečíst 1
    var denTyd=datum.getDay();          //číslo dne v týdnu 0-neděle, 1-pondělí,... 6-sobota
    if(denTyd==0) {denTyd=7;}           //změníme číslo neděle na 7
    //alert(datum.toLocaleString());
    var pocetDniMesice = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);      //počet dní v měsíci
    if (((rok % 4 == 0) && (rok % 100 != 0)) || (rok % 400 == 0)) pocetDniMesice[2] = 29;   //přestupný rok - únor 29 dní
    var tab="<table><thead><tr><th onclick='pred1()'>&lsaquo;&lsaquo;</th><th colspan='5'>"+nazevMesice[mesic]+" "+rok+"</th><th onclick='dal1()'>&rsaquo;&rsaquo;</th></tr></thead><tbody><tr><th>Po</th><th>Út</th><th>St</th><th>Čt</th><th>Pá</th><th>So</th><th>Ne</th></tr><tr>";
    for(i=1; i<denTyd; i++) {
      tab+="<td></td>"; //prázdné buňky před 1. dnem měsíce
    }
    
    for(den=1; den<=pocetDniMesice[mesic]; den++) {
      if(rok==dnes.getFullYear() && mesic==dnes.getMonth()+1 && den==dnes.getDate()) {styl="dnes";}
      //else if(rok==r && mesic==m && den==d) {styl="akt";}
      else {styl="";}
      tab+="<td onclick='vloz1(this)' class='"+styl+"'>"+den+"</td>";
      if(i % 7 == 0 && den!=pocetDniMesice[mesic]) {tab+="</tr><tr>";} 
      i++;
    }
    for(i=i-1; i % 7 !=0; i++) {
      tab+="<td></td>"; //prázdné buňky za posledním dnem měsíce pro dokončení tabulky
    }
    tab+="</tr></tbody></table>";
    return tab;
  }
  
  function dal1() {  //funkce je spuštěna kliknutím na >> v kalendáři
    if(m==12) {r++; m=1;}
    else {m++;}
    zobrazKalendar1(m,r);
  }
  
  function pred1() {  //funkce je spuštěna kliknutím na << v kalendáři
    if(m==1) {r--; m=12;}
    else {m--;}
    zobrazKalendar1(m,r);
  }
  function vloz1(td) {
    document.getElementsByName("datum1")[0].value=td.innerHTML+"."+m+"."+r;
    skryjKalendar1();
  }
  
  function zobrazKalendar1(mesic,rok) {
      document.getElementById("kalendar1").innerHTML=kalendar1(mesic,rok);  //vytvoření kalendáře
      document.getElementById("kalendar1").style.display="block";          //zobrazení kalendáře
  }
  function skryjKalendar1() {
    document.getElementById("kalendar1").innerHTML="";
    document.getElementById("kalendar1").style.display="none";
  }
  
  function zobrazSkryjKalendar1() {   //funkce spuštěna při kliknutí na ikonu kalendáře ve formuláři
      if(document.getElementsByName("datum1")[0].value!="" && document.getElementById("kalendar1").innerHTML=="") {
        var dat=new Array();
        dat=document.getElementsByName("datum1")[0].value.split("."); //rozdělení zapsaného datumu na části
        if(dat.length==3 && dat[1]>=1 && dat[1]<=12 ) {d=dat[0]; m=dat[1]; r=dat[2];}
      }
      if(document.getElementById("kalendar1").style.display!="block") {zobrazKalendar1(m,r);}
      else {skryjKalendar1();}
  }
  function kalendar2(mesic,rok) {
    var dnes=new Date();      //aktuální datum
    var nazevMesice=new Array("","leden","únor","březen","duben","květen","červen","červenec","srpen","září","říjen","listopad","prosinec");
    var datum=new Date(rok,mesic-1,1);  //1. den v zadaném měsíci - v JavaScriptu se měsíce číslují od 0, proto musíme odečíst 1
    var denTyd=datum.getDay();          //číslo dne v týdnu 0-neděle, 1-pondělí,... 6-sobota
    if(denTyd==0) {denTyd=7;}           //změníme číslo neděle na 7
    //alert(datum.toLocaleString());
    var pocetDniMesice = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);      //počet dní v měsíci
    if (((rok % 4 == 0) && (rok % 100 != 0)) || (rok % 400 == 0)) pocetDniMesice[2] = 29;   //přestupný rok - únor 29 dní
    var tab1="<table><thead><tr><th onclick='pred2()'>&lsaquo;&lsaquo;</th><th colspan='5'>"+nazevMesice[mesic]+" "+rok+"</th><th onclick='dal2()'>&rsaquo;&rsaquo;</th></tr></thead><tbody><tr><th>Po</th><th>Út</th><th>St</th><th>Čt</th><th>Pá</th><th>So</th><th>Ne</th></tr><tr>";
    for(i=1; i<denTyd; i++) {
      tab1+="<td></td>"; //prázdné buňky před 1. dnem měsíce
    }
    
    for(den=1; den<=pocetDniMesice[mesic]; den++) {
      if(rok==dnes.getFullYear() && mesic==dnes.getMonth()+1 && den==dnes.getDate()) {styl="dnes";}
      //else if(rok==r && mesic==m && den==d) {styl="akt";}
      else {styl="";}
      tab1+="<td onclick='vloz2(this)' class='"+styl+"'>"+den+"</td>";
      if(i % 7 == 0 && den!=pocetDniMesice[mesic]) {tab1+="</tr><tr>";} 
      i++;
    }
    for(i=i-1; i % 7 !=0; i++) {
      tab1+="<td></td>"; //prázdné buňky za posledním dnem měsíce pro dokončení tabulky
    }
    tab1+="</tr></tbody></table>";
    return tab1;
  }
  
  function dal2() {  //funkce je spuštěna kliknutím na >> v kalendáři
    if(m==12) {r++; m=1;}
    else {m++;}
    zobrazKalendar2(m,r);
  }
  
  function pred2() {  //funkce je spuštěna kliknutím na << v kalendáři
    if(m==1) {r--; m=12;}
    else {m--;}
    zobrazKalendar2(m,r);
  }
  function vloz2(td) {
    document.getElementsByName("datum2")[0].value=td.innerHTML+"."+m+"."+r;
    skryjKalendar2();
  }
  
  function zobrazKalendar2(mesic,rok) {
      document.getElementById("kalendar2").innerHTML=kalendar2(mesic,rok);  //vytvoření kalendáře
      document.getElementById("kalendar2").style.display="block";          //zobrazení kalendáře
  }
  function skryjKalendar2() {
    document.getElementById("kalendar2").innerHTML="";
    document.getElementById("kalendar2").style.display="none";
  }
  
  function zobrazSkryjKalendar2() {   //funkce spuštěna při kliknutí na ikonu kalendáře ve formuláři
      if(document.getElementsByName("datum2")[0].value!="" && document.getElementById("kalendar2").innerHTML=="") {
        var dat=new Array();
        dat=document.getElementsByName("datum2")[0].value.split("."); //rozdělení zapsaného datumu na části
        if(dat.length==3 && dat[1]>=1 && dat[1]<=12 ) {d=dat[0]; m=dat[1]; r=dat[2];}
      }
      if(document.getElementById("kalendar2").style.display!="block") {zobrazKalendar2(m,r);}
      else {skryjKalendar2();}
  }

