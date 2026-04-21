init python:
    # --- 下落式音游配置 ---
    # 键位对应 (0-5 轨道)
    RHYTHM_KEY_MAP = ['s', 'd', 'f', 'j', 'k', 'l']
    
    # 轨道X坐标 (根据 1280x720 分辨率估算，可调整)
    LANE_X = [340, 440, 540, 740, 840, 940] 
    JUDGE_Y = 600  # 判定线 Y 坐标
    NOTE_SPEED = 12 # 音符下落速度 (像素/帧)
    
    class FallingNote:
        def __init__(self, lane, speed_mod=1.0):
            self.lane = lane # 轨道 0-5
            self.x = LANE_X[lane]
            self.y = -50     # 从屏幕上方生成
            self.speed = NOTE_SPEED * speed_mod
            self.is_hit = False
            self.is_miss = False
            # 对应的吉他音效 Key ("1"-"6")
            # 轨道0->6弦, 轨道5->1弦 (反向映射以符合吉他习惯: S是低音6弦, L是高音1弦)
            self.sound_key = str(6 - lane) 

    class FallingGameEngine:
        def __init__(self, difficulty):
            self.notes = []
            self.score = 0
            self.combo = 0
            self.hp = 100
            self.state = "playing" # playing, win, lose
            self.time_elapsed = 0
            
            # 难度配置
            diff_config = {
                "Easy":    {"spawn_rate": 60, "speed_mod": 0.8,  "win_score": 500},
                "Normal":  {"spawn_rate": 45, "speed_mod": 1.0,  "win_score": 1000},
                "Hard":    {"spawn_rate": 30, "speed_mod": 1.2,  "win_score": 1500},
                "Expert":  {"spawn_rate": 20, "speed_mod": 1.5,  "win_score": 2500},
                "Experts": {"spawn_rate": 10, "speed_mod": 1.8,  "win_score": 4000},
            }
            self.cfg = diff_config.get(difficulty, diff_config["Easy"])
            self.spawn_timer = 0
            self.game_duration = 30.0 # 游戏时长(秒)

        def update(self):
            if self.state != "playing": return

            self.time_elapsed += 0.02 # 假设 timer 0.02
            self.spawn_timer += 1

            # 1. 生成音符
            if self.spawn_timer >= self.cfg["spawn_rate"]:
                if self.time_elapsed < self.game_duration: # 时间到了就不生成了
                    lane = random.randint(0, 5)
                    self.notes.append(FallingNote(lane, self.cfg["speed_mod"]))
                    self.spawn_timer = 0
            
            # 2. 移动音符与Miss判定
            for note in self.notes[:]:
                if not note.is_hit:
                    note.y += note.speed
                    # 漏键判定 (超过屏幕下方)
                    if note.y > 750:
                        note.is_miss = True
                        self.combo = 0
                        self.hp -= 5
                        self.notes.remove(note)
                        renpy.restart_interaction()

            # 3. 胜利/失败判定
            if self.hp <= 0:
                self.state = "lose"
                renpy.checkpoint() # 触发一次交互以跳转
            elif self.time_elapsed >= self.game_duration + 3 and len(self.notes) == 0:
                # 时间到且屏幕无音符
                if self.score >= self.cfg["win_score"]:
                    self.state = "win"
                else:
                    self.state = "lose" # 分数不够也算输
                renpy.checkpoint()

        def input(self, lane_idx):
            if self.state != "playing": return
            
            # 寻找该轨道上最接近判定线的音符
            target_note = None
            min_dist = 1000
            
            for note in self.notes:
                if note.lane == lane_idx and not note.is_hit:
                    dist = abs(note.y - JUDGE_Y)
                    if dist < min_dist:
                        min_dist = dist
                        target_note = note
            
            # 判定命中
            if target_note and min_dist < 80: # 判定区间
                # 播放音效
                renpy.play(guitar_strings[target_note.sound_key])
                store.showing_note = target_note.sound_key # 触发琴弦震动动画
                
                # 移除音符
                self.notes.remove(target_note)
                
                # 评分
                if min_dist < 30:
                    self.score += 100
                    self.hp = min(100, self.hp + 2)
                    renpy.notify("PERFECT!") # 简单反馈
                else:
                    self.score += 50
                    self.hp = min(100, self.hp + 1)
                    renpy.notify("GOOD")
                
                self.combo += 1
            else:
                # 空挥惩罚 (可选)
                pass
            
            renpy.restart_interaction()

