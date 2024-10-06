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
MacroID=b496594b-3192-4e83-9e63-409753fccfe9
Description=研磨
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
Delay 1000
UserVar counter=0 "设置内容"

While True
	KeyPress "X", 1
	Delay 30
	LeftClick 1
	Delay 30
	LeftClick 1
	Delay 5000
	KeyPress "Enter", 1
	SayString "自动研磨...." & counter
	KeyPress "Enter", 1
	counter = counter + 1
	If counter = 50 Then 
		KeyPress "1", 1
	End If
	If counter = 100 Then 
		KeyPress "2", 1
	End If
	If counter = 150 Then 
		KeyPress "3", 1
	End If
	If counter = 200 Then 
		KeyPress "4", 1
	End If
	If counter = 250 Then 
		KeyPress "5", 1
	End If
	If counter = 300 Then 
		KeyPress "6", 1
	End If
	If counter = 350 Then 
		KeyPress "7", 1
	End If
	If counter = 400 Then 
		KeyPress "8", 1
	End If
	If counter = 450 Then 
		KeyPress "9", 1
	End If
	If counter = 500 Then 
		KeyPress "0", 1
	End If
	If counter = 550 Then 
		KeyPress "-", 1
	End If
	If counter = 600 Then 
		KeyPress "=", 1
	End If
	If counter = 650 Then 
		KeyPress "V", 1
	End If
	If counter = 700 Then 
		KeyPress "R", 1
	End If
	If counter = 750 Then 
		KeyPress "E", 1
	End If
	If counter = 800 Then 
		KeyPress "`", 1
	End If
Wend
