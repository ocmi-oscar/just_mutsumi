# ==============================================================================
# 📱 手机系统 v5
# 修复：图标灰掉、小游戏布局、游戏结束回归
# ==============================================================================

default phone_current_view = "home"

# ============================================================
# 动画
# ============================================================

transform phone_slide_up:
    on show:
        yoffset 500 alpha 0.0 zoom 0.9
        easein_back 0.45 yoffset 0 alpha 1.0 zoom 1.0
    on hide:
        easeout_quint 0.3 yoffset 300 alpha 0.0 zoom 0.92

transform phone_overlay_fade:
    on show:
        alpha 0.0
        easein_cubic 0.3 alpha 1.0
    on hide:
        easeout_cubic 0.2 alpha 0.0

transform app_icon_press:
    on idle:
        zoom 1.0
    on hover:
        easein_cubic 0.15 zoom 1.08

transform now_playing_pulse:
    block:
        easein_cubic 1.0 zoom 1.04 alpha 0.7
        easeout_cubic 1.0 zoom 1.0 alpha 1.0
        repeat

transform song_item_in(i):
    alpha 0.0 xoffset 40
    pause (i * 0.03)
    easein_quint 0.3 alpha 1.0 xoffset 0

transform game_card_in(i):
    alpha 0.0 yoffset 30
    pause (i * 0.08)
    easein_quint 0.35 alpha 1.0 yoffset 0


# ============================================================
# 辅助函数
# ============================================================

init python:
    def start_game_from_phone(game_label):
        store.phone_open = False
        store.phone_current_view = "home"
        store.quick_menu = False
        renpy.hide_screen("main_interaction_ui")
        renpy.hide_screen("phone_system")
        if 'diary_log_game' in dir(store):
            diary_log_game()
        renpy.jump(game_label)


# ============================================================
# 📱 手机主界面
# ============================================================

screen phone_system():
    zorder 100

    # ★ 修复：is_locked 只控制手机呼出按钮，不传入手机内部 ★
    $ _phone_locked = (
        renpy.get_screen("say") or
        renpy.get_screen("choice") or
        talking_to_mutsumi
    )

    # 番茄钟后台
    if p_running:
        timer 1.0 action Function(p_tick_logic) repeat True
        button:
            align (0.98, 0.02)
            background Solid("#1a2e1fdd")
            hover_background Solid("#2a4e2fdd")
            padding (14, 8)
            action [SetVariable("phone_open", True), SetVariable("phone_current_view", "pomodoro")]
            hbox:
                spacing 10
                text "FOCUS" size 11 color "#5a8a6a" bold True yalign 0.5
                $ _pm, _ps = divmod(p_time, 60)
                text "[_pm:02d]:[_ps:02d]" size 20 color "#95e1d3" yalign 0.5 font "DejaVuSans.ttf"

    # 呼出图标 — 对话中禁用
    imagebutton:
        idle "images/phone/entry_icon.png"
        hover "images/phone/entry_icon_hover.png"
        align (0.98, 0.99)
        action [SetVariable("phone_current_view", "home"), ToggleVariable("phone_open")]
        sensitive not _phone_locked
        at transform:
            zoom 0.35
            alpha (0.4 if _phone_locked else 1.0)

    showif phone_open:
        button:
            action [SetVariable("phone_open", False), SetVariable("phone_current_view", "home")]
            background Solid("#00000044")
            at phone_overlay_fade
            xfill True yfill True

    showif phone_open:
        # 对话出现时自动关闭手机
        if _phone_locked:
            timer 0.01 action SetVariable("phone_open", False)

        frame:
            at phone_slide_up
            align (0.99, 0.95)
            xsize 310 ysize 580
            background Solid("#1a1a1a")
            padding (6, 6)

            frame:
                xfill True yfill True
                if phone_current_view == "home":
                    background Frame(Image(persistent.phone_bg), 10, 10)
                else:
                    background Solid("#0d1210f5")
                padding (0, 0)

                fixed:
                    xfill True yfill True
                    if phone_current_view == "home":
                        use phone_view_home
                    elif phone_current_view == "music":
                        use phone_view_music
                    elif phone_current_view == "pomodoro":
                        use phone_view_pomodoro
                    elif phone_current_view == "games":
                        use phone_view_games
                    elif phone_current_view == "browser":
                        use phone_view_browser
                    elif phone_current_view == "calendar":
                        use phone_view_calendar
                    elif phone_current_view == "todo":
                        use phone_view_todo
                    elif phone_current_view == "diary":
                        use phone_view_diary
                    elif phone_current_view == "milestone":
                        use phone_view_milestone
                    elif phone_current_view == "persona":
                        use phone_view_persona
                    elif phone_current_view == "custom":
                        use phone_view_custom
                    elif phone_current_view == "greenhouse":
                        use phone_view_greenhouse
                    elif phone_current_view == "whitenoise":
                        use phone_view_whitenoise
                    elif phone_current_view == "weather":
                        use phone_view_weather
                    elif phone_current_view == "mail":
                        use phone_view_mail
                    elif phone_current_view == "fortune":
                        use phone_view_fortune
                    elif phone_current_view == "capsule":
                        use phone_view_capsule
                    elif phone_current_view == "roundtable":
                        use phone_view_roundtable
                    elif phone_current_view == "shop":
                        use phone_view_shop
                    elif phone_current_view == "farm":
                        use phone_view_farm
                    elif phone_current_view == "mood":
                        use phone_view_mood


