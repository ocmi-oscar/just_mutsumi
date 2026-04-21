# ==============================================================================
# 🧩 小睦华容道 — Mutsumi Sliding Puzzle
#
# 支持 3x3 (8-puzzle) / 4x4 (15-puzzle) / 5x5 (24-puzzle)
# 开发者面板：AI自动求解(3x3/4x4)、一键通关、重置
# ==============================================================================

init python:
    import random as _sp_random
    import time as _sp_time

    class SlidingPuzzle(python_object):

        def __init__(self, size, shuffle_moves, time_limit=0):
            self.size = size
            self.total = size * size
            self.board = list(range(1, self.total)) + [0]
            self.goal = list(self.board)
            self.step_count = 0
            self.time_limit = time_limit
            self.shuffle_amount = shuffle_moves
            self.started = False
            self.start_time = 0.0
            self.won = False
            self.game_over = False

            self.dev_open = False
            self.auto_solving = False
            self.solution_moves = []
            self.solution_idx = 0

            self._shuffle(shuffle_moves)

        def _find_empty(self, board=None):
            b = board if board is not None else self.board
            return b.index(0)

        def _get_neighbors(self, pos):
            r, c = pos // self.size, pos % self.size
            nb = []
            if r > 0: nb.append(pos - self.size)
            if r < self.size - 1: nb.append(pos + self.size)
            if c > 0: nb.append(pos - 1)
            if c < self.size - 1: nb.append(pos + 1)
            return nb

        def _shuffle(self, moves):
            for _ in range(moves):
                empty = self._find_empty()
                nb = self._get_neighbors(empty)
                swap = _sp_random.choice(nb)
                self.board[empty], self.board[swap] = self.board[swap], self.board[empty]
            if self.board == self.goal:
                self._shuffle(moves)

        def tap(self, idx):
            if self.won or self.game_over or self.auto_solving:
                return
            empty = self._find_empty()
            if idx not in self._get_neighbors(empty):
                return
            if not self.started:
                self.started = True
                self.start_time = _sp_time.time()
            self.board[empty], self.board[idx] = self.board[idx], self.board[empty]
            self.step_count += 1
            if self.board == self.goal:
                self.won = True
                self.game_over = True
            renpy.restart_interaction()

        def get_remaining(self):
            if self.time_limit <= 0:
                return 9999
            if not self.started:
                return self.time_limit
            return max(0, self.time_limit - (_sp_time.time() - self.start_time))

        def get_elapsed(self):
            if not self.started:
                return 0
            return _sp_time.time() - self.start_time

        def check_timeout(self):
            if self.time_limit > 0 and self.started and not self.game_over:
                if self.get_remaining() <= 0:
                    self.game_over = True
                    self.won = False
                    renpy.restart_interaction()

        def get_tile_color(self, val):
            if val == 0:
                return "#0a0f0c"
            hue_step = 360.0 / (self.total - 1)
            h = (val - 1) * hue_step
            if h < 60:
                return "#1e3a2a"
            elif h < 120:
                return "#1e2e3a"
            elif h < 180:
                return "#2e1e3a"
            elif h < 240:
                return "#3a2e1e"
            elif h < 300:
                return "#1e3a34"
            else:
                return "#2a1e3a"

        def get_text_color(self, val):
            if val == 0:
                return "#000000"
            hue_step = 360.0 / (self.total - 1)
            h = (val - 1) * hue_step
            if h < 60:
                return "#95e1d3"
            elif h < 120:
                return "#6ab8d8"
            elif h < 180:
                return "#b8a0ff"
            elif h < 240:
                return "#d8a06a"
            elif h < 300:
                return "#6ad8b8"
            else:
                return "#d86aaa"

        # ── 开发者工具 ──

        def reset(self):
            self.board = list(self.goal)
            self._shuffle(self.shuffle_amount)
            self.step_count = 0
            self.started = False
            self.start_time = 0.0
            self.won = False
            self.game_over = False
            self.auto_solving = False
            self.solution_moves = []
            self.solution_idx = 0
            renpy.restart_interaction()

        def instant_win(self):
            self.board = list(self.goal)
            self.won = True
            self.game_over = True
            if not self.started:
                self.started = True
                self.start_time = _sp_time.time()
            renpy.restart_interaction()

        def start_auto_solve(self):
            path = self._solve_ida_star()
            if path is not None:
                self.solution_moves = path
                self.solution_idx = 0
                self.auto_solving = True
                if not self.started:
                    self.started = True
                    self.start_time = _sp_time.time()
                renpy.restart_interaction()

        def auto_step(self):
            if not self.auto_solving:
                return
            if self.solution_idx < len(self.solution_moves):
                idx = self.solution_moves[self.solution_idx]
                empty = self._find_empty()
                if idx in self._get_neighbors(empty):
                    self.board[empty], self.board[idx] = self.board[idx], self.board[empty]
                    self.step_count += 1
                self.solution_idx += 1
                if self.board == self.goal:
                    self.won = True
                    self.game_over = True
                    self.auto_solving = False
                renpy.restart_interaction()
            else:
                self.auto_solving = False
                renpy.restart_interaction()

        # ── IDA* 求解 (支持 3x3 和 4x4) ──

        def _manhattan(self, board):
            dist = 0
            sz = self.size
            for i, v in enumerate(board):
                if v == 0:
                    continue
                tr, tc = (v - 1) // sz, (v - 1) % sz
                cr, cc = i // sz, i % sz
                dist += abs(tr - cr) + abs(tc - cc)
            return dist

        def _solve_ida_star(self):
            start = tuple(self.board)
            goal = tuple(self.goal)
            if start == goal:
                return []

            sz = self.size
            limit = self._manhattan(start)
            max_iterations = 500000 if self.size <= 3 else 2000000

            while limit <= (80 if self.size <= 3 else 200):
                counter = [0]
                result = self._ida_search(start, goal, 0, limit, [], -1, sz, counter, max_iterations)
                if isinstance(result, list):
                    return result
                if result == float('inf'):
                    return None
                limit = result

            return None

        def _ida_search(self, state, goal, g, limit, path, last_move, sz, counter, max_iter):
            h = self._manhattan(state)
            f = g + h
            if f > limit:
                return f
            if state == goal:
                return path
            counter[0] += 1
            if counter[0] > max_iter:
                return float('inf')

            empty = state.index(0)
            er, ec = empty // sz, empty % sz
            min_t = float('inf')

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = er + dr, ec + dc
                if 0 <= nr < sz and 0 <= nc < sz:
                    ni = nr * sz + nc
                    if ni == last_move:
                        continue
                    ns = list(state)
                    ns[empty], ns[ni] = ns[ni], ns[empty]
                    ns_t = tuple(ns)
                    result = self._ida_search(ns_t, goal, g + 1, limit, path + [ni], empty, sz, counter, max_iter)
                    if isinstance(result, list):
                        return result
                    if result < min_t:
                        min_t = result

            return min_t

    def sliding_puzzle_reward(sp):
        if sp.won:
            if sp.size == 3:
                add_hgd("若叶睦", 0.5, daily_id="slide_daily_easy", max_daily=1)
            elif sp.size == 4:
                add_hgd("若叶睦", 1.0, daily_id="slide_daily_normal", max_daily=1)
            elif sp.size == 5:
                add_hgd("若叶睦", 1.5, daily_id="slide_daily_hard", max_daily=1)


