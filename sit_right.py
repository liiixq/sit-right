"""桌面定时弹幕：别跷二郎腿提醒。
运行：python sit_right.py
退出：右键系统托盘图标 → 退出。
"""

import random
import threading
import time
import tkinter as tk

from PIL import Image, ImageDraw, ImageFont
import pystray

# ===== 配置 =====
INTERVAL_MINUTES = 15         # 每隔多少分钟提醒一次
DANMAKU_DURATION = 10         # 提醒在屏幕上悬浮多少秒
FONT_FAMILY = "Microsoft YaHei"
FONT_SIZE = 58
SHOW_ON_START = True         # 启动时立刻演示一次

MESSAGES = [
    "别跷二郎腿！",
    "坐直",
    "二郎腿放下，保护脊柱",
    "当心脊柱侧弯~",
    "双脚踩地，骨盆放平",
    "你又跷二郎腿了！",
    "现在！把腿放下！",
]

COLORS = ["#FF3B30", "#FF9500", "#FFCC00", "#34C759",
          "#5AC8FA", "#AF52DE", "#FF2D55"]
# ==================


# 全局暂停标志，托盘菜单可切换
PAUSED = False


def show_one(root):
    """在屏幕随机位置悬浮显示一条提醒，停留 DANMAKU_DURATION 秒后消失。"""
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    text = random.choice(MESSAGES)
    color = random.choice(COLORS)

    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.attributes("-transparentcolor", "white")
    win.config(bg="white")

    label = tk.Label(
        win, text=text, fg=color, bg="white",
        font=(FONT_FAMILY, FONT_SIZE, "bold"),
    )
    label.pack()
    win.update_idletasks()
    text_w = label.winfo_reqwidth()
    text_h = label.winfo_reqheight()

    x = (screen_w - text_w) // 2
    y = int(screen_h * 0.2)
    win.geometry(f"{text_w}x{text_h}+{x}+{y}")

    win.after(DANMAKU_DURATION * 1000, win.destroy)


def scheduler(root):
    """后台线程：定时触发提醒，PAUSED 时跳过。"""
    def loop():
        while True:
            time.sleep(INTERVAL_MINUTES * 60)
            if not PAUSED:
                root.after(0, show_one, root)
    threading.Thread(target=loop, daemon=True).start()


def make_tray_icon():
    """生成托盘图标：橙底白色"坐"字。"""
    img = Image.new("RGBA", (64, 64), (255, 149, 0, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("msyh.ttc", 44)
    except OSError:
        font = ImageFont.load_default()
    # 居中绘制"坐"字
    bbox = draw.textbbox((0, 0), "坐", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((64 - tw) / 2 - bbox[0], (64 - th) / 2 - bbox[1]),
              "坐", fill="white", font=font)
    return img


def setup_tray(root):
    """创建系统托盘图标，挂载菜单。托盘运行在自己的线程。"""
    def toggle_pause(icon, item):
        global PAUSED
        PAUSED = not PAUSED
        icon.update_menu()

    def remind_now(icon, item):
        root.after(0, show_one, root)

    def quit_app(icon, item):
        icon.stop()
        root.after(0, root.quit)

    menu = pystray.Menu(
        pystray.MenuItem(
            lambda item: "继续提醒" if PAUSED else "暂停提醒",
            toggle_pause,
        ),
        pystray.MenuItem("立即提醒一次", remind_now),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", quit_app),
    )
    icon = pystray.Icon("sit-right", make_tray_icon(), "别跷二郎腿", menu)
    threading.Thread(target=icon.run, daemon=True).start()


def main():
    root = tk.Tk()
    root.withdraw()
    if SHOW_ON_START:
        root.after(500, show_one, root)
    scheduler(root)
    setup_tray(root)
    root.mainloop()


if __name__ == "__main__":
    main()
