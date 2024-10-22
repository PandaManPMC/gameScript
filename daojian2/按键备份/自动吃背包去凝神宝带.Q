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
MacroID=777fe852-3608-462a-a90a-f93c3935d794
Description=自动吃背包去凝神宝带
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

// 导航所在
UserVar navigationX =2358 "导航所在"
UserVar navigationY =1267 "导航所在"

UserVar tuDunX = 1407 "土遁所在 X "
UserVar tuDunY = 1295 "土遁所在 Y "

UserVar tuDunChuFaX = 1384 "土遁出发 X"
UserVar tuDunChuFaY = 952 "土遁出发 Y"

UserVar tuDunOkX = 1199 "土遁确定 X"
UserVar tuDunOkY = 756 "土遁确定 Y"

UserVar tuDunJiuFengX = 1308 "九凤 X"
UserVar tuDunJiuFengY = 839 "九凤 Y"

UserVar mountHorseX = 1357 "马 X"
UserVar mountHorseY = 1304 "马 Y"

// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"

UserVar isNingShenBaoDai = False "是否是凝神宝袋"

// 吃卷：注意，背包必须移动到右上角
Function eatReel(tag)
	Delay 100
	KeyPress "B", 1
	Delay 30
	// 双循环遍历32个格子
	i = 0
	While i < 8
		j = 0
		While j < 4
			x = 2195 + i * 48
			y = 70 + j * 48
			MoveTo x, y
			Delay 20
			delNinShenBaoDai (0)
			
			If isNingShenBaoDai Then 
			
			Else 
				RightClick 3
				Delay 10
				RightClick 3
				Delay 10
				RightClick 3
				Delay 10
			End If
			
			
			j = j+1
		Wend
		i = i+1
	Wend
	//Delay 100
	// 吃第二背包的
	i = 0
	While i < 8
		j = 0
		While j < 5
			x = 2195 + i * 48
			y = 295 + j * 48
			MoveTo x, y
			Delay 20
			
			delNinShenBaoDai (0)
			TracePrint "eatReel isNingShenBaoDai=" &isNingShenBaoDai
			
			If isNingShenBaoDai Then 
			
			Else 
				RightClick 2
				Delay 20
				RightClick 2
				Delay 20
				RightClick 2
			End If
			
			
			j = j+1
		Wend
		i = i+1
	Wend
	Delay 100

	KeyPress "B", 1
	eatCount = eatCount + 1
	Delay 100
End Function


// 删除凝神宝袋
Function delNinShenBaoDai(tag)
	isNingShenBaoDai = False
	Delay 100
	FindPic 1400, 10, screenWidth, screenHight-700, "C:\Users\Administrator\Documents\dao2\ningshenbaodai.bmp", 0.6, intX, intY
	
	If intX > 0 And intY > 0 Then 
		TracePrint "delNinShenBaoDai 找到图形"
		Delay 30
		// 鼠标左键单击，鼠标移动出包裹，再单击左键，点确定，删除凝神宝袋
		LeftClick 1
		Delay 30
		MoveTo 2048, 133
		Delay 30
		LeftClick 1
		Delay 30
		MoveTo 1197,758
		Delay 30
		LeftClick 1
		Delay 30
		isNingShenBaoDai = True
	Else 
		TracePrint "未找到图形"
	End If
	
End Function



eatReel(0)
