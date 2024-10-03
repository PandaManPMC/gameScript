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
MacroID=8da6d18d-90d4-4856-942e-d6711dafe408
Description=拾取
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
HwndEx  = Plugin.Window.Search("夏禹剑 - 刀剑2")
//MsgBox "查找到符合的窗口句柄为："& HwndEx   

While True
	For Each value In Split(HwndEx, "|")
		If value = "" Then 
		Else
			Call Plugin.Bkgnd.KeyPress(Clng(value), 119)
		End If
	Next : Delay 50
	Delay 800
Wend
