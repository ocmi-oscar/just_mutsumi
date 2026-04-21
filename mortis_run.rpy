# ==========================================
# 🏃‍♀️ 跑酷游戏 - 最终完善版 (v4.1)
# - 修复音乐还原问题 (退出后自动播放之前的BGM)
# - 修改场景切换分数为 2500
# ==========================================

init python:
    import pygame 
    import random 
    import os 

    # 游戏配置
    class RunConfig:
        GRAVITY = 0.9
        JUMP_FORCE = -17
        SPEED_START = 10
        SPEED_MAX = 25
        GROUND_Y = 640
        PLAYER_X = 250
        JUMP_SPRITE_OFFSET = -10 

    class RunnerGame:
        def __init__(self):
            # 游戏状态
            self.playing = True
            self.score = 0
            self.cucumbers = 0
            self.speed = RunConfig.SPEED_START
            self.stage = 1
            self.transition_progress = 0.0
            
            # 玩家状态
            self.player_y = RunConfig.GROUND_Y
            self.player_vy = 0
            self.grounded = True
            
            # 游戏对象
            self.obstacles = []
            self.bg_offset = 0
            self.spawn_counter = 60
            
            # 动画控制 (frame_counter 用于计算固定帧率)
            self.current_anim = "run"
            self.frame_counter = 0
            self.is_ducking = False
            
            # 障碍物图片预加载
            self.obstacle_images = {
                'ground_1': 'images/minigame/run/obs_ground_1.png',
                'ground_2': 'images/minigame/run/obs_ground_2.png',
                'ground_3': 'images/minigame/run/obs_ground_3.png',
                'ground_4': 'images/minigame/run/obs_ground_4.png',
                'ground_5': 'images/minigame/run/obs_ground_5.png',
                'ground_6': 'images/minigame/run/obs_ground_6.png',
                'air_1': 'images/minigame/run/obs_air_1.png',
                'air_2': 'images/minigame/run/obs_air_1.png',
                'air_3': 'images/minigame/run/obs_air_1.png',
                'air_4': 'images/minigame/run/obs_air_1.png',
            }
            
            # 图片路径
            self.duck_image = "images/minigame/run/mutsumi_duck.png" 
            self.hit_image = "images/minigame/run/mutsumi_hit.png"

            # 容错：如果没有蹲下图，临时用跑步图代替防止报错
            if not renpy.loadable(self.duck_image):
                self.duck_image = "images/minigame/run/mutsumi_run_1.png"

            
        def handle_input(self):
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            
            jump_pressed = keys[pygame.K_SPACE] or mouse_buttons[0]
            duck_pressed = keys[pygame.K_DOWN] or keys[pygame.K_s] or mouse_buttons[2]
            
            # 蹲下
            if duck_pressed and self.grounded and not jump_pressed:
                self.is_ducking = True
                self.current_anim = "duck"
            else:
                self.is_ducking = False
            
            # 跳跃
            if jump_pressed and not self.is_ducking:
                if self.grounded:
                    self.player_vy = RunConfig.JUMP_FORCE
                    self.grounded = False
                    self.current_anim = "jump"
                    renpy.play("audio/sfx_jump.ogg", channel="sound")
            
            # 状态更新
            if not self.grounded and not self.is_ducking:
                self.current_anim = "jump"
            elif self.grounded and not self.is_ducking:
                self.current_anim = "run"
                    
        def update_physics(self):
            self.player_vy += RunConfig.GRAVITY
            self.player_y += self.player_vy
            
            if self.player_y >= RunConfig.GROUND_Y:
                self.player_y = RunConfig.GROUND_Y
                self.player_vy = 0
                self.grounded = True
                
        def update_game(self):
            # 分数与黄瓜
            self.score += 1
            self.cucumbers = int(self.score / 500)

            # 速度逻辑
            if self.speed < RunConfig.SPEED_MAX:
                self.speed += 0.005 
                
            # ==========================
            # 🔄 场景切换逻辑 (修改处)
            # ==========================
            # 这里原本是 1800，现在改为 2500
            if self.score > 2500:
                self.stage = 2
                if renpy.music.get_playing() != "audio/bgm_run_hype.ogg":
                    renpy.music.play("audio/bgm_run_hype.ogg", fadein=4.0, if_changed=True)
                
                if self.transition_progress < 1.0:
                    self.transition_progress += 0.01
            
            # 背景滚动
            self.bg_offset -= self.speed * 0.5
            
            # 障碍物生成
            self.spawn_counter -= 1
            if self.spawn_counter <= 0:
                self.spawn_obstacle()
                min_interval = max(40, 100 - int(self.speed * 3))
                max_interval = max(70, 160 - int(self.speed * 3))
                self.spawn_counter = random.randint(min_interval, max_interval)
                
            # 障碍物移动与碰撞
            for obs in self.obstacles[:]:
                obs['x'] -= self.speed
                if self.check_collision(obs):
                    renpy.play("audio/sfx_crash.ogg", channel="sound")
                    self.playing = False
                    self.current_anim = "hit"
                    return
                if obs['x'] < -200:
                    self.obstacles.remove(obs)
                    
        def spawn_obstacle(self):
            rand = random.randint(1, 10)
            if rand <= 5: # 地面
                variant = random.randint(1, 6)
                self.obstacles.append({
                    'type': 'ground',
                    'img': self.obstacle_images['ground_{}'.format(variant)],
                    'x': 1350, 'y': RunConfig.GROUND_Y + 10, 'w': 60, 'h': 80
                })
            elif rand <= 8: # 中等
                variant = random.randint(1, 4)
                mid_height = RunConfig.GROUND_Y - random.choice([50, 60, 70, 80])
                self.obstacles.append({
                    'type': 'mid',
                    'img': self.obstacle_images['air_{}'.format(variant)],
                    'x': 1350, 'y': mid_height, 'w': 60, 'h': 60
                })
            else: # 高空
                variant = random.randint(1, 4)
                high_height = RunConfig.GROUND_Y - random.choice([120, 140, 160])
                self.obstacles.append({
                    'type': 'high',
                    'img': self.obstacle_images['air_{}'.format(variant)],
                    'x': 1350, 'y': high_height, 'w': 60, 'h': 60
                })
                
        def check_collision(self, obs):
            if self.is_ducking:
                p_left = RunConfig.PLAYER_X - 30
                p_right = RunConfig.PLAYER_X + 30
                p_top = self.player_y - 40
                p_bottom = self.player_y
            else:
                p_left = RunConfig.PLAYER_X - 25
                p_right = RunConfig.PLAYER_X + 25
                p_top = self.player_y - 80
                p_bottom = self.player_y
            
            o_left = obs['x']
            o_right = obs['x'] + obs['w']
            o_top = obs['y'] - obs['h']
            o_bottom = obs['y']
            
            return (p_right > o_left and p_left < o_right and
                    p_bottom > o_top and p_top < o_bottom)
                    
        def get_sprite_image(self):
            if not self.playing:
                return self.hit_image
            
            if self.current_anim == "duck":
                return self.duck_image
            elif self.current_anim == "jump":
                # 跳跃使用奔跑第一帧
                return "images/minigame/run/mutsumi_run_1.png"
            else:
                # 固定频率动画
                frame = (self.frame_counter // 3) % 8 + 1
                return "images/minigame/run/mutsumi_run_{}.png".format(frame)

        def get_sprite_y_offset(self):
            if self.current_anim == "jump" and not self.grounded:
                return RunConfig.JUMP_SPRITE_OFFSET
            return 0
                
        def update(self):
            if not self.playing:
                return
            
            # 防崩检查
            if not hasattr(self, 'frame_counter'):
                self.frame_counter = 0
            
            self.frame_counter += 1
            self.handle_input()
            self.update_physics()
            self.update_game()

# 背景图定义
image bg_runner_school = "images/minigame/run/bg_school.png"
image bg_runner_stage = "images/minigame/run/bg_stage.png"

screen runner_game_screen(game):
    modal True
    
    # 游戏循环
    timer 0.02 repeat True action Function(game.update)
    
    # ==========================
    # 🖼️ 背景层 (平滑过渡)
    # ==========================
    fixed:
        xsize 1280 ysize 720
        add Solid("#87CEEB")
        
        $ scroll_x = int(game.bg_offset) % 2560
        $ fade_out_alpha = 1.0 - game.transition_progress
        $ fade_in_alpha = game.transition_progress
        
        # 1. 绘制“学校”背景
        add "bg_runner_school":
            xpos (scroll_x - 2560) ypos 0
            alpha fade_out_alpha 
            
        add "bg_runner_school":
            xpos scroll_x ypos 0
            alpha fade_out_alpha 
            
        # 2. 绘制“舞台”背景
        add "bg_runner_stage":
            xpos (scroll_x - 2560) ypos 0
            alpha fade_in_alpha
            
        add "bg_runner_stage":
            xpos scroll_x ypos 0
            alpha fade_in_alpha 
    
    # 障碍物层
    python:
        obs_to_draw = []
        for obs in game.obstacles:
            obs_to_draw.append({'image': obs['img'], 'x': int(obs['x']), 'y': int(obs['y'])})
    for obs_data in obs_to_draw:
        add obs_data['image'] xpos obs_data['x'] ypos obs_data['y'] anchor (0.0, 1.0)
    
    # 玩家层
    python:
        player_sprite = game.get_sprite_image()
        sprite_y_offset = game.get_sprite_y_offset()
        player_display_y = int(game.player_y + sprite_y_offset)

    add player_sprite:
        xpos RunConfig.PLAYER_X 
        ypos player_display_y 
        anchor (0.5, 1.0)
    
    # ==========================
    # 🌍 地面层 (循环滚动)
    # ==========================
    fixed:
        ypos RunConfig.GROUND_Y
        xsize 1280
        
        $ ground_scroll_x = int(game.bg_offset) % 1280
        
        add "images/minigame/run/ui_ground.png":
            xpos (ground_scroll_x - 1280)
            ypos 0
            
        add "images/minigame/run/ui_ground.png":
            xpos ground_scroll_x
            ypos 0
    
    # UI 层
    frame:
        background None
        xalign 0.0 yalign 0.0
        padding (20, 20)
        hbox:
            spacing 40
            text "得分: [game.score]" size 40 color "#FFF" outlines [(3, "#000")] bold True
            text "🥒 × [game.cucumbers]" size 40 color "#FFD700" outlines [(3, "#000")] bold True
    
    # 游戏结束界面
    if not game.playing:
        frame:
            modal True
            background Solid("#000000DD")
            align (0.5, 0.5)
            padding (60, 60)
            vbox:
                spacing 25
                align (0.5, 0.5)
                text "游戏结束" size 70 color "#FF4444" xalign 0.5 bold True
                null height 20
                text "最终得分: [game.score]" size 35 color "#FFF" xalign 0.5
                text "黄瓜收获: [game.cucumbers]" size 35 color "#FFD700" xalign 0.5
                null height 30
                hbox:
                    spacing 40
                    xalign 0.5
                    textbutton "再来一次":
                        background Solid("#4CAF50")
                        hover_background Solid("#66BB6A")
                        padding (30, 15)
                        text_size 30
                        text_color "#FFF"
                        text_bold True
                        action Jump("start_mortis_run_retry")
                    textbutton "返回":
                        background Solid("#757575")
                        hover_background Solid("#9E9E9E")
                        padding (30, 15)
                        text_size 30
                        text_color "#FFF"
                        text_bold True
                        action Return()

# ==========================================
# 游戏入口
# ==========================================
label start_mortis_run:
    scene black
    
    # ================================
    # 🎵 音乐记忆逻辑 (新增)
    # ================================
    python:
        # 获取当前播放的音乐
        current_playing_track = renpy.music.get_playing("music")
        
        # 定义跑酷游戏的专属音乐列表
        run_game_tracks = ["audio/bgm_run_chill.ogg", "audio/bgm_run_hype.ogg"]
        
        # 只有当【当前音乐】不是【跑酷音乐】时，才保存它
        # 这样防止“重试”时把跑酷音乐当成旧音乐保存了
        if current_playing_track not in run_game_tracks:
            store.mortis_last_music = current_playing_track

    # 隐藏菜单 & 播放跑酷音乐
    $ renpy.hide_screen("game_center_menu")
    $ renpy.music.play("audio/bgm_run_chill.ogg", loop=True, fadein=1.0)
    
    python:
        runner_game = RunnerGame()
    
    call screen runner_game_screen(runner_game)
    
    # ==========================
    # 🏆 结算奖励
    # ==========================
    python:
        if runner_game.cucumbers >= 5:
            # 检查函数是否存在，防止报错
            if "add_hgd" in globals():
                add_hgd("若叶睦", 3.0, daily_id="run_big_reward", max_daily=1)
    
    # ================================
    # 🎵 音乐还原逻辑 (新增)
    # ================================
    python:
        # 如果有保存的旧音乐，就播旧的
        if getattr(store, "mortis_last_music", None):
            renpy.music.play(store.mortis_last_music, fadein=2.0, loop=True)
        else:
            # 如果没保存到（或者之前没音乐），就停止音乐
            renpy.music.stop(fadeout=1.0)

    jump game_center_start

label start_mortis_run_retry:
    jump start_mortis_run