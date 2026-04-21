# ============================================================
# OP 第二阶段 (0:21.06 - 0:42.00)
# BPM: 183 | 每拍 0.328s
# 所有未到位素材用色块+文字占位
# ============================================================

image bg_white_scene    = Solid("#F0F0F0")
image bg_grey_scene     = Solid("#C8D0D8")
image bg_black_scene    = Solid("#050510")
image bg_sky_blue       = Solid("#8FB8D8")
image flash_white2      = Solid("#FFFFFF")
image flash_black       = Solid("#000000")
image flash_bluepurple  = Solid("#3a4878")

# CG 占位
image cg_mutsumi_smile  = Solid("#A88872")
image cg_sayoko_dark    = Solid("#2a3048")
image cg_soyo_run       = Solid("#5a7ab0")
image cg_pair_close     = Solid("#B0C4B0")

# ── 转场（如单独运行需解注）────────────────────────────────
# define op_soft_diss  = Dissolve(0.45, alpha=True)
# define op_fast_diss  = Dissolve(0.25, alpha=True)
# define op_snap_diss  = Dissolve(0.12, alpha=True)

# ══════════════════════════════════════════════════════════
# ── Transform 定义 ────────────────────────────────────────
# ══════════════════════════════════════════════════════════

transform bg_pan_sky_slow:
    xpos 0
    linear 3.0 xpos -30

transform bg_pan_mid:
    xpos 0
    linear 1.0 xpos -80

transform bg_pan_mid_cont:
    xpos -80
    linear 1.03 xpos -180

transform bg_pan_near:
    xpos 0
    linear 1.0 xpos -130

transform bg_pan_near_cont:
    xpos -130
    linear 1.03 xpos -260

transform rooftop_figure_idle:
    yoffset 0
    linear 0.5 yoffset -2
    linear 0.5 yoffset 0
    repeat

transform upsidedown_figure_enter:
    ypos -0.4
    xpos 0.38
    zoom 1.0
    rotate 0
    alpha 0.0
    parallel:
        easeout 0.25 ypos 0.0
    parallel:
        linear 0.2 alpha 0.9
    pause 0.45
    parallel:
        easein 0.5 zoom 2.6 rotate 10
    parallel:
        linear 0.5 alpha 0.85

transform script_text_swoop:
    xpos 1.1 ypos 0.72
    rotate -12
    alpha 0.0
    parallel:
        linear 0.3 alpha 1.0
    parallel:
        easeout 1.0 xpos 0.22

transform cg_mutsumi_push:
    zoom 1.0
    xalign 0.5 yalign 0.4
    alpha 0.0
    parallel:
        linear 0.25 alpha 1.0
    parallel:
        ease 1.6 zoom 1.14 xalign 0.52 yalign 0.42

transform text_kotoba_fade:
    alpha 0.0
    yoffset 14
    parallel:
        linear 0.5 alpha 1.0
    parallel:
        easeout 0.5 yoffset 0

transform cg_sayoko_tilt:
    zoom 1.08
    xalign 0.5 yalign 0.5
    rotate -5
    alpha 0.0
    parallel:
        linear 0.2 alpha 1.0
    parallel:
        ease 2.0 rotate 3 zoom 1.18

transform phone_push_in:
    zoom 0.88
    xalign 0.5 yalign 0.55
    alpha 0.0
    parallel:
        linear 0.25 alpha 1.0
    parallel:
        ease 1.8 zoom 1.08 xalign 0.48 yalign 0.52

transform camera_shake:
    xoffset 0 yoffset 0
    parallel:
        linear 0.08 xoffset 3 yoffset -2
        linear 0.08 xoffset -3 yoffset 2
        linear 0.08 xoffset 2 yoffset 0
        linear 0.08 xoffset 0 yoffset 0
        repeat

transform sun_flare_pulse:
    alpha 0.6
    zoom 1.0
    parallel:
        linear 0.5 alpha 0.9 zoom 1.1
        linear 0.5 alpha 0.6 zoom 1.0
        repeat

transform runner_push:
    zoom 0.95
    xalign 0.45 yalign 0.65
    parallel:
        linear 0.3 alpha 1.0
    parallel:
        ease 1.8 zoom 1.12 xalign 0.5

transform rabbithole_flip:
    zoom 1.05
    rotate 180
    xalign 0.5 yalign 0.5
    alpha 0.0
    linear 0.15 alpha 1.0

transform rabbithole_text_slide:
    xpos 1.1 ypos 0.5
    alpha 0.0
    rotate -3
    parallel:
        linear 0.2 alpha 1.0
    parallel:
        easeout 0.4 xpos 0.55