# ==============================================================================
# 入口
# ==============================================================================

label start_sliding_puzzle:
    m1 "……把碎片，拼回原来的样子。"
    menu:
        "简单 (3x3 · 8块)":
            $ _sp_game = SlidingPuzzle(3, 25)
        "普通 (4x4 · 15块)":
            $ _sp_game = SlidingPuzzle(4, 60)
        "困难 (5x5 · 24块 · 限时300秒)":
            $ _sp_game = SlidingPuzzle(5, 120, 300)
    call screen sliding_puzzle_screen(_sp_game)
    python:
        sliding_puzzle_reward(_sp_game)
    jump game_center_start


# ==============================================================================
# 游戏画面
# ==============================================================================

screen sliding_puzzle_screen(sp):
    modal True
    zorder 200

    timer 1.0 action Function(sp.check_timeout) repeat True

    if sp.auto_solving:
        timer 0.25 action Function(sp.auto_step) repeat True

    add Solid("#0a0f0c")

    # 动态计算卡牌尺寸
    $ _sp_sz = sp.size
    $ _sp_gap = 6 if _sp_sz <= 3 else (4 if _sp_sz == 4 else 3)
    $ _sp_area = 420 if _sp_sz <= 3 else (440 if _sp_sz == 4 else 460)
    $ _sp_tile = (_sp_area - _sp_gap * (_sp_sz + 1)) // _sp_sz
    $ _sp_grid = _sp_sz * (_sp_tile + _sp_gap) - _sp_gap
    $ _sp_font = 36 if _sp_sz <= 3 else (26 if _sp_sz == 4 else 20)

    # ======== 顶部 ========
    frame:
        xfill True ysize 80
        background Solid("#111a14")
        padding (30, 12)

        hbox:
            xfill True yalign 0.5

            vbox:
                spacing 2
                text "小睦华容道" size 18 color "#95e1d3" bold True
                text "[_sp_sz]x[_sp_sz] Puzzle" size 10 color "#5a8a6a"

            vbox:
                xalign 0.5 spacing 2
                if sp.time_limit > 0:
                    $ _sp_rem = int(sp.get_remaining())
                    $ _sp_m = _sp_rem // 60
                    $ _sp_s = _sp_rem % 60
                    if _sp_rem <= 20 and sp.started:
                        text "[_sp_m]:[_sp_s:02d]" size 24 color "#ff6666" xalign 0.5 font "DejaVuSans.ttf"
                    else:
                        text "[_sp_m]:[_sp_s:02d]" size 24 color "#95e1d3" xalign 0.5 font "DejaVuSans.ttf"
                    text "剩余时间" size 9 color "#5a8a6a" xalign 0.5
                else:
                    $ _sp_el = int(sp.get_elapsed())
                    text "[_sp_el]s" size 24 color "#95e1d3" xalign 0.5 font "DejaVuSans.ttf"
                    text "已用时" size 9 color "#5a8a6a" xalign 0.5

            vbox:
                xalign 1.0 spacing 2
                text "[sp.step_count] 步" size 16 color "#ffffffaa" xalign 1.0
                if sp.auto_solving:
                    text "AI 求解中..." size 10 color "#b8a0ff" xalign 1.0

    # ======== 参考图（只在3x3和4x4时显示）========
    if _sp_sz <= 4:
        frame:
            xalign 0.88 yalign 0.28
            background Solid("#111a14")
            padding (6, 6)
            vbox:
                spacing 3
                text "目标" size 9 color "#5a8a6a" xalign 0.5
                $ _ref_ts = 18 if _sp_sz <= 3 else 14
                grid _sp_sz _sp_sz:
                    spacing 1
                    for _ri in range(sp.total):
                        $ _rv = sp.goal[_ri]
                        frame:
                            xsize _ref_ts ysize _ref_ts
                            if _rv == 0:
                                background Solid("#0a0f0c")
                            else:
                                background Solid("#1a2e1f")
                            if _rv > 0:
                                text "[_rv]" align (0.5, 0.5) size 8 color "#95e1d3" font "DejaVuSans.ttf"

    # ======== 主棋盘 ========
    frame:
        xalign 0.45 yalign 0.55
        xsize (_sp_grid + 36) ysize (_sp_grid + 36)
        background Solid("#111a14")
        padding (18, 18)

        grid _sp_sz _sp_sz:
            spacing _sp_gap
            xalign 0.5 yalign 0.5

            for _si in range(sp.total):
                $ _sv = sp.board[_si]
                if _sv == 0:
                    frame:
                        xsize _sp_tile ysize _sp_tile
                        background Solid("#0a0f0c")
                else:
                    $ _sc = sp.get_tile_color(_sv)
                    $ _stc = sp.get_text_color(_sv)
                    $ _correct = (_sv == sp.goal[_si])
                    button:
                        xsize _sp_tile ysize _sp_tile
                        if _correct and not sp.won:
                            background Solid("#1a3a1a")
                        else:
                            background Solid(_sc)
                        hover_background Solid("#2a4a2f")
                        action Function(sp.tap, _si)
                        sensitive (not sp.auto_solving)
                        text "[_sv]" align (0.5, 0.5) size _sp_font color _stc bold True font "DejaVuSans.ttf"

    # ======== DEV ========
    textbutton "DEV":
        xalign 0.98 yalign 0.12
        text_size 11 text_color "#ffffff33" text_hover_color "#b8a0ff"
        action ToggleField(sp, "dev_open")

    if sp.dev_open:
        frame:
            xalign 0.98 yalign 0.25
            xsize 180
            background Solid("#1a1a2eee")
            padding (12, 12)

            vbox:
                spacing 8
                xfill True

                text "开发者工具" size 12 color "#b8a0ff" bold True xalign 0.5
                add Solid("#ffffff11") xsize 156 ysize 1

                textbutton "AI 自动求解":
                    action Function(sp.start_auto_solve)
                    text_size 13 text_color "#95e1d3" text_hover_color "#b8f0d8"
                    xalign 0.5
                    sensitive (not sp.auto_solving and not sp.game_over)

                if _sp_sz >= 5:
                    text "5x5求解可能较慢" size 9 color "#ffffff33" xalign 0.5

                textbutton "一键通关":
                    action Function(sp.instant_win)
                    text_size 13 text_color "#ffd700" text_hover_color "#ffee88"
                    xalign 0.5
                    sensitive (not sp.game_over)

                textbutton "重置棋盘":
                    action Function(sp.reset)
                    text_size 13 text_color "#6ab8d8" text_hover_color "#8ad8f0"
                    xalign 0.5

    # ======== 底部 ========
    frame:
        xfill True ysize 50
        yalign 1.0
        background Solid("#0a0f0c")
        padding (40, 10)

        hbox:
            xfill True yalign 0.5

            if not sp.started:
                text "点击数字方块开始" size 12 color "#5a8a6a" yalign 0.5
            elif sp.auto_solving:
                $ _sa_left = len(sp.solution_moves) - sp.solution_idx
                text "AI 还需 [_sa_left] 步..." size 12 color "#b8a0ff" yalign 0.5
            elif not sp.game_over:
                text "把数字排列到正确位置" size 12 color "#5a8a6a" yalign 0.5

            textbutton "退出":
                action Return()
                text_size 14 text_color "#5a8a6a" text_hover_color "#ff6666"
                xalign 1.0 yalign 0.5

    # ======== 胜利/失败弹窗 ========
    if sp.game_over and not sp.auto_solving:
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

                add Solid("#95e1d3" if sp.won else "#ff6666") xsize 60 ysize 3 xalign 0.5

                if sp.won:
                    text "拼图完成" size 22 color "#95e1d3" xalign 0.5 bold True
                    $ _sp_t = int(sp.get_elapsed())
                    text "用时 [_sp_t] 秒 · [sp.step_count] 步" size 14 color "#ffffffaa" xalign 0.5
                    text "……碎片回到了原来的位置。" size 13 color "#95e1d3" xalign 0.5
                else:
                    text "时间到" size 22 color "#ff6666" xalign 0.5 bold True
                    text "完成了 [sp.step_count] 步" size 14 color "#ffffffaa" xalign 0.5
                    text "……时间不够了呢。" size 13 color "#5a8a6a" xalign 0.5

                null height 4
                add Solid("#ffffff11") xsize 200 ysize 1 xalign 0.5
                null height 4

                hbox:
                    xalign 0.5 spacing 20

                    button:
                        action Function(sp.reset)
                        xsize 120 ysize 38
                        background Solid("#6ab8d822")
                        hover_background Solid("#6ab8d844")
                        text "再来一局" align (0.5, 0.5) size 14 color "#6ab8d8"

                    button:
                        action Return()
                        xsize 120 ysize 38
                        background Solid("#95e1d322")
                        hover_background Solid("#95e1d344")
                        text "返回" align (0.5, 0.5) size 14 color "#95e1d3"
