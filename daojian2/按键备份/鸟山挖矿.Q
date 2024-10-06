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
MacroID=4d82c2b2-1a39-4960-88ac-55da92da1ebc
Description=鸟山挖矿
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


UserVar counter=0 "次数"
UserVar diedCount = 0 "死亡次数"


Function miner(tag)
	KeyPress "Num 5", 1
	Delay 500
	
//	KeyPress "Num 2", 1
//	Delay 100
	

	
	For i=1 To 9	
		FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\xihunkuangshi.bmp", 0.6, intX, intY
		
		If intX > 0 And intY > 0 Then 
			MoveTo intX, intY+50
			TracePrint "找到图形，鼠标已经移到图形上面"
			Delay 50
			LeftClick 1
			Delay 5200
			counter = counter + 1
			say("挖矿..." & counter)
		Else 
			TracePrint "未找到图形"
			Delay 50
		End If
		
		
	Next


End Function

// 打开导航
Function openNavigation(tag)
	Delay 20
	MoveTo navigationX,navigationY
	Delay 20
	LeftClick 1
End Function

// 导航输入框,输入坐标寻路
Function gotoLocation(xy)
	say("去:" & xy & "，自动组队已开启，挖矿。开源 ,diedCount=" & diedCount & ",counter=" & counter)
	Delay 100
	MoveTo 2407, 1143
	Delay 30
	LeftClick 1
	
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

// 土遁去鸟山
Function gotoWuQueShan(tag)
	Delay 20
	MoveTo 1407, 1295
	LeftClick 1
	Delay 20
	MoveTo 1247, 732
	LeftClick 1
	Delay 20
	MoveTo 1384, 952
	LeftClick 1
	Delay 20
	MoveTo 1199, 756
	LeftClick 1
	Delay 7000
	KeyPress "W", 1
	Delay 1000
End Function

// 如果死亡 就复活重新来过
Function resurrection(tag)
	//say("resurrection 复活检测")
	FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\huangquanzhilu.bmp", 0.6, intX, intY
	If intX > 0 And intY > 0 Then 
		diedCount = diedCount + 1
		say ("检测到死亡，唉，又白忙活了...复活..重来...diedCount=" & diedCount)
		Delay 300
		MoveTo intX, intY
		TracePrint "resurrection 找到图形，鼠标已经移到图形上面"
		Delay 20
		LeftClick 1
		Delay 3000
		KeyPress "Esc", 1
		gotoWuQueShan (0)
		Goto begin
	Else 
		TracePrint "resurrection 未找到图形"
	End If

End Function

// 上马
Function mountHorse(tag)
	Delay 300
	MoveTo 1357, 1304
	Delay 20
	LeftClick 1
	Delay 5000
End Function

pointArray = Array("358,228","364,217","366,185", "396,178")
delayArray = Array(10000, 10000, 10000, 10000, 10000)



Rem begin


gotoWuQueShan(0)

openNavigation (0)


While True
	
	inx = 0
	For Each val In pointArray
		resurrection(0)
		gotoLocation (val)
//		If inx < 1 Then 
//			Delay 1000
//			mountHorse(0)
//		End If
		Delay delayArray(inx)
		miner(0)
		inx = inx+1
	Next
	
	gotoLocation (pointArray(0))
	Delay 20000
	
Wend