transform stand_enter_right:
    xpos 0.85 ypos 0.75
    alpha 0.0
    parallel:
        linear 0.3 alpha 1.0
    parallel:
        easeout 0.6 xpos 0.68

transform stand_enter_left_small:
    xpos 0.15 ypos 0.82
    alpha 0.0
    parallel:
        linear 0.3 alpha 0.9
    parallel:
        easeout 0.6 xpos 0.28

transform folklore_text_slide:
    xpos 1.2 ypos 0.55
    alpha 0.0
    rotate -5
    parallel:
        linear 0.25 alpha 1.0
    parallel:
        easeout 0.9 xpos 0.08

transform single_enter_right:
    xpos 0.75 ypos 0.82
    alpha 0.0
    zoom 0.95
    parallel:
        linear 0.25 alpha 1.0
    parallel:
        ease 0.5 zoom 1.02

transform saint_text_slide:
    xpos 1.0 ypos 0.48
    alpha 0.0
    parallel:
        linear 0.2 alpha 1.0
    parallel:
        easeout 0.5 xpos 0.4

transform duo_cg_push:
    zoom 1.0
    xalign 0.5 yalign 0.5
    alpha 0.0
    parallel:
        linear 0.25 alpha 1.0
    parallel:
        ease 2.0 zoom 1.25 xalign 0.48

transform secrets_text_appear:
    alpha 0.0
    yoffset 10
    parallel:
        linear 0.4 alpha 1.0
    parallel:
        easeout 0.4 yoffset 0

transform dark_cg_entry:
    zoom 1.05
    xalign 0.5 yalign 0.5
    alpha 0.0
    linear 0.15 alpha 1.0

transform invention_text_pulse:
    alpha 0.0
    zoom 0.95
    parallel:
        linear 0.2 alpha 1.0
    parallel:
        easeout 0.3 zoom 1.0

transform silhouette_on_roof:
    alpha 0.0
    yoffset 10
    parallel:
        linear 0.4 alpha 1.0
    parallel:
        easeout 0.6 yoffset 0

transform trio_silhouette_fade:
    alpha 0.0
    linear 0.35 alpha 1.0

transform five_enter_0:
    alpha 0.0
    yoffset 15
    parallel:
        linear 0.35 alpha 1.0
    parallel:
        easeout 0.4 yoffset 0

transform five_enter_1:
    alpha 0.0
    yoffset 15
    parallel:
        pause 0.06
        linear 0.35 alpha 1.0
    parallel:
        pause 0.06
        easeout 0.4 yoffset 0

transform five_enter_2:
    alpha 0.0
    yoffset 15
    parallel:
        pause 0.12
        linear 0.35 alpha 1.0
    parallel:
        pause 0.12
        easeout 0.4 yoffset 0

transform five_enter_3:
    alpha 0.0
    yoffset 15
    parallel:
        pause 0.18
        linear 0.35 alpha 1.0
    parallel:
        pause 0.18
        easeout 0.4 yoffset 0

transform five_enter_4:
    alpha 0.0
    yoffset 15
    parallel:
        pause 0.24
        linear 0.35 alpha 1.0
    parallel:
        pause 0.24
        easeout 0.4 yoffset 0

transform five_enter_5:
    alpha 0.0
    yoffset 15
    parallel:
        pause 0.30
        linear 0.35 alpha 1.0
    parallel:
        pause 0.30
        easeout 0.4 yoffset 0

transform looking_glass_appear:
    alpha 0.0
    xoffset -15
    zoom 0.96
    parallel:
        easein 0.3 alpha 1.0
    parallel:
        easeout 0.5 xoffset 0
    parallel:
        easeout 0.5 zoom 1.0

transform shard_in_0:
    alpha 0.0
    zoom 0.88
    parallel:
        linear 0.22 alpha 1.0
    parallel:
        easeout 0.28 zoom 1.0

transform shard_in_1:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.035
        linear 0.22 alpha 1.0
    parallel:
        pause 0.035
        easeout 0.28 zoom 1.0

transform shard_in_2:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.07
        linear 0.22 alpha 1.0
    parallel:
        pause 0.07
        easeout 0.28 zoom 1.0

transform shard_in_3:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.105
        linear 0.22 alpha 1.0
    parallel:
        pause 0.105
        easeout 0.28 zoom 1.0

transform shard_in_4:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.14
        linear 0.22 alpha 1.0
    parallel:
        pause 0.14
        easeout 0.28 zoom 1.0

