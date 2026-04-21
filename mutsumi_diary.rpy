# ==============================================================================
# 📖 睦の日記 — Mutsumi's Action-Triggered Diary
# 基于玩家每日行为数据的碎片化文本生成器
# ==============================================================================

# ── 行为追踪变量 ──────────────────────────────────────────────

default persistent.diary_today_data = None
default persistent.diary_yesterday_entry = ""
default persistent.diary_last_date = ""
default persistent.diary_login_streak = 0

init python:
    import random as _diary_rng
    import datetime as _diary_dt
    import time as _diary_time

    # ── 今日行为数据结构 ──
    def diary_new_day():
        return {
            "date": "",
            "login_hour": 0,
            "talk_count": 0,
            "played_game": False,
            "used_gacha": False,
            "did_pomodoro": False,
            "online_start": 0.0,
            "online_seconds": 0,
            "gw_start": 0.0,
            "gw_end": 0.0,
        }

    def diary_ensure_today():
        """确保今日数据存在，如果是新的一天则结算昨天并重置"""
        today_str = _diary_dt.date.today().strftime("%Y-%m-%d")
        if persistent.diary_today_data is None:
            persistent.diary_today_data = diary_new_day()
        if persistent.diary_today_data.get("date", "") != today_str:
            # 新的一天：先结算昨天的日记
            old = persistent.diary_today_data
            if old.get("date", ""):
                persistent.diary_yesterday_entry = diary_generate(old)
            # 更新连续登录
            if persistent.diary_last_date:
                try:
                    last = _diary_dt.datetime.strptime(persistent.diary_last_date, "%Y-%m-%d").date()
                    diff = (_diary_dt.date.today() - last).days
                    if diff == 1:
                        persistent.diary_login_streak += 1
                    elif diff > 1:
                        persistent.diary_login_streak = 1
                except:
                    persistent.diary_login_streak = 1
            else:
                persistent.diary_login_streak = 1
            persistent.diary_last_date = today_str
            # 重置今日数据
            nd = diary_new_day()
            nd["date"] = today_str
            nd["login_hour"] = _diary_dt.datetime.now().hour
            nd["online_start"] = _diary_time.time()
            # 记录当前好感度
            try:
                nd["gw_start"] = getattr(persistent, 'goodwill_wakaba', 0)
            except:
                nd["gw_start"] = 0
            persistent.diary_today_data = nd
            renpy.save_persistent()

    # ── 行为记录钩子（在各处调用）──
    def diary_log_talk():
        diary_ensure_today()
        persistent.diary_today_data["talk_count"] = persistent.diary_today_data.get("talk_count", 0) + 1
        renpy.save_persistent()

    def diary_log_game():
        diary_ensure_today()
        persistent.diary_today_data["played_game"] = True
        renpy.save_persistent()

    def diary_log_gacha():
        diary_ensure_today()
        persistent.diary_today_data["used_gacha"] = True
        renpy.save_persistent()

    def diary_log_pomodoro():
        diary_ensure_today()
        persistent.diary_today_data["did_pomodoro"] = True
        renpy.save_persistent()

    # ── 文案库 ──────────────────────────────────────────────

    _DIARY_OPENING = {
        "day": [
            "今天早上的光线很好。{0}出现的时候，光正好照在吉他弦上。",
            "温室里的温度刚刚好。{0}推开门的时候，带进来了一点微风。",
            "白天的黄瓜藤看起来很有精神。和{0}一起度过的上午，很安静。",
            "阳光穿过温室的玻璃，在地上画了一些格子。{0}踩着那些光走了进来。",
            "给植物翻了翻土。{0}来的时候，手上还沾着泥。",
        ],
        "night": [
            "天已经很暗了。本来打算去睡觉……还好{0}来了。",
            "晚上的温室有点冷。但是看到{0}的时候，稍微暖和了一点。",
            "只有仪表的指示灯亮着。{0}在深夜陪我，辛苦了。",
            "月光透过窗户洒在吉他上。{0}来了，夜晚变得没那么安静了。",
            "夜里的黄瓜叶上有露水。{0}来得很晚……但还是来了。",
        ],
        "streak": [
            "今天{0}也来了。习惯是一件有点可怕，但又让人安心的事情。",
            "连续看到{0}的脸。就像按时给植物浇水一样，让人很踏实。",
            "今天也没有缺席呢。谢谢{0}。",
            "{0}每天都来。这种节奏，像是一首很稳定的曲子。",
        ],
        "return": [
            "温室里很安静。昨天只有风的声音。今天……{0}终于来了。",
            "土壤干了一点。{0}不在的时候，时间过得很慢。",
            "终于来了。我还以为{0}把我和温室一起忘记了。",
            "好久没有看到{0}了。叶子好像也在等你。",
        ],
    }

    _DIARY_INTERACT = {
        "talked_much": [
            "和{0}说了一些话。我的声音有点小，但{0}好像听见了。",
            "{0}今天聊了很多。虽然我不太会接话，但我都有在认真听。",
            "听到了{0}的声音。比木吉他的扫弦声还要好听。",
            "今天说的话比平时多。舌头有点打结，但{0}没有笑我。",
        ],
        "talked_none": [
            "只是坐在一起。没有说话。我看着叶子，{0}看着我。",
            "{0}只是默默地待着。不用费力去找话题，这种默契我很喜欢。",
            "温室里只能听见彼此的呼吸声。一点也不觉得尴尬。",
        ],
        "played_game": [
            "{0}好像很喜欢那个游戏。稍微有点吵，但不讨厌。",
            "{0}玩游戏的时候很认真。我也在旁边偷偷看着。",
            "一起玩了游戏。希望{0}觉得开心。",
        ],
        "used_gacha": [
            "{0}拿到了新的东西。看{0}专注的样子，稍微有点羡慕那个盒子。",
            "{0}打开了M-Box。不知道里面有没有{0}真正想要的东西。",
            "收集的物品又变多了。那是{0}在这里留下的痕迹。",
        ],
        "did_pomodoro": [
            "嘱咐{0}去专注。{0}照做了。就像照顾植物一样……希望{0}健康。",
            "{0}很认真地完成了番茄钟。是个知道自律的人呢。",
            "看着{0}好好专注学习，我也会觉得放心。",
        ],
    }

    _DIARY_DURATION = {
        "short": [
            "{0}很快就走了。还没来得及调好一根弦。",
            "只是打了个招呼就下线了。有点短暂，但总比不来要好。",
            "{0}似乎很忙。希望下次能多留一会儿。",
        ],
        "medium": [
            "{0}陪了我一会儿。时间刚刚好，足够我给幼苗浇完一次水。",
            "{0}停留的时间，刚好够我弹完一首不完整的曲子。",
            "不长不短的陪伴。温室里的空气变得很舒服。",
        ],
        "long": [
            "待了很久。久到外面的光线都变了。其实，一直和{0}待在这里也可以。",
            "陪了我很长很长的时间。{0}不会觉得无聊吗？不过，我很开心。",
            "感觉好像一整天都和{0}待在一起。藤蔓好像都因为这样长快了。",
        ],
    }

    _DIARY_ENDING = {
        "gw_up": [
            "黄瓜的藤蔓，好像又靠近了一点。明天见，{0}。",
            "今天发生的一切都很美好。晚安，{0}。",
            "心里有一种满溢出来的感觉。希望明天也能见到{0}。",
        ],
        "gw_same": [
            "把吉他收起来了。平静的一天，又要结束了。",
            "温室要熄灯了。普通的日常，也很珍贵。",
            "给植物盖上布。今天也是安稳的一天。",
        ],
        "gw_down": [
            "是我哪里做错了吗。稍微，有点难过。",
            "稍微有点低落。希望明天，{0}能多对我笑一下。",
            "弦绷得太紧，好像要断了。今天……稍微有点累了。",
        ],
    }

    # ── 日记生成器 ──────────────────────────────────────────

    def diary_generate(data):
        pname = persistent.playername or "你"
        parts = []

        # 模块1：开篇
        hour = data.get("login_hour", 12)
        streak = persistent.diary_login_streak
        last_date = persistent.diary_last_date or ""

        if streak >= 3:
            parts.append(_diary_rng.choice(_DIARY_OPENING["streak"]).format(pname))
        elif streak <= 1 and last_date:
            parts.append(_diary_rng.choice(_DIARY_OPENING["return"]).format(pname))
        elif hour >= 6 and hour < 18:
            parts.append(_diary_rng.choice(_DIARY_OPENING["day"]).format(pname))
        else:
            parts.append(_diary_rng.choice(_DIARY_OPENING["night"]).format(pname))

        # 模块2：互动
        talk_count = data.get("talk_count", 0)
        if talk_count >= 3:
            parts.append(_diary_rng.choice(_DIARY_INTERACT["talked_much"]).format(pname))
        else:
            parts.append(_diary_rng.choice(_DIARY_INTERACT["talked_none"]).format(pname))

        if data.get("played_game", False):
            parts.append(_diary_rng.choice(_DIARY_INTERACT["played_game"]).format(pname))
        if data.get("used_gacha", False):
            parts.append(_diary_rng.choice(_DIARY_INTERACT["used_gacha"]).format(pname))
        if data.get("did_pomodoro", False):
            parts.append(_diary_rng.choice(_DIARY_INTERACT["did_pomodoro"]).format(pname))

        # 模块3：时长
        online = data.get("online_seconds", 0)
        if online < 300:
            parts.append(_diary_rng.choice(_DIARY_DURATION["short"]).format(pname))
        elif online < 1800:
            parts.append(_diary_rng.choice(_DIARY_DURATION["medium"]).format(pname))
        else:
            parts.append(_diary_rng.choice(_DIARY_DURATION["long"]).format(pname))

        # 模块4：结尾
        gw_start = data.get("gw_start") or 0
        gw_end = data.get("gw_end") or 0
        if gw_end > gw_start:
            parts.append(_diary_rng.choice(_DIARY_ENDING["gw_up"]).format(pname))
        elif gw_end < gw_start:
            parts.append(_diary_rng.choice(_DIARY_ENDING["gw_down"]).format(pname))
        else:
            parts.append(_diary_rng.choice(_DIARY_ENDING["gw_same"]).format(pname))

        return " ".join(parts)

    # ── 实时生成今日日记预览 ──
    def diary_preview_today():
        diary_ensure_today()
        d = persistent.diary_today_data
        if not d or not d.get("date"):
            return "……还没有什么可以记录的。"
        # 更新在线时长
        if d.get("online_start", 0) > 0:
            d["online_seconds"] = int(_diary_time.time() - d["online_start"])
        # 更新好感度
        try:
            d["gw_end"] = getattr(persistent, 'goodwill_wakaba', 0)
        except:
            d["gw_end"] = 0
        return diary_generate(d)