screen falling_rhythm_game(game):
    modal True
    zorder 2000
    
    # 背景遮罩
    add Solid("#000000e6")
    
    # --- 核心循环驱动 ---
    # 每 0.02 秒刷新一次逻辑 (50FPS)
    timer 0.02 repeat True action Function(game.update)
    
    # 状态自动跳转
    if game.state == "win":
        timer 1.0 action Return("win")
    elif game.state == "lose":
        timer 1.0 action Return("lose")

    # --- 游戏区域绘制 ---
    fixed:
        xsize 1280 ysize 720
        
        # 1. 绘制轨道线
        for x in LANE_X:
            add Solid("#ffffff33") xsize 2 ysize 720 xpos x+50 # +50是居中偏移
        
        # 2. 绘制判定线
        add Solid("#ff0000aa") xsize 700 ysize 4 xalign 0.5 ypos JUDGE_Y
        
        # 3. 绘制音符
        for note in game.notes:
            frame:
                xpos note.x
                ypos int(note.y)
                xsize 100 ysize 30
                # 不同轨道颜色略有不同
                if note.lane in [2, 3]: # 中间两轨
                    background Solid("#f1c40f") 
                else:
                    background Solid("#3498db") 
        
        # 4. 底部按键/点击区 (支持鼠标点击)
        for i in range(6):
            $ key_char = RHYTHM_KEY_MAP[i]
            $ x_pos = LANE_X[i]
            
            # 键盘监听
            key key_char action Function(game.input, i)
            
            # 鼠标/触摸按钮
            button:
                xpos x_pos ypos 620
                xsize 100 ysize 100
                background Frame(Solid("#ffffff22"), 4, 4)
                hover_background Frame(Solid("#ffffff66"), 4, 4)
                action Function(game.input, i)
                
                text key_char.upper() align (0.5, 0.5) size 40 color "#fff" bold True

    # --- HUD 信息显示 ---
    frame:
        background None
        xfill True
        padding (20, 20)
        
        hbox:
            spacing 50
            text "SCORE: [game.score]" size 36 color "#fff" outlines [(2, "#000")]
            text "COMBO: [game.combo]" size 36 color "#f1c40f" bold True outlines [(2, "#000")]
            
        # 血条
        vbox:
            align (1.0, 0.0)
            text "LIFE" xalign 1.0 size 20 color "#fff"
            bar:
                value game.hp range 100
                xsize 300 ysize 20
                right_bar Solid("#550000")
                left_bar Solid("#00ff00")

    # 退出按钮
    textbutton "退出":
        align (0.02, 0.98)
        action Return("quit")

# ==========================================
# 🎵 下落式音游入口与结算
# ==========================================

label guitar_falling_game_start:
    # 初始化游戏引擎
    $ falling_game = FallingGameEngine(selected_diff)
    
    # 呼叫屏幕，并等待返回结果
    call screen falling_rhythm_game(falling_game)
    $ result = _return
    
    if result == "quit":
        jump recovery_and_jump_sjdh
    
    # 结算逻辑
    python:
        # 每日奖励
        add_hgd("若叶睦", 1.0, daily_id="guitar_daily_play", max_daily=2)
        
        if result == "win":
            # 根据分数给予额外奖励（模拟）
            if falling_game.score > 2000:
                add_hgd("若叶睦", 1.0, daily_id="guitar_high_score", max_daily=1)

    window show
    if result == "win":
        m1 "……好厉害。"
        m1 "这样的手速……[player_name]以前玩过乐队吗？"
    else:
        m1 "……有点手忙脚乱呢。"
        m1 "如果是你的话，一定能做得更好。"
        
    window hide
    jump recovery_and_jump_sjdh