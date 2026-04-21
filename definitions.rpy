# 音乐 / 音效
define audio.bgm1 = "audio/1.ogg" # 睦子咪的小曲
#背景

image black = "#000000"
image dark = "#000000e4"
image darkred = "#110000c8"
image white = "#ffffff"
image bg street_day = "images/bg/street_day.jpg"#街道
image tos ="gui/tos.png"
image tos2 ="gui/tos2.png"
default persistent.current_bg_id = "default"
init python:
    def get_current_bg_image(st, at):
        if persistent.current_bg_id == "default":
            return Image("images/temp.png"), None
        target_path = "images/gacha_items/" + persistent.current_bg_id + ".png"

        if renpy.loadable(target_path):
            return Image(target_path), None
        else:
            return Image("images/temp.png"), None

# 3. 让 image temp 接管这个逻辑
image temp = DynamicDisplayable(get_current_bg_image)
image mutsumi_normal ="images/temp.png"
image justmortis ="images/temp0.png"
#下面是mortis模式的定义
image woshi_yewan ="images/mortis/1.png"
image woshi_morning ="images/mortis/2.png"
image library_day ="images/mortis/3.1.png"
image library_day1 ="images/mortis/3.2.png"
image library_day2 ="images/mortis/3.3.png"
image mutsumi_with_guitar ="images/mutsumi_with_guitar.png"
image mylove ="images/mylove.png"
image cafe_street_day ="images/mortis/4.png"
image park_sunset ="images/mortis/5.png"
image shopping_street_day="images/mortis/6.png"
image music_store_indoor="images/mortis/7.png"
image school_rooftop_sunset="images/mortis/8.png"
image amusement_park_day="images/mortis/9.png"
image art_gallery_red="images/mortis/10.png"
image botanical_garden_mist="images/mortis/11.png"
image living_room_night_cozy="images/mortis/12.png"
image riverside_sunset_gold="images/mortis/13.png"
image bus_stop_countryside="images/mortis/14.png"
image ferris_wheel_interior="images/mortis/15.png"
image seaside_dusk_vast="images/mortis/16.png"
image planetarium_dark="images/mortis/17.png"
image shrine_stairs_sunset="images/mortis/18.png"
image concert_hall_dark="images/mortis/19.png"
image mortis000="images/mortis/20.png"
image baocuo="images/mortis/baocuo.png"
#下面是主线故事模式的定义
image item_payslip ="images/bg/item_payslip.png"
image bg_greenhouse_exterior="images/bg/bg02.png"
image bg_school_gate_dusk="images/bg/bg01.png"
image item_id_card="images/bg/card.png"
image item_old_keycard="images/bg/card2.png"
image bg_greenhouse_inside="images/bg/bg03.png"
image bg_greenhouse_inside_rain ="images/bg/bg04.png"
image bg_school_courtyard="images/bg/bg05.png"#月之森的路
image bg_train_interior_night="images/bg/bg06.png"#电车地铁
image bg_train_interior_afternoon="images/bg/bg08.png"
image bg_apartment_room="images/bg/bg07.png"#主角的家
image bg_greenhouse_inside_dusk="images/bg/bg09.png"#有血的温室
image bg_greenhouse_corner_dusk:
    "images/bg/bg03.png"
    zoom 1.3
image cg_mu_protect_guitar="images/cg/1.png"#睦被砸伤
image bg_greenhouse_corner_guitar:
    "images/bg/guitarbag.png"
    zoom 0.29
    yoffset -100
image mu1_0:
    "images/character/m1_1_2.png"
    size(1116,3510)
    zoom 0.5
    yalign 0.1
    yoffset 680
    xalign 0.5
image m1_2:
    "images/character/m1_2.png"
    size(1116,3510)
    zoom 0.5
    yalign 0.1
    yoffset 680
    xalign 0.5
image mu1_1:
    "images/character/m1_2_2.png"
    size(1116,3510)
    zoom 0.5
    yalign 0.1
    yoffset 680
    xalign 0.5
image mu1_2:
    "images/character/m1_3.png"
    zoom 0.5
    yalign 0.1
    yoffset 680
    xalign 0.5
image mu1_3:
    "images/character/m1_4.png"
    zoom 0.5
    yalign 0.1
    yoffset 0
    xalign 0.5
