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
MacroID=ce2c7d65-3557-4c7a-9da1-cebfadc934fb
Description=多开接九凤任务
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

/******** 注意，在开启脚本前，要用 ALT + TAB  把所有刀2的游戏窗口切换一遍，否则 Active 无法激活窗口，无法识图正常排队和战斗。
********* 开启脚本后，会频繁切窗口识图。开多少个号就会切多少排多少
*/

// 指定句柄
//Hwnd1 = Plugin.Window.Find("pg_gui_window_default_class[7328]", "夏禹剑 - 刀剑2")
//Hwnd2 = Plugin.Window.Find("pg_gui_window_default_class[26288]", "夏禹剑 - 刀剑2")
//hwndArr = Array(Hwnd1, Hwnd2)


// 所有窗口 
HwndEx  = Plugin.Window.Search("夏禹剑 - 刀剑2")
hwndArr = Split(HwndEx, "|")

hwndArrLength = UBound(hwndArr)

say("读取到刀2句柄数量=" & hwndArrLength)

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

// 切窗口识图延迟，电脑反应慢的，需要适量增加
tabWindowDelay = 400

// --------- end

// 土遁去九凤
Function gotoJiuFeng(tag)
	Delay 20
	MoveTo tuDunX, tuDunY
	LeftClick 1
	Delay 200
	MoveTo tuDunJiuFengX, tuDunJiuFengY
	LeftClick 1
	Delay 200
	MoveTo tuDunChuFaX, tuDunChuFaY
	LeftClick 1
	Delay 200
	MoveTo tuDunOkX, tuDunOkY
	LeftClick 1
	Delay 2000
End Function


// 打开导航
Function openNavigation(tag)
	Delay 100
	MoveTo navigationX,navigationY
	Delay 100
	LeftClick 1
	Delay 100
End Function

// 上马
Function mountHorse(tag)
	Delay 300
	MoveTo mountHorseX, mountHorseY
	Delay 20
	LeftClick 1
	Delay 6000
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
	Delay 50
	KeyPress "BackSpace", 20
	// 输入坐标
	SayString xy
	Delay 50
	KeyPress "Enter", 1

End Function

// 接任务
Function getTask(name)
	FindPic 100, 100, screenWidth, screenHight, imageBaseUri & name & ".bmp", 0.7, intX, intY

	If intX > 0 And intY > 0 Then 
		MoveTo intX, intY
		TracePrint "getTask 找到图形:" & name
		Delay 100
		
		LeftClick 1
		Delay 300
		
		FindPic 100, 100, screenWidth, screenHight, imageBaseUri & "jiaogeiwoba.bmp", 0.7, intX2, intY2
		If intX2 > 0 And intY2 > 0 Then 
			MoveTo intX2, intY2
			LeftClick 1
			Delay 500
		End If
	Else 
		TracePrint "getTask 未找到图形"
	End If
End Function


Function tabWindow(hwnd)
	// 激活窗口会被系统拦截或其它问题，改为 TAB 切
	Call Plugin.Window.Active(hwnd)
	
	// TAB 切窗口 每次切最后一个	
	/*
	KeyDown "Alt", 1
	For i = 1 To length-1
		KeyPress "Tab", 1
    	Delay 50   
	Next  
	KeyUp "Alt", 1
	*/
End Function


// 轮询激活窗口 去九凤、接任务、回楼梯口上马

// 去九凤
For Each val In hwndArr
	If val = "" Then 
	Else 
		// 轮流激活窗口，土遁去九凤
		tabWindow (val)
		Delay tabWindowDelay
		gotoJiuFeng (0)
	End If
Next


For Each val In hwndArr
	If val = "" Then 
	Else 
		// 轮流激活窗口，打开导航，去悬赏牌
		tabWindow (val)
		Delay tabWindowDelay
		KeyPress "W", 2
		Delay 3000
		openNavigation (0)
		Delay 500
		gotoLocation ("252,854")
		Delay 500
	End If
Next

Delay 38000

// 死循环 识图，直到接到任务
findTaskCount = 0
While findTaskCount < hwndArrLength
	
	For Each val In hwndArr
	
		If val = "" Then 
		Else 
			tabWindow (val)
			Delay tabWindowDelay
			KeyPress "Num 5", 1
			Delay 300
			FindPic 300, 100, screenWidth, screenHight, imageBaseUri & "renwu_img.bmp", 0.7, intX, intY

			If intX > 0 And intY > 0 Then 
				MoveTo intX+10, intY+10
				TracePrint "找到图形" & val & ",findTaskCount=" & findTaskCount
				Delay 50
				// 点击
				LeftClick 1
				Delay 1500
				// 接任务
				getTask ("jiedanmojiufeng")
				
				Delay 200
				MoveTo intX + 10, intY + 10
				LeftClick 1
				Delay 2000
				
				getTask("jiexiangmojiufeng")
				findTaskCount = findTaskCount +1
			Else 
				TracePrint "未找到图形" & val & ",findTaskCount=" & findTaskCount
			End If
		End If
	Next

Wend

// 都接到任务，回楼梯 370,880
For Each val In hwndArr
	If val = "" Then 
	Else 
		// 轮流激活窗口，上马
		tabWindow (val)
		Delay tabWindowDelay
		gotoLocation ("370,880")
		Delay 500
	End If
Next

Delay 35000

For Each val In hwndArr
	If val = "" Then 
	Else 
		// 轮流激活窗口，上马
		tabWindow (val)
		Delay tabWindowDelay
		mountHorse(0)
	End If
Next