# ============================================================
# 📱 新增 App 注册
# ============================================================

init python:
    # 在原 phone_apps 列表末尾追加新 App（在开发者面板之前插入）
    _new_apps = [
        App("个性化", "images/phone/icon_gxh.png", NullAction()),
        App("设置", "images/phone/icon_setting.png", NullAction()),
        App("M-Search", "images/phone/icon_llq.png", NullAction()),
        App("白噪音", "images/phone/icon_asmr.png", NullAction()),
        App("温室备忘录", "images/phone/icon_greenhouse_todo.png", NullAction()),
        App("天气", "images/phone/icon_weather.png", NullAction()),
        App("信箱", "images/phone/icon_mail.png", NullAction()),
        App("占卜", "images/phone/icon_fortune.png", NullAction()),
        App("时间胶囊", "images/phone/icon_capsule.png", NullAction()),
        App("商店", "images/phone/icon_shop.png", NullAction()),
        App("温室", "images/phone/icon_farm.png", NullAction()),
        App("桌宠", "images/phone/icon_pet.png", NullAction()),
        App("圆桌会议", "images/phone/icon_roundtable.png", NullAction()),
    ]
    # 找到开发者面板的位置，在它前面插入
    _dev_idx = None
    for _i, _a in enumerate(phone_apps):
        if _a.is_dev:
            _dev_idx = _i
            break
    if _dev_idx is not None:
        for _j, _na in enumerate(_new_apps):
            phone_apps.insert(_dev_idx + _j, _na)
    else:
        phone_apps.extend(_new_apps)


# ============================================================
# 🏠 主屏（双页滑动）
# ============================================================

default _phone_page = 0

