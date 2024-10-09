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
MacroID=9ceeb143-9b4a-48a4-bbbd-ab3484d2ce9c
Description=打群侠
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


// ---------- 不同环境需要调试的参数 begin

// 马在 A+6 土遁在 A+Q

// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

// 导航所在
UserVar navigationX =2358 "导航所在 X"
UserVar navigationY =1267 "导航所在 Y"

UserVar tuDunX = 1407 "土遁所在 X "
UserVar tuDunY = 1295 "土遁所在 Y "

// 瓦当
UserVar waDangX = 1277 "瓦当 X"
UserVar waDangY = 482 "瓦当 Y"

// 朝歌
UserVar zgX = 1255 "朝歌 X"
UserVar zgY = 521 "朝歌 Y"

UserVar tuDunChuFaX = 1384 "土遁出发 X"
UserVar tuDunChuFaY = 952 "土遁出发 Y"

UserVar tuDunOkX = 1199 "土遁确定 X"
UserVar tuDunOkY = 756 "土遁确定 Y"

UserVar bangShouX = 983 "挑战时的帮手 X"
UserVar bangShouY = 610 "挑战时的帮手 Y"


// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"

// ------------- end


// ------ 不同角色要调整的参数 begin
// 延迟和技能需要单独配置

// 技能快捷键：罗刹 - 不动尊、金刚、逆火、蛮牛、铁浮
//attackArr = Array("X", "V", "R", "E", "`")
// 技能施法时间
//attackDelayArr = Array(900, 4000, 3000, 2200, 1500)


// 技能快捷键：日天剑侠 - 征鸿、盗甲、雨溅、云去、如封
attackArr = Array("X", "V", "R", "E", "`")
// 技能施法时间
attackDelayArr = Array(1800, 1500, 3000, 2300, 1500)



// --------- end

// 土遁去瓦当
Function gotoWaDang(tag)
	Delay 20
	MoveTo tuDunX, tuDunY
	LeftClick 1
	Delay 100
	MoveTo waDangX, waDangY
	LeftClick 1
	Delay 100
	MoveTo tuDunChuFaX, tuDunChuFaY
	LeftClick 1
	Delay 100
	MoveTo tuDunOkX, tuDunOkY
	LeftClick 1
	Delay 8000
	KeyPress "W", 1
	Delay 1000
End Function


// 土遁去朝歌
Function gotoZhaoGe(tag)
	Delay 20
	MoveTo tuDunX, tuDunY
	LeftClick 1
	Delay 100
	MoveTo zgX, zgY
	LeftClick 1
	Delay 100
	MoveTo tuDunChuFaX, tuDunChuFaY
	LeftClick 1
	Delay 100
	MoveTo tuDunOkX, tuDunOkY
	LeftClick 1
	Delay 8000
	KeyPress "W", 1
	Delay 1000
End Function

// 打开导航
Function openNavigation(tag)
	Delay 20
	MoveTo navigationX,navigationY
	Delay 20
	LeftClick 1
	Delay 100
End Function

// 导航输入框,输入坐标寻路
Function gotoLocation(xy)
	say("去:" & xy & "，打群侠。开源 github")
	Delay 100
	MoveTo 2407, 1143
	Delay 30
	LeftClick 1
	Delay 100
	
	// 删除坐标
	Delay 30
	KeyPress "BackSpace", 20
	// 输入坐标
	SayString xy
	Delay 20
	KeyPress "Enter", 1

End Function

Function say(txt)
	now=Plugin.GetSysInfo.GetDateTime()    
	TracePrint now & "：" & txt
	KeyPress "Enter", 1
	SayString now & "：" & txt
	KeyPress "Enter", 1
End Function

// 上马
Function mountHorse(tag)
	Delay 300
	MoveTo 1357, 1304
	Delay 20
	LeftClick 1
	Delay 5000
End Function

UserVar isFindQunXia = False "是否找到"

Function findQunXia(name)
	KeyPress "Num 5", 1
	Delay 400
	isFindQunXia = False
	For i = 1 To 15
		FindPic 300, 300, screenWidth - 200, screenHight - 200, imageBaseUri & name & ".bmp", 0.7, intX, intY
		If intX > 0 And intY > 0 Then 
			TracePrint "findQunXia 找到图形，鼠标已经移到图形上面"
			Delay 20
			MoveTo intX, intY+90
			Delay 500
			LeftClick 1
			Delay 3000
			
			FindPic 300, 300, screenWidth - 200, screenHight - 100, imageBaseUri & "biwuqiujiu.bmp", 0.7, intX2, intY2
			If intX2 > 0 And intY2 > 0 Then 
				TracePrint "findQunXia 2 找到图形，鼠标已经移到图形上面"
				Delay 20
				MoveTo intX2, intY2
				Delay 500
				LeftClick 1
				Delay 300
				MoveTo intX2 + 200, intY2 - 200
				isFindQunXia = True
				Exit For
				Delay 500
			End If

		Else 
			TracePrint "未找到图形"
			Delay 100
			KeyPress "Num 4", 1
			Delay 300
		End If
	Next

