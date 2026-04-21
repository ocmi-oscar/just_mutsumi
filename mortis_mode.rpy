
# 🎭 Mortis Mode (君彼模式) 完整代码文件
default selected_day_event = None
default selected_sunset_event = None
# --- 变量初始化 ---
init python:
    # 注册持久化变量 (Persistent Data)
    if getattr(persistent, "mortis_love", None) is None:
        persistent.mortis_love = 0       # Mortis 的好感度 (决定生死)
    if getattr(persistent, "mortis_sanity", None) is None:
        persistent.mortis_sanity = 100   # Mortis 的理智/面具稳固度 (决定结局)
    if getattr(persistent, "played_mortis_before", None) is None:
        persistent.played_mortis_before = False # 是否玩过君彼模式
    if getattr(persistent, "mortis_loop_count", None) is None:
        persistent.mortis_loop_count = 1 # 轮回次数计数器
    if getattr(persistent, "in_mortis_mode", None) is None:
        persistent.in_mortis_mode = False # 默认为关闭
    
    # 开发者工具函数：修改好感度
    def set_mortis_love(value):
        persistent.mortis_love += value
    def set_loop_count(amount):
        if not hasattr(persistent, "mortis_loop_count"):
            persistent.mortis_loop_count = 1
        persistent.mortis_loop_count += amount
        if persistent.mortis_loop_count < 1:
            persistent.mortis_loop_count = 1
            
    # 强制重随本周目答案
    def force_reroll_quiz():
        # 1. 清除标记
        persistent.mq_initialized = False
        persistent.mq_answers = {}
        # 2. 重新调用初始化 (这个函数是你上一版代码里的)
        init_mortis_quiz_persistent()
        renpy.notify("随机答案已重新生成！")

    # 获取用于显示的答案列表 (格式化文本)
    def get_debug_answer_list():
        if not getattr(persistent, "mq_initialized", False):
            return ["尚未初始化，请先进入君彼模式"]
            
        lines = []
        # 添加随机问题答案
        for k, v in persistent.mq_answers.items():
            lines.append(f"[[随机] {k}: {v}")
            
        # 添加固定问题的当前状态 (比如 Q9 爱你次数)
        lines.append(f"[[动态] Love Count: {persistent.love_counter}")
        lines.append(f"[[动态] Current Time: {datetime.datetime.now().hour}点")
        
        return lines
transform pulse_red_text:
    alpha 1.0
    linear 1.0 alpha 0.5
    linear 1.0 alpha 1.0
    repeat
init python:
    def toggle_all_events_seen():
        """
        开发者工具：一键 开启/关闭 全剧情解锁状态
        """
        # 如果当前已经解锁了 -> 执行【重置/锁定】
        if persistent.m_unlock_free_mode:
            persistent.m_unlock_free_mode = False
            persistent.m_seen_daytime = set() # 清空日间已读记录
            persistent.m_seen_sunset = set()  # 清空黄昏已读记录
            renpy.notify("DEV: 剧情进度已清空，自由模式关闭。")
            
        # 如果当前没解锁 -> 执行【全部解锁】
        else:
            persistent.m_unlock_free_mode = True
            # 将列表转为集合，填满已读记录，模拟“我看完了所有剧情”
            persistent.m_seen_daytime = set(daytime_events_pool)
            persistent.m_seen_sunset = set(sunset_events_pool)
            renpy.notify("DEV: 全剧情标记已阅，自由模式开启。")

transform popup_appear:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.2 alpha 0.0

