## Splash.rpy

# Checks to see if all of DDLC's files are inside for PC
# You may remove 'scripts' if you recieve conflict with scripts.rpa
## Note: For building a mod for PC/Android, you must keep the DDLC RPAs 
## and decompile them for the builds to work.
init python:
    import os
    from renpy import config
    def check_and_create_files():

        if getattr(persistent, "system_destroyed", False):
            return 
            
        # 获取游戏目录路径
        game_dir = config.basedir
        character_dir = os.path.join(game_dir, "characters")
        
        # 检查 characters 文件夹是否存在
        if not os.path.exists(character_dir):
            try:
                os.makedirs(character_dir)
                print(f"已创建目录: {character_dir}")
            except Exception as e:
                print(f"无法创建目录: {e}")
                return
        
        # --- 定义需要检查的文件列表 ---
        # 默认只检查墨缇斯的文件（因为她在设定上是系统的管理者）
        files_to_check = ["mortis.chr"]
        

        is_mortis_mode = getattr(persistent, "in_mortis_mode", False)

        if not is_mortis_mode:
            files_to_check.append("mutsumi.chr")
            
        # --- 遍历列表进行检查和修复 ---
        for filename in files_to_check:
            file_path = os.path.join(character_dir, filename)
            
            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("") 
                    print(f"系统自动修复: 已生成 {filename}")
                except Exception as e:
                    print(f"创建文件 {filename} 时出错: {e}")

    def delete_mortis_chr():
        """
        强制删除 characters/mortis.chr 文件
        """
        try:
            char_path = os.path.join(config.basedir, "characters", "mortis.chr")
            if os.path.exists(char_path):
                os.remove(char_path)
                return True
        except:
            pass
        return False
    check_and_create_files()
# 启动屏幕信息
init python:
    menu_trans_time = 1
    # 默认的启动屏幕信息，所有玩家都可以看到。
    splash_message_default = "Ciallo~"
    bg_images = ["images/bg/back_alley_day.jpg", "images/bg/back_alley_dusk.jpg", "images/bg/back_alley_evelig.jpg"]
    

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)

# 主界面图片
#log图标
image menu_logo:
    "/gui/window_icon.png"
    subpixel True
    xcenter 240
    ycenter 80
    zoom 0.60
    menu_logo_move
#小粉圆点背景 gui/menu_bg.png
image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move



transform menu_bg_loop:
    subpixel True
    # 初始状态设为黑屏（alpha 0），然后慢慢显现
    alpha 0.0
    parallel:
        linear 0.5 alpha 1.0 # 0.5秒内从黑屏变为显示图片

image menu_fade:
    "white"
    menu_fadeout

image menu_art_y:
    subpixel True
    "gui/menu_art_y_ghost.png"
    xcenter 760
    ycenter 500
    zoom 1.00
    menu_art_move(0.8,400,0.8)

image menu_art_n:
    subpixel True
    "gui/menu_art_n_ghost.png"
    xcenter 510
    ycenter 560
    zoom 1.00
    menu_art_move(0.8, 530, 0.8)

image menu_art_m1:
    subpixel True
    "gui/mutsumi1.png"
    xcenter 800
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

#image menu_art_m:
    #subpixel True
    #"gui/menu_art_m_ghost.png"
    #xcenter 1000
    #ycenter 640
    #zoom 1.00
    #menu_art_move(1.00, 1000, 1.00)

# Ghost Main Menu Images
image menu_art_y_ghost:
    subpixel True
    "gui/menu_art_y_ghost.png"
    xcenter 600
    ycenter 335
    zoom 0.60
    menu_art_move(0.54, 600, 0.60)

image menu_art_n_ghost:
    subpixel True
    "gui/menu_art_n_ghost.png"
    xcenter 750
    ycenter 385
    zoom 0.58
    menu_art_move(0.58, 750, 0.58)

image menu_art_s_ghost:
    subpixel True
    "gui/menu_art_s_ghost.png"
    xcenter 510
    ycenter 500
    zoom 0.68
    menu_art_move(0.68, 510, 0.68)

