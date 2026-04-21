# ==============================================================================
# 📖 对话回顾系统 — Dialogue Replay
# 为所有吉他睦/墨缇斯随机对话命名，提供回顾功能
# ==============================================================================

init python:

    # ══════════════════════════════════════════════════════════
    #  对话名称注册表
    # ══════════════════════════════════════════════════════════

    DIALOGUE_REGISTRY = {

        # ── 若叶睦（吉他睦）── 33条
        "p_guitar_v3_01": {"name": "关于「你来了」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_02": {"name": "关于「黄瓜与心」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_03": {"name": "关于「大家还好吗」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_04": {"name": "关于「不会说谎」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_05": {"name": "关于「打字声」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_06": {"name": "关于「修好的琴弦」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_07": {"name": "关于「面具与真我」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_08": {"name": "关于「苦涩的巧克力」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_09": {"name": "关于「你的背影」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_10": {"name": "关于「回不去了」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_11": {"name": "关于「枯叶与新生」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_12": {"name": "关于「苦涩的抹茶」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_13": {"name": "关于「大家散了」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_14": {"name": "关于「我是谁」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_15": {"name": "关于「指尖的茧」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_16": {"name": "关于「被拒绝的黄瓜」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_18": {"name": "关于「风扇与呼吸」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_19": {"name": "关于「你会腻吗」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_20": {"name": "关于「窗口内外」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_28": {"name": "关于「想变成树」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_29": {"name": "关于「凝固的时间」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_30": {"name": "关于「空旷的家」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_31": {"name": "关于「语言的变质」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_32": {"name": "关于「颤动的琴弦」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_33": {"name": "关于「跨越时空的光」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_34": {"name": "关于「你的名字」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_35": {"name": "关于「雨中心跳」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_36": {"name": "关于「天冷弦紧」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_37": {"name": "关于「黄瓜的种子」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_38": {"name": "关于「绿色围巾」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_39": {"name": "关于「被遗忘的物品」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_40": {"name": "关于「角落的苔藓」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},
        "p_guitar_v3_41": {"name": "关于「清水」的对话", "speaker": "若叶睦", "color": "#8FBC8F"},

        # ── 墨缇斯 ── 13条
        "p_metis_v3_01": {"name": "关于「观察频道」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_02": {"name": "关于「模仿爽世」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_03": {"name": "关于「海铃的拉面」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_05": {"name": "关于「我话太多了吗」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_06": {"name": "关于「难搞的琴弦」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_07": {"name": "关于「Ave Mujica的面具」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_08": {"name": "关于「送黄瓜的傻瓜」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_09": {"name": "关于「丢掉吉他」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_10": {"name": "关于「如果我消失了」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_11": {"name": "关于「模仿喵姆」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_12": {"name": "关于「搞砸一切」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_13": {"name": "关于「剪断琴弦」的对话", "speaker": "墨缇斯", "color": "#CC4444"},
        "p_metis_v3_14": {"name": "关于「初华的温柔」的对话", "speaker": "墨缇斯", "color": "#CC4444"},

        # ── 双人格互动 ── 19条
        "p_meta_v3_21": {"name": "关于「爱的游戏」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_22": {"name": "关于「噩梦」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_23": {"name": "关于「虚拟直播」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_24": {"name": "关于「感情是否虚假」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_25": {"name": "关于「喜欢的感觉」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_26": {"name": "关于「恋爱经历」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_27": {"name": "关于「捉迷藏」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_270": {"name": "关于「你的叹气」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        "p_meta_v3_28": {"name": "关于「蝴蝶与自由」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_29": {"name": "关于「摘下笑容」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_30": {"name": "关于「祥子的怨念」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_31": {"name": "关于「Ave Mujica的衣服」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_32": {"name": "关于「温室里的猫」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_33": {"name": "关于「你的视线」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_34": {"name": "关于「守护噩梦」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_35": {"name": "关于「游戏标题」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_36": {"name": "关于「好无聊」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_37": {"name": "关于「丧气台词」的对话", "speaker": "双人格", "color": "#d4a0ff"},
        " p_meta_v3_38": {"name": "关于「安静的墨缇斯」的对话", "speaker": "双人格", "color": "#d4a0ff"},
    }

    def get_seen_dialogues():
        """获取玩家已看过的对话列表，按类别分组"""
        seen = getattr(persistent, 'seen_random_labels', []) or []
        result = {"若叶睦": [], "墨缇斯": [], "双人格": []}
        for lid in DIALOGUE_REGISTRY:
            if lid in seen or lid.strip() in seen:
                info = DIALOGUE_REGISTRY[lid]
                result[info["speaker"]].append({
                    "id": lid,
                    "name": info["name"],
                    "color": info["color"],
                })
        return result

    def get_dialogue_progress():
        """获取对话收集进度"""
        seen = getattr(persistent, 'seen_random_labels', []) or []
        total = len(DIALOGUE_REGISTRY)
        found = 0
        for lid in DIALOGUE_REGISTRY:
            if lid in seen or lid.strip() in seen:
                found += 1
        return found, total

    def replay_dialogue(label_id):
        """回顾一段对话"""
        lid = label_id.strip()
        if renpy.has_label(lid):
            renpy.call_replay(lid)
        elif renpy.has_label(label_id):
            renpy.call_replay(label_id)


# ==============================================================================
# 对话回顾界面
# ==============================================================================

default _replay_tab = 0

screen dialogue_replay_screen():
    tag menu
    modal True
    zorder 200

    add Solid("#0d1210f0")

    $ _rp_data = get_seen_dialogues()
    $ _rp_found, _rp_total = get_dialogue_progress()
    $ _rp_tabs = ["若叶睦", "墨缇斯", "双人格"]
    $ _rp_colors = ["#8FBC8F", "#CC4444", "#d4a0ff"]
    $ _rp_cur_tab = _rp_tabs[_replay_tab] if _replay_tab < 3 else "若叶睦"
    $ _rp_list = _rp_data.get(_rp_cur_tab, [])
    $ _rp_cur_color = _rp_colors[_replay_tab] if _replay_tab < 3 else "#8FBC8F"

    # 顶部标题
    frame:
        xfill True ysize 80
        background Solid("#111a14")
        padding (30, 14)

        hbox:
            xfill True yalign 0.5

            vbox:
                spacing 4
                text "对话回顾" size 24 color "#ffffff" bold True
                text "Dialogue Archive" size 11 color "#ffffff44"

            vbox:
                xalign 1.0 spacing 2
                text "收集进度" size 10 color "#ffffff55" xalign 1.0
                text "[_rp_found] / [_rp_total]" size 18 color "#95e1d3" xalign 1.0 bold True font "DejaVuSans.ttf"

    # Tab 栏
    frame:
        ypos 80 xfill True ysize 40
        background Solid("#0a0f0c")
        padding (30, 0)

        hbox:
            yalign 0.5 spacing 0

            for _ti in range(3):
                $ _tn = _rp_tabs[_ti]
                $ _tc = _rp_colors[_ti]
                $ _t_active = (_replay_tab == _ti)
                $ _t_count = len(_rp_data.get(_tn, []))
                button:
                    xsize 200 ysize 40
                    background Solid(_tc + "22" if _t_active else "#00000000")
                    hover_background Solid(_tc + "11")
                    action SetVariable("_replay_tab", _ti)
                    hbox:
                        align (0.5, 0.5) spacing 6
                        text "[_tn]" size 14 color (_tc if _t_active else "#ffffff55") bold _t_active
                        text "([_t_count])" size 11 color (_tc + "88" if _t_active else "#ffffff33")

            # 关闭按钮
            textbutton "返回":
                action [Hide("dialogue_replay_screen")]
                text_size 14 text_color "#ffffff55" text_hover_color "#ffffff"
                xalign 1.0 yalign 0.5

    # 分割线
    add Solid(_rp_cur_color + "44") ypos 120 xsize 1280 ysize 2

    # 内容列表
    viewport:
        ypos 126 ysize 574
        xfill True mousewheel True scrollbars None

        vbox:
            spacing 2 xfill True

            if not _rp_list:
                null height 80
                text "还没有解锁的对话" size 16 color "#ffffff33" xalign 0.5
                text "在日常互动中触发随机对话即可解锁" size 12 color "#ffffff22" xalign 0.5
            else:
                for _di in range(len(_rp_list)):
                    $ _d = _rp_list[_di]
                    $ _did = _d["id"]
                    $ _dname = _d["name"]
                    $ _dcolor = _d["color"]

                    button:
                        xfill True ysize 56
                        background Solid("#ffffff05")
                        hover_background Solid(_dcolor + "15")
                        action Function(replay_dialogue, _did)
                        padding (30, 10)

                        hbox:
                            spacing 14 xfill True yalign 0.5

                            # 序号
                            $ _dnum = _di + 1
                            frame:
                                xsize 32 ysize 32
                                background Solid(_dcolor + "33")
                                text "[_dnum]" align (0.5, 0.5) size 12 color _dcolor font "DejaVuSans.ttf"

                            # 标题
                            text "[_dname]" size 14 color "#ffffffcc" yalign 0.5

                            # 播放图标
                            text "▶" size 12 color _dcolor xalign 1.0 yalign 0.5

                    add Solid("#ffffff08") xsize 1200 ysize 1 xalign 0.5

            null height 30
