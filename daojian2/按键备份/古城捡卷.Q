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
MacroID=d360edeb-9a1e-4dae-9304-7ca2dd341031
Description=古城捡卷
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
Hwnd = Plugin.Window.Find("pg_gui_window_default_class[13680]", "夏禹剑 - 刀剑2")
Delay 1000

UserVar counter=0 "次数"
UserVar maxGather=8 "总次数"

// 屏幕分辨率参数
UserVar screenWidth=2560 "屏幕宽度"
UserVar screenHight=1440 "屏幕高度"

// 导航所在
UserVar navigationX =2358 "导航所在"
UserVar navigationY =1267 "导航所在"

UserVar tuDunX = 1407 "土遁所在 X "
UserVar tuDunY = 1295 "土遁所在 Y "

// 瓦当
UserVar waDangX = 1277 "瓦当 X"
UserVar waDangY = 482 "瓦当 Y"

// 朝歌
UserVar zgX = 1255 "朝歌 X"
UserVar zgY = 521 "朝歌 Y"


// 琼云
UserVar tuDunQionYunX = 1243 "琼云 X"
UserVar tuDunQionYunY = 591 "琼云 Y"


UserVar tuDunChuFaX = 1384 "土遁出发 X"
UserVar tuDunChuFaY = 952 "土遁出发 Y"


UserVar tuDunOkX = 1199 "土遁确定 X"
UserVar tuDunOkY = 756 "土遁确定 Y"

UserVar bangShouX = 983 "挑战时的帮手 X"
UserVar bangShouY = 610 "挑战时的帮手 Y"


// 图片资源路径
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "图片路径"


UserVar isCollect = False "为 True 则捡过东西"

UserVar diedCount = 0 "死亡次数"
UserVar eatCount = 0 "吃卷次数"
UserVar storageCount = 0 "存库次数"


UserVar isStorage = False "是否存过仓库"

// 土遁去瓦当
Function gotoWaDang(tag)
	Delay 20
	MoveTo tuDunX, tuDunY
	LeftClick 1
	Delay 200
	MoveTo waDangX, waDangY
	LeftClick 1
	Delay 200
	MoveTo tuDunChuFaX, tuDunChuFaY
	LeftClick 1
	Delay 200
	MoveTo tuDunOkX, tuDunOkY
	LeftClick 1
	Delay 8000
	KeyPress "W", 2
	Delay 1500
End Function

Function gotoQionYun(tag)
	Delay 20
	MoveTo tuDunX, tuDunY
	LeftClick 1
	Delay 200
	MoveTo tuDunQionYunX, tuDunQionYunY
	LeftClick 1
	Delay 200
	MoveTo tuDunChuFaX, tuDunChuFaY
	LeftClick 1
	Delay 200
	MoveTo tuDunOkX, tuDunOkY
	LeftClick 1
	Delay 8000
	KeyPress "W", 2
	Delay 1500
End Function


// 打开导航
Function openNavigation(tag)
	Delay 20
	MoveTo navigationX,navigationY
	Delay 20
	LeftClick 1
End Function

// 找指定NPC ，通过 导航功能
Function gotoNPC(name)
	say("去:" & name & "，捡卷。,storageCount=" & storageCount)
	Delay 100
	MoveTo 2407, 1143
	Delay 100
	LeftClick 1
	
	// 删除坐标
	Delay 100
	KeyPress "BackSpace", 20
	
	
	// 输入NPC
	//SayString name
	//Delay 100
	
	// 点击导航
	//MoveTo 2240, 1147
	//Delay 100
	//LeftClick 1
	
	
	// 找 NPC，鼠标滚轮在导航下移动，不断识图
	MoveTo 2464, 1092
	Delay 100
	
	isOk = True
	While isOk
		Delay 300
		FindPic 1000, 800, screenWidth, screenHight, imageBaseUri & "nav_" & name & ".bmp", 0.7, intX, intY
		If intX > 0 And intY > 0 Then 
			MoveTo intX, intY
			TracePrint "gotoNPC 找到图形，" & name
			Delay 100
			LeftClick 1
			isOk = False			
		Else 
			TracePrint "gotoNPC 未找到图形" & name
			// 鼠标滚轮往下滚
			MouseWheel -1
			Delay 200
		End If
	Wend

		
End Function

// 导航输入框,输入坐标寻路
Function gotoLocation(xy)
	say("去:" & xy & "，捡卷。开源 github counter=" & counter & ",diedCount=" & diedCount & ",storageCount=" & storageCount)
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
	Delay 6000
End Function


UserVar isGuCheng = False "是否进古城"
// 异世界 地图，通过右下角小地图 判断
Function yiDiTu(tag)
	Delay 300
	FindPic 800, 600, screenWidth, screenHight, imageBaseUri & "yiditu.bmp", 0.7, intX, intY
	
	If intX > 0 And intY > 0 Then 
		MoveTo intX, intY
		//TracePrint "yiDiTu 找到图形，鼠标已经移到图形上面"
		say("yiDiTu 找到图形，鼠标已经移到图形上面")
		Delay 20
		isGuCheng = True
	Else 
		TracePrint "未找到图形"
		isGuCheng = False
	End If	
	
End Function

