# ==========================================
# 🎮 小游戏集合逻辑 (已整合好感度系统)
# ==========================================
init python:
    import random

    # --------------------------------------------------------
    # 1. 扫雷逻辑
    # --------------------------------------------------------
    class SilentMessengerLogic(object):
        # 增加了 difficulty 参数来识别难度
        def __init__(self, rows=10, cols=10, stones=15, difficulty="normal"):
            self.rows, self.cols, self.total_stones = rows, cols, stones
            self.difficulty = difficulty # 记录难度
            self.cell_size = 45 if rows > 10 or cols > 10 else 60
            self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
            self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
            self.flags = [[False for _ in range(cols)] for _ in range(rows)]
            self.game_over = self.victory = False
            self.first_click = True 
            self.mutsumi_comment = "……这就是，土壤之下。" 
            self.quotes = {
                "start": ["……这就是，土壤之下。", "……小心。"],
                "mid": ["……还有很多。", "……稍微，有点期待。"],
                "near": ["……快要，看清了。", "……泥土的味道。"],
                "win": ["……所有的种子，都找到了。", "……嗯，收成不错。"],
                "lose": ["……啊。碰到了石头。", "……手，震得有点麻。"]
            }

        def place_stones(self, safe_r, safe_c):
            placed = 0
            while placed < self.total_stones:
                r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
                if (abs(r - safe_r) <= 1 and abs(c - safe_c) <= 1) or self.grid[r][c] == -1: continue
                self.grid[r][c] = -1
                placed += 1
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == -1: continue
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if self.grid[nr][nc] == -1: count += 1
                    self.grid[r][c] = count

        def reveal(self, r, c):
            if self.game_over or self.flags[r][c]: return
            if self.revealed[r][c]:
                if self.grid[r][c] > 0: self.perform_chording(r, c)
                return
            if self.first_click:
                self.place_stones(r, c)
                self.first_click = False
            self.reveal_cell(r, c)
            self.check_victory()
            renpy.restart_interaction()

        def perform_chording(self, r, c):
            target_num, flag_count, neighbors = self.grid[r][c], 0, []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
                        if self.flags[nr][nc]: flag_count += 1
            if flag_count == target_num:
                for nr, nc in neighbors:
                    if not self.flags[nr][nc] and not self.revealed[nr][nc]: self.reveal_cell(nr, nc)

        def reveal_cell(self, r, c):
            if self.revealed[r][c] or self.flags[r][c]: return
            self.revealed[r][c] = True
            if self.grid[r][c] == -1:
                self.game_over, self.victory = True, False
                self.mutsumi_comment = random.choice(self.quotes["lose"])
                return
            if self.grid[r][c] == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols: self.reveal_cell(nr, nc)

        def toggle_flag(self, r, c):
            if not self.revealed[r][c] and not self.game_over: self.flags[r][c] = not self.flags[r][c]
            renpy.restart_interaction()

        def check_victory(self):
            safe_cells = sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] != -1)
            revealed_safe = sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] != -1 and self.revealed[r][c])
            if revealed_safe == safe_cells:
                self.game_over, self.victory = True, True
                self.mutsumi_comment = random.choice(self.quotes["win"])

    # --------------------------------------------------------
    # 2. 五子棋逻辑
    # --------------------------------------------------------
    class MutsumiGomokuLogic(object):
        def __init__(self, size=13, difficulty="normal"):
            self.size = size
            self.difficulty = difficulty
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
            self.game_over = False
            self.winner = 0
            self.configs = {
                "easy": {"start": "……陪我，随便走走吗？", "win": "……啊，赢了。", "lose": "……很厉害。", "turn": "……该你了。"},
                "normal": {"start": "……专注一点。", "win": "……承让了。", "lose": "……精彩的对局。", "turn": "……你会，怎么走？"},
                "hard": {"start": "……我会，全力以赴。", "win": "……我看透了，所有的气。", "lose": "……是我，计算不够。", "turn": "……绝路。"}
            }
            self.mutsumi_comment = self.configs[difficulty]["start"]

        def place_stone(self, r, c):
            if self.grid[r][c] != 0 or self.game_over: return
            self.grid[r][c] = 1 
            if self.check_win(r, c, 1):
                self.game_over, self.winner = True, 1
                self.mutsumi_comment = self.configs[self.difficulty]["lose"]
            else:
                self.mutsumi_turn()
            renpy.restart_interaction()

        def check_win(self, r, c, p):
            for dr, dc in [(1,0), (0,1), (1,1), (1,-1)]:
                count = 1
                for i in [1, -1]:
                    nr, nc = r + dr*i, c + dc*i
                    while 0<=nr<self.size and 0<=nc<self.size and self.grid[nr][nc]==p:
                        count += 1
                        nr, nc = nr + dr*i, nc + dc*i
                if count >= 5: return True
            return False

        def get_line_pattern_score(self, r, c, dr, dc, p):
            line = []
            for i in range(-4, 5):
                nr, nc = r + dr*i, c + dc*i
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    line.append(self.grid[nr][nc])
                else:
                    line.append(-1)
            line[4] = p
            s = "".join(["X" if x == p else "O" if x == (3-p) else "_" if x == 0 else "B" for x in line])
            
            if "XXXXX" in s: return 1000000 
            if "_XXXX_" in s: return 100000
            if "_XXXXO" in s or "OXXXX_" in s or "XXX_X" in s or "X_XXX" in s or "XX_XX" in s: return 10000
            if "_XXX__" in s or "__XXX_" in s or "_X_XX_" in s or "_XX_X_" in s: return 15000
            if "XXX__" in s or "__XXX" in s or "OXXX__" in s: return 2000
            if "__XX__" in s or "_X_X_" in s: return 1000
            return 0

        def evaluate_point(self, r, c, p):
            score = 0
            for dr, dc in [(1,0), (0,1), (1,1), (1,-1)]:
                score += self.get_line_pattern_score(r, c, dr, dc, p)
            return score

        def mutsumi_turn(self):
            candidates = set()
            for r in range(self.size):
                for c in range(self.size):
                    if self.grid[r][c] != 0:
                        for dr in range(-2, 3):
                            for dc in range(-2, 3):
                                nr, nc = r+dr, c+dc
                                if 0<=nr<self.size and 0<=nc<self.size and self.grid[nr][nc] == 0:
                                    candidates.add((nr, nc))
            
            if not candidates: candidates.add((self.size//2, self.size//2))
            
            best_move = None
            max_score = -1e18 
            
            for r, c in candidates:
                atk = self.evaluate_point(r, c, 2)
                dfs = self.evaluate_point(r, c, 1)
                
                if self.difficulty == "hard":
                    current_score = atk + (dfs * 2.2) 
                elif self.difficulty == "normal":
                    current_score = atk + (dfs * 1.2)
                else:
                    current_score = atk + (dfs * 0.4) + random.randint(0, 500)
                
                dist = abs(r - self.size//2) + abs(c - self.size//2)
                current_score += (self.size - dist)

                if current_score > max_score:
                    max_score = current_score
                    best_move = (r, c)

            if best_move:
                r, c = best_move
                self.grid[r][c] = 2
                if self.check_win(r, c, 2):
                    self.game_over, self.winner = True, 2
                    self.mutsumi_comment = self.configs[self.difficulty]["win"]
                else:
                    self.mutsumi_comment = self.configs[self.difficulty]["turn"]

# ==========================================
# 🖥️ 界面系统 (修改了返回跳转)
# ==========================================

screen silent_messenger_game(logic):
    modal True
    tag game_screen
    add Solid("#1a1a1af2")
    
    $ total_cells = logic.rows * logic.cols
    $ revealed_count = sum(row.count(True) for row in logic.revealed)
    $ is_actually_win = (total_cells - revealed_count == logic.total_stones)
    $ is_actually_lose = logic.game_over and not logic.victory

    hbox:
        align (0.5, 0.45) spacing 50
        frame:
            background Frame(Solid("#2c3e50"), 10, 10) padding (15, 15)
            vbox:
                spacing 2
                for r in range(logic.rows):
                    hbox:
                        spacing 2
                        for c in range(logic.cols):
                            $ val, is_rev, is_flag = logic.grid[r][c], logic.revealed[r][c], logic.flags[r][c]
                            button:
                                xsize logic.cell_size ysize logic.cell_size
                                action If(not (is_actually_win or is_actually_lose), [Function(logic.reveal, r, c), renpy.restart_interaction])
                                alternate If(not (is_actually_win or is_actually_lose), [Function(logic.toggle_flag, r, c), renpy.restart_interaction])
                                
                                if is_rev:
                                    background Solid("#ecf0f1")
                                    if val == -1:
                                        text "🪨" size int(logic.cell_size*0.6) align (0.5, 0.5)
                                    elif val > 0:
                                        $ num_color = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6", "#f1c40f", "#1abc9c", "#34495e", "#000"][val-1]
                                        text str(val) size int(logic.cell_size*0.55) color num_color align (0.5, 0.5) bold True
                                elif is_flag:
                                    background Solid("#f1c40f")
                                    text "🌱" size int(logic.cell_size*0.6) align (0.5, 0.5)
                                else:
                                    background Solid("#4a4a4a") hover_background Solid("#666666")
        vbox:
            yalign 0.5 xsize 350 spacing 20
            frame:
                background Solid("#00000088") padding (20, 20) xfill True
                vbox:
                    text "睦：" size 26 color "#95e1d3" bold True
                    text "[logic.mutsumi_comment]" size 24 color "#fff"
            
            if not (is_actually_win or is_actually_lose):
                textbutton "放弃退出":
                    action Jump("game_center_start") 
                    background Solid("#c0392b") padding (10, 10) xfill True

    if is_actually_win or is_actually_lose:
        add Solid("#000000cc")
        frame:
            modal True align (0.5, 0.5) padding (60, 40) background Solid("#1a1a1ae6")
            vbox:
                spacing 30 xalign 0.5
                if is_actually_win:
                    text "所有的种子，都找到了。" color "#95e1d3" size 45 xalign 0.5
                else:
                    text "触碰到了岩石..." color "#ff4444" size 45 xalign 0.5
                
                textbutton "返回":
                    # --- 修改处：跳转到好感度结算 ---
                    action Jump("minesweeper_reward") 
                    background Solid("#2980b9") 
                    padding (20, 10) xalign 0.5 text_size 30

screen mutsumi_gomoku_game(logic):
    modal True
    tag game_screen
    add Solid("#1a1a1af2")
    hbox:
        align (0.5, 0.45) spacing 50
        frame:
            background Solid("#dcb35c") padding (10, 10)
            vbox:
                spacing 1
                for r in range(logic.size):
                    hbox:
                        spacing 1
                        for c in range(logic.size):
                            button:
                                xsize 45 ysize 45 background Solid("#00000022")
                                action Function(logic.place_stone, r, c)
                                if logic.grid[r][c] == 1:
                                    text "●" color "#ffffff" size 35 align (0.5, 0.5)
                                elif logic.grid[r][c] == 2:
                                    text "●" color "#000000" size 35 align (0.5, 0.5)
        vbox:
            yalign 0.5 xsize 350 spacing 20
            frame:
                background Solid("#00000088") padding (20, 20) xfill True
                vbox:
                    text ("睦 (%s)：" % logic.difficulty.upper()) size 22 color "#95e1d3"
                    text "[logic.mutsumi_comment]" size 24 color "#fff"
            textbutton "退出棋局":
                action Jump("game_center_start") background Solid("#c0392b") padding (10, 10)
    if logic.game_over:
        frame:
            modal True align (0.5, 0.5) padding (50, 50) background Solid("#000000f2")
            vbox:
                spacing 20 xalign 0.5
                text ("你赢了。" if logic.winner == 1 else "睦赢了。") color "#fff" size 40 xalign 0.5
                textbutton "返回":
                    # --- 修改处：跳转到好感度结算 ---
                    action Jump("gomoku_reward") 
                    background Solid("#2980b9") padding (15, 10) xalign 0.5

# ==========================================
# 🎬 跳转与好感度奖励逻辑
# ==========================================

label minesweeper_reward:
    python:
        # 1. 每日基础奖励 (胜1.0/负0.5，每日限一次)
        if m_logic.victory:
            add_hgd("若叶睦", 1.0, daily_id="ms_daily_limit", max_daily=1)
            # 2. 首次胜利挑战奖励 (永恒一次)
            if m_logic.difficulty == "easy":
                add_hgd("若叶睦", 0.5, once_id="ms_first_win_easy")
            elif m_logic.difficulty == "normal":
                add_hgd("若叶睦", 1.0, once_id="ms_first_win_normal")
            elif m_logic.difficulty == "hard":
                add_hgd("若叶睦", 1.5, once_id="ms_first_win_hard")
        else:
            add_hgd("若叶睦", 0.5, daily_id="ms_daily_limit", max_daily=1)
    jump game_center_start

label gomoku_reward:
    python:
        # 1. 每日基础奖励 (胜1.0/负0.5，每日限一次)
        if g_logic.winner == 1: # 玩家胜
            add_hgd("若叶睦", 1.0, daily_id="gomoku_daily_limit", max_daily=1)
            # 2. 首次胜利挑战奖励 (永恒一次)
            if g_logic.difficulty == "easy":
                add_hgd("若叶睦", 0.5, once_id="gomoku_first_win_easy")
            elif g_logic.difficulty == "normal":
                add_hgd("若叶睦", 1.0, once_id="gomoku_first_win_normal")
            elif g_logic.difficulty == "hard":
                add_hgd("若叶睦", 1.5, once_id="gomoku_first_win_hard")
        else: # 睦胜或平局
            add_hgd("若叶睦", 0.5, daily_id="gomoku_daily_limit", max_daily=1)
    jump game_center_start

label game_center_start:
    $ quick_menu = True
    show screen main_interaction_ui
    show screen phone_system
    $ store.phone_open = True
    $ store.phone_current_view = "games"
    jump sjdh








label start_silent_messenger_entry:
    # (旧菜单已移除)
    m1 "……要多大的土地？"
    menu:
        "小花盆 (6x6)":
            $ m_logic = SilentMessengerLogic(6, 6, 6, difficulty="easy")
        "家庭菜园 (10x8)":
            $ m_logic = SilentMessengerLogic(10, 8, 12, difficulty="normal")
        "睦的温室 (12x10)":
            $ m_logic = SilentMessengerLogic(12, 10, 22, difficulty="hard")
    call screen silent_messenger_game(m_logic)
    jump game_center_start

label start_gomoku_difficulty:
    # (旧菜单已移除)
    m1 "……你想看，什么状态的我？"
    menu:
        "随便下下 ":
            $ g_logic = MutsumiGomokuLogic(13, "easy")
        "专注 ":
            $ g_logic = MutsumiGomokuLogic(13, "normal")
        "全神贯注 ":
            $ g_logic = MutsumiGomokuLogic(13, "hard")
    call screen mutsumi_gomoku_game(g_logic)
    jump game_center_start

label recovery_from_game_center:
    $ quick_menu = True
    show screen main_interaction_ui
    show screen phone_system
    $ store.phone_open = True
    $ store.phone_current_view = "games"
    jump sjdh








# --- 菜单按钮样式 ---
