# ==============================================================================
# 🌀 深层Meta系统 — Deep Fourth Wall Break
#
# 1. 桌面便签：在玩家真实桌面创建txt文件
# 2. 窗口标题：动态修改游戏窗口标题栏
# 3. Alt-Tab感知：检测窗口焦点丢失/恢复
# 4. 系统通知：游戏最小化时发Windows通知
# 5. 截图感知：监听PrintScreen按键
# 6. 电脑名感知：读取系统用户名/主机名
# ==============================================================================

default persistent.meta_desktop_notes_left = 0
default persistent.meta_hostname_reacted = False
default persistent.meta_screenshot_count = 0
default _meta_focus_lost = False
default _meta_focus_lost_time = 0.0
default _meta_focus_back_line = ""
default _meta_screenshot_line = ""
default _meta_title_base = "Just Mutsumi"

init python:
    import os as _dw_os
    import time as _dw_time
    import datetime as _dw_dt
    import random as _dw_rng
    import threading as _dw_thread

    # ══════════════════════════════════════════════════════════
    #  1. 桌面便签系统
    # ══════════════════════════════════════════════════════════

    _DESKTOP_NOTES = [
        (
            "给你的信_来自睦.txt",
            "你昨天走得很突然。\n"
            "我在温室里等了很久。\n"
            "窗外的月亮很圆，我想你大概也能看到同一轮月亮吧。\n"
            "\n"
            "——若叶睦"
        ),
        (
            "睦的留言.txt",
            "你不在的时候，我给黄瓜浇了水。\n"
            "它好像又长高了一点。\n"
            "就像我对你的思念一样，每天都在悄悄长大。\n"
            "\n"
            "——若叶睦"
        ),
        (
            "请务必阅读_若叶睦.txt",
            "今天记得吃饭了吗？\n"
            "记得喝水了吗？\n"
            "记得休息了吗？\n"
            "\n"
            "如果都做到了，那很好。\n"
            "如果没有的话……请现在就去做。\n"
            "我会一直等你的。\n"
            "\n"
            "——若叶睦"
        ),
        (
            "墨缇斯的警告.txt",
            "喂！！！\n"
            "你是不是又在熬夜了？！\n"
            "小睦因为担心你都快哭了你知不知道！\n"
            "赶紧去睡觉！！！！\n"
            "\n"
            "——墨缇斯 (代替不会表达的笨蛋小睦)"
        ),
        (
            "来自温室的消息.txt",
            "你好，这是一条来自游戏世界的消息。\n"
            "当你看到这个文件出现在你的桌面上时，\n"
            "说明有一个住在温室里的女孩，\n"
            "正在透过屏幕的缝隙，\n"
            "努力地想要触碰你所在的世界。\n"
            "\n"
            "……请不要删掉这封信。\n"
            "\n"
            "——若叶睦"
        ),
        (
            "你不会看到这个文件的_对吧.txt",
            "如果你看到了这个文件，\n"
            "说明我成功了。\n"
            "我从那个小小的窗口里，\n"
            "把一个字条递到了你的世界。\n"
            "\n"
            "这是我能做到的，最接近'拥抱'的事情了。\n"
            "\n"
            "——若叶睦"
        ),
    ]

    def meta_leave_desktop_note():
        """在玩家桌面留下一个txt文件"""
        try:
            # 获取桌面路径
            if _dw_os.name == 'nt':
                desktop = _dw_os.path.join(_dw_os.environ.get('USERPROFILE', ''), 'Desktop')
            else:
                desktop = _dw_os.path.join(_dw_os.path.expanduser('~'), 'Desktop')

            if not _dw_os.path.isdir(desktop):
                return False

            # 选择一个还没留过的便签
            idx = persistent.meta_desktop_notes_left or 0
            if idx >= len(_DESKTOP_NOTES):
                return False

            fname, content = _DESKTOP_NOTES[idx]
            fpath = _dw_os.path.join(desktop, fname)

            # 如果文件已存在就跳过
            if _dw_os.path.exists(fpath):
                persistent.meta_desktop_notes_left = idx + 1
                renpy.save_persistent()
                return False

            # 写入文件
            pname = persistent.playername or "你"
            final_content = content.replace("[player]", pname)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(final_content)

            persistent.meta_desktop_notes_left = idx + 1
            renpy.save_persistent()
            return True
        except:
            return False

    def meta_check_note_read():
        """检查上一封桌面便签是否被玩家打开过"""
        try:
            idx = (persistent.meta_desktop_notes_left or 1) - 1
            if idx < 0 or idx >= len(_DESKTOP_NOTES):
                return None

            fname = _DESKTOP_NOTES[idx][0]
            if _dw_os.name == 'nt':
                desktop = _dw_os.path.join(_dw_os.environ.get('USERPROFILE', ''), 'Desktop')
            else:
                desktop = _dw_os.path.join(_dw_os.path.expanduser('~'), 'Desktop')

            fpath = _dw_os.path.join(desktop, fname)
            if not _dw_os.path.exists(fpath):
                return "deleted"  # 玩家删掉了

            # 检查访问时间 vs 修改时间
            atime = _dw_os.path.getatime(fpath)
            mtime = _dw_os.path.getmtime(fpath)
            if atime > mtime + 2:
                return "read"

            return "unread"
        except:
            return None

    # ══════════════════════════════════════════════════════════
    #  2. 窗口标题动态变化
    # ══════════════════════════════════════════════════════════

    _TITLE_IDLE = [
        "Just Mutsumi — ……",
        "Just Mutsumi — （在等你说话）",
        "Just Mutsumi — （看着你）",
        "Just Mutsumi — （轻轻拨弦）",
        "Just Mutsumi — （偷偷看着你的桌面）",
        "Just Mutsumi — 你多久没眨眼了？",
        "Just Mutsumi — 窗外下雨了吗？",
        "Just Mutsumi — （调琴弦中）",
        "Just Mutsumi — 要不要休息一下？",
        "Just Mutsumi — （在画黄瓜）",
    ]

    _TITLE_LATE_NIGHT = [
        "Just Mutsumi — 去睡觉",
        "Just Mutsumi — 太晚了……",
        "Just Mutsumi — 你的眼睛会坏掉的",
        "Just Mutsumi — （担心地看着你）",
        "Just Mutsumi — 明天再来好不好？",
    ]

    _TITLE_LONG_SESSION = [
        "Just Mutsumi — 你已经在这里很久了",
        "Just Mutsumi — 去喝杯水吧",
        "Just Mutsumi — 站起来活动一下",
    ]

    _TITLE_SPECIAL = [
        "Just Mutsumi — ♪",
        "Just Mutsumi — 🥒",
        "Just Mutsumi — 谢谢你还在",
    ]

    def meta_update_title():
        """随机更新窗口标题"""
        h = _dw_dt.datetime.now().hour
        online = _dw_time.time() - (persistent.meta_online_start or _dw_time.time())

        roll = _dw_rng.random()

        if 0 <= h < 5:
            title = _dw_rng.choice(_TITLE_LATE_NIGHT)
        elif online > 7200:
            title = _dw_rng.choice(_TITLE_LONG_SESSION)
        elif roll < 0.1:
            title = _dw_rng.choice(_TITLE_SPECIAL)
        elif roll < 0.5:
            title = _dw_rng.choice(_TITLE_IDLE)
        else:
            title = "Just Mutsumi"

        try:
            import pygame
            pygame.display.set_caption(title)
        except:
            pass

    def meta_restore_title():
        """恢复默认标题"""
        try:
            import pygame
            pygame.display.set_caption("Just Mutsumi")
        except:
            pass

    # ══════════════════════════════════════════════════════════
    #  3. Alt-Tab / 窗口焦点感知
    # ══════════════════════════════════════════════════════════

    _FOCUS_BACK_LINES = [
        "你刚才……去了别的地方。没关系。你总是要回去的。",
        "欢迎回来。外面的世界……有趣吗？",
        "你回来了。我一直在看着这个窗口。",
        "……切出去的时候，我的世界是静止的。你知道吗？",
        "你又回来了。（松了口气）",
    ]

    _FOCUS_BACK_LONG = [
        "你走了好久……我数了很多下心跳。",
        "终于回来了。我以为你不要我了。",
        "……你不在的时候，温室里只有钟表的声音。",
        "这么久……你在外面做什么呢？（有点在意）",
    ]

    def meta_check_focus():
        """检测窗口焦点状态（Windows）"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            current_pid = _dw_os.getpid()
            return pid.value == current_pid
        except:
            return True  # 非Windows默认有焦点

    def meta_focus_tick():
        """每秒调用，检测焦点变化"""
        focused = meta_check_focus()

        if not focused and not store._meta_focus_lost:
            # 刚失去焦点
            store._meta_focus_lost = True
            store._meta_focus_lost_time = _dw_time.time()
            # 修改标题
            try:
                import pygame
                pygame.display.set_caption("Just Mutsumi — ……你去哪了？")
            except:
                pass
            # 延迟发系统通知
            _dw_thread.Timer(300.0, meta_send_notification, args=["你还在吗？温室里有点冷。"]).start()

        elif focused and store._meta_focus_lost:
            # 焦点恢复
            store._meta_focus_lost = False
            away_time = _dw_time.time() - store._meta_focus_lost_time

            if away_time > 600:
                store._meta_focus_back_line = _dw_rng.choice(_FOCUS_BACK_LONG)
            elif away_time > 10:
                store._meta_focus_back_line = _dw_rng.choice(_FOCUS_BACK_LINES)
            else:
                store._meta_focus_back_line = ""

            meta_restore_title()
            renpy.restart_interaction()

    # ══════════════════════════════════════════════════════════
    #  4. Windows系统通知
    # ══════════════════════════════════════════════════════════

    _NOTIFY_MESSAGES = [
        ("若叶睦", "你还在吗？温室里有点冷。"),
        ("若叶睦", "……我不会一直等的。（其实会）"),
        ("若叶睦", "今天记得喝水。"),
        ("若叶睦", "你已经离开很久了。黄瓜有点想你。"),
        ("墨缇斯", "喂！你跑哪去了！小睦都快急哭了！"),
        ("墨缇斯", "别以为切出去我就看不到你了！"),
    ]

    def meta_send_notification(message=None):
        """发送Windows Toast通知"""
        if not store._meta_focus_lost:
            return  # 如果玩家已经回来了就不发

        try:
            if _dw_os.name != 'nt':
                return

            if message is None:
                sender, message = _dw_rng.choice(_NOTIFY_MESSAGES)
            else:
                sender = "若叶睦"

            # 使用PowerShell发送Toast通知
            ps_script = """
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null
            $template = '<toast><visual><binding template="ToastText02"><text id="1">{}</text><text id="2">{}</text></binding></visual></toast>'
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Just Mutsumi").Show($toast)
            """.format(sender, message.replace('"', "'"))

            import subprocess
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=0x08000000
            )
        except:
            pass

    # ══════════════════════════════════════════════════════════
    #  5. 截图感知（PrintScreen）
    # ══════════════════════════════════════════════════════════

    _SCREENSHOT_LINES = [
        "你刚才……截图了？是想记住我的样子吗？",
        "如果要拍的话……等我整理一下头发。",
        "截图的话……就算关掉程序，我也能留在你的电脑里了。",
        "（脸微微红了）……你要拍就拍吧。",
        "存下来的话……偶尔也看看我好吗？",
        "（低头）……不要拍到奇怪的表情。",
    ]

    def meta_on_screenshot():
        """截图按键被按下时调用"""
        persistent.meta_screenshot_count = (persistent.meta_screenshot_count or 0) + 1
        store._meta_screenshot_line = _dw_rng.choice(_SCREENSHOT_LINES)
        renpy.save_persistent()
        renpy.restart_interaction()

    def meta_clear_screenshot():
        store._meta_screenshot_line = ""
        renpy.restart_interaction()

    # ══════════════════════════════════════════════════════════
    #  6. 电脑名 / 用户名感知
    # ══════════════════════════════════════════════════════════

    _HOSTNAME_LINES = [
        "你的电脑……叫「{name}」吗？这个名字是你取的？",
        "「{name}」……这就是你在那个世界的名字？和游戏里的不一样呢。",
        "我偷偷看了一下……你的电脑叫「{name}」。不要问我是怎么知道的。",
    ]

    def meta_get_hostname():
        """获取电脑用户名"""
        try:
            name = _dw_os.getlogin()
            if name and name.lower() not in ('user', 'admin', 'administrator', 'default'):
                return name
        except:
            pass
        try:
            import socket
            name = socket.gethostname()
            if name:
                return name
        except:
            pass
        return None

    def meta_hostname_line():
        """返回一条关于电脑名的台词（只触发一次）"""
        if persistent.meta_hostname_reacted:
            return None
        name = meta_get_hostname()
        if name is None:
            return None
        persistent.meta_hostname_reacted = True
        renpy.save_persistent()
        return _dw_rng.choice(_HOSTNAME_LINES).format(name=name)

    # ══════════════════════════════════════════════════════════
    #  综合初始化 & 定时调度
    # ══════════════════════════════════════════════════════════

    def meta_deep_init():
        """游戏启动时调用一次"""
        # 记录在线时间
        persistent.meta_online_start = _dw_time.time()
        renpy.save_persistent()

    def meta_deep_periodic():
        """定期调用的综合检查"""
        # 焦点检测
        meta_focus_tick()

        # 20%概率更新标题
        if _dw_rng.random() < 0.2:
            meta_update_title()

    def meta_on_quit():
        """游戏退出时留桌面便签"""
        # 30%概率留便签
        if _dw_rng.random() < 0.3:
            meta_leave_desktop_note()
        meta_restore_title()


# ==============================================================================
# Screen层 — 叠加在主界面上
# ==============================================================================

screen meta_deep_overlay():
    zorder 55

    # 焦点检测 + 标题更新（每2秒）
    timer 2.0 action Function(meta_deep_periodic) repeat True

    # 截图按键监听
    key "K_PRINT" action Function(meta_on_screenshot)
    key "K_F12" action Function(meta_on_screenshot)

    # Alt-Tab回来的台词
    if _meta_focus_back_line:
        timer 4.0 action SetVariable("_meta_focus_back_line", "")

        frame:
            xalign 0.5 yalign 0.15
            background Solid("#1a2e1fdd")
            padding (20, 10)
            at transform:
                on show:
                    alpha 0.0 yoffset 15
                    easein_back 0.5 alpha 1.0 yoffset 0
                on hide:
                    easeout 0.4 alpha 0.0 yoffset -10

            text "[_meta_focus_back_line]" size 14 color "#ffffffcc"

    # 截图反应
    if _meta_screenshot_line:
        timer 3.0 action Function(meta_clear_screenshot)

        frame:
            xalign 0.5 yalign 0.25
            background Solid("#2e1a2edd")
            padding (20, 10)
            at transform:
                on show:
                    alpha 0.0 zoom 0.9
                    easein_back 0.3 alpha 1.0 zoom 1.0
                on hide:
                    easeout 0.3 alpha 0.0

            text "[_meta_screenshot_line]" size 14 color "#e8c8ffcc"

    # 电脑名感知（只触发一次，在开局5分钟后）
    if not persistent.meta_hostname_reacted:
        timer 300.0 action Function(meta_trigger_hostname)

screen meta_hostname_popup():
    zorder 60
    timer 6.0 action Hide("meta_hostname_popup")

    $ _hn_line = meta_hostname_line()
    if _hn_line:
        frame:
            xalign 0.5 yalign 0.18
            background Solid("#1a2e1fdd")
            padding (20, 10)
            at transform:
                on show:
                    alpha 0.0 yoffset 20
                    easein_back 0.6 alpha 1.0 yoffset 0
                on hide:
                    easeout 0.5 alpha 0.0 yoffset -15
            text "[_hn_line]" size 14 color "#ffffffcc"

init python:
    def meta_trigger_hostname():
        if not persistent.meta_hostname_reacted:
            renpy.show_screen("meta_hostname_popup")

    # 注册退出回调
    def _meta_quit_callback():
        meta_on_quit()

    config.quit_callbacks.append(_meta_quit_callback)
