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
MacroID=343b421c-d486-45a2-8f8c-8067d546b435
Description=ʶͼ
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
// ��Ļ�ֱ��ʲ���
UserVar screenWidth=2560 "��Ļ����"
UserVar screenHight=1440 "��Ļ�߶�"

// ͼƬ��Դ·��
UserVar imageBaseUri = "C:\Users\Administrator\Documents\dao2\" "ͼƬ·��"

//FindPic 0, 0, screenWidth, screenHight, "C:\Users\Administrator\Documents\dao2\zhanchangpaidui.bmp", 0.7, intX, intY
FindPic 100, 100, screenWidth, screenHight, imageBaseUri & "jiedanmojiufeng.bmp", 0.7, intX, intY

If intX > 0 And intY > 0 Then 
	MoveTo intX+10, intY+10
	TracePrint "�ҵ�ͼ�Σ�����Ѿ��Ƶ�ͼ������"
	Delay 20
Else 
	TracePrint "δ�ҵ�ͼ��"
End If

//MouseWheel -2

/*
Hwnd = Plugin.Window.Find("pg_gui_window_default_class[7536]", "������ - ����2")

TracePrint "Hwnd=" &Hwnd

Call Plugin.Window.Active(Hwnd)

Delay 500

*/


/*
KeyDown "Alt", 1
KeyPress "Tab", 1
KeyUp "Alt", 1
*/





// ���д���
/*
HwndEx  = Plugin.Window.Search("������ - ����2")
hwndArr = Split(HwndEx, "|")


For Each val In hwndArr
If val = "" Then 
Else 
	Call Plugin.Window.Active(Clng(val))
	Delay 1000
	TracePrint "hwnd=" & val
End If
Next
*/


