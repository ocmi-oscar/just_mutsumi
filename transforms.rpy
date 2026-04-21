
transform ad_left:
    xalign 0.15 yalign 0.5 zoom 0.8 alpha 0.0
    on show:
        pause 0.5
        easein 0.8 alpha 1.0 xoffset 20
    on hide:
        easeout 0.5 alpha 0.0 xoffset -20

transform ad_right:
    xalign 0.85 yalign 0.5 zoom 0.8 alpha 0.0
    on show:
        pause 0.5
        easein 0.8 alpha 1.0 xoffset -20
    on hide:
        easeout 0.5 alpha 0.0 xoffset 20
# =========================================================
# ⚡ ATL 变换定义 (修复版)
# =========================================================

# --- 1. 剧烈撕裂抖动 (Tearing Shake) ---
# 让画面在极短时间内大幅度左右横跳
transform glitch_tearing_shake:
    # 【修复点】align (0.5, 0.5) 已经包含了居中锚点，删除了重复的 xanchor/yanchor
    align (0.5, 0.5)
    
    # 疯狂的随机抖动序列 (总耗时约 0.3秒)
    parallel:
        xoffset 0
        linear 0.02 xoffset 50  # 向右猛冲
        linear 0.02 xoffset -40 # 向左回拉
        linear 0.02 xoffset 30
        linear 0.02 xoffset -60
        linear 0.02 xoffset 20
        linear 0.02 xoffset -10
        linear 0.02 xoffset 0   # 回归原位
    parallel:
        # 伴随轻微的纵向抖动
        yoffset 0
        linear 0.05 yoffset 10
        linear 0.05 yoffset -15
        linear 0.05 yoffset 5
        linear 0.05 yoffset 0

# --- 2. 颜色反转闪烁 (Invert Flash) ---
# 利用 matrixcolor 瞬间反转画面颜色，模拟信号丢失
transform glitch_invert_flash:
    matrixcolor InvertMatrix(0.0) # 初始正常
    linear 0.05 matrixcolor InvertMatrix(1.0) # 瞬间反色
    pause 0.05
    linear 0.05 matrixcolor InvertMatrix(0.0) # 恢复正常
    pause 0.05
    linear 0.05 matrixcolor InvertMatrix(0.8) # 部分反色
    linear 0.1 matrixcolor InvertMatrix(0.0) # 恢复

# =========================================================
# 📺 故障转场特效素材定义
# =========================================================

# --- 1. 定义动态噪点图层 ---
# 使用 Solid 色块快速切换，模拟电视雪花噪点
image glitch_static_noise:
    Solid("#000") # 黑帧
    pause 0.05
    Solid("#fff") # 白帧
    pause 0.05
    Solid("#888") # 灰帧
    pause 0.05
    Solid("#333") # 深灰帧
    pause 0.05
    repeat # 循环播放

# --- 2. 定义故障音效 (占位符) ---
# 【重要】请准备一个刺耳的电流麦或数据损坏音效，命名为 sfx_glitch_loud.ogg 放入 audio 文件夹
# 如果没有，暂时用这个空的代替，但效果会大打折扣
if not renpy.loadable("audio/sfx_glitch_loud.ogg"):
    # 如果找不到文件，定义一个静音文件防止报错
    define audio.glitch_loud = "audio/sfx_blank.ogg" 
else:
    define audio.glitch_loud = "audio/sfx_glitch_loud.ogg"

# 一个稍微短一点的故障音
if not renpy.loadable("audio/sfx_glitch_short.ogg"):
    define audio.glitch_short = "audio/sfx_blank.ogg"
else:
    define audio.glitch_short = "audio/sfx_glitch_short.ogg"

label glitch_scene(next_bg_image):
    if renpy.loadable("audio/sfx_glitch_short.ogg"):
        play sound audio.glitch_short
    show layer master at glitch_invert_flash
    pause 0.2
    play sound audio.glitch_loud
    show glitch_static_noise as noise_layer zorder 999 at truecenter
    show layer master at glitch_tearing_shake
    
    pause 0.1
    scene black # 瞬间黑屏
    pause 0.05

    show glitch_static_noise as noise_layer zorder 999 at truecenter
    pause 0.1
    $ renpy.show(next_bg_image)
    hide noise_layer
    show layer master at glitch_invert_flash
    pause 0.3
    show layer master at default
    return