# ==============================================================================
# 手机内日记界面
# ==============================================================================

screen phone_view_diary():
    default _diary_tab = 0
    $ diary_ensure_today()
    $ _d_today_str = persistent.diary_today_data.get("date", "") if persistent.diary_today_data else ""
    $ _d_streak = persistent.diary_login_streak
    $ _d_yesterday = persistent.diary_yesterday_entry or ""
    $ _d_preview = diary_preview_today()

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 56
            background Solid("#1a1e2a")
            padding (14, 8)
            vbox:
                spacing 2
                text "睦の日記" size 14 color "#d4a0ff" bold True
                text "Mutsumi's Diary" size 8 color "#ffffff44"

        # Tab切换
        frame:
            ypos 56 xfill True ysize 32
            background Solid("#0d1018")
            padding (0, 0)
            hbox:
                xfill True

                # 用 screen default 切换
                button:
                    xsize 149 ysize 32
                    background Solid("#d4a0ff22" if not _diary_tab else "#00000000")
                    hover_background Solid("#d4a0ff11")
                    action SetScreenVariable("_diary_tab", False)
                    text "今日" align (0.5, 0.5) size 12 color ("#d4a0ff" if not _diary_tab else "#ffffff55") bold (not _diary_tab)

                button:
                    xsize 149 ysize 32
                    background Solid("#d4a0ff22" if _diary_tab else "#00000000")
                    hover_background Solid("#d4a0ff11")
                    action SetScreenVariable("_diary_tab", True)
                    text "昨日" align (0.5, 0.5) size 12 color ("#d4a0ff" if _diary_tab else "#ffffff55") bold _diary_tab

        # 内容区
        viewport:
            ypos 92 ysize 420
            xfill True mousewheel True scrollbars None

            frame:
                xfill True
                background Solid("#0d1018")
                padding (16, 16)

                if not _diary_tab:
                    # 今日预览
                    vbox:
                        spacing 12 xfill True

                        hbox:
                            spacing 8
                            text "[_d_today_str]" size 12 color "#ffffff66"
                            text "连续登录 [_d_streak] 天" size 10 color "#d4a0ff88"

                        add Solid("#d4a0ff22") xsize 260 ysize 1

                        # 行为标签
                        $ _td = persistent.diary_today_data or {}
                        $ _td_talks = _td.get("talk_count", 0)
                        $ _td_game = _td.get("played_game", False)
                        $ _td_gacha = _td.get("used_gacha", False)
                        $ _td_pomo = _td.get("did_pomodoro", False)
                        hbox:
                            spacing 6
                            if _td_talks > 0:
                                frame:
                                    background Solid("#95e1d322")
                                    padding (6, 2)
                                    text "对话x[_td_talks]" size 9 color "#95e1d3"
                            if _td_game:
                                frame:
                                    background Solid("#6ab8d822")
                                    padding (6, 2)
                                    text "游戏" size 9 color "#6ab8d8"
                            if _td_gacha:
                                frame:
                                    background Solid("#ffd70022")
                                    padding (6, 2)
                                    text "抽卡" size 9 color "#ffd700"
                            if _td_pomo:
                                frame:
                                    background Solid("#ff666622")
                                    padding (6, 2)
                                    text "专注" size 9 color "#ff6666"

                        null height 6

                        text "[_d_preview]" size 13 color "#ffffffcc" line_spacing 8

                        null height 10
                        text "日记会在次日生成完整版本" size 9 color "#ffffff33" xalign 0.5

                else:
                    # 昨日日记
                    vbox:
                        spacing 12 xfill True

                        text "昨日的日记" size 12 color "#ffffff66"
                        add Solid("#d4a0ff22") xsize 260 ysize 1
                        null height 6

                        if _d_yesterday:
                            text "[_d_yesterday]" size 13 color "#ffffffcc" line_spacing 8
                        else:
                            null height 40
                            text "……还没有昨天的记忆。" size 13 color "#ffffff44" xalign 0.5

        # 底部
        frame:
            ypos 516 xfill True ysize 52
            background Solid("#0a0c14")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)

    default _diary_tab = False
