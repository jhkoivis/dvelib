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