# ============================================================
# 基础定义 (Helpers)
# ============================================================
transform glitch_shake:
    parallel:
        linear 0.05 xoffset 20
        linear 0.05 xoffset -20
        linear 0.05 xoffset 0
        repeat
    parallel:
        alpha 0.8
        linear 0.1 alpha 1.0
        linear 0.1 alpha 0.6
        repeat

# 2. 颜色分离 (RGB Split) - 模拟花屏
transform chromatic_aberration:
    parallel:
        xoffset -5 alpha 0.5
        linear 0.1 xoffset 5
        repeat
    
# 3. 乱码文字生成器
init python:
    import random
    import string
    
    def glitch_text(length=10):
        # 生成一串看起来像乱码的字符
        chars = "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß"
        return "".join(random.choice(chars) for _ in range(length))

# 4. 模拟控制台屏幕
screen fake_console(lines):
    zorder 100
    add Solid("#000000CC") # 半透明黑底
    
    vbox:
        xalign 0.05
        yalign 0.05
        spacing 5
        
        for line in lines:
            text line:
                font "gui/font/SourceHanSerifCN-Bold.otf" # 最好用等宽字体
                size 24
                color "#00FF00" # 黑客绿
                outlines [(1, "#000", 0, 0)]

        
# 标准立绘大小
define CHAR_ZOOM = 0.80
# 说话时放大的倍率
define FOCUS_ZOOM = 1.05 
# 站立位置基准
define CHAR_Y = 1.03

define dissolve_scene_full = MultipleTransition([
    False, Dissolve(1.0),
    Solid("#000"), Pause(1.0),
    Solid("#000"), Dissolve(1.0),
    True])

# 半程黑屏过渡 (dissolve_scene_half)
define dissolve_scene_half = MultipleTransition([
    Solid("#000"), Pause(1.0),
    Solid("#000"), Dissolve(1.0),
    True])


define fade = Fade(0.5, 0.0, 0.5)

# 像素化 (Pixellate)
define pixellate = Pixellate(1.0, 5)

# 移动效果 (Move)
# 比如 show monika at t11 with move
define move = MoveTransition(0.3)

# 通用重置变换：每次变换前重置状态，防止叠加错误
transform reset_state(x, z=CHAR_ZOOM):
    # 锚点设为底部中心
    xcenter x 
    yoffset 0 
    yanchor 1.0 
    ypos CHAR_Y 
    alpha 1.0 
    subpixel True
    
    # 平滑过渡逻辑 (替代原版的 easein .25)
    on show:
        yoffset 20 alpha 0.0 zoom (z * 0.95)
        easein 0.3 yoffset 0 alpha 1.0 zoom z
    
    on replace:
        # 0.3秒的平滑移动，比原版稍微慢0.05秒，更柔和
        ease 0.3 xcenter x zoom z yoffset 0 alpha 1.0

# 瞬间出现 (Instant)
transform instant_state(x, z=CHAR_ZOOM):
    xcenter x 
    yoffset 0 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True

# 聚焦/说话 (Focus)
transform focus_state(x, z=CHAR_ZOOM):
    xcenter x 
    yanchor 1.0 
    ypos CHAR_Y 
    subpixel True
    
    on show:
        yoffset 20 alpha 0.0 zoom (z * 0.95)
        easein 0.3 yoffset 0 alpha 1.0 zoom (z * FOCUS_ZOOM)
    
    on replace:
        # 说话时稍微放大，并确保位置对齐
        ease 0.2 xcenter x zoom (z * FOCUS_ZOOM) yoffset 0 alpha 1.0

# 下沉 (Sink)
transform sink_state(x, z=CHAR_ZOOM):
    xcenter x 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True
    # 向下沉入屏幕底部
    easein 0.5 ypos 1.15

# 跳跃 (Hop)
transform hop_state(x, z=CHAR_ZOOM):
    xcenter x 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True
    # 快速跳起
    easein 0.1 yoffset -25
    easeout 0.1 yoffset 0
