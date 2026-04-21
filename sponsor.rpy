init python:
    def get_sponsors():
        """
        在这里直接管理赞助者名单。
        每次修改后，Ren'Py 重新启动即可生效。
        """
        
        # 【资深培育者】 - 高档赞助
        high_tier = [
            "铃音SuzuneOfficial",
            "Y0ung杨杨杨杨",
            "梦溪沈谈",
        ]
        
        # 【暖心园丁】 - 基础赞助
        base_tier = [
            "Zephyria_Yoshino",
            
        ]
        
        # 【自由资助者】 - 自定义赞助
        # 格式为: ("名字", 金额)
        custom_data = [
            ("motis_nartiaa", 12),
            ("XYKerman", 6.32),
            ("晓歌的压裙刀", 2.04),
        ]
        
        # 自动逻辑：按金额排序并提取名字
        custom_data.sort(key=lambda x: x[1], reverse=True)
        final_custom = [x[0] for x in custom_data]
        
        return high_tier, base_tier, final_custom

# --- 2. 动画效果定义 ---
transform sponsor_master_transform:
    on show:
        alpha 0.0 yoffset 100
        easein_back 0.8 alpha 1.0 yoffset 0
    on hide:
        parallel:
            easeout_quint 0.6 alpha 0.0
        parallel:
            easeout_back 0.6 xoffset 200 zoom 0.9 blur 10

# --- 3. 界面布局 ---
screen sponsor_list():
    modal True
    zorder 200
    
    # 界面私有变量
    default high_list = []
    default base_list = []
    default custom_list = []

    # 界面显示时加载数据
    on "show" action [
        SetScreenVariable("high_list", get_sponsors()[0]),
        SetScreenVariable("base_list", get_sponsors()[1]),
        SetScreenVariable("custom_list", get_sponsors()[2])
    ]

    # 背景遮罩
    add Solid("#00000088") 

    fixed:
        at sponsor_master_transform

        frame:
            align (0.5, 0.5)
            xsize 650 ysize 750
            # 使用半透明深绿色调，贴合睦的温室风格
            background Frame(Window(Solid("#1a261af2")), 15, 15)
            padding (40, 40)

            # 右上角关闭按钮
            textbutton "×":
                align (1.0, 0.0)
                action Hide("sponsor_list")
                text_size 45
                text_color "#ffffff66"
                text_hover_color "#ff6666"
                offset (20, -20)

            vbox:
                spacing 20
                text "温 室 园 丁 名 录" size 30 color "#ffffff" xalign 0.5 bold True
                
                null height 10
                add Solid("#ffffff22") ysize 2 
                null height 10

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    
                    vbox:
                        spacing 35
                        xfill True

                        # --- 高档赞助 ---
                        vbox:
                            spacing 12
                            text "【 资深培育者 】" color "#ffd700" size 24 bold True 
                            if not high_list:
                                text " ……暂时，还没有人。" color "#ffffff44" size 18 xoffset 20
                            else:
                                for name in high_list:
                                    text "🌱 " + name color "#ffffff" size 22 xoffset 20

                        # --- 基础赞助 ---
                        vbox:
                            spacing 12
                            text "【 暖心园丁 】" color "#ffffffcc" size 24 bold True
                            if not base_list:
                                text " ……空荡荡的。" color "#ffffff44" size 18 xoffset 20
                            else:
                                for name in base_list:
                                    text "☘️ " + name color "#ffffff" size 22 xoffset 20

                        # --- 自定义赞助 ---
                        vbox:
                            spacing 12
                            text "【 自由资助者 】" color "#ffffff88" size 24 bold True
                            if not custom_list:
                                text " ……只有风吹过。" color "#ffffff44" size 18 xoffset 20
                            else:
                                for name in custom_list:
                                    text "🍃 " + name color "#ffffff" size 20 xoffset 20

                null height 20
                
                # 底部关闭按钮
                textbutton "离开温室":
                    action Hide("sponsor_list")
                    xalign 0.5
                    text_size 22 
                    text_color "#ffffffaa"
                    text_hover_color "#ff6666"
                    background Solid("#ffffff11")
                    padding (20, 10)

# ============================================================