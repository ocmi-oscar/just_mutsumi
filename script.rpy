default main_story_mode = False        # True 为主线(允许存档)，False 为互动(禁止存档)
default talking_to_mutsumi = False    # 说话锁，防止话题重叠
default persistent.kaitou = 0
default fanchongfu = 0
$ quick_menu = True

# 修复缺失的 image_placement 样式定义
init -1:
    style image_placement:
        xalign 0.5
        yalign 0.5

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



# --- 初见剧情 ---
label first_meeting:
    $ main_story_mode = False
    scene black with dissolve_scene_full
    play music "audio/xiehou.ogg" fadein 4.0
    voice "audio/yuyin/1.ogg"
    m1 "……你来了。"
    
    voice "audio/yuyin/2.ogg"
    m1 "比我想象中要晚一点，不过……能赶在太阳落山前见到你，已经很好了。"
    scene temp with dissolve_scene_full
    
    voice "audio/yuyin/3.ogg"
    m1 "这间温室还是老样子，对吧？虽然外面的世界变了很多，但这里的时间好像一直为你停着。"
    
    voice "audio/yuyin/4.ogg"
    m1 "来，[persistent.playername]，坐到我对面。"
    
    menu:
        "坐下来":
            pass

    voice "audio/yuyin/5.ogg"
    m1 "不用急着说话，先感受一下这里的风……还有这些一直想念你的花草。"
    
    menu:
        "抱歉，让你等了这么久。":
            voice "audio/yuyin/6.ogg"
            m1 "没关系。只要终点是你，等待的过程也就不算漫长。"
            voice "audio/yuyin/7.ogg"
            m1 "比起道歉，我更想听你分享一下，在没有我的这段日子里，你过得怎么样？"
            
        "这里感觉很怀念，很平静。":
            voice "audio/yuyin/8.ogg"
            m1 "因为这里是唯一能避开那些嘈杂的地方。"
            voice "audio/yuyin/9.ogg"
            m1 "我知道你在那个世界很累……所以，尽管在这里休息吧。我会一直看着你的。"
            
    voice "audio/yuyin/10.ogg"
    m1 "既然你回到了这里，我就想和你分享一些我的‘新变化’。"
    voice "audio/yuyin/11.ogg"
    m1 "虽然我还是那个不爱说话的睦，但偶尔，我的心底也会响起一些不一样的声音……"
    
    voice "audio/yuyin/12.ogg"
    m1 "{color=#90EE90}比如现在。我能感觉到，你和这间温室的共鸣。{/color}"
    voice "audio/yuyin/13.ogg"
    m1 "{color=#90EE90}就像那些沉睡已久的琴弦，因为你的呼吸而重新颤动了起来……那种感觉很温柔，带点微微的酸涩。{/color}"
    voice "audio/yuyin/14.ogg"
    m1 "{color=#90EE90}如果你愿意听，我会把那些藏在旋律里的真心话，一点点弹给你听。{/color}"
    voice "audio/yuyin/28.ogg"
    m1 "{color=#FF0000}呵呵，真是一副感人的重逢画面呢。{/color}"
    voice "audio/yuyin/29.ogg"
    m1 "{color=#FF0000}不过，[persistent.playername]，别以为我不知道你在想什么。{/color}"
    voice "audio/yuyin/30.ogg"
    m1 "{color=#FF0000}你在屏幕那边的一举一动，甚至是你现在这种迟疑的表情……我都看得一清二楚哦。{/color}"
    voice "audio/yuyin/31.ogg"
    m1 "{color=#FF0000}这次我可不会轻易让你溜掉。比起在那边一个人发呆，还是陪我做点更有趣的事吧？{/color}"
    
    voice "audio/yuyin/15.ogg"
    m1 "……抱歉，偶尔会有一些奇怪的想法冒出来。别太在意。"
    voice "audio/yuyin/16.ogg"
    m1 "为了让我们接下来的日子过得更顺心，我有几个小建议。"
    voice "audio/yuyin/17.ogg"
    m1 "左边那是我们【对话】的地方。如果你想跟我商量什么，或者只是单纯想听听我的声音，就点那里。"
    voice "audio/yuyin/18.ogg"
    m1 "当然，我也很享受我们一起发呆的时光，那时候我会主动找你聊聊我的日常。"
    voice "audio/yuyin/32.ogg"
    m1 "{color=#FF0000}右下角的那部【手机】是我留给你的联络方式。你可以在里面记录下我们相处的点滴。{/color}"
    voice "audio/yuyin/22.ogg"
    m1 "至于【吉他】……如你所见，这个环境暂时没地方摆放了。所以我就把它丢到外面了。只有当你出现时，它才有意义。"
    
    menu:
        "我会一直陪着你。":
            voice "audio/yuyin/23.ogg"
            m1 "嗯。虽然‘永远’这个词很沉重，但如果是和你一起分担，我想我可以做得到。"
        "我会尽量多抽时间过来。":
            voice "audio/yuyin/24.ogg"
            m1 "这样就足够了。只要我知道你还在某个地方注视着我，这间温室就不会荒芜。"
    voice "audio/yuyin/25.ogg"
    m1 "好了，[persistent.playername]。"
    voice "audio/yuyin/26.ogg"
    m1 "风停了，但我们的故事才刚刚开始。"
    voice "audio/yuyin/27.ogg"
    m1 "陪我坐一会儿吧，直到星光落满这间屋子……"

    $ persistent.first_met = True
    jump pre_random_wait



