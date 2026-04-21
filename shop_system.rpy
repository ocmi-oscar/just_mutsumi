# ==============================================================================
# 🏪 商店 — Fragment Exchange Shop
# 将抽卡获得的黄瓜分解为碎片，兑换各种材料
# ==============================================================================

default persistent.shop_fragments = 0

init python:
    import random as _shop_rng

    # 分解价值
    _SHOP_DECOMPOSE = {
        3: 1,    # 3星 → 1碎片
        4: 5,    # 4星 → 5碎片
    }

    # 商品列表
    _SHOP_ITEMS = [
        {"id": "seed_basic",    "name": "普通种子",       "cost": 3,   "type": "seed",      "desc": "最基础的黄瓜种子。成长周期2天。"},
        {"id": "seed_rare",     "name": "优质种子",       "cost": 8,   "type": "seed",      "desc": "品质更好的种子。成长周期3天，产出更多。"},
        {"id": "seed_epic",     "name": "传说种子",       "cost": 20,  "type": "seed",      "desc": "极其稀有的种子。成长周期5天，丰收时有惊喜。"},
        {"id": "fertilizer",    "name": "肥料",           "cost": 5,   "type": "material",  "desc": "加速植物生长，缩短1天成长时间。"},
        {"id": "water_plus",    "name": "营养液",         "cost": 3,   "type": "material",  "desc": "提升一次收获量20%。"},
        {"id": "coins_10",      "name": "睦币 x10",      "cost": 10,  "type": "currency",  "desc": "10枚睦币。"},
        {"id": "coins_50",      "name": "睦币 x50",      "cost": 45,  "type": "currency",  "desc": "50枚睦币，批量折扣。"},
        {"id": "story_ticket",  "name": "剧情解锁卷",    "cost": 30,  "type": "ticket",    "desc": "解锁一段隐藏剧情。"},
        {"id": "wp_ticket",     "name": "壁纸解锁卷",    "cost": 40,  "type": "ticket",    "desc": "解锁一张手机壁纸。上限9张。"},
    ]

    def shop_decompose_all():
        """一键分解所有3星4星黄瓜"""
        inv = persistent.player_inventory or {}
        total_frags = 0
        decomposed = 0

        # 从gacha_all_items找所有可分解物品
        for item in gacha_all_items:
            if item["type"] == "item" and item["rarity"] in (3, 4):
                item_id = item["id"]
                count = inv.get(item_id, 0)
                if count > 0:
                    frags = count * _SHOP_DECOMPOSE[item["rarity"]]
                    total_frags += frags
                    decomposed += count
                    inv[item_id] = 0

        if total_frags > 0:
            persistent.shop_fragments = (persistent.shop_fragments or 0) + total_frags
            persistent.player_inventory = inv
            renpy.save_persistent()
            renpy.notify("分解了{}个黄瓜，获得{}碎片".format(decomposed, total_frags))
        else:
            renpy.notify("没有可分解的黄瓜")
        renpy.restart_interaction()

    def shop_decompose_single(item_id, rarity):
        """分解单个物品"""
        inv = persistent.player_inventory or {}
        count = inv.get(item_id, 0)
        if count <= 0:
            return
        frags = _SHOP_DECOMPOSE.get(rarity, 1)
        inv[item_id] = count - 1
        persistent.shop_fragments = (persistent.shop_fragments or 0) + frags
        persistent.player_inventory = inv
        renpy.save_persistent()
        renpy.notify("+{} 碎片".format(frags))
        renpy.restart_interaction()

    def shop_buy(item_idx):
        """购买商品"""
        if item_idx < 0 or item_idx >= len(_SHOP_ITEMS):
            return
        item = _SHOP_ITEMS[item_idx]
        cost = item["cost"]
        frags = persistent.shop_fragments or 0

        if frags < cost:
            renpy.notify("碎片不足")
            return

        persistent.shop_fragments = frags - cost

        # 发放奖励
        itype = item["type"]
        iid = item["id"]

        if itype == "currency":
            amount = 10 if "10" in iid else 50
            persistent.mutsumi_coins = (getattr(persistent, 'mutsumi_coins', 0) or 0) + amount
        elif itype == "ticket" and iid == "story_ticket":
            persistent.milestone_story_tickets = (getattr(persistent, 'milestone_story_tickets', 0) or 0) + 1
        elif itype == "ticket" and iid == "wp_ticket":
            wp = getattr(persistent, 'milestone_wallpaper_tickets', 0) or 0
            if wp >= 9:
                renpy.notify("壁纸卷已达上限")
                persistent.shop_fragments = frags  # 退还
                return
            persistent.milestone_wallpaper_tickets = wp + 1
        elif itype in ("seed", "material"):
            # 存入温室材料背包
            if persistent.greenhouse_inventory is None:
                persistent.greenhouse_inventory = {}
            cur = persistent.greenhouse_inventory.get(iid, 0)
            persistent.greenhouse_inventory[iid] = cur + 1

        renpy.save_persistent()
        renpy.notify("购买成功！")
        renpy.restart_interaction()

    def shop_get_decomposable():
        """获取可分解的物品列表"""
        inv = persistent.player_inventory or {}
        result = []
        for item in gacha_all_items:
            if item["type"] == "item" and item["rarity"] in (3, 4):
                count = inv.get(item["id"], 0)
                if count > 0:
                    result.append({"id": item["id"], "name": item["name"], "rarity": item["rarity"], "count": count})
        return result


