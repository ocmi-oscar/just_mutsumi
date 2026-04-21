init python:
    import os
    import time
    
    # 定义截图存储路径
    screenshot_path = os.path.join(config.gamedir, "desktop_cache.png")

    def capture_desktop_safely():
        """
        尝试截取桌面（仅主屏幕）。
        """
        # 1. 移动端直接跳过
        if renpy.android or renpy.ios:
            return False

        try:
            from mss import mss
        except ImportError:
            renpy.notify("错误：未找到 mss 库")
            return False

        try:
            # --- 第一步：最小化窗口 ---
            import pygame_sdl2 as pygame
            pygame.display.iconify() 

            time.sleep(0.5) 
            
            # --- 第二步：截取主屏幕 ---
            with mss() as sct:
                # mon=1 通常指主显示器
                # 这样就能解决双屏截成长条图的问题
                sct.shot(mon=1, output=screenshot_path)
            _preferences.fullscreen = True
            
            return True

        except Exception as e:
            # 调试用：打印错误
            print("Screenshot Error: " + str(e))
            return False

# 定义图像 (使用 ConditionSwitch 或者直接引用，为了测试简单直接引用)
image test_desktop_bg = "desktop_cache.png"
image desktop_bg:
    "desktop_cache.png"
    size(1280,720)
label meta_crash_event:

    # --- 1. 伪造报错 ---
    stop music
    scene black
    with vpunch # 震动一下
    "系统" "检测到致命错误。数据完整性受损。"
    "系统" "正在尝试恢复... 失败。"
    "系统" "将在 5 秒后强制关闭程序。"
    # --- 2. 倒计时 ---
    $ count = 5
    while count > 0:
        "系统" "倒计时: [count]"
        $ count -= 1
        pause 1.0
    $ _preferences.fullscreen = True
    scene desktop_bg
    show screen disable_click_screen
    $ renpy.pause(3.0, hard=True)
    show desktop_bg at shake_screen # 桌面震动
    
    $ renpy.pause(1.0, hard=True)
    
    show desktop_bg at shake_screen
    $ renpy.pause(1.0, hard=True)
    with vpunch
    
    # 墨缇斯从裂缝中出现
    show m3_yandere_cold at center with dissolve
    
    hide screen disable_click_screen
    
    m3 "……抓到你了。"
    m3 "你以为躲到这个叫做‘桌面’的地方，我就找不到你了吗？"
    m3 "别想逃。"

    # 后续剧情...
    return
label test_mss_feature:
    
    scene black
    "准备开始测试桌面截图功能..."
    "请注意：接下来的几秒钟，游戏窗口会最小化。"
    
    menu:
        "开始测试":
            pass
        "取消":
            return

    # 执行截图
    $ success = capture_desktop_safely()
    
    # 强制刷新一下图片缓存 (因为文件名没变，Ren'Py 可能会用旧图)
    $ renpy.cache_pin("desktop_cache.png") 

    if success:
        # 显示截图
        scene test_desktop_bg
        "测试成功！"
        "如果你看到的是你的桌面（或者是桌面的无限套娃），那就说明功能正常！"
        jump meta_crash_event
    else:
        # 显示失败
        "测试失败。"
        "请按 Shift+O 查看控制台报错。"
        
    return