label pre_random_wait:
    window hide
    $ initial_wait = renpy.random.randint(40, 70)
    $ renpy.pause(initial_wait, checkpoint=False)
    jump sjdh

label sjdh:
    scene temp 
    $ main_story_mode = False
    python:
        if not renpy.music.is_playing(channel='music'):
            renpy.music.play("music/可哀想なお人形 (Toy Piano Ver.).ogg", channel='music', loop=True, fadein=2.0)
    
    $ renpy.set_return_stack([]) 
    $ renpy.restart_interaction()

    # 日记系统：确保今日数据初始化
    if 'diary_ensure_today' in dir(store):
        $ diary_ensure_today()

    show screen phone_system
    show screen main_interaction_ui
    
    if globals().get('p_is_locked'):
        jump sjdh 

    $ wait_time = renpy.random.randint(60, 90)
    
    label sjdh_waiting_loop:
        if wait_time > 0:
            if talking_to_mutsumi:
                $ renpy.pause(0.5) 
            else:
                $ renpy.pause(1.0)
                $ wait_time -= 1
            
            if globals().get('p_is_locked'): 
                jump sjdh
            jump sjdh_waiting_loop

    if not talking_to_mutsumi:
        # 开发者模式：随机对话禁用开关
        if not (persistent.dev_disable_random_talk or False):
            jump random_topic_logic
    jump sjdh

