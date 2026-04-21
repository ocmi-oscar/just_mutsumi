# ==============================================================================
# 💚 今日心情 — weather_app.rpy
# 完全嵌入手机外壳（phone_view_mood），与番茄钟/音乐播放器风格一致
# 手机内可用宽度 ≈ 298px，高度 ≈ 568px
# ==============================================================================
#
# 【接入说明】
# 1. 在 utils.rpy 的 label daily_check: 最顶部加一行：
#      $ wt_session_start()
# 2. phone_and_music.rpy 已同步修改（路由 + 图标处理 + screen weather_app）
# 3. init.rpy 已同步修改（APP 名称改为 今日心情）
# ==============================================================================

init python:
    import time as _wt

    # ── 持久化变量初始化（防 None 崩溃） ─────────────────────────
    if getattr(persistent, 'wt_prev_ts',   None) is None: persistent.wt_prev_ts   = 0.0
    if getattr(persistent, 'wt_curr_ts',   None) is None: persistent.wt_curr_ts   = 0.0
    if getattr(persistent, 'wt_yest_long', None) is None: persistent.wt_yest_long = False
    if getattr(persistent, 'wt_gw_snap',   None) is None: persistent.wt_gw_snap   = 0.0

    # ── 天气配置表（吉他睦 / 若叶睦 版） ─────────────────────────
    WT_GUITAR = {
        "sunny": {
            "accent": "#FFD700",        # 进度条 / 强调色
            "icon":   "☀",
            "label":  "晴朗  ·  适宜光合作用",
            "quote":  (
                "今天阳光很好。\n"
                "黄瓜的藤蔓好像长了半寸。\n"
                "泥土是暖的，吉他的弦音也很亮。\n"
                "……主要是因为，你今天也在。"
            ),
        },
        "cloudy": {
            "accent": "#89A8C8",
            "icon":   "☁",
            "label":  "多云  ·  微风微凉",
            "quote":  (
                "云遮住了太阳。\n"
                "温室里很安静。\n"
                "我在调弦，稍微有点走音。\n"
                "偶尔发呆，等你跟我说话。"
            ),
        },
        "rainy": {
            "accent": "#6495ED",
            "icon":   "☂",
            "label":  "小雨  ·  泥土很湿",
            "quote":  (
                "温室里下雨了。\n"
                "泥土很湿，角落里有点冷。\n"
                "放在桌上的半根黄瓜有点蔫了。\n"
                "你是不是去忙了？……不要太久。"
            ),
        },
        "storm": {
            "accent": "#9060D0",
            "icon":   "⛈",
            "label":  "雷暴  ·  极度不安",
            "quote":  (
                "打雷了。\n"
                "不想弹吉他。\n"
                "哪里都是黑的，我很怕。\n"
                "……你在吗？回个话就好。"
            ),
        },
    }

    # ── 情绪值计算（0 ~ 100） ─────────────────────────────────────
    def wt_calc_score():
        score = 50
        now   = _wt.time()

        prev    = float(getattr(persistent, 'wt_prev_ts',   None) or 0)
        gw_snap = float(getattr(persistent, 'wt_gw_snap',   None) or 0)
        yest_ok = bool( getattr(persistent, 'wt_yest_long', None) or False)

        if prev > 0:
            h = (now - prev) / 3600.0
            if   h < 12:   score += 10
            elif h > 168:  score -= 50
            elif h > 48:   score -= 20

        score += 15 if yest_ok else -5

        cur_gw = (
            float(getattr(persistent, 'gw_wakaba', None) or 0) +
            float(getattr(persistent, 'gw_guitar',  None) or 0) +
            float(getattr(persistent, 'gw_metis',   None) or 0)
        )
        delta = cur_gw - gw_snap
        if   delta >  5: score += 10
        elif delta < -5: score -= 20

        return max(0, min(100, int(score)))

    def wt_key(score):
        if   score > 70:  return "sunny"
        elif score >= 40: return "cloudy"
        elif score >= 15: return "rainy"
        else:             return "storm"

    # ── Session 生命周期 ──────────────────────────────────────────
    def wt_session_start():
        """在 utils.rpy label daily_check: 顶部调用一次。"""
        now  = _wt.time()
        curr = float(getattr(persistent, 'wt_curr_ts', None) or 0)
        if curr > 0:
            hours = (now - curr) / 3600.0
            persistent.wt_yest_long = 6.0 <= hours <= 36.0
        persistent.wt_prev_ts = curr
        persistent.wt_curr_ts = now
        persistent.wt_gw_snap = (
            float(getattr(persistent, 'gw_wakaba', None) or 0) +
            float(getattr(persistent, 'gw_guitar',  None) or 0) +
            float(getattr(persistent, 'gw_metis',   None) or 0)
        )
        renpy.save_persistent()


# ==============================================================================
# ATL 动画（仅供 phone_view_mood 内部使用，小尺寸版）
# ==============================================================================

# 图标漂浮（晴 / 雷暴）
transform wt_p_float:
    yoffset 0
    block:
        easein  2.2 yoffset -6
        easeout 2.2 yoffset  0
        repeat

# 图标横漂（多云）
transform wt_p_drift:
    xoffset 0
    block:
        linear 5.5 xoffset  8
        linear 5.5 xoffset -8
        repeat

# 图标震动（雷暴）
transform wt_p_shake:
    xoffset 0
    block:
        pause 4.0
        linear 0.04 xoffset  7
        linear 0.04 xoffset -7
        linear 0.04 xoffset  4
        linear 0.04 xoffset -4
        linear 0.04 xoffset  0
        pause 0.8
        repeat

