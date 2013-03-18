// ==UserScript==
// @name       oikotie add hider
// @namespace  http://use.i.E.your.homepage/
// @version    1.0
// @description  hides two divs that adblock can't hide
// @match      http://asunnot.oikotie.fi/*
// @copyright  MIT-license
// ==/UserScript==


var a = document.getElementById("widget-ad-etua");
a.style.display = 'none';

var b = document.getElementById("header-links");
b.style.display = 'none';


