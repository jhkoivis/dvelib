// ==UserScript==
// @name       oikotie add hider
// @namespace  https://dvelib.googlecode.com/svn/trunk/production/userization/tamper/asunnot_oikotie_fi.tamper.js
// @version    1.0
// @description  hides two divs that adblock can't hide
// @match      http://asunnot.oikotie.fi/*
// @copyright  MIT-license
// ==/UserScript==


var a = document.getElementById("widget-ad-etua");
a.style.display = 'none';

var b = document.getElementById("header-links");
b.style.display = 'none';

// Distance to keravan asema below

function DynamicDiv(link) {       
    var dynDiv = document.createElement("div");
    dynDiv.id = "divDyna";
    //dynDiv.innerHTML = link;
    dynDiv.style.height = "20px";
    dynDiv.style.width = "300px";     
    //dynDiv.style.backgroundColor = 'gray';
    dynDiv.style.position = "absolute";
    dynDiv.style.top = "0px";
    dynDiv.style.right = "0px";
    dynDiv.appendChild(link);
    //var innerText = '<object type="text/html" data="www.google.fi" style="width:100%; height:400px; margin:1%;"></object>';
    //alert(innerText);
    //dynDiv.innerHTML = innerText;

    document.body.appendChild(dynDiv);
}

//<object type="text/html" data="http://yahoo.com/" style="width:100%; height:400px; margin:1%;"></object>




function getElementByClass(matchClass) {
    var elems = document.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + matchClass + ' ')
                > -1) {
            return elems[i];
        }
    }
}

function getAddress(){

    var elem = getElementByClass('widget-ad-information-table');
	var tableText = elem.innerHTML;
    var startIndPre = tableText.indexOf('ijainti');
    var startInd = tableText.indexOf('<td>', startIndPre) + 4;
    var endInd = tableText.indexOf('</td>', startInd);
    
    return tableText.substring(startInd, endInd);
}

function createGoogleLink(from, to){
	var linkAddress = 'https://maps.google.com/maps?saddr=' + from.trim() + '&daddr=' + to.trim() + '&dirflg=w';
	//return linkAddress;
    var link = document.createElement('a');
    link.href = linkAddress;
    link.target = "_blank";
    link.innerHTML = 'googleMaps from-to';
    return link;
}


DynamicDiv(createGoogleLink(getAddress(), 'keravan asema'));

