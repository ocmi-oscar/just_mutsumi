# ==============================================================================
# 🛠 开发者面板 — Developer Panel
# 完整的测试与调试工具
# ==============================================================================

init python:
    def dev_reset_mail():
        """重置信箱App，清除所有邮箱和历史记录"""
        persistent.meta_mail_email = ""
        persistent.meta_mail_registered = False
        persistent.meta_mail_sent_count = 0
        persistent.meta_mail_history = []
        try:
            store._mail_inbox = []
            store._mail_compose_text = ""
            store._mail_status = ""
            store._mail_email_input = ""
        except:
            pass
        renpy.save_persistent()
        renpy.notify("信箱已重置，可以重新注册邮箱了")
        renpy.restart_interaction()

    def dev_add_resource(field, amount):
        """增加资源，修改 gw_ 好感度变量后自动同步 total"""
        cur = float(getattr(persistent, field, 0) or 0)
        new_val = cur + amount
        # gw_ 变量有范围限制
        if field.startswith("gw_"):
            new_val = max(-100.0, min(10000.0, new_val))
        setattr(persistent, field, new_val)
        # 如果改的是好感度变量，刷新 total
        if field.startswith("gw_") and 'gw_tools' in dir(store):
            gw_tools._refresh_total()
        renpy.save_persistent()
        renpy.notify("{} → {}".format(field, new_val))
        renpy.restart_interaction()

    def dev_set_value(field, value):
        setattr(persistent, field, value)
        if field.startswith("gw_") and 'gw_tools' in dir(store):
            gw_tools._refresh_total()
        renpy.save_persistent()
        renpy.notify("{} 已设为 {}".format(field, value))
        renpy.restart_interaction()

    def dev_reset_feature(feature):
        """重置某个系统"""
        if feature == "gacha":
            persistent.gacha_pity_6star = 0
            persistent.gacha_pity_5star = 0
            persistent.player_inventory = {}
        elif feature == "diary":
            persistent.diary_today_data = None
            persistent.diary_yesterday_entry = ""
            persistent.diary_login_streak = 0
        elif feature == "farm":
            persistent.gh_farm_plots = None
            persistent.gh_farm_harvest_total = 0
            persistent.gh_farm_stolen_total = 0
            persistent.gh_farm_neighbors = None
            persistent.gh_farm_last_refresh = ""
        elif feature == "fortune":
            persistent.fortune_last_date = ""
            persistent.fortune_today = None
            persistent.fortune_streak = 0
        elif feature == "capsule":
            persistent.time_capsules = []
        elif feature == "mood":
            persistent.today_mood = None
            persistent.mood_history = []
        elif feature == "todo":
            persistent.todo_items = []
        elif feature == "notes":
            persistent.calendar_notes = {}
        elif feature == "persona":
            persistent.meta_hostname_reacted = False
            persistent.meta_desktop_notes_left = 0
            persistent.meta_screenshot_count = 0
            persistent.meta_wallpaper_last = ""
        elif feature == "pet":
            persistent.pet_affection_taps = 0
            persistent.pet_fed_today = ""
        elif feature == "all_goodwill":
            persistent.gw_wakaba = 0.0
            persistent.gw_guitar = 0.0
            persistent.gw_metis = 0.0
            persistent.gw_total = 0.0
            persistent.gw_event_flags = {}
            persistent.gw_daily_counts = {}
            persistent.milestone_claimed = []
            persistent.mutsumi_coins = 0
            persistent.milestone_story_tickets = 0
            persistent.milestone_wallpaper_tickets = 0
        elif feature == "milestone_only":
            persistent.milestone_claimed = []
            persistent.mutsumi_coins = 0
            persistent.milestone_story_tickets = 0
            persistent.milestone_wallpaper_tickets = 0
            _base = ["images/musuoping.png"]
            persistent.unlocked_wallpapers = _base
        renpy.save_persistent()
        renpy.notify("{} 已重置".format(feature))
        renpy.restart_interaction()

    def dev_unlock_all_cgs():
        if persistent.unlocked_cgs is None:
            persistent.unlocked_cgs = []
        for item in gacha_all_items:
            if item.get("type") == "cg":
                if item["id"] not in persistent.unlocked_cgs:
                    persistent.unlocked_cgs.append(item["id"])
        renpy.save_persistent()
        renpy.notify("所有CG已解锁")
        renpy.restart_interaction()

    # 随机对话开关
    if not hasattr(persistent, "dev_disable_random_talk"):
        persistent.dev_disable_random_talk = False

    def dev_toggle_random_talk():
        persistent.dev_disable_random_talk = not (persistent.dev_disable_random_talk or False)
        renpy.save_persistent()
        renpy.restart_interaction()

    def dev_toggle_dev_mode():
        persistent.developer_mode = not persistent.developer_mode
        renpy.save_persistent()
        renpy.notify("开发者模式: {}".format("开启" if persistent.developer_mode else "关闭"))
        renpy.restart_interaction()


