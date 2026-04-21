# ==============================================================================
# 🔮 占卜 — Daily Fortune (睦の塔罗)
# 每日一签，仪式感抽卡 + 人格化解读
# ==============================================================================

default persistent.fortune_last_date = ""
default persistent.fortune_today = None
default persistent.fortune_streak = 0

init python:
    import random as _ft_rng
    import datetime as _ft_dt

    _FORTUNE_LEVELS = [
        {"id": "dai_kichi", "name": "大吉", "color": "#ffd700", "weight": 10},
        {"id": "chu_kichi", "name": "中吉", "color": "#95e1d3", "weight": 20},
        {"id": "sho_kichi", "name": "小吉", "color": "#8FBC8F", "weight": 20},
        {"id": "kichi",     "name": "吉",   "color": "#6ab8d8", "weight": 20},
        {"id": "sue_kichi", "name": "末吉", "color": "#ffffffaa", "weight": 15},
        {"id": "kyo",       "name": "凶",   "color": "#cc6666", "weight": 12},
        {"id": "dai_kyo",   "name": "大凶", "color": "#ff4444", "weight": 3},
    ]

    _FORTUNE_THEMES = {
        "dai_kichi": [
            {"sign": "万事如意，心愿必达", "mutsumi": "大吉……最好的结果。你值得这份好运。我也是。", "mortis": "大吉！看到没！这是我施的魔法！今天你可以横着走！"},
            {"sign": "贵人相助，逢凶化吉", "mutsumi": "身边……有在乎你的人。好好珍惜。", "mortis": "贵人？那个贵人就是我啊！不用谢！"},
            {"sign": "星光璀璨，前路光明", "mutsumi": "前面的路……很亮。你不用害怕。我会在你身后。", "mortis": "前路光明！冲啊！把挡路的全部推开！"},
        ],
        "chu_kichi": [
            {"sign": "心意已在途中，耐心等待回音", "mutsumi": "你在等谁的回答吗？如果是我的话……你不用等的。答案一直都在。", "mortis": "等回音？直接冲过去问啊！磨磨蹭蹭的！"},
            {"sign": "稳步前行，收获在秋", "mutsumi": "不急。黄瓜也要慢慢长。你做的事情……一定会有结果的。", "mortis": "秋天？太远了吧！我要现在就收获！"},
            {"sign": "云开雾散，柳暗花明", "mutsumi": "如果现在很迷茫……再等等。光会来的。", "mortis": "迷雾？让我来吹散它！哈——"},
        ],
        "sho_kichi": [
            {"sign": "小有所获，不宜冒进", "mutsumi": "今天……适合做小小的事情。浇花。调弦。看你。", "mortis": "不宜冒进？切，小心翼翼的人生多无聊啊。"},
            {"sign": "守静待机，蓄势待发", "mutsumi": "安静也是一种力量。种子在土里的时候……也在用力。", "mortis": "蓄势？好吧，我就当是在给大招充能！"},
        ],
        "kichi": [
            {"sign": "平安顺遂，波澜不惊", "mutsumi": "平凡的一天。但平凡……很珍贵。", "mortis": "普通的吉？行吧，至少不是凶。我接受！"},
            {"sign": "日常有暖，细微处见真心", "mutsumi": "你今天……有没有注意到温暖的小事？哪怕很小也好。", "mortis": "细微处见真心……比如我偷偷帮小睦整理琴弦？"},
        ],
        "sue_kichi": [
            {"sign": "祸福相依，谨言慎行", "mutsumi": "末吉。不好不坏。但……小心一点比较好。今天不要做太大的决定。", "mortis": "谨言慎行？那我先闭嘴五秒。一、二……啊不行我做不到！"},
            {"sign": "风波未定，静观其变", "mutsumi": "有些事情还没有定下来。等等看。我陪你等。", "mortis": "静观其变？我偏要主动出击！"},
        ],
        "kyo": [
            {"sign": "小有波折，但终会过去", "mutsumi": "凶……今天可能不太顺利。但没关系。我在的话，坏运气会绕道走的。来温室陪我就好。", "mortis": "凶？哈！正好！墨缇斯最擅长对付坏运气了！来，躲到我身后！"},
            {"sign": "谨防口舌，宜守不宜攻", "mutsumi": "今天少说话比较好。话说多了……容易受伤。你也是，我也是。", "mortis": "宜守不宜攻？我偏要攻！不过……算了，今天就保护你一天吧。"},
        ],
        "dai_kyo": [
            {"sign": "风雨将至，但请记得，暴风雨总会过去", "mutsumi": "大凶。（沉默了很久）……没关系。再大的风雨，也吹不倒温室的玻璃。今天不要去做重要的决定……来陪我就好。", "mortis": "大凶？！完美！今天就是搞破坏的好日子！不是——我是说，今天别出门了！跟我待在这里！我保护你！"},
        ],
    }

    def fortune_draw():
        """抽签"""
        today = _ft_dt.date.today().strftime("%Y-%m-%d")
        if persistent.fortune_last_date == today:
            return  # 今天已经抽过

        # 动态权重调整
        gw = getattr(persistent, 'goodwill_wakaba', 0) or 0
        weights = []
        for lv in _FORTUNE_LEVELS:
            w = lv["weight"]
            if lv["id"] in ("dai_kichi", "chu_kichi"):
                w += min(gw / 10, 15)
            elif lv["id"] in ("kyo", "dai_kyo"):
                w = max(w - min(gw / 10, 8), 1)
            weights.append(w)

        # 加权随机
        total = sum(weights)
        roll = _ft_rng.random() * total
        cumul = 0
        chosen_idx = 0
        for i, w in enumerate(weights):
            cumul += w
            if roll <= cumul:
                chosen_idx = i
                break

        level = _FORTUNE_LEVELS[chosen_idx]
        themes = _FORTUNE_THEMES.get(level["id"], [{"sign": "平安", "mutsumi": "……", "mortis": "嗯。"}])
        theme = _ft_rng.choice(themes)

        result = {
            "level_id": level["id"],
            "level_name": level["name"],
            "level_color": level["color"],
            "sign": theme["sign"],
            "mutsumi": theme["mutsumi"],
            "mortis": theme["mortis"],
            "date": today,
        }

        persistent.fortune_today = result
        persistent.fortune_last_date = today
        persistent.fortune_streak = (persistent.fortune_streak or 0) + 1
        renpy.save_persistent()
        renpy.restart_interaction()

    def fortune_can_draw():
        today = _ft_dt.date.today().strftime("%Y-%m-%d")
        return persistent.fortune_last_date != today


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_fortune():
    $ _ft_can = fortune_can_draw()
    $ _ft_result = persistent.fortune_today
    $ _ft_streak = persistent.fortune_streak or 0
    $ _ft_persona = persona_current() if 'persona_current' in dir(store) else "wakaba"

    default _ft_phase = "idle"
    default _ft_selected = -1

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 50
            background Solid("#1a1420")
            padding (14, 8)
            hbox:
                xfill True yalign 0.5
                vbox:
                    spacing 1
                    text "占卜" size 14 color "#e8c8ff" bold True
                    text "Daily Fortune" size 7 color "#ffffff33"
                if _ft_streak >= 7:
                    text "连续[_ft_streak]天" size 9 color "#ffd70088" xalign 1.0 yalign 0.5

        if _ft_can and _ft_phase == "idle":
            # ── 选牌界面 ──
            frame:
                ypos 54 xfill True ysize 514
                background Solid("#0d0a14")
                padding (14, 20)

                vbox:
                    spacing 16 xfill True

                    null height 20
                    text "……选一张。" size 14 color "#ffffffaa" xalign 0.5
                    null height 20

                    # 5张倒扣的牌
                    hbox:
                        xalign 0.5 spacing 8
                        for _ci in range(5):
                            button:
                                xsize 50 ysize 72
                                background Solid("#2a1a3a")
                                hover_background Solid("#3a2a4a")
                                action [SetScreenVariable("_ft_selected", _ci), SetScreenVariable("_ft_phase", "reveal")]
                                vbox:
                                    align (0.5, 0.5) spacing 4
                                    text "?" size 22 color "#e8c8ff44" xalign 0.5
                                    text "✦" size 10 color "#e8c8ff22" xalign 0.5

                    null height 30
                    text "每日一签" size 10 color "#ffffff33" xalign 0.5
                    text "用心去感受，选择你被吸引的那一张" size 10 color "#ffffff22" xalign 0.5

        elif _ft_phase == "reveal":
            # ── 翻牌动画 ──
            timer 0.8 action [Function(fortune_draw), SetScreenVariable("_ft_phase", "result")]

            frame:
                ypos 54 xfill True ysize 514
                background Solid("#0d0a14")
                padding (14, 20)

                vbox:
                    align (0.5, 0.4) spacing 16

                    # 选中的牌翻转
                    frame:
                        xsize 80 ysize 110
                        xalign 0.5
                        background Solid("#e8c8ff33")
                        at transform:
                            zoom 1.0
                            easein_back 0.4 zoom 1.2
                            easeout 0.3 zoom 1.0
                        text "✦" align (0.5, 0.5) size 30 color "#e8c8ff"

                    text "命运正在揭晓……" size 12 color "#e8c8ff88" xalign 0.5

        else:
            # ── 结果展示 ──
            if _ft_result:
                $ _ftr = _ft_result
                $ _ftr_name = _ftr.get("level_name", "?")
                $ _ftr_color = _ftr.get("level_color", "#ffffff")
                $ _ftr_sign = _ftr.get("sign", "")
                $ _ftr_date = _ftr.get("date", "")
                # 根据当前人格选择解读
                $ _ftr_reading = _ftr.get("mutsumi", "") if _ft_persona == "wakaba" else _ftr.get("mortis", "")
                $ _ftr_speaker = "若叶睦" if _ft_persona == "wakaba" else "墨缇斯"
                $ _ftr_spk_color = "#8FBC8F" if _ft_persona == "wakaba" else "#CC4444"

                frame:
                    ypos 54 xfill True ysize 514
                    background Solid("#0d0a14")
                    padding (14, 16)

                    viewport:
                        xfill True ysize 500
                        mousewheel True scrollbars None

                        vbox:
                            spacing 14 xfill True

                            null height 10

                            # 运势等级
                            frame:
                                xalign 0.5 xsize 120 ysize 50
                                background Solid(_ftr_color + "22")
                                text "[_ftr_name]" align (0.5, 0.5) size 28 color _ftr_color bold True

                            # 日期
                            text "[_ftr_date]" size 10 color "#ffffff33" xalign 0.5

                            add Solid("#e8c8ff22") xsize 200 ysize 1 xalign 0.5

                            # 签文
                            frame:
                                xfill True
                                background Solid("#ffffff06")
                                padding (16, 12)
                                text "「[_ftr_sign]」" size 14 color "#ffffffcc" text_align 0.5 xalign 0.5

                            add Solid("#e8c8ff11") xsize 200 ysize 1 xalign 0.5

                            # 睦的解读
                            frame:
                                xfill True
                                background Solid(_ftr_spk_color + "11")
                                padding (14, 12)
                                vbox:
                                    spacing 6
                                    text "[_ftr_speaker]的解读：" size 11 color _ftr_spk_color
                                    text "[_ftr_reading]" size 13 color "#ffffffcc" line_spacing 6

                            null height 6

                            if not _ft_can:
                                text "明天再来抽签吧" size 10 color "#ffffff33" xalign 0.5

                            # 切换人格视角
                            if _ft_persona == "wakaba":
                                $ _alt_reading = _ftr.get("mortis", "")
                                textbutton "看看墨缇斯怎么说":
                                    action SetVariable("_ft_persona", "mortis")
                                    text_size 11 text_color "#CC444488" text_hover_color "#CC4444"
                                    xalign 0.5
                            else:
                                $ _alt_reading = _ftr.get("mutsumi", "")
                                textbutton "看看若叶睦怎么说":
                                    action SetVariable("_ft_persona", "wakaba")
                                    text_size 11 text_color "#8FBC8F88" text_hover_color "#8FBC8F"
                                    xalign 0.5

            else:
                frame:
                    ypos 54 xfill True ysize 514
                    background Solid("#0d0a14")
                    text "还没有抽过签" align (0.5, 0.5) size 14 color "#ffffff33"

        # 底部
        frame:
            ypos 518 xfill True ysize 50
            background Solid("#0a0814")
            padding (12, 6)
            button:
                action [SetVariable("phone_current_view", "home"), SetScreenVariable("_ft_phase", "idle")]
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
