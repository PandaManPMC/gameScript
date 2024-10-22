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
MacroID=9d8cbaef-c514-4472-8b34-f07b80cf9f60
Description=ºóÌ¨°´¼ü
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

Hwnd = Plugin.Window.Find("pg_gui_window_default_class[19608]", "ÏÄÓí½£ - µ¶½£2")
//Hwnd = Plugin.Window.Find("pg_gui_window_default_class[19608]", "ÏÄÓí½£ - µ¶½£2")
Delay 2100
While True
	Call Plugin.Window.SendKeyPress(Hwnd, 49)
	//Delay 35000
	Delay 27000
Wend