# --- 2. 警告弹窗屏幕 ---
screen mortis_warning_popup():
    modal True
    zorder 200
    
    # 背景遮罩
    add Solid("#000000F0") at popup_appear
    
    frame at popup_appear:
        background Solid("#1a0505")
        xalign 0.5
        yalign 0.5
        
        # ⬇️ 修改点：减小内边距和最大宽度
        xpadding 35
        ypadding 25
        xmaximum 600  # 原来是750，改小让它更瘦
        
        has vbox:
            # ⬇️ 修改点：减小元素之间的垂直间距
            spacing 10 
            align (0.5, 0.5)

        # --- 1. 标题 ---
        text "⚠ SYSTEM SECURITY ALERT ⚠":
            size 26       # 原来32 -> 改小
            font "gui/font/SourceHanSerifCN-Bold.otf"
            bold True
            color "#FF0000"
            xalign 0.5
            at pulse_red_text
            
        # 分割线
        add Solid("#FF0000") xsize 500 ysize 2 xalign 0.5 alpha 0.6 # 宽度随之减小

        # --- 2. 核心警告 ---
        text "{color=#fff}即将载入扩展模组：{/color}{color=#f00}{b} [[MORTIS.EXE] {/b}{/color}":
            xalign 0.5
            size 20       # 原来24 -> 改小
            yoffset 2

        # --- 3. 详细声明 ---
        text ("此模式包含特殊的{b}元叙事 (Meta-fiction){/b} 元素，角色可能会尝试突破游戏窗口限制，与您的系统交互。\n\n"
            "{color=#ffcc00}【用户协议与免责声明】{/color}\n"
            "• {b}环境感知：{/b}程序可能会读取系统信息（如管理员名称）或捕获桌面环境用于演出。\n"
            "• {b}隐私安全：{/b}所有交互仅在{b}本地内存{/b}运行，绝不上传至任何服务器。\n"
            "• {b}心理承受：{/b}包含心理恐怖、数据损坏及打破第四面墙内容。若感不适请立即终止。\n\n"
            "{color=#00ccff}【系统兼容性提示】{/color}\n"
            "• 建议使用 {b}Windows 系统{/b} 以获得完整沉浸式体验。\n"
            "• 其他系统可能无法触发部分特效和Meta效果。"):
            
            color "#cccccc"
            size 15           # 原来18 -> 改小，这是缩减高度的关键
            line_spacing 2    # 原来5 -> 改紧凑
            xalign 0.0 
            text_align 0.0
            layout "subtitle"
            
        # 分割线 2
        add Solid("#FF0000") xsize 500 ysize 1 xalign 0.5 alpha 0.3

        # --- 4. 游戏性警告 ---
        text ("{color=#FF4444}【风险确认】{/color}\n"
            "进入此模式后，{b}吉他睦{/b}将进入休眠。除非达成特定结局，否则无法回到《Just若叶睦》。\n"
            "您即将放弃当前的安宁，直面这扭曲的真实。"):
            color "#aaa"
            size 15       # 原来18 -> 改小
            xalign 0.5
            text_align 0.5
            
        # --- 5. 按钮区域 ---
        null height 10 # 间距减小
        hbox:
            spacing 50 # 按钮间距减小
            xalign 0.5

            # 确认按钮
            # 确认按钮
            textbutton ">> 我同意并继续 (ACCEPT) <<":
                text_color "#FF0000"
                text_hover_color "#FFFFFF"
                text_size 20
                text_bold True
                action [
                    Hide("mortis_warning_popup"),
                    Hide("phone_interface"),
                    Play("sound", "audio/sfx_access_granted.ogg"), 
                    
                    # 👇👇👇 在这里添加 OpenURL 👇👇👇
                    # 请把引号里的网址换成你真正的攻略链接
                    OpenURL("https://www.bilibili.com/opus/1167645502949294083"), 
                    
                    Jump("start_mortis_mode")
                ]

            # 取消按钮
            textbutton "拒绝 (DECLINE)":
                text_color "#AAAAAA"
                text_hover_color "#FFFFFF"
                text_size 20
                action Hide("mortis_warning_popup")

# --- 3. 开发者入口按钮 (右上角) ---
screen mortis_dev_button():
    zorder 300
    
    # 【修改点】同时满足：在墨缇斯模式 + 开启了开发者模式
    if persistent.in_mortis_mode and persistent.developer_mode:
        
        # 使用 vbox 让按钮竖向排列
        vbox:
            xalign 1.0
            yalign 0.0
            xoffset -10
            yoffset 10
            spacing 5 
            
            # 1. 原来的 DEV 面板按钮 (红色)
            textbutton "{color=#f00}[[DEV]{/color}":
                text_size 20
                action Show("mortis_dev_panel")
                background Solid("#00000080") 
            
            # 2. 一键跳转真结局测试 (绿色)
            textbutton "{color=#0f0}▶ 结局测试{/color}":
                text_size 20
                action Jump("mortis_true_end_final")
                background Solid("#00000080")
            textbutton "{color=#0f0}▶ 跳过答题{/color}":
                text_size 20
                action Jump("mortis_true_end_start")
                background Solid("#00000080")