screen debug_goodwill_panel():
    tag menu
    modal True
    zorder 200

    default _dev_tab = 0

    add Solid("#0a0a14f0")

    # 顶部标题
    frame:
        xfill True ysize 60
        background Solid("#1a1a2e")
        padding (30, 12)
        hbox:
            xfill True yalign 0.5
            vbox:
                spacing 2
                text "🛠 开发者面板" size 22 color "#ffd700" bold True
                text "Developer Panel — 测试工具集" size 10 color "#ffffff44"
            textbutton "关闭":
                action Hide("debug_goodwill_panel")
                text_size 14 text_color "#ff6666" text_hover_color "#ffffff"
                xalign 1.0 yalign 0.5

    # Tab栏
    frame:
        ypos 60 xfill True ysize 40
        background Solid("#0d0d18")
        padding (20, 0)
        hbox:
            spacing 0 yalign 0.5
            for _ti, _tn in enumerate(["资源", "好感度", "重置", "解锁", "系统"]):
                button:
                    xsize 120 ysize 40
                    background Solid("#ffd70022" if _dev_tab == _ti else "#00000000")
                    hover_background Solid("#ffd70011")
                    action SetScreenVariable("_dev_tab", _ti)
                    text "[_tn]" align (0.5, 0.5) size 14 color ("#ffd700" if _dev_tab == _ti else "#ffffff55") bold (_dev_tab == _ti)

    # 内容
    viewport:
        ypos 104 ysize 580
        xfill True mousewheel True scrollbars None

        frame:
            xfill True
            background None
            padding (30, 20)

            if _dev_tab == 0:
                # ══ 资源 ══
                vbox:
                    spacing 12 xfill True

                    text "资源管理" size 16 color "#ffd700" bold True
                    add Solid("#ffd70033") xsize 1100 ysize 1

                    # 睦币
                    $ _coins = getattr(persistent, 'mutsumi_coins', 0) or 0
                    hbox:
                        spacing 10 yalign 0.5
                        text "睦币 当前: [_coins]" size 14 color "#ffffff" xsize 260
                        for _amt in [10, 50, 100, 500, 1000]:
                            textbutton "+[_amt]":
                                action Function(dev_add_resource, "mutsumi_coins", _amt)
                                text_size 13 text_color "#ffd700" text_hover_color "#ffffff"
                        textbutton "清零":
                            action Function(dev_set_value, "mutsumi_coins", 0)
                            text_size 13 text_color "#ff6666" text_hover_color "#ffffff"

                    # 碎片
                    $ _frags = getattr(persistent, 'shop_fragments', 0) or 0
                    hbox:
                        spacing 10 yalign 0.5
                        text "碎片 当前: [_frags]" size 14 color "#ffffff" xsize 260
                        for _amt in [10, 50, 100, 500]:
                            textbutton "+[_amt]":
                                action Function(dev_add_resource, "shop_fragments", _amt)
                                text_size 13 text_color "#ffa040" text_hover_color "#ffffff"
                        textbutton "清零":
                            action Function(dev_set_value, "shop_fragments", 0)
                            text_size 13 text_color "#ff6666" text_hover_color "#ffffff"

                    # 剧情解锁卷
                    $ _st = getattr(persistent, 'milestone_story_tickets', 0) or 0
                    hbox:
                        spacing 10 yalign 0.5
                        text "剧情卷 当前: [_st]" size 14 color "#ffffff" xsize 260
                        for _amt in [1, 5, 10]:
                            textbutton "+[_amt]":
                                action Function(dev_add_resource, "milestone_story_tickets", _amt)
                                text_size 13 text_color "#d4a0ff" text_hover_color "#ffffff"

                    # 壁纸卷
                    $ _wt = getattr(persistent, 'milestone_wallpaper_tickets', 0) or 0
                    hbox:
                        spacing 10 yalign 0.5
                        text "壁纸卷 当前: [_wt]" size 14 color "#ffffff" xsize 260
                        for _amt in [1, 5, 9]:
                            textbutton "+[_amt]":
                                action Function(dev_add_resource, "milestone_wallpaper_tickets", _amt)
                                text_size 13 text_color "#6ab8d8" text_hover_color "#ffffff"

                    null height 10
                    text "抽卡资源" size 14 color "#ffd70088"
                    add Solid("#ffd70022") xsize 1100 ysize 1

                    # M-Box抽卡币
                    $ _gcoins = getattr(persistent, 'gacha_currency', 0) or 0
                    hbox:
                        spacing 10 yalign 0.5
                        text "抽卡币 当前: [_gcoins]" size 14 color "#ffffff" xsize 260
                        for _amt in [160, 800, 1600, 8000]:
                            textbutton "+[_amt]":
                                action Function(dev_add_resource, "gacha_currency", _amt)
                                text_size 13 text_color "#ffd700" text_hover_color "#ffffff"

            elif _dev_tab == 1:
                # ══ 好感度 ══
                vbox:
                    spacing 14 xfill True

                    text "好感度调整" size 16 color "#ffd700" bold True
                    add Solid("#ffd70033") xsize 1100 ysize 1

                    # 若叶睦（吉他睦）— 使用 goodwill_system.rpy 的正确变量 gw_guitar
                    $ _gw = float(getattr(persistent, 'gw_guitar', 0) or 0)
                    hbox:
                        spacing 10 yalign 0.5
                        text "若叶睦 [_gw]" size 14 color "#8FBC8F" xsize 220
                        for _amt in [-50, -10, -1, 1, 10, 50, 100]:
                            textbutton "[_amt]":
                                action Function(dev_add_resource, "gw_guitar", _amt)
                                text_size 13 text_color "#8FBC8F" text_hover_color "#ffffff"
                        textbutton "MAX":
                            action Function(dev_set_value, "gw_guitar", 10000)
                            text_size 13 text_color "#ffd700" text_hover_color "#ffffff"

                    # 墨缇斯 — 使用正确变量 gw_metis
                    $ _gm = float(getattr(persistent, 'gw_metis', 0) or 0)
                    hbox:
                        spacing 10 yalign 0.5
                        text "墨缇斯 [_gm]" size 14 color "#CC4444" xsize 220
                        for _amt in [-50, -10, -1, 1, 10, 50, 100]:
                            textbutton "[_amt]":
                                action Function(dev_add_resource, "gw_metis", _amt)
                                text_size 13 text_color "#CC4444" text_hover_color "#ffffff"
                        textbutton "MAX":
                            action Function(dev_set_value, "gw_metis", 10000)
                            text_size 13 text_color "#ffd700" text_hover_color "#ffffff"

                    null height 16
                    hbox:
                        spacing 10
                        button:
                            xsize 200 ysize 40
                            background Solid("#ff444433")
                            hover_background Solid("#ff444455")
                            action Function(dev_reset_feature, "all_goodwill")
                            text "全部好感度归零" align (0.5, 0.5) size 13 color "#ff4444"
                        button:
                            xsize 200 ysize 40
                            background Solid("#44448833")
                            hover_background Solid("#44448855")
                            action Function(dev_reset_feature, "milestone_only")
                            text "重置里程碑领取" align (0.5, 0.5) size 13 color "#8888ff"

            elif _dev_tab == 2:
                # ══ 重置 ══
                vbox:
                    spacing 10 xfill True

                    text "系统重置" size 16 color "#ffd700" bold True
                    text "点击重置对应系统的数据（不可恢复，谨慎使用）" size 10 color "#ffffff55"
                    add Solid("#ffd70033") xsize 1100 ysize 1
                    null height 6

                    # 邮箱重置（最重要！）
                    button:
                        xfill True ysize 52
                        background Solid("#ff444422")
                        hover_background Solid("#ff444444")
                        action Function(dev_reset_mail)
                        hbox:
                            spacing 12 yalign 0.5 xoffset 16
                            text "📮" size 22 yalign 0.5
                            vbox:
                                spacing 1 yalign 0.5
                                text "重置信箱App" size 14 color "#ffffff" bold True
                                text "清除注册邮箱、发件记录、本地收件箱 — 可重新注册" size 10 color "#ffffff88"

                    null height 8

                    for _fid, _fname, _fdesc, _fcolor in [
                        ("gacha", "M-Box 抽卡", "清除保底计数和所有抽到的物品", "#d4a0ff"),
                        ("diary", "睦の日记", "清除日记记录和登录连击", "#8FBC8F"),
                        ("farm", "温室农场", "清除地块、收获记录、邻居状态", "#8FBC8F"),
                        ("fortune", "占卜", "清除每日签文记录", "#e8c8ff"),
                        ("capsule", "时间胶囊", "删除所有胶囊", "#6ab8d8"),
                        ("mood", "今日心情", "清除心情历史", "#ffa040"),
                        ("todo", "待办清单", "清空所有任务", "#ffffff"),
                        ("notes", "日历备注", "清空所有日历备注", "#ffffff"),
                        ("persona", "Meta系统", "重置桌面便签、截图计数等", "#d4a0ff"),
                        ("pet", "桌宠", "重置喂食和抚摸次数", "#8FBC8F"),
                    ]:
                        button:
                            xfill True ysize 42
                            background Solid("#ffffff08")
                            hover_background Solid(_fcolor + "22")
                            action Function(dev_reset_feature, _fid)
                            hbox:
                                spacing 12 yalign 0.5 xoffset 16
                                text "[_fname]" size 13 color _fcolor bold True xsize 140
                                text "[_fdesc]" size 11 color "#ffffff66"

            elif _dev_tab == 3:
                # ══ 解锁 ══
                vbox:
                    spacing 12 xfill True

                    text "快速解锁" size 16 color "#ffd700" bold True
                    add Solid("#ffd70033") xsize 1100 ysize 1

                    button:
                        xfill True ysize 50
                        background Solid("#ffd70022")
                        hover_background Solid("#ffd70044")
                        action Function(dev_unlock_all_cgs)
                        text "解锁所有CG" align (0.5, 0.5) size 14 color "#ffd700" bold True

                    button:
                        xfill True ysize 50
                        background Solid("#d4a0ff22")
                        hover_background Solid("#d4a0ff44")
                        action [Function(dev_set_value, "milestone_wallpaper_tickets", 9), Function(dev_set_value, "milestone_story_tickets", 20)]
                        text "最大化解锁卷 (壁纸9 + 剧情20)" align (0.5, 0.5) size 14 color "#d4a0ff"

                    button:
                        xfill True ysize 50
                        background Solid("#8FBC8F22")
                        hover_background Solid("#8FBC8F44")
                        action [Function(dev_set_value, "mutsumi_guitar_tutorial_done", True), Function(dev_set_value, "greenhouse_inventory", {"seed_basic": 10, "seed_rare": 5, "seed_epic": 2, "fertilizer": 10, "water_plus": 10})]
                        text "解锁吉他教程 + 温室满背包" align (0.5, 0.5) size 14 color "#8FBC8F"

            elif _dev_tab == 4:
                # ══ 系统 ══
                vbox:
                    spacing 12 xfill True

                    text "系统开关" size 16 color "#ffd700" bold True
                    add Solid("#ffd70033") xsize 1100 ysize 1

                    $ _dm = persistent.developer_mode
                    hbox:
                        spacing 14 yalign 0.5
                        text "开发者模式: [_dm]" size 14 color "#ffffff" xsize 300
                        textbutton "切换":
                            action Function(dev_toggle_dev_mode)
                            text_size 13 text_color "#ffd700" text_hover_color "#ffffff"

                    null height 6

                    # ── 随机对话开关 ──
                    $ _rdt = persistent.dev_disable_random_talk or False
                    $ _rdt_label = "已禁用 ⛔" if _rdt else "正常运行 ✓"
                    $ _rdt_color = "#ff6644" if _rdt else "#8FBC8F"
                    hbox:
                        spacing 14 yalign 0.5
                        vbox:
                            spacing 2 yalign 0.5
                            text "随机对话触发" size 14 color "#ffffff" xsize 300
                            text "[_rdt_label]" size 11 color _rdt_color
                        textbutton ("开启" if _rdt else "禁用"):
                            action Function(dev_toggle_random_talk)
                            text_size 13 text_color ("#8FBC8F" if _rdt else "#ff6644") text_hover_color "#ffffff"

                    null height 6
                    text "当前存档信息" size 14 color "#ffd70088"
                    add Solid("#ffd70022") xsize 1100 ysize 1

                    $ _pn = persistent.playername or "未设置"
                    $ _email = persistent.meta_mail_email or "未注册"
                    $ _reg = persistent.meta_mail_registered
                    text "玩家名: [_pn]" size 12 color "#ffffffcc"
                    text "注册邮箱: [_email]" size 12 color "#ffffffcc"
                    text "已注册: [_reg]" size 12 color "#ffffffcc"

                    null height 20
                    button:
                        xsize 300 ysize 44
                        background Solid("#ff444433")
                        hover_background Solid("#ff444455")
                        action Confirm("确定要清空所有存档数据吗？此操作不可恢复！", yes=[Function(MainMenu(confirm=False))])
                        text "返回主菜单" align (0.5, 0.5) size 13 color "#ff4444"