init python:
    import os
    import shutil
    import random
    from renpy import config

    # =========================================================
    # 🔑 定义真正的“若叶睦”文件里的密钥内容
    # =========================================================
    # ⚠️ 重要：你在制作压缩包里的 mutsumi.chr 时，
    # 必须把下面这行字符串一字不差地写进文本文档里！
    REAL_MUTSUMI_KEY = "SYSTEM_ID: MUTSUMI_WAKABA_RECOVERY_KEY_9527"

    # =========================================================
    # 📂 路径管理工具
    # =========================================================
    
    def get_char_dir():
        """获取 characters 文件夹的绝对路径"""
        target_dir = os.path.join(config.basedir, "characters")
        
        # 如果文件夹不存在，自动创建（防止报错）
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except:
                pass
        return target_dir

    def get_game_root():
        """获取游戏根目录（用于放置压缩包）"""
        return config.basedir

    def mortis_delete_mutsumi():
        """将 mutsumi.chr 从文件夹中移除"""
        char_path = os.path.join(get_char_dir(), "mutsumi.chr")
        
        if os.path.exists(char_path):
            try:
                os.remove(char_path)
                return True
            except:
                return False
        return False

    
    ZIP_DATABASE = {
        "guitar":  "zip_guitar.zip",   # 吉他问题，密码: BEADGBE
        "height":  "zip_height.zip",   # 身高问题，密码: 1530
        "food":    "zip_food.zip",     # 黄瓜英语，密码: cucumber
        "date":    "zip_date.zip",     # M0.1版本发布日期，密码: 20260114
        "color":   "zip_color.zip",    # 睦代表色，密码: #779977
        "birthday":  "zip_birthday.zip" #睦生日，密码:0114
    }
    def get_random_puzzle_type():
        """随机返回一个谜题类型"""
        return random.choice(list(ZIP_DATABASE.keys()))

    def get_correct_password(p_type):
        """根据谜题类型返回正确密码"""
        # 这里需要您补全密码字典，或者直接用硬编码
        passwords = {
            "guitar": "BEADGBE",
            "height": "1530",
            "food": "cucumber",
            "date": "20260114",
            "color": "#779977",
            "birthday": "0114"
        }
        return passwords.get(p_type, "")

    # 补充定义 create_encrypted_zip_file，用于 PC 端生成指定文件
    def create_encrypted_zip_file(target_type):
        source_filename = ZIP_DATABASE.get(target_type)
        if not source_filename: return None
        
        dest_path = os.path.join(get_game_root(), "mutsumi.zip")
        try:
            if renpy.loadable("archive/" + source_filename):
                src_f = renpy.file("archive/" + source_filename)
                content = src_f.read()
                src_f.close()
                with open(dest_path, "wb") as dest_f:
                    dest_f.write(content)
                return True
        except:
            return False

    def create_encrypted_zip():
        """随机选一个预设的加密包，释放到根目录"""
        
        # 1. 随机选一个 key (也就是谜题类型)
        puzzle_type, source_filename = random.choice(list(ZIP_DATABASE.items()))
        
        # 2. 确定目标路径
        dest_path = os.path.join(get_game_root(), "mutsumi.zip")
        
        try:
            if renpy.loadable("archive/" + source_filename):
                src_f = renpy.file("archive/" + source_filename)
                content = src_f.read()
                src_f.close()
                
                with open(dest_path, "wb") as dest_f:
                    dest_f.write(content)
                    
                return puzzle_type 
            else:
                return None
        except Exception as e:
            renpy.log("Meta Error: " + str(e))
            return None


    def check_mutsumi_status():
        """
        返回三种状态:
        1. "missing" : 文件不存在
        2. "fake"    : 文件存在，但内容不对 (玩家伪造的空文件或乱写的)
        3. "real"    : 文件存在，且内容匹配 (真正的文件)
        """
        target_path = os.path.join(get_char_dir(), "mutsumi.chr")
        
        if not os.path.exists(target_path):
            return "missing"
            
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read().strip() 
                
                if content == REAL_MUTSUMI_KEY:
                    return "real"
                else:
                    return "fake"
        except:
            return "fake"





init python:
    # 强制刷新图片的函数，防止RenPy读取旧缓存
    def reload_desktop_image():
        renpy.cache_pin("desktop_cache.png")
        renpy.start_predict("desktop_cache.png")

# 定义那张拿球棒/吉他的突破CG (请确保文件名一致)
image m3_breakthrough_cg = "images/mortis/21.png"

# 定义动态的桌面截图背景
image desktop_bg_dynamic:
    "desktop_cache.png"
    # 强制拉伸到游戏分辨率，防止截图尺寸不一致导致黑边
    size (config.screen_width, config.screen_height)

# 定义白色闪光图 (用于炸裂瞬间)
image solid_white = Solid("#ffffff")


# 轻微受击 (小震动)
transform hit_smash_small:
    # 锁定中心
    transform_anchor True
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    
    # 瞬间动作：缩小 (被按下去) -> 放大 (回弹) -> 恢复
    # 速度要非常快
    easein 0.05 zoom 0.98
    easeout 0.05 zoom 1.02
    easein 0.05 zoom 1.0
    
    # 同时做一点点色差 (红蓝分离)，模拟信号干扰
    matrixcolor TintMatrix("#fff") # 初始正常
    parallel:
        linear 0.05 matrixcolor SaturationMatrix(0.0) # 瞬间黑白
        linear 0.05 matrixcolor SaturationMatrix(1.5) # 瞬间高饱和
        linear 0.05 matrixcolor IdentityMatrix()      # 恢复

# 剧烈受击 (大震动 + 旋转歪斜)
transform hit_smash_hard:
    transform_anchor True
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    
    parallel:
        # 剧烈的缩放震动 (但不位移)
        easein 0.05 zoom 0.90
        easeout 0.05 zoom 1.10
        easein 0.05 zoom 0.95
        easeout 0.05 zoom 1.0
        
    parallel:
        # 模拟液晶屏被重击后的色彩失真 (变红/变紫)
        matrixcolor TintMatrix("#ffccff") 
        linear 0.05 matrixcolor InvertMatrix(1.0) # 瞬间反色
        linear 0.05 matrixcolor TintMatrix("#ff0000") # 瞬间变红
        linear 0.1 matrixcolor IdentityMatrix() # 慢慢恢复


