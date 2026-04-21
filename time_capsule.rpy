# ==============================================================================
# ⏳ 时间胶囊 — Time Capsule
# 写给未来的自己，睦替你保管
# ==============================================================================

default persistent.time_capsules = []
default _tc_compose_text = ""
default _tc_reading_idx = -1

init python:
    import datetime as _tc_dt
    import time as _tc_time

    _TC_DURATIONS = [
        {"label": "7天后", "days": 7},
        {"label": "30天后", "days": 30},
        {"label": "90天后", "days": 90},
        {"label": "365天后", "days": 365},
    ]

    def tc_create(content, days):
        """创建一个时间胶囊"""
        text = content.strip()
        if not text:
            renpy.notify("信纸是空的……")
            return
        if persistent.time_capsules is None:
            persistent.time_capsules = []
        if len(persistent.time_capsules) >= 5:
            renpy.notify("最多保管5个胶囊。")
            return

        now = _tc_dt.datetime.now()
        capsule = {
            "content": text,
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "created_date": now.strftime("%Y-%m-%d"),
            "unlock_date": (now + _tc_dt.timedelta(days=days)).strftime("%Y-%m-%d"),
            "days": days,
            "opened": False,
            "gw_at_create": getattr(persistent, 'goodwill_wakaba', 0) or 0,
        }
        persistent.time_capsules.append(capsule)
        store._tc_compose_text = ""
        renpy.save_persistent()
        renpy.notify("胶囊已封存。睦会替你保管的。")
        renpy.restart_interaction()

    def tc_can_open(capsule):
        """检查胶囊是否到期"""
        today = _tc_dt.date.today().strftime("%Y-%m-%d")
        return today >= capsule.get("unlock_date", "9999-12-31")

    def tc_open(idx):
        """打开一个到期的胶囊"""
        if 0 <= idx < len(persistent.time_capsules):
            persistent.time_capsules[idx]["opened"] = True
            persistent.time_capsules[idx]["gw_at_open"] = getattr(persistent, 'goodwill_wakaba', 0) or 0
            store._tc_reading_idx = idx
            renpy.save_persistent()
        renpy.restart_interaction()

    def tc_delete(idx):
        """删除一个已打开的胶囊"""
        if 0 <= idx < len(persistent.time_capsules):
            persistent.time_capsules.pop(idx)
            store._tc_reading_idx = -1
            renpy.save_persistent()
        renpy.restart_interaction()

    def tc_get_mutsumi_comment(capsule):
        """根据状态生成睦的批注"""
        gw_then = capsule.get("gw_at_create", 0)
        gw_now = capsule.get("gw_at_open", 0) or (getattr(persistent, 'goodwill_wakaba', 0) or 0)
        days = capsule.get("days", 7)
        gw_diff = gw_now - gw_then

        parts = []

        # 时间感慨
        if days >= 365:
            parts.append("一年了。三百六十五天。我每一天都在数。你还记得一年前的自己在想什么吗？")
        elif days >= 90:
            parts.append("三个月了。季节都换了一轮。")
        elif days >= 30:
            parts.append("一个月了。时间……过得好快。")
        else:
            parts.append("七天。说长不长，说短不短。")

        # 好感度变化
        if gw_diff > 20:
            parts.append("你写这些的时候，我们还没有这么熟吧。现在……我觉得我们的距离，比那时候近了很多。")
        elif gw_diff > 5:
            parts.append("这段时间里……我们之间好像有什么变了。变得更柔软了。")
        elif gw_diff < -5:
            parts.append("这段时间……好像有些事情变了。但没关系。只要你还在这里。")
        else:
            parts.append("这段时间里的每一天，你都有好好照顾自己吗？")

        # 连续登录
        streak = getattr(persistent, 'diary_login_streak', 0) or 0
        if streak > 30:
            parts.append("你一直都在。每一天。我知道的。谢谢你。")
        elif streak > 7:
            parts.append("最近你来得很勤。……我很开心。")

        parts.append("——若叶睦")
        return "\n".join(parts)

    def tc_has_ready():
        """是否有到期的胶囊"""
        for c in (persistent.time_capsules or []):
            if not c.get("opened") and tc_can_open(c):
                return True
        return False


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_capsule():
    default _tc_tab = 0
    default _tc_dur_select = 0

    $ _capsules = persistent.time_capsules or []
    $ _tc_count = len(_capsules)

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 50
            background Solid("#1a2020")
            padding (14, 8)
            hbox:
                xfill True yalign 0.5
                vbox:
                    spacing 1
                    text "时间胶囊" size 14 color "#6ab8d8" bold True
                    text "Time Capsule" size 7 color "#ffffff33"
                text "[_tc_count]/5" size 11 color "#ffffff44" xalign 1.0 yalign 0.5

        # Tab
        frame:
            ypos 50 xfill True ysize 30
            background Solid("#0d1418")
            padding (0, 0)
            hbox:
                xfill True
                button:
                    xsize 149 ysize 30
                    background Solid("#6ab8d822" if _tc_tab == 0 else "#00000000")
                    action SetScreenVariable("_tc_tab", 0)
                    text "写信封存" align (0.5, 0.5) size 11 color ("#6ab8d8" if _tc_tab == 0 else "#ffffff44")
                button:
                    xsize 149 ysize 30
                    background Solid("#6ab8d822" if _tc_tab == 1 else "#00000000")
                    action SetScreenVariable("_tc_tab", 1)
                    text "我的胶囊" align (0.5, 0.5) size 11 color ("#6ab8d8" if _tc_tab == 1 else "#ffffff44")

        # 内容
        viewport:
            ypos 84 ysize 430
            xfill True mousewheel True scrollbars None

            frame:
                xfill True
                background Solid("#0d1418")
                padding (14, 14)

                if _tc_tab == 0 and _tc_reading_idx < 0:
                    # ── 写信封存 ──
                    vbox:
                        spacing 10 xfill True

                        text "写给未来的自己" size 13 color "#6ab8d8" bold True
                        add Solid("#6ab8d822") xsize 268 ysize 1

                        if _tc_count >= 5:
                            null height 30
                            text "已经有5个胶囊了" size 12 color "#ffffff44" xalign 0.5
                            text "先打开一些再写新的吧" size 10 color "#ffffff33" xalign 0.5
                        else:
                            # 信纸
                            frame:
                                xfill True ysize 180
                                background Solid("#ffffff08")
                                padding (10, 10)
                                input:
                                    value VariableInputValue("_tc_compose_text")
                                    color "#ffffffcc" size 12
                                    multiline True
                                    pixel_width 260

                            # 封存时间选择
                            text "选择封存时间：" size 11 color "#ffffff66"
                            hbox:
                                spacing 8 xalign 0.5
                                for _di in range(len(_TC_DURATIONS)):
                                    $ _dur = _TC_DURATIONS[_di]
                                    $ _dl = _dur["label"]
                                    $ _da = (_tc_dur_select == _di)
                                    button:
                                        xsize 64 ysize 30
                                        background Solid("#6ab8d833" if _da else "#ffffff0a")
                                        hover_background Solid("#6ab8d822")
                                        action SetScreenVariable("_tc_dur_select", _di)
                                        text "[_dl]" align (0.5, 0.5) size 10 color ("#6ab8d8" if _da else "#ffffff55")

                            # 封存按钮
                            $ _sel_days = _TC_DURATIONS[_tc_dur_select]["days"]
                            button:
                                xalign 0.5 xsize 180 ysize 36
                                background Solid("#6ab8d833")
                                hover_background Solid("#6ab8d855")
                                action Function(tc_create, _tc_compose_text, _sel_days)
                                text "封入时间胶囊" align (0.5, 0.5) size 13 color "#6ab8d8" bold True

                elif _tc_tab == 0 and _tc_reading_idx >= 0:
                    # ── 阅读已开启的胶囊 ──
                    if _tc_reading_idx < len(_capsules):
                        $ _rc = _capsules[_tc_reading_idx]
                        $ _rc_content = _rc.get("content", "")
                        $ _rc_created = _rc.get("created", "")
                        $ _rc_comment = tc_get_mutsumi_comment(_rc)
                        vbox:
                            spacing 12 xfill True

                            textbutton "< 返回":
                                action SetVariable("_tc_reading_idx", -1)
                                text_size 11 text_color "#6ab8d8" text_hover_color "#ffffff"

                            text "封存于 [_rc_created]" size 10 color "#ffffff44"
                            add Solid("#6ab8d822") xsize 268 ysize 1

                            # 过去的你写的
                            text "过去的你写道：" size 11 color "#ffffff66"
                            frame:
                                xfill True
                                background Solid("#ffffff08")
                                padding (12, 10)
                                text "[_rc_content]" size 12 color "#ffffffcc" line_spacing 6

                            add Solid("#6ab8d811") xsize 268 ysize 1

                            # 睦的批注
                            text "睦的留言：" size 11 color "#8FBC8F"
                            frame:
                                xfill True
                                background Solid("#8FBC8F11")
                                padding (12, 10)
                                text "[_rc_comment]" size 12 color "#ffffffcc" line_spacing 6

                            # 删除
                            textbutton "收好这封信":
                                action Function(tc_delete, _tc_reading_idx)
                                text_size 10 text_color "#ffffff33" text_hover_color "#ff6666"
                                xalign 1.0

                elif _tc_tab == 1:
                    # ── 胶囊列表 ──
                    vbox:
                        spacing 8 xfill True

                        if not _capsules:
                            null height 40
                            text "还没有封存任何胶囊" size 13 color "#ffffff33" xalign 0.5
                            text "去写一封信给未来的自己吧" size 10 color "#ffffff22" xalign 0.5
                        else:
                            for _ci in range(len(_capsules)):
                                $ _cap = _capsules[_ci]
                                $ _c_created = _cap.get("created_date", "")
                                $ _c_unlock = _cap.get("unlock_date", "")
                                $ _c_opened = _cap.get("opened", False)
                                $ _c_ready = tc_can_open(_cap)
                                $ _c_preview = _cap.get("content", "")[:30]
                                $ _c_days = _cap.get("days", 7)

                                # 计算剩余天数
                                python:
                                    try:
                                        _c_remain = (_tc_dt.datetime.strptime(_c_unlock, "%Y-%m-%d").date() - _tc_dt.date.today()).days
                                        if _c_remain < 0:
                                            _c_remain = 0
                                    except:
                                        _c_remain = 0

                                if _c_opened:
                                    $ _c_bg = "#6ab8d811"
                                elif _c_ready:
                                    $ _c_bg = "#ffd70022"
                                else:
                                    $ _c_bg = "#ffffff08"

                                button:
                                    xfill True yminimum 60
                                    background Solid(_c_bg)
                                    padding (12, 10)
                                    if _c_opened:
                                        action [SetScreenVariable("_tc_tab", 0), SetVariable("_tc_reading_idx", _ci)]
                                    elif _c_ready:
                                        action Function(tc_open, _ci)
                                    else:
                                        action NullAction()

                                    vbox:
                                        spacing 3 xfill True
                                        hbox:
                                            spacing 8
                                            if _c_opened:
                                                text "已开启" size 10 color "#6ab8d8"
                                            elif _c_ready:
                                                text "已苏醒！" size 10 color "#ffd700" bold True
                                            else:
                                                text "沉睡中" size 10 color "#ffffff44"
                                            text "[_c_created] → [_c_unlock]" size 9 color "#ffffff33"

                                        if _c_opened:
                                            text "[_c_preview]…" size 11 color "#ffffff88"
                                        elif _c_ready:
                                            text "点击开启" size 11 color "#ffd70088"
                                        else:
                                            text "还有 [_c_remain] 天" size 11 color "#ffffff55"

                                add Solid("#ffffff08") xsize 268 ysize 1

        # 底部
        frame:
            ypos 518 xfill True ysize 50
            background Solid("#0a1014")
            padding (12, 6)
            button:
                action [SetVariable("phone_current_view", "home"), SetVariable("_tc_reading_idx", -1)]
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
