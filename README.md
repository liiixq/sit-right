# sit-right

桌面小工具：每隔 N 分钟在屏幕顶部居中悬浮一条提醒，督促你**别跷二郎腿**，避免长时间不良坐姿带来的脊柱侧弯。

仅 Windows，单文件 exe，双击即用。

---

## 功能

- **定时悬浮提醒**：屏幕水平居中、垂直靠上，停留几秒自动消失，不打断手头工作
- **随机文案与颜色**：从一组提示语和颜色中随机挑选，避免视觉疲劳
- **系统托盘控制**：右键托盘图标可暂停 / 继续 / 立即提醒 / 退出
- **轻量**：运行时约 7 MB 内存，无网络通信，无后台数据采集

## 快速开始（普通用户）

1. 在仓库 [Code](https://github.com/liiixq/sit-right) 页面进入 `dist/`，下载 `sit-right.exe`
   - 或克隆仓库后到本地 `dist\sit-right.exe`
2. 把 `sit-right.exe` 放到桌面或任意目录，双击运行
3. 启动后会立即在屏幕顶部演示一条提醒，之后按默认间隔（**1 分钟**）循环
4. 系统通知区会出现一个橙色「坐」字图标，右键可控制

> 不依赖 Python 环境，对方电脑装 Win10/Win11 即可。

### 托盘菜单

| 菜单项 | 作用 |
|---|---|
| 暂停提醒 / 继续提醒 | 临时停用定时提醒（菜单文字会切换） |
| 立即提醒一次 | 不等定时器，马上弹一条 |
| 退出 | 干净关闭程序 |

## 自定义配置

打开 `sit_right.py` 顶部「配置区」修改：

```python
INTERVAL_MINUTES = 1         # 每隔多少分钟提醒一次
DANMAKU_DURATION = 5         # 提醒在屏幕上悬浮多少秒
FONT_FAMILY = "Microsoft YaHei"
FONT_SIZE = 42
SHOW_ON_START = True         # 启动时立刻演示一次

MESSAGES = [
    "别跷二郎腿！",
    "坐直",
    "二郎腿放下，保护脊柱",
    # ...
]

COLORS = ["#FF3B30", "#FF9500", "#FFCC00", "#34C759", "#5AC8FA", "#AF52DE", "#FF2D55"]
```

改完保存后双击 `build.bat` 重新打包，新 exe 在 `dist\sit-right.exe`。

## 从源码运行（开发者）

需要 Python 3.9+。

```powershell
pip install pystray Pillow
python sit_right.py
```

## 重新打包成 exe

双击仓库根目录的 `build.bat` 即可。脚本会：

1. 在 `.venv\` 创建（或复用）干净的虚拟环境，避免 Anaconda 等环境牵连大库
2. 安装 `pystray`、`Pillow`、`pyinstaller==5.13.2`
3. 用 PyInstaller 打成单文件 `dist\sit-right.exe`（约 16-17 MB）

> 已经跑过一次后，再次打包大约 1-2 分钟。

**注意**：旧的 `sit-right.exe` 如果还在运行，先从托盘退出，否则文件被占用会覆盖失败。

## 技术栈

| 模块 | 用途 |
|---|---|
| `tkinter` | 创建无边框、透明背景、置顶的弹幕窗口 |
| `pystray` + `Pillow` | 系统托盘图标和菜单 |
| `threading` | 后台定时器线程 |
| `PyInstaller` | 打包成单文件 exe |

## 已知限制

- **仅 Windows**：依赖 tkinter 的 `-transparentcolor` 属性，仅在 Windows 下生效
- **没有点击穿透**：弹幕停留期间会拦截鼠标点击，悬浮区域较小且时间短一般无感
- **退出仅靠托盘**：`--noconsole` 模式无控制台窗口，请通过托盘菜单退出

## 许可证

MIT
