# ============================================================
# 🎬 制作名单系统 (Credits System v2.1 - With Result Popup)
# ============================================================

# --- 1. 逻辑与数据初始化 ---
default persistent.developer_mode = False
init python:
    # 你的超级后门密钥 (建议搞复杂点)
    DEV_ACCESS_KEY = "11037Oscar0721" 

    # 普通兑换码
    GIFT_CODES = {
        "GreenChoco": 30,
        "Kyuri2026": 30,
        "Zephyria_Yoshino5273": 120,
        "motis_nartiaa8941": 120,
        "Y0ung杨杨杨杨1605": 120,
        "梦溪沈谈7329": 120,
        "XYKerman4098": 120,
        "晓歌的压裙刀6582": 120,
        "叫我苍或者静雨吧2147": 60,
        "圆润の小圆前辈3690": 60,
        "戴数学5812": 60,
        
        
        
    }

    def redeem_code(code_input):
        code = code_input.strip() # 去除首尾空格
        
        # 0. 先关闭输入窗口
        renpy.hide_screen("code_input_popup")

        # 1. 检查是否为空
        if not code:
            show_redemption_result(False, "请输入兑换码", "输入为空")
            return

        # ==========================================
        # 🛠️ 后门逻辑：检查是否是开发者密钥
        # ==========================================
        if code == DEV_ACCESS_KEY:
            # 切换状态 (开启 -> 关闭 / 关闭 -> 开启)
            persistent.developer_mode = not persistent.developer_mode
            renpy.save_persistent()
            
            if persistent.developer_mode:
    
                show_redemption_result(True, "系统限制解除。\nDeveloper Mode: [[ON]", "⚠ 警告 ⚠")
            else:
                show_redemption_result(False, "系统限制恢复。\nDeveloper Mode: [[OFF]", "系统提示")
            
            # 强制刷新一下界面，确保按钮状态更新
            renpy.restart_interaction()
            return
        # ==========================================

        # 2. 普通玩家逻辑：检查是否已领取过
        if code in persistent.redeemed_codes:
            show_redemption_result(False, "这个兑换码已经使用过了哦。", "重复兑换")
            return

        # 3. 检查普通码是否有效
        if code in GIFT_CODES:
            reward = GIFT_CODES[code]
            persistent.mutsumi_coins += reward
            persistent.redeemed_codes.add(code)
            renpy.save_persistent()
            show_redemption_result(True, f"兑换成功！\n已将 {reward} 睦币存入您的账户。", "兑换成功")
        else:
            show_redemption_result(False, "无效的兑换码，请检查拼写。", "兑换失败")

    def show_redemption_result(is_success, msg, title):
        """
        辅助函数：显示结果弹窗
        """
        renpy.show_screen("code_result_popup", is_success=is_success, message=msg, title_text=title)

    # 音乐控制函数 (保持不变)
    def store_current_music():
        store.last_played_music = renpy.music.get_playing(channel='music')
    def restore_last_music():
        if hasattr(store, 'last_played_music') and store.last_played_music:
            renpy.music.play(store.last_played_music, fadein=1.5)
    def safe_play_oscar_theme():
        if renpy.loadable("audio/oscar_theme.mp3"):
            renpy.music.play("audio/oscar_theme.mp3", fadein=1.5)

# --- 变量初始化 ---
default persistent.claimed_dev_gift = False 
default persistent.redeemed_codes = set()

# --- 动画定义 ---
transform credits_master_transform:
    on show:
        alpha 0.0 yoffset 100
        easein_back 1.0 alpha 1.0 yoffset 0
    on hide:
        parallel:
            easeout_quint 0.8 alpha 0.0
        parallel:
            easeout_back 0.8 xoffset 300 zoom 0.8 blur 15

transform pop_up_appear:
    alpha 0.0 zoom 0.8
    linear 0.2 alpha 1.0 zoom 1.0

