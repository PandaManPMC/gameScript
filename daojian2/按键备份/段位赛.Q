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

/******** 注意，在开启脚本前，要用 ALT + TAB  把所有刀2的游戏窗口切换一遍，否则 Active 无法激活窗口，无法识图正常排队和战斗。
********* 开启脚本后，会频繁切窗口识图。开多少个号就会切多少排多少
*/


// 所有窗口 
HwndEx  = Plugin.Window.Search("夏禹剑 - 刀剑2")
hwndArr = Split(HwndEx, "|")

length = UBound(hwndArr)

say("读取到刀2句柄数量=" & length)


// 需要根据不同电脑环境修改的参数 ----------------------  begin

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

// -------------------------------------------------------------



// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"


// 技能快捷键 x v r e ` 0
attackArr = Array(88, 86, 82, 69, 192, 48)

// 切窗口识图延迟，电脑反应慢的，需要适量增加
tabWindowDelay = 300

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
	Delay 100
	//For i = 1 To 3
		//iCoord = Plugin.Bkgnd.FindPic(hwnd,0,0,1024,768, imageBaseUri & "tuichufuben.bmp",  0, 0.7)   
		//XY = Split(iCoord, "|")
		//intX = XY(0)
		//intY = XY(1)
		
		// 激活窗口 识图
		tabWindow(hwnd)
		Delay tabWindowDelay
		FindPic 600, 600, screenWidth, screenHight, imageBaseUri & "tuichufuben.bmp", 0.7, intX, intY
		
		
		If intX > 0 And intY > 0 Then 
			TracePrint hwnd & "isFuben 找到图形，鼠标已经移到图形上面"
			say(hwnd & "isFuben 检测到正在副本")
			Delay 20
			isFubened = True
			Exit Function
		Else 
			TracePrint hwnd & "isFuben 未找到图形"
			Delay 20
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
	//Delay 100
	
	//iCoord = Plugin.Bkgnd.FindPic(hwnd,0,0,1024,768, imageBaseUri & "zhanchangpaidui.bmp",  0, 0.7)   
	//XY = Split(iCoord, "|")
	//intX = XY(0)
	//intY = XY(1)
	
	// 激活窗口 识图
	tabWindow(hwnd)
	Delay tabWindowDelay

	FindPic 600, 600, screenWidth, screenHight, imageBaseUri & "zhanchangpaidui.bmp", 0.7, intX, intY
	
	
	If intX > 0 And intY > 0 Then 
		TracePrint hwnd & "isQueueUp 找到图形"
		say(hwnd & "isQueueUp 检测到正在排队")
		Delay 20
		isQueueUpEd = True
		Exit Function
	Else 
		TracePrint hwnd & "isQueueUp 未找到图形"
		Delay 100
		isQueueUpEd = False
	End If

End Function


// 全部开始排队
For Each val In hwndArr
	queueUp(val)
Next


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
				Call Plugin.Bkgnd.KeyPress(val, 101)// 摄像头归位
								
				If inx < 4 Then 
					Call Plugin.Bkgnd.KeyPress(val, 87)
					Delay 100
					Call Plugin.Bkgnd.KeyPress(val, 87)
					Delay 100
					Call Plugin.Bkgnd.KeyPress(val, 101)
					Delay 50
				End If

				Call Plugin.Bkgnd.KeyPress(val, 9)
				Delay 50
				Call Plugin.Bkgnd.KeyPress(val, 9)
				Delay 50
				Call Plugin.Bkgnd.KeyPress(val, attackArr(inx))
				Delay 50
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
	If inx = 6 Then 
		inx = 0
	End If
Wend