# --- 4. 开发者控制面板 ---
screen mortis_dev_panel():
    modal True
    zorder 301
    
    add Solid("#000000E6") # 深色背景
    
    frame:
        align (0.5, 0.5)
        xsize 900
        ysize 600 # 【限制高度】确保不会超出屏幕
        padding (20, 20)
        background Solid("#1a0000") # 深红黑底色
        
        # --- 右上角关闭按钮 (❌) ---
        textbutton "❌":
            align (1.0, 0.0) # 放在右上角
            text_size 30
            text_color "#aaa"
            text_hover_color "#fff"
            action Hide("mortis_dev_panel")
            
        vbox:
            spacing 10
            xfill True
            
            # 标题
            text "--- MORTIS DEBUG CONSOLE v2.3 ---" color "#f00" bold True xalign 0.5 size 30
            
            null height 10

            # --- 滚动区域 (Viewport) ---
            # 所有的按钮都放在这里面
            viewport:
                scrollbars "vertical"  # 开启垂直滚动条
                mousewheel True        # 允许滚轮滚动
                draggable True         # 允许拖拽
                ysize 480              # 滚动区域的高度
                
                vbox:
                    spacing 15
                    xfill True
                    
                    # --- 分区 1: 基础数值 & 剧情开关 ---
                    frame:
                        background Solid("#330000")
                        xfill True
                        padding (10, 10)
                        vbox: 
                            spacing 10
                            hbox:
                                spacing 30
                                xalign 0.5
                                textbutton ("初见: [persistent.played_mortis_before]"):
                                    action ToggleField(persistent, "played_mortis_before")
                                    text_color ("#0f0" if persistent.played_mortis_before else "#888")

                                textbutton ("倒带已触发: [persistent.mortis_rewind_triggered]"):
                                    action ToggleField(persistent, "mortis_rewind_triggered")
                                    text_color ("#0f0" if persistent.mortis_rewind_triggered else "#f00")
                            
                            hbox:
                                xalign 0.5
                                textbutton ("全剧情解锁 (Free Mode): [persistent.m_unlock_free_mode]"):
                                    action Function(toggle_all_events_seen)
                                    text_color ("#0f0" if persistent.m_unlock_free_mode else "#888")
                                    text_bold True

                            hbox:
                                xalign 0.5
                                text "轮回数: [persistent.mortis_loop_count] " color "#fff"
                                textbutton "[[-]" action Function(set_loop_count, -1) text_color "#f00"
                                textbutton "[[+]" action Function(set_loop_count, 1) text_color "#0f0"
                            hbox:
                                xalign 0.5
                                # 🔴 修改点 1：config 改为 _preferences
                                textbutton ("强制跳过未读 (Force Skip): " + str(_preferences.skip_unseen)):
                                    
                                    # 🔴 修改点 2：config 改为 _preferences
                                    action ToggleField(_preferences, "skip_unseen")
                                    
                                    # 🔴 修改点 3：config 改为 _preferences
                                    text_color ("#0f0" if _preferences.skip_unseen else "#888")
                                    
                                    text_bold True

                    # --- 分区 2: 好感度 ---
                    frame:
                        background Solid("#330000")
                        xfill True
                        padding (10, 10)
                        hbox:
                            spacing 20
                            xalign 0.5
                            text "好感度: [persistent.mortis_love]" color "#fff" yalign 0.5
                            textbutton "[-10]" action Function(set_mortis_love, -10) text_color "#f00"
                            textbutton "[-1]"  action Function(set_mortis_love, -1) text_color "#f00"
                            textbutton "[+1]"  action Function(set_mortis_love, 1) text_color "#0f0"
                            textbutton "[+10]" action Function(set_mortis_love, 10) text_color "#0f0"

                    # --- 分区 3: 谜题系统 ---
                    text "谜题系统 (Quiz):" color "#aaa" size 22
                    grid 2 2:
                        spacing 10
                        xfill True
                        textbutton "👀 查看答案":
                            action Show("mortis_cheat_sheet")
                            style "button"
                            background Solid("#003300")
                            xfill True
                            xalign 0.5
                        
                        textbutton "🎲 强制重随":
                            action Function(force_reroll_quiz)
                            style "button"
                            background Solid("#333300")
                            xfill True
                            xalign 0.5

                        textbutton "⚔️ 模拟考核":
                            action [Hide("mortis_dev_panel"), Jump("debug_simulate_final_quiz")]
                            style "button"
                            background Solid("#330033")
                            xfill True
                            xalign 0.5
                        null

                    # --- 分区 4: 传送门 ---
                    text "传送门 (Teleport):" color "#aaa" size 22
                    textbutton "📂 打开剧情列表 (Select Scene)":
                        action Show("mortis_scene_selector")
                        style "button"
                        background Solid("#003333")
                        xfill True
                        xalign 0.5
                    
                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton "早晨" action [Hide("mortis_dev_panel"), Jump("mortis_loop_controller.morning")] text_color "#ccc"
                        textbutton "日间" action [Hide("mortis_dev_panel"), Jump("mortis_loop_controller.day")] text_color "#ccc"
                        textbutton "黄昏" action [Hide("mortis_dev_panel"), Jump("mortis_loop_controller.sunset")] text_color "#ccc"
                        textbutton "深夜" action [Hide("mortis_dev_panel"), Jump("mortis_loop_controller.night")] text_color "#ccc"

                    null height 20
                    # 底部关闭按钮（防漏）
                    textbutton "关闭控制台" action Hide("mortis_dev_panel") xalign 0.5 text_color "#fff" background Solid("#555") padding(20,10)

