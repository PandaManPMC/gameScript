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
MacroID=343b421c-d486-45a2-8f8c-8067d546b435
Description=识图
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
// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"

//FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\zhanchangpaidui.bmp", 0.7, intX, intY
FindPic 0, 0, screenWidth, screenHight, imageBaseUri & "zhanchangpaidui.bmp", 0.7, intX, intY

If intX > 0 And intY > 0 Then 
	MoveTo intX, intY
	TracePrint "找到图形，鼠标已经移到图形上面"
	Delay 20
Else 
	TracePrint "未找到图形"
End If

