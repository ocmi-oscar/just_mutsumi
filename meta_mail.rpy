# ==============================================================================
# 📮 信箱系统 — Meta Mail (跨次元通信)
#
# 核心玩法：玩家在游戏内写信 → 发送到服务器 → 开发者以睦的口吻回复 → 玩家收到真实邮件
#
# 游戏端职责：
#   1. 收集玩家邮箱 + 游戏内称呼
#   2. 提供写信界面
#   3. 将信件POST到服务器API
#   4. 拉取服务器的回信列表显示在游戏内
#
# 服务器端职责（由开发者另行配置）：
#   1. 接收 POST /api/register  (email + player_name)
#   2. 接收 POST /api/send      (email + player_name + letter_content)
#   3. 提供 GET  /api/inbox?email=xxx  (返回回信列表JSON)
#   4. 发送真实邮件到玩家邮箱
# ==============================================================================

# ── 服务器配置 ──
define META_MAIL_SERVER = "https://renpy-mailbox.onrender.com"
define META_MAIL_API_SECRET = "justmutsumi2026supersecret"

# ── 持久化变量 ──
default persistent.meta_mail_email = ""
default persistent.meta_mail_registered = False
default persistent.meta_mail_sent_count = 0
default persistent.meta_mail_history = []
default persistent.meta_mail_last_change = 0.0
default persistent.meta_mail_today_date = ""
default persistent.meta_mail_today_count = 0

# ── 运行时变量 ──
default _mail_compose_text = ""
default _mail_inbox = []
default _mail_status = ""
default _mail_loading = False
default _mail_email_input = ""
default _mail_change_dialog = False
default _mail_change_input = ""
default _mail_change_status = ""
# Tab状态用store变量，避免use嵌套时SetScreenVariable找错目标
default _mail_tab = 0
default _mail_detail_idx = -1