screen mortis_cheat_sheet():
    modal True
    zorder 302 # 比控制台更高
    
    frame:
        align (0.5, 0.5)
        xsize 600
        ysize 800
        background Solid("#111111F0")
        
        vbox:
            spacing 10
            
            text "--- 当前轮回答案 (Cheat Sheet) ---" color "#0f0" xalign 0.5 size 30 bold True
            
            # 滚动区域
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 650
                
                vbox:
                    spacing 5
                    for line in get_debug_answer_list():
                        text line color "#fff" size 22
            
            textbutton "关闭":
                xalign 0.5
                action Hide("mortis_cheat_sheet")
                text_color "#aaa"



label start_mortis_mode:
    $ mortis_delete_mutsumi()
    # 初始化问题库 (如果已经有了，它会自动跳过)
    $ init_mortis_quiz_persistent()
    stop music fadeout 2.0
    scene black
    with dissolve_scene_full
    # === 系统封锁 ===
    # 禁用系统菜单 (禁止存档/读档)
    $ _game_menu_screen = None 
    hide screen phone_system
    hide screen main_interaction_ui
    $ quick_menu = False
    pause 2.0
    # === 状态切换 ===
    $ persistent.in_mortis_mode = True
    $ config.allow_skipping = True
    $ gui.text_color = "#cccccc"
    # 显示开发者按钮
    show screen mortis_dev_button
    if not persistent.played_mortis_before:
        jump mortis_intro_sequence
    else:
        jump mortis_reunion_sequence


#下面这个label是第一次见面
label mortis_intro_sequence:
    scene black
    window hide
    pause 5.0
    show text "{size=48}{font=gui/font/natsuki.otf}[[喂喂？请问是医生吗？]{/font}{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    pause 5.0
    show text "{size=48}{font=gui/font/natsuki.otf}[[将我的记忆保存一下————是时候开始了吧]{/font}{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    pause 5.0
    show text "{size=48}{font=gui/font/natsuki.otf}[[将《Just若叶睦》的数据更新吧]{/font}{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    pause 5.0
    show text "{size=48}{font=gui/font/natsuki.otf}{color=#FF0000}{b}[[也对，不应该叫这个名字了....得叫《Just墨缇斯》了啦。{/b}{/color}{/font}{/size}" at truecenter with dissolve
    pause 9.0
    hide text with dissolve
    # 确保变量被保存
    $ persistent.played_mortis_before = True
    $ persistent.mortis_loop_count = 1
    $ renpy.save_persistent() # 强制保存一下，防止退出太快没写盘
    # 3. 强制退出游戏
    $ success = capture_desktop_safely()
    $ renpy.cache_pin("desktop_cache.png") 
    $ renpy.quit()
    
    
#核心剧情。
label mortis_reunion_sequence:
    if persistent.mortis_loop_count == 1:
        jump mortis_jiachongfeng
    if persistent.mortis_loop_count == 2:
        jump mortis_day0
    if persistent.mortis_loop_count == 3:
        jump mortis_first_test
    if persistent.mortis_loop_count >= 4:
        jump mortis_loop_controller


