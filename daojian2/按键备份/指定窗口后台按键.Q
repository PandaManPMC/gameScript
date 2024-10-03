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
MacroID=85ed068e-bee6-4801-921e-479623d0cb40
Description=指定窗口后台按键
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
Hwnd = Plugin.Window.Find("pg_gui_window_default_class[16432]", "夏禹剑 - 刀剑2")
//MsgBox "查找到的父窗口句柄为："& Hwnd  
Delay 1000
While True
	Call Plugin.Window.SendKeyPress(Hwnd, 49)
	Delay 33000
Wend