# ============================================================
# 📱 主界面 Screen
# ============================================================
screen credits_app():
    modal True
    zorder 300
    
    on "show" action [Function(store_current_music), Function(safe_play_oscar_theme)]
    on "hide" action Function(restore_last_music)
    
    fixed:
        at credits_master_transform

        add Solid("#0d120df2")

        frame:
            align (0.5, 0.5)
            xsize 1280 ysize 720
            background Solid("#1a261af2") 
            padding (80, 80)

            vbox:
                vbox:
                    spacing 5
                    text "《Just 若叶睦》制作名单" size 42 color "#FFFFFF" kerning 10 outlines [(3, "#00000088", 1, 1)]
                    text "关于这片温室的一切存证" size 16 color "#779977" kerning 4
                    add Solid("#779977aa") ysize 2 xsize 1120
                
                null height 50

                hbox:
                    spacing 60 
                    
                    # 左侧：头像区
                    vbox:
                        xsize 380
                        spacing 20
                        frame:
                            background Frame(Solid("#77997733"), 4, 4)
                            padding (10, 10)
                            if renpy.loadable("images/phone/oscar_photo.png"):
                                add "images/phone/oscar_photo.png" xsize 360 ysize 360
                            else:
                                add Solid("#222") xsize 360 ysize 360 
                        
                        vbox:
                            xalign 0.5
                            text "缄 默 奥 斯 卡" size 32 color "#FFFFFF" bold True kerning 4
                            text "不知名的独立游戏开发者" size 16 color "#B2C9B2" xalign 0.5

                    # 右侧：信息与按钮区
                    vbox:
                        spacing 25 
                        
                        # --- 按钮区域 ---
                        vbox:
                            spacing 15 

                            # 第一行
                            hbox:
                                spacing 20
                                textbutton "访问 BiliBili":
                                    action OpenURL("https://space.bilibili.com/391616943")
                                    text_size 18 text_color "#FFFFFFCC" text_hover_color "#fb7299"
                                    background Frame(Solid("#ffffff11"), 4, 4)
                                    hover_background Frame(Solid("#fb729922"), 4, 4)
                                    padding (20, 12)

                                textbutton "个人博客":
                                    action OpenURL("https://wakaba.top")
                                    text_size 18 text_color "#FFFFFFCC" text_hover_color "#B2C9B2"
                                    background Frame(Solid("#ffffff11"), 4, 4)
                                    hover_background Frame(Solid("#B2C9B222"), 4, 4)
                                    padding (20, 12)

                            # 第二行
                            hbox:
                                spacing 20
                                
                                # [开发者礼物]
                                if not persistent.claimed_dev_gift:
                                    textbutton "开发者の礼物":
                                        action [
                                            SetField(persistent, "mutsumi_coins", persistent.mutsumi_coins + 100),
                                            SetField(persistent, "claimed_dev_gift", True),
                                            Notify("🎁 叮！发现了开发者的福利！获得 100 睦币")
                                        ]
                                        text_size 18 text_color "#FFFFFFCC" text_hover_color "#ffd700"
                                        background Frame(Solid("#ffffff11"), 4, 4)
                                        hover_background Frame(Solid("#ffd70022"), 4, 4)
                                        padding (20, 12)
                                else:
                                    textbutton "已领取":
                                        action None
                                        text_size 18 text_color "#ffffff44"
                                        background Frame(Solid("#00000033"), 4, 4)
                                        padding (20, 12)

                                # [兑换码按钮]
                                textbutton "礼包兑换":
                                    action Show("code_input_popup")
                                    text_size 18 text_color "#FFFFFFCC" text_hover_color "#00d2ff"
                                    background Frame(Solid("#ffffff11"), 4, 4)
                                    hover_background Frame(Solid("#00d2ff22"), 4, 4) 
                                    padding (20, 12)

                        # --- 职员表 ---
                        viewport:
                            mousewheel True
                            draggable True
                            scrollbars "vertical"
                            xsize 550 ysize 280 
                            
                            vbox:
                                spacing 14
                                $ staff_items = [
                                    ("项目企划", "缄默奥斯卡"),
                                    ("脚本剧情", "缄默奥斯卡"),
                                    ("程序架构", "缄默奥斯卡"),
                                    ("交互逻辑", "缄默奥斯卡"),
                                    ("素材润色", "缄默奥斯卡"),
                                    ("环境渲染", "缄默奥斯卡"),
                                    ("测试排错", "缄默奥斯卡、Stradlin")
                                ]
                                
                                for role, name in staff_items:
                                    hbox:
                                        frame:
                                            xsize 160 background None padding (0,0)
                                            text role size 16 color "#FFFFFF66" yalign 0.5
                                        text name size 22 color "#FFFFFF" yalign 0.5

                        null height 10
                        vbox:
                            spacing 8
                            add Solid("#77997733") ysize 1 xsize 500 
                            text "特别致谢：感谢 北风的猫5306（b站） 和 纯真的志超（b站） 提供的技术支持" size 16 color "#FFFFFF66" italic True

        # --- 彩蛋按钮 ---
        textbutton "X":
            action Show("oscar_trivia_1") 
            align (1.0, 0.0)
            offset (-30, 30)
            text_size 50
            text_color "#ffffff44"
            text_hover_color "#ff4444"