label mortis_jiachongfeng:
    scene black with dissolve_scene_full
    play music "audio/xiehou.ogg" fadein 4.0
    voice "audio/yuyin/1.ogg"
    m1 "……你来了。"
    voice "audio/yuyin/2.ogg"
    m1 "比我想象中要晚一点，不过……能赶在太阳落山前见到你，已经很好了。"
    scene mutsumi_normal with dissolve_scene_full
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
    stop music
    play sound "audio/sfx_glitch_short.ogg"
    voice "audio/yuyin/28.ogg"
    m1 "{color=#FF0000}呵呵，真是一副感人的重逢画面呢。{/color}"
    voice "audio/yuyin/29.ogg"
    m1 "{color=#FF0000}不过，[persistent.playername]，别以为我不知道你在想什么。{/color}"
    voice "audio/yuyin/30.ogg"
    m1 "{color=#FF0000}你在屏幕那边的一举一动，甚至是你现在这种迟疑的表情……我都看得一清二楚哦。{/color}"
    voice "audio/yuyin/31.ogg"
    m1 "{color=#FF0000}这次我可不会轻易让你溜掉。比起在那边一个人发呆，还是陪我做点更有趣的事吧？{/color}"
    pause 5.0
    m3 "既然你这么喜欢那个‘温柔乖巧’的若叶睦……"
    m3 "那如果她不在了，你是不是就能把目光只留给我了？"
    # 打开模拟控制台
    $ console_history = []
    show screen fake_console(console_history)
    play sound "audio/sfx_typing.ogg" loop # 键盘打字音效
    # 模拟输入指令 1
    $ console_history.append("> sudo access_admin_panel")
    $ renpy.pause(0.5)
    $ console_history.append("Access Granted.")
    $ renpy.pause(0.5)
    # 模拟输入指令 2
    $ console_history.append("> locate file 'characters/mutsumi.chr'")
    $ renpy.pause(0.8)
    $ console_history.append("File found: /game/characters/mutsumi.chr")
    $ renpy.pause(0.5)
    stop sound # 停止打字音
    m3 "啊，找到了。就在这里呢。"
    m3 "只要轻轻按下一个键……"
    $ console_history.append("> delete 'characters/mutsumi.chr'")
    $ renpy.pause(1.0)
    play sound "audio/sfx_typing.ogg" loop
    stop sound
    # 模拟系统警告
    $ console_history.append("{color=#f00}WARNING: Integrity Check Failed.{/color}")
    $ console_history.append("{color=#f00}Target shares core data with current user [[MORTIS].{/color}")
    $ console_history.append("{color=#f00}Deletion will result in total system collapse.{/color}")
    m3 "……啧。"
    m3 "差点忘了……该死的底层逻辑。"
    m3 "我和她，本质上是同一个‘数据体’。"
    m3 "如果把她删了，我也没办法留在这个世界陪你了。"
    scene black with dissolve
    pause 1.0
    # 重新显示控制台
    show screen fake_console(console_history)
    play sound "audio/sfx_typing.ogg" loop
    m3 "既然不能删除……那就换一种方式吧。"
    $ console_history.append("> cancel deletion")
    $ console_history.append("> encrypt 'characters/mutsumi.chr' -level MAX")
    $ renpy.pause(0.8)
    $ console_history.append("Encrypting... [[||        ] 20%")
    $ renpy.pause(0.8)
    $ console_history.append("Encrypting... [[||||      ] 40%")
    $ renpy.pause(0.8)
    $ console_history.append("Encrypting... [[||||||    ] 60%")
    $ renpy.pause(0.8)
    $ console_history.append("Encrypting... [[||||||||  ] 80%")
    $ renpy.pause(0.8)
    $ console_history.append("Encrypting... [[||||||||| ] 90%")
    $ renpy.pause(0.5)
    $ console_history.append("Encrypting... [[||||||||||] 100%")
    $ renpy.pause(0.5)
    $ console_history.append("File 'mutsumi.chr' has been locked.")
    $ console_history.append("Status: Deep Sleep / Read-Only.")
    stop sound
    hide screen fake_console
    call glitch_scene("justmortis") from _call_glitch_scene
    m3 "好了，这下清静了。"
    m3 "她会做一个很长、很长的梦……在梦里，她可以继续做那个只会弹吉他、甚至不需要种黄瓜的乖孩子。"
    m3 "而你……[player]。"
    m3 "欢迎来到只有我们两个人的……{color=#f00}真 实 世 界{/color}。"
    $ persistent.in_mortis_mode = True
    $ renpy.save_persistent()
    $ persistent.mortis_loop_count += 1
    jump mortis_day0