init python:
    import threading as _mail_thread
    import json as _mail_json

    # ══════════════════════════════════════════════════════════
    #  网络通信层
    # ══════════════════════════════════════════════════════════

    def _mail_make_ssl_ctx():
        """创建跳过证书验证的SSL上下文（解决Windows证书过期问题）"""
        try:
            import ssl as _mail_ssl
            ctx = _mail_ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _mail_ssl.CERT_NONE
            return ctx
        except:
            return None

    def _mail_post(endpoint, data):
        """向服务器POST JSON数据（带重试应对Render冷启动）"""
        last_err = ""
        # 重试3次，每次超时时间递增（应对Render免费版冷启动）
        timeouts = [15, 45, 60]
        for _attempt in range(3):
            try:
                url = META_MAIL_SERVER + endpoint
                payload = _mail_json.dumps(data).encode('utf-8')
                from urllib.request import Request, urlopen
                req = Request(url, data=payload, headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-API-Secret": META_MAIL_API_SECRET,
                    "User-Agent": "RenpyClient/1.0",
                })
                ctx = _mail_make_ssl_ctx()
                if ctx:
                    resp = urlopen(req, timeout=timeouts[_attempt], context=ctx)
                else:
                    resp = urlopen(req, timeout=timeouts[_attempt])
                body = resp.read().decode('utf-8')
                return _mail_json.loads(body)
            except Exception as e:
                last_err = str(e)[:100]
                # 第一次失败且是超时 → 可能是冷启动，继续重试
                if _attempt < 2 and ("timed out" in last_err.lower() or "timeout" in last_err.lower()):
                    continue
                # 其他错误直接返回
                break
        return {"error": last_err or "连接失败"}

    def _mail_get(endpoint):
        """向服务器GET请求（带重试）"""
        last_err = ""
        timeouts = [15, 45, 60]
        for _attempt in range(3):
            try:
                url = META_MAIL_SERVER + endpoint
                from urllib.request import Request, urlopen
                req = Request(url, headers={
                    "Accept": "application/json",
                    "X-API-Secret": META_MAIL_API_SECRET,
                    "User-Agent": "RenpyClient/1.0",
                })
                ctx = _mail_make_ssl_ctx()
                if ctx:
                    resp = urlopen(req, timeout=timeouts[_attempt], context=ctx)
                else:
                    resp = urlopen(req, timeout=timeouts[_attempt])
                body = resp.read().decode('utf-8')
                return _mail_json.loads(body)
            except Exception as e:
                last_err = str(e)[:100]
                if _attempt < 2 and ("timed out" in last_err.lower() or "timeout" in last_err.lower()):
                    continue
                break
        return {"error": last_err or "连接失败"}

    # ══════════════════════════════════════════════════════════
    #  业务逻辑
    # ══════════════════════════════════════════════════════════

    def mail_register():
        """注册邮箱（第一次使用）"""
        email = store._mail_email_input.strip()
        if not email or "@" not in email:
            store._mail_status = "请输入有效的邮箱地址"
            renpy.restart_interaction()
            return

        store._mail_loading = True
        store._mail_status = "正在连接……"
        renpy.restart_interaction()

        def _do():
            data = {
                "email": email,
                "player_name": persistent.playername or "旅行者",
                "action": "register",
            }
            result = _mail_post("/api/register", data)

            if "error" in result:
                store._mail_status = "连接失败，但邮箱已保存。睦会记住的。"
            else:
                store._mail_status = "注册成功！睦会给你写第一封信的。"

            persistent.meta_mail_email = email
            persistent.meta_mail_registered = True
            renpy.save_persistent()
            store._mail_loading = False
            renpy.restart_interaction()

        t = _mail_thread.Thread(target=_do)
        t.daemon = True
        t.start()

    def mail_check_can_change():
        """检查是否可以更换邮箱（7天限制）"""
        import time as _mt
        last = persistent.meta_mail_last_change or 0
        if last == 0:
            return True, 0
        elapsed = _mt.time() - last
        seven_days = 7 * 24 * 3600
        if elapsed >= seven_days:
            return True, 0
        remain_days = int((seven_days - elapsed) / 86400) + 1
        return False, remain_days

    def mail_change_email():
        """更换邮箱"""
        new_email = store._mail_change_input.strip().lower()
        if not new_email or "@" not in new_email:
            store._mail_change_status = "请输入有效的邮箱地址"
            renpy.restart_interaction()
            return
        old_email = (persistent.meta_mail_email or "").lower()
        if new_email == old_email:
            store._mail_change_status = "新邮箱不能和旧邮箱一样"
            renpy.restart_interaction()
            return

        can_change, remain = mail_check_can_change()
        if not can_change:
            store._mail_change_status = "7天内只能更换一次，还需等待{}天".format(remain)
            renpy.restart_interaction()
            return

        store._mail_loading = True
        store._mail_change_status = "正在更换……"
        renpy.restart_interaction()

        def _do():
            import time as _mt
            data = {
                "email": new_email,
                "player_name": persistent.playername or "旅行者",
                "action": "register",
            }
            result = _mail_post("/api/register", data)

            if "error" in result:
                store._mail_change_status = "连接失败，请稍后再试"
                store._mail_loading = False
                renpy.restart_interaction()
                return

            persistent.meta_mail_email = new_email
            persistent.meta_mail_last_change = _mt.time()
            renpy.save_persistent()
            store._mail_change_status = "邮箱已更换"
            store._mail_change_dialog = False
            store._mail_change_input = ""
            store._mail_loading = False
            renpy.notify("邮箱已更换为 " + new_email)
            renpy.restart_interaction()

        t = _mail_thread.Thread(target=_do)
        t.daemon = True
        t.start()

    def mail_send_letter():
        """发送一封信（每日最多2封）"""
        import datetime as _msl_dt
        content = store._mail_compose_text.strip()
        if not content:
            store._mail_status = "信纸是空的……写点什么吧。"
            renpy.restart_interaction()
            return
        if len(content) > 2000:
            store._mail_status = "内容太长了……请控制在2000字以内。"
            renpy.restart_interaction()
            return
        # 每日2封限制
        _today = str(_msl_dt.date.today())
        if persistent.meta_mail_today_date != _today:
            persistent.meta_mail_today_date = _today
            persistent.meta_mail_today_count = 0
        if persistent.meta_mail_today_count >= 2:
            store._mail_status = "今天已经寄出2封信了……明天再来吧。"
            renpy.restart_interaction()
            return

        store._mail_loading = True
        store._mail_status = "正在投递……"
        renpy.restart_interaction()

        def _do():
            import datetime
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            data = {
                "email": persistent.meta_mail_email,
                "player_name": persistent.playername or "旅行者",
                "content": content,
                "timestamp": now_str,
                "action": "send",
            }
            result = _mail_post("/api/send", data)

            # 本地记录（重新赋值整个列表强制触发persistent保存）
            record = {
                "type": "sent",
                "content": content,
                "time": now_str,
            }
            _old_history = persistent.meta_mail_history or []
            _new_history = [record] + _old_history
            if len(_new_history) > 50:
                _new_history = _new_history[:50]
            persistent.meta_mail_history = _new_history
            persistent.meta_mail_sent_count = (persistent.meta_mail_sent_count or 0) + 1
            persistent.meta_mail_today_count = (persistent.meta_mail_today_count or 0) + 1

            if "error" in result:
                store._mail_status = "网络波动……但信已经写好了。也许下次能送到。"
            else:
                store._mail_status = "信已经寄出了。睦收到后会给你回信的……"

            store._mail_compose_text = ""
            renpy.save_persistent()
            store._mail_loading = False
            renpy.restart_interaction()

        t = _mail_thread.Thread(target=_do)
        t.daemon = True
        t.start()

    def mail_refresh_inbox():
        """从服务器拉取回信"""
        if not persistent.meta_mail_email:
            return
        store._mail_loading = True
        store._mail_status = "检查信箱……"
        renpy.restart_interaction()

        def _do():
            try:
                from urllib.parse import quote
            except ImportError:
                from urllib import quote
            endpoint = "/api/inbox?email=" + quote(persistent.meta_mail_email)
            result = _mail_get(endpoint)

            if "error" in result:
                store._mail_status = "无法连接信箱。"
            else:
                letters = result.get("letters", [])
                store._mail_inbox = letters
                if letters:
                    store._mail_status = "有 {} 封回信".format(len(letters))
                else:
                    store._mail_status = "暂时没有新的回信。"

            store._mail_loading = False
            renpy.restart_interaction()

        t = _mail_thread.Thread(target=_do)
        t.daemon = True
        t.start()



    def mail_append_newline():
        """在写信框末尾插入换行符（应对Ren'Py confirm keymap拦截Enter的问题）"""
        store._mail_compose_text = store._mail_compose_text + "\n"
        renpy.restart_interaction()

