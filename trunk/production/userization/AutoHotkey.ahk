

#MaxHotkeysPerInterval 2000

WheelUp::
Send {WheelDown}
Return

WheelDown::
Send {WheelUp}
Return

*<#c::^c  ; win+c -> ctrl+c = copy
*<#v::^v  ; win+v -> ctrl+v = paste
*<#x::^x  ; win+x -> ctrl+x = cut
*<#s::^s  ; win+s -> ctrl+s = save
*<#z::^z  ; win+z -> ctrl+z = undo

