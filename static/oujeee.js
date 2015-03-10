/*        oujee.js JavaScript    */

// aby selektor :contains byl caseInsensitive
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});

/*********************************************
 *      List filter 
 **********************************************/

var listFilter = {
    init : function() {
        // formulář
        listFilter.form = $("<form>").attr({ 
            "class":"j-filterform",
            "action":"#"
        });
        // odstavec
        listFilter.p = $('<p>').addClass('j-filterp');
        listFilter.p.html('Filter pro otázky <br />')
        // input  
        listFilter.input = $("<input>").attr({
            "class":"j-filterinput",
            "type":"text",
            "placeholder":"hledaný regulární výraz",
        });   
        listFilter.rst = $("<input>").attr({
            "type":"reset",
            "value":"X",
        });   
        // složím to dohromady
        listFilter.p.append(listFilter.input);
        listFilter.p.append(listFilter.rst);
        listFilter.form.append(listFilter.p);
        listFilter.list = $(".listfilter");
        listFilter.list.before(listFilter.form);

        // Když dám enter
//        listFilter.input.change(listFilter.changeRegExListner);
        // Když něco napíšu
        listFilter.input.keyup(listFilter.changeRegExListner);
        // Když kliknu na RESET
        listFilter.rst.click(listFilter.showAll);
    },

    changeRegExListner : function() {
        // Zobrazí jen li, které obsahují regulární výraz
        var filter = listFilter.input.val();
        var regex = new RegExp(filter, "i");
        var li = listFilter.list.find("li");
        for (var i = 0; i< li.length; i++) {
            textNadpis = $(li[i]).find('h2').text();
            textObsah = $(li[i]).find('p').text();
            if (regex.test(textNadpis) || regex.test(textObsah) ) {
                $(li[i]).show();
            } else {
                $(li[i]).hide();
            }
        }
    },

    showAll : function() {
        // Zobrazí znovu celý seznam
        listFilter.list.find('li').show()
    }, 

//    changeListner : function() {
//        // get the value of the input, which we filter on
//        var filter = listFilter.input.val();
//        // Hledám v napisech
//        listFilter.list.find("li h2:contains("+filter+")")
//            .parentsUntil('ul','li').show();
//        listFilter.list.find("li h2:not(:contains("+filter+ "))")
//            .parentsUntil('ul','li').hide();
//        // hledám v obsahu
//        listFilter.list.find("li p:contains("+filter+")")
//            .parentsUntil('ul','li').show();
//        listFilter.list.find("li p:not(:contains("+filter+ "))")
//            .parentsUntil('ul','li').hide();
//    },
}

// ready
$( listFilter.init );
