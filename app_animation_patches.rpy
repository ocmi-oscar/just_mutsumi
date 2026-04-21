# ==========================================================
# 📋 各App动画优化补丁
# ==========================================================


# ==========================
# 📝 note_app.rpy 改动
# ==========================

# ❌ 旧代码 (约第2行):
# transform note_app_animation:
#     on show:
#         yoffset 100 alpha 0.0 zoom 0.98
#         easein_cubic 0.4 yoffset 0 alpha 1.0 zoom 1.0
#     on hide:
#         easeout_cubic 0.4 yoffset 100 alpha 0.0 zoom 0.98

# ✅ 替换为（加入轻微回弹，退出更快）:
transform note_app_animation:
    on show:
        yoffset 80 alpha 0.0 zoom 0.95
        easein_back 0.4 yoffset 0 alpha 1.0 zoom 1.0
    on hide:
        easeout_quint 0.3 yoffset 60 alpha 0.0 zoom 0.97


# ==========================
# ✅ todo_app.rpy 改动
# ==========================

# ❌ 旧代码 (约第2行):
# transform todo_card_appear:
#     on show:
#         xoffset 100 alpha 0.0
#         easein_back 0.4 xoffset 0 alpha 1.0
#     on hide:
#         easeout_back 0.4 xoffset 100 alpha 0.0

# ✅ 替换为（加入缩放，退出更干脆）:
transform todo_card_appear:
    on show:
        xoffset 120 alpha 0.0 zoom 0.95
        easein_back 0.4 xoffset 0 alpha 1.0 zoom 1.0
    on hide:
        easeout_quint 0.25 xoffset 80 alpha 0.0 zoom 0.97

# ❌ 旧代码 (约第169行):
# transform d_fade:
#     alpha 0.0
#     linear 0.3 alpha 1.0
#     on hide:
#         linear 0.3 alpha 0.0

# ✅ 替换为:
transform d_fade:
    on show:
        alpha 0.0
        easein_cubic 0.3 alpha 1.0
    on hide:
        easeout_cubic 0.25 alpha 0.0


# ==========================
# 🍅 tomato.rpy 改动
# ==========================

# 找到 pomodoro_finish_notice 弹窗中的:
#     frame:
#         align (0.5, 0.45)
#         xsize 450 ysize 300

# 在 frame: 下方添加:
#         at ui_popup

# 同样，找到弹窗前的:
#     add Solid("#000000aa")
# 替换为:
#     add Solid("#000000aa") at ui_overlay_fade

# 找到 pomodoro_app 中运行时切换到小窗的逻辑。
# 当前是通过 if not p_running 直接切换大小，没有过渡。
# 这个因为Ren'Py的screen刷新机制限制，无法直接加ATL动画。
# 建议保持现状，或在大小窗切换时简单加一个 zoom 过渡：

# 在 pomodoro_app 的 frame 中，
# if not p_running 的 frame 后面加:
#         at transform:
#             zoom 0.95 alpha 0.0
#             easein_back 0.3 zoom 1.0 alpha 1.0


# ==========================
# 📅 rili.rpy 改动
# ==========================

# ❌ 旧代码 (约第9行):
# transform cal_appear:
#     alpha 0.0 zoom 0.95
#     easein_back 0.3 alpha 1.0 zoom 1.0

# ✅ 替换为（更柔和的展开）:
transform cal_appear:
    on show:
        alpha 0.0 zoom 0.92 yoffset 20
        easein_back 0.4 alpha 1.0 zoom 1.0 yoffset 0
    on hide:
        easeout_quint 0.25 alpha 0.0 zoom 0.95 yoffset 15

# ❌ 旧代码 (约第13行):
# transform cal_today_pulse:
#     matrixcolor TintMatrix("#ffffff00")
#     linear 1.0 matrixcolor TintMatrix("#ffffff44")
#     linear 1.0 matrixcolor TintMatrix("#ffffff00")
#     repeat

# ✅ 替换为（更柔和的呼吸）:
transform cal_today_pulse:
    matrixcolor TintMatrix("#ffffff00")
    easein_cubic 1.2 matrixcolor TintMatrix("#ffffff44")
    easeout_cubic 1.2 matrixcolor TintMatrix("#ffffff00")
    repeat


# ==========================
# 🌿 sponsor.rpy 改动
# ==========================

# ❌ 旧代码 (约第42行):
# transform sponsor_master_transform:
#     on show:
#         alpha 0.0 yoffset 100
#         easein_back 0.8 alpha 1.0 yoffset 0
#     on hide:
#         parallel:
#             easeout_quint 0.6 alpha 0.0
#         parallel:
#             easeout_back 0.6 xoffset 200 zoom 0.9 blur 10

# ✅ 替换为（出场和退场更协调）:
transform sponsor_master_transform:
    on show:
        alpha 0.0 yoffset 60 zoom 0.93
        easein_back 0.5 alpha 1.0 yoffset 0 zoom 1.0
    on hide:
        easeout_quint 0.35 alpha 0.0 yoffset 30 zoom 0.95
