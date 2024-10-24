use druid::widget::{Button, Flex, TextBox, Either};
use druid::{AppLauncher, Data, Lens, Widget, WidgetExt, WindowDesc, Color};
use windows::Win32::Foundation::{HWND, LPARAM, BOOL, WPARAM};
use windows::Win32::UI::WindowsAndMessaging::{PostMessageW, EnumWindows, GetWindowTextW, WM_KEYDOWN, WM_KEYUP};
use std::ffi::{CString, OsString};
use std::os::windows::ffi::OsStringExt;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;
use std::time::Duration;
use windows::Win32::UI::Input::KeyboardAndMouse::{SendInput, INPUT, INPUT_0, INPUT_KEYBOARD, VIRTUAL_KEY, KEYBDINPUT,KEYBD_EVENT_FLAGS,VK_F8, KEYEVENTF_KEYUP, KEYEVENTF_SCANCODE, VK_CONTROL,VK_E, VkKeyScanW};
#[derive(Clone, Data, Lens)]
struct AppState {
    input: String,
    f8_active: bool,
}

// 定义一个全局的 AtomicBool 变量，用于控制循环是否继续
static GLOBAL_LOOP_FLAG: AtomicBool = AtomicBool::new(false);

fn main() {
    // 创建一个窗口描述
    let main_window = WindowDesc::new(build_ui())
        .title("刀剑2群控助手")
        .window_size((640.0, 480.0));

    // 启动应用程序
    AppLauncher::with_window(main_window)
        .launch(AppState {
            input: "夏禹剑 - 刀剑2".into(),
            f8_active: false,
        })
        .expect("Failed to launch application");
}

// 构建 UI
fn build_ui() -> impl Widget<AppState> {
    let textbox = TextBox::new()
        .with_placeholder("窗口标题")
        .lens(AppState::input);

    // 定义白色背景按钮
    let white_button = Button::new("全体自动拾取(F8)-关闭")
        .on_click(|_ctx, data: &mut AppState, _env| {
            data.f8_active = !data.f8_active;  // 切换按钮状态
            // 启动/停止后台循环
            if data.f8_active {
                GLOBAL_LOOP_FLAG.store(true, Ordering::SeqCst);  // 设置为 true 开始循环
                start_f8_task(data.input.clone());
            } else {
                GLOBAL_LOOP_FLAG.store(false, Ordering::SeqCst);  // 设置为 false 停止循环
            }
        })
        .background(Color::WHITE);

    // 定义红色背景按钮
    let red_button = Button::new("全体自动拾取(F8)-已开启")
        .on_click(|_ctx, data: &mut AppState, _env| {
            data.f8_active = !data.f8_active;  // 切换按钮状态
            // 启动/停止后台循环
            if data.f8_active {
                GLOBAL_LOOP_FLAG.store(true, Ordering::SeqCst);  // 设置为 true 开始循环
                start_f8_task(data.input.clone());
            } else {
                GLOBAL_LOOP_FLAG.store(false, Ordering::SeqCst);  // 设置为 false 停止循环
            }
        })
        .background(Color::RED);

    // 使用 Either 控件，根据 `is_active` 显示不同背景颜色的按钮
    let button = Either::new(
        |data: &AppState, _env| data.f8_active,  // 判断按钮是否处于激活状态
        red_button,
        white_button,
    );

    Flex::column()
        .with_child(textbox)
        .with_spacer(8.0)
        .with_child(button)

}

// 启动后台任务，定时发送 F8 按键
fn start_f8_task(window_title: String) {
    thread::spawn(move || {
        while GLOBAL_LOOP_FLAG.load(Ordering::SeqCst) {
            // 每 1 秒发送一次 F8
            send_key_to_window(&window_title);
            thread::sleep(Duration::from_millis(100));
        }
    });
}

// 枚举窗口的回调函数
unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: LPARAM) -> BOOL {
    let mut title: [u16; 512] = [0; 512];
    let length = GetWindowTextW(hwnd, &mut title);

    if length > 0 {
        let window_title = OsString::from_wide(&title[..length as usize]);
        let window_title_str = window_title.to_string_lossy();

        // 获取目标窗口标题
        let target_title = std::ffi::CStr::from_ptr(lparam.0 as *const i8)
            .to_str()
            .unwrap();
        // println!("enum_windows_proc.target_title={}", target_title);

        // 匹配窗口标题
        if window_title_str.contains(target_title) {
            println!("Found target window: {:?}", window_title_str);

            send_f8(hwnd);  // 发送 F8 键

            return BOOL(0); // 停止枚举
        }
    }

    BOOL(1) // 继续枚举其他窗口
}

// 使用 PostMessageW 发送 F8 按键
unsafe fn send_f8(hwnd: HWND) {
    PostMessageW(hwnd, WM_KEYDOWN, WPARAM(VK_F8.0 as usize), LPARAM(0));
    PostMessageW(hwnd, WM_KEYUP, WPARAM(VK_F8.0 as usize), LPARAM(0));
}

// 发送 F8 按键到指定窗口
fn send_key_to_window(window_title: &str) {
    unsafe {
        let target_title = CString::new(window_title).unwrap();
        EnumWindows(Some(enum_windows_proc), LPARAM(target_title.as_ptr() as isize));
    }
}
