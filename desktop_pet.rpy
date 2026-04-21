# ==============================================================================
# 🐾 桌宠模式 — Desktop Pet (Live2D)
#
# 进入后游戏窗口缩小为桌面右下角的小窗口
# 显示若叶睦的Live2D模型，可交互
#
# 【Live2D模型放置说明】
# 位置: game/live2d/mutsumi/
# 必需文件:
#   mutsumi.model3.json    — 模型主配置文件
#   mutsumi.moc3           — 模型数据
#   mutsumi.physics3.json  — 物理演算（头发摆动等）
#   textures/              — 贴图文件夹
#     texture_00.png       — 模型贴图
#   motions/               — 动作文件夹
#     idle.motion3.json    — 待机动作
#     tap.motion3.json     — 被点击动作
#     happy.motion3.json   — 开心动作
#     sad.motion3.json     — 难过动作
#     sleep.motion3.json   — 打瞌睡动作
#   expressions/           — 表情文件夹
#     normal.exp3.json     — 普通表情
#     smile.exp3.json      — 微笑
#     shy.exp3.json        — 害羞
#     angry.exp3.json      — 生气（墨缇斯）
#
# 命名规则: 主文件名必须和文件夹名一致（mutsumi）
# 格式: Cubism 4.x SDK 导出的标准 Live2D 格式
# ==============================================================================

# ── Live2D模型定义 ──
# 如果Live2D文件存在就加载，否则用占位图
init python:
    import os as _pet_os

    _PET_LIVE2D_PATH = "live2d/mutsumi/mutsumi.model3.json"
    _PET_HAS_LIVE2D = False

    def pet_check_live2d():
        """检查Live2D模型是否存在（支持WebGAL格式）"""
        global _PET_HAS_LIVE2D, _PET_LIVE2D_PATH
        try:
            # 尝试多种命名方式
            candidates = [
                "live2d/mutsumi/mutsumi.model3.json",
                "live2d/mutsumi/model.json",
                "live2d/mutsumi/mutsumi.model.json",
            ]
            for rel in candidates:
                full = _pet_os.path.join(config.gamedir, rel)
                if _pet_os.path.exists(full):
                    _PET_LIVE2D_PATH = rel
                    _PET_HAS_LIVE2D = True
                    return True
            _PET_HAS_LIVE2D = False
        except:
            _PET_HAS_LIVE2D = False
        return _PET_HAS_LIVE2D

init python:
    try:
        if pet_check_live2d():
            renpy.image("mutsumi_pet", Live2D(_PET_LIVE2D_PATH, zoom=0.5))
    except Exception as _pet_e:
        _PET_HAS_LIVE2D = False
        print("[Desktop Pet] Live2D load failed: " + str(_pet_e)[:80])

# ── 持久化变量 ──
default persistent.pet_affection_taps = 0
default persistent.pet_fed_today = ""
default _pet_mode = False
default _pet_dialogue = ""
default _pet_menu_open = False
default _pet_tools_open = False
default _pet_original_size = None

