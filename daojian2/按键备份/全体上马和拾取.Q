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
MacroID=513c7418-8ba8-4e1d-8954-bf06e9825652
Description=全体上马和拾取
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
		// 组合键
		Call Plugin.Bkgnd.KeyDown(Clng(value), 17)
		Call Plugin.Bkgnd.KeyPress(Clng(value), 69)
		Call Plugin.Bkgnd.KeyUp(Clng(value), 17)
	End If
Next : Delay 30

TracePrint "上马结束"



// 捡东西
While True
	For Each value In Split(HwndArr, "|")
		If value = "" Then 
		Else
			Call Plugin.Bkgnd.KeyPress(Clng(value), 90)
		End If
	Next : Delay 50
	Delay 400
Wend
