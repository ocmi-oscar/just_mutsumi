# ==============================================================================
# 🃏 翻牌记忆 — Memory Cards
#
# 玩法：翻开两张卡牌，找出相同的图案配对
# 素材：images/gacha_items/emote_mutsumi_1.png ~ emote_mutsumi_56.png
# 难度：简单(3x4) / 普通(4x4) / 困难(4x5)
# ==============================================================================

init python:
    import random as _mc_random
    import time as _mc_time

    class MemoryCardGame(python_object):
        """翻牌记忆游戏逻辑"""

        def __init__(self, rows, cols, time_limit):
            self.rows = rows
            self.cols = cols
            self.total = rows * cols
            self.pairs_needed = self.total // 2
            self.time_limit = time_limit

            # 随机选表情包
            emote_pool = list(range(1, 57))
            _mc_random.shuffle(emote_pool)
            chosen = emote_pool[:self.pairs_needed]

            # 每个ID出现两次，打乱
            deck = chosen * 2
            _mc_random.shuffle(deck)
            self.cards = deck

            # 状态
            self.revealed = [False] * self.total
            self.matched = [False] * self.total
            self.first = None
            self.second = None
            self.moves = 0
            self.pairs_found = 0
            self.checking = False
            self.game_over = False
            self.won = False
            self.started = False
            self.start_time = 0.0

        def flip(self, idx):
            """翻开一张牌"""
            if self.game_over or self.checking:
                return
            if self.revealed[idx] or self.matched[idx]:
                return

            # 首次翻牌开始计时
            if not self.started:
                self.started = True
                self.start_time = _mc_time.time()

            self.revealed[idx] = True

            if self.first is None:
                self.first = idx
            else:
                self.second = idx
                self.moves += 1

                if self.cards[self.first] == self.cards[self.second]:
                    # 配对成功
                    self.matched[self.first] = True
                    self.matched[self.second] = True
                    self.pairs_found += 1
                    self.first = None
                    self.second = None

                    if self.pairs_found >= self.pairs_needed:
                        self.won = True
                        self.game_over = True
                else:
                    # 不匹配，标记等待翻回
                    self.checking = True

            renpy.restart_interaction()

        def hide_mismatch(self):
            """翻回不匹配的两张牌"""
            if self.first is not None:
                self.revealed[self.first] = False
            if self.second is not None:
                self.revealed[self.second] = False
            self.first = None
            self.second = None
            self.checking = False
            renpy.restart_interaction()

        def get_remaining(self):
            """剩余时间"""
            if not self.started:
                return self.time_limit
            elapsed = _mc_time.time() - self.start_time
            return max(0, self.time_limit - elapsed)

        def check_timeout(self):
            """检查是否超时"""
            if self.started and not self.game_over and self.get_remaining() <= 0:
                self.game_over = True
                self.won = False
                renpy.restart_interaction()

        def get_card_image(self, idx):
            """获取卡牌图片路径"""
            emote_id = self.cards[idx]
            return "images/gacha_items/emote_mutsumi_{}.png".format(emote_id)

        def get_elapsed(self):
            """已用时间"""
            if not self.started:
                return 0
            if self.game_over:
                return self.time_limit - self.get_remaining()
            return _mc_time.time() - self.start_time

    # 好感度结算
    def memory_game_reward(mg):
        """根据难度给好感度奖励"""
        if mg.won:
            if mg.rows == 3 and mg.cols == 4:
                add_hgd("若叶睦", 0.5, daily_id="memory_daily_easy", max_daily=1)
            elif mg.rows == 4 and mg.cols == 5:
                add_hgd("若叶睦", 1.0, daily_id="memory_daily_normal", max_daily=1)
            elif mg.rows == 5 and mg.cols == 6:
                add_hgd("若叶睦", 1.5, daily_id="memory_daily_hard", max_daily=1)


# ==============================================================================
# 入口标签
# ==============================================================================

label start_memory_card_game:
    m1 "……来，试试看你的记忆。"
    menu:
        "小花盆 (3x4 · 6对 · 90秒)":
            $ _mc_game = MemoryCardGame(3, 4, 90)
        "家庭菜园 (4x5 · 10对 · 120秒)":
            $ _mc_game = MemoryCardGame(4, 5, 120)
        "睦的温室 (5x6 · 15对 · 150秒)":
            $ _mc_game = MemoryCardGame(5, 6, 150)
    call screen memory_card_screen(_mc_game)
    python:
        memory_game_reward(_mc_game)
    jump game_center_start


# ==============================================================================
# 游戏画面
# ==============================================================================

