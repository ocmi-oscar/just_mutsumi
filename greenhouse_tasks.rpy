# ==============================================================================
# 🌱 温室备忘录 — Greenhouse Daily Tasks
# 每日活跃度任务系统，嵌入手机
# ==============================================================================

default persistent.gh_tasks = None
default persistent.gh_last_date = ""
default persistent.gh_points = 0
default persistent.gh_chests = [False, False, False]

init python:
    import random as _gh_rng
    import datetime as _gh_dt

    # 任务池
    _GH_TASK_POOL = [
        {"id": "talk3", "desc": "和睦对话3次", "points": 20, "check": "talk"},
        {"id": "talk5", "desc": "和睦对话5次", "points": 30, "check": "talk5"},
        {"id": "game1", "desc": "玩一局小游戏", "points": 20, "check": "game"},
        {"id": "gacha1", "desc": "在M-Box抽一次卡", "points": 15, "check": "gacha"},
        {"id": "pomo1", "desc": "完成一次番茄钟", "points": 25, "check": "pomodoro"},
        {"id": "online10", "desc": "在线陪伴10分钟", "points": 15, "check": "online10"},
        {"id": "online30", "desc": "在线陪伴30分钟", "points": 25, "check": "online30"},
        {"id": "water", "desc": "现实中喝一杯水", "points": 10, "check": "manual"},
        {"id": "stretch", "desc": "站起来伸个懒腰", "points": 10, "check": "manual"},
        {"id": "smile", "desc": "对着屏幕笑一下", "points": 10, "check": "manual"},
        {"id": "diary", "desc": "查看睦の日记", "points": 15, "check": "diary"},
        {"id": "mood", "desc": "查看今日心情", "points": 10, "check": "mood"},
    ]

    _GH_CHESTS = [
        {"threshold": 30, "reward_coins": 5, "reward_gw": 0.5, "label": "铜宝箱"},
        {"threshold": 60, "reward_coins": 10, "reward_gw": 1.0, "label": "银宝箱"},
        {"threshold": 100, "reward_coins": 20, "reward_gw": 2.0, "label": "金宝箱"},
    ]

    def gh_init_daily():
        today = _gh_dt.date.today().strftime("%Y-%m-%d")
        if persistent.gh_last_date != today:
            persistent.gh_last_date = today
            persistent.gh_points = 0
            persistent.gh_chests = [False, False, False]
            # 随机选5个任务
            pool = list(_GH_TASK_POOL)
            _gh_rng.shuffle(pool)
            tasks = []
            for t in pool[:5]:
                tasks.append({
                    "id": t["id"],
                    "desc": t["desc"],
                    "points": t["points"],
                    "check": t["check"],
                    "done": False,
                })
            persistent.gh_tasks = tasks
            renpy.save_persistent()

    def gh_complete_task(idx):
        if persistent.gh_tasks and 0 <= idx < len(persistent.gh_tasks):
            t = persistent.gh_tasks[idx]
            if not t["done"]:
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
                renpy.save_persistent()
                renpy.notify("+" + str(t["points"]) + " 活跃点")
        renpy.restart_interaction()

    def gh_auto_check():
        """自动检查可自动完成的任务"""
        if not persistent.gh_tasks:
            return
        d = persistent.diary_today_data or {}
        for t in persistent.gh_tasks:
            if t["done"]:
                continue
            ck = t["check"]
            if ck == "talk" and d.get("talk_count", 0) >= 3:
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "talk5" and d.get("talk_count", 0) >= 5:
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "game" and d.get("played_game", False):
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "gacha" and d.get("used_gacha", False):
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "pomodoro" and d.get("did_pomodoro", False):
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "online10" and d.get("online_seconds", 0) >= 600:
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
            elif ck == "online30" and d.get("online_seconds", 0) >= 1800:
                t["done"] = True
                persistent.gh_points = (persistent.gh_points or 0) + t["points"]
        renpy.save_persistent()

    def gh_claim_chest(idx):
        if persistent.gh_chests[idx]:
            return
        chest = _GH_CHESTS[idx]
        if (persistent.gh_points or 0) < chest["threshold"]:
            return
        persistent.gh_chests[idx] = True
        persistent.mutsumi_coins = (getattr(persistent, 'mutsumi_coins', 0) or 0) + chest["reward_coins"]
        if chest["reward_gw"] > 0:
            add_hgd("若叶睦", chest["reward_gw"], daily_id="gh_chest_{}".format(idx), max_daily=1)
        renpy.save_persistent()
        renpy.notify("领取{}！".format(chest["label"]))
        renpy.restart_interaction()


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_greenhouse():
    $ gh_init_daily()
    $ gh_auto_check()
    $ _gh_pts = persistent.gh_points or 0
    $ _gh_tasks = persistent.gh_tasks or []

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 56
            background Solid("#1a2e1a")
            padding (14, 8)
            vbox:
                spacing 2
                text "温室备忘录" size 14 color "#95e1d3" bold True
                text "Daily Goals" size 8 color "#ffffff44"

        # 活跃度条 + 宝箱
        frame:
            ypos 56 xfill True ysize 64
            background Solid("#0d1a10")
            padding (14, 8)

            vbox:
                spacing 6 xfill True
                hbox:
                    spacing 6
                    text "活跃度" size 11 color "#ffffff88" yalign 0.5
                    text "[_gh_pts]" size 16 color "#95e1d3" bold True yalign 0.5 font "DejaVuSans.ttf"
                    text "/ 100" size 11 color "#ffffff44" yalign 0.5

                # 进度条 + 宝箱标记
                frame:
                    xfill True ysize 24
                    background Solid("#0a0f0c")
                    padding (0, 0)

                    # 进度填充
                    $ _gh_pct = min(_gh_pts, 100)
                    $ _gh_w = int(2.7 * _gh_pct)
                    add Solid("#95e1d3") xsize _gh_w ysize 24

                    # 三个宝箱
                    hbox:
                        yalign 0.5 xfill True
                        for _ci in range(3):
                            $ _ct = _GH_CHESTS[_ci]
                            $ _cx = _ct["threshold"]
                            $ _cc = persistent.gh_chests[_ci]
                            $ _cr = _gh_pts >= _cx
                            # 宝箱在对应位置
                            frame:
                                xsize 90 ysize 24
                                background None
                                if _cc:
                                    text "V" xalign 0.5 yalign 0.5 size 12 color "#ffd700" bold True
                                elif _cr:
                                    textbutton "!":
                                        xalign 0.5 yalign 0.5
                                        action Function(gh_claim_chest, _ci)
                                        text_size 14 text_color "#ffd700" text_hover_color "#ffee88"
                                else:
                                    $ _cx_int = int(_cx)
                                    text "[_cx_int]" xalign 0.5 yalign 0.5 size 9 color "#ffffff33" font "DejaVuSans.ttf"

        # 任务列表
        viewport:
            ypos 124 ysize 340
            xfill True mousewheel True scrollbars None

            vbox:
                spacing 4 xfill True

                for _ti in range(len(_gh_tasks)):
                    $ _task = _gh_tasks[_ti]
                    $ _td = _task.get("done", False)
                    $ _tdesc = _task.get("desc", "")
                    $ _tpts = _task.get("points", 0)
                    $ _tcheck = _task.get("check", "")
                    $ _tbg = "#95e1d311" if _td else "#0d1210"

                    frame:
                        xfill True yminimum 56
                        background Solid(_tbg)
                        padding (14, 10)

                        hbox:
                            spacing 10 xfill True yalign 0.5

                            # 勾选
                            if _td:
                                text "V" size 14 color "#95e1d3" bold True yalign 0.5
                            else:
                                text "O" size 14 color "#ffffff33" yalign 0.5

                            # 内容
                            vbox:
                                spacing 2 yalign 0.5
                                $ _tcolor = "#ffffff55" if _td else "#ffffffcc"
                                text "[_tdesc]" size 12 color _tcolor strikethrough _td
                                text "+[_tpts] 活跃点" size 9 color ("#95e1d388" if not _td else "#ffffff33")

                            # 手动完成按钮
                            if not _td and _tcheck == "manual":
                                textbutton "完成":
                                    action Function(gh_complete_task, _ti)
                                    text_size 11 text_color "#95e1d3" text_hover_color "#ffffff"
                                    xalign 1.0 yalign 0.5

                null height 10
                text "任务每日刷新" size 9 color "#ffffff22" xalign 0.5

        # 宝箱详情
        frame:
            ypos 468 xfill True ysize 46
            background Solid("#111a14")
            padding (14, 6)
            hbox:
                spacing 8 xfill True yalign 0.5
                for _ci in range(3):
                    $ _ct = _GH_CHESTS[_ci]
                    $ _cc = persistent.gh_chests[_ci]
                    $ _cl = _ct["label"]
                    $ _ccr = _ct["reward_coins"]
                    frame:
                        xsize 90 ysize 32
                        background Solid("#95e1d311" if _cc else "#0d1210")
                        padding (4, 4)
                        vbox:
                            spacing 1
                            text "[_cl]" size 9 color ("#95e1d3" if _cc else "#ffffff55") xalign 0.5
                            text "+[_ccr]币" size 8 color "#ffffff33" xalign 0.5

        # 底部
        frame:
            ypos 518 xfill True ysize 50
            background Solid("#0a0f0c")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