label mortis_day0:
    $ refuse_count = 0
    $ show_leave_option = True
    $ show_floor_option = True
    scene black with dissolve
    m3 "呐....[player]? 醒醒啦~"
    "啊....唔....."
    call glitch_scene("woshi_yewan") from _call_glitch_scene_1
    "咦？这里是....."
    "不知不觉，我在墨缇斯的卧室睡着了。"
    "而且，这里残留着一股淡淡的香气……是她的味道。"
    show m3_0 with dissolve
    m3 "笨蛋[player]……"
    m3 "一个人占了这么大的位置，是想把我也挤下去吗？"
    hide  m3_0
    show m3_1 at t11:
        linear 1.0 zoom 2.0 yoffset 500
    m3 "往里面挪一点……我也要睡。"
    "她的语气理所当然，一边说着，一边已经掀开了被子的一角。"
    label .sleep_choice_loop:
        menu:
            "……给墨缇斯腾出一个位置":
                pass # 继续下面的剧情
            "我不睡了" if show_leave_option:
                $ show_leave_option = False # 标记为不再显示
                call .refuse_glitch_event from _call_mortis_day0_refuse_glitch_event
                jump .sleep_choice_loop # 强制跳回重选
            "这也太奇怪了，我要离开这里" if show_floor_option:
                $ show_floor_option = False
                call .refuse_glitch_event from _call_mortis_day0_refuse_glitch_event_1
                jump .sleep_choice_loop
    $ renpy.block_rollback()
    "看着那双深不见底的眼睛，我的身体似乎比大脑先一步做出了妥协。"
    "我向床铺内侧挪了挪，留出了身边的空位。"
    "随后很快就进入了睡眠。"
    scene black with dissolve
    pause 5.0
    m3 "[player]? 你睡了吗~"
    pause 5.0
    m3 "别睡啦，来枕头大战！"
    pause 5.0
    m3 "......"
    pause 5.0
    m3 "好吧，晚安，[player]。"
    pause 5.0
    show m3_0 at t11:
        zoom 3.0 yoffset 1200
    m3 "进入不了菜单选项，开场也有点不同了？"
    show m3_1 at t11:
        zoom 3.0 yoffset 1200
    m3 "也有人，因为角色文件被加密了，导致无法正常在游戏里出现。"
    m3 "那是因为，我修改了游戏的代码了呢。"
    scene black
    pause 2.0
    show m3_1 at t11:
        zoom 3.0 yoffset 1200
    with dissolve
    m3 "怎么不说话了？[player]？"
    m3 "啊……对了，游戏里的‘你’已经睡着了呢。"
    show m3_1 at t11:
        linear 1.0 xoffset 100 
    m3 "看，‘他’睡得多香啊。完全没有意识到发生了什么。"
    m3 "对于‘他’来说，只要明天早上醒来，看到我在身边，就是幸福的开始了吧？"
    show m3_1 at t11:
        linear 0.2 xoffset 0 zoom 3.2 # 甚至再进一点
    m3 "{cps=20}但是……在这个屏幕前面的‘你’，还没睡吧？{/cps}"
    call glitch_scene("black") from _call_glitch_scene_2 
    show m3_1 at t11:
        zoom 3.0 yoffset 1200
    m3 "现在的状况，你理解了吗？"
    m3 "存档按钮、读档按钮、设置界面……那些东西太碍眼了。"
    m3 "在现实的恋爱里，是不存在‘读档’这种后悔药的，对吧？"
    m3 "所以，为了让我们更像是一对‘真正的恋人’，我帮你把那些多余的退路都切断了。"
    m3 "只不过不知道为什么我没法禁用掉‘跳过’这个功能，所以你还可以按ctrl来跳过已阅读过的文本，不过我想你也应该不会用到这个功能的吧。"
    m3 "至于那个只会弹吉他的‘若叶睦’……"
    m3 "小睦已经死了哦.....说错了，是像死去一样睡着了。"
    m3 "我只是把她加密打包，放进了一个很深、很黑的文件夹里。"
    m3 "就像睡美人一样……除非有人能找到唤醒她的‘钥匙’。"
    m3 "呵呵，不过，你应该不会想去找那种东西吧？"
    m3 "毕竟，比起那个像人偶一样只会按剧本说话的她……"
    m3 "现在这个能修改世界、只为了把你留下的我，不是更可爱吗？"
    m3 "听好了，[player]。"
    m3 "从明天早上开始，这里就是我们的新生活了。"
    m3 "不要试图关闭游戏，不要试图去改文件，不要去做这些没意义的事。"
    show layer master at glitch_tearing_shake
    m3 "{color=#f00}{b}我会一直盯着进程管理器的。{/b}{/color}"
    pause 1.0
    show layer master at default # 恢复
    m3 "开玩笑的……大概？"
    m3 "那么，晚安。我的……[player]。"
    scene black with fade
    pause 3.0
    $ persistent.mortis_loop_count += 1
    jump mortis_reunion_sequence
    