End Function



// 挑战
Function challenge(name)
	isFinished = False
	Delay 300
	FindPic 300, 300, screenWidth - 200, screenHight - 100, imageBaseUri & "queding_black.bmp", 0.7, intX2, intY2
	If intX2 > 0 And intY2 > 0 Then 
		TracePrint "challenge 1 找到图形，鼠标已经移到图形上面"
		Delay 20
		MoveTo intX2, intY2
		Delay 100
		LeftClick 1
		Delay 300
		
		isFinish1 (name)
		If isFinished Then 
			Exit Function
		End If
		
		// 帮手
		MoveTo bangShouX, bangShouY
		Delay 200
		LeftClick 1
		Delay 2000
		
		//  再次检测是否完成
		isFinish2 (name)
		If isFinished Then 
			Exit Function
		End If
		
		
		// 向前走		
		KeyDown "W", 1
		Delay 4000
		KeyUp "W", 1

		KeyPress "Tab", 1
		Delay 300
		
		// 攻击
		notFinish = True
		While notFinish
			inx = 0
			
			For Each val In attackArr
				KeyPress val, 1
				Delay attackDelayArr(inx)
				inx = inx + 1
				KeyPress "Tab", 1
				
				If 3 = inx Then 
					KeyPress "S", 2
				End If
				
				// 打完检测
				FindPic 300, 300, screenWidth - 100, screenHight - 300, imageBaseUri & "queding_black_finish.bmp", 0.7, intX3, intY3
				If intX3 > 0 And intY3 > 0 Then 
					MoveTo intX3, intY3
					TracePrint "challenge 2 找到图形，鼠标已经移到图形上面"
					Delay 20
					LeftClick 1
					Delay 200
					notFinish = False
				Else 
					TracePrint "未找到图形"
				End If
			Next
			
		Wend
		
	End If
End Function

UserVar isFinished = False "是否完成"
Function isFinish1(name)
	Delay 500
	FindPic 300, 50, screenWidth - 300, screenHight - 300, imageBaseUri & "qunxiayida.bmp", 0.7, intX, intY
	If intX > 0 And intY > 0 Then 
		MoveTo intX, intY
		TracePrint "isFinish 找到图形，鼠标已经移到图形上面"
		say("isFinish1 检测到" & name & "已经完成")
		isFinished = True
		Delay 20
		Exit Function
	Else 
		TracePrint "未找到图形"
	End If
	
End Function

Function isFinish2(name)
	Delay 500	
	// 第二种检测是否已经完成的办法
	For i = 1 To 5
		FindPic 500, 500, screenWidth, screenHight, imageBaseUri & "tuichufuben.bmp", 0.7, intX, intY
		If intX > 0 And intY > 0 Then 
			TracePrint "isFinish2 找到图形，鼠标已经移到图形上面"
			say("isFinish2 检测到" & name & "正在副本")
			Delay 20
			isFinished = False
			Exit Function
		Else 
			TracePrint "未找到图形"
			Delay 300
			isFinished = True
		End If
	Next
	say("isFinish2 检测到" & name & "已经完成")
End Function


// 挑战三次
Function threeChallenge(name)
	For 5
		findQunXia (name)
		If isFindQunXia Then 
			challenge (name)
			Delay 3500
			gift(0)
			If isFinished Then 
				Exit Function
			End If
		End If
		Delay 500
	Next
End Function

// 礼物
Function gift(tag)
	Delay 400
	FindPic 300, 300, screenWidth - 300, screenHight - 300, imageBaseUri & "qunxiagaojiliwu.bmp", 0.7, intX, intY

	If intX > 0 And intY > 0 Then 
		MoveTo intX, intY
		TracePrint "找到图形，鼠标已经移到图形上面"
		Delay 50
		LeftClick 1
	Else 
		TracePrint "未找到图形"
	End If
	
End Function

gotoWaDang(0)

Rem begin

// 打开
openNavigation (0)
Delay 300

// 陈仓
gotoLocation ("672,555")
mountHorse(0)
Delay 13000
threeChallenge ("chencang")


// 高乘风
gotoLocation ("626,470")
Delay 13000
threeChallenge ("gaochengfeng")



// 苏媚
gotoLocation ("629,456")
Delay 6000
threeChallenge ("sumei")

// 去朝歌
gotoZhaoGe (0)

// 单平
gotoLocation ("1291,1340")
mountHorse(0)
Delay 13000
threeChallenge ("danping")

// 慕容澈
gotoLocation ("1187,1349")
mountHorse(0)
Delay 13000
threeChallenge ("murongche")

// 韩啸声
gotoLocation ("1504,991")
Delay 8000
mountHorse(0)
Delay 30000
threeChallenge ("hanxiaosheng")


MessageBox "挑战群侠结束"