# ============================================================
# ⌨️ 兑换码输入弹窗
# ============================================================
screen code_input_popup():
    modal True
    zorder 350 
    
    default code_input_value = ""
    
    add Solid("#000000aa")
    
    frame:
        at pop_up_appear
        align (0.5, 0.5)
        xsize 500 ysize 300
        background Solid("#1a261a")
        padding (40, 40)
        
        vbox:
            spacing 30
            align (0.5, 0.5)
            
            text "请输入兑换码" size 30 color "#fff" xalign 0.5 bold True
            
            # 输入框
            input:
                value ScreenVariableInputValue("code_input_value")
                length 20 
                # allow 属性已删除，允许输入中文
                xalign 0.5
                color "#ffd700" 
                size 28
            
            add Solid("#ffffff44") ysize 2 xsize 400 xalign 0.5

            hbox:
                spacing 40
                xalign 0.5
                
                # 确认按钮：直接调用 Python 函数
                textbutton "确认兑换":
                    action Function(redeem_code, code_input_value)
                    text_size 22 text_color "#fff"
                    background Frame(Solid("#779977"), 4, 4)
                    hover_background Solid("#5a7a5a")
                    padding (30, 10)
                
                # 取消按钮
                textbutton "取消":
                    action Hide("code_input_popup")
                    text_size 22 text_color "#aaa"
                    padding (30, 10)

# ============================================================
# 🆕 兑换结果弹窗 (新增)
# ============================================================
screen code_result_popup(is_success, message, title_text):
    modal True
    zorder 360 # 比输入框更高
    
    add Solid("#000000aa")
    
    frame:
        at pop_up_appear
        align (0.5, 0.5)
        xsize 500 ysize 300
        background Solid("#1a261a")
        padding (40, 40)
        
        # 装饰性边框，颜色根据成功/失败变化
        if is_success:
            add Solid("#ffd700") xsize 4 ysize 220 align (0.0, 0.5) # 金色左边条
        else:
            add Solid("#ff4444") xsize 4 ysize 220 align (0.0, 0.5) # 红色左边条

        vbox:
            spacing 25
            align (0.5, 0.5)
            xfill True
            
            # 标题
            text title_text:
                size 34 
                color ("#ffd700" if is_success else "#ff4444") # 成功金色，失败红色
                xalign 0.5 
                bold True
            
            # 分割线
            add Solid("#ffffff33") ysize 2 xsize 400 xalign 0.5
            
            # 详细信息
            text message:
                size 22 
                color "#dddddd" 
                xalign 0.5 
                text_align 0.5
                layout "subtitle" # 自动换行
            
            null height 10

            # 关闭按钮
            textbutton "确定":
                action Hide("code_result_popup")
                xalign 0.5
                text_size 22 text_color "#fff"
                # 按钮背景色也随结果变化
                background Frame(Solid(("#779977" if is_success else "#555555")), 4, 4)
                hover_background Solid(("#5a7a5a" if is_success else "#777777"))
                padding (40, 10)

# --- 3. 互动小窗口1 (保持不变) ---
screen oscar_trivia_1():
    modal True
    zorder 310
    add Solid("#000000cc") 

    frame:
        at pop_up_appear
        align (0.5, 0.5)
        xsize 700 ysize 520
        background Solid("#1a261a")
        padding (30, 30)

        vbox:
            spacing 20
            xfill True
            
            frame:
                xsize 640 ysize 280
                background Solid("#00000055")
                if renpy.loadable("images/gacha_1.png"):
                    add "images/gacha_1.png" align (0.5, 0.5)

            text "你知道吗？其实在设定上缄默奥斯卡在「绮丽人偶们的嬉戏招募」中第一个十连就出了素睦。" size 20 color "#FFF" line_spacing 8
            
            null height 10

            textbutton "是吗，为什么告诉我这个.....":
                xalign 0.5
                padding (20, 10)
                background Frame(Solid("#779977aa"), 4, 4)
                hover_background Solid("#4a664a")
                text_size 20
                action [Hide("oscar_trivia_1"), Show("oscar_trivia_2")]

# --- 4. 互动小窗口2 (保持不变) ---
screen oscar_trivia_2():
    $ add_hgd("若叶睦", 2, once_id="creits_oscar_1")
    $ add_hgd("吉他睦", 2, once_id="creits_oscar_2")
    $ add_hgd("墨缇斯", 2, once_id="creits_oscar_3")
    
    modal True
    zorder 320
    add Solid("#000000cc")

    frame:
        at pop_up_appear
        align (0.5, 0.5)
        xsize 700 ysize 520
        background Solid("#1a261a")
        padding (30, 30)

        vbox:
            spacing 20
            xfill True

            frame:
                xsize 640 ysize 280
                background Solid("#00000055")
                if renpy.loadable("images/gacha_2.png"):
                    add "images/gacha_2.png" align (0.5, 0.5)

            text "没什么，只是想让你知道.....还有第二个十连又出了一张素睦，还带了张海希。" size 20 color "#FFF" line_spacing 8

            null height 10

            textbutton ".......":
                xalign 0.5
                padding (40, 10)
                background Frame(Solid("#779977aa"), 4, 4)
                hover_background Solid("#ff4444")
                text_size 20
                action [Hide("oscar_trivia_2"), Hide("credits_app")]