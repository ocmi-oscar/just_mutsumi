# ==============================================================================
# 🌱 温室种植 — Greenhouse Farm
# 种植黄瓜 + AI邻居农场 + 偷菜系统
# ==============================================================================

default persistent.gh_farm_plots = None
default persistent.gh_farm_harvest_total = 0
default persistent.gh_farm_stolen_total = 0
default persistent.gh_farm_neighbors = None
default persistent.gh_farm_last_refresh = ""
default persistent.greenhouse_inventory = {}

init python:
    import random as _ghf_rng
    import time as _ghf_time
    import datetime as _ghf_dt

    # ── 种子配置 ──
    _GHF_SEEDS = {
        "seed_basic": {
            "name": "普通黄瓜",
            "grow_hours": 48,
            "yield_min": 3, "yield_max": 6,
            "color": "#8FBC8F",
        },
        "seed_rare": {
            "name": "优质黄瓜",
            "grow_hours": 72,
            "yield_min": 6, "yield_max": 12,
            "color": "#6ab8d8",
        },
        "seed_epic": {
            "name": "传说黄瓜",
            "grow_hours": 120,
            "yield_min": 15, "yield_max": 30,
            "color": "#d4a0ff",
        },
    }

    # ── AI邻居 ──
    _GHF_NEIGHBORS = [
        {"id": "soyo",     "name": "长崎爽世", "color": "#CC6699", "personality": "diligent", "icon": "爽"},
        {"id": "sakiko",   "name": "丰川祥子", "color": "#9966CC", "personality": "strict",   "icon": "祥"},
        {"id": "tomorin",  "name": "千早灯",   "color": "#FF9966", "personality": "cheerful", "icon": "灯"},
        {"id": "uika",     "name": "三角初华", "color": "#FF66AA", "personality": "gentle",   "icon": "初"},
        {"id": "nyamu",    "name": "祐天寺若麦","color": "#FFCC00", "personality": "wild",     "icon": "喵"},
        {"id": "umiri",    "name": "八幡海铃", "color": "#4488CC", "personality": "quiet",    "icon": "海"},
    ]

    # ── 偷菜台词 ──
    _GHF_STEAL_LINES = {
        "soyo":    "爽世发现你偷了她的菜，但只是微笑着说「没关系，下次记得打招呼哦。」",
        "sakiko":  "祥子面无表情地看着你：「作为惩罚，你需要多练习三个小时的吉他。」",
        "tomorin": "灯开心地说：「欸？你喜欢我种的菜！太好了！多拿点！」",
        "uika":    "初华温柔地递给你一个篮子：「要偷的话……至少用这个装。」",
        "nyamu":   "若麦大喊：「哇！偷菜的贼！抓住她——啊不对，是你啊。那算了。」",
        "umiri":   "海铃沉默了一会儿：「……反正我种太多了。」",
    }

    _GHF_GUARD_LINES = {
        "soyo":    "爽世正在巡视她的农场。不是偷菜的好时机……",
        "sakiko":  "祥子坐在农场中央，正在记录数据。不敢靠近。",
        "tomorin": "灯在给植物唱歌。她好像没注意到你。（但你还是不忍心偷）",
        "uika":    "初华正在浇水，对你微笑着挥了挥手。（太善良了偷不下去）",
        "nyamu":   "若麦正在到处跑来跑去。偷菜风险太高了。",
        "umiri":   "海铃不在。但她的菜还没成熟。",
    }

    # ══════════════════════════════════════════════════════════
    #  农场逻辑
    # ══════════════════════════════════════════════════════════

    def ghf_init():
        """初始化农场"""
        if persistent.gh_farm_plots is None:
            persistent.gh_farm_plots = [None, None, None, None, None]  # 5个地块
        if persistent.greenhouse_inventory is None:
            persistent.greenhouse_inventory = {}
        ghf_refresh_neighbors()

    def ghf_plant(plot_idx, seed_id):
        """在指定地块种植"""
        plots = persistent.gh_farm_plots
        if plots[plot_idx] is not None:
            renpy.notify("这块地已经有植物了")
            return

        inv = persistent.greenhouse_inventory
        if inv.get(seed_id, 0) <= 0:
            renpy.notify("种子不足！去商店兑换")
            return

        inv[seed_id] = inv[seed_id] - 1
        seed_info = _GHF_SEEDS[seed_id]

        # 好感度加成：每10点好感减少5%生长时间
        gw = getattr(persistent, 'goodwill_wakaba', 0) or 0
        gw_bonus = min(gw / 10 * 0.05, 0.3)
        actual_hours = seed_info["grow_hours"] * (1.0 - gw_bonus)

        plots[plot_idx] = {
            "seed_id": seed_id,
            "name": seed_info["name"],
            "planted_at": _ghf_time.time(),
            "grow_seconds": actual_hours * 3600,
            "yield_min": seed_info["yield_min"],
            "yield_max": seed_info["yield_max"],
            "fertilized": False,
            "watered": False,
        }
        renpy.save_persistent()
        renpy.notify("种下了" + seed_info["name"])
        renpy.restart_interaction()

    def ghf_harvest(plot_idx):
        """收获"""
        plots = persistent.gh_farm_plots
        plot = plots[plot_idx]
        if plot is None:
            return

        progress = ghf_get_progress(plot)
        if progress < 1.0:
            renpy.notify("还没成熟呢……")
            return

        ymin = plot["yield_min"]
        ymax = plot["yield_max"]
        bonus = 1.2 if plot.get("watered") else 1.0
        amount = int(_ghf_rng.randint(ymin, ymax) * bonus)

        persistent.shop_fragments = (persistent.shop_fragments or 0) + amount
        persistent.gh_farm_harvest_total = (persistent.gh_farm_harvest_total or 0) + amount
        plots[plot_idx] = None
        renpy.save_persistent()
        renpy.notify("收获了 {} 碎片！".format(amount))
        renpy.restart_interaction()

    def ghf_use_item(plot_idx, item_id):
        """对地块使用道具"""
        plots = persistent.gh_farm_plots
        plot = plots[plot_idx]
        if plot is None:
            return

        inv = persistent.greenhouse_inventory
        if inv.get(item_id, 0) <= 0:
            renpy.notify("道具不足")
            return

        if item_id == "fertilizer" and not plot.get("fertilized"):
            plot["grow_seconds"] = max(plot["grow_seconds"] - 86400, 3600)
            plot["fertilized"] = True
            inv["fertilizer"] = inv["fertilizer"] - 1
            renpy.notify("施肥成功！成长时间-1天")
        elif item_id == "water_plus" and not plot.get("watered"):
            plot["watered"] = True
            inv["water_plus"] = inv["water_plus"] - 1
            renpy.notify("浇了营养液！收获+20%")
        else:
            renpy.notify("已经用过了")
            return

        renpy.save_persistent()
        renpy.restart_interaction()

    def ghf_get_progress(plot):
        """获取生长进度 0.0~1.0"""
        if plot is None:
            return 0.0
        elapsed = _ghf_time.time() - plot["planted_at"]
        return min(elapsed / max(plot["grow_seconds"], 1), 1.0)

    def ghf_get_stage(progress):
        """进度→阶段文字"""
        if progress >= 1.0: return "成熟"
        elif progress >= 0.7: return "结果"
        elif progress >= 0.4: return "开花"
        elif progress >= 0.1: return "发芽"
        else: return "种子"

    # ══════════════════════════════════════════════════════════
    #  AI邻居农场 & 偷菜
    # ══════════════════════════════════════════════════════════

    def ghf_refresh_neighbors():
        """刷新邻居农场状态（每天一次）"""
        today = _ghf_dt.date.today().strftime("%Y-%m-%d")
        if persistent.gh_farm_last_refresh == today:
            return

        persistent.gh_farm_last_refresh = today
        neighbors = {}
        for nb in _GHF_NEIGHBORS:
            nid = nb["id"]
            # 随机生成邻居的农场状态
            has_crop = _ghf_rng.random() < 0.7  # 70%概率有作物
            is_ripe = _ghf_rng.random() < 0.4 if has_crop else False
            is_guarding = _ghf_rng.random() < 0.35
            stolen_today = False

            neighbors[nid] = {
                "has_crop": has_crop,
                "is_ripe": is_ripe,
                "is_guarding": is_guarding,
                "stolen_today": stolen_today,
                "crop_name": _ghf_rng.choice(["黄瓜", "番茄", "草莓", "西瓜", "向日葵"]),
            }
        persistent.gh_farm_neighbors = neighbors
        renpy.save_persistent()

    def ghf_steal(neighbor_id):
        """偷菜"""
        ghf_refresh_neighbors()
        nb_data = persistent.gh_farm_neighbors.get(neighbor_id, {})

        if nb_data.get("stolen_today"):
            renpy.notify("今天已经偷过了！做人不能太贪心。")
            return None
        if not nb_data.get("has_crop"):
            renpy.notify("邻居的地是空的")
            return None
        if not nb_data.get("is_ripe"):
            renpy.notify("还没成熟，偷不了")
            return None
        if nb_data.get("is_guarding"):
            # 被抓
            line = _GHF_GUARD_LINES.get(neighbor_id, "邻居在看着你。")
            return ("guard", line)

        # 偷成功
        amount = _ghf_rng.randint(1, 4)
        persistent.shop_fragments = (persistent.shop_fragments or 0) + amount
        persistent.gh_farm_stolen_total = (persistent.gh_farm_stolen_total or 0) + amount
        nb_data["stolen_today"] = True
        renpy.save_persistent()

        line = _GHF_STEAL_LINES.get(neighbor_id, "你偷走了一些菜。")
        return ("success", line, amount)

    def ghf_get_inventory_display():
        """获取温室背包显示"""
        inv = persistent.greenhouse_inventory or {}
        items = []
        for sid, sdata in _GHF_SEEDS.items():
            count = inv.get(sid, 0)
            if count > 0:
                items.append({"id": sid, "name": sdata["name"] + "种子", "count": count, "type": "seed"})
        for mid, mname in [("fertilizer", "肥料"), ("water_plus", "营养液")]:
            count = inv.get(mid, 0)
            if count > 0:
                items.append({"id": mid, "name": mname, "count": count, "type": "material"})
        return items


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_farm():
    default _farm_tab = 0
    default _farm_plant_select = -1
    default _farm_steal_result = ""

    $ ghf_init()
    $ _plots = persistent.gh_farm_plots or [None]*5
    $ _frags = persistent.shop_fragments or 0
    $ _harvested = persistent.gh_farm_harvest_total or 0
    $ _stolen = persistent.gh_farm_stolen_total or 0

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 50
            background Solid("#1a2e1a")
            padding (14, 8)
            hbox:
                xfill True yalign 0.5
                vbox:
                    spacing 1
                    text "温室" size 14 color "#8FBC8F" bold True
                    text "Greenhouse" size 7 color "#ffffff33"
                vbox:
                    xalign 1.0 spacing 1
                    text "碎片 [_frags]" size 10 color "#ffa04088" xalign 1.0
                    text "收获 [_harvested]" size 8 color "#ffffff33" xalign 1.0

        # Tab
        frame:
            ypos 50 xfill True ysize 30
            background Solid("#0d1a0d")
            padding (0, 0)
            hbox:
                xfill True
                for _ti, _tn in enumerate(["我的农场", "邻居", "背包"]):
                    button:
                        xsize 99 ysize 30
                        background Solid("#8FBC8F22" if _farm_tab == _ti else "#00000000")
                        action SetScreenVariable("_farm_tab", _ti)
                        text "[_tn]" align (0.5, 0.5) size 11 color ("#8FBC8F" if _farm_tab == _ti else "#ffffff44")

        # 内容
        viewport:
            ypos 84 ysize 424
            xfill True mousewheel True scrollbars None

            frame:
                xfill True
                background Solid("#0d1a0d")
                padding (10, 10)

                if _farm_tab == 0:
                    # ══ 我的农场 ══
                    vbox:
                        spacing 8 xfill True

                        text "花圃" size 12 color "#8FBC8F88"

                        for _pi in range(5):
                            $ _plot = _plots[_pi]
                            $ _pnum = _pi + 1

                            if _plot is None:
                                # 空地
                                frame:
                                    xfill True ysize 56
                                    background Solid("#ffffff06")
                                    padding (10, 8)

                                    hbox:
                                        spacing 10 xfill True yalign 0.5
                                        text "[_pnum]" size 14 color "#ffffff22" yalign 0.5 font "DejaVuSans.ttf"
                                        text "空地" size 12 color "#ffffff33" yalign 0.5

                                        # 种植按钮
                                        if _farm_plant_select == _pi:
                                            # 选择种子
                                            $ _inv_seeds = [s for s in ghf_get_inventory_display() if s["type"] == "seed"]
                                            if _inv_seeds:
                                                hbox:
                                                    spacing 4 xalign 1.0
                                                    for _si in range(len(_inv_seeds)):
                                                        $ _seed = _inv_seeds[_si]
                                                        $ _sn = _seed["name"][:2]
                                                        $ _sc = _seed["count"]
                                                        textbutton "[_sn]([_sc])":
                                                            action [Function(ghf_plant, _pi, _seed["id"]), SetScreenVariable("_farm_plant_select", -1)]
                                                            text_size 9 text_color "#8FBC8F" text_hover_color "#ffffff"
                                                            yalign 0.5
                                            else:
                                                text "无种子" size 9 color "#ffffff33" xalign 1.0 yalign 0.5
                                        else:
                                            textbutton "种植":
                                                action SetScreenVariable("_farm_plant_select", _pi)
                                                text_size 11 text_color "#8FBC8F" text_hover_color "#ffffff"
                                                xalign 1.0 yalign 0.5

                            else:
                                # 有植物
                                $ _prog = ghf_get_progress(_plot)
                                $ _stage = ghf_get_stage(_prog)
                                $ _pname = _plot.get("name", "黄瓜")
                                $ _pct = int(_prog * 100)
                                $ _ripe = _prog >= 1.0
                                $ _seedid = _plot.get("seed_id", "seed_basic")
                                $ _scolor = _GHF_SEEDS.get(_seedid, {}).get("color", "#8FBC8F")

                                frame:
                                    xfill True ysize 56
                                    background Solid(_scolor + "11")
                                    padding (10, 8)

                                    hbox:
                                        spacing 8 xfill True yalign 0.5
                                        text "[_pnum]" size 14 color _scolor yalign 0.5 font "DejaVuSans.ttf"
                                        vbox:
                                            spacing 1 yalign 0.5
                                            text "[_pname]" size 11 color "#ffffffcc"
                                            hbox:
                                                spacing 6
                                                text "[_stage]" size 9 color _scolor
                                                text "[_pct]%" size 9 color "#ffffff44" font "DejaVuSans.ttf"
                                                if _plot.get("fertilized"):
                                                    text "肥" size 8 color "#ffa040"
                                                if _plot.get("watered"):
                                                    text "水" size 8 color "#6ab8d8"

                                        if _ripe:
                                            textbutton "收获":
                                                action Function(ghf_harvest, _pi)
                                                text_size 11 text_color "#ffd700" text_hover_color "#ffffff"
                                                xalign 1.0 yalign 0.5
                                        else:
                                            hbox:
                                                spacing 4 xalign 1.0 yalign 0.5
                                                if not _plot.get("fertilized"):
                                                    textbutton "肥":
                                                        action Function(ghf_use_item, _pi, "fertilizer")
                                                        text_size 10 text_color "#ffa04088" text_hover_color "#ffa040"
                                                if not _plot.get("watered"):
                                                    textbutton "水":
                                                        action Function(ghf_use_item, _pi, "water_plus")
                                                        text_size 10 text_color "#6ab8d888" text_hover_color "#6ab8d8"

                elif _farm_tab == 1:
                    # ══ 邻居农场 ══
                    vbox:
                        spacing 6 xfill True

                        text "偷了 [_stolen] 碎片" size 9 color "#ffffff22"

                        if _farm_steal_result:
                            frame:
                                xfill True
                                background Solid("#ffffff0a")
                                padding (10, 8)
                                text "[_farm_steal_result]" size 11 color "#ffffffcc" line_spacing 4
                            null height 4

                        $ _nb_states = persistent.gh_farm_neighbors or {}

                        for _ni in range(len(_GHF_NEIGHBORS)):
                            $ _nb = _GHF_NEIGHBORS[_ni]
                            $ _nid = _nb["id"]
                            $ _nname = _nb["name"]
                            $ _ncolor = _nb["color"]
                            $ _nicon = _nb["icon"]
                            $ _ns = _nb_states.get(_nid, {})
                            $ _n_has = _ns.get("has_crop", False)
                            $ _n_ripe = _ns.get("is_ripe", False)
                            $ _n_stolen = _ns.get("stolen_today", False)
                            $ _n_crop = _ns.get("crop_name", "黄瓜")

                            frame:
                                xfill True ysize 52
                                background Solid("#ffffff06")
                                padding (8, 6)

                                hbox:
                                    spacing 8 xfill True yalign 0.5

                                    frame:
                                        xsize 28 ysize 28
                                        background Solid(_ncolor)
                                        text "[_nicon]" align (0.5, 0.5) size 14 color "#ffffff" bold True

                                    vbox:
                                        spacing 1 yalign 0.5
                                        text "[_nname]" size 11 color "#ffffffcc"
                                        if not _n_has:
                                            text "空地" size 9 color "#ffffff33"
                                        elif _n_ripe:
                                            text "[_n_crop] · 成熟" size 9 color "#ffd700"
                                        else:
                                            text "[_n_crop] · 生长中" size 9 color "#8FBC8F88"

                                    if _n_ripe and not _n_stolen:
                                        textbutton "偷":
                                            action Function(ghf_do_steal, _nid)
                                            text_size 11 text_color "#ff6666" text_hover_color "#ffffff"
                                            xalign 1.0 yalign 0.5
                                    elif _n_stolen:
                                        text "已偷" size 9 color "#ffffff22" xalign 1.0 yalign 0.5

                elif _farm_tab == 2:
                    # ══ 背包 ══
                    vbox:
                        spacing 8 xfill True

                        $ _inv = ghf_get_inventory_display()
                        if _inv:
                            for _ii in range(len(_inv)):
                                $ _item = _inv[_ii]
                                $ _iname = _item["name"]
                                $ _icount = _item["count"]
                                frame:
                                    xfill True ysize 38
                                    background Solid("#ffffff06")
                                    padding (10, 6)
                                    hbox:
                                        xfill True yalign 0.5
                                        text "[_iname]" size 12 color "#ffffffcc"
                                        text "x[_icount]" size 12 color "#8FBC8F" xalign 1.0 font "DejaVuSans.ttf"
                        else:
                            null height 30
                            text "背包空空的" size 12 color "#ffffff33" xalign 0.5
                            text "去商店兑换种子和道具吧" size 10 color "#ffffff22" xalign 0.5

        # 底部
        frame:
            ypos 512 xfill True ysize 56
            background Solid("#0a0f0a")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)

init python:
    def ghf_do_steal(nid):
        """偷菜并显示结果"""
        result = ghf_steal(nid)
        if result is None:
            return
        if result[0] == "guard":
            store._farm_steal_result = result[1]
        elif result[0] == "success":
            store._farm_steal_result = result[1] + "\n获得 {} 碎片！".format(result[2])
        renpy.restart_interaction()