image mu1_4:#蹲下
    "images/character/m1_5.png"
    zoom 0.2
    yalign 0.1
    yoffset 0
    xalign 0.5
image mu1_5:#蹲下伸手
    "images/character/m1_6.png"
    zoom 0.2
    yalign 0.1
    yoffset 0
    xalign 0.5

image mu1_6:#抱着吉他
    "images/character/m1_7_2.png"
    size(1252,3510)
    zoom 0.3
    yalign 0.1
    yoffset 400
    xalign 0.5
image m3_0:
    "images/mortis/m3_0.png"
    zoom 0.35
    yoffset 250
image m3_1:
    "images/mortis/m3_1.png"
    zoom 0.35
    yoffset 250
image m3_2:
    "images/mortis/m3_2.png"
    zoom 0.35
    yoffset 250
image m3_3:
    "images/mortis/m3_3.png"
    zoom 0.35
    yoffset 250
image m3_shy_smile:
    "images/mortis/m3_3.png"
    zoom 0.35
    yoffset 250
image m3_4:
    "images/mortis/m3_4.png"
    zoom 0.35
    yoffset 250
image m3_smile:
    "images/mortis/m3_4.png"
    zoom 0.35
    yoffset 250
    
image m3_surprise:
    "images/mortis/m3_5.png"
    zoom 0.35
    yoffset 250
image m3_pout:
    "images/mortis/m3_6.png"
    zoom 0.35
    yoffset 250
image m3_thinking:
    "images/mortis/m3_7.png"
    zoom 0.35
    yoffset 250
image m3_7:
    "images/mortis/m3_7.png"
    zoom 0.35
    yoffset 250
image m3_8:
    "images/mortis/m3_8.png"
    zoom 0.35
    yoffset 250
image m3_angry:
    "images/mortis/m3_9.png"
    zoom 0.35
    yoffset 250
image m3_side_normal:
    "images/mortis/m3_10.png"
    zoom 0.35
    yoffset 250
image m3_10:
    "images/mortis/m3_10.png"
    zoom 0.35
    yoffset 250
image m3_menu_reading:
    "images/mortis/m3_11.png"
    zoom 0.35
    yoffset 250
image m3_smug:
    "images/mortis/m3_12.png"
    zoom 0.35
    yoffset 250     
image m3_12:
    "images/mortis/m3_12.png"
    zoom 0.35
    yoffset 250     
image m3_happy_closed_eyes:
    "images/mortis/m3_13.png"
    zoom 0.35
    yoffset 250    
image m3_sparkle_eyes:
    "images/mortis/m3_14.png"
    zoom 0.35
    yoffset 250             
image m3_side_tired:
    "images/mortis/m3_15.png"
    zoom 0.35
    yoffset 250              
  
    
image m3_sitting_relax:
    "images/mortis/m3_16.png"
    zoom 0.35
    yoffset 250                 
image m3_closed_eyes_sniffing:
    "images/mortis/m3_17.png"
    zoom 0.35
    yoffset 250                 
image m3_yandere_cold:
    "images/mortis/m3_18.png"
    zoom 0.35
    yoffset 250     
image m3_18:
    "images/mortis/m3_18.png"
    zoom 0.35
    yoffset 250  
image m3_sad:
    "images/mortis/m3_19.png"
    zoom 0.35
    yoffset 250        
image m3_cold_stare:
    "images/mortis/m3_20.png"
    zoom 0.35
    yoffset 250   
image m3_dark:
    "images/mortis/m3_20.png"
    zoom 0.35
    yoffset 250  
image m3_cry:
    "images/mortis/m3_21.png"
    zoom 0.35
    yoffset 250 
image m3_21:
    "images/mortis/m3_21.png"
    zoom 0.35
    yoffset 250 
define audio.story1 = "audio/story/変わらないからこそ.ogg"#欢快的小曲
define audio.story2 = "audio/story/電波リレーの勝者.ogg"#温室内部的小曲
define audio.story3 = "audio/story/なぜ日は傾くのか.ogg"#夕阳的小曲
define audio.story4 = "audio/story/怪優奇優侏儒巨人美少女等募集.ogg"#怪异的小曲
define audio.story5 = "audio/story/邂逅.ogg"#Just若叶睦自己的关羽之歌
define audio.story6 = "audio/story/小さな記憶.ogg"#电车小曲
define audio.story7 = "audio/story/joker.ogg"#丑爷八音盒
define audio.story8 = "audio/story/天使だから病みます (feat. Aiobahn +81).ogg"#超天酱发病的小曲
define audio.story9 = "audio/story/天使は感動する (feat. Aiobahn +81).ogg"#超天酱突破粉丝的小曲
#杂项
default persistent.playername = ""