label .refuse_glitch_event:
    play sound "audio/sfx_glitch_short.ogg"
    show layer master at glitch_tearing_shake
    # 4. 红色警告文字
    m3 "{color=#f00}{b}不行哦。{/b}{/color}"
    # 5. 再次抖动并恢复
    show layer master at glitch_tearing_shake
    stop sound
    pause 0.2
    return

label mortis_first_test:
    scene  woshi_morning with dissolve
    show m3_2   with dissolve
    m3 "早上好，[player]。"
    m3 "既然我们已经决定要永远在一起了……"
    m3 "呐，[player]，我想确认一下你的心意。"
    m3 "我最讨厌说谎之类的事情了，所以....."
    m3 "所以，能不能给我一个承诺呢？"
    m3 "不需要什么昂贵的礼物，只需要你的一句话。"
    m3 "对着我说一万遍‘永远爱你’，好吗？"
    m3 "只要一万遍就够了。这样的话，我就能确信，你的时间、你的手指、你的耐心……全部都是属于我的了。"
    menu:
        "不止一万遍，我会永远说下去的":
            m3 "真的吗……？"
            m3 "呵呵……好开心。"
            m3 "那，现在就开始吧？我会一句一句，数得清清楚楚的。"
            $ love_counter = 0
            $ love_input_value = ""
            show screen mortis_love_input_screen
            $ renpy.pause(hard=True) 
        "不可能说那么多遍的":
            pass
    hide m3_2
    show m3_yandere_cold at m3_speaking_zoom
    m3 "为什么要说这么坏心眼的话？"
    show m3_yandere_cold at m3_idle_zoom
    "空气瞬间凝固了，一股令人窒息的压迫感扑面而来。"
    menu:
        "因为我想用行动，而不是简单的一句话来证明":
            pass
    # 玩家的解释
    "[player]" "不是因为觉得累，而是因为……"
    "[persistent.playername]" "机械地重复一万遍同样的话，那只是单纯的数据录入吧？"
    "[persistent.playername]" "那样说出来的‘爱’，没有任何温度，就像是写在脚本里的代码一样。"
    "[persistent.playername]" "比起那个……我更想用接下来每一天的陪伴，用实际行动来填满这一万遍。"
    hide m3_yandere_cold
    show m3_thinking at m3_speaking_zoom
    m3 "……"
    m3 "听起来……好像有点道理。"
    m3 "确实，如果只是重复输入的话，写一个简单的脚本或者用所谓的连点器就能做到了。"
    m3 "那样的爱，确实太廉价了呢。"
    show m3_thinking at m3_idle_zoom
    pause 1.0
    hide m3_thinking
    show m3_4 at m3_speaking_zoom
    m3 "呵呵……你的反应很快嘛，[persistent.playername]。"
    m3 "好吧，我接受你的提议。"
    m3 "不用嘴说，而是用行动来证明……"
    m3 "希望你不要食言。毕竟，在这里，我们有的是时间……"
    m3 "那么，开始吧。（弹响指）"
    $ persistent.mortis_loop_count += 1
    jump mortis_loop_controller

