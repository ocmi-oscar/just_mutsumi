# ============================================================
# OP 完整开场动画 (0:00 - 0:21.26) — 优化版 v2
# BanG Dream! MyGO 同人 VN「Just 若叶睦」/ SILENT-OSCAR
# BPM: 183 | 参考：素晴らしき日々 OP
# 所有素材放在 game/op/ 文件夹
# ============================================================

define op_font_regular   = "fonts/ShipporiMincho-Regular.ttf"
define op_font_bold      = "fonts/ShipporiMincho-Bold.ttf"
define op_font_extrabold = "fonts/ShipporiMincho-ExtraBold.ttf"
define op_font_en_bold   = "fonts/CormorantGaramond-Bold.ttf"

style op_text_regular:
    font "fonts/ShipporiMincho-Regular.ttf"
    size 36
    color "#ffffff"

style op_text_bold:
    font "fonts/ShipporiMincho-Bold.ttf"
    size 36
    color "#ffffff"

style op_text_extrabold:
    font "fonts/ShipporiMincho-ExtraBold.ttf"
    size 72
    color "#ffffff"

image op_white_bg          = Solid("#FAFAF8")
image flash_white          = Solid("#FFFFFF")
image bg_mutsumi_sky       = "op/bg_mutsumi_sky.png"
image bg_bright_sky        = "op/bg_bright_sky.png"
image bg_empty_greenhouse  = "op/bg_empty_greenhouse.png"
image img_leaf             = "op/img_leaf.png"
image logo_game_title      = "op/logo_game_title.png"
image img_mutsumi_standing = "op/img_mutsumi_standing.png"

# ── 自定义转场 ────────────────────────────────────────────
define op_soft_diss  = Dissolve(0.45, alpha=True)
define op_fast_diss  = Dissolve(0.25, alpha=True)
define op_snap_diss  = Dissolve(0.12, alpha=True)
define op_flash_diss = Dissolve(0.35, alpha=True, time_warp=_warper.easein)
define op_fade_in    = Dissolve(0.6, alpha=True)

# ── Screen ────────────────────────────────────────────────

screen op_studio_tag():
    hbox at op_studio_fade:
        xalign 0.5
        yalign 0.47
        spacing 20
        text "presented by":
            font op_font_regular
            size 28
            color "#222222"
            yalign 0.5
            outlines []
        add "op/logo.png":
            zoom 0.6
            yalign 0.5

# ATL 总时长约 2.95s（淡入0.6 + 停留1.85 + 淡出0.5）
# 在 label 里：show 于 0:00.28，pause 2.22s 后到 0:02.50
# ATL 的淡出段（最后 0.5s）在 0:02.80 左右结束
# hide screen 在 pause 2.50 后执行，时序安全
transform op_studio_fade:
    alpha 0.0
    easein 0.6 alpha 1.0
    pause 1.85
    easeout 0.5 alpha 0.0

screen op_sky_quote():
    text "I never thought it was fun.":
        font op_font_en_bold
        size 46
        color "#2a2a2a"
        xanchor 0.0
        yanchor 0.5
        outlines []
        at op_sky_quote_move

transform op_sky_quote_move:
    rotate -8
    xpos 1.2
    ypos 0.42
    alpha 0.0
    parallel:
        easein 0.4 alpha 1.0
    parallel:
        easeout 2.0 xpos -0.05

# ── ATL Transform ─────────────────────────────────────────

# Phase1：zoom 2.8 → 2.3，yalign 0.85 → 0.70，历时 5.0s
transform mutsumi_sky_phase1:
    zoom 2.8
    xalign 0.5
    yalign 0.85
    ease 5.0 zoom 2.3 yalign 0.70

# Phase2：从 Phase1 结束值（zoom 2.3, yalign 0.70）继续上拉
# 起始值与 phase1 终值完全对齐，避免跳帧
transform mutsumi_sky_phase2:
    zoom 2.3
    xalign 0.5
    yalign 0.70
    easein 1.5 yalign 0.0 zoom 2.25

transform sky_pan_up:
    zoom 2.0
    xalign 0.5
    yalign 0.8
    alpha 0.0
    parallel:
        easein 0.5 alpha 1.0
    parallel:
        linear 12.0 yalign 0.0

# 叶片：飞入，在出画前自然结束（2.5s 足以飞出右上方）
transform leaf_fly:
    xpos -0.05 ypos 0.85
    rotate -20
    zoom 0.9
    alpha 0.0
    parallel:
        easein 0.3 alpha 1.0
    parallel:
        easeout 2.5 xpos 1.05 ypos -0.1 rotate 40
    # 飞出画面后 alpha 已经因位置不可见，无需额外淡出

transform greenhouse_move_left:
    zoom 1.02
    xalign 0.5 yalign 0.5
    alpha 0.0
    parallel:
        easein 0.35 alpha 1.0
    parallel:
        linear 2.0 xalign 0.42 zoom 1.05

# 标题场景 Transform ────────────────────────────────────

transform title_sky_bg:
    zoom 1.1
    xalign 0.5
    yalign 0.6
    linear 7.0 yalign 0.3 zoom 1.15