default m1_name = '若叶睦'
default m2_name = '墨缇斯'
default mu = '若叶睦'
default player = persistent.playername
init python:
    def m3_auto_zoom_callback(event, interact=True, **kwargs):
        # 如果不是交互模式（比如回想模式），就不执行
        if not interact:
            return

        # 这里填你 show 语句里用的标签名，通常是 "m3"
        image_tag = "m3" 

        if event == "begin":
            # 说话开始：应用放大变换
            renpy.show(image_tag, at_list=[m3_speaking_zoom])
        
        elif event == "end":
            # 说话结束：应用恢复变换
            renpy.show(image_tag, at_list=[m3_idle_zoom])
    
#角色定义
define mc = DynamicCharacter('player',  image='', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m1 = DynamicCharacter('m1_name', image='', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m2 = DynamicCharacter('m2_name', image='', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m3 = Character("墨缇斯",color="#FF0000", what_color="#CCCCCC")

style ruby_style is default:
    size 12
    yoffset -25

style say_dialogue:
    ruby_line_leading 12
    ruby_style style.ruby_style

style history_text:
    ruby_line_leading 12
    ruby_style style.ruby_style

init python:
    config.keymap['game_menu'].remove('mouseup_3')
    config.keymap['hide_windows'].append('mouseup_3')
    config.keymap['self_voicing'] = []
    config.keymap['clipboard_voicing'] = []
    config.keymap['toggle_skip'] = []
    renpy.music.register_channel("music_poem", mixer="music", tight=True)
    
    # Get's position of Music
    def get_pos(channel='music'):
        pos = renpy.music.get_pos(channel=channel)
        if pos: return pos
        return 0
    
    # 删除所有存档
    def delete_all_saves():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)
    # 控制时间所用的暂停
    def pause(time=None):
        #global _windows_hidden
        if not time:
            #_windows_hidden = True
            renpy.ui.saybehavior(afm=" ")
            renpy.ui.interact(mouse='pause', type='pause', roll_forward=None)
            #_windows_hidden = False
            return
        if time <= 0: return
        # _windows_hidden = True
        renpy.pause(time)
        # _windows_hidden = False

    VALID_MUTSUMI_NAMES = [
            "若叶睦", "睦", "小睦",  "mutsumi", 
            "吉他睦",  "mutsumi wakaba"
        ]
    def check_is_mutsumi(input_name):
            if not input_name:
                return False
            # 转小写并去空格，防止大小写差异
            norm_name = input_name.strip().lower()
            # 只要输入的文字包含列表里的任意一个词，就算对
            # 比如输入 "把若叶睦还给我"，也能识别出 "若叶睦"
            for keyword in VALID_MUTSUMI_NAMES:
                if keyword in norm_name:
                    return True
            return False
    def check_is_self_ref(input_name):
        """
        检查玩家是否输入了墨缇斯自己的名字
        """
        if not input_name:
            return False
            
        # 转小写并去空格
        norm_name = input_name.strip().lower()
        
        # 禁止词列表
        forbidden_names = ["墨缇斯", "mortis", "m3", "墨提斯"]
        
        for name in forbidden_names:
            if name in norm_name:
                return True
        return False

screen mortis_name_popup():
    # ==========================================
    # 变量定义
    # ==========================================
    default input_name = "" 
    # 新增：用于显示警告信息的变量
    default warning_msg = "" 
    
    modal True
    zorder 200
    
    add Solid("#000000D0") 
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        padding (40, 40)
        background Solid("#1a0505") 
        
        vbox:
            spacing 20
            xfill True
            
            text "⚠ SYSTEM WARNING: NULL POINTER EXCEPTION" color "#f00" size 20 bold True xalign 0.5
            text "请输入目标对象名称以覆盖当前变量：" color "#fff" size 28 xalign 0.5
            
            null height 10
            
            # 输入框
            input:
                value ScreenVariableInputValue("input_name") 
                length 20
                
                # 【优化】当玩家修改文字时，清空警告信息，提升体验
                changed Function(lambda s: SetScreenVariable("warning_msg", "")())
                
                color "#0f0" 
                size 50
                xalign 0.5
                text_align 0.5
            
            # --- 🔴 动态警告信息显示区域 ---
            if warning_msg != "":
                text "[warning_msg]" color "#f00" size 24 xalign 0.5 bold True at glitch_tearing_shake_text
            else:
                # 占位符，防止布局跳动
                null height 33
            # ---------------------------
            
            null height 10
            
            # 确认按钮
            textbutton "[[ 确 认 / ENTER ]":
                xalign 0.5
                style "button"
                text_size 30
                text_color "#aaa"
                text_hover_color "#fff"
                background Solid("#333")
                padding (20, 10)

                action If(
                    check_is_self_ref(input_name), 
                    SetScreenVariable("warning_msg", "你在干什么？我就在你面前啊。"), 
                    Return(input_name)
                )

    key "K_RETURN" action If(check_is_self_ref(input_name), SetScreenVariable("warning_msg", "你在干什么？我就在你面前啊。"), Return(input_name))
    key "K_KP_ENTER" action If(check_is_self_ref(input_name), SetScreenVariable("warning_msg", "你在干什么？我就在你面前啊。"), Return(input_name))

transform glitch_tearing_shake_text:
    xoffset 0
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 0
init python:
    # --- 🐭 鼠标争夺战逻辑 ---
    import random

    # 定义按钮的初始位置
    runaway_x = 0.5
    runaway_y = 0.5

    def teleport_button():
        """
        当鼠标悬停在按钮上时，强制把按钮瞬移到屏幕其他地方
        """
        global runaway_x, runaway_y
        
        # 随机生成新坐标 (避免生成在边缘)
        new_x = random.uniform(0.1, 0.9)
        new_y = random.uniform(0.1, 0.9)
        
        # 只有当新坐标距离够远时才移动，防止闪烁
        store.runaway_x = new_x
        store.runaway_y = new_y
        
        # 播放一个滑稽或故障的音效
        renpy.play("audio/sfx_ui_run.ogg", channel="audio") 
        renpy.restart_interaction() # 强制刷新屏幕

    # --- 🖥️ 窗口控制逻辑 ---
    def scare_minimize():
        """
        强制最小化游戏窗口，模拟闪退
        """
        import pygame
        # 尝试使用 Ren'Py 内置的 iconify
        try:
            renpy.iconify()
        except:
            pass

    def generate_fake_script():
        """
        在游戏根目录生成一个假的 script.rpy 文件
        内容模仿 Ren'Py 的源代码格式
        """
        target_path = os.path.join(get_game_root(), "script.rpy")
        
        # 预设的伪代码内容
        content = """# ==================================================================
# Just Mutsumi - Core System Script
# Copyright (C) 2026 Mortis AI. All rights reserved.
# ==================================================================

define config.name = "Just Mutsumi"
define config.version = "0.X版"

# [SYSTEM CRITICAL SETTINGS]
# 警告：修改此部分可能导致世界线变动或系统崩溃。

default persistent.allow_quit = False
default persistent.love_level = "MAX"

# ------------------------------------------------------------------
# [CURRENT GAME MODE STATUS]
# True  = 开启 Just 墨缇斯 模式 (当前状态)
# False = 开启 原始 Galgame 模式 (已废弃)
# ------------------------------------------------------------------

persistent.in_mortis_mode = True

init python:
    import datetime
    import random

    # 针对 Windows 平台，强制将渲染器锁定为 angle (DirectX)
    if renpy.windows:
        try:
            config.renderer = "angle"
        except:
            pass

    # 基础引擎配置
    config.gl2 = True
    config.allow_skipping = False

    # --- 变量初始化检查 ---
    if persistent.asked_birthday is None: persistent.asked_birthday = False
    if persistent.asked_gender is None: persistent.asked_gender = False
    if persistent.asked_real_name is None: persistent.asked_real_name = False
    if persistent.first_met is None: persistent.first_met = False
    if persistent.playername is None: persistent.playername = ""
    if persistent.player_bday_month is None: persistent.player_bday_month = 0
    if persistent.player_bday_day is None: persistent.player_bday_day = 0
    if persistent.player_gender is None: persistent.player_gender = "unknown"
    if persistent.seen_random_labels is None: persistent.seen_random_labels = []
    if persistent.last_login_date is None: persistent.last_login_date = ""
    if persistent.last_talk_reward_date is None: persistent.last_talk_reward_date = ""
    if persistent.random_talk_today_count is None: persistent.random_talk_today_count = 0
    if persistent.last_time_period_bonus is None: persistent.last_time_period_bonus = ""


    def FileActionMod(name, page=None, **kwargs):
        if renpy.get_screen("save"):
            return Show(
                screen="dialog",
                message="没有存档的必要。\n睦一直都会在你的身边。",
                ok_action=Hide("dialog")
            )
        
        # 读取依然是被允许的
        if renpy.get_screen("load"):
            return FileLoad(name, page=page, **kwargs)
            
        return FileAction(name, page=page, **kwargs)


    # 辅助函数
    def check_today_event():
        today = datetime.date.today()
        m, d = today.month, today.day
        if m == persistent.player_bday_month and d == persistent.player_bday_day:
            return "birthday"
        return None

    def get_time_period():
        hour = datetime.datetime.now().hour
        if 5 <= hour < 11: 
            return "morning"
            
        # 中午：11:00 - 13:59
        elif 11 <= hour < 14: 
            return "noon"
            
        # 下午：14:00 - 17:59 
        elif 14 <= hour < 18: 
            return "afternoon"
            
        # 晚上：18:00 - 22:59 
        elif 18 <= hour < 23: 
            return "evening"
            
        # 深夜：23:00 - 04:59 
        else: 
            return "midnight"

# ==========================================================
# 🛡️ 3. 读档保护标签 (关键修复)
# ==========================================================
label after_load:
    if main_story_mode:
        $ renpy.retain_after_load()
    return



label start:
    # 强制称呼输入
    
    if not persistent.playername.strip():
        call screen name_input(message="请输入睦对你的称呼", ok_action=Function(FinishEnterName))
        while not persistent.playername.strip():
            call screen name_input(message="名字不能为空，请输入称呼", ok_action=Function(FinishEnterName))

    if persistent.in_mortis_mode:
        $ in_mortis_mode = True # 同步运行时变量
        jump start_mortis_mode  # 强制踢回里世界
                
    $ persistent.ghost_menu = True
    $ quick_menu = True

    if not persistent.first_met:
        jump first_meeting
    else:
        jump daily_check




# ==================================================================
# End of File
# ==================================================================
"""
        try:
            # 写入文件
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except:
            return False

    def check_script_modification():
        """
        检查 script.rpy 中的关键变量是否被修改
        返回: "unchanged" (未修改), "modified" (修改成功), "error" (文件丢失)
        """
        target_path = os.path.join(get_game_root(), "script.rpy")
        
        if not os.path.exists(target_path):
            return "error"
            
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # 检查关键行是否被修改
            # 允许玩家写 False, false, 0 等
            if "persistent.in_mortis_mode = False" in content:
                return "modified"
            elif "persistent.in_mortis_mode = false" in content:
                return "modified"
            else:
                return "unchanged"
        except:
            return "error"
screen mortis_runaway_choice():
    
    modal True
    zorder 100
    
    # 背景变暗
    add Solid("#000000A0")
    
    # 墨缇斯的嘲讽文字 (显示在屏幕上方)
    text "手滑了吗？再给你一次机会哦。" color "#f00" size 40 outlines [(2, "#000", 0, 0)] xalign 0.5 yalign 0.1 at glitch_tearing_shake_text

    # --- 那个会逃跑的按钮 (想选“是”) ---
    button:
        # 位置绑定变量
        align (runaway_x, runaway_y)
        
        # 样式
        background Solid("#aa0000")
        padding (30, 15)
        
        text "【恢复若叶睦的数据】" size 30 color "#fff"
        
        # 核心：鼠标一放上去 (hovered)，就调用瞬移函数
        hovered Function(teleport_button)
        
        # 根本点不到，所以 action 随便写
        action NullAction()
        
        # 加一个平滑移动的效果，让它看起来像在“躲”
        at transform:
            linear 0.1 align (runaway_x, runaway_y)

    # --- 只能选的按钮 (被迫选“否”) ---
    textbutton "【放弃抵抗】":
        align (0.5, 0.8) # 固定在下方
        style "button"
        background Solid("#333")
        padding (30, 15)
        text_size 30
        text_color "#aaa"
        
        # 只有这个能点
        action Return("give_up")