screen memory_card_screen(mg):
    modal True
    zorder 200

    # 每秒刷新（驱动计时器和超时检测）
    timer 1.0 action Function(mg.check_timeout) repeat True

    # 不匹配时0.8秒后翻回
    if mg.checking:
        timer 0.8 action Function(mg.hide_mismatch) repeat False

    # 深色背景
    add Solid("#0a0f0c")

    # 计算卡牌尺寸
    $ _mc_cols = mg.cols
    $ _mc_rows = mg.rows
    $ _mc_gap = 8
    # 根据行列数计算合适的卡牌大小
    $ _mc_max_w = (700 - _mc_gap * (_mc_cols + 1)) // _mc_cols
    $ _mc_max_h = (450 - _mc_gap * (_mc_rows + 1)) // _mc_rows
    $ _mc_card_size = min(_mc_max_w, _mc_max_h, 120)
    $ _mc_grid_w = _mc_cols * (_mc_card_size + _mc_gap) - _mc_gap
    $ _mc_grid_h = _mc_rows * (_mc_card_size + _mc_gap) - _mc_gap

    # ======== 顶部信息栏 ========
    frame:
        xfill True ysize 80
        background Solid("#111a14")
        padding (40, 15)

        hbox:
            xfill True yalign 0.5

            # 左：标题
            vbox:
                spacing 2
                text "翻牌记忆" size 20 color "#6ab8d8" bold True
                text "Memory Cards" size 10 color "#4a8aaa"

            # 中：计时
            vbox:
                xalign 0.5
                spacing 2
                $ _mc_rem = int(mg.get_remaining())
                $ _mc_min = _mc_rem // 60
                $ _mc_sec = _mc_rem % 60
                if _mc_rem <= 15 and mg.started:
                    text "[_mc_min]:[_mc_sec:02d]" size 28 color "#ff6666" xalign 0.5 font "DejaVuSans.ttf"
                else:
                    text "[_mc_min]:[_mc_sec:02d]" size 28 color "#95e1d3" xalign 0.5 font "DejaVuSans.ttf"
                text "剩余时间" size 9 color "#5a8a6a" xalign 0.5

            # 右：翻牌次数 + 配对数
            vbox:
                xalign 1.0
                spacing 2
                text "[mg.moves] 次翻牌" size 14 color "#ffffffaa" xalign 1.0
                text "[mg.pairs_found]/[mg.pairs_needed] 对" size 14 color "#95e1d3" xalign 1.0

    # ======== 卡牌网格 ========
    frame:
        xalign 0.5 yalign 0.55
        xsize (_mc_grid_w + 40) ysize (_mc_grid_h + 40)
        background Solid("#0d1210")
        padding (20, 20)

        grid _mc_cols _mc_rows:
            spacing _mc_gap
            xalign 0.5 yalign 0.5

            for _ci in range(mg.total):
                if mg.matched[_ci]:
                    # 已配对 — 显示图片 + 绿色边框效果
                    frame:
                        xsize _mc_card_size ysize _mc_card_size
                        background Solid("#1a3a2a")
                        padding (3, 3)
                        add Transform(mg.get_card_image(_ci), size=(_mc_card_size - 6, _mc_card_size - 6)) align (0.5, 0.5)
                elif mg.revealed[_ci]:
                    # 已翻开但未配对
                    frame:
                        xsize _mc_card_size ysize _mc_card_size
                        background Solid("#1a2a3a")
                        padding (3, 3)
                        add Transform(mg.get_card_image(_ci), size=(_mc_card_size - 6, _mc_card_size - 6)) align (0.5, 0.5)
                else:
                    # 未翻开 — 卡牌背面
                    button:
                        xsize _mc_card_size ysize _mc_card_size
                        background Solid("#1a2a20")
                        hover_background Solid("#2a3a30")
                        action Function(mg.flip, _ci)
                        text "?" align (0.5, 0.5) size (_mc_card_size // 3) color "#5a8a6a"

    # ======== 底部栏 ========
    frame:
        xfill True ysize 50
        yalign 1.0
        background Solid("#0a0f0c")
        padding (40, 10)

        hbox:
            xfill True yalign 0.5

            # 左：提示
            if not mg.started:
                text "翻开第一张牌开始计时" size 12 color "#5a8a6a" yalign 0.5
            elif not mg.game_over:
                text "找出所有配对的卡牌" size 12 color "#5a8a6a" yalign 0.5
            else:
                text "" yalign 0.5

            # 右：退出按钮
            textbutton "退出":
                action Return()
                text_size 14
                text_color "#5a8a6a"
                text_hover_color "#ff6666"
                xalign 1.0 yalign 0.5

    # ======== 游戏结束弹窗 ========
    if mg.game_over:
        # 遮罩
        add Solid("#000000cc")

        frame:
            align (0.5, 0.45)
            xsize 400 ysize 260
            background Solid("#151f1af2")
            padding (30, 25)

            vbox:
                align (0.5, 0.5)
                spacing 14
                xfill True

                add Solid("#6ab8d8" if mg.won else "#ff6666") xsize 60 ysize 3 xalign 0.5

                if mg.won:
                    text "记忆完成" size 22 color "#6ab8d8" xalign 0.5 bold True
                    $ _mc_elapsed = int(mg.get_elapsed())
                    text "用时 [_mc_elapsed] 秒 · [mg.moves] 次翻牌" size 14 color "#ffffffaa" xalign 0.5
                    text "……你记住了，每一个我的表情。" size 13 color "#95e1d3" xalign 0.5
                else:
                    text "时间到" size 22 color "#ff6666" xalign 0.5 bold True
                    text "找到了 [mg.pairs_found]/[mg.pairs_needed] 对" size 14 color "#ffffffaa" xalign 0.5
                    text "……再试一次吧。" size 13 color "#5a8a6a" xalign 0.5

                null height 4

                add Solid("#ffffff11") xsize 200 ysize 1 xalign 0.5

                null height 4

                hbox:
                    xalign 0.5
                    spacing 30
                    button:
                        action Return()
                        xsize 130 ysize 38
                        background Solid("#6ab8d822")
                        hover_background Solid("#6ab8d844")
                        text "返回" align (0.5, 0.5) size 15 color "#6ab8d8"