transform shard_in_5:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.175
        linear 0.22 alpha 1.0
    parallel:
        pause 0.175
        easeout 0.28 zoom 1.0

transform shard_in_6:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.21
        linear 0.22 alpha 1.0
    parallel:
        pause 0.21
        easeout 0.28 zoom 1.0

transform shard_in_7:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.245
        linear 0.22 alpha 1.0
    parallel:
        pause 0.245
        easeout 0.28 zoom 1.0

transform shard_in_8:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.28
        linear 0.22 alpha 1.0
    parallel:
        pause 0.28
        easeout 0.28 zoom 1.0

transform shard_in_9:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.315
        linear 0.22 alpha 1.0
    parallel:
        pause 0.315
        easeout 0.28 zoom 1.0

transform shard_in_10:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.35
        linear 0.22 alpha 1.0
    parallel:
        pause 0.35
        easeout 0.28 zoom 1.0

transform shard_in_11:
    alpha 0.0
    zoom 0.88
    parallel:
        pause 0.385
        linear 0.22 alpha 1.0
    parallel:
        pause 0.385
        easeout 0.28 zoom 1.0

transform fade_to_white:
    alpha 1.0
    linear 0.94 alpha 0.0

# ══════════════════════════════════════════════════════════
# ── Screen 定义 ───────────────────────────────────────────
# ══════════════════════════════════════════════════════════

screen building_pan_screen():
    fixed at bg_pan_sky_slow:
        frame:
            background Solid("#CFE3F2")
            xfill True ysize 460 yalign 0.0
        frame:
            background Solid("#e8f2f8")
            xsize 280 ysize 36
            xpos 120 ypos 140
            at transform:
                alpha 0.7
        frame:
            background Solid("#e8f2f8")
            xsize 200 ysize 28
            xpos 520 ypos 100
            at transform:
                alpha 0.6
        frame:
            background Solid("#dce8f0")
            xfill True ypos 460 ysize 260
    fixed at bg_pan_mid:
        frame:
            background Solid("#d8e4ee")
            xsize 620 ysize 660
            xpos 640 ypos 60
        frame:
            background Solid("#b8cce0")
            xsize 620 ysize 18
            xpos 640 ypos 60
        frame:
            background Solid("#b0c4d8")
            xsize 620 ysize 14
            xpos 640 ypos 706
        for i in range(12):
            frame:
                background Solid("#b8cce0")
                xsize 4 ysize 640
                xpos (650 + i * 52) ypos 70
        frame:
            background Solid("#c8dce8")
            xsize 620 ysize 6
            xpos 640 ypos 280
        frame:
            background Solid("#c8dce8")
            xsize 620 ysize 6
            xpos 640 ypos 480
        frame at rooftop_figure_idle:
            background Solid("#2a3a5a")
            xsize 6 ysize 18
            xpos 920 ypos 48
    fixed at bg_pan_near:
        frame:
            background Solid("#e4eef8")
            xsize 380 ysize 420
            xpos -20 ypos 300
        for r in range(5):
            for c in range(6):
                frame:
                    background Solid("#b8cce0")
                    xsize 40 ysize 40
                    xpos (10 + c * 60) ypos (320 + r * 68)
        frame:
            background Solid("#a8bcd0")
            xsize 380 ysize 8
            xpos -20 ypos 300

screen building_chars_pan_screen():
    fixed at bg_pan_sky_slow:
        frame:
            background Solid("#CFE3F2")
            xfill True ysize 460 yalign 0.0
        frame:
            background Solid("#dce8f0")
            xfill True ypos 460 ysize 260
        frame:
            background Solid("#e8f2f8")
            xsize 280 ysize 36
            xpos 120 ypos 140
            at transform:
                alpha 0.7
    fixed at bg_pan_mid_cont:
        frame:
            background Solid("#d8e4ee")
            xsize 620 ysize 660
            xpos 640 ypos 60
        frame:
            background Solid("#b8cce0")
            xsize 620 ysize 18
            xpos 640 ypos 60
        for i in range(12):
            frame:
                background Solid("#b8cce0")
                xsize 4 ysize 640
                xpos (650 + i * 52) ypos 70
        frame:
            background Solid("#c8dce8")
            xsize 620 ysize 6
            xpos 640 ypos 280
    fixed at bg_pan_near_cont:
        frame:
            background Solid("#e4eef8")
            xsize 380 ysize 420
            xpos -20 ypos 300
        for r in range(5):
            for c in range(6):
                frame:
                    background Solid("#b8cce0")
                    xsize 40 ysize 40
                    xpos (10 + c * 60) ypos (320 + r * 68)
    # 睦（右大）
    frame:
        background Solid("#3a4a6a")
        xsize 240 ysize 540
        xpos 820 ypos 180
        at transform:
            xpos 820
            linear 1.03 xpos 760
        vbox:
            xalign 0.5 yalign 0.5
            text "若叶睦":
                font op_font_regular
                size 18 color "#ffffff" xalign 0.5
            text "（立绘占位）":
                font op_font_regular
                size 11 color "#ffffff88" xalign 0.5
    # 爽世（中）
    frame:
        background Solid("#6a4a8a")
        xsize 130 ysize 290
        xpos 580 ypos 360
        at transform:
            xpos 580
            linear 1.03 xpos 500
        text "长崎爽世":
            font op_font_regular
            size 13 color "#ffffff" xalign 0.5 yalign 0.5
    # 祥子（左）
    frame:
        background Solid("#3a5a8a")
        xsize 160 ysize 360
        xpos 200 ypos 340
        at transform:
            xpos 200
            linear 1.03 xpos 120
        text "丰川祥子":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5

