# ==============================================================================
# 🃏 UNO!!! — 睦的纸牌对决 (v3 - 图片+fallback)
# ==============================================================================

init python:
    import random as _uno_rng

    _UNO_COLOR_FILE = {"red": "Red", "blue": "Blue", "green": "Green", "yellow": "Yellow"}

    class UnoCard(python_object):
        COLOR_CN = {"red": "红", "blue": "蓝", "green": "绿", "yellow": "黄", "wild": ""}
        BG = {"red": "#CC3333", "blue": "#2266CC", "green": "#22AA44", "yellow": "#CC9900", "wild": "#222222"}
        BG_DIM = {"red": "#661a1a", "blue": "#113366", "green": "#115522", "yellow": "#664d00", "wild": "#111111"}
        LABELS = {"skip": "S", "reverse": "R", "draw2": "+2", "wild": "W", "draw4": "+4"}

        def __init__(self, color, value, img_path=""):
            self.color = color
            self.value = value
            self.img = img_path

        def has_image(self):
            return bool(self.img) and renpy.loadable(self.img)

        def bg(self, dim=False):
            return (self.BG_DIM if dim else self.BG).get(self.color, "#333")

        def label(self):
            return str(self.value) if isinstance(self.value, int) else self.LABELS.get(self.value, "?")

        def matches(self, top, cur_color):
            if self.color == "wild": return True
            if self.color == cur_color: return True
            if self.value == top.value: return True
            return False

    class UnoGame(python_object):
        COLOR_CN = {"red": "红", "blue": "蓝", "green": "绿", "yellow": "黄"}
        COLOR_HEX = {"red": "#CC3333", "blue": "#2266CC", "green": "#22AA44", "yellow": "#CC9900"}

        def __init__(self, player_names, personalities):
            self.players = player_names
            self.personalities = personalities
            self.n = len(player_names)
            self.hands = [[] for _ in range(self.n)]
            self.draw_pile = []
            self.discard = []
            self.cur = 0
            self.direction = 1
            self.cur_color = None
            self.game_over = False
            self.winner = -1
            self.choosing_color = False
            self.played_by = 0
            self.drawn_playable = False
            self.msg = ""
            self.turn_count = 0
            self._build()
            self._deal()
            self._flip_first()

        def _img(self, color, value, variant=1):
            cf = _UNO_COLOR_FILE.get(color, "")
            candidates = []
            if isinstance(value, int):
                candidates = [
                    "images/uno/{}- {}.png".format(cf, value),
                    "images/uno/{}-{}.png".format(cf, value),
                ]
            elif value == "skip":
                candidates = [
                    "images/uno/{} Skip- {}.png".format(cf, variant),
                    "images/uno/{} Skip-{}.png".format(cf, variant),
                    "images/uno/{} Skip- 1.png".format(cf),
                    "images/uno/{} Skip-1.png".format(cf),
                ]
            elif value == "reverse":
                candidates = [
                    "images/uno/{} Reverse- {}.png".format(cf, variant),
                    "images/uno/{} Reverse-{}.png".format(cf, variant),
                    "images/uno/{} Reverse- 1.png".format(cf),
                    "images/uno/{} Reverse-1.png".format(cf),
                ]
            elif value == "draw2":
                candidates = [
                    "images/uno/{} Draw2- {}.png".format(cf, variant),
                    "images/uno/{} Draw2-{}.png".format(cf, variant),
                    "images/uno/{} Draw2- 1.png".format(cf),
                    "images/uno/{} Draw2-1.png".format(cf),
                ]
            elif value == "wild":
                candidates = [
                    "images/uno/Wild-{}.png".format(variant),
                    "images/uno/Wild- {}.png".format(variant),
                    "images/uno/Wild-1.png",
                ]
            elif value == "draw4":
                candidates = [
                    "images/uno/Draw4- {}.png".format(variant),
                    "images/uno/Draw4-{}.png".format(variant),
                    "images/uno/Draw4- 1.png",
                    "images/uno/Draw4-1.png",
                ]
            for c in candidates:
                if renpy.loadable(c):
                    return c
            return candidates[0] if candidates else ""

        def _build(self):
            d = []
            for c in ["red", "blue", "green", "yellow"]:
                d.append(UnoCard(c, 0, self._img(c, 0)))
                for v in range(1, 10):
                    d.append(UnoCard(c, v, self._img(c, v)))
                    d.append(UnoCard(c, v, self._img(c, v)))
                for a in ["skip", "reverse", "draw2"]:
                    d.append(UnoCard(c, a, self._img(c, a, 1)))
                    d.append(UnoCard(c, a, self._img(c, a, 2)))
            for i in range(4):
                d.append(UnoCard("wild", "wild", self._img("wild", "wild", i+1)))
                d.append(UnoCard("wild", "draw4", self._img("wild", "draw4", i+1)))
            _uno_rng.shuffle(d)
            self.draw_pile = d

        def _deal(self):
            for _ in range(7):
                for i in range(self.n):
                    self.hands[i].append(self.draw_pile.pop())

        def _flip_first(self):
            card = self.draw_pile.pop()
            while card.color == "wild":
                self.draw_pile.insert(0, card)
                _uno_rng.shuffle(self.draw_pile)
                card = self.draw_pile.pop()
            self.discard.append(card)
            self.cur_color = card.color
            if card.value == "skip":
                self.cur = self._next()
            elif card.value == "reverse":
                self.direction *= -1
            elif card.value == "draw2":
                self._draw_cards(0, 2)
                self.cur = self._next()

        def _refill(self):
            if len(self.draw_pile) < 2:
                top = self.discard.pop()
                self.draw_pile.extend(self.discard)
                self.discard = [top]
                _uno_rng.shuffle(self.draw_pile)

        def _next(self, fr=None):
            if fr is None: fr = self.cur
            return (fr + self.direction) % self.n

        def _draw_cards(self, p, count):
            for _ in range(count):
                self._refill()
                if self.draw_pile:
                    self.hands[p].append(self.draw_pile.pop())

        def playable(self, p):
            top = self.discard[-1]
            return [i for i, c in enumerate(self.hands[p]) if c.matches(top, self.cur_color)]

        def play(self, p, ci, color=None):
            card = self.hands[p].pop(ci)
            self.discard.append(card)
            self.played_by = p
            self.drawn_playable = False
            if card.color == "wild" and color is None:
                self.choosing_color = True
                return
            if card.color == "wild":
                self.cur_color = color
            else:
                self.cur_color = card.color
            self._finalize(card, p)

        def set_color(self, color):
            self.cur_color = color
            self.choosing_color = False
            self._finalize(self.discard[-1], self.played_by)

        def _finalize(self, card, p):
            nxt = self._next()
            self.msg = ""
            if card.value == "skip":
                self.msg = self.players[nxt] + " 被跳过！"
                self.cur = nxt
            elif card.value == "reverse":
                self.direction *= -1
                self.msg = "方向反转！"
                if self.n == 2: self.cur = self._next()
            elif card.value == "draw2":
                self._draw_cards(nxt, 2)
                self.msg = self.players[nxt] + " +2！"
                self.cur = nxt
            elif card.value == "draw4":
                self._draw_cards(nxt, 4)
                self.msg = self.players[nxt] + " +4！"
                self.cur = nxt
            if len(self.hands[p]) == 1:
                self.msg = self.players[p] + " : UNO!"
            if not self.hands[p]:
                self.game_over = True
                self.winner = p
                renpy.restart_interaction()
                return
            self.cur = self._next()
            self.turn_count += 1
            renpy.restart_interaction()

        def human_draw(self):
            self._refill()
            if not self.draw_pile:
                self.cur = self._next()
                renpy.restart_interaction()
                return
            card = self.draw_pile.pop()
            self.hands[0].append(card)
            if card.matches(self.discard[-1], self.cur_color):
                self.drawn_playable = True
                self.msg = "可以出这张牌！"
            else:
                self.drawn_playable = False
                self.msg = ""
                self.cur = self._next()
            renpy.restart_interaction()

        def human_pass(self):
            self.drawn_playable = False
            self.msg = ""
            self.cur = self._next()
            self.turn_count += 1
            renpy.restart_interaction()

        def ai_play(self):
            if self.game_over or self.choosing_color or self.cur == 0:
                return
            p = self.cur
            plist = self.playable(p)
            if plist:
                ci = self._ai_pick(p, plist)
                card = self.hands[p][ci]
                self.msg = self.players[p] + " 出了一张牌"
                if card.color == "wild":
                    self.play(p, ci, self._ai_color(p))
                else:
                    self.play(p, ci)
            else:
                self._refill()
                if self.draw_pile:
                    card = self.draw_pile.pop()
                    self.hands[p].append(card)
                    if card.matches(self.discard[-1], self.cur_color):
                        ci = len(self.hands[p]) - 1
                        if card.color == "wild":
                            self.play(p, ci, self._ai_color(p))
                        else:
                            self.play(p, ci)
                        return
                self.msg = self.players[p] + " 摸了一张"
                self.cur = self._next()
                self.turn_count += 1
                renpy.restart_interaction()

        def _color_counts(self, p):
            cc = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
            for c in self.hands[p]:
                if c.color in cc: cc[c.color] += 1
            return cc

        def _ai_color(self, p):
            cc = self._color_counts(p)
            return max(cc, key=cc.get) if any(cc.values()) else "red"

        def _ai_pick(self, p, plist):
            hand = self.hands[p]
            cc = self._color_counts(p)
            nxt_sz = len(self.hands[self._next()])
            style = self.personalities[p]
            scored = []
            for ci in plist:
                card = hand[ci]
                s = 0.0
                if card.color in cc: s += cc[card.color] * 1.5
                if card.value == "draw4": s += 22
                elif card.value == "draw2": s += 16
                elif card.value == "skip": s += 12
                elif card.value == "reverse": s += 10
                elif card.value == "wild": s += 6
                elif isinstance(card.value, int): s += card.value * 0.5
                if nxt_sz <= 2 and card.value in ("skip", "draw2", "draw4"): s += 15
                if style == "aggressive" and card.value in ("draw2", "draw4", "skip"): s += 10
                elif style == "defensive" and isinstance(card.value, int): s += 5
                elif style == "color_control":
                    best = max(cc, key=cc.get)
                    if card.color == best: s += 8
                elif style == "optimal":
                    if len(hand) <= 3 and card.value in ("draw2", "draw4", "skip"): s += 20
                    if card.color == "wild" and len(hand) > 3: s -= 12
                s += _uno_rng.random() * 3
                scored.append((s, ci))
            scored.sort(reverse=True)
            return scored[0][1]


