# ==========================================================
# 🎬 抽卡动画重制版 (M0.62 - Crash Fix)
# ==========================================================

# --- 1. 基础图形定义 (无需图片) ---
image anim_particle_green = Frame(Solid("#95e1d3"), xsize=20, ysize=20)
image anim_particle_gold  = Frame(Solid("#ffd700"), xsize=25, ysize=25)
image anim_particle_red   = Frame(Solid("#ff3333"), xsize=30, ysize=30)

image anim_flash_white = Solid("#ffffff")
image anim_bg_dark = Solid("#000000")
image anim_bg_red = Solid("#330000")

# --- 2. ATL 动画特效 ---

# [通用] 粒子上升
transform particle_float(d_time=1.0, x_var=100):
    alpha 0.0 yoffset 300 xoffset 0 zoom 0.5
    parallel:
        easein d_time alpha 0.8
    parallel:
        easeout d_time yoffset -300
    parallel:
        linear d_time xoffset (renpy.random.randint(-x_var, x_var))
    parallel:
        linear d_time zoom 1.0
    easeout 0.2 alpha 0.0

# [5星] 聚光灯旋转
transform spotlight_rotate:
    align (0.5, 0.5)
    alpha 0.0 zoom 0.0 rotate 0
    parallel:
        easein 0.5 alpha 1.0 zoom 3.0
    parallel:
        linear 3.0 rotate 360

# [5星] 强烈闪光
transform intense_flash:
    alpha 0.0
    easein 0.1 alpha 1.0
    easeout 0.5 alpha 0.0

# [6星] 故障抖动 (Glitch Shake) - 【CRASH FIX: Added time duration】
transform glitch_shake:
    align (0.5, 0.5)
    parallel:
        # Position shake
        linear 0.05 xoffset -20
        linear 0.05 xoffset 20
        linear 0.05 xoffset -10
        linear 0.05 xoffset 10
        linear 0.05 xoffset 0
        repeat
    parallel:
        # Zoom shake (Added pause to prevent infinite loop)
        choice:
            zoom 1.0
            pause 0.05
        choice:
            zoom 1.02
            pause 0.05
        choice:
            zoom 0.98
            pause 0.05
        repeat

# [6星] 红色脉冲警告
transform red_alert_pulse:
    alpha 0.3
    easein 0.2 alpha 0.6
    easeout 0.2 alpha 0.3
    repeat

# --- 3. 动画播放界面 ---
# gacha_animation_screen 已移至 gacha_system_new.rpy