screen white_trio_base():
    frame:
        background Solid("#F2F2F2")
        xfill True yfill True
    frame:
        background Solid("#4a5a7a")
        xsize 120 ysize 280
        xpos 80 ypos 390
        text "祥子":
            font op_font_regular
            size 13 color "#ffffff" xalign 0.5 yalign 0.5
    frame:
        background Solid("#6a4a8a")
        xsize 100 ysize 220
        xpos 520 ypos 440
        text "爽世":
            font op_font_regular
            size 12 color "#ffffff" xalign 0.5 yalign 0.5
    frame:
        background Solid("#3a4a6a")
        xsize 220 ysize 460
        xpos 940 ypos 260
        text "若叶睦":
            font op_font_regular
            size 18 color "#ffffff" xalign 0.5 yalign 0.5

screen upsidedown_shadow():
    fixed at upsidedown_figure_enter:
        frame:
            background Solid("#2a3868")
            xsize 110 ysize 130
            xpos 200 ypos 260
            at transform:
                alpha 0.92
        frame:
            background Solid("#2a3868")
            xsize 80 ysize 160
            xpos 140 ypos 140
            at transform:
                rotate -25
                alpha 0.85
        frame:
            background Solid("#2a3868")
            xsize 70 ysize 140
            xpos 260 ypos 150
            at transform:
                rotate 22
                alpha 0.85
        frame:
            background Solid("#3a4878")
            xsize 60 ysize 120
            xpos 100 ypos 100
            at transform:
                rotate -40
                alpha 0.75
        frame:
            background Solid("#3a4878")
            xsize 60 ysize 120
            xpos 310 ypos 100
            at transform:
                rotate 40
                alpha 0.75
        frame:
            background Solid("#2a3868")
            xsize 95 ysize 30
            xpos 208 ypos 230
        frame:
            background Solid("#2a3868")
            xsize 140 ysize 140
            xpos 185 ypos 90
        frame:
            background Solid("#3a4878")
            xsize 220 ysize 60
            xpos 145 ypos 40
            at transform:
                rotate -4
                alpha 0.9
        frame:
            background Solid("#2a3868")
            xsize 32 ysize 90
            xpos 200 ypos -30
            at transform:
                rotate -3
        frame:
            background Solid("#2a3868")
            xsize 32 ysize 90
            xpos 256 ypos -30
            at transform:
                rotate 3

screen trio_with_shadow():
    use white_trio_base
    use upsidedown_shadow

screen script_destruction():
    text "Destruction and melody.":
        font op_font_en_bold
        italic True
        size 22
        color "#334455"
        outlines []
        at script_text_swoop

screen cg_mutsumi_smile_screen():
    add Solid("#A88872") at cg_mutsumi_push
    vbox:
        xalign 0.5 yalign 0.5
        spacing 8
        text "若叶睦 · 温柔微笑 CG":
            font op_font_bold
            size 32 color "#ffffff" xalign 0.5
        text "（CG 01 占位）":
            font op_font_regular
            size 14 color "#ffffff88" xalign 0.5

screen kotoba_to_senritsu():
    vbox at text_kotoba_fade:
        xalign 0.5 yalign 0.58
        spacing 6
        text '"言葉と旋律"の物語':
            font op_font_bold
            size 30 color "#3a2a2a"
            xalign 0.5
            outlines [(1, "#ffffff88", 0, 0)]
        text "A tale made up of both words and melody":
            font op_font_en_bold
            size 18 color "#4a3a3a"
            italic True
            xalign 0.5
            outlines []