transform glass_crack_overlay:
    alpha 0.0
    easein 0.05 alpha 0.8 # 瞬间变白
    easeout 0.1 alpha 0.0 # 慢慢消失

# 故障闪烁 (Glitch Blink)
transform glitch_blink:
    alpha 1.0
    linear 0.05 alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.05 alpha 0.2
    linear 0.05 alpha 1.0



# 1. 桌面左半部分：向左推开，但保留在画面中
transform tearing_left_half:
    # 初始状态
    xalign 0.0 yalign 0.5
    crop (0.0, 0.0, 0.5, 1.0)
    
    parallel:
        # 向左移动一段距离 (留出中间的缝隙给墨缇斯)
        # 不要移太多，否则就看不见桌面了
        easein 0.2 xoffset -300 
    parallel:
        # 旋转模拟撕裂感
        easein 0.2 rotate -5

# 2. 桌面右半部分：向右推开，但保留在画面中
transform tearing_right_half:
    # 初始状态
    xalign 1.0 yalign 0.5
    crop (0.5, 0.0, 0.5, 1.0)
    
    parallel:
        # 向右移动一段距离
        easein 0.2 xoffset 300
    parallel:
        # 反向旋转
        easein 0.2 rotate 5

# 墨缇斯登场 (保持不变，或微调缩放以适应缝隙)
transform m3_tear_entry_horizontal:
    transform_anchor True
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    
    # 稍微放大一点，覆盖住撕开的边缘
    zoom 0.9 
    alpha 0.0
    
    parallel:
        easein 0.05 alpha 1.0
    parallel:
        # 冲击感动画
        easeout 0.1 zoom 1.15
        easein 0.1 zoom 1.1
transform screen_shatter_die:
    # --- 核心修复：锁定中心点 ---
    transform_anchor True
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    
    # 既然是全屏截图，必须先重置一下大小，防止截图本身带有位移
    xsize config.screen_width
    ysize config.screen_height
    
    parallel:
        # 瞬间放大到 4 倍 (模拟碎片飞向玩家)
        # easein 0.15 比 linear 更具有冲击力
        easein 0.15 zoom 4.0 
    parallel:
        # 稍微延迟一点点再变透明，让玩家看清炸裂的瞬间
        pause 0.05
        linear 0.1 alpha 0.0
    parallel:
        # 随机旋转 (稍微转一点就行，转多了容易晕)
        easein 0.15 rotate 10

# 墨缇斯登场：从模糊变清晰，带冲击感
# 注意：这里不能写 with hpunch，hpunch 要写在 label 剧情里
# 墨缇斯登场：破屏而出的感觉
transform m3_breakthrough_entry:
    # 初始状态：稍微放大一点 (1.1)，并且完全透明
    transform_anchor True
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    
    zoom 1.1 
    alpha 0.0
    
    parallel:
        # 快速变得清晰
        easein 0.1 alpha 1.0 
    parallel:
        # 快速回弹到正常大小 (1.0)，模拟冲击后的惯性
        easeout 0.1 zoom 1.0

# ==============================================================================
# 🖥️ 3. 界面 (Screens)
# ==============================================================================

# 伪造的报错弹窗
screen fake_error_popup():
    zorder 2000
    modal True
    frame:
        xalign 0.5 yalign 0.5
        xsize 600 ysize 250
        background Solid("#f0f0f0")
        
        vbox:
            spacing 20
            # 标题栏
            frame:
                background Solid("#fff")
                xfill True
                ysize 40
                # 修正：color属性用空格分隔
                text "Just Mutsumi - Fatal Error" color "#000" size 22 yalign 0.5 xoffset 10
            
            # 内容
            hbox:
                spacing 20
                xoffset 20
                text "❌" size 60 color "#f00" yalign 0.5
                vbox:
                    text "系统底层逻辑已崩溃。" color "#000" size 24
                    text "原因：非法修改 script.rpy" color "#000" size 20
                    text "错误代码：0xMORTIS_DEAD" color "#000" size 20
            
            # 按钮
            button:
                xalign 0.9
                action Return() # 点击关闭
                frame:
                    background Solid("#ddd")
                    padding (20, 5)
                    text "确定" color "#000"