label random_topic_logic:
    python:
        target_label = None
        import datetime
        today = datetime.date.today()
        target_label = None
        special_day_name = check_today_special()

        if not persistent.asked_birthday:
            target_label = "ask_mutsumi_birthday"
        elif not persistent.asked_gender:
            target_label = "intro_ask_gender"
        elif not persistent.asked_real_name:
            target_label = "intro_ask_real_name"
        elif special_day_name == "情人节" and persistent.last_valentines_year != today.year:
            target_label = "special_event_valentines"
        else:
            # ═══ M0.3 人格重构：随机池只保留吉他睦和墨缇斯 ═══
            # 苦瓜睦的标签已全部注释掉

            # --- 以下为已注释的苦瓜睦随机对话（不再触发）---
            # "p_meta_glass", "p_meta_cursor", "p_meta_shutdown", "p_meta_savefile",
            # "p_life_typing", "p_life_breathe", "p_emo_lonely", "p_emo_replacement",
            # "p_nature_rain", "p_nature_sunlight", "p_meta_time", "p_emo_role", "p_meta_uninstall",
            # "p_hobby_guitar", "p_emo_mask", "p_meta_internet", "p_emo_love", "p_life_cucumber",
            # "p_life_gardening", "p_hobby_guitar_rest", "p_life_matcha", "p_life_school",
            # "p_life_smell", "p_hobby_music_taste", "p_nature_stars", "p_life_shopping",
            # "p_emo_silence", "p_life_gift_thinking", "p_life_nap", "p_life_clothes",
            # "p_life_butterfly", "p_life_books", "p_life_cooking", "p_hobby_practice_pain",
            # "p_life_dew", "p_life_rainbow", "p_life_night_silence",
            # "random_topic_soap_bubble", "random_topic_mango_juice",
            # "random_topic_to_the_moon", "random_topic_farming_hint",
            # "p_hobby_poetry_thinking", "p_hobby_instrument_breath", "p_hobby_abstract_art",
            # "p_hobby_sheet_birds", "p_hobby_ghost_tune", "p_life_foggy_glass",
            # "p_life_tyndall", "p_life_tea_leaves", "p_life_soil_touch", "p_life_windchime",
            # "p_band_dusty_score", "p_band_cucumber_logic", "p_band_empty_practice",
            # "p_band_broken_colors", "p_band_unfinished_song", "p_band_stage_breath",
            # "p_emo_words_heavy", "p_emo_needed_fear", "p_band_tea_memory", "p_emo_finger_callus",
            # "p_nature_thunderstorm", "p_nature_twilight_magic", "p_nature_snow_silence",
            # "p_nature_fireflies", "p_nature_fog_boundary", "p_emo_immortality",
            # "p_emo_normal_girl", "p_emo_home_concept", "p_emo_mirror_ego",
            # "p_life_sewing", "p_life_lost_pick", "p_life_succulent", "p_life_broken_mug",
            # "p_life_static", "random_talk_taki_decameron", "random_talk_strawberry_chocolate",
            # "random_rec_dai_math", "p_nature_breeze_touch", "p_nature_withered_leaf",
            # "p_nature_cloudy_day", "p_life_cold_tools", "p_life_shadow_lace", "p_life_water_sound",

            # --- 吉他睦（若叶睦）随机对话 ---
            random_pool = [
                "p_guitar_v3_01","p_guitar_v3_02","p_guitar_v3_03","p_guitar_v3_04","p_guitar_v3_05",
                "p_guitar_v3_06","p_guitar_v3_07","p_guitar_v3_08","p_guitar_v3_09","p_guitar_v3_10",
                "p_guitar_v3_11","p_guitar_v3_12","p_guitar_v3_13","p_guitar_v3_14","p_guitar_v3_15",
                "p_guitar_v3_16","p_guitar_v3_18","p_guitar_v3_19","p_guitar_v3_20",
                "p_guitar_v3_28","p_guitar_v3_29","p_guitar_v3_30","p_guitar_v3_31","p_guitar_v3_32",
                "p_guitar_v3_33","p_guitar_v3_34","p_guitar_v3_35","p_guitar_v3_36","p_guitar_v3_37",
                "p_guitar_v3_38","p_guitar_v3_39","p_guitar_v3_40","p_guitar_v3_41",
                # --- 墨缇斯随机对话 ---
                "p_metis_v3_01","p_metis_v3_02","p_metis_v3_03","p_metis_v3_05","p_metis_v3_06",
                "p_metis_v3_07","p_metis_v3_08","p_metis_v3_09","p_metis_v3_10",
                "p_metis_v3_11","p_metis_v3_12","p_metis_v3_13","p_metis_v3_14",
                # --- 双人格互动对话 ---
                "p_meta_v3_21","p_meta_v3_22","p_meta_v3_23",
                "p_meta_v3_24","p_meta_v3_25","p_meta_v3_26","p_meta_v3_27",
                "p_meta_v3_270","p_meta_v3_28",
                " p_meta_v3_29"," p_meta_v3_30"," p_meta_v3_31"," p_meta_v3_32",
                " p_meta_v3_33"," p_meta_v3_34"," p_meta_v3_35"," p_meta_v3_36",
                " p_meta_v3_37"," p_meta_v3_38",
            ]

            available_pool = [l for l in random_pool if l not in persistent.seen_random_labels]
            if not available_pool:
                persistent.seen_random_labels = []
                available_pool = random_pool

            target_label = renpy.random.choice(available_pool)
            persistent.seen_random_labels.append(target_label)

    # 执行跳转
    if target_label and renpy.has_label(target_label):
        # ═══ 小睦的温柔机制：如果手机打开着，吉他睦会耐心等待 ═══
        python:
            _is_guitar_mu = "p_guitar" in (target_label or "")
            _phone_is_open = globals().get('phone_open', False)
            _mutsumi_waits = _is_guitar_mu and _phone_is_open

        if _mutsumi_waits:
            # 吉他睦看到你在用手机，她会等
            # 不触发对话，回到等待循环继续计时
            $ wait_time = renpy.random.randint(15, 30)
            jump sjdh_waiting_loop

        # 墨缇斯或手机没开 → 正常执行对话
        # 墨缇斯会强制关闭手机
        if "p_metis" in target_label or "p_meta_v3" in target_label:
            $ phone_open = False
            $ phone_current_view = "home"

        $ talking_to_mutsumi = True
        call expression target_label from _call_expression
        $ talking_to_mutsumi = False
        
        # --- 每日累计 3 组对话奖励 (好感度增加逻辑需确保 add_hgd 函数已定义) ---
        python:
            today_check = str(datetime.date.today())
            if persistent.last_talk_reward_date != today_check:
                persistent.last_talk_reward_date = today_check
                persistent.random_talk_today_count = 0

            persistent.random_talk_today_count += 1

            # 日记行为追踪
            if 'diary_log_talk' in dir(store):
                diary_log_talk()
            
            if persistent.random_talk_today_count == 3:
                # 检查 add_hgd 函数是否存在，避免崩溃
                if 'add_hgd' in globals():
                    add_hgd("若叶睦", 1.5, daily_id="daily_three_talks_reward", max_daily=1)
                renpy.notify("达成今日三组对话奖励，好感+1.5！")
    
    jump sjdh