screen cg_sayoko_dark_screen():
    add Solid("#2a3048") at cg_sayoko_tilt
    frame:
        background Solid("#d8d0c8")
        xsize 280 ysize 180
        xpos 60 ypos 50
        at transform:
            rotate -8
            alpha 0.55
    frame:
        background Solid("#c8c0b8")
        xsize 220 ysize 14
        xpos 90 ypos 90
        at transform:
            rotate -8
            alpha 0.45
    frame:
        background Solid("#c8c0b8")
        xsize 200 ysize 8
        xpos 90 ypos 110
        at transform:
            rotate -8
            alpha 0.45
    vbox:
        xalign 0.5 yalign 0.5
        text "丰川祥子 · 黑衣 CG":
            font op_font_bold
            size 28 color "#ffffff" xalign 0.5
        text "（CG 02 占位）":
            font op_font_regular
            size 13 color "#ffffff88" xalign 0.5

screen phone_screen_shot():
    add Solid("#d4c4b0")
    frame:
        background Solid("#e8d8c0")
        xsize 420 ysize 420
        xpos 100 ypos 100
        at transform:
            alpha 0.5
    fixed at phone_push_in:
        frame:
            background Solid("#1c1c20")
            xsize 376 ysize 636
            xpos 452 ypos 42
        frame:
            background Solid("#f8f8f8")
            xsize 344 ysize 604
            xpos 468 ypos 58
        text "14:15":
            font op_font_bold
            size 17 color "#1a1a1a"
            xpos 482 ypos 66
        frame:
            background Solid("#b8a898")
            xsize 120 ysize 120
            xpos 580 ypos 130
        text "睦":
            font op_font_bold
            size 44 color "#ffffff"
            xpos 622 ypos 158
        text "若叶 睦":
            font op_font_bold
            size 28 color "#1a1a1a"
            xpos 556 ypos 270
        text "通話中  14:41":
            font op_font_regular
            size 16 color "#5a5a5a"
            xpos 574 ypos 316
        frame:
            background Solid("#d04040")
            xsize 60 ysize 60
            xpos 610 ypos 520
        text "×":
            font op_font_bold
            size 28 color "#ffffff"
            xpos 634 ypos 528

screen running_sun_screen():
    fixed at camera_shake:
        add Solid("#8FB8D8")
        frame:
            background Solid("#6fa4cc")
            xfill True ysize 240 yalign 0.0
            at transform:
                alpha 0.55
        frame:
            background Solid("#f0f4f8")
            xsize 340 ysize 50
            xpos 60 ypos 290
            at transform:
                alpha 0.75
        frame:
            background Solid("#ffffff")
            xsize 280 ysize 80
            xpos 400 ypos 440
            at transform:
                alpha 0.88
        frame:
            background Solid("#fff0c0")
            xsize 480 ysize 480
            xpos 720 ypos -80
            at transform:
                alpha 0.22
        frame:
            background Solid("#ffffff")
            xsize 160 ysize 160
            xpos 880 ypos 80
            at sun_flare_pulse
        frame:
            background Solid("#fffaea")
            xsize 800 ysize 6
            xpos 560 ypos 157
            at transform:
                rotate 8
                alpha 0.4
        frame at runner_push:
            background Solid("#2a2a38")
            xsize 280 ysize 520
            xpos 350 ypos 180
            vbox:
                xalign 0.5 yalign 0.5
                text "奔跑女孩":
                    font op_font_bold
                    size 22 color "#ffffff" xalign 0.5
                text "（CG 占位）":
                    font op_font_regular
                    size 13 color "#ffffff88" xalign 0.5

screen down_rabbithole_screen():
    add Solid("#7a7a80")
    frame at rabbithole_flip:
        background Solid("#505058")
        xsize 700 ysize 540
        xalign 0.5 yalign 0.5
        vbox:
            xalign 0.5 yalign 0.5
            text "倒立 CG（黑白）":
                font op_font_regular
                size 20 color "#c0c0c0" xalign 0.5
            text "（CG 占位）":
                font op_font_regular
                size 12 color "#a0a0a0" xalign 0.5
    text "Down the Rabbit-Hole":
        font op_font_en_bold
        italic True
        size 26 color "#1a1a1a"
        outlines []
        at rabbithole_text_slide