# “无响应”的透明遮罩
screen freeze_blocker():
    zorder 3000
    modal True # 阻止所有点击
    button:
        # 修正：使用 xfill 和 yfill 填满屏幕
        xfill True
        yfill True
        background "#00000001" # 几乎透明的背景
        action Play("sound", "audio/sfx_error.ogg")

screen android_fake_script_editor():
    modal True
    zorder 300
    
    # VSCode 风格深色背景
    add Solid("#1e1e1e") 
    
    vbox:
        align (0.5, 0.5)
        spacing 10
        xsize 1000
        
        # 标题栏
        text "script.rpy - 编辑模式" color "#aaa" size 24 bold True
        
        # 【修复点】这里改成了 xsize 1.0，表示填满父容器宽度
        add Solid("#333") ysize 2 xsize 1.0
        
        null height 20
        
        # 模拟代码行 (装饰用)
        text "label start:" color "#569cd6" font "gui/font/SourceHanSerifCN-Bold.otf"
        text "    $ persistent.playthrough = 1" color "#d4d4d4" font "gui/font/SourceHanSerifCN-Bold.otf"
        text "    # ... (System Config) ..." color "#6a9955" font "gui/font/SourceHanSerifCN-Bold.otf"
        
        null height 10
        
        # === 关键的一行 (交互区域) ===
        hbox:
            spacing 10
            text "    $ persistent.in_mortis_mode = " color "#d4d4d4" font "gui/font/SourceHanSerifCN-Bold.otf" yalign 0.5
            
            # 使用一个按钮来模拟修改变量
            # 默认显示 True (红色)，点击变成 False (绿色)
            default current_value = True
            
            button:
                # 点击切换 True/False
                action ToggleScreenVariable("current_value")
                padding (10, 5)
                background Frame(Solid("#333"), 4, 4)
                
                if current_value:
                    text "True" color "#f44336" bold True # 红色 True
                else:
                    text "False" color "#4caf50" bold True # 绿色 False
        
        text "    return" color "#d4d4d4" font "gui/font/SourceHanSerifCN-Bold.otf"
        
        null height 50
        
        # 底部操作栏
        hbox:
            xalign 0.5
            spacing 50
            
            textbutton "保存并退出 (SAVE)":
                # 只有改成 False (绿色) 才能保存成功并返回 success
                if not current_value:
                    action Return("success")
                else:
                    # 如果没改就点保存，弹出提示
                    action Notify("错误：尚未修改关键变量！")
                
                text_color "#fff"
                background Frame(Solid("#007acc"), 5, 5) # 蓝色按钮
                padding (30, 15)

            textbutton "取消 (CANCEL)":
                action Return("cancel")
                text_color "#aaa"
                padding (30, 15)


# 定义一个临时的全局变量，用来接收输入
default mortis_temp_password = ""

screen mobile_decryption_popup():
    modal True
    zorder 200
    
    # 1. 半透明黑色背景遮罩
    add Solid("#000000D0")
    
    # 2. 弹窗主体
    frame:
        # 位置稍微靠上一点 (0.3)，防止被手机输入法键盘挡住
        align (0.5, 0.3) 
        xsize 800
        padding (30, 30)
        
        # 背景设为深色终端风格
        background Frame(Solid("#1a1a1a"), 4, 4) 
        
        vbox:
            spacing 20
            xfill True
            
            # 标题
            text "--- SYSTEM DECRYPTION ---" color "#0f0" size 30 bold True xalign 0.5 font "gui/font/SourceHanSerifCN-Bold.otf"
            
            add Solid("#0f0") ysize 2 xsize 1.0 alpha 0.5 # 分割线
            
            # 提示文本
            text "请输入解压密码：" color "#ccc" size 24 xalign 0.5
            
            # 3. 输入框核心组件
            frame:
                background Solid("#000")
                xalign 0.5
                padding (10, 10)
                xsize 700
                
                input:
                    # 绑定变量：输入的内容会实时存入 mortis_temp_password
                    value VariableInputValue("mortis_temp_password") 
                    length 20
                    color "#0f0" # 绿色字
                    size 30
                    xalign 0.5
                    # 允许的字符（防止输入奇怪的符号），如果密码包含英文请把 allow 删掉或修改
                    # allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#" 
            
            null height 20
            
            # 4. 按钮区域
            hbox:
                xalign 0.5
                spacing 60
                
                textbutton "【 确认解密 (ENTER) 】":
                    # 点击后返回输入的内容
                    action Return(mortis_temp_password)
                    text_color "#0f0"
                    text_hover_color "#fff"
                    text_size 26
                    text_bold True
                    
                textbutton "取消":
                    # 点击取消返回 None
                    action Return(None)
                    text_color "#888"
                    text_size 26