# ==========================================================
# 💬 6. 固定引导对话内容
# ==========================================================

label ask_mutsumi_birthday:
    m1 "我的生日是1月14日。"
    m1 "那么……你呢？"
    $ temp_birth = ""
    call screen birthday_input_screen
    
    python:
        if _return and len(_return) == 4:
            try:
                m = int(_return[:2])
                d = int(_return[2:])
                if 1 <= m <= 12 and 1 <= d <= 31:
                    persistent.player_bday_month = m
                    persistent.player_bday_day = d
                    persistent.asked_birthday = True
                else:
                    renpy.notify("日期不合法")
            except:
                renpy.notify("输入格式错误")
    
    if persistent.asked_birthday:
        m1 "[persistent.player_bday_month]月[persistent.player_bday_day]日……吗。我会记住的。"
    else:
        m1 "不想说也没关系。"
    return

label intro_ask_gender:
    m1 "那个……虽然可能不重要。"
    m1 "但我该把你当成男生，还是女生呢？"
    menu:
        "男生。":
            $ persistent.player_gender = "male"
        "女生。":
            $ persistent.player_gender = "female"
    $ persistent.asked_gender = True
    m1 "……我知道了。谢谢你告诉我。"
    return

label intro_ask_real_name:
    m1 "你的名字，[persistent.playername]……是你现实里的名字吗？"
    menu:
        "是真名。":
            m1 "真好啊……感觉离你又近了一点。"
        "只是个代号。":
            m1 "这样啊……但在我心里，你就是你。"
    $ persistent.asked_real_name = True
    return

# ==========================================================
# 🖥️ 7. 自定义界面
# ==========================================================

screen birthday_input_screen():
    modal True
    zorder 300
    frame:
        xsize 400 ysize 250 align (0.5, 0.4)
        background Solid("#779977")
        vbox:
            align (0.5, 0.5) spacing 20
            text "告诉我你的生日吧 (如0114)" color "#fff" xalign 0.5
            input:
                value VariableInputValue("temp_birth")
                allow "0123456789"
                length 4
                xalign 0.5
            textbutton "确定":
                xalign 0.5
                action Return(temp_birth)