# ==============================================================================
# 入口
# ==============================================================================

label start_uno_game:
    m1 "来玩UNO吧。"
    menu:
        "3人":
            python:
                _uno_names = [persistent.playername, "若叶睦", "墨缇斯"]
                _uno_pers = ["human", "balanced", "aggressive"]
        "4人":
            python:
                _extra = ["若叶睦·过去的人格", "若叶睦·经纪人人格", "若叶睦·牌神人格"]
                _uno_rng.shuffle(_extra)
                _uno_names = [persistent.playername, "若叶睦", "墨缇斯", _extra[0]]
                _pmap = {"若叶睦·过去的人格": "defensive", "若叶睦·经纪人人格": "color_control", "若叶睦·牌神人格": "optimal"}
                _uno_pers = ["human", "balanced", "aggressive", _pmap[_extra[0]]]
        "5人":
            python:
                _extra = ["若叶睦·过去的人格", "若叶睦·经纪人人格", "若叶睦·牌神人格"]
                _uno_rng.shuffle(_extra)
                _uno_names = [persistent.playername, "若叶睦", "墨缇斯", _extra[0], _extra[1]]
                _pmap = {"若叶睦·过去的人格": "defensive", "若叶睦·经纪人人格": "color_control", "若叶睦·牌神人格": "optimal"}
                _uno_pers = ["human", "balanced", "aggressive", _pmap[_extra[0]], _pmap[_extra[1]]]
        "6人":
            python:
                _extra = ["若叶睦·过去的人格", "若叶睦·经纪人人格", "若叶睦·牌神人格"]
                _uno_rng.shuffle(_extra)
                _uno_names = [persistent.playername, "若叶睦", "墨缇斯", _extra[0], _extra[1], _extra[2]]
                _pmap = {"若叶睦·过去的人格": "defensive", "若叶睦·经纪人人格": "color_control", "若叶睦·牌神人格": "optimal"}
                _uno_pers = ["human", "balanced", "aggressive", _pmap[_extra[0]], _pmap[_extra[1]], _pmap[_extra[2]]]
    $ _uno = UnoGame(_uno_names, _uno_pers)
    call screen uno_screen(_uno)
    if _uno.winner == 0:
        $ add_hgd("若叶睦", 1.5, daily_id="uno_daily_win", max_daily=1)
    jump game_center_start


