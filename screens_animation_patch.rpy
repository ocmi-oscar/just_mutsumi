# ==========================================================
# 📋 screens.rpy 动画优化补丁说明
# 以下是需要在 screens.rpy 中替换的代码段
# ==========================================================

# ----------------------------------------------------------
# 改动1: 通知动画 (notify_appear)
# 位置: 约第1754行
# 原因: 原版只有简单淡入淡出，没有位移，看起来突兀
# ----------------------------------------------------------

# ❌ 旧代码:
# transform notify_appear:
#     on show:
#         alpha 0
#         linear .25 alpha 1.0
#     on hide:
#         linear .5 alpha 0.0

# ✅ 替换为:
transform notify_appear:
    on show:
        yoffset -40 alpha 0.0
        easein_back 0.35 yoffset 0 alpha 1.0
    on hide:
        easeout_cubic 0.4 yoffset -25 alpha 0.0


# ----------------------------------------------------------
# 改动2: 手机弹出动画 (phone_slide_up)
# 位置: 约第2296行
# 原因: 用了 linear 做滑动，看起来像机器推上来的，没有手感
# ----------------------------------------------------------

# ❌ 旧代码:
# transform phone_slide_up:
#     on show:
#         yoffset 800 alpha 0.0
#         linear 0.3 yoffset 0 alpha 1.0
#     on hide:
#         linear 0.3 yoffset 800 alpha 0.0

# ✅ 替换为:
transform phone_slide_up:
    on show:
        yoffset 600 alpha 0.0 zoom 0.95
        easein_quint 0.4 yoffset 0 alpha 1.0 zoom 1.0
    on hide:
        easeout_cubic 0.3 yoffset 400 alpha 0.0 zoom 0.97


# ----------------------------------------------------------
# 改动3: 故障闪烁效果 (glitch_appear)
# 位置: 约第164行
# 原因: 全部 linear 等速切换，缺乏"故障"的不规则感
# ----------------------------------------------------------

# ❌ 旧代码:
# transform glitch_appear:
#     alpha 0.0
#     linear 0.1 alpha 1.0
#     linear 0.1 alpha 0.2
#     linear 0.1 alpha 1.0
#     linear 0.1 alpha 0.5
#     linear 0.1 alpha 1.0

# ✅ 已在 transforms.rpy 中重写，此处保持一致即可
# (transforms.rpy 中的版本会自动覆盖)


# ----------------------------------------------------------
# 改动4: CTC (点击继续) 提示动画
# 位置: 约第301行
# 原因: 动画可以更柔和
# ----------------------------------------------------------

# ❌ 旧代码:
# image ctc:
#     xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
#     "gui/ctc.png"
#     block:
#         easeout 0.75 alpha 1.0 xoffset 0
#         easein 0.75 alpha 0.5 xoffset -5
#         repeat

# ✅ 替换为:
image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout_cubic 0.8 alpha 1.0 xoffset 0
        easein_cubic 0.8 alpha 0.4 xoffset -4
        repeat


# ----------------------------------------------------------
# 改动5: 输入光标闪烁
# 位置: 约第322行
# 原因: linear闪烁太生硬
# ----------------------------------------------------------

# ❌ 旧代码:
# image input_caret:
#     Solid("#779977")
#     size (2,25) subpixel True
#     block:
#         linear 0.35 alpha 0
#         linear 0.35 alpha 1
#         repeat

# ✅ 替换为:
image input_caret:
    Solid("#779977")
    size (2,25) subpixel True
    block:
        easeout_cubic 0.4 alpha 0
        easein_cubic 0.4 alpha 1
        repeat


# ----------------------------------------------------------
# 改动6: 睦的Toast弹窗 (mutsumi_toast)
# 位置: 约第2445行
# 原因: 没有任何出入场动画
# ----------------------------------------------------------

# ❌ 旧代码:
# screen mutsumi_toast(msg):
#     timer 2.0 action Hide("mutsumi_toast")
#     frame:
#         align (0.5, 0.1)
#         background Solid("#779977cc")
#         padding (20, 10)
#         text "[msg]" size 18 color "#fff"

# ✅ 替换为:
screen mutsumi_toast(msg):
    timer 2.5 action Hide("mutsumi_toast")
    frame:
        align (0.5, 0.1)
        background Solid("#779977cc")
        padding (20, 10)
        at ui_toast
        text "[msg]" size 18 color "#fff"


# ----------------------------------------------------------
# 改动7: 话题分类面板 (talk_category_screen)
# 位置: 约第2069行
# 原因: 面板直接出现没有过渡
# ----------------------------------------------------------

# 找到 talk_category_screen 中的:
#     button:
#         action [Hide("talk_category_screen"), SetVariable("talking_to_mutsumi", False)]
#         background Solid("#00000077")
#         xfill True yfill True

# 在 background 下一行添加:
#         at ui_overlay_fade

# 找到:
#     frame:
#         background Frame(Solid("#779977dd"), 4, 4)
#         align (0.5, 0.4)

# 在 frame: 下一行添加:
#         at ui_popup


# ----------------------------------------------------------
# 改动8: 额外功能弹窗 (extra_features)
# 位置: 约第2460行
# 原因: 弹窗没有过渡动画
# ----------------------------------------------------------

# 找到 screen extra_features(): 中的:
#     add Solid("#000000aa")

# 替换为:
#     add Solid("#000000aa") at ui_overlay_fade

# 找到:
#     frame:
#         xsize 450 ysize 380

# 在 frame: 下方添加:
#         at ui_popup
