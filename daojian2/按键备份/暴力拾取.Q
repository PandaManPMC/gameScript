[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=59b62c92-3ac2-419d-88d9-05182899b902
Description=±©¡¶ ∞»°
Enable=1
AutoRun=0
[Repeat]
Type=0
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]
HwndEx  = Plugin.Window.Search("œƒ”ÌΩ£ - µ∂Ω£2")

While True
	For Each value In Split(HwndEx, "|")
		If value = "" Then 
		Else
			Call Plugin.Bkgnd.KeyPress(Clng(value), 119)
		End If
	Next : Delay 50
	Delay 10
Wend