init python:
    # App名→视图路由映射（统一管理）
    PHONE_VIEW_MAP = {
        "音乐": "music",
        "番茄钟": "pomodoro",
        "小游戏": "games",
        "M-Search": "browser",
        "日历": "calendar",
        "待办清单": "todo",
        "今日心情": "mood",
        "睦の日记": "diary",
        "好感度": "milestone",
        "切换人格": "persona",
        "个性化": "custom",
        "白噪音": "whitenoise",
        "温室备忘录": "greenhouse",
        "天气": "weather",
        "信箱": "mail",
        "占卜": "fortune",
        "时间胶囊": "capsule",
        "商店": "shop",
        "温室": "farm",
    }

    PHONE_APPS_PER_PAGE = 20

    def phone_app_action(app_name):
        """统一处理App点击"""
        if app_name in PHONE_VIEW_MAP:
            store.phone_current_view = PHONE_VIEW_MAP[app_name]
            renpy.restart_interaction()
        elif app_name == "设置":
            store.phone_open = False
            store.phone_current_view = "home"
            renpy.run(ShowMenu("preferences"))
        elif app_name == "桌宠":
            renpy.run(Show("coming_soon_popup", app_name="桌宠"))
        elif app_name == "圆桌会议":
            renpy.run(Show("coming_soon_popup", app_name="圆桌会议"))
        else:
            for a in phone_apps:
                if a.name == app_name:
                    store.phone_open = False
                    store.phone_current_view = "home"
                    renpy.run(a.action)
                    return

    def phone_get_visible_apps():
        """获取可见App列表（排除隐藏的开发者面板）"""
        return [a for a in phone_apps if not a.is_dev or persistent.developer_mode]

    def phone_get_page_count():
        apps = phone_get_visible_apps()
        return max(1, -(-len(apps) // PHONE_APPS_PER_PAGE))

    def phone_switch_page(direction):
        total = phone_get_page_count()
        store._phone_page = (store._phone_page + direction) % total
        renpy.restart_interaction()

# 页面切换动画
transform phone_page_slide_left:
    xoffset 310
    easeout 0.3 xoffset 0

transform phone_page_slide_right:
    xoffset -310
    easeout 0.3 xoffset 0

screen phone_view_home():
    default _slide_dir = 0  # -1=向左滑(切到右页), 1=向右滑(切到左页)

    $ _visible_apps = phone_get_visible_apps()
    $ _total_pages = phone_get_page_count()
    $ _cur_page = min(_phone_page, _total_pages - 1)
    $ _page_start = _cur_page * PHONE_APPS_PER_PAGE
    $ _page_end = min(_page_start + PHONE_APPS_PER_PAGE, len(_visible_apps))
    $ _page_apps = _visible_apps[_page_start:_page_end]

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 30
            background None
            padding (10, 4)
            text "[persistent.playername]与睦的手机" size 10 color "#ffffffaa" yalign 0.5

        add Solid("#ffffff22") xsize 280 ysize 1 xalign 0.5 ypos 30

        # 左右翻页按钮（覆盖整个左右两侧区域）
        if _cur_page > 0:
            button:
                xpos 0 ypos 36 xsize 50 ysize 480
                background Solid("#ffffff08")
                hover_background Solid("#ffffff15")
                action [SetScreenVariable("_slide_dir", 1), Function(phone_switch_page, -1)]
                text "‹" align (0.5, 0.5) size 36 color "#ffffff33"

        if _cur_page < _total_pages - 1:
            button:
                xpos 248 ypos 36 xsize 50 ysize 480
                background Solid("#ffffff08")
                hover_background Solid("#ffffff15")
                action [SetScreenVariable("_slide_dir", -1), Function(phone_switch_page, 1)]
                text "›" align (0.5, 0.5) size 36 color "#ffffff33"

        # App网格（带切换动画）
        frame:
            ypos 36 xfill True ysize 480
            background None
            padding (8, 4)

            key "K_LEFT" action [SetScreenVariable("_slide_dir", 1), Function(phone_switch_page, -1)]
            key "K_RIGHT" action [SetScreenVariable("_slide_dir", -1), Function(phone_switch_page, 1)]

            fixed:
                xfill True yfill True
                # 根据滑动方向选择动画
                if _slide_dir == -1:
                    at phone_page_slide_left
                elif _slide_dir == 1:
                    at phone_page_slide_right

                vpgrid:
                    cols 4 spacing 4 xalign 0.5 yoffset 6

                    for _app in _page_apps:
                        $ _aname = _app.name
                        vbox:
                            spacing 3 xsize 62
                            imagebutton:
                                idle Transform(_app.icon, size=(46, 46))
                                action Function(phone_app_action, _aname)
                                xalign 0.5
                                at app_icon_press
                            text _app.name size 10 xalign 0.5 text_align 0.5 color "#fff"

        # 页面指示器（小圆点）
        hbox:
            xalign 0.5 ypos 525
            spacing 8

            for _pi in range(_total_pages):
                button:
                    if _pi == _cur_page:
                        xsize 18 ysize 6
                        background Solid("#ffffffcc")
                    else:
                        xsize 6 ysize 6
                        background Solid("#ffffff44")
                    hover_background Solid("#ffffff88")
                    action [SetScreenVariable("_slide_dir", -1 if _pi > _cur_page else 1), SetVariable("_phone_page", _pi)]


# ============================================================
# 🎵 音乐
# ============================================================

screen phone_view_music():
    $ all_songs_data = get_music_files()
    if playlist_view == "fav":
        $ playlist = [s for s in all_songs_data if s["name"] in persistent.favorite_songs]
    else:
        $ playlist = all_songs_data
    $ is_paused = renpy.music.get_pause(channel='music')
    $ is_playing = (current_playing_song != "未在播放")

    fixed:
        xfill True yfill True

        frame:
            xfill True ysize 180 background Solid("#151f1a") padding (16, 14)
            vbox:
                spacing 6 xfill True
                hbox:
                    xfill True
                    text "MUSIC" size 12 color "#5a8a6a" bold True kerning 3 yalign 0.5
                    textbutton "导入" action Function(import_music_action) text_size 12 text_color "#5a8a6a" text_hover_color "#95e1d3" xalign 1.0 yalign 0.5
                null height 4
                if is_playing:
                    hbox:
                        spacing 8
                        frame:
                            yalign 0.5 xsize 6 ysize 6 background Solid("#95e1d3")
                            at now_playing_pulse
                        text "[current_playing_song]" size 14 color "#ffffff" bold True xsize 240
                else:
                    text "等待播放..." size 14 color "#ffffff44"
                null height 4
                if is_playing:
                    bar value AudioPositionValue(channel='music') xsize 265 ysize 3 left_bar Solid("#95e1d3") right_bar Solid("#ffffff15") thumb None
                else:
                    add Solid("#ffffff10") xsize 265 ysize 3
                null height 6
                hbox:
                    xalign 0.5 spacing 36
                    textbutton mode_names[play_mode] action SetVariable("play_mode", (play_mode + 1) % 3) text_size 13 text_color "#5a8a6a" text_hover_color "#95e1d3" yalign 0.5
                    if is_paused or not is_playing:
                        textbutton "▶" action Function(toggle_pause) text_size 26 text_color "#95e1d3" text_hover_color "#b8f0d8" yalign 0.5
                    else:
                        textbutton "||" action Function(toggle_pause) text_size 22 text_color "#95e1d3" text_hover_color "#b8f0d8" text_bold True yalign 0.5
                    textbutton "■" action [Stop("music"), SetVariable("current_playing_song", "未在播放")] text_size 18 text_color "#5a8a6a" text_hover_color "#ff6666" yalign 0.5

        hbox:
            ypos 180 xfill True
            button:
                action SetVariable("playlist_view", "base") xsize 149 ysize 34
                background Solid("#95e1d322" if playlist_view == "base" else "#00000000")
                hover_background Solid("#95e1d311")
                text "全部" align (0.5, 0.5) size 13 color ("#95e1d3" if playlist_view == "base" else "#5a8a6a") bold (playlist_view == "base")
            button:
                action SetVariable("playlist_view", "fav") xsize 149 ysize 34
                background Solid("#95e1d322" if playlist_view == "fav" else "#00000000")
                hover_background Solid("#95e1d311")
                text "收藏" align (0.5, 0.5) size 13 color ("#95e1d3" if playlist_view == "fav" else "#5a8a6a") bold (playlist_view == "fav")

        add Solid("#ffffff0a") ypos 214 xsize 298 ysize 1

        viewport id "music_vp":
            ypos 218 ysize 280 xfill True mousewheel True scrollbars None
            vbox:
                xfill True
                if not playlist:
                    null height 50
                    text "空无一物" size 14 color "#ffffff22" xalign 0.5
                else:
                    for idx, song_data in enumerate(playlist):
                        $ _fn = song_data["name"]
                        $ _cn = get_clean_song_name(song_data)
                        $ _is_cur = (current_playing_song == _cn)
                        $ _fav = _fn in persistent.favorite_songs
                        $ _star = "★" if _fav else "☆"
                        $ _star_color = "#ffd700" if _fav else "#555555"
                        hbox:
                            xfill True yminimum 42 spacing 6 at song_item_in(idx)
                            textbutton "[_star]" action Function(toggle_favorite, _fn) text_size 16 text_color _star_color text_hover_color "#ffd700" yalign 0.5 xsize 32 xoffset 8
                            textbutton "[_cn]" action [Function(play_user_music, song_data), SetVariable("current_playing_song", _cn)] text_size 12 text_color ("#95e1d3" if _is_cur else "#bbbbbb") text_hover_color "#ffffff" text_bold _is_cur yalign 0.5 xsize 200
                            if _is_cur:
                                text "♪" size 12 color "#95e1d3" yalign 0.5

        frame:
            ypos 502 xfill True ysize 66 background Solid("#0a0f0c") padding (12, 4)
            vbox:
                xfill True spacing 6
                hbox:
                    xfill True spacing 8
                    text "♪" size 12 color "#5a8a6a" yalign 0.5
                    bar value Preference("music volume") xsize 240 ysize 3 yalign 0.5 left_bar Solid("#95e1d3") right_bar Solid("#ffffff10") thumb None
                button:
                    action SetVariable("phone_current_view", "home")
                    xalign 0.5 xsize 120 ysize 18 background None hover_background None
                    add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 🍅 番茄钟
# ============================================================

screen phone_view_pomodoro():
    fixed:
        xfill True yfill True

        frame:
            xfill True ysize 80 background Solid("#1a2e1f") padding (16, 12)
            vbox:
                spacing 4 xfill True
                text "FOCUS" size 12 color "#5a8a6a" bold True kerning 3
                if not p_running:
                    text "静默成长" size 16 color "#ffffffcc"
                else:
                    text "汲取养分中..." size 16 color "#95e1d3" italic True

        frame:
            ypos 80 xfill True ysize 420 background Solid("#0d1210") padding (20, 20)
            vbox:
                xfill True spacing 16
                null height 10
                bar value p_time range p_target_time xsize 258 ysize 6 xalign 0.5 left_bar Solid("#95e1d3") right_bar Solid("#ffffff15") thumb None
                null height 5
                $ m, s = divmod(p_time, 60)
                text "[m:02d]:[s:02d]" size 72 color "#ffffff" xalign 0.5 font "DejaVuSans.ttf"
                null height 10

                if not p_running:
                    hbox:
                        xalign 0.5 spacing 8
                        text "时长(分):" size 13 color "#5a8a6a" yalign 0.5
                        input value VariableInputValue("p_custom_input") allow "0123456789" length 3 color "#fff" size 16 xsize 50
                        textbutton "应用" action Function(set_p_time_fix, p_custom_input) text_size 13 text_color "#5a8a6a" text_hover_color "#95e1d3" yalign 0.5
                    null height 10
                    hbox:
                        xalign 0.5 spacing 12
                        for preset in [("5", 5), ("10", 10), ("25", 25), ("45", 45), ("60", 60)]:
                            textbutton preset[0] action Function(set_p_time_fix, str(preset[1])) text_size 14 text_color ("#95e1d3" if p_target_time == preset[1] * 60 else "#5a8a6a") text_hover_color "#ffffff" xsize 40
                    null height 20
                    button:
                        action [SetVariable("p_running", True), SetVariable("phone_current_view", "home"), SetVariable("phone_open", False)]
                        xalign 0.5 xsize 200 ysize 44
                        background Solid("#95e1d3") hover_background Solid("#b8f0d8")
                        text "开始专注" align (0.5, 0.5) size 18 color "#0d1210" bold True
                else:
                    null height 20
                    hbox:
                        xalign 0.5 spacing 30
                        textbutton "暂停" action SetVariable("p_running", False) text_size 18 text_color "#95e1d3" text_hover_color "#b8f0d8"
                        textbutton "放弃" action [SetVariable("p_running", False), SetVariable("p_time", p_target_time)] text_size 18 text_color "#5a8a6a" text_hover_color "#ff6666"

        frame:
            ypos 504 xfill True ysize 64 background Solid("#0a0f0c") padding (12, 6)
            vbox:
                xfill True spacing 6
                if not p_running:
                    text "设定10分钟以上可获得好感度奖励" size 10 color "#5a8a6a" xalign 0.5
                else:
                    text "关闭手机后计时继续" size 10 color "#5a8a6a" xalign 0.5
                button:
                    action SetVariable("phone_current_view", "home")
                    xalign 0.5 xsize 120 ysize 18 background None hover_background None
                    add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 🎮 小游戏中心
# ============================================================

screen phone_view_games():
    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 48
            background Solid("#12121e")
            padding (16, 8)
            hbox:
                yalign 0.5 spacing 10
                text "▶" size 14 color "#7a6ad8" yalign 0.5
                vbox:
                    spacing 1
                    text "GAMES" size 10 color "#7a6ad8" bold True kerning 3
                    text "选择一个游戏" size 9 color "#ffffff55"

        # 游戏卡片列表
        viewport:
            ypos 50 ysize 462
            xfill True mousewheel True scrollbars None

            vbox:
                xfill True spacing 0

                # ── 无声传言 ──
                button:
                    action Function(start_game_from_phone, "start_silent_messenger_entry")
                    xfill True ysize 88
                    background Solid("#0d1210")
                    hover_background Solid("#162016")
                    padding (0, 0)
                    at game_card_in(0)
                    hbox:
                        add Solid("#95e1d3") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "无声传言" size 14 color "#95e1d3" bold True
                                text "Silent Messenger" size 8 color "#5a8a6a"
                                text "在土壤之下寻找被埋藏的种子。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 青苔棋局 ──
                button:
                    action Function(start_game_from_phone, "start_gomoku_difficulty")
                    xfill True ysize 88
                    background Solid("#0d1210")
                    hover_background Solid("#162016")
                    padding (0, 0)
                    at game_card_in(1)
                    hbox:
                        add Solid("#4a8a4a") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "青苔棋局" size 14 color "#95e1d3" bold True
                                text "Moss Chess" size 8 color "#5a8a6a"
                                text "和睦下一盘安静的五子棋。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 小睦快跑 ──
                button:
                    action Function(start_game_from_phone, "mutsumi_runner_start")
                    xfill True ysize 88
                    background Solid("#10101a")
                    hover_background Solid("#1a1a2a")
                    padding (0, 0)
                    at game_card_in(2)
                    hbox:
                        add Solid("#7a6ad8") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "小睦快跑" size 14 color "#b8a0ff" bold True
                                text "Mutsumi Runner" size 8 color "#6a5aaa"
                                text "黑白像素风五幕叙事跑酷。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 翻牌记忆 ──
                button:
                    action Function(start_game_from_phone, "start_memory_card_game")
                    xfill True ysize 88
                    background Solid("#0d1214")
                    hover_background Solid("#162026")
                    padding (0, 0)
                    at game_card_in(3)
                    hbox:
                        add Solid("#6ab8d8") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "翻牌记忆" size 14 color "#6ab8d8" bold True
                                text "Memory Cards" size 8 color "#4a8aaa"
                                text "翻开卡牌，找出成对的睦。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 小睦华容道 ──
                button:
                    action Function(start_game_from_phone, "start_sliding_puzzle")
                    xfill True ysize 88
                    background Solid("#0d1210")
                    hover_background Solid("#162016")
                    padding (0, 0)
                    at game_card_in(4)
                    hbox:
                        add Solid("#95e1d3") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "小睦华容道" size 14 color "#95e1d3" bold True
                                text "Mutsumi Puzzle" size 8 color "#5a8a6a"
                                text "把碎片拼回原来的样子。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── UNO!!! ──
                button:
                    action Function(start_game_from_phone, "start_uno_game")
                    xfill True ysize 88
                    background Solid("#12100d")
                    hover_background Solid("#2a2010")
                    padding (0, 0)
                    at game_card_in(5)
                    hbox:
                        add Solid("#ff6644") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "UNO!!!" size 14 color "#ff6644" bold True
                                text "Mutsumi UNO" size 8 color "#aa5533"
                                text "和睦们来一局纸牌对决。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 老虎机 ──
                button:
                    action Function(start_game_from_phone, "start_slot_machine")
                    xfill True ysize 88
                    background Solid("#1a1a0d")
                    hover_background Solid("#2a2a10")
                    padding (0, 0)
                    at game_card_in(6)
                    hbox:
                        add Solid("#ffd700") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "老虎机" size 14 color "#ffd700" bold True
                                text "Mutsumi Slots" size 8 color "#aa8800"
                                text "消耗睦币，试试手气。" size 10 color "#ffffff66"

                add Solid("#ffffff08") xsize 290 ysize 1

                # ── 音乐演奏 ──
                button:
                    action Function(start_game_from_phone, "start_rhythm_game")
                    xfill True ysize 88
                    background Solid("#141020")
                    hover_background Solid("#201830")
                    padding (0, 0)
                    at game_card_in(7)
                    hbox:
                        add Solid("#d4a0ff") xsize 4 ysize 88
                        frame:
                            background None
                            padding (14, 10)
                            vbox:
                                spacing 4
                                text "音乐演奏" size 14 color "#d4a0ff" bold True
                                text "Mutsumi Rhythm" size 8 color "#9966cc"
                                text "和睦合奏，支持导入自己的音乐。" size 10 color "#ffffff66"

        # 底部
        frame:
            ypos 516 xfill True ysize 52 background Solid("#0a0a10") padding (12, 6)
            vbox:
                xfill True spacing 6
                button:
                    action SetVariable("phone_current_view", "home")
                    xalign 0.5 xsize 120 ysize 18 background None hover_background None
                    add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 🌐 M-Search 浏览器
# ============================================================

default _browser_input = ""

init python:
    def do_mutsumi_search(query):
        q = query.strip()
        if not q:
            renpy.notify("请输入搜索内容")
            return
        try:
            import urllib
            encoded = urllib.quote(q.encode('utf-8'))
        except:
            encoded = q.replace(" ", "+")
        url = "https://www.baidu.com/s?wd=" + encoded
        import webbrowser
        webbrowser.open(url)
        renpy.notify("已在浏览器中打开搜索结果")
        renpy.restart_interaction()

screen phone_view_browser():
    fixed:
        xfill True yfill True

        # 顶部地址栏
        frame:
            xfill True ysize 96
            background Solid("#1a1a2e")
            padding (14, 10)
            vbox:
                spacing 8 xfill True
                hbox:
                    spacing 8
                    text "M" size 22 color "#4a8aee" bold True yalign 0.5
                    text "M-Search" size 14 color "#ffffffcc" yalign 0.5
                frame:
                    xfill True ysize 36
                    background Solid("#ffffff11")
                    padding (12, 6)
                    hbox:
                        xfill True yalign 0.5
                        input:
                            value VariableInputValue("_browser_input")
                            color "#ffffff"
                            size 14
                            xsize 200
                            pixel_width 200
                            yalign 0.5
                        textbutton "搜索":
                            action Function(do_mutsumi_search, _browser_input)
                            text_size 13 text_color "#4a8aee" text_hover_color "#6aaaff"
                            xalign 1.0 yalign 0.5

        # 主体
        frame:
            ypos 100 xfill True ysize 380
            background Solid("#0d0d1a")
            padding (16, 30)
            vbox:
                spacing 16 xfill True
                null height 40
                text "M" size 60 color "#4a8aee" xalign 0.5 bold True
                text "M-Search" size 16 color "#ffffff88" xalign 0.5
                null height 20
                text "搜索结果将在你的浏览器中打开" size 11 color "#ffffff44" xalign 0.5

        # 底部返回（贴底）
        frame:
            ypos 484 xfill True ysize 84
            background Solid("#0a0a14")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0
                xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 📅 日历 (嵌入手机)
# ============================================================
default _cal_year = 2026
default _cal_month = 1
default _cal_selected_day = 0
default _cal_note_input = ""
default _cal_initialized = False

init python:
    import calendar as _cal_mod
    import datetime as _cal_dt

    if persistent.calendar_notes is None:
        persistent.calendar_notes = {}

    def cal_init_today():
        t = _cal_dt.date.today()
        store._cal_year = t.year
        store._cal_month = t.month
        store._cal_selected_day = t.day
        store._cal_initialized = True
        renpy.restart_interaction()

    def cal_adjust(delta):
        store._cal_month += delta
        if store._cal_month > 12:
            store._cal_month = 1
            store._cal_year += 1
        elif store._cal_month < 1:
            store._cal_month = 12
            store._cal_year -= 1
        store._cal_selected_day = 0
        store._cal_note_input = ""
        renpy.restart_interaction()

    def cal_select_day(day):
        store._cal_selected_day = day
        key = "{}-{}-{}".format(store._cal_year, store._cal_month, day)
        store._cal_note_input = persistent.calendar_notes.get(key, "")
        renpy.restart_interaction()

    def cal_save_note():
        key = "{}-{}-{}".format(store._cal_year, store._cal_month, store._cal_selected_day)
        t = store._cal_note_input.strip()
        if t:
            persistent.calendar_notes[key] = t
        elif key in persistent.calendar_notes:
            del persistent.calendar_notes[key]
        renpy.save_persistent()
        renpy.notify("已保存")
        renpy.restart_interaction()

    def cal_delete_note():
        key = "{}-{}-{}".format(store._cal_year, store._cal_month, store._cal_selected_day)
        if key in persistent.calendar_notes:
            del persistent.calendar_notes[key]
            store._cal_note_input = ""
            renpy.save_persistent()
            renpy.notify("已删除")
        renpy.restart_interaction()

    def cal_get_note(year, month, day):
        key = "{}-{}-{}".format(year, month, day)
        return persistent.calendar_notes.get(key, "")

    def cal_get_holidays(year, month):
        h = {
            (1, 1): "元旦", (1, 14): "睦的生日",
            (2, 14): "情人节", (3, 12): "植树节",
            (5, 1): "劳动节", (6, 1): "儿童节",
            (10, 1): "国庆节", (12, 25): "圣诞节",
        }
        if persistent.player_bday_month == month and persistent.player_bday_day > 0:
            h[(month, persistent.player_bday_day)] = "你的生日"
        return h

screen phone_view_calendar():
    # 初始化到今天
    if not _cal_initialized:
        timer 0.01 action Function(cal_init_today)

    $ _today = _cal_dt.date.today()
    $ _weeks = _cal_mod.monthcalendar(_cal_year, _cal_month)
    $ _holidays = cal_get_holidays(_cal_year, _cal_month)
    $ _is_current_month = (_cal_year == _today.year and _cal_month == _today.month)

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 46
            background Solid("#1a2a1e")
            padding (14, 8)
            hbox:
                xfill True yalign 0.5
                text "日历" size 14 color "#95e1d3" bold True yalign 0.5

                # 今天按钮
                if not _is_current_month:
                    textbutton "今天":
                        action Function(cal_init_today)
                        text_size 11 text_color "#95e1d3" text_hover_color "#ffffff"
                        xalign 1.0 yalign 0.5

        # 年月切换
        frame:
            ypos 46 xfill True ysize 34
            background Solid("#0d1a10")
            padding (10, 4)
            hbox:
                xfill True yalign 0.5
                textbutton "<" action Function(cal_adjust, -1) text_size 16 text_color "#95e1d3" text_hover_color "#ffffff" yalign 0.5
                text "[_cal_year]年[_cal_month]月" size 14 color "#ffffff" xalign 0.5 yalign 0.5 bold True
                textbutton ">" action Function(cal_adjust, 1) text_size 16 text_color "#95e1d3" text_hover_color "#ffffff" yalign 0.5

        # 星期头
        frame:
            ypos 80 xfill True ysize 20
            background Solid("#0d1210")
            padding (2, 2)
            hbox:
                xfill True
                for _dname in ["日", "一", "二", "三", "四", "五", "六"]:
                    text "[_dname]" size 10 color "#5a8a6a" xalign 0.5 xsize 42

        # 日历网格
        frame:
            ypos 102 xfill True ysize 290
            background Solid("#0d1210")
            padding (2, 4)

            vbox:
                spacing 2 xfill True

                for _wk in _weeks:
                    hbox:
                        xfill True spacing 0
                        for _d in _wk:
                            if _d == 0:
                                frame:
                                    xsize 42 ysize 44
                                    background None
                            else:
                                $ _is_today = (_is_current_month and _d == _today.day)
                                $ _is_sel = (_cal_selected_day == _d)
                                $ _h = _holidays.get((_cal_month, _d), "")
                                $ _has_note = bool(cal_get_note(_cal_year, _cal_month, _d))

                                # 背景色
                                if _is_today and _is_sel:
                                    $ _dbg = "#95e1d355"
                                elif _is_today:
                                    $ _dbg = "#95e1d333"
                                elif _is_sel:
                                    $ _dbg = "#ffffff22"
                                else:
                                    $ _dbg = "#00000000"

                                button:
                                    xsize 42 ysize 44
                                    background Solid(_dbg)
                                    hover_background Solid("#ffffff11")
                                    action Function(cal_select_day, _d)

                                    vbox:
                                        align (0.5, 0.5) spacing 1
                                        if _is_today:
                                            text "[_d]" size 14 color "#95e1d3" xalign 0.5 bold True font "DejaVuSans.ttf"
                                        elif _h:
                                            text "[_d]" size 13 color "#ffcccc" xalign 0.5 font "DejaVuSans.ttf"
                                        else:
                                            text "[_d]" size 13 color "#ffffffcc" xalign 0.5 font "DejaVuSans.ttf"

                                        if _h:
                                            text "[_h]" size 6 color "#ffcccc" xalign 0.5
                                        elif _has_note:
                                            text "·" size 10 color "#95e1d3" xalign 0.5

        # 选中日期详情区
        frame:
            ypos 396 xfill True ysize 120
            background Solid("#111a14")
            padding (12, 10)

            if _cal_selected_day > 0:
                $ _sel_h = _holidays.get((_cal_month, _cal_selected_day), "")
                vbox:
                    spacing 6 xfill True

                    # 日期标题
                    hbox:
                        spacing 8
                        text "[_cal_year].[_cal_month].[_cal_selected_day]" size 14 color "#ffffff" bold True yalign 0.5
                        if _sel_h:
                            frame:
                                background Solid("#ffcccc22")
                                padding (6, 2)
                                text "[_sel_h]" size 10 color "#ffcccc"

                    # 备注输入框
                    frame:
                        xfill True ysize 32
                        background Solid("#0d1210")
                        padding (8, 4)

                        input:
                            value VariableInputValue("_cal_note_input")
                            color "#ffffffcc" size 12
                            xsize 260 pixel_width 260

                    # 操作按钮
                    hbox:
                        spacing 12 xalign 1.0

                        textbutton "保存":
                            action Function(cal_save_note)
                            text_size 11 text_color "#95e1d3" text_hover_color "#ffffff"

                        if cal_get_note(_cal_year, _cal_month, _cal_selected_day):
                            textbutton "删除":
                                action Function(cal_delete_note)
                                text_size 11 text_color "#ff6666" text_hover_color "#ff8888"
            else:
                text "点击日期添加备注" size 11 color "#ffffff33" xalign 0.5 yalign 0.5

        # 底部
        frame:
            ypos 520 xfill True ysize 48
            background Solid("#0a0f0c")
            padding (12, 6)
            button:
                action [SetVariable("phone_current_view", "home"), SetVariable("_cal_initialized", False)]
                xalign 0.5 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 📝 待办清单 (嵌入手机)
# ============================================================

default _todo_input = ""

init python:
    if persistent.todo_list is None:
        persistent.todo_list = []

    def phone_add_todo(text):
        t = text.strip()
        if t:
            persistent.todo_list.insert(0, {"task": t, "done": False})
            renpy.save_persistent()
            store._todo_input = ""
        renpy.restart_interaction()

    def phone_remove_todo(item):
        if item in persistent.todo_list:
            persistent.todo_list.remove(item)
            renpy.save_persistent()
        renpy.restart_interaction()

    def phone_toggle_todo(item):
        item["done"] = not item.get("done", False)
        renpy.save_persistent()
        renpy.restart_interaction()

screen phone_view_todo():
    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 52
            background Solid("#1a2a1e")
            padding (14, 8)
            vbox:
                spacing 2
                text "待办事项" size 14 color "#95e1d3" bold True
                python:
                    _td_total = len(persistent.todo_list)
                    _td_done = len([t for t in persistent.todo_list if t.get("done")])
                text "[_td_done]/[_td_total] 完成" size 9 color "#ffffff55"

        # 输入区
        frame:
            ypos 52 xfill True ysize 44
            background Solid("#111a14")
            padding (12, 8)
            hbox:
                spacing 8 xfill True
                frame:
                    xsize 220 ysize 28
                    background Solid("#0d1210")
                    padding (8, 4)
                    input:
                        value VariableInputValue("_todo_input")
                        color "#ffffff" size 12
                        xsize 200 pixel_width 200
                textbutton "添加":
                    action Function(phone_add_todo, _todo_input)
                    text_size 12 text_color "#95e1d3" text_hover_color "#ffffff"
                    yalign 0.5

        # 任务列表
        viewport:
            ypos 100 ysize 410
            xfill True mousewheel True scrollbars None

            vbox:
                spacing 2 xfill True

                if not persistent.todo_list:
                    null height 60
                    text "暂无待办事项" size 12 color "#ffffff33" xalign 0.5

                for _ti, _item in enumerate(persistent.todo_list):
                    $ _td = _item.get("done", False)
                    $ _task = _item.get("task", "")
                    $ _tbg = "#95e1d311" if _td else "#0d1210"

                    frame:
                        xfill True yminimum 44
                        background Solid(_tbg)
                        padding (12, 8)

                        hbox:
                            spacing 10 xfill True yalign 0.5

                            # 勾选框
                            if _td:
                                textbutton "V":
                                    action Function(phone_toggle_todo, _item)
                                    text_size 14 text_color "#95e1d3"
                                    yalign 0.5 xsize 24
                            else:
                                textbutton "O":
                                    action Function(phone_toggle_todo, _item)
                                    text_size 14 text_color "#ffffff44"
                                    text_hover_color "#95e1d3"
                                    yalign 0.5 xsize 24

                            # 任务文字
                            $ _tcolor = "#ffffff55" if _td else "#ffffffcc"
                            text "[_task]" size 12 color _tcolor yalign 0.5 xsize 200 strikethrough _td

                            # 删除
                            textbutton "x":
                                action Function(phone_remove_todo, _item)
                                text_size 12 text_color "#ffffff22" text_hover_color "#ff6666"
                                yalign 0.5

                    add Solid("#ffffff08") xsize 280 ysize 1

        # 底部
        frame:
            ypos 514 xfill True ysize 54
            background Solid("#0a0f0c")
            padding (12, 6)
            vbox:
                xfill True spacing 6
                button:
                    action [Function(renpy.save_persistent), SetVariable("phone_current_view", "home")]
                    xalign 0.5 xsize 120 ysize 18
                    background None hover_background None
                    add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)


# ============================================================
# 兼容层
# ============================================================

screen music_player():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "music")]