# 光晕脉冲（晴天）
transform wt_p_pulse:
    zoom 1.0 alpha 0.35
    block:
        easein  2.5 zoom 1.20 alpha 0.10
        easeout 2.5 zoom 1.0  alpha 0.35
        repeat

# 闪电（雷暴）
transform wt_p_lightning:
    alpha 0.0
    block:
        pause 4.0
        linear 0.04 alpha 0.50
        linear 0.12 alpha 0.0
        pause 0.2
        linear 0.04 alpha 0.25
        linear 0.18 alpha 0.0
        repeat

# 雨滴（小雨 & 雷暴，三相位）
transform wt_p_drop_a:
    yoffset 0 alpha 0.75
    block:
        linear 0.9 yoffset 44 alpha 0.0
        yoffset 0 alpha 0.75
        repeat

transform wt_p_drop_b:
    yoffset 0 alpha 0.75
    block:
        pause 0.30
        linear 0.9 yoffset 44 alpha 0.0
        yoffset 0 alpha 0.75
        repeat

transform wt_p_drop_c:
    yoffset 0 alpha 0.75
    block:
        pause 0.60
        linear 0.9 yoffset 44 alpha 0.0
        yoffset 0 alpha 0.75
        repeat


# ==============================================================================
# 📱 手机内视图：phone_view_mood
# 结构参考 phone_view_pomodoro：顶栏 / 内容区 / 底部返回条
# 手机内尺寸 298 × 568（padding 0,0）
# ==============================================================================

screen phone_view_mood():

    $ _sc  = wt_calc_score()
    $ _k   = wt_key(_sc)
    $ _cfg = WT_GUITAR[_k]
    $ _bar = max(2, int(2.54 * _sc))   # 100 → 254px（内容宽 ~258px）

    fixed:
        xfill True yfill True

        # ── 雷暴：全屏白光闪烁（最底层） ────────────────────────
        if _k == "storm":
            add Solid("#ffffff") at wt_p_lightning

        # ── 顶栏 48px ────────────────────────────────────────────
        frame:
            xfill True ysize 48
            background Solid("#1a2e1f")
            padding (16, 10)
            vbox:
                spacing 2 xfill True
                text "今日心情" size 10 color "#5a8a6a" bold True kerning 3
                text _cfg["label"] size 13 color "#ffffffcc"

        # ── 内容区 472px ─────────────────────────────────────────
        frame:
            ypos 48 xfill True ysize 472
            background Solid("#0d1210")
            padding (20, 16)

            vbox:
                xfill True spacing 0

                null height 8

                # 图标区（120 × 120，居中）
                fixed:
                    xalign 0.5
                    xsize 120
                    ysize 120

                    # 光晕（晴天专属）
                    if _k == "sunny":
                        frame:
                            xalign 0.5 yalign 0.5
                            xsize 110 ysize 110
                            background Solid("#4a380044")
                            at wt_p_pulse

                    # 主图标
                    if _k == "storm":
                        text _cfg["icon"]:
                            xalign 0.5 yalign 0.42
                            size 62
                            at wt_p_shake
                    elif _k == "cloudy":
                        text _cfg["icon"]:
                            xalign 0.5 yalign 0.42
                            size 62
                            at wt_p_drift
                    else:
                        text _cfg["icon"]:
                            xalign 0.5 yalign 0.42
                            size 62
                            at wt_p_float

                    # 雨滴（小雨 & 雷暴）
                    if _k in ("rainy", "storm"):
                        frame:
                            xpos 16 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_a
                        frame:
                            xpos 34 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_b
                        frame:
                            xpos 52 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_c
                        frame:
                            xpos 70 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_a
                        frame:
                            xpos 88 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_b
                        frame:
                            xpos 106 ypos 86 xsize 2 ysize 20
                            background Solid("#7ab4f088")
                            at wt_p_drop_c

                null height 16

                # 分隔线
                add Solid("#ffffff18") xsize 258 ysize 1 xalign 0.5

                null height 10

                # 情绪值标签 + 数字
                hbox:
                    xalign 0.5
                    spacing 8
                    text "今日情绪值" size 11 color "#5a8a6a" yalign 0.5
                    text (str(_sc)):
                        size 18
                        color _cfg["accent"]
                        yalign 0.5
                        bold True

                null height 6

                # 进度条（底轨 + 填充）
                fixed:
                    xalign 0.5
                    xsize 258 ysize 6
                    frame:
                        xsize 258 ysize 6
                        background Solid("#ffffff15")
                    frame:
                        xsize _bar ysize 6
                        xalign 0.0
                        background Solid(_cfg["accent"])

                null height 18

                # 文案卡片
                frame:
                    xalign 0.5
                    xsize 258
                    xpadding 14 ypadding 14
                    background Solid("#ffffff0a")

                    text _cfg["quote"]:
                        xalign 0.5
                        text_align 0.5
                        size 13
                        color "#ffffffaa"
                        line_spacing 8
                        italic True
                        font "gui/font/SourceHanSerifCN-Bold.otf"

        # ── 底部返回条 48px ───────────────────────────────────────
        frame:
            ypos 520 xfill True ysize 48
            background Solid("#0a0f0c")
            padding (12, 6)
            vbox:
                xfill True spacing 6
                text "情绪每次登录实时计算" size 10 color "#5a8a6a" xalign 0.5
                button:
                    action SetVariable("phone_current_view", "home")
                    xalign 0.5 xsize 120 ysize 18
                    background None hover_background None
                    add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