transform m3_speaking_zoom:
    subpixel True            # 开启亚像素渲染，保证移动平滑
    xalign 0.5 yalign 1.0    # 锚点设为底部中心，保证站在地上放大
    parallel:
        easein 0.2 zoom 1.05 # 0.2秒内放大到 1.05 倍
    parallel:
        easein 0.2 yoffset 20 # 稍微向下偏移一点，防止头顶出屏幕太突兀(视立绘情况调整)

# 不说话时：恢复原状
transform m3_idle_zoom:
    subpixel True
    xalign 0.5 yalign 1.0
    parallel:
        easeout 0.2 zoom 1.0 # 0.2秒内恢复 1.0 倍
    parallel:
        easeout 0.2 yoffset 0
        
# 聚焦跳跃 (Focus Hop)
transform hop_focus_state(x, z=CHAR_ZOOM):
    xcenter x 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom (z * FOCUS_ZOOM) 
    alpha 1.0 
    subpixel True
    easein 0.1 yoffset -25
    easeout 0.1 yoffset 0
# =========================================================
# 📼 特效定义：倒带效果 (VHS Rewind)
# =========================================================
transform vhs_rewind_effect:
    # 模拟录像带倒带时的画面抖动和条纹
    parallel:
        linear 0.1 xoffset 20
        linear 0.1 xoffset -20
        repeat
    parallel:
        alpha 0.8
        linear 0.05 alpha 0.6
        linear 0.05 alpha 0.8
        repeat
image white_noise = Solid("#ffffff") # 或者用一张雪花屏图片
transform shake_screen:
    linear 0.05 xoffset -20
    linear 0.05 xoffset 20
    linear 0.05 xoffset -20
    linear 0.05 xoffset 20
    linear 0.05 xoffset 0
# 蹲下/躲避 (Dip)
transform dip_state(x, z=CHAR_ZOOM):
    xcenter x 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True
    # 快速蹲下
    easein 0.2 yoffset 30
    easeout 0.2 yoffset 0

# 左侧滑入 (Left In)
transform left_in_state(x, z=CHAR_ZOOM):
    xcenter -300 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True
    ease 0.3 xcenter x

# 右侧滑入 (Right In)
transform right_in_state(x, z=CHAR_ZOOM):
    xcenter 1580 
    yanchor 1.0 
    ypos CHAR_Y 
    zoom z 
    alpha 1.0 
    subpixel True
    ease 0.3 xcenter x

# 隐藏 (Hide / thide)
transform thide(z=CHAR_ZOOM):
    subpixel True
    # 淡出并稍微下沉
    on hide:
        easeout 0.3 zoom (z * 0.95) alpha 0.0 yoffset 20

# 向左跑掉 (lhide)
transform lhide:
    subpixel True
    on hide:
        easeout 0.3 xcenter -500

# 向右跑掉 (rhide)
transform rhide:
    subpixel True
    on hide:
        easeout 0.3 xcenter 1780

# ============================================================
# 经典位置定义 (t11 - t44)
# 保留了原版坐标，方便直接套用旧脚本
# ============================================================

# --- 单人 (Center) ---
transform t11:
    reset_state(640)

# --- 双人 (Two Characters) ---
transform t21:
    reset_state(400)
transform t22:
    reset_state(880)

# --- 三人 (Three Characters) ---
transform t31:
    reset_state(240)
transform t32:
    reset_state(640)
transform t33:
    reset_state(1040)

# --- 四人 (Four Characters) ---
transform t41:
    reset_state(200)
transform t42:
    reset_state(493)
transform t43:
    reset_state(786)
transform t44:
    reset_state(1080)

# ============================================================
# 聚焦定义 (Focus / f11 - f44)
# ============================================================

transform f11:
    focus_state(640)

transform f21:
    focus_state(400)
transform f22:
    focus_state(880)

transform f31:
    focus_state(240)
transform f32:
    focus_state(640)
transform f33:
    focus_state(1040)

transform f41:
    focus_state(200)
transform f42:
    focus_state(493)
transform f43:
    focus_state(786)
transform f44:
    focus_state(1080)

# ============================================================
# 瞬间出现 (Instant / i11 - i44)
# ============================================================

transform i11:
    instant_state(640)

transform i21:
    instant_state(400)
transform i22:
    instant_state(880)

transform i31:
    instant_state(240)
transform i32:
    instant_state(640)
transform i33:
    instant_state(1040)

transform i41:
    instant_state(200)