# ==============================================================================
# 手机界面
# ==============================================================================

default persistent.greenhouse_inventory = {}

screen phone_view_shop():
    default _shop_tab = 0

    $ _shop_frags = persistent.shop_fragments or 0
    $ _shop_decomp = shop_get_decomposable()

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 54
            background Solid("#2a1a10")
            padding (14, 8)
            hbox:
                xfill True yalign 0.5
                vbox:
                    spacing 1
                    text "商店" size 14 color "#ffa040" bold True
                    text "Fragment Shop" size 7 color "#ffffff33"
                vbox:
                    xalign 1.0 spacing 1
                    text "碎片" size 9 color "#ffa04088" xalign 1.0
                    text "[_shop_frags]" size 16 color "#ffa040" bold True xalign 1.0 font "DejaVuSans.ttf"

        # Tab
        frame:
            ypos 54 xfill True ysize 30
            background Solid("#1a1008")
            padding (0, 0)
            hbox:
                xfill True
                button:
                    xsize 149 ysize 30
                    background Solid("#ffa04022" if _shop_tab == 0 else "#00000000")
                    action SetScreenVariable("_shop_tab", 0)
                    text "分解" align (0.5, 0.5) size 11 color ("#ffa040" if _shop_tab == 0 else "#ffffff44")
                button:
                    xsize 149 ysize 30
                    background Solid("#ffa04022" if _shop_tab == 1 else "#00000000")
                    action SetScreenVariable("_shop_tab", 1)
                    text "兑换" align (0.5, 0.5) size 11 color ("#ffa040" if _shop_tab == 1 else "#ffffff44")

        # 内容
        viewport:
            ypos 88 ysize 420
            xfill True mousewheel True scrollbars None

            frame:
                xfill True
                background Solid("#1a1008")
                padding (12, 12)

                if _shop_tab == 0:
                    # ── 分解 ──
                    vbox:
                        spacing 8 xfill True

                        # 一键分解
                        button:
                            xfill True ysize 40
                            background Solid("#ffa04033")
                            hover_background Solid("#ffa04055")
                            action Function(shop_decompose_all)
                            text "一键分解全部黄瓜" align (0.5, 0.5) size 13 color "#ffa040" bold True

                        text "3星=1碎片  4星=5碎片" size 9 color "#ffffff33" xalign 0.5

                        add Solid("#ffffff11") xsize 268 ysize 1

                        if _shop_decomp:
                            for _di in range(len(_shop_decomp)):
                                $ _sd = _shop_decomp[_di]
                                $ _sd_name = _sd["name"]
                                $ _sd_count = _sd["count"]
                                $ _sd_rarity = _sd["rarity"]
                                $ _sd_frags = _SHOP_DECOMPOSE.get(_sd_rarity, 1)
                                $ _sd_color = "#6ab8d8" if _sd_rarity == 3 else "#b088d0"

                                frame:
                                    xfill True ysize 40
                                    background Solid("#ffffff06")
                                    padding (10, 6)
                                    hbox:
                                        spacing 8 xfill True yalign 0.5
                                        text "[_sd_rarity]★" size 11 color _sd_color yalign 0.5
                                        text "[_sd_name]" size 11 color "#ffffffcc" yalign 0.5
                                        text "x[_sd_count]" size 10 color "#ffffff66" yalign 0.5
                                        textbutton "分解":
                                            action Function(shop_decompose_single, _sd["id"], _sd_rarity)
                                            text_size 10 text_color "#ffa040" text_hover_color "#ffffff"
                                            xalign 1.0 yalign 0.5
                        else:
                            null height 30
                            text "没有可分解的黄瓜" size 12 color "#ffffff33" xalign 0.5
                            text "去M-Box抽卡获取吧" size 10 color "#ffffff22" xalign 0.5

                else:
                    # ── 兑换 ──
                    vbox:
                        spacing 6 xfill True

                        for _si in range(len(_SHOP_ITEMS)):
                            $ _item = _SHOP_ITEMS[_si]
                            $ _s_name = _item["name"]
                            $ _s_cost = _item["cost"]
                            $ _s_desc = _item["desc"]
                            $ _s_afford = _shop_frags >= _s_cost

                            button:
                                xfill True yminimum 52
                                background Solid("#ffffff08" if _s_afford else "#ffffff04")
                                hover_background Solid("#ffa04015" if _s_afford else "#ffffff04")
                                action Function(shop_buy, _si)
                                sensitive _s_afford
                                padding (10, 8)

                                hbox:
                                    spacing 8 xfill True yalign 0.5
                                    vbox:
                                        spacing 2 yalign 0.5
                                        text "[_s_name]" size 12 color ("#ffffffcc" if _s_afford else "#ffffff44")
                                        text "[_s_desc]" size 8 color "#ffffff33"
                                    text "[_s_cost]" size 12 color ("#ffa040" if _s_afford else "#ffffff22") xalign 1.0 yalign 0.5 font "DejaVuSans.ttf"

        # 底部
        frame:
            ypos 512 xfill True ysize 56
            background Solid("#120a04")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
