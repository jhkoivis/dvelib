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
#cinst -force notepadplusplus
#cinst -force gimp
#cinst -force inkscape
#cinst -force ccleaner
cinst -force python2-x86_32
cinst easy.install
#cinst -force GoogleChrome
#cinst -force gevent
#cinst -force PDFCreator
cinst eclipse-standard-kepler




# python packages
setx PATH "%PATH%;%systemdrive%\python27"
$env:Path += "%systemdrive%\python27"
setx PATH "%PATH%;%systemdrive%\python27\Scripts"
$env:Path += "%systemdrive%\python27\Scripts"

$easy_install = $env:systemdrive+"\python27\Scripts\easy_install.exe"
iex "$easy_install greenlet"
iex "$easy_install ouimeaux"
iex "$easy_install numpy"
iex "$easy_install scipy"
iex "$easy_install matplotlib"




# python packages
setx PATH "%PATH%;%systemdrive%\python2-x86_32"
$env:Path += "%systemdrive%\python2-x86_32"
setx PATH "%PATH%;%systemdrive%\python2-x86_32\Scripts"
$env:Path += "%systemdrive%\python2-x86_32\Scripts"

$easy_install = $env:systemdrive+"\python2-x86_32\Scripts\easy_install.exe"
iex "$easy_install greenlet"
iex "$easy_install ouimeaux"
iex "$easy_install numpy"
iex "$easy_install scipy"
iex "$easy_install matplotlib"




