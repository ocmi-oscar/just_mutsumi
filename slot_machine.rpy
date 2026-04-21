# ==============================================================================
# 🎰 老虎机 — Mutsumi Slots
# 消耗睦币，纯代码UI
# ==============================================================================

init python:
    import random as _slot_rng

    SLOT_SYMBOLS = ["🥒", "🌿", "🎸", "★", "♪", "💚", "🌙"]
    SLOT_COST = 5

    class SlotMachine(python_object):
        def __init__(self):
            self.reels = ["?", "?", "?"]
            self.spinning = False
            self.result_msg = ""
            self.result_color = "#ffffff55"
            self.total_spins = 0
            self.total_won = 0

        def spin(self):
            coins = getattr(persistent, 'mutsumi_coins', 0) or 0
            if coins < SLOT_COST:
                self.result_msg = "睦币不足！"
                self.result_color = "#ff6666"
                renpy.restart_interaction()
                return
            persistent.mutsumi_coins = coins - SLOT_COST
            self.spinning = True
            self.result_msg = ""
            renpy.restart_interaction()

        def finish_spin(self):
            self.reels = [_slot_rng.choice(SLOT_SYMBOLS) for _ in range(3)]
            self.spinning = False
            self.total_spins += 1
            # 判定奖励
            if self.reels[0] == self.reels[1] == self.reels[2]:
                if self.reels[0] == "🥒":
                    reward = 100
                    self.result_msg = "大奖！黄瓜三连！+{}睦币".format(reward)
                    self.result_color = "#ffd700"
                elif self.reels[0] == "★":
                    reward = 50
                    self.result_msg = "星星三连！+{}睦币".format(reward)
                    self.result_color = "#ffd700"
                else:
                    reward = 30
                    self.result_msg = "三连！+{}睦币".format(reward)
                    self.result_color = "#95e1d3"
                persistent.mutsumi_coins = (getattr(persistent, 'mutsumi_coins', 0) or 0) + reward
                self.total_won += reward
            elif self.reels[0] == self.reels[1] or self.reels[1] == self.reels[2]:
                reward = 8
                persistent.mutsumi_coins = (getattr(persistent, 'mutsumi_coins', 0) or 0) + reward
                self.total_won += reward
                self.result_msg = "两连！+{}睦币".format(reward)
                self.result_color = "#ffffffaa"
            else:
                self.result_msg = "没有中奖…"
                self.result_color = "#ffffff44"
            renpy.save_persistent()
            renpy.restart_interaction()

label start_slot_machine:
    $ _slot = SlotMachine()
    call screen slot_machine_screen(_slot)
    jump game_center_start

screen slot_machine_screen(sm):
    modal True
    zorder 200

    if sm.spinning:
        timer 0.8 action Function(sm.finish_spin)

    add Solid("#0a0a1a")

    $ _sm_coins = getattr(persistent, 'mutsumi_coins', 0) or 0

    # 顶部
    frame:
        xfill True ysize 80
        background Solid("#1a1a2e")
        padding (30, 12)
        hbox:
            xfill True yalign 0.5
            vbox:
                spacing 2
                text "老虎机" size 20 color "#ffd700" bold True
                text "Mutsumi Slots" size 10 color "#ffffff44"
            vbox:
                xalign 1.0 spacing 2
                text "睦币" size 10 color "#ffd700" xalign 1.0
                text "[_sm_coins]" size 22 color "#ffd700" bold True xalign 1.0 font "DejaVuSans.ttf"

    # 老虎机主体
    frame:
        xalign 0.5 yalign 0.42
        xsize 500 ysize 220
        background Solid("#12122a")
        padding (20, 20)

        vbox:
            spacing 16 xfill True

            # 三个卷轴
            hbox:
                xalign 0.5 spacing 20

                for _ri in range(3):
                    frame:
                        xsize 120 ysize 120
                        background Solid("#1a1a3a")
                        padding (4, 4)

                        if sm.spinning:
                            text "?" align (0.5, 0.5) size 50 color "#ffd700"
                        else:
                            $ _sym = sm.reels[_ri]
                            text "[_sym]" align (0.5, 0.5) size 50

            # 结果
            if sm.result_msg:
                text "[sm.result_msg]" size 16 color sm.result_color xalign 0.5 bold True

    # 费用说明
    frame:
        xalign 0.5 yalign 0.68
        background Solid("#00000066")
        padding (20, 6)
        text "每次消耗 [SLOT_COST] 睦币" size 12 color "#ffffff66"

    # 拉杆按钮
    if not sm.spinning:
        button:
            xalign 0.5 yalign 0.78
            xsize 200 ysize 50
            background Solid("#ffd700" if _sm_coins >= SLOT_COST else "#333333")
            hover_background Solid("#ffee88" if _sm_coins >= SLOT_COST else "#333333")
            action Function(sm.spin)
            sensitive (_sm_coins >= SLOT_COST)
            text "拉杆！" align (0.5, 0.5) size 20 color "#1a1a2e" bold True
    else:
        frame:
            xalign 0.5 yalign 0.78
            xsize 200 ysize 50
            background Solid("#333333")
            text "转动中..." align (0.5, 0.5) size 18 color "#ffffff44"

    # 统计
    frame:
        xalign 0.5 yalign 0.9
        background None
        padding (0, 0)
        hbox:
            spacing 30
            text "转了 [sm.total_spins] 次" size 11 color "#ffffff44"
            text "赢了 [sm.total_won] 睦币" size 11 color "#ffd70088"

    # 退出
    textbutton "退出" xalign 0.98 yalign 0.98 text_size 12 text_color "#ffffff44" text_hover_color "#ff6666" action Return()

    # 赔率说明
    frame:
        xpos 30 yalign 0.92
        background Solid("#ffffff08")
        padding (10, 6)
        vbox:
            spacing 2
            text "赔率表" size 9 color "#ffffff44"
            text "三连🥒 = 100币" size 8 color "#ffd700"
            text "三连★ = 50币" size 8 color "#ffd700"
            text "其他三连 = 30币" size 8 color "#95e1d3"
            text "两连 = 8币" size 8 color "#ffffffaa"