Function intoGuCheng(tag)
	isGuCheng = False
	KeyPress "Num 5", 1
	Delay 500
	For i=1 To 15
		FindPic 200, 200, screenWidth - 200, screenHight-300, imageBaseUri & "banghuishizhe.bmp", 0.5, intX, intY
		If intX > 0 And intY > 0 Then 
			Delay 200
			MoveTo intX+5, intY+5
			TracePrint "intoGuCheng 找到图形，鼠标已经移到图形上面"
			Delay 200
			LeftClick 1
			Delay 2000
			MoveTo 1188, 1222
			Delay 500
			LeftClick 1
			Delay 5000
			yiDiTu(0)
			formTeam (0)
			
			Exit For
		Else 
			TracePrint "intoGuCheng 未找到图形"
			If i = 6 Then 
				KeyPress "D", 1
				Delay 200
				KeyPress "W", 1
				Delay 200
				KeyPress "Num 5", 1
				Delay 400
			End If
			isGuCheng = False
			KeyPress "Num 4", 1
			Delay 1000
		End If
	Next
End Function

// 拾取
Function collect(count)
	isFinish = True
	i = 0
	While isFinish
		For 10
			KeyPress 119, 1
			Delay 250
		Next
		
		resurrection(0)
		
		FindPic 200,500, screenWidth, screenHight, imageBaseUri & "jindu.bmp", 0.6, intX, intY
		If intX > 0 And intY > 0 Then 
			//MoveTo intX, intY
			TracePrint "collect 找到图形"
			counter = counter + 1
			//say ("拾取" & counter & ",重置基数i=" & i)
			i = 0
			Delay 13500
			isCollect = true
		Else 
			TracePrint "未找到图形"
			i= i+1
		End If
		
		If i = count Then 
			isFinish = False
		End If
	Wend

	
End Function

// 组队
Function formTeam(tag)
	Delay 100
	MoveTo 1084, 1360
	Delay 100
	LeftClick 1
	Delay 100
	LeftClick 1
	MoveTo 1119, 1251
	Delay 100
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

// 卷子捡够了回
Function isFull(tag)
	If counter > maxGather Then 
		Goto fullTag
	End If
End Function

UserVar isDied = False "死亡"
// 如果死亡 就复活重新来过
Function resurrection(tag)
	//say("resurrection 复活检测")
	Delay 300
	FindPic 300, 200, screenWidth, screenHight, imageBaseUri & "huangquanzhilu.bmp", 0.6, intX, intY
	If intX > 0 And intY > 0 Then 
		diedCount = diedCount + 1
		say ("检测到死亡，白忙活了...复活...diedCount=" & diedCount)
		Delay 300
		MoveTo intX, intY
		TracePrint "resurrection 找到图形，鼠标已经移到图形上面"
		Delay 100
		LeftClick 1
		Delay 7000
		KeyPress "W", 2
		Delay 1000
		KeyPress "Esc", 1
		Delay 1000
		gotoWaDang (0)
		isDied = True
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
			RightClick 1
			Delay 300
			
			FindPic 500, 200, screenWidth, screenHight, imageBaseUri & "quanbucunru.bmp", 0.6, intX, intY

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
	//gotoLocation ("612,468")
	gotoNPC("wodecangku")
	
	Delay 20000
	KeyPress "Num 5", 1
	Delay 300
	storageCount = storageCount +1
	For i=1 To 35
		//FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\cangku.bmp", 0.6, intX, intY
		// 找钱庄2字
		FindPic 300, 600, screenWidth, screenHight, imageBaseUri & "qianzhuang.bmp", 0.7, intX, intY
		If intX > 0 And intY > 0 Then 
			MoveTo intX, intY
			TracePrint "storage 找到图形，鼠标已经移到图形上面"
			Delay 100
			// 点击钱庄
			LeftClick 1
			Delay 1500
			// 存卷子
			save(0)
			Exit For
		Else 
			TracePrint "storage 未找到图形"
			isGuCheng = False
			If i = 10 Then 
				KeyPress "A", 1
				Delay 500
				KeyPress "Num 5", 1
				Delay 300
			End If
			If i = 20 Then 
				KeyPress "D", 1
				Delay 500
				KeyPress "Num 5", 1
				Delay 300
			End If
			KeyPress "Num 6", 1
			Delay 500
		End If
	Next
		
End Function


pointArray = Array("1005,647","1049,656", "959,626", "950,653", "952,704", "966,761", "823,735", "895,759", "818,771", "884,833","1020,788", "1047,896", "1110,913", "1024,944", "1059,991", "986,987", "989,931", "979,864", "1010,812", "941,801", "903,772","909,722", "932,684")
collectArray = Array(2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1,1, 1)

isStorage = False


gotoWaDang (0)

Rem begin


// 打开
openNavigation (0)
Delay 300

Rem begin2

counter = 0
isCollect = False

TracePrint "isStorage =" & isStorage
// 帮会使者
gotoLocation ("675,519")
If False = isStorage Then 
	mountHorse (0)
	isStorage = False
ElseIf isDied Then
	isDied = False
	mountHorse (0)
End If

Delay 12000
resurrection(tag)

intoGuCheng (0)
resurrection(tag)

If False = isGuCheng Then 
	TracePrint "未找到古城"
	KeyPress "Esc", 1
	gotoWaDang (0)
	resurrection(tag)
	Goto begin
End If

Rem startFound

// 已经到古城,开始
UserVar inx = 0 "下标"
For Each val In pointArray
	gotoLocation (val)
	If isCollect Then 
		isCollect = False
		mountHorse (0)
	End If
	collect (collectArray(inx))
	isFull (0)
	inx = inx+1
Next


If counter < maxGather Then 
	Goto startFound
End If

// 捡足够数量 回瓦当仓库
Rem fullTag

gotoWaDang (0)

// 吃卷子
//eatReel (0)
//Delay 2000
//Goto begin

// 存仓库
isStorage = True
storage(0)

Goto begin2

MessageBox "脚本结束"
