# ==============================================================================
# 🍅 番茄钟系统 (M0.3 — 逻辑+结算弹窗)
# 界面已移至 phone_and_music.rpy，此文件只保留逻辑和结算弹窗
# ==============================================================================

init python:
    def set_p_time_fix(minutes):
        try:
            m = int(minutes)
            if m > 0:
                store.p_target_time = m * 60
                store.p_time = m * 60
                store.p_running = False
                renpy.restart_interaction()
        except:
            pass

    def p_tick_logic():
        if store.p_running and store.p_time > 0:
            store.p_time -= 1
            renpy.restart_interaction()

        elif store.p_running and store.p_time <= 0:
            store.p_running = False

            if store.p_target_time >= 600:
                add_hgd("若叶睦", 1.5, daily_id="pomodoro_daily", max_daily=1)

            if 'diary_log_pomodoro' in dir(store):
                diary_log_pomodoro()

            renpy.show_screen("pomodoro_finish_notice")
            renpy.restart_interaction()

# 默认变量
default p_time = 1500
default p_target_time = 1500
default p_running = False
default p_is_locked = False
default p_custom_input = "25"

# 结算弹窗（美化版）
screen pomodoro_finish_notice():
    modal True
    zorder 300

    # 背景遮罩
    add Solid("#000000aa") at transform:
        on show:
            alpha 0.0
            easein_cubic 0.3 alpha 1.0

    frame:
        align (0.5, 0.45)
        xsize 420 ysize 280
        background Solid("#151f1af2")
        padding (30, 25)

        at transform:
            on show:
                alpha 0.0 zoom 0.9 yoffset 20
                easein_back 0.4 alpha 1.0 zoom 1.0 yoffset 0
            on hide:
                easeout_quint 0.25 alpha 0.0 zoom 0.95

        vbox:
            align (0.5, 0.5)
            spacing 16
            xfill True

            # 顶部装饰线
            add Solid("#95e1d3") xsize 60 ysize 3 xalign 0.5

            null height 4

            text "……已经，结束了。" color "#ffffff" size 20 xalign 0.5 text_align 0.5

            if p_target_time >= 600:
                text "你很努力……这是给你的奖励。" color "#95e1d3" size 15 xalign 0.5 text_align 0.5
            else:
                text "虽然时间很短……但能专心也很好了。" color "#5a8a6a" size 15 xalign 0.5 text_align 0.5

            null height 8

            # 装饰线
            add Solid("#ffffff11") xsize 200 ysize 1 xalign 0.5

            null height 4

            button:
                action Hide("pomodoro_finish_notice")
                xalign 0.5 xsize 160 ysize 40
                background Solid("#95e1d322")
                hover_background Solid("#95e1d344")
                text "谢谢，睦" align (0.5, 0.5) size 16 color "#95e1d3"
