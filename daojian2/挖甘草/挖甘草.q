Hwnd = Plugin.Window.Find("pg_gui_window_default_class[13680]", "夏禹剑 - 刀剑2")
Delay 1000

// 聊天切换到队伍模式，防止识图到拾取记录

UserVar counter=0 "挖次数"
UserVar maxGather=180 "总挖次数"

// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

// 导航所在
UserVar navigationX =2358 "导航所在"
UserVar navigationY =1267 "导航所在"

UserVar isCollect = False "为 True 则捡过东西"

// 上马
Function mountHorse(tag)
	isCollect = False
	Delay 300
	MoveTo 1357, 1304
	Delay 20
	LeftClick 1
	Delay 5000
End Function

// 采集
Function gather(tag)
	//KeyPress "Num 5", 1
	//KeyPress "Num 2", 3
	//KeyPress "Num 4", 5// 左旋
	Delay 300
	k=0
	j=0
	i= 0
	While i < 10
		Delay 150
    	FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\gancao.bmp", 0.5, intX, intY
		//FindPic 0, 0, 2560, 1440, "C:\Users\Administrator\Documents\dao2\dahuang.bmp", 0.5, intX, intY
		
		If intX > 0 And intY > 0 Then 
			MoveTo intX + 20, intY + 50
			TracePrint "找到图形，鼠标已经移到图形上面"
			//MessageBox "找到图形，鼠标已经移到图形上面"
			say("挖" & counter)
			Delay 50
			LeftClick 1
			Delay 100
			MoveTo 100, 100
			Delay 5200
			counter = counter + 1
			// 换锄头
			If counter = 50 Then 
				KeyPress "1", 1
			End If
			If counter = 100 Then 
				KeyPress "2", 1
			End If
			isCollect = True
		Else 
			//MessageBox "未找到图形"
			j= j+1
			TracePrint "未找到图形"
			If j < 3 Then  
				//KeyPress "Num 8", 1// 降低摄像头
				//Delay 50
				KeyPress "Num 4", 1
				k=k+1
			End If
			Delay 300
			i = i+1
		End If
	Wend
	
	For k
		say("摄像头归位" & k)
		Delay 50
		KeyPress "Num 6", 1
	Next

End Function

// 土遁去碎木
Function gotoSuiMu(tag)
	Delay 20
	MoveTo 1407, 1295
	LeftClick 1
	Delay 20
	MoveTo 1250, 902
	LeftClick 1
	Delay 20
	MoveTo 1392, 953
	LeftClick 1
	Delay 20
	MoveTo 1199, 756
	LeftClick 1
	Delay 6000
	KeyPress "W", 1
	Delay 1000
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
	Delay 30
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


// 打开
openNavigation (0)


While counter < maxGather

	KeyPress "Ctrl", 1

    // 前往第一点
	gotoLocation ("646,848")
	Delay 13000
	gather (0)
	
	
	// 前往第二点
	gotoLocation ("641,941")
	Delay 14000
	gather (0)
	
	// 前往第三点
	gotoLocation ("646,963")
	Delay 14000
	gather (0)
	
	// 前往第4点
	gotoLocation ("687,1054")
	Delay 28000
	gather (0)
	
	// 前往第5点
	KeyPress "Ctrl", 1
	gotoLocation ("792,1053")
	Delay 22000
	gather (0)
	
	//去碎木
	gotoSuiMu(0)
Wend

MessageBox "脚本结束"