# ==============================================================================
# 单张卡牌渲染（图片优先，fallback用色块）
# ==============================================================================

screen uno_card_display(card, w, h, dimmed=False):
    fixed:
        xsize w ysize h
        if card.has_image():
            if dimmed:
                add Transform(card.img, size=(w, h)) alpha 0.35
            else:
                add Transform(card.img, size=(w, h))
        else:
            # fallback: 色块+白色内芯+文字
            $ _fbg = card.bg(dim=dimmed)
            $ _fl = card.label()
            frame:
                xfill True yfill True
                background Solid(_fbg)
                padding (3, 3)
                frame:
                    align (0.5, 0.5)
                    xsize (w - 14) ysize (h - 14)
                    background Solid("#ffffffcc" if not dimmed else "#ffffff44")
                    padding (0, 0)
                    text "[_fl]" align (0.5, 0.5) size (h // 3) color _fbg bold True font "DejaVuSans.ttf"


# ==============================================================================
# 游戏画面
# ==============================================================================

screen uno_screen(ug):
    modal True
    zorder 200

    # ★ 修复：repeat True 防止AI卡住 ★
    if not ug.game_over and ug.cur != 0 and not ug.choosing_color:
        timer 1.0 action Function(ug.ai_play) repeat True

    $ _my_turn = (ug.cur == 0 and not ug.game_over and not ug.choosing_color)
    $ _my_playable = ug.playable(0) if _my_turn else []
    $ _dp_count = len(ug.draw_pile)
    $ _my_count = len(ug.hands[0])
    $ _dir_sym = "→" if ug.direction == 1 else "←"
    $ _top = ug.discard[-1] if ug.discard else None
    $ _top_bg = _top.bg() if _top else "#333"
    $ _cc_hex = ug.COLOR_HEX.get(ug.cur_color, "#333")
    $ _cur_cn = ug.COLOR_CN.get(ug.cur_color, "?")

    python:
        _opp_count = ug.n - 1
        if _opp_count == 2:
            _opp_positions = [(340, 20), (780, 20)]
        elif _opp_count == 3:
            _opp_positions = [(80, 100), (480, 15), (880, 100)]
        elif _opp_count == 4:
            _opp_positions = [(60, 110), (320, 15), (640, 15), (950, 110)]
        elif _opp_count == 5:
            _opp_positions = [(40, 130), (250, 15), (490, 15), (730, 15), (970, 130)]
        else:
            _opp_positions = [(500, 20)]

    # ======== 背景 ========
    add Solid("#0b3318")
    # 桌面
    add Solid("#093015") xpos 140 ypos 100 xsize 1000 ysize 420

    # ======== 对手 ========
    for _oi in range(_opp_count):
        $ _pi = _oi + 1
        $ _oname = ug.players[_pi]
        $ _ocount = len(ug.hands[_pi])
        $ _oactive = (ug.cur == _pi)
        $ _ox, _oy = _opp_positions[_oi] if _oi < len(_opp_positions) else (400, 20)
        $ _obg = "#1a6a2aee" if _oactive else "#0d1a10cc"
        $ _name_colors = ["#CC3333", "#2266CC", "#22AA44", "#CC9900", "#9944CC"]
        $ _nc = _name_colors[_oi % 5]
        # 头像取"若叶睦·"后面的第一个字，如果没有·就取第一个字
        $ _initial = _oname.split("·")[-1][0] if "·" in _oname else (_oname[0] if _oname else "?")
        # 显示名：如果有·取后半部分
        $ _display_name = _oname.split("·")[-1] if "·" in _oname else _oname

        frame:
            xpos _ox ypos _oy
            xsize 200 ysize 82
            background Solid(_obg)
            padding (10, 8)

            hbox:
                spacing 8 yalign 0.5

                frame:
                    xsize 30 ysize 30
                    background Solid(_nc)
                    text "[_initial]" align (0.5, 0.5) size 15 color "#ffffff" bold True

                vbox:
                    spacing 3
                    hbox:
                        spacing 6
                        text "[_display_name]" size 13 color "#ffffff" bold _oactive
                        if _ocount == 1:
                            text "UNO!" size 11 color "#ff4444" bold True yalign 0.5
                        else:
                            text "[_ocount]张" size 11 color "#ffffffaa" yalign 0.5
                    hbox:
                        spacing 1
                        for _bi in range(min(_ocount, 14)):
                            add Solid("#ffffff33") xsize 8 ysize 12

        # 活跃光条
        if _oactive:
            add Solid("#95e1d3") xpos _ox ypos (_oy + 82) xsize 200 ysize 3

    # ======== 中央弃牌 ========
    if _top:
        frame:
            xalign 0.5 yalign 0.43
            xsize 94 ysize 148
            background Solid("#ffffff22")
            padding (3, 3)
            use uno_card_display(_top, 88, 142)

    # 万能牌颜色提示
    if _top and _top.color == "wild":
        frame:
            xalign 0.5 yalign 0.56
            background Solid(_cc_hex)
            padding (12, 4)
            text "[_cur_cn]" size 14 color "#ffffff" bold True

    # 颜色指示
    frame:
        xalign 0.36 yalign 0.36
        background Solid(_cc_hex)
        padding (8, 6)
        hbox:
            spacing 6
            text "当前" size 11 color "#ffffffaa" yalign 0.5
            text "[_cur_cn]" size 16 color "#ffffff" bold True yalign 0.5

    # 方向
    frame:
        xalign 0.5 yalign 0.27
        background Solid("#00000066")
        padding (16, 5)
        hbox:
            spacing 12
            text "[_dir_sym]" size 18 color "#ffffffaa"
            text "回合 [ug.turn_count]" size 12 color "#ffffff55" yalign 0.5

    # 摸牌堆
    if _my_turn and not ug.drawn_playable:
        button:
            xalign 0.64 yalign 0.43
            xsize 72 ysize 105
            background Solid("#1a4a2a")
            hover_background Solid("#2a6a3a")
            action Function(ug.human_draw)
            vbox:
                align (0.5, 0.5) spacing 4
                text "摸牌" size 14 color "#ffffff" xalign 0.5 bold True
                text "[_dp_count]" size 12 color "#ffffffaa" xalign 0.5 font "DejaVuSans.ttf"
    else:
        frame:
            xalign 0.64 yalign 0.43
            xsize 72 ysize 105
            background Solid("#0d2a14")
            padding (4, 4)
            vbox:
                align (0.5, 0.5) spacing 4
                text "牌堆" size 12 color "#5a8a6a" xalign 0.5
                text "[_dp_count]" size 11 color "#ffffff55" xalign 0.5 font "DejaVuSans.ttf"

    # ======== 消息 ========
    if ug.msg:
        frame:
            xalign 0.5 yalign 0.60
            background Solid("#000000bb")
            padding (24, 8)
            text "[ug.msg]" size 16 color "#ffd700" bold True

    # ======== 回合提示 + 跳过 ========
    frame:
        xalign 0.5 ypos 498
        background None
        padding (0, 0)
        hbox:
            spacing 20
            if _my_turn:
                text "你的回合" size 14 color "#95e1d3" yalign 0.5 bold True
            elif ug.cur != 0 and not ug.game_over:
                $ _cn = ug.players[ug.cur]
                text "[_cn] 的回合..." size 14 color "#ffffff88" yalign 0.5
            if ug.drawn_playable and ug.cur == 0:
                textbutton "跳过" action Function(ug.human_pass) text_size 14 text_color "#ff6666" text_hover_color "#ff8888" yalign 0.5

    # ======== 玩家手牌 ========
    frame:
        ypos 528 xfill True ysize 150
        background Solid("#071a0cee")
        padding (0, 0)

        # 名牌
        $ _pname = ug.players[0]
        $ _pn_bg = "#1a5a2a" if _my_turn else "#0d1a10"
        frame:
            xpos 8 ypos 8
            background Solid(_pn_bg)
            padding (8, 6)
            hbox:
                spacing 6
                frame:
                    xsize 28 ysize 28
                    background Solid("#ffd700")
                    text "P" align (0.5, 0.5) size 16 color "#000" bold True font "DejaVuSans.ttf"
                vbox:
                    spacing 1
                    text "[_pname]" size 11 color "#ffffff"
                    text "[_my_count] 张" size 9 color "#ffffffaa"

        # 手牌
        viewport:
            xpos 140 xsize 1000 ypos 5 ysize 140
            scrollbars None mousewheel "horizontal"

            hbox:
                spacing 4 yalign 0.5

                for _ci in range(_my_count):
                    $ _card = ug.hands[0][_ci]
                    $ _can = (_ci in _my_playable)
                    $ _ch = 104 if _can else 90

                    button:
                        xsize 62 ysize (110 if _can else 96)
                        yalign (0.0 if _can else 0.5)
                        background None
                        hover_background Solid("#ffffff22")
                        action Function(ug.play, 0, _ci)
                        sensitive _can
                        use uno_card_display(_card, 58, _ch, dimmed=(not _can))

    # 退出
    textbutton "退出" xalign 0.99 yalign 0.99 text_size 12 text_color "#ffffff44" text_hover_color "#ff6666" action Return()

    # ======== 选色 ========
    if ug.choosing_color and ug.played_by == 0:
        add Solid("#000000cc")
        frame:
            align (0.5, 0.42)
            xsize 380 ysize 200
            background Solid("#151f1af5")
            padding (24, 20)
            vbox:
                spacing 20 xfill True
                text "选择颜色" size 22 color "#ffffff" xalign 0.5 bold True
                hbox:
                    xalign 0.5 spacing 16
                    for _sc, _sh in [("red", "#CC3333"), ("blue", "#2266CC"), ("green", "#22AA44"), ("yellow", "#CC9900")]:
                        $ _scn = ug.COLOR_CN.get(_sc, "?")
                        button:
                            xsize 64 ysize 64
                            background Solid(_sh)
                            hover_background Solid("#ffffff44")
                            action Function(ug.set_color, _sc)
                            text "[_scn]" align (0.5, 0.5) size 24 color "#ffffff" bold True

    if ug.choosing_color and ug.played_by != 0:
        timer 0.5 action Function(ug.set_color, ug._ai_color(ug.played_by))

    # ======== 结束 ========
    if ug.game_over:
        add Solid("#000000cc")
        frame:
            align (0.5, 0.42)
            xsize 400 ysize 240
            background Solid("#151f1af5")
            padding (30, 25)
            vbox:
                align (0.5, 0.5) spacing 14 xfill True
                if ug.winner == 0:
                    add Solid("#ffd700") xsize 80 ysize 3 xalign 0.5
                    text "你赢了！" size 28 color "#ffd700" xalign 0.5 bold True
                    text "UNO!!!" size 18 color "#ff6644" xalign 0.5
                else:
                    add Solid("#95e1d3") xsize 60 ysize 3 xalign 0.5
                    $ _wn = ug.players[ug.winner]
                    text "[_wn] 获胜" size 24 color "#95e1d3" xalign 0.5 bold True
                    text "下次会赢的……大概。" size 13 color "#ffffff88" xalign 0.5
                text "共 [ug.turn_count] 回合" size 12 color "#ffffff55" xalign 0.5
                null height 2
                add Solid("#ffffff11") xsize 200 ysize 1 xalign 0.5
                button:
                    action Return()
                    xalign 0.5 xsize 150 ysize 40
                    background Solid("#95e1d322")
                    hover_background Solid("#95e1d344")
                    text "返回" align (0.5, 0.5) size 16 color "#95e1d3"