screen duo_folklore_screen():
    add Solid("#F2F2F2")
    frame:
        background Solid("#c8d0d8")
        xfill True
        ysize 60 ypos 520
        at transform:
            alpha 0.7
    frame at stand_enter_right:
        background Solid("#7a5a9a")
        xsize 260 ysize 520
        yanchor 1.0 xanchor 0.5
        vbox:
            xalign 0.5 yalign 0.5
            text "紫发女主角":
                font op_font_bold
                size 20 color "#ffffff" xalign 0.5
            text "（立绘占位）":
                font op_font_regular
                size 12 color "#ffffff88" xalign 0.5
    frame at stand_enter_left_small:
        background Solid("#5a4a7a")
        xsize 140 ysize 290
        yanchor 1.0 xanchor 0.5
        text "小女孩":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5
    text "There was one folklore.":
        font op_font_en_bold
        italic True
        size 24 color "#2a2a2a"
        outlines []
        at folklore_text_slide

screen single_saint_screen():
    add Solid("#F2F2F2")
    frame:
        background Solid("#c8d0d8")
        xfill True
        ysize 60 ypos 520
        at transform:
            alpha 0.7
    frame at single_enter_right:
        background Solid("#8a5a4a")
        xsize 230 ysize 460
        yanchor 1.0 xanchor 0.5
        vbox:
            xalign 0.5 yalign 0.5
            text "棕发女孩":
                font op_font_bold
                size 20 color "#ffffff" xalign 0.5
            text "（立绘占位）":
                font op_font_regular
                size 12 color "#ffffff88" xalign 0.5
    text "Saint triangle that was made up of folklore.":
        font op_font_en_bold
        italic True
        size 22 color "#2a2a2a"
        outlines []
        at saint_text_slide

screen duo_close_cg_screen():
    add Solid("#B0C4B0") at duo_cg_push
    for r in range(8):
        frame:
            background Solid("#4a8878")
            xsize 1280 ysize 2
            xpos 0 ypos (120 + r * 60)
            at transform:
                alpha 0.35
    for c in range(14):
        frame:
            background Solid("#4a8878")
            xsize 2 ysize 720
            xpos (c * 96) ypos 0
            at transform:
                alpha 0.35
    vbox:
        xalign 0.5 yalign 0.3
        text "双人近景 CG":
            font op_font_bold
            size 26 color "#ffffff" xalign 0.5
        text "（CG 占位）":
            font op_font_regular
            size 12 color "#ffffff88" xalign 0.5
    vbox at secrets_text_appear:
        xalign 0.5 yalign 0.88
        spacing 4
        text "Secrets that were made up of ...":
            font op_font_en_bold
            italic True
            size 20 color "#2a2a2a"
            xalign 0.5
            outlines []

screen dark_invention_screen():
    add Solid("#1a1a22")
    frame at dark_cg_entry:
        background Solid("#2a2a38")
        xsize 900 ysize 600
        xalign 0.5 yalign 0.45
        vbox:
            xalign 0.5 yalign 0.5
            text "暗黑 CG（仰望）":
                font op_font_bold
                size 22 color "#d0d0d0" xalign 0.5
            text "（CG 占位）":
                font op_font_regular
                size 12 color "#a0a0a0" xalign 0.5
    text "It's my own Invention":
        font op_font_en_bold
        italic True
        size 22 color "#ffffff"
        xalign 0.5 yalign 0.65
        outlines []
        at invention_text_pulse

screen city_sky_screen():
    fixed at camera_shake:
        add Solid("#f0f4f8")
        frame:
            background Solid("#e0ecf4")
            xsize 500 ysize 160
            xpos 140 ypos 240
            at transform:
                alpha 0.85
        frame:
            background Solid("#8090a0")
            xfill True ysize 80 ypos 500
            at transform:
                alpha 0.75
        for x, h in [(60, 100), (160, 60), (240, 140), (360, 80), (480, 120), (620, 70), (720, 110), (860, 90), (980, 130), (1100, 75), (1200, 105)]:
            frame:
                background Solid("#6a7888")
                xsize 80 ysize h
                xpos x ypos (500 - h + 20)
                at transform:
                    alpha 0.82

screen blue_silhouette_screen():
    add Solid("#f8fafc")
    frame:
        background Solid("#b8d0e4")
        xsize 900 ysize 200
        xpos 100 ypos 200
        at transform:
            alpha 0.7
    frame:
        background Solid("#3a5878")
        xfill True ysize 4 ypos 520
        at transform:
            alpha 0.9
    frame at silhouette_on_roof:
        background Solid("#2040a0")
        xsize 180 ysize 440
        xpos 780 ypos 100
        text "蓝色剪影":
            font op_font_regular
            size 16 color "#ffffff" xalign 0.5 yalign 0.5

