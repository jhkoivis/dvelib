# Welcome to Dvelib #

Scripts and small programs that should be available in every os, mostly networking and python related. The most useful ones are listed here.

## Stream video through network ##

  * Really simple (if you know ssh pipes or have no firewalls)
  * TODO: add to python remote commands
  * tested on osx (nc command might be different on linux or windows)
  * 127.0.0.1 is your client's (or server's) ip

On client. The client (listener) has to be first:
```
nc -l 127.0.0.1 5001 | mplayer -fps 31 -cache 1024 -
```
On server
```
cat Sample.mp4 | nc 127.0.0.1 5001
```

## Armylist Excel ##

  * Utilizes excel's autocomplete by adding "item" names as named cells
  * Can be used as a normal excel sheet

[download here](https://dvelib.googlecode.com/svn/trunk/production/excelArmyList/ExcelArmyList.xlsm)

![https://dvelib.googlecode.com/svn/trunk/production/excelArmyList/AutoCompleteArmylistExplained.png](https://dvelib.googlecode.com/svn/trunk/production/excelArmyList/AutoCompleteArmylistExplained.png)

## Autohotkey to startup ##

Copy this to powershell:

```
cd '~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
$path = '' + $(pwd) + '/keyRemap.ahk'
$url = 'https://dvelib.googlecode.com/svn/trunk/production/userization/keyRemap.ahk'
(new-object System.Net.WebClient).DownloadFile($url, $path)
```

  * inverts mouse (wheel)

## Tampermonkey scripts ##

  * Install [Tampermonkey](http://tampermonkey.net/)
  * Allow access to file URLs: chrome->settings->extensions->tampermonkey where tick "Allow access to file URLs"
  * click links below to install script

[oikotie cleaner](https://dvelib.googlecode.com/svn/trunk/production/userization/tamper/asunnot_oikotie_fi.tamper.js)



## Timer Bar ##

Timer Bar written in javascript. Object oriented approach.

wget https://dvelib.googlecode.com/files/javaScriptTimeBar.zip

https://dvelib.googlecode.com/svn/trunk/production/javaScriptTimeBar/timeBarHtml.PNG
![https://dvelib.googlecode.com/svn/trunk/production/javaScriptTimeBar/timerBarSchematic.png](https://dvelib.googlecode.com/svn/trunk/production/javaScriptTimeBar/timerBarSchematic.png)

## .bashrc ##

Get it with wget:

`wget https://dvelib.googlecode.com/svn/trunk/production/userization/.bashrc`

  * arrow up is autocomplete from history (search backwords text written to command line)
  * Shows current directory between command lines in dark green and starts command line at the left edge of the screen.
    * Colors are for black background.
    * most commands fit to one line.
    * path is still visible but on the background (as it's dark colored).
> https://dvelib.googlecode.com/svn/trunk/production/userization/shellExample.PNG


## Finnish Apple keyboard for windows 7 32/64 bit ##

The best apple things ever: 7/|\, 8([{... Those that are unfamiliar with apple products, 7/|\ means: 7, 7+shift, 7+alt, 7+alt+shift...

https://dvelib.googlecode.com/files/finnish-apple-keyboard-layout-for-windows.zip