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
MacroID=df2b8bba-358e-40d5-89ac-8ad6e3ae23e6
Description=背包遍历
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
// 吃卷：注意，背包必须移动到右上角
Function eatReel(tag)
	Delay 100
	// 双循环遍历32个格子
	i = 0
	While i < 8
		j = 0
		While j < 4
			x = 2195 + i * 48
			y = 70 + j * 48
			MoveTo x, y
			Delay 30
			RightClick 30
			
			j = j+1
		Wend
		i = i+1
	Wend
	Delay 100
	Delay 100
End Function

eatReel(0)
