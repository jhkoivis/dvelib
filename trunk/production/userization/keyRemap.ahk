
;
;
; HKEY_LOCAL_MACHINE\Software\Microsoft\WindowsNT\Cu rrentVersion\WinLogon\
;
;
; Get-ChildItem HKEY_LOCAL_MACHINE\Software\Microsoft\WindowsNT\Cu rrentVersion\WinLogon\
;
; cd '~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
; (new-object System.Net.WebClient).DownloadFile('https://dvelib.googlecode.com/svn-history/r50/trunk/production/userization/keyRemap.ahk','~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
;
;
;
;(new-object System.Net.WebClient).DownloadFile('https://dvelib.googlecode.com/svn-history/r50/trunk/production/userization/keyRemap.ahk', 'C:\users\juha koivisto\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\keyRemap.ahk')
;
;

WheelUp::
Send {WheelDown}
Return

WheelDown::
Send {WheelUp}
Return