screen trio_silhouette_roof():
    add Solid("#f0f4f8")
    frame:
        background Solid("#c0d4e4")
        xsize 800 ysize 160
        xpos 120 ypos 180
        at transform:
            alpha 0.7
    frame:
        background Solid("#3a5878")
        xfill True ysize 3 ypos 500
        at transform:
            alpha 0.85
    fixed at trio_silhouette_fade:
        frame:
            background Solid("#4060a0")
            xsize 90 ysize 260
            xpos 180 ypos 300
        frame:
            background Solid("#2040a0")
            xsize 160 ysize 400
            xpos 580 ypos 160
        frame:
            background Solid("#4060a0")
            xsize 100 ysize 280
            xpos 960 ypos 290

screen five_chars_row():
    add Solid("#F2F2F2")
    frame:
        background Solid("#d0dce8")
        xfill True ysize 50 ypos 550
        at transform:
            alpha 0.6
    frame at five_enter_0:
        background Solid("#5a4a3a")
        xsize 140 ysize 360
        xpos 100 ypos 310
        text "角色 1":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5
    frame at five_enter_1:
        background Solid("#3a5a8a")
        xsize 130 ysize 340
        xpos 290 ypos 330
        text "角色 2":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5
    frame at five_enter_2:
        background Solid("#4a7a5a")
        xsize 150 ysize 380
        xpos 470 ypos 300
        text "角色 3":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5
    frame at five_enter_3:
        background Solid("#7a5a8a")
        xsize 220 ysize 460
        xpos 660 ypos 240
        vbox:
            xalign 0.5 yalign 0.5
            text "主角 · 若叶睦":
                font op_font_bold
                size 18 color "#ffffff" xalign 0.5
    frame at five_enter_4:
        background Solid("#8a5a3a")
        xsize 140 ysize 360
        xpos 920 ypos 310
        text "角色 4":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5
    frame at five_enter_5:
        background Solid("#5a8a7a")
        xsize 130 ysize 340
        xpos 1100 ypos 330
        text "角色 5":
            font op_font_regular
            size 14 color "#ffffff" xalign 0.5 yalign 0.5

screen looking_glass_blank():
    add Solid("#FAFAFA")
    text "Looking-glass Insects":
        font op_font_en_bold
        italic True
        size 26 color "#4a4a4a"
        xalign 0.5 yalign 0.5
        outlines []
        at looking_glass_appear

screen shards_mosaic_screen():
    add Solid("#1a1a22")
    frame at shard_in_0:
        background Solid("#4a6878")
        xpos 0 ypos 0 xsize 330 ysize 260
        at transform:
            rotate -3
        vbox:
            xalign 0.5 yalign 0.5
            text "祥子":
                font op_font_bold
                size 18 color "#ffffff" xalign 0.5
            text "立绘":
                font op_font_regular
                size 10 color "#ffffff88" xalign 0.5
    frame at shard_in_1:
        background Solid("#5a7a6a")
        xpos 300 ypos 20 xsize 300 ysize 240
        at transform:
            rotate 4
        text "立希":
            font op_font_regular
            size 18 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_2:
        background Solid("#7a6a5a")
        xpos 580 ypos 0 xsize 320 ysize 280
        at transform:
            rotate -2
        text "爱音":
            font op_font_regular
            size 18 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_3:
        background Solid("#6a5a7a")
        xpos 880 ypos 10 xsize 400 ysize 300
        at transform:
            rotate 3
        vbox:
            xalign 0.5 yalign 0.5
            text "若叶睦":
                font op_font_bold
                size 22 color "#ffffff" xalign 0.5
            text "（主角）":
                font op_font_regular
                size 11 color "#ffff88" xalign 0.5
    frame at shard_in_4:
        background Solid("#5a4a6a")
        xpos -20 ypos 240 xsize 220 ysize 260
        at transform:
            rotate 5
        text "素世":
            font op_font_regular
            size 16 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_5:
        background Solid("#8a6a5a")
        xpos 200 ypos 230 xsize 280 ysize 260
        at transform:
            rotate -4
        vbox:
            xalign 0.5 yalign 0.5
            text "三角初华":
                font op_font_regular
                size 15 color "#ffffff" xalign 0.5
            text "&纯田真奈":
                font op_font_regular
                size 13 color "#ffffff" xalign 0.5
    frame at shard_in_6:
        background Solid("#3a6a7a")
        xpos 460 ypos 260 xsize 320 ysize 220
        at transform:
            rotate 2
        text "海玲":
            font op_font_regular
            size 16 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_7:
        background Solid("#7a5a3a")
        xpos 760 ypos 280 xsize 300 ysize 240
        at transform:
            rotate -5
        text "要乐奈":
            font op_font_regular
            size 16 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_8:
        background Solid("#5a7a8a")
        xpos 0 ypos 470 xsize 260 ysize 260
        at transform:
            rotate -3
        text "若麦":
            font op_font_regular
            size 15 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_9:
        background Solid("#6a4a7a")
        xpos 240 ypos 460 xsize 330 ysize 280
        at transform:
            rotate 4
        text "长崎爽世":
            font op_font_bold
            size 18 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_10:
        background Solid("#4a7a5a")
        xpos 550 ypos 470 xsize 360 ysize 260
        at transform:
            rotate -2
        text "高松燈":
            font op_font_regular
            size 17 color "#ffffff" xalign 0.5 yalign 0.5
    frame at shard_in_11:
        background Solid("#8a5a6a")
        xpos 890 ypos 450 xsize 390 ysize 280
        at transform:
            rotate 3
        vbox:
            xalign 0.5 yalign 0.5
            text "其他群像":
                font op_font_regular
                size 16 color "#ffffff" xalign 0.5
            text "Ave Mujica":
                font op_font_regular
                size 11 color "#ffff88" xalign 0.5