transform i42:
    instant_state(493)
transform i43:
    instant_state(786)
transform i44:
    instant_state(1080)

# ============================================================
# 跳跃 (Hop / h11 - h44)
# ============================================================

transform h11:
    hop_state(640)

transform h21:
    hop_state(400)
transform h22:
    hop_state(880)

transform h31:
    hop_state(240)
transform h32:
    hop_state(640)
transform h33:
    hop_state(1040)

transform h41:
    hop_state(200)
transform h42:
    hop_state(493)
transform h43:
    hop_state(786)
transform h44:
    hop_state(1080)

# ============================================================
# 聚焦跳跃 (Hop Focus / hf11 - hf44)
# ============================================================

transform hf11:
    hop_focus_state(640)

transform hf21:
    hop_focus_state(400)
transform hf22:
    hop_focus_state(880)

transform hf31:
    hop_focus_state(240)
transform hf32:
    hop_focus_state(640)
transform hf33:
    hop_focus_state(1040)

transform hf41:
    hop_focus_state(200)
transform hf42:
    hop_focus_state(493)
transform hf43:
    hop_focus_state(786)
transform hf44:
    hop_focus_state(1080)

# ============================================================
# 下沉 (Sink / s11 - s44)
# ============================================================

transform s11:
    sink_state(640)

transform s21:
    sink_state(400)
transform s22:
    sink_state(880)

transform s31:
    sink_state(240)
transform s32:
    sink_state(640)
transform s33:
    sink_state(1040)

transform s41:
    sink_state(200)
transform s42:
    sink_state(493)
transform s43:
    sink_state(786)
transform s44:
    sink_state(1080)

# ============================================================
# 滑入效果 (Slide In / l, r)
# ============================================================

# 左侧滑入
transform l11:
    left_in_state(640)
transform l21:
    left_in_state(400)
transform l22:
    left_in_state(880)
transform l31:
    left_in_state(240)
transform l32:
    left_in_state(640)
transform l33:
    left_in_state(1040)
transform l41:
    left_in_state(200)
transform l42:
    left_in_state(493)
transform l43:
    left_in_state(786)
transform l44:
    left_in_state(1080)

# 右侧滑入
transform r11:
    right_in_state(640)
transform r21:
    right_in_state(400)
transform r22:
    right_in_state(880)
transform r31:
    right_in_state(240)
transform r32:
    right_in_state(640)
transform r33:
    right_in_state(1040)
transform r41:
    right_in_state(200)
transform r42:
    right_in_state(493)
transform r43:
    right_in_state(786)
transform r44:
    right_in_state(1080)

# ============================================================
# 其他特效 (Special Effects)
# ============================================================

# 脸部特写 (Zoom Face)
transform face(z=0.80, y=500):
    subpixel True
    xcenter 640
    yanchor 1.0 
    ypos 1.03
    yoffset y
    zoom (z * 2.00)

# 惊慌/震动 (Panic) - 重写了震动逻辑
transform panic(z=CHAR_ZOOM):
    yanchor 1.0 
    ypos CHAR_Y
    zoom z
    subpixel True
    parallel:
        ease 0.06 xoffset 5
        ease 0.06 xoffset -5
        repeat
    parallel:
        ease 0.08 yoffset 5
        ease 0.08 yoffset -5
        repeat

# 噪音效果 (Noise) - 优化了写法
image noise:
    truecenter
    "images/bg/noise1.jpg"
    pause 0.05
    "images/bg/noise2.jpg"
    pause 0.05
    "images/bg/noise3.jpg"
    pause 0.05
    "images/bg/noise4.jpg"
    pause 0.05
    repeat

transform noise_alpha:
    alpha 0.25

# 转场定义 (Transitions)
define dissolve = Dissolve(0.25)
define dissolve_cg = Dissolve(0.75)
define dissolve_scene = Dissolve(1.0)
define tpause = Pause(0.25)

# 睁眼闭眼效果
define close_eyes = MultipleTransition([
    False, Dissolve(0.5),
    Solid("#000"), Pause(0.25),
    True])

define open_eyes = MultipleTransition([
    False, Dissolve(0.5),
    True])

define trueblack = MultipleTransition([
    Solid("#000"), Pause(0.25),
    Solid("#000")
    ])