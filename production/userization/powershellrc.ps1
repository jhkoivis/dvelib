

Set-Alias l color-ls
Set-Alias makeVideo 'echo ffmpeg -start_number 0 -i 3mm_steel_bearings_45deg_%06d.tif.png -vb 20M -filter:v "setpts=1*PTS" -vf steel.avi'
Set-Alias make nmake

Set-PSReadlineOption -TokenKind Command -ForegroundColor Gray

$HOST.UI.RawUI.ForegroundColor = "Gray"

Write-Host "Ctrl-S: opens settings (in Console2 window)"
Write-Host "Crtl-right: drags window"
Write-Host " "

##########################################################################

pushd "C:\Users\jhkoi\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0" 
cmd /c "vcvarsall.bat&set" |
foreach {
  if ($_ -match "=") {
    $v = $_.split("="); set-item -force -path "ENV:\$($v[0])"  -value "$($v[1])"
  }
}
popd

###########################################################################

Function Global:Prompt 
{
   $wid=[System.Security.Principal.WindowsIdentity]::GetCurrent()
   $prp=new-object System.Security.Principal.WindowsPrincipal($wid)
   $adm=[System.Security.Principal.WindowsBuiltInRole]::Administrator
   $IsAdmin=$prp.IsInRole($adm)
   
   if ($IsAdmin)
   {
     Write-Host -Fore "DarkRed" $PWD 
     Write-Host -Fore "DarkRed" -no ">"
   }else{
     Write-Host -Fore "DarkGreen" $PWD 
     Write-Host -Fore "DarkGreen" -no ">"
   } 
  
  return " "

}

function color-ls
{
    $regex_opts = ([System.Text.RegularExpressions.RegexOptions]::IgnoreCase `
          -bor [System.Text.RegularExpressions.RegexOptions]::Compiled)
    $fore = $Host.UI.RawUI.ForegroundColor
    $compressed = New-Object System.Text.RegularExpressions.Regex(
          '\.(zip|tar|gz|rar|jar|war)$', $regex_opts)
    $executable = New-Object System.Text.RegularExpressions.Regex(
          '\.(exe|bat|cmd|py|pl|ps1|psm1|vbs|rb|reg)$', $regex_opts)
    $text_files = New-Object System.Text.RegularExpressions.Regex(
          '\.(txt|cfg|conf|ini|csv|log|xml|java|c|cpp|cs)$', $regex_opts)

    Invoke-Expression ("Get-ChildItem $args") | ForEach-Object {
        if ($_.GetType().Name -eq 'DirectoryInfo') 
        {
            $Host.UI.RawUI.ForegroundColor = 'Magenta'
            echo $_
            $Host.UI.RawUI.ForegroundColor = $fore
        }
        elseif ($compressed.IsMatch($_.Name)) 
        {
            $Host.UI.RawUI.ForegroundColor = 'darkgreen'
            echo $_
            $Host.UI.RawUI.ForegroundColor = $fore
        }
        elseif ($executable.IsMatch($_.Name))
        {
            $Host.UI.RawUI.ForegroundColor = 'Red'
            echo $_
            $Host.UI.RawUI.ForegroundColor = $fore
        }
        elseif ($text_files.IsMatch($_.Name))
        {
            $Host.UI.RawUI.ForegroundColor = 'Yellow'
            echo $_
            $Host.UI.RawUI.ForegroundColor = $fore
        }
        else
        {
            echo $_
        }
    }
}


################################################################

function which
{
    get-command $args[0] |select -expandproperty Path
}

