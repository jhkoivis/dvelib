#############################
# get and run this file     #
#############################
# @powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://dvelib.googlecode.com/svn/trunk/production/userization/cinst_et_all.bat'))"

# get chocolatey.org
powershell.exe -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" 
# set chocolatey path (permanent and current session)
setx PATH "%PATH%;%systemdrive%\chocolatey\bin"
$env:Path += "%systemdrive%\chocolatey\bin"

# install programs
cinst notepad++
cinst gimp
cinst inkscape






