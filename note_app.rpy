# --- 1. 动画定义：组合了位移、淡入淡出和轻微缩放 ---
transform note_app_animation:
    on show:
        # 进场：从下方 100 像素处滑入，伴随淡入和轻微放大
        yoffset 100 alpha 0.0 zoom 0.98
        easein_cubic 0.4 yoffset 0 alpha 1.0 zoom 1.0
    on hide:
        # 退场：向下方滑落并淡出，轻微缩小
        easeout_cubic 0.4 yoffset 100 alpha 0.0 zoom 0.98

init python:
    # 初始化持久化变量
    if persistent.player_notes is None:
        persistent.player_notes = []

    def add_new_note():
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_note = {"title": "无名刻痕", "content": " ", "date": now}
        persistent.player_notes.insert(0, new_note)
        renpy.save_persistent()
        renpy.restart_interaction()

screen note_app():
    modal True
    zorder 300
    
    default focus_target = 1
    default current_edit = 0
    
    $ M_DEEP = "#2d3a2d" 
    $ M_SOFT = "#769176" 
    $ M_PAPER = "#fdfdfd" 

    # 快捷键逻辑
    key "K_TAB" action If(focus_target == 1, SetScreenVariable("focus_target", 2), SetScreenVariable("focus_target", 1))
    
    if focus_target == 2 and persistent.player_notes:
        $ current_note = persistent.player_notes[current_edit]
        key "K_RETURN" action [SetDict(current_note, "content", current_note["content"] + "\n"), Function(renpy.save_persistent)]
        key "K_KP_ENTER" action [SetDict(current_note, "content", current_note["content"] + "\n"), Function(renpy.save_persistent)]

    # 遮罩层背景
    fixed:
        # 这里的遮罩也建议加一个淡入淡出，防止背景黑影闪现
        add Solid("#1a201af2") at d_fade 

        frame:
            # --- 💡 关键：应用动画 ---
            at note_app_animation 
            
            # -----------------------------------------------------------
            # 【修改开始】手机端键盘避让逻辑
            # -----------------------------------------------------------
            # 如果是 (手机端) 并且 (正在编辑正文/focus_target==2)
            if renpy.variant("touch") and focus_target == 2:
                # 强制靠上对齐 (yalign 0.05)，给下面腾出空间放键盘
                align (0.5, 0.05) 
            else:
                # 电脑端，或者没在输入时，保持居中
                align (0.5, 0.5)
            # -----------------------------------------------------------

            xsize 1120 ysize 780
            background Solid(M_PAPER)
            padding (40, 40)

        frame:
            # --- 💡 关键：应用动画 ---
            at note_app_animation 
            
            align (0.5, 0.5)
            xsize 1120 ysize 780
            background Solid(M_PAPER)
            padding (40, 40)

            # 返回按钮：点击时会触发 on hide 动画
            textbutton "返回":
                action [Function(renpy.save_persistent), Hide("note_app")]
                align (1.0, 0.0)
                background Solid(M_DEEP)
                padding (15, 8)
                text_color "#ffffff" text_size 20 text_outlines []

            hbox:
                spacing 45
                
                # --- 左侧栏 ---
                vbox:
                    xsize 300
                    spacing 15
                    frame:
                        background Solid(M_SOFT + "11")
                        padding (15, 15)
                        xfill True
                        vbox:
                            spacing 8
                            text "〖 使用说明 〗" size 18 color M_DEEP bold True outlines []
                            text "• [[Tab]] 键切换输入位置" size 14 color M_SOFT outlines []
                            $ current_label = "标题" if focus_target == 1 else "正文"
                            text "• 当前位置：[current_label]" size 16 color "#d14" bold True outlines []

                    add Solid("#e0e8e0") ysize 2 
                    text "存证目录" size 22 color M_DEEP bold True outlines []
                    textbutton "＋ 新增刻痕" action Function(add_new_note) text_size 20 text_color M_SOFT text_outlines []

                    viewport:
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 10
                            for idx, note in enumerate(persistent.player_notes):
                                $ is_sel = (current_edit == idx)
                                button:
                                    xfill True ysize 60
                                    background (Solid(M_SOFT + "22") if is_sel else Solid("#00000005"))
                                    action [Function(renpy.save_persistent), SetScreenVariable("current_edit", idx), SetScreenVariable("focus_target", 1)]
                                    # 修复变量显示逻辑
                                    $ title_text = note.get("title", "无标题")[:10]
                                    text "[title_text]" color (M_DEEP if is_sel else "#7f8c8d") size 16 outlines [] align (0.0, 0.5) xoffset 10

                # --- 右侧编辑区 ---
                if persistent.player_notes:
                    # 确保索引安全
                    $ safe_idx = min(current_edit, len(persistent.player_notes)-1)
                    $ active_note = persistent.player_notes[safe_idx]
                    
                    vbox:
                        xsize 680
                        spacing 15
                        
                        if focus_target == 1:
                            input:
                                value DictInputValue(active_note, "title")
                                size 32 color M_DEEP bold True outlines [(1, "#ffffff88")]
                                default_focus True
                        else:
                            $ title_val = active_note.get("title", "")
                            text "[title_val]" size 32 color M_DEEP bold True outlines [(1, "#ffffff88")]

                        add Solid("#e0e8e0") ysize 1
                        $ d_val = active_note.get('date', '')
                        text "时间: [d_val]" size 14 color M_SOFT outlines []

                        frame:
                            xfill True ysize 450
                            background Solid("#fbfbfb")
                            padding (20, 20)
                            
                            if focus_target == 2:
                                fixed:
                                    xsize 640
                                    input:
                                        value DictInputValue(active_note, "content")
                                        multiline True
                                        size 24 color "#444444"
                                        line_spacing 8
                                        outlines []
                                        default_focus True
                            else:
                                viewport:
                                    mousewheel True
                                    draggable True
                                    $ content_val = active_note.get("content", "...")
                                    text "[content_val]" size 24 color "#444444" line_spacing 8 outlines []

                        textbutton "抹除此段存证":
                            action Confirm("确定抹除？", [Function(persistent.player_notes.pop, safe_idx), Function(renpy.save_persistent), SetScreenVariable("current_edit", 0)])
                            text_size 16 text_color M_SOFT xalign 1.0 text_outlines []

# 辅助动画：背景遮罩淡入淡出
transform d_fade:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

