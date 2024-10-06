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
MacroID=0a472745-2202-4fe1-976c-f3807fdf88f6
Description=段位赛
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
// 指定句柄
//Hwnd1 = Plugin.Window.Find("pg_gui_window_default_class[7328]", "夏禹剑 - 刀剑2")
//Hwnd2 = Plugin.Window.Find("pg_gui_window_default_class[26288]", "夏禹剑 - 刀剑2")
//hwndArr = Array(Hwnd1, Hwnd2)

// 所有窗口
HwndEx  = Plugin.Window.Search("夏禹剑 - 刀剑2")
hwndArr = Split(HwndEx, "|")

length = UBound(hwndArr)

say("读取到刀2句柄数量=" & length)


// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

UserVar jingjiX = 2252 "竞技活动按钮 X"
UserVar jingjiY = 45 "竞技活动按钮 Y"

UserVar duanweiX = 885 "段位赛选择 X"
UserVar duanweiY = 548 "段位赛选择 Y"

UserVar baomingX = 920 "报名按钮 X"
UserVar baomingY = 944 "报名按钮 Y"

UserVar guanbiX = 1745 "关闭窗口按钮 X"
UserVar guanbiY = 406 "关闭窗口按钮 Y"


// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"



Function say(txt)
	now=Plugin.GetSysInfo.GetDateTime()    
	TracePrint now & "：" & txt
	//KeyPress "Enter", 1
	//SayString now & "：" & txt
	//KeyPress "Enter", 1
End Function

UserVar isFubened = False "是否在副本"
Function isFuben(hwnd)
	isFubened = False
	Delay 300	
	//For i = 1 To 3
		//iCoord = Plugin.Bkgnd.FindPic(hwnd,0,0,1024,768, imageBaseUri & "tuichufuben.bmp",  0, 0.7)   
		//XY = Split(iCoord, "|")
		//intX = XY(0)
		//intY = XY(1)
		
		// 激活窗口 识图
		Call Plugin.Window.Active(hwnd)
		Delay 300
		FindPic 0, 0, screenWidth, screenHight, imageBaseUri & "tuichufuben.bmp", 0.7, intX, intY
		
		
		If intX > 0 And intY > 0 Then 
			TracePrint hwnd & "isFuben 找到图形，鼠标已经移到图形上面"
			say(hwnd & "isFuben 检测到正在副本")
			Delay 20
			isFubened = True
			Exit Function
		Else 
			TracePrint hwnd & "isFuben 未找到图形"
			Delay 300
			isFubened = False
		End If
	//Next
End Function

// 排队
Function queueUp(val)
	// 打开竞技窗口
	If val = "" Then 
	Else
		Call Plugin.Bkgnd.LeftClick(val, jingjiX, jingjiY)
	End If
	Delay 300
	
	// 选择段位赛
	If val = "" Then 
	Else
		Call Plugin.Bkgnd.LeftClick(val, duanweiX, duanweiY)
	End If
	Delay 300
	
	// 报名
	If val = "" Then 
	Else
		Call Plugin.Bkgnd.LeftClick(val, baomingX, baomingY)
	End If
	Delay 300
	
	// 关闭窗口
	If val = "" Then 
	Else
		Call Plugin.Bkgnd.LeftClick(val, guanbiX, guanbiY)
	End If
	Delay 300

End Function


isQueueUpEd = False
// 是否在排队
Function isQueueUp(hwnd)
	isQueueUpEd = False
	Delay 100
	
	//iCoord = Plugin.Bkgnd.FindPic(hwnd,0,0,1024,768, imageBaseUri & "zhanchangpaidui.bmp",  0, 0.7)   
	//XY = Split(iCoord, "|")
	//intX = XY(0)
	//intY = XY(1)
	
	// 激活窗口 识图
	Call Plugin.Window.Active(hwnd)
	Delay 300

	FindPic 0, 0, screenWidth, screenHight, imageBaseUri & "zhanchangpaidui.bmp", 0.7, intX, intY
	
	
	If intX > 0 And intY > 0 Then 
		TracePrint hwnd & "isQueueUp 找到图形"
		say(hwnd & "isQueueUp 检测到正在排队")
		Delay 20
		isQueueUpEd = True
		Exit Function
	Else 
		TracePrint hwnd & "isQueueUp 未找到图形"
		Delay 300
		isQueueUpEd = False
	End If

End Function


// 全部开始排队
For Each val In hwndArr
	queueUp(val)
Next


// 技能快捷键 x v r e `
attackArr = Array(88, 86, 82, 69, 192, 48)

// 轮询 直到进入比赛
inx = 0
While True
	
	For Each val In hwndArr
		If val = "" Then 
		Else 
			isFuben (val)
			If isFubened Then 
				// 在副本了 开始打
				//say (val & "，已经在竞技 开始攻击")
				If inx > 3 Then 
					Call Plugin.Bkgnd.KeyPress(val, 68)
					Delay 100
					Call Plugin.Bkgnd.KeyPress(val, 68)
					Delay 100
					Call Plugin.Bkgnd.KeyPress(val, 101)
					Delay 100
				Else 
					Call Plugin.Bkgnd.KeyPress(val, 87)
					Delay 100
					Call Plugin.Bkgnd.KeyPress(val, 87)
					Delay 100
				End If

				Call Plugin.Bkgnd.KeyPress(val, 9)
				Delay 100
				Call Plugin.Bkgnd.KeyPress(val, 9)
				Delay 100
				Call Plugin.Bkgnd.KeyPress(val, attackArr(inx))
				Delay 3000
			Else 
				// 排队检测
				isQueueUp (val)
				If False = isQueueUpEd Then 
					//say(val & "，没在竞技 开始排队")
					queueUp(val)
				End If
			End If
			
		End If
	Next
	inx = inx + 1
	If inx = 5 Then 
		inx = 0
	End If
Wend