transform mutsumi_title_stand:
    xalign 0.72
    yalign 1.0
    alpha 0.0
    zoom 0.75
    parallel:
        ease 0.8 alpha 0.9
    parallel:
        ease 0.8 yalign 0.95

# 曝光瞬闪：easein 延长至 0.12s，确保可感知
transform flash_peak:
    alpha 0.0
    easein 0.12 alpha 1.0
    easeout 0.28 alpha 0.0

# logo砸入：去掉内置淡出，由 label 在合适时机统一控制
# 原版：pause 4.55 → easein 1.0 alpha 0.0（会在 t=5.55s 自行消失）
# 修订：logo 全程保持可见，由 label jump 前统一 hide
transform logo_slam:
    zoom 2.5
    xalign 0.5 yalign 0.5
    alpha 0.0
    parallel:
        easeout 0.45 zoom 0.87
    parallel:
        linear 0.35 alpha 1.0

# logo 退出（jump 前调用）
transform logo_fadeout:
    alpha 1.0
    zoom 0.87
    xalign 0.5 yalign 0.5
    easein 0.5 alpha 0.0

# ── Label ─────────────────────────────────────────────────

label op_stage_1:

    play music "op/op.mp3" fadein 0.0

    # ════════════════
    # 0:00.00 - 0:00.28 │ 纯白底
    # ════════════════
    scene op_white_bg

    pause 0.28

    # ════════════════
    # 0:00.28 │ 厂牌渐显
    # ATL 自带淡入(0.6s)+停留(1.85s)+淡出(0.5s)，共约 2.95s
    # ════════════════
    show screen op_studio_tag

    pause 2.22            # → 0:02.50

    # ════════════════
    # 0:02.50 - 0:07.50 │ 天空推镜 Phase1
    # 厂牌 ATL 的淡出段此时仍在进行（约再持续 0.28s），
    # scene 切换后厂牌会因 screen 独立层而继续淡完，无干扰
    # ════════════════
    scene bg_mutsumi_sky at mutsumi_sky_phase1 with op_soft_diss

    pause 2.50            # → 0:05.00
    hide screen op_studio_tag   # ATL 已淡完，此时 hide 安全

    pause 2.50            # → 0:07.50

    # ════════════════
    # 0:07.50 - 0:09.00 │ Phase2：继续上拉
    # 注意：show 同一张图片会重置 ATL，
    # phase2 起始值 (zoom 2.3, yalign 0.70) 与 phase1 终值对齐
    # ════════════════
    show bg_mutsumi_sky at mutsumi_sky_phase2

    pause 1.50            # → 0:09.00

    # ════════════════
    # 0:09.00 - 0:10.00 │ 切换亮天空
    # scene 会清除之前所有 show 的图层，状态干净
    # ════════════════
    scene bg_bright_sky at sky_pan_up with op_soft_diss

    pause 1.00            # → 0:10.00

    # ════════════════
    # 0:10.00 - 0:12.00 │ 叶片飞过 + 天空寄语
    # leaf_fly 总时长 2.5s，飞出画面后自然不可见
    # op_sky_quote 在 2.0s 时手动淡出（给 0.3s 淡出时间）
    # ════════════════
    show img_leaf at leaf_fly zorder 3
    show screen op_sky_quote

    pause 1.70            # → 0:11.70（给 quote 0.3s 淡出）

    # quote 淡出（hide screen 支持 with 转场）
    hide screen op_sky_quote with Dissolve(0.30)

    pause 0.30            # → 0:12.00（叶片仍在飞，quote 淡完）

    # ════════════════
    # 0:12.00 - 0:14.00 │ 温室空镜
    # leaf 已飞出画面，hide 清理
    # ════════════════
    hide img_leaf

    scene bg_bright_sky with op_soft_diss      # 保留天空底层
    show bg_empty_greenhouse at greenhouse_move_left zorder 5 with op_soft_diss

    pause 2.00            # → 0:14.00

    # ════════════════
    # 0:14.00 - 0:15.00 │ 溶回天空底色，准备标题
    # hide 温室后 scene 切换天空，层级干净
    # ════════════════
    hide bg_empty_greenhouse with op_soft_diss

    scene bg_bright_sky at title_sky_bg with op_soft_diss

    pause 1.00            # → 0:15.00

    # ════════════════
    # 0:15.00 - 0:21.26 │ 标题砸入
    # 层级：天空(scene) < 睦立绘(zorder 1) < logo(zorder 10) < 闪光(zorder 20)
    # ════════════════

    # 曝光瞬闪（0.12s 亮起 + 0.28s 退去，共 0.4s）
    show flash_white at flash_peak zorder 20

    # 睦立绘淡入
    show img_mutsumi_standing at mutsumi_title_stand zorder 1

    # logo 砸入（不含内置淡出，全程可见）
    show logo_game_title at logo_slam zorder 10

    pause 5.80            # → 0:20.80

    # logo 与立绘同步淡出，给 jump 前留 0.46s 过渡
    show logo_game_title at logo_fadeout zorder 10

    pause 0.46            # → 0:21.26

    hide flash_white
    hide logo_game_title
    hide img_mutsumi_standing

    jump op_stage_2