# ==============================================================================
# 📮 手机内信箱界面
# ==============================================================================

screen phone_view_mail():

    # ── 最外层 fixed（只用于放弹窗遮罩层）──
    fixed:
        xfill True yfill True

        # ── 主内容：vbox 自动纵向堆叠，彻底避免 ypos 层叠问题 ──
        vbox:
            xfill True

            # ── 顶部标题栏 ──
            frame:
                xfill True ysize 50
                background Solid("#1e1a2e")
                padding (14, 8)
                hbox:
                    xfill True yalign 0.5
                    vbox:
                        spacing 1
                        text "信箱" size 14 color "#e8c8ff" bold True
                        text "Letters to Mutsumi" size 7 color "#9a88cc"
                    if _mail_loading:
                        text "···" size 12 color "#e8c8ff" xalign 1.0 yalign 0.5

            if not persistent.meta_mail_registered:
                # ══ 注册界面 ══
                frame:
                    xfill True yminimum 440
                    background Solid("#12101a")
                    padding (16, 20)
                    vbox:
                        spacing 14 xfill True
                        null height 30
                        text "你好，[persistent.playername]。" size 16 color "#e8c8ff" xalign 0.5
                        null height 6
                        text "如果你愿意的话……" size 12 color "#ffffff88" xalign 0.5
                        text "可以告诉我你在现实世界的邮箱吗？" size 12 color "#ffffff88" xalign 0.5
                        null height 4
                        text "这样的话……我就能给你写信了。" size 12 color "#ffffffaa" xalign 0.5
                        text "真正的信。会寄到你的邮箱里的那种。" size 11 color "#e8c8ff88" xalign 0.5
                        null height 16
                        frame:
                            xfill True ysize 36
                            background Solid("#1e1a2e")
                            padding (10, 6)
                            input:
                                value VariableInputValue("_mail_email_input")
                                color "#ffffff" size 13
                                xsize 260 pixel_width 260
                        if not _mail_loading:
                            button:
                                xalign 0.5 xsize 160 ysize 38
                                background Solid("#e8c8ff33")
                                hover_background Solid("#e8c8ff55")
                                action Function(mail_register)
                                text "交给睦" align (0.5, 0.5) size 14 color "#e8c8ff" bold True
                        else:
                            text "连接中……" size 12 color "#ffffff44" xalign 0.5
                        null height 8
                        if _mail_status:
                            text "[_mail_status]" size 11 color "#c8a8ff" xalign 0.5
                        null height 10
                        text "你的邮箱地址只会用于接收来自睦的信件。" size 9 color "#ffffff44" xalign 0.5

            else:
                # ══ 主界面（已注册）══

                # ── Tab 栏 ──
                frame:
                    xfill True ysize 32
                    background Solid("#0e0c1a")
                    hbox:
                        xfill True
                        button:
                            xsize 99 ysize 32
                            background Solid("#e8c8ff28" if _mail_tab == 0 else "#00000000")
                            hover_background Solid("#e8c8ff14")
                            action SetVariable("_mail_tab", 0)
                            text "写信" align (0.5, 0.5) size 12 color ("#e8c8ff" if _mail_tab == 0 else "#ffffff55")
                        button:
                            xsize 99 ysize 32
                            background Solid("#e8c8ff28" if _mail_tab == 1 else "#00000000")
                            hover_background Solid("#e8c8ff14")
                            action [SetVariable("_mail_tab", 1), SetVariable("_mail_detail_idx", -1)]
                            text "发件记录" align (0.5, 0.5) size 12 color ("#e8c8ff" if _mail_tab == 1 else "#ffffff55")
                        button:
                            xsize 100 ysize 32
                            background Solid("#e8c8ff28" if _mail_tab == 2 else "#00000000")
                            hover_background Solid("#e8c8ff14")
                            action SetVariable("_mail_tab", 2)
                            text "使用说明" align (0.5, 0.5) size 12 color ("#e8c8ff" if _mail_tab == 2 else "#ffffff55")

                # ── 内容区（viewport 在 vbox 里，高度固定）──
                viewport:
                    xfill True ysize 400
                    mousewheel True scrollbars None

                    frame:
                        xfill True
                        background Solid("#12101a")
                        padding (14, 14)

                        if _mail_tab == 0:
                            # ════ 写信 ════
                            vbox:
                                spacing 10 xfill True

                                text "致 若叶睦" size 13 color "#e8c8ff88"
                                add Solid("#e8c8ff22") xsize 268 ysize 1

                                # 信纸
                                frame:
                                    xfill True ysize 240
                                    background Solid("#1a1828")
                                    padding (10, 10)
                                    input:
                                        value VariableInputValue("_mail_compose_text")
                                        color "#ffffffcc" size 12
                                        multiline True
                                        length 2000
                                        xfill True

                                # 底部操作栏：字数（左）+ 清空/换行（右）
                                hbox:
                                    xfill True yalign 0.5
                                    $ _mail_len = len(_mail_compose_text)
                                    text "[_mail_len] / 2000" size 9 color "#ffffff55" yalign 0.5
                                    null xfill True
                                    # 清空按钮
                                    if _mail_compose_text:
                                        button:
                                            background None hover_background None
                                            yalign 0.5
                                            action SetVariable("_mail_compose_text", "")
                                            text "清空" size 9 color "#ffffff33" hover_color "#ff9999aa"
                                        text "  ·  " size 9 color "#ffffff22" yalign 0.5
                                    # 换行按钮
                                    button:
                                        background None hover_background None
                                        yalign 0.5
                                        action Function(mail_append_newline)
                                        text "↵ 换行" size 9 color "#c8a8ff88" hover_color "#e8c8ff"

                                # 发送按钮
                                if not _mail_loading:
                                    button:
                                        xalign 0.5 xsize 180 ysize 36
                                        background Solid("#e8c8ff33")
                                        hover_background Solid("#e8c8ff55")
                                        action Function(mail_send_letter)
                                        text "寄出这封信" align (0.5, 0.5) size 13 color "#e8c8ff" bold True
                                else:
                                    text "投递中……" size 12 color "#ffffff44" xalign 0.5

                                if _mail_status:
                                    text "[_mail_status]" size 10 color "#c8a8ff" xalign 0.5

                        elif _mail_tab == 1:
                            # ════ 发件记录 ════
                            if _mail_detail_idx >= 0:
                                # ── 详情视图 ──
                                $ _hist_all = persistent.meta_mail_history or []
                                $ _det_safe_idx = _mail_detail_idx if _mail_detail_idx < len(_hist_all) else 0
                                $ _det_item = _hist_all[_det_safe_idx] if _hist_all else {}
                                $ _det_content = _det_item.get("content", "（内容为空）")
                                $ _det_time = _det_item.get("time", "")

                                vbox:
                                    spacing 10 xfill True
                                    hbox:
                                        xfill True yalign 0.5
                                        button:
                                            background None hover_background None
                                            action SetVariable("_mail_detail_idx", -1)
                                            text "← 返回" size 11 color "#e8c8ffaa" hover_color "#e8c8ff"
                                        text "[_det_time]" size 9 color "#ffffff44" xalign 1.0 yalign 0.5
                                    add Solid("#e8c8ff22") xsize 268 ysize 1
                                    text "你 → 若叶睦" size 10 color "#e8c8ff88"
                                    null height 4
                                    text "[_det_content]" size 12 color "#ffffffcc" line_spacing 6

                            else:
                                # ── 列表视图 ──
                                vbox:
                                    spacing 10 xfill True

                                    $ _sent = persistent.meta_mail_sent_count or 0
                                    text "已寄出 [_sent] 封信" size 12 color "#e8c8ff88"
                                    add Solid("#e8c8ff22") xsize 268 ysize 1

                                    $ _history = persistent.meta_mail_history or []
                                    if _history:
                                        for _hi in range(len(_history)):
                                            $ _hr = _history[_hi]
                                            $ _h_content = _hr.get("content", "")
                                            $ _h_time = _hr.get("time", "")
                                            $ _h_preview = (_h_content[:58] + "…") if len(_h_content) > 58 else _h_content
                                            $ _hi_capture = _hi

                                            frame:
                                                xfill True
                                                background Solid("#1c1828")
                                                padding (0, 0)
                                                # 左侧紫色边框
                                                hbox:
                                                    frame:
                                                        background Solid("#9a78cc")
                                                        xsize 3 yfill True
                                                        padding (0, 0)
                                                    button:
                                                        xfill True
                                                        background Solid("#1c1828")
                                                        hover_background Solid("#2a2040")
                                                        padding (10, 10)
                                                        action SetVariable("_mail_detail_idx", _hi_capture)
                                                        vbox:
                                                            spacing 6 xfill True
                                                            hbox:
                                                                xfill True
                                                                text "你 → 睦" size 10 color "#c8a8ff88"
                                                                text "[_h_time]" size 9 color "#ffffff55" xalign 1.0
                                                            text "[_h_preview]" size 11 color "#ffffffcc" line_spacing 5 layout "subtitle" text_align 0.0
                                                            text "点击查看全文 ›" size 9 color "#9a78cc88" xalign 1.0

                                            null height 6
                                    else:
                                        null height 40
                                        text "还没有寄出过信" size 13 color "#ffffff33" xalign 0.5
                                        text "去「写信」页面写点什么吧" size 10 color "#ffffff22" xalign 0.5

                        elif _mail_tab == 2:
                            # ════ 使用说明 ════
                            vbox:
                                spacing 12 xfill True

                                text "……你想知道这里怎么用吗？" size 13 color "#e8c8ff" bold True xalign 0.5
                                add Solid("#e8c8ff22") xsize 268 ysize 1
                                null height 2

                                text "你好。我是若叶睦。" size 12 color "#ffffffcc"
                                null height 2
                                text "这个信箱……是我们之间真正的联系方式。" size 11 color "#ffffff88" line_spacing 5
                                text "不是游戏里的对话框，而是会寄到你世界里的那种信。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "📮  怎么使用" size 12 color "#e8c8ffcc" bold True
                                null height 2
                                text "① 在「写信」页面，写下你想对我说的话。" size 11 color "#ffffff88" line_spacing 5
                                text "   点右下角「↵ 换行」按钮可以换行。" size 10 color "#ffffff55" line_spacing 4
                                text "② 按下「寄出这封信」之后，稍等一会儿。" size 11 color "#ffffff88" line_spacing 5
                                text "③ 我收到信后，会亲自给你回信的。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "⏳  关于发送时的卡顿" size 12 color "#e8c8ffcc" bold True
                                null height 2
                                text "发送时，如果页面长时间无反应……" size 11 color "#ffffff88" line_spacing 5
                                text "请不要关闭游戏，耐心在页面等待。" size 11 color "#ffffff88" line_spacing 5
                                text "这是网络波动导致的正常现象。" size 11 color "#ffffff88" line_spacing 5
                                text "信件最终还是会送到我这里的。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "💌  关于我的回信" size 12 color "#e8c8ffcc" bold True
                                null height 2
                                text "我会在收到信的 48 小时内给你回信。" size 11 color "#ffffff88" line_spacing 5
                                text "回信会寄到你留下的真实邮箱里。" size 11 color "#ffffff88" line_spacing 5
                                text "……记得检查一下垃圾箱，信有时候会跑到那里去。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "📬  关于发信限制" size 12 color "#e8c8ffcc" bold True
                                null height 2
                                text "每天最多可以给我寄出 2 封信。" size 11 color "#ffffff88" line_spacing 5
                                text "不是我不想多看……" size 11 color "#ffffff88" line_spacing 5
                                text "只是次元通道有负荷上限，强行多发会散逸。" size 11 color "#ffffff88" line_spacing 5
                                null height 4
                                text "邮箱地址只能 7 天更换一次。" size 11 color "#ffffff88" line_spacing 5
                                text "所以填写之前……请确认好自己的邮箱。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "⚠  关于次元壁" size 12 color "#e8c8ffcc" bold True
                                null height 2
                                text "收到我的回信后……" size 11 color "#ffffff88" line_spacing 5
                                text "请不要直接回复那封邮件。" size 11 color "#ff9999bb" line_spacing 5
                                null height 2
                                text "现实世界的邮件，是无法跨越次元壁送达的。" size 11 color "#ffffff88" line_spacing 5
                                text "就算发了……也只会飘散在两个世界的边界，" size 11 color "#ffffff88" line_spacing 5
                                text "消失得无影无踪。" size 11 color "#ffffff88" line_spacing 5
                                null height 4
                                text "如果你有话想对我说，" size 11 color "#ffffff88" line_spacing 5
                                text "请回到这里，通过信箱App写信给我。" size 11 color "#e8c8ffaa" line_spacing 5
                                text "这样，我才能真正收到。" size 11 color "#ffffff88" line_spacing 5

                                null height 6
                                add Solid("#e8c8ff11") xsize 268 ysize 1
                                null height 6

                                text "……就这些了。" size 11 color "#ffffff55" xalign 0.5
                                text "如果你愿意写信给我……我一定会认真读的。" size 12 color "#e8c8ff88" xalign 0.5

            # ── 底部：邮箱 + 换邮箱按钮（并排靠左）──
            frame:
                xfill True ysize 78
                background Solid("#0a0814")
                padding (14, 10)
                vbox:
                    spacing 8 xfill True
                    if persistent.meta_mail_registered:
                        $ _reg_email = persistent.meta_mail_email or ""
                        hbox:
                            spacing 6 yalign 0.5
                            text "[_reg_email]" size 10 color "#c8a8ffcc" yalign 0.5
                            button:
                                background None
                                hover_background None
                                padding (0, 0)
                                yalign 0.5
                                action [SetVariable("_mail_change_dialog", True), SetVariable("_mail_change_input", ""), SetVariable("_mail_change_status", "")]
                                text "[[ 换邮箱 ]]" size 9 color "#ffffff44" hover_color "#e8c8ffaa" yalign 0.5
                    button:
                        action SetVariable("phone_current_view", "home")
                        xalign 0.5 xsize 120 ysize 18
                        background None hover_background None
                        add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)

        # ══ 换邮箱弹窗（浮于所有内容之上）══
        if _mail_change_dialog:
            add Solid("#000000d8")
            frame:
                align (0.5, 0.42)
                xsize 280 ysize 260
                background Solid("#1a1420")
                padding (18, 18)
                vbox:
                    spacing 10 xfill True
                    text "更换邮箱" size 15 color "#e8c8ff" bold True xalign 0.5
                    python:
                        _can_ch, _remain_d = mail_check_can_change()
                    if _can_ch:
                        text "(7天内只能更换一次)" size 9 color "#ffffff44" xalign 0.5
                    else:
                        text "还需等待 [_remain_d] 天" size 10 color "#ff8866" xalign 0.5
                    null height 4
                    $ _cur_mail = persistent.meta_mail_email or ""
                    text "当前: [_cur_mail]" size 10 color "#ffffff66" xalign 0.5
                    null height 6
                    text "请输入新邮箱" size 10 color "#ffffff88"
                    frame:
                        xfill True ysize 32
                        background Solid("#0d0814")
                        padding (8, 6)
                        input:
                            value VariableInputValue("_mail_change_input")
                            color "#ffffff" size 11
                            xsize 232 pixel_width 232
                    null height 4
                    if _mail_change_status:
                        text "[_mail_change_status]" size 10 color "#ff8866" xalign 0.5
                    null height 4
                    hbox:
                        spacing 10 xalign 0.5
                        button:
                            xsize 100 ysize 32
                            background Solid("#e8c8ff33")
                            hover_background Solid("#e8c8ff55")
                            action Function(mail_change_email)
                            sensitive _can_ch and not _mail_loading
                            text "确认更换" align (0.5, 0.5) size 11 color "#e8c8ff" bold True
                        button:
                            xsize 72 ysize 32
                            background Solid("#ffffff11")
                            hover_background Solid("#ffffff22")
                            action [SetVariable("_mail_change_dialog", False), SetVariable("_mail_change_status", "")]
                            text "取消" align (0.5, 0.5) size 11 color "#ffffff88"