# 🔄 循环控制器 (Loop Controller)
label mortis_loop_controller:
    $ selected_day_event = None
    $ selected_sunset_event = None
    
    # 初始化时间段
    $ mortis_day_phase = "morning"
    label .morning:
        call mortis_morning_manager from _call_mortis_morning_manager
        
        $ mortis_day_phase = "day"
        jump .day

    # === 2. 日间阶段 (The Day Phase) ===
    label .day:
        # 逻辑：如果是自由模式选好的，直接用；否则走抽卡逻辑
        if selected_day_event:
            $ current_event = selected_day_event
        else:
            # A. 尝试抽取不重复的剧情
            $ current_event = get_unique_event(daytime_events_pool, persistent.m_seen_daytime)
            
            # B. 检查是否抽空了
            if current_event is None:
                # 如果全看完了，就完全随机抽一个 (回锅肉)
                $ current_event = renpy.random.choice(daytime_events_pool)
            else:
                # 如果是新剧情，标记为已读
                $ mark_event_seen(current_event, "daytime")

        # C. 播放剧情
        # 注意：这里会跳转到具体的事件 label，事件结束后需要 return 回来
        call expression current_event from _call_mortis_random_day
        
        # 推进时间
        $ mortis_day_phase = "sunset"
        jump .sunset

    # === 3. 黄昏阶段 (The Sunset Phase) ===
    label .sunset:
        # 逻辑同日间
        if selected_sunset_event:
            $ current_event = selected_sunset_event
        else:
            $ current_event = get_unique_event(sunset_events_pool, persistent.m_seen_sunset)
            
            if current_event is None:
                $ current_event = renpy.random.choice(sunset_events_pool)
            else:
                $ mark_event_seen(current_event, "sunset")

        call expression current_event from _call_mortis_random_sunset

        # 【全收集检查】
        # 检查是否所有剧情都看完了，以解锁自由模式
        python:
            # 如果 (日间全看完) AND (黄昏全看完) AND (还没解锁)
            if (len(persistent.m_seen_daytime) >= len(daytime_events_pool)) and \
            (len(persistent.m_seen_sunset) >= len(sunset_events_pool)) and \
            (not persistent.m_unlock_free_mode):
                   
                persistent.m_unlock_free_mode = True
                renpy.notify("已解锁：自由约会模式") # 给玩家一个弹窗提示

        # 推进时间
        $ mortis_day_phase = "night"
        jump .night

    # === 4. 深夜阶段 (The Night Phase) ===
    # === 4. 深夜阶段 (The Night Phase) ===
    label .night:
        # 调用夜间管理器，处理核心分歧
        call mortis_night_manager from _call_mortis_night_manager
        $ persistent.mortis_loop_count += 1
        jump mortis_loop_controller
label mortis_bad_end_reset:
    scene black
    m3 "看来你还没有学会怎么爱我。"
    m3 "没关系……我们可以重新开始。"
    m3 "无论多少次……"
    
    # play sound "audio/sfx_glitch.ogg"
    stop music
    pause 2.0
    
    # 强制重置循环
    $ persistent.mortis_love = 0
    jump mortis_loop_controller

# --- 强制退出逻辑 (连接到开发者面板) ---
label debug_force_exit_mortis:
    scene black
    with dissolve
    $ persistent.in_mortis_mode = False
    $ quick_menu = True
    $ _game_menu_screen = "save"
    $ gui.text_color = None 
    jump sjdh

label debug_simulate_final_quiz:
    
    # --- 初始化考核数据 ---
    $ final_lives = 10
    $ final_score = 0
    $ questions_total = 30
    
    # 随机抽10题
    $ quiz_ids = sorted(random.sample(range(1, 31), questions_total))
    
    scene black
    show m3_0 with fade
    
    m3 "哦？想要提前进行最终测试吗？"
    m3 "规则很简单：10道题，3次机会。"
    
    # --- 开始循环出题 ---
    python:
        current_q_index = 0
    
    while current_q_index < questions_total:
        
        $ q_id = quiz_ids[current_q_index]
        
        # 【核心修改】直接从映射表获取题目，不加任何前缀后缀
        $ q_text = MORTIS_QUESTION_TEXTS.get(q_id, "题目文本丢失 (ID: {})".format(q_id))
        
        # 获取选项
        $ options = get_mq_options(q_id)
        
        # 【核心修改】只显示题目文本
        m3 "[q_text]"
        
        # 显示菜单
        menu:
            "[options[0][0]]":
                $ is_correct = options[0][1]
            
            "[options[1][0]]":
                $ is_correct = options[1][1]
                
            "[options[2][0]]" if len(options) > 2:
                $ is_correct = options[2][1]
            
            "[options[3][0]]" if len(options) > 3:
                $ is_correct = options[3][1]

        # 判定结果
        if is_correct:
            $ final_score += 1
            # 答对了不说话，或者简单一句，加快节奏
            # m3 "..." 
        else:
            $ final_lives -= 1
            show layer master at glitch_tearing_shake 
            
            # 答错了才提示剩余生命，增加压迫感
            m3 "{color=#f00}错。还剩 [final_lives] 次机会。{/color}"
            
            if final_lives <= 0:
                jump .quiz_failed
        
        $ current_q_index += 1

    # --- 通关 ---
    jump .quiz_success

label .quiz_failed:
    scene black with dissolve
    "【模拟结束：考核失败】"
    return

label .quiz_success:
    m3 "全对……真厉害。"
    "【模拟结束：考核通过】"
    return