# ══════════════════════════════════════════════════════════
# ── Label ─────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════

label op_stage_2:

    show flash_white2 at fade_to_white zorder 25
    show screen building_pan_screen

    pause 1.00                 # → 0:22.00

    hide flash_white2

    pause 1.00                 # → 0:23.00

    hide screen building_pan_screen
    show screen building_chars_pan_screen with op_fast_diss

    pause 1.03                 # → 0:24.03

    hide screen building_chars_pan_screen
    scene bg_white_scene with op_snap_diss

    show screen trio_with_shadow
    show screen script_destruction

    pause 0.97                 # → 0:25.00

    hide screen trio_with_shadow
    hide screen script_destruction

    show flash_white2 at fade_to_white zorder 25
    show screen cg_mutsumi_smile_screen with op_fast_diss

    pause 0.85

    show screen kotoba_to_senritsu
    hide flash_white2

    pause 0.65                 # → 0:26.50

    hide screen cg_mutsumi_smile_screen
    hide screen kotoba_to_senritsu

    show screen cg_sayoko_dark_screen with op_fast_diss

    pause 1.00                 # → 0:27.50

    hide screen cg_sayoko_dark_screen

    show screen phone_screen_shot with op_soft_diss

    pause 2.00                 # → 0:29.50

    hide screen phone_screen_shot

    show screen running_sun_screen with op_snap_diss

    pause 2.00                 # → 0:31.50

    hide screen running_sun_screen

    show flash_black zorder 25
    pause 0.08
    hide flash_black

    show screen down_rabbithole_screen with op_snap_diss

    pause 0.42                 # → 0:32.00

    hide screen down_rabbithole_screen

    show screen duo_folklore_screen with op_fast_diss

    pause 1.50                 # → 0:33.50

    hide screen duo_folklore_screen

    show screen single_saint_screen with op_fast_diss

    pause 0.50                 # → 0:34.00

    hide screen single_saint_screen

    show screen duo_close_cg_screen with op_soft_diss

    pause 2.00                 # → 0:36.00

    hide screen duo_close_cg_screen

    show flash_black zorder 25
    pause 0.06
    hide flash_black

    show screen dark_invention_screen with op_snap_diss

    pause 0.44                 # → 0:36.50

    hide screen dark_invention_screen

    show screen city_sky_screen with op_fast_diss

    pause 1.00                 # → 0:37.50

    hide screen city_sky_screen

    show screen blue_silhouette_screen with op_fast_diss

    pause 1.00                 # → 0:38.50

    hide screen blue_silhouette_screen

    show screen trio_silhouette_roof with op_fast_diss

    pause 1.00                 # → 0:39.50

    hide screen trio_silhouette_roof

    show screen five_chars_row with op_fast_diss

    pause 1.00                 # → 0:40.50

    hide screen five_chars_row

    show screen looking_glass_blank with op_soft_diss

    pause 0.50                 # → 0:41.00

    hide screen looking_glass_blank

    show screen shards_mosaic_screen with op_fast_diss

    pause 1.00                 # → 0:42.00

    return
