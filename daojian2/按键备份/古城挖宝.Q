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
MacroID=2ab7b1e3-91ca-4ac4-b07c-f3519ef88fb3
Description=古城挖宝
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
Hwnd = Plugin.Window.Find("pg_gui_window_default_class[13680]", "夏禹剑 - 刀剑2")
Delay 1000

UserVar counter=0 "次数"

// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

// 导航所在
UserVar navigationX =2358 "导航所在"
UserVar navigationY =1267 "导航所在"

UserVar isCollect = False "为 True 则捡过东西"

UserVar diedCount = 0 "死亡次数"
UserVar eatCount = 0 "吃卷次数"
UserVar storageCount = 0 "存库次数"

// 土遁去瓦当
Function gotoWaDang(tag)
	Delay 20
	MoveTo 1407, 1295
	LeftClick 1
	Delay 20
	MoveTo 1277, 482
	LeftClick 1
	Delay 20
	MoveTo 1384, 952
	LeftClick 1
	Delay 20
	MoveTo 1199, 756
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
End Function

// 导航输入框,输入坐标寻路
Function gotoLocation(xy)
	say("去:" & xy & "，自动组队已开启，捡卷。开源 github eatCount=" & eatCount & ",diedCount=" & diedCount & ",storageCount=" & storageCount)
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

// 上马
Function mountHorse(tag)
	Delay 300
	MoveTo 1357, 1304
	Delay 20
	LeftClick 1
	Delay 5000
End Function

UserVar isGuCheng = False "是否进古城"

Function intoGuCheng(tag)
	isGuCheng = False
	KeyPress "Num 5", 1
	Delay 400
	For i=1 To 6
		FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\banghuishizhe.bmp", 0.5, intX, intY
		If intX > 0 And intY > 0 Then 
			MoveTo intX, intY
			TracePrint "intoGuCheng 找到图形，鼠标已经移到图形上面"
			Delay 20
			LeftClick 1
			Delay 500
			MoveTo 1188, 1222
			Delay 20
			LeftClick 1
			Delay 4000
			formTeam (0)
			isGuCheng = True
			Exit For
		Else 
			TracePrint "intoGuCheng 未找到图形"
			isGuCheng = False
			KeyPress "Num 4", 1
			Delay 500
		End If
	Next
End Function


// 挖宝
Function miner(tag)
	// 挖
	KeyPress "5", 1
	Delay 11000
	// 攻击宝箱
	KeyPress "4", 1
	Delay 3000
	
	// 拾取
	For 35
		KeyPress 119, 1
		Delay 300
	Next
	resurrection(0)
End Function

// 组队
Function formTeam(tag)
	Delay 20
	MoveTo 1084, 1360
	Delay 20
	LeftClick 1
	Delay 50
	LeftClick 1
	MoveTo 1119, 1251
	Delay 50
	LeftClick 1
End Function

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
			Delay 30
			RightClick 5
			
			j = j+1
		Wend
		i = i+1
	Wend
	Delay 100
	// 吃第二背包的
	i = 0
	While i < 8
		j = 0
		While j < 4
			x = 2195 + i * 48
			y = 295 + j * 48
			MoveTo x, y
			Delay 30
			RightClick 5
			
			j = j+1
		Wend
		i = i+1
	Wend
	Delay 100

	KeyPress "B", 1
	eatCount = eatCount + 1
	Delay 100
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
		gotoWaDang (0)
		Goto begin
	Else 
		TracePrint "resurrection 未找到图形"
	End If

End Function

Function save(tag)
	Delay 200
	// 双循环遍历32个格子
	i = 0
	While i < 8
		j = 0
		While j < 4
			x = 2195 + i * 48
			y = 70 + j * 48
			MoveTo x, y
			Delay 30
			// 凝神宝袋的处理
			delNinShenBaoDai(0)
			
			RightClick 1
			Delay 300
			
			FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\quanbucunru.bmp", 0.6, intX, intY

			If intX > 0 And intY > 0 Then 
				TracePrint "save 找到图形 需要点击确定"
				Delay 20
				MoveTo 1201, 755
				Delay 50
				LeftClick 1
				Delay 50
			Else 
				TracePrint "未找到图形"
			End If
			
			j = j+1
		Wend
		i = i+1
	Wend
	Delay 100
End Function

// 存仓库
Function storage(tag)
	gotoLocation ("612,468")
	Delay 21000
	KeyPress "Num 5", 1
	Delay 300
	storageCount = storageCount +1
	For i=1 To 10
		FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\cangku.bmp", 0.6, intX, intY
		If intX > 0 And intY > 0 Then 
			MoveTo intX, intY
			TracePrint "storage 找到图形，鼠标已经移到图形上面"
			Delay 20
			LeftClick 1
			Delay 500
			MoveTo 892, 1178
			Delay 20
			LeftClick 1
			Delay 1500
			// 存卷子
			save(0)
			Exit For
		Else 
			TracePrint "intoGuCheng 未找到图形"
			isGuCheng = False
			KeyPress "Num 6", 1
			Delay 300
		End If
	Next
		
End Function

// 删除凝神宝袋
Function delNinShenBaoDai(tag)
	Delay 200
	FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\ningshenbaodai.bmp", 0.6, intX, intY
	
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
	Else 
		TracePrint "未找到图形"
	End If
	
End Function

pointArray1 = Array("956,627", "999,633", "1030,643")
pointArray2 = Array("940,686", "952,720", "917,733", "889,725")
waitArray1 = Array(3000, 3000, 5000)
waitArray2 = Array(3000, 5000, 4000, 5000)

Rem begin

// 打开
openNavigation (0)
Delay 300

Rem begin2

// 帮会使者
gotoLocation ("675,519")
mountHorse(0)
Delay 18000

intoGuCheng(0)

If False = isGuCheng Then 
	TracePrint "未找到古城"
	KeyPress "Esc", 1
	gotoWaDang (0)
	Goto begin
End If

Rem startFound


// 已经到古城,开始
If counter < 2 Then 
	// 第一个路线
	inx = 0
	For Each val In pointArray1
		gotoLocation (val)
		Delay waitArray1(inx)
		inx = inx + 1
		counter = counter + 1
		miner(0)
	Next
Else 
	// 第二个路线
	inx = 0
	For Each val In pointArray2
		gotoLocation (val)
		Delay waitArray2(inx)
		inx = inx + 1
		counter = counter + 1
		miner(0)
	Next
	// 第二路线完成 重置计数器
	counter = 0
End If

gotoWaDang (0)

// 存仓库
storage(0)


Goto begin2

MessageBox "脚本结束"