screen pomodoro_app():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "pomodoro")]

screen weather_app():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "mood")]

screen game_center_menu():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "games")]

screen custom_calendar():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "calendar")]

screen todo_app():
    on "show" action [SetVariable("phone_open", True), SetVariable("phone_current_view", "todo")]


# ============================================================
# Toast
# ============================================================

screen mutsumi_toast(msg):
    timer 2.5 action Hide("mutsumi_toast")
    frame:
        align (0.5, 0.1)
        background Solid("#779977cc")
        padding (20, 10)
        at transform:
            on show:
                yoffset 20 alpha 0.0
                easein_back 0.3 yoffset 0 alpha 1.0
            on hide:
                easeout_cubic 0.4 yoffset -15 alpha 0.0
        text "[msg]" size 18 color "#fff"


# ============================================================
# 📱 功能开发中弹窗（桌宠 / 圆桌会议）
# ============================================================

screen coming_soon_popup(app_name=""):
    modal True
    zorder 300

    add Solid("#000000cc")

    frame:
        align (0.5, 0.45)
        xsize 320
        background Solid("#1a1828")
        padding (28, 28)

        at transform:
            on show:
                alpha 0.0 zoom 0.92
                easein_back 0.3 alpha 1.0 zoom 1.0
            on hide:
                easeout_cubic 0.2 alpha 0.0 zoom 0.95

        vbox:
            spacing 16 xfill True

            # 标题
            hbox:
                spacing 10 xalign 0.5
                text "🌿" size 20 yalign 0.5
                text "[app_name]" size 15 color "#e8c8ff" bold True yalign 0.5

            frame:
                background Solid("#e8c8ff22")
                xfill True ysize 1
                padding (0, 0)

            # 若叶睦的口吻
            if app_name == "桌宠":
                text "……这里还没整理好。{w=0.3}\n\n我想让它更完整一些再给你看。{w=0.3}\n\n等我把温室收拾好……{w=0.3}\n我就把它带给你。" size 12 color "#ffffffaa" line_spacing 8 xalign 0.5 text_align 0.5
            elif app_name == "圆桌会议":
                text "……大家还没聚齐。{w=0.3}\n\n要把所有人都叫到同一张桌子上……{w=0.3}\n需要一点时间。{w=0.3}\n\n你先等我一下，好吗？" size 12 color "#ffffffaa" line_spacing 8 xalign 0.5 text_align 0.5
            else:
                text "……这里还没准备好。\n\n请再等我一下。" size 12 color "#ffffffaa" line_spacing 8 xalign 0.5 text_align 0.5

            null height 4

            # 关闭按钮
            button:
                xalign 0.5 xsize 140 ysize 34
                background Solid("#e8c8ff22")
                hover_background Solid("#e8c8ff44")
                action Hide("coming_soon_popup")
                text "……好，我等你" align (0.5, 0.5) size 12 color "#e8c8ffcc"

    # 点击遮罩也能关闭
    key "mouseup_1" action Hide("coming_soon_popup")
