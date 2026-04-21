# ==============================================================================
# 🎧 白噪音 — Immersive Companion
# 环境音播放器，嵌入手机
# 注意：音频文件需要实际存在才能播放，目前用占位路径
# ==============================================================================

default persistent.wn_current = ""
default persistent.wn_volume = 0.5

init python:
    import random as _wn_rng
    import time as _wn_time

    _WN_CHANNELS = [
        {
            "id": "rain",
            "name": "雨声",
            "desc": "温室外淅淅沥沥的雨",
            "file": "audio/wn_rain.ogg",
            "color": "#4a8aee",
            "icon": "R",
        },
        {
            "id": "greenhouse",
            "name": "温室",
            "desc": "植物生长的细微声响",
            "file": "audio/wn_greenhouse.ogg",
            "color": "#22AA44",
            "icon": "G",
        },
        {
            "id": "night",
            "name": "夜晚",
            "desc": "虫鸣与微风",
            "file": "audio/wn_night.ogg",
            "color": "#6a5acd",
            "icon": "N",
        },
        {
            "id": "keyboard",
            "name": "键盘声",
            "desc": "指尖敲击的节奏",
            "file": "audio/wn_keyboard.ogg",
            "color": "#CC9900",
            "icon": "K",
        },
        {
            "id": "guitar",
            "name": "吉他调弦",
            "desc": "睦在调吉他的声音",
            "file": "audio/wn_guitar.ogg",
            "color": "#CC4444",
            "icon": "M",
        },
    ]

    def wn_play(channel_id):
        for ch in _WN_CHANNELS:
            if ch["id"] == channel_id:
                try:
                    if renpy.loadable(ch["file"]):
                        renpy.music.play(ch["file"], channel="music", loop=True, fadein=2.0)
                        persistent.wn_current = channel_id
                    else:
                        persistent.wn_current = channel_id
                        renpy.notify("音频文件待添加")
                except:
                    persistent.wn_current = channel_id
                    renpy.notify("音频文件待添加")
                renpy.save_persistent()
                renpy.restart_interaction()
                return

    def wn_stop():
        renpy.music.stop(channel="music", fadeout=2.0)
        persistent.wn_current = ""
        renpy.save_persistent()
        renpy.restart_interaction()


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_whitenoise():
    $ _wn_cur = persistent.wn_current or ""
    $ _wn_playing = bool(_wn_cur)

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 80
            background Solid("#1a1e2a")
            padding (14, 10)

            vbox:
                spacing 4
                text "白噪音" size 14 color "#6a5acd" bold True
                text "Immersive Companion" size 8 color "#ffffff44"
                null height 4
                if _wn_playing:
                    hbox:
                        spacing 8
                        frame:
                            xsize 6 ysize 6
                            background Solid("#6a5acd")
                        $ _wn_cname = ""
                        python:
                            for _wch in _WN_CHANNELS:
                                if _wch["id"] == _wn_cur:
                                    _wn_cname = _wch["name"]
                        text "正在播放: [_wn_cname]" size 11 color "#ffffffaa"
                else:
                    text "选择一个频道开始" size 11 color "#ffffff44"

        # 频道列表
        viewport:
            ypos 84 ysize 380
            xfill True mousewheel True scrollbars None

            vbox:
                spacing 6 xfill True
                null height 6

                for _wi in range(len(_WN_CHANNELS)):
                    $ _wch = _WN_CHANNELS[_wi]
                    $ _wid = _wch["id"]
                    $ _wname = _wch["name"]
                    $ _wdesc = _wch["desc"]
                    $ _wcolor = _wch["color"]
                    $ _wicon = _wch["icon"]
                    $ _wactive = (_wn_cur == _wid)
                    $ _wbg = _wcolor + "22" if _wactive else "#0d101888"

                    button:
                        xfill True ysize 72
                        background Solid(_wbg)
                        hover_background Solid(_wcolor + "11")
                        if _wactive:
                            action Function(wn_stop)
                        else:
                            action Function(wn_play, _wid)

                        hbox:
                            spacing 12 yalign 0.5
                            xoffset 14

                            # 图标
                            frame:
                                xsize 40 ysize 40
                                background Solid(_wcolor if _wactive else _wcolor + "66")
                                text "[_wicon]" align (0.5, 0.5) size 18 color "#ffffff" bold True font "DejaVuSans.ttf"

                            vbox:
                                spacing 3 yalign 0.5
                                text "[_wname]" size 14 color ("#ffffff" if _wactive else "#ffffffcc")
                                text "[_wdesc]" size 10 color "#ffffff55"

                            if _wactive:
                                text "播放中" size 10 color _wcolor xalign 1.0 yalign 0.5 xoffset -14

        # 音量控制
        frame:
            ypos 468 xfill True ysize 46
            background Solid("#0d1018")
            padding (14, 8)
            hbox:
                spacing 8 xfill True yalign 0.5
                text "♪" size 12 color "#6a5acd" yalign 0.5
                bar value Preference("music volume") xsize 220 ysize 3 yalign 0.5 left_bar Solid("#6a5acd") right_bar Solid("#ffffff10") thumb None

        # 底部
        frame:
            ypos 518 xfill True ysize 50
            background Solid("#0a0a14")
            padding (12, 6)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)
