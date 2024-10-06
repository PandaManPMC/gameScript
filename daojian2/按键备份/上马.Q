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
MacroID=15d5ff97-6a14-4f3a-b03e-98fea8a66d11
Description=上马
Enable=0
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
HwndArr = Plugin.Window.Search("夏禹剑 - 刀剑2")

// E 上马 Z 拾取

// 所有窗口上马
For Each value In Split(HwndArr, "|")
	If value = "" Then 
	Else
		//Call Plugin.Bkgnd.KeyPress(Clng(value), 69)
		Call Plugin.Bkgnd.KeyDown(Clng(value), 17)
		Call Plugin.Bkgnd.KeyDown(Clng(value), 69)
		//Call Plugin.Bkgnd.KeyPress(Clng(value), 69)
		Call Plugin.Bkgnd.KeyUp(Clng(value), 69)
		Call Plugin.Bkgnd.KeyUp(Clng(value), 17)
		
	End If
Next : Delay 30

TracePrint "上马结束"

HwndArr = Plugin.Window.Search("夏禹剑 - 刀剑2")

For Each value In Split(HwndArr, "|")
	If value = "" Then 
	Else
		Call Plugin.Bkgnd.KeyPress(Clng(value), 17)	
	End If
Next : Delay 30