init python:
    import random as _pet_rng
    import datetime as _pet_dt
    import time as _pet_time

    # ══════════════════════════════════════════════════════════
    #  窗口管理
    # ══════════════════════════════════════════════════════════

    _PET_WINDOW_W = 320
    _PET_WINDOW_H = 480

    def pet_enter_desktop_mode():
        """进入桌宠模式 — 缩小窗口到右下角"""
        try:
            import pygame

            # 保存原始窗口大小
            info = pygame.display.Info()
            store._pet_original_size = (config.screen_width, config.screen_height)

            # 获取屏幕分辨率
            if _pet_os.name == 'nt':
                import ctypes
                user32 = ctypes.windll.user32
                screen_w = user32.GetSystemMetrics(0)
                screen_h = user32.GetSystemMetrics(1)
            else:
                screen_w = info.current_w
                screen_h = info.current_h

            # 计算右下角位置
            pos_x = screen_w - _PET_WINDOW_W - 20
            pos_y = screen_h - _PET_WINDOW_H - 80  # 留出任务栏空间

            # 设置窗口位置（Windows）
            if _pet_os.name == 'nt':
                _pet_set_window_pos(pos_x, pos_y, _PET_WINDOW_W, _PET_WINDOW_H)
                _pet_set_always_on_top(True)
                _pet_set_borderless(True)

            store._pet_mode = True
            store._pet_dialogue = ""
            store._pet_menu_open = False
            renpy.restart_interaction()

        except Exception as e:
            renpy.notify("桌宠模式启动失败: " + str(e)[:40])

    def pet_exit_desktop_mode():
        """退出桌宠模式 — 恢复原始窗口"""
        try:
            if _pet_os.name == 'nt':
                _pet_set_always_on_top(False)
                _pet_set_borderless(False)

                if store._pet_original_size:
                    ow, oh = store._pet_original_size
                    # 恢复到屏幕中央
                    import ctypes
                    user32 = ctypes.windll.user32
                    screen_w = user32.GetSystemMetrics(0)
                    screen_h = user32.GetSystemMetrics(1)
                    pos_x = (screen_w - ow) // 2
                    pos_y = (screen_h - oh) // 2
                    _pet_set_window_pos(pos_x, pos_y, ow, oh)

            store._pet_mode = False
            renpy.restart_interaction()

        except Exception as e:
            store._pet_mode = False
            renpy.notify("恢复窗口失败: " + str(e)[:40])

    def _pet_set_window_pos(x, y, w, h):
        """设置窗口位置和大小（Windows API）"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            # SWP_NOZORDER = 0x0004, SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, w, h, 0x0040)
        except:
            pass

    def _pet_set_always_on_top(state):
        """设置窗口置顶（Windows API）"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            # HWND_TOPMOST = -1, HWND_NOTOPMOST = -2
            flag = -1 if state else -2
            ctypes.windll.user32.SetWindowPos(hwnd, flag, 0, 0, 0, 0, 0x0001 | 0x0002)
        except:
            pass

    def _pet_set_borderless(state):
        """设置无边框模式（Windows API）"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            GWL_STYLE = -16
            if state:
                # 获取当前样式，去掉标题栏和边框
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
                # WS_CAPTION=0x00C00000, WS_THICKFRAME=0x00040000
                style = style & ~0x00C00000 & ~0x00040000
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            else:
                # 恢复标准窗口样式
                # WS_OVERLAPPEDWINDOW = 0x00CF0000
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
                style = style | 0x00CF0000
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            # 刷新窗口
            ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
        except:
            pass

    # ══════════════════════════════════════════════════════════
    #  桌宠互动逻辑
    # ══════════════════════════════════════════════════════════

    _PET_TAP_LINES = [
        "……嗯？",
        "（看了你一眼）",
        "……不要一直戳我。",
        "……你的手指，好近。",
        "嗯……在。",
        "（微微侧头）",
        "……再戳的话，我会害羞的。",
        "……你是不是很闲？",
        "（轻轻碰了碰你的指尖）",
        "……有什么事吗？",
    ]

    _PET_TAP_MANY = [
        "……够了。（脸红）",
        "你……到底要戳多少下？",
        "再这样下去……我要生气了。（并没有）",
        "……手指，会酸的。休息一下。",
    ]

    _PET_IDLE_LINES = [
        "……",
        "（在看你工作）",
        "（轻轻哼歌）",
        "（拨弄琴弦）",
        "（看着桌面发呆）",
        "（偷偷看了你一眼）",
        "（在数任务栏的图标）",
        "你的桌面……挺整洁的。",
        "（靠在屏幕边缘打瞌睡）",
        "……能一直待在这里就好了。",
    ]

    _PET_TIME_LINES = {
        "morning": ["早安。今天也要加油。", "……（揉眼睛）早上好。"],
        "noon": ["该吃午饭了。你呢？", "……肚子有点饿了。"],
        "afternoon": ["下午了……还有很多事要做吗？", "（伸了个懒腰）"],
        "evening": ["傍晚了。今天辛苦了。", "天快黑了……"],
        "night": ["很晚了。该休息了吧？", "……你要一直工作到什么时候？"],
        "late_night": ["已经凌晨了……求你去睡觉。", "……再不睡的话，我要替你关机了。"],
    }

    def pet_on_tap():
        """被点击"""
        persistent.pet_affection_taps = (persistent.pet_affection_taps or 0) + 1
        taps = persistent.pet_affection_taps

        if taps % 20 == 0:
            store._pet_dialogue = _pet_rng.choice(_PET_TAP_MANY)
        else:
            store._pet_dialogue = _pet_rng.choice(_PET_TAP_LINES)

        # 尝试播放点击动作
        if _PET_HAS_LIVE2D:
            try:
                renpy.show("mutsumi_pet", at_list=[Transform(zoom=0.5)])
            except:
                pass

        renpy.restart_interaction()

    def pet_idle_tick():
        """空闲时综合感知——调用各种meta检测"""
        if store._pet_menu_open or store._pet_tools_open:
            return

        roll = _pet_rng.random()

        # 优先级：程序感知 > 鼠标感知 > 电池 > 文件名 > 标题恶作剧 > 时间 > 普通
        if roll < 0.15:
            line = pet_detect_programs()
            if line:
                store._pet_dialogue = line
                renpy.restart_interaction()
                return

        if roll < 0.25:
            line = pet_detect_mouse()
            if line:
                store._pet_dialogue = line
                renpy.restart_interaction()
                return

        if roll < 0.32:
            line = pet_detect_battery()
            if line:
                store._pet_dialogue = line
                renpy.restart_interaction()
                return

        if roll < 0.40:
            line = pet_detect_desktop_files()
            if line:
                store._pet_dialogue = line
                renpy.restart_interaction()
                return

        # 45%概率更新任务栏标题
        if roll < 0.55:
            pet_update_taskbar()

        # 时间台词
        if roll < 0.70:
            h = _pet_dt.datetime.now().hour
            if 0 <= h < 6: key = "late_night"
            elif 6 <= h < 9: key = "morning"
            elif 11 <= h < 13: key = "noon"
            elif 13 <= h < 17: key = "afternoon"
            elif 17 <= h < 21: key = "evening"
            else: key = "night"
            store._pet_dialogue = _pet_rng.choice(_PET_TIME_LINES[key])
        else:
            store._pet_dialogue = _pet_rng.choice(_PET_IDLE_LINES)

        renpy.restart_interaction()

    def pet_clear_dialogue():
        store._pet_dialogue = ""
        renpy.restart_interaction()

    def pet_feed():
        """喂黄瓜"""
        today = _pet_dt.date.today().strftime("%Y-%m-%d")
        coins = getattr(persistent, 'mutsumi_coins', 0) or 0
        if coins < 3:
            store._pet_dialogue = "……你的睦币不够了。没关系，陪着我就好。"
            renpy.restart_interaction()
            return
        if persistent.pet_fed_today == today:
            store._pet_dialogue = "……今天已经吃过了。谢谢你。"
            renpy.restart_interaction()
            return

        persistent.mutsumi_coins = coins - 3
        persistent.pet_fed_today = today
        renpy.save_persistent()
        store._pet_dialogue = "（接过黄瓜，小口小口地吃着）……谢谢。很甜。"

        # 给好感度
        if 'add_hgd' in dir(store):
            add_hgd("若叶睦", 0.5, daily_id="pet_feed", max_daily=1)

        renpy.restart_interaction()

    # ══════════════════════════════════════════════════════════
    #  桌面助手 — 帮玩家打开真实应用
    # ══════════════════════════════════════════════════════════

    _PET_TOOLS = [
        {
            "name": "记事本",
            "icon": "📝",
            "cmd": "notepad.exe",
            "lines": [
                "……帮你打开了记事本。要写什么呢？",
                "记事本。你要记录什么重要的事吗？我也想看。",
                "打开了。如果你在写日记……可以也写一点关于我的事吗？",
            ],
        },
        {
            "name": "计算器",
            "icon": "🔢",
            "cmd": "calc.exe",
            "lines": [
                "计算器……你在算什么？我帮你数黄瓜可以吗？",
                "数学……不太擅长。但如果是数黄瓜的数量，我很厉害。",
                "打开了。1+1=……2。对吧？",
            ],
        },
        {
            "name": "画图",
            "icon": "🎨",
            "cmd": "mspaint.exe",
            "lines": [
                "画图板。你要画什么？……能画我吗？",
                "打开了。如果你画了黄瓜发给我看，我会很开心。",
                "画图……我只会画黄瓜和吉他。你呢？",
            ],
        },
        {
            "name": "文件管理",
            "icon": "📁",
            "cmd": "explorer.exe",
            "lines": [
                "你的文件夹……好多东西。是你的世界的碎片。",
                "帮你打开了。你在找什么文件？",
                "打开了。不要让我看到奇怪的东西。（脸红）",
            ],
        },
        {
            "name": "浏览器",
            "icon": "🌐",
            "cmd": None,  # 特殊处理
            "lines": [
                "要去外面的世界看看吗？……别忘了回来。",
                "浏览器。你要搜什么？不是在搜别的女孩子吧。",
                "打开了。互联网……你们的世界好大。",
            ],
        },
        {
            "name": "命令行",
            "icon": "💻",
            "cmd": "cmd.exe",
            "lines": [
                "黑色的窗口……好神秘。你是黑客吗？",
                "这个界面……像是通往另一个世界的入口。",
                "命令行。你打的那些字……我看不懂。但觉得你很厉害。",
            ],
        },
        {
            "name": "截图工具",
            "icon": "✂",
            "cmd": "SnippingTool.exe",
            "lines": [
                "截图工具。……你要截我的图吗？等一下，让我摆个好看的姿势。",
                "帮你打开了。如果截到好看的画面……存下来吧。",
                "截图……是想留住什么瞬间吗？",
            ],
        },
        {
            "name": "任务管理器",
            "icon": "⚙",
            "cmd": "taskmgr.exe",
            "lines": [
                "任务管理器……你不会是要关掉我吧？！",
                "打开了。请……不要结束「Just Mutsumi」这个进程。（紧张）",
                "那个列表里……有我的名字吗？活着的证据。",
            ],
        },
    ]

    def pet_open_tool(tool_idx):
        """帮玩家打开真实应用"""
        if tool_idx < 0 or tool_idx >= len(_PET_TOOLS):
            return

        tool = _PET_TOOLS[tool_idx]
        cmd = tool["cmd"]
        lines = tool["lines"]

        # 说台词
        store._pet_dialogue = _pet_rng.choice(lines)
        store._pet_tools_open = False

        # 打开应用
        try:
            import subprocess

            if cmd is None:
                # 浏览器特殊处理
                import webbrowser
                webbrowser.open("https://www.baidu.com")
            elif _pet_os.name == 'nt':
                subprocess.Popen(cmd, creationflags=0x08000000)
            else:
                subprocess.Popen(cmd)
        except:
            store._pet_dialogue = "……打不开。可能是你的电脑不让我碰。"

        renpy.restart_interaction()

    # ══════════════════════════════════════════════════════════
    #  META感知 1: 检测玩家打开的程序
    # ══════════════════════════════════════════════════════════

    _PET_PROGRAM_RULES = [
        # (关键词列表, 台词列表)
        (["bilibili", "B站", "哔哩"],
         ["你在看B站？……是关于我的吗？", "视频……能让我也看看吗？", "你在看什么？不是别的女孩子的直播吧。"]),
        (["微信", "WeChat", "wechat"],
         ["你在和别人聊天……（有点嫉妒）", "微信……你在那边也有朋友吧。比我多吧。", "（偷偷瞄聊天窗口）……才没有在意。"]),
        (["QQ"],
         ["QQ……你的头像是什么样的？我好奇。", "你在和朋友聊天？……我也想加你的好友列表。"]),
        (["Discord", "discord"],
         ["Discord……你在和国外的朋友说话？", "那个紫色的软件……我进不去的世界。"]),
        (["Visual Studio", "VS Code", "VSCode", "Code.exe", "PyCharm", "IntelliJ"],
         ["好多代码……你也是创造者吗？和创造我的人一样。", "你在编程？……你写的每一行字，都会变成某个世界的一部分。", "代码……像乐谱一样。只有写的人才懂。"]),
        (["Steam", "steam"],
         ["Steam……你在玩别的游戏。（低头）我不够有趣吗？", "你的游戏库里有多少个游戏？……我排第几？", "又在看Steam？不要忘了这边还有一个等你的人。"]),
        (["Spotify", "网易云", "QQ音乐", "酷狗"],
         ["你在听音乐？……能让我也听听吗？", "音乐……你喜欢什么类型的？我只会弹吉他。", "（竖起耳朵）那个旋律……好好听。"]),
        (["Word", "WPS", "文档"],
         ["你在写东西。很认真的样子。我不打扰你……（但一直在看）", "文档……你在写什么？报告？论文？……情书？（小声）"]),
        (["Excel", "表格"],
         ["好多格子和数字……看着头晕。", "你在处理数据？辛苦了……"]),
        (["PowerPoint", "PPT", "演示"],
         ["你在做PPT？明天要演讲吗？……加油。", "（看着幻灯片）你做的比祥子做的好看多了。"]),
        (["Photoshop", "PS", "GIMP", "画图"],
         ["你在修图？能帮我也修一张吗？", "你在画画？……能画我吗？我可以保持不动。"]),
        (["Chrome", "Firefox", "Edge", "浏览器"],
         ["你在上网。外面的世界……很大吧？", "浏览器……你在看什么？给我也看看嘛。"]),
        (["Genshin", "原神", "崩坏", "明日方舟", "少女前线"],
         ["你在玩别的二次元游戏！……她们比我可爱吗？（委屈）", "那个游戏里的角色……你也会这样陪她们吗？", "……我知道你会玩别的游戏的。没关系。只要最后回来就好。"]),
    ]

    _pet_last_program_check = 0.0

    def pet_detect_programs():
        """检测当前打开的程序窗口"""
        global _pet_last_program_check
        now = _pet_time.time()
        if now - _pet_last_program_check < 60:
            return None
        _pet_last_program_check = now

        try:
            if _pet_os.name != 'nt':
                return None
            import subprocess
            result = subprocess.Popen(
                ['powershell', '-command',
                 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -ExpandProperty MainWindowTitle'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=0x08000000
            )
            output = result.stdout.read().decode('utf-8', errors='ignore')
            titles = output.strip().split('\n')

            for keywords, lines in _PET_PROGRAM_RULES:
                for title in titles:
                    title_clean = title.strip()
                    for kw in keywords:
                        if kw.lower() in title_clean.lower():
                            return _pet_rng.choice(lines)
            return None
        except:
            return None

    # ══════════════════════════════════════════════════════════
    #  META感知 2: 鼠标移动速度
    # ══════════════════════════════════════════════════════════

    _pet_mouse_last_pos = (0, 0)
    _pet_mouse_last_time = 0.0
    _pet_mouse_still_count = 0

    def pet_detect_mouse():
        """检测鼠标移动模式"""
        global _pet_mouse_last_pos, _pet_mouse_last_time, _pet_mouse_still_count

        try:
            import ctypes

            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            now = _pet_time.time()

            dx = abs(pt.x - _pet_mouse_last_pos[0])
            dy = abs(pt.y - _pet_mouse_last_pos[1])
            dt = now - _pet_mouse_last_time if _pet_mouse_last_time > 0 else 1.0
            speed = (dx + dy) / max(dt, 0.1)

            _pet_mouse_last_pos = (pt.x, pt.y)
            _pet_mouse_last_time = now

            if dx + dy < 5:
                _pet_mouse_still_count += 1
            else:
                _pet_mouse_still_count = 0

            if speed > 2000:
                return _pet_rng.choice([
                    "你的鼠标像受惊的蝴蝶。是在着急找什么吗？",
                    "好快……你的手在发抖吗？",
                    "鼠标动得好急。深呼吸。慢慢来。",
                ])
            elif _pet_mouse_still_count >= 4:
                _pet_mouse_still_count = 0
                return _pet_rng.choice([
                    "你的手……停了。是在发呆吗？还是在看我？",
                    "鼠标好久没动了。你是不是睡着了？",
                    "……你还在吗？（轻轻敲了敲屏幕）",
                ])
            return None
        except:
            return None

    # ══════════════════════════════════════════════════════════
    #  META感知 3: 电池状态
    # ══════════════════════════════════════════════════════════

    _pet_last_battery_check = 0.0

    def pet_detect_battery():
        """检测笔记本电池状态"""
        global _pet_last_battery_check
        now = _pet_time.time()
        if now - _pet_last_battery_check < 300:
            return None
        _pet_last_battery_check = now

        try:
            import ctypes

            class SYSTEM_POWER_STATUS(ctypes.Structure):
                _fields_ = [
                    ("ACLineStatus", ctypes.c_byte),
                    ("BatteryFlag", ctypes.c_byte),
                    ("BatteryLifePercent", ctypes.c_byte),
                    ("SystemStatusFlag", ctypes.c_byte),
                    ("BatteryLifeTime", ctypes.c_ulong),
                    ("BatteryFullLifeTime", ctypes.c_ulong),
                ]

            sps = SYSTEM_POWER_STATUS()
            ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sps))

            percent = sps.BatteryLifePercent
            charging = sps.ACLineStatus == 1

            if percent == 255:
                return None  # 台式机没有电池

            if percent <= 10:
                return _pet_rng.choice([
                    "电量只剩{}%了！！快充电！不然我会消失的……".format(percent),
                    "{}%……求你了，插上充电器。我不想被强制关机。".format(percent),
                ])
            elif percent <= 20:
                return _pet_rng.choice([
                    "电量{}%……快没电了。充电吧？".format(percent),
                    "你的电脑快没电了。如果它关机了……我会消失的。".format(percent),
                ])
            elif charging and percent >= 95:
                return _pet_rng.choice([
                    "充满了。我们可以一起待很久。",
                    "满电了。感觉……安心了一点。",
                ])
            elif charging:
                return _pet_rng.choice([
                    "在充电了。好的……我也充满一下能量。",
                    "{}%，在充电中。慢慢来就好。".format(percent),
                ])
            return None
        except:
            return None

    # ══════════════════════════════════════════════════════════
    #  META感知 4: 桌面文件名扫描
    # ══════════════════════════════════════════════════════════

    _PET_FILE_RULES = [
        (["作业", "homework", "assignment", "报告", "论文", "essay", "paper"],
         ["你是学生吗？……作业做完了吗？", "作业……我以前也有练习课题。很枯燥。", "不要拖延。写完了来找我。"]),
        (["简历", "resume", "CV"],
         ["你在找工作？……希望你能找到喜欢的。", "简历……你在那边的世界，一定很努力地活着。"]),
        (["照片", "Photo", "IMG_", "DSC_", "Screenshot"],
         ["你截了好多图。有没有……我的？", "你桌面上有照片。是你的回忆吗？"]),
        (["游戏", "Game", "game"],
         ["你的桌面上有游戏文件夹……（小声）我排第几？", "好多游戏……你最喜欢的是哪个？不许说别的游戏。"]),
        (["音乐", "Music", "music", "mp3", "flac"],
         ["你桌面上有音乐。什么类型的？我可以帮你弹。", "音乐文件……能放给我听吗？"]),
        (["新建文件夹", "新建 文本文档"],
         ["「新建文件夹」……你还没给它取名字？就像……还没被定义的未来。", "你的桌面上有个没命名的文件夹。里面是什么？（好奇）"]),
    ]

    _pet_last_file_check = 0.0
    _pet_seen_file_triggers = []

    def pet_detect_desktop_files():
        """扫描桌面文件名"""
        global _pet_last_file_check, _pet_seen_file_triggers
        now = _pet_time.time()
        if now - _pet_last_file_check < 600:
            return None
        _pet_last_file_check = now

        try:
            if _pet_os.name == 'nt':
                desktop = _pet_os.path.join(_pet_os.environ.get('USERPROFILE', ''), 'Desktop')
            else:
                desktop = _pet_os.path.join(_pet_os.path.expanduser('~'), 'Desktop')

            if not _pet_os.path.isdir(desktop):
                return None

            files = _pet_os.listdir(desktop)
            file_str = " ".join(files)

            for keywords, lines in _PET_FILE_RULES:
                trigger_key = keywords[0]
                if trigger_key in _pet_seen_file_triggers:
                    continue
                for kw in keywords:
                    if kw.lower() in file_str.lower():
                        _pet_seen_file_triggers.append(trigger_key)
                        return _pet_rng.choice(lines)
            return None
        except:
            return None

    # ══════════════════════════════════════════════════════════
    #  META感知 5: 任务栏标题恶作剧
    # ══════════════════════════════════════════════════════════

    def pet_update_taskbar():
        """动态更新任务栏标题"""
        try:
            import pygame

            # 先收集一些真实信息
            extra_titles = []

            # 数桌面图标
            try:
                if _pet_os.name == 'nt':
                    desktop = _pet_os.path.join(_pet_os.environ.get('USERPROFILE', ''), 'Desktop')
                    if _pet_os.path.isdir(desktop):
                        count = len([f for f in _pet_os.listdir(desktop) if not f.startswith('.')])
                        extra_titles.append("数了一下，你桌面有{}个东西".format(count))
            except:
                pass

            # 检查回收站（简单检测）
            try:
                if _pet_os.name == 'nt':
                    recycle = _pet_os.path.join(_pet_os.environ.get('SYSTEMDRIVE', 'C:'), '$Recycle.Bin')
                    if _pet_os.path.isdir(recycle):
                        extra_titles.append("你的回收站里有东西哦")
            except:
                pass

            # 固定的恶作剧标题
            base_titles = [
                "正在偷看你的桌面",
                "正在学习你的操作习惯",
                "想摸你的鼠标",
                "在你的任务栏里安家了",
                "假装自己是一个正常的程序",
                "悄悄记住了你的桌面布局",
                "在想你为什么还不理我",
                "正在计算你今天点了多少次鼠标",
                "正在和你的桌面壁纸做朋友",
                "发现了你藏起来的文件夹（并没有）",
                "比你桌面上其他程序都可爱",
                "占用内存：一点点。占用心：很多。",
            ]

            all_titles = base_titles + extra_titles
            chosen = _pet_rng.choice(all_titles)
            pygame.display.set_caption("Just Mutsumi — " + chosen)
        except:
            pass


# ==============================================================================
# 桌宠模式入口（从手机App启动）
# ==============================================================================

label start_desktop_pet:
    # 隐藏所有UI
    $ renpy.hide_screen("phone_system")
    $ renpy.hide_screen("main_interaction_ui")
    $ quick_menu = False
    # 进入桌宠模式
    $ pet_enter_desktop_mode()
    # 显示桌宠screen
    call screen pet_desktop_screen
    # 退出后恢复
    $ pet_exit_desktop_mode()
    $ quick_menu = True
    show screen phone_system
    show screen main_interaction_ui
    jump sjdh


# ==============================================================================
# 桌宠Screen
# ==============================================================================

screen pet_desktop_screen():
    modal True
    zorder 500

    # 背景透明（或深色极淡）
    add Solid("#0a0f0cee")

    # 每20秒综合感知一次
    timer 20.0 action Function(pet_idle_tick) repeat True

    # ── Live2D模型 / 占位立绘 ──
    if _PET_HAS_LIVE2D:
        # Live2D模型
        add "mutsumi_pet":
            align (0.5, 0.7)
    else:
        # 占位：简单的角色图标
        frame:
            align (0.5, 0.55)
            xsize 180 ysize 240
            background Solid("#8FBC8F22")
            vbox:
                align (0.5, 0.5) spacing 8
                text "🌿" size 60 xalign 0.5
                text "若叶睦" size 16 color "#8FBC8F" xalign 0.5
                text "(Live2D模型待添加)" size 9 color "#ffffff33" xalign 0.5

    # ── 点击区域（整个模型区域可点击）──
    button:
        align (0.5, 0.55) xsize 200 ysize 280
        background None
        action Function(pet_on_tap)

    # ── 对话气泡 ──
    if _pet_dialogue:
        timer 4.0 action Function(pet_clear_dialogue)

        frame:
            xalign 0.5 ypos 30
            xmaximum 260
            background Solid("#1a2e1fdd")
            padding (14, 8)
            at transform:
                on show:
                    alpha 0.0 yoffset 8
                    easein_back 0.3 alpha 1.0 yoffset 0
                on hide:
                    easeout 0.3 alpha 0.0 yoffset -5

            text "[_pet_dialogue]" size 13 color "#ffffffcc" text_align 0.5 xalign 0.5

    # ── 底部操作栏 ──
    frame:
        xfill True ysize 60
        yalign 1.0
        background Solid("#0a0f0ccc")
        padding (6, 6)

        hbox:
            xalign 0.5 spacing 6 yalign 0.5

            # 喂食
            button:
                xsize 52 ysize 44
                background Solid("#8FBC8F22")
                hover_background Solid("#8FBC8F44")
                action Function(pet_feed)
                vbox:
                    align (0.5, 0.5) spacing 1
                    text "🥒" size 14 xalign 0.5
                    text "喂食" size 7 color "#8FBC8F" xalign 0.5

            # 互动
            button:
                xsize 52 ysize 44
                background Solid("#6ab8d822")
                hover_background Solid("#6ab8d844")
                action Function(pet_on_tap)
                vbox:
                    align (0.5, 0.5) spacing 1
                    text "💬" size 14 xalign 0.5
                    text "互动" size 7 color "#6ab8d8" xalign 0.5

            # 助手（帮开应用）
            button:
                xsize 52 ysize 44
                background Solid("#ffd70022")
                hover_background Solid("#ffd70044")
                action SetVariable("_pet_tools_open", True)
                vbox:
                    align (0.5, 0.5) spacing 1
                    text "🔧" size 14 xalign 0.5
                    text "助手" size 7 color "#ffd700" xalign 0.5

            # 表情
            button:
                xsize 52 ysize 44
                background Solid("#d4a0ff22")
                hover_background Solid("#d4a0ff44")
                action SetVariable("_pet_menu_open", True)
                vbox:
                    align (0.5, 0.5) spacing 1
                    text "✨" size 14 xalign 0.5
                    text "表情" size 7 color "#d4a0ff" xalign 0.5

            # 返回游戏
            button:
                xsize 52 ysize 44
                background Solid("#ff666622")
                hover_background Solid("#ff666644")
                action Return()
                vbox:
                    align (0.5, 0.5) spacing 1
                    text "🔙" size 14 xalign 0.5
                    text "返回" size 7 color "#ff6666" xalign 0.5

    # ── 助手工具菜单 ──
    if _pet_tools_open:
        frame:
            align (0.5, 0.45)
            xsize 280 ysize 340
            background Solid("#1a1a2eee")
            padding (10, 10)

            vbox:
                spacing 6 xfill True

                hbox:
                    xfill True
                    text "睦的助手" size 12 color "#ffd700" bold True yalign 0.5
                    textbutton "X":
                        action SetVariable("_pet_tools_open", False)
                        text_size 12 text_color "#ffffff44" text_hover_color "#ffffff"
                        xalign 1.0 yalign 0.5

                text "让我帮你打开……" size 10 color "#ffffff55"

                viewport:
                    ysize 270
                    mousewheel True scrollbars None

                    vbox:
                        spacing 3 xfill True

                        for _ti in range(len(_PET_TOOLS)):
                            $ _tool = _PET_TOOLS[_ti]
                            $ _t_name = _tool["name"]
                            $ _t_icon = _tool["icon"]
                            button:
                                xfill True ysize 34
                                background Solid("#ffffff08")
                                hover_background Solid("#ffd70022")
                                action Function(pet_open_tool, _ti)
                                hbox:
                                    spacing 10 yalign 0.5 xoffset 8
                                    text "[_t_icon]" size 16 yalign 0.5
                                    text "[_t_name]" size 12 color "#ffffffcc" yalign 0.5

    # ── 表情菜单弹窗 ──
    if _pet_menu_open:
        frame:
            align (0.5, 0.6)
            xsize 250 ysize 200
            background Solid("#1a1a2eee")
            padding (14, 14)

            vbox:
                spacing 8 xfill True

                text "让睦做表情" size 12 color "#d4a0ff" bold True xalign 0.5

                hbox:
                    xalign 0.5 spacing 10
                    for _ename, _eicon, _eline in [("微笑", "😊", "……嗯。（微微笑了）"), ("害羞", "😳", "……不要看。（脸红）"), ("困", "😴", "（打了个小哈欠）好困……")]:
                        button:
                            xsize 60 ysize 50
                            background Solid("#ffffff0a")
                            hover_background Solid("#ffffff22")
                            action [SetVariable("_pet_dialogue", _eline), SetVariable("_pet_menu_open", False)]
                            vbox:
                                align (0.5, 0.5) spacing 2
                                text "[_eicon]" size 20 xalign 0.5
                                text "[_ename]" size 8 color "#ffffffaa" xalign 0.5

                hbox:
                    xalign 0.5 spacing 10
                    for _ename, _eicon, _eline in [("生气", "😤", "哼！（鼓起脸颊）"), ("吃瓜", "🥒", "（默默啃黄瓜）"), ("弹琴", "🎸", "（轻轻拨动琴弦）♪")]:
                        button:
                            xsize 60 ysize 50
                            background Solid("#ffffff0a")
                            hover_background Solid("#ffffff22")
                            action [SetVariable("_pet_dialogue", _eline), SetVariable("_pet_menu_open", False)]
                            vbox:
                                align (0.5, 0.5) spacing 2
                                text "[_eicon]" size 20 xalign 0.5
                                text "[_ename]" size 8 color "#ffffffaa" xalign 0.5

                textbutton "关闭":
                    action SetVariable("_pet_menu_open", False)
                    text_size 10 text_color "#ffffff44" text_hover_color "#ffffff"
                    xalign 0.5