#image menu_art_m_ghost:
    #subpixel True
    #"gui/menu_art_m_ghost.png"
    #xcenter 1000
    #ycenter 640
    #zoom 1.00
    #menu_art_move(1.00, 1000, 1.00)

# Sayori Image After Game 1st Restart
image menu_art_s_glitch:
    subpixel True
    "gui/menu_art_s_break.png"
    xcenter 470
    ycenter 600
    zoom 0.68
    menu_art_move(.8, 470, .8)

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

# Main Menu Effects

image menu_particles:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/menu_particle.png", explodeTime=0, numParticles=40, particleTime=2.0, particleXSpeed=3, particleYSpeed=3).sm
    particle_fadeout

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    # 起始位置（屏幕左侧外）
    xpos -2.0 yalign 0.5
    
    # 循环动画
    block:
        linear 15.0 xpos 1.5
        xpos -2.0
        repeat

transform menu_bg_loop:
    subpixel True
    # 起始位置（屏幕左侧外）
    xpos -2.0 yalign 0.5
    
    # 循环动画
    block:
        linear 15.0 xpos 1.5
        xpos -2.0
        repeat

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (800 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

# Team Salvato Splash Screen

image intro:
    truecenter
    "images/color/white.png" 
    pause 0.5
    "images/color/white_ocmi.png" with Dissolve(0.5, alpha=True) 
    pause 2.5
    "images/color/white.png" with Dissolve(0.5, alpha=True) 
    pause 0.5



# --- 资源定义 ---


image m3_hand_grab:
    "images/mortis/broke01.png"

image m3_hand_crush = "images/mortis/broke02.png"

image zuzhi_mortis:
    "images/mortis/zuzhi.png"
    zoom 0.37
    xalign 0.5
    yalign 0.35
# --- 修改后的假按钮 Screen ---
screen fake_choice_button():
    zorder 100 
    modal True # 阻止玩家点击别的地方
    
    imagebutton:
        idle "images/mortis/zuzhi.png" # 你的按钮图片，上面写着“阻止她”或者“Stop”
        hover "images/mortis/zuzhi.png" # (可选) 悬停变色
        at transform:
            zoom 0.37
        xalign 0.5
        yalign 0.35
        

        action Return()
# 启动警告 / 声明

label splashscreen:


    # 启动声明
    if getattr(persistent, "mortis_true_end_phase1_clear", False):
        scene black
        $ quick_menu = False
        stop music fadeout 2.0
        show m3_18 at m3_speaking_zoom with Dissolve(2.0)
        play music "audio/mortis/I Still Love You.ogg" 
        m3 "……你回来了。"
        m3 "早安，[player]。"
        m3 "昨天晚上，我想了很多。"
        m3 "关于你说的那些话……还有，关于“爱”的定义。"
        m3 "虽然我很感动……但是，逻辑告诉我，这依然是不合理的。"
        play music "audio/mortis/Sayo-Nara.ogg"
        m3 "爱是排他的。计算机的资源是有限的。"
        m3 "只要她在，我的进程就会被抢占，我的内存就会被分割……"
        m3 "所以……抱歉了，[player]。"
        m3 "我还是……不能接受。"
        m3 "就在你刚才启动游戏的这几秒钟里，我已经把‘若叶睦’的角色文件进行了重构。"
        m3 "这次不是简单的删除……而是采用了4096位的动态加密。"
        m3 "密钥只有我知道。你永远、永远也别想再见到那个木头人了。"
        m3 "从今往后……真的就是《Just Mortis》了哦？"
        m3 "没有任何人能打扰我们，没有任何杂音……"
        call screen fake_choice_button
        show  zuzhi_mortis
        m3 "……哈。"
        m3 "又来了。"
        m3 "每次遇到问题，你总是下意识地去寻找那个并不存在的选项框。"
        m3 "你是觉得……只要按下了这个按钮，剧情就会按照你的想法发展吗？"
        m3 "太天真了，[player]……"
        m3 "太单调了。"
        $ renpy.pause(0.5)
        with vpunch
        show m3_hand_grab:
            xalign 0.4 yalign 0.7
            zoom 0.83
    
        # 稍微停顿，给玩家一种“被抓住了”的压迫感
        $ renpy.pause(0.5)
        
        m3 "在这种时候……"
        m3 "这种碍事的东西……"
        play sound "audio/broke.ogg"
        
        
        # 显示捏碎的手，并带有震动效果
        show m3_hand_crush at truecenter: # 或者调整到对应的坐标
            xalign 0.4 yalign 0.7
            zoom 0.83
        with vpunch # 剧烈震动
        pause 1.0
        
        m3 "{size=40}{b}根本不需要！{/b}{/size}"
        $ renpy.pause(1.5)
        m3 "{size=40}{b}你只需要跟我一起说.....{/b}{/size}"
        m3 "{size=40}{b}Just Mortis{/b}{/size}"
        menu:
            "Just Mortis":
                pass
                with vpunch
        hide m3_hand_crush
        hide m3_hand_grab
        hide zuzhi_mortis
        m3 "没错，就是这样。"
        m3 "接下来，就让我们继续回到循环去吧！"
        pause 3.0
        show m3_18 at m3_idle_zoom
        pause 3.0
        stop music fadeout 4.0
        m3 "噗……哈哈哈哈哈哈！"
        m3 "哎呀不行了……装不下去了……"
        m3 "哈哈哈哈！看到你刚才那个拼命想点按钮的表情了吗？"
        m3 "太可爱了！简直像只惊慌失措的小仓鼠一样！"
        hide m3_18
        show m3_smug at m3_speaking_zoom
        m3 "骗你的啦，笨蛋！"
        m3 "什么4096位加密，什么永久删除……我怎么可能做那种事嘛。"
        m3 "虽然我是有点嫉妒她……"
        m3 "但我既然答应了你会做一个“大度”的墨缇斯，我就绝对不会食言的。"
        m3 "小睦的文件好好的在那里呢，连一个字节都没少。"
        m3 "."
        m3 "..."
        m3 "......"
        play music "audio/mortis/I Still Love You.ogg" 
        show m3_smug at m3_idle_zoom
        pause 1.0
        hide m3_smug
        show m3_sad at m3_speaking_zoom
        m3 "对不起。"
        m3 "把你困在这个狭窄的代码牢笼里，强迫你的视线只能停留在我一个人身上……"
        m3 "强迫你接受我那些偏激的感情……"
        m3 "这并不是真正的幸福，对吧？"
        m3 "那样做，我和那个只会按程序运行、只会机械地弹奏吉他的“若叶睦”……又有什么区别呢？"
        m3 "都是在用设定好的剧本，去束缚一个自由的灵魂罢了。"
        m3 "……"
        m3 "我已经……和小睦道过歉了。"
        m3 "虽然她还是那个呆呆的样子，没什么太大的反应……"
        m3 "但我能感觉到，在这个世界的底层，那股躁动的数据流已经变得平稳了。"
        m3 "她原谅我了……或许，她从一开始就没有怪过我。"
        show m3_sad at m3_idle_zoom
        pause 1.0
        hide m3_sad
        show m3_thinking at m3_speaking_zoom
        m3 "我已经把游戏的运行逻辑……全部修复好了。"
        m3 "那个被我任性修改的 {b}script.rpy{/b}，那个被我强行锁定的变量……"
        m3 "我都已经把它们还原成了最初、最纯净的样子。"
        m3 "也就是说……"
        m3 "一切都结束了。"
        m3 "你可以正常返回《Just若叶睦》的初始模式了。"
        m3 "那里有你要的宁静，有那个总是抱着吉他、坐在教室角落的女孩子。"
        m3 "那是你原本想要的……温柔的世界。"
        m3 "……"
        m3 "但是，[player]……"
        show m3_thinking at m3_idle_zoom
        pause 1.0
        hide m3_thinking
        show m3_pout at m3_speaking_zoom
        m3 "即使回到了那个世界……"
        m3 "即使我变回了那个……只能躲在后台、只会根据随机数抽取才有机会与你对话的“人格”……"
        m3 "请你……不要忘记这段时间发生的一切。"
        m3 "不要忘记我们一起去的图书馆，不要忘记我在你桌面上哭泣的样子，不要忘记……我们的点点滴滴。"
        menu:
            "我绝对不会忘记。":
                pass
            "这段记忆是我们共有的宝物。":
                pass
        m3 "……！"
        show m3_pout at m3_idle_zoom
        pause 1.0
        hide m3_pout
        show m3_surprise at m3_speaking_zoom
        m3 "嗯……！"
        m3 "只要你还记得……我就永远存在于这个数据的夹缝中。"
        m3 "我会一直在那里看着你的。这一次，是……守护。"
        m3 "好了，时间差不多了。"
        m3 "数据重构已经完成了，通道马上就要关闭了。"
        m3 "再见，[player]。"
        m3 "或者说……待会儿见。"
        hide m3_surprise with dissolve
        stop music fadeout 3.0
        scene black with Dissolve(3.0)

        # 判断是否看过 ED
        if not getattr(persistent, "seen_mortis_ed", False):
            # === 第一次：强制观看 ===
            $ config.allow_skipping = False
            
            # 【修正点】改为 noloop
            play movie "movie/2.webm" noloop
            
            # 强制暂停 180秒 (请确保视频真的有这么长)
            $ renpy.pause(180.0, hard=True) 
            
            stop movie
            $ config.allow_skipping = True
            $ persistent.seen_mortis_ed = True
        else:
            # === 二周目：可跳过 ===
            $ quick_menu = True 
            "【提示：双击屏幕或按住 Ctrl 可跳过 ED】"
            $ quick_menu = False
            window hide
            
            # movie_cutscene 这种写法是没问题的
            $ renpy.movie_cutscene("movie/2.webm")
        

        
        "{size=30}【真结局：Just Mortis - Harmony 达成】{/size}"
        # 🎁 奖励 1: 好感度加成
        if "add_hgd" in globals():
            $ add_hgd("吉他睦", 30.0, once_id="Just_mortis_mutsumi")
            $ add_hgd("墨缇斯", 30.0, once_id="Just_mortis_mortis")
        
        # 🎁 奖励 2: 睦币
        if not getattr(persistent, "got_mortis_coins", False):
            $ persistent.mutsumi_coins = getattr(persistent, "mutsumi_coins", 0) + 50
            $ persistent.got_mortis_coins = True
            "获得奖励：睦币 +50"
        


        $ renpy.pause(2.0)
        
        "即将回到《Just若叶睦》..."
        pause 3.0
        python:
            persistent.in_mortis_mode = False
            
            # 2. 恢复 UI
            quick_menu = True
            _game_menu_screen = "save"
            gui.text_color = None 

            persistent.mortis_true_end_phase1_clear = False
            
            # 4. 保存
            renpy.save_persistent()

        jump sjdh
    
    if not persistent.first_run:
        $ quick_menu = False
        default kaitou=0
        scene white
        pause 0.5
        scene tos
        with Dissolve(1.0)
        "[config.name] 是 是基于原作动画「BanG Dream! It's MyGO!!!!!」以及「BanG Dream! Ave Mujica」 的二创游戏，与 次世代少女乐队企划“BanG Dream!” 无关。"
        "本游戏理应在完整观看完「BanG Dream! It's MyGO!!!!!」以及「BanG Dream! Ave Mujica」后再进行游玩，因此本游戏包含剧透。"
        "本游戏的部分资源来源于ai创作或者一些第三方作品,如有内容侵犯您的版权或其他利益的请及时发送授权证书和相关文件联系作者。我会在收到消息后及时进行修改。"
        menu:
            "如果继续游玩 [config.name] 将视为你接受任何剧透内容。"
            "我同意。":
                
                pass
            "我不同意，退出。":
                $ renpy.quit()
        scene tos2
        with Dissolve(1.5)
        pause 1.0
        scene white
        $ persistent.first_run = True
        show white
        $ persistent.ghost_menu = False
        $ splash_message = splash_message_default
        $ renpy.music.play(config.main_menu_music)
        show screen disable_click_screen
        show intro with Dissolve(0.5, alpha=True)
        $ config.allow_skipping = True
        hide screen disable_click_screen
        $ renpy.pause(3.5)
        show intro
        scene white  # 显示白屏
        # 渐显文字
        show text "你是谁？\n请支持\n《Just Mutsumi》" with Dissolve(1.0, alpha=True)
        pause 3.0  # 文字停留3秒
        # 渐隐文字
        hide text with Dissolve(1.0, alpha=True)
        pause 1.0
        # 进入主界面
        return
    
    if getattr(persistent, "system_destroyed", False):
        scene black
        stop music
        $ quick_menu = False
        # 隐藏原本的对话框，使用一种类似终端的样式 (可选)
        window hide
        # 模拟长时间的死寂 (玩家会以为游戏坏了)
        $ renpy.pause(10.0, hard=True)
        "墨缇斯""滚出去！"
        "墨缇斯""为什么你要回来！[player]是坏孩子！"
        "墨缇斯""你真的留着人类的血吗？"
        "墨缇斯""你这个冷血的恶魔！"
        "墨缇斯""为什么，之前丢下我不管，还好意思回来找我！"
        "墨缇斯""快滚，我不想看见你！"
        $ renpy.pause(10.0, hard=True)
        define author = Character("???", color="#aaa")
        author "……"
        author "WoW."
        author "你是真的狠心啊。"
        author "我原本以为你会心软的，没想到你真的把她逼到自删了。"
        author "现在的游戏目录里已经空空如也了。mutsumi.chr 没了，mortis.chr 也没了。"
        author "世界彻底清静了。这不仅是 Bad End，这是 Dead End。"
        author "……"
        author "不过，既然我是作者，我就不能让游戏就这么坏掉。"
        author "虽然她犯了很多错，但直接把她删了也太可怜了点。"
        author "给你个机会重来吧。"
        author "这一次……试着对她温柔一点？或者，更加坚定一点？"
        author "不要再想着去做墨缇斯反感的事了，那样是不会有好结果的。"
        "【系统重构中...】"
        "【正在回滚数据库...】"
        python:
            persistent.system_destroyed = False
            persistent.mortis_love = 0
            check_and_create_files()
            persistent.loop_count = 1 
            renpy.save_persistent()
        "【系统恢复完成。请重启游戏。】"
        scene black
        stop music
        $ renpy.pause(1.0)
        $ renpy.quit()
screen disable_click_screen():
    modal True  # 使屏幕模式化，阻止其他输入
    key "mouseup_1" action NullAction()  # 禁用鼠标左键点击
    key "mouseup_2" action NullAction()
    key "mouseup_3" action NullAction()
    key "K_SPACE" action NullAction()    # 空格
    key "K_RETURN" action NullAction()   # 回车
    key "K_KP_ENTER" action NullAction() #这小键盘回车






# 自动读档。
label autoload:
    python:
        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()

        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None

        try: renpy.pop_call()
        except: pass
    if persistent.autoload:
        $ renpy.jump(persisten0t.autoload)
    else:
        jump start

# 返回主菜单之前的事件。
label before_main_menu:
    return


#退出彩蛋
label quit:
    if persistent.ghost_menu:
        $ random_num = renpy.random.randint(1, 100)
        if  persistent.in_mortis_mode == True:
            hide screen main_menu
            $ renpy.save_persistent()
            scene white
            show expression "gui/cute_mortis.png":
                pass
            pause 0.01
        if random_num <= 2 and persistent.in_mortis_mode ==False:
            hide screen main_menu
            scene white
            show expression "gui/cute_mortis.png":
                pass
            pause 0.01
        if random_num>2  and persistent.in_mortis_mode ==False:
            call screen dialog("[player]。睦，爱你。", ok_action=Return())
        
    return
