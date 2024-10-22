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
Description=Ç°Ì¨°´¼ü
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

/*
Hwnd = Plugin.Window.Find("pg_gui_window_default_class[13220]", "ÏÄÓí½£ - µ¶½£2")
Delay 1000
While True
	Call Plugin.Window.SendKeyPress(Hwnd, 49)
	Delay 27500
Wend
*/

Delay 2000
While True
	KeyPress 49, 1
	Delay 27000
	//Delay 35000
Wend
