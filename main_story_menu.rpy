# ==========================================================
# 📚 睦の藏书阁 - 书架与多线剧情系统
init python:
    library_books = [
        {
            "id": "main_story",
            "title": "君与若叶睦的镜中坠落", 
            "subtitle": "Main Story",
            "color": "#2f3a2f", 
            "is_locked": False
        },
        {
            "id": "side_story_love",
            "title": "番外：\n恋后时光",
            "subtitle": "After Story",
            "color": "#8b4513", 
            "is_locked": True 
        },
        {
            "id": "side_story_if",
            "title": "IF线：\n假如...",
            "subtitle": "What If?",
            "color": "#483d8b", 
            "is_locked": True 
        }
    ]

    # --- 章节内容数据 (Ave Mujica 救赎线重置版) ---
    
    book_content_main = [
        # 序章保持不变：压抑的开端
        {"type": "header", "text": "序章： Down the Rabbit Hole —— 土中之呼吸 (De Profundis)"},
        {"type": "chap", "label": "op_stage_1", "name": "土中之呼吸 · 起", "req": 0},
        {"type": "chap", "label": "prologue_part2", "name": "土中之呼吸 · 承", "req": 20},
        {"type": "chap", "label": "prologue_part3", "name": "土中之呼吸 · 展", "req": 35},
        {"type": "chap", "label": "prologue_part4", "name": "土中之呼吸 · 转", "req": 50},
        {"type": "chap", "label": "prologue_part5", "name": "土中之呼吸 · 合", "req": 30001},
        
        # 第一章：八幡海铃 (Timoris - 恐惧) / 核心：看透伪装的无声接纳
        {"type": "header", "text": "第一章：Timoris —— 无声者的沉锚 (The Silent Anchor)"},
        {"type": "chap", "label": "chap1_1", "name": "无声者的沉锚 · 潜", "req": 30001}, # 潜入地下Livehouse
        {"type": "chap", "label": "chap1_2", "name": "无声者的沉锚 · 窥", "req": 30001}, # 海铃窥破墨缇斯的伪装
        {"type": "chap", "label": "chap1_3", "name": "无声者的沉锚 · 拆", "req": 30001}, # 拆解防备
        {"type": "chap", "label": "chap1_4", "name": "无声者的沉锚 · 容", "req": 30001}, # “坏掉了也没关系”的包容
        {"type": "chap", "label": "chap1_5", "name": "无声者的沉锚 · 泊", "req": 30001}, # 获得第一个现实锚点

        # 第二章：祐天寺若麦 (Amoris - 爱) / 核心：强硬闯入的鲜活色彩
        {"type": "header", "text": "第二章：Amoris —— 狂热的失序色彩 (Feverish Colors)"},
        {"type": "chap", "label": "chap2_1", "name": "狂热的失序色彩 · 噪", "req": 30001}, # 喧闹的街头，墨缇斯嫌吵
        {"type": "chap", "label": "chap2_2", "name": "狂热的失序色彩 · 曳", "req": 30001}, # 被若麦强行拉着跑(拖曳)
        {"type": "chap", "label": "chap2_3", "name": "狂热的失序色彩 · 悖", "req": 30001}, # 违背悲剧剧本的日常
        {"type": "chap", "label": "chap2_4", "name": "狂热的失序色彩 · 绚", "req": 30001}, # 属于她自己的色彩
        {"type": "chap", "label": "chap2_5", "name": "狂热的失序色彩 · 霁", "req": 30001}, # 阴霾散去，第一次感到轻松

        # 第三章：三角初华 (Doloris - 悲痛) / 核心：同类之间的镜像共振
        {"type": "header", "text": "第三章：Doloris —— 悲叹的同面之镜 (Mirror of Sorrow)"},
        {"type": "chap", "label": "chap3_1", "name": "悲叹的同面之镜 · 寻", "req": 30001}, # 寻访仰望星空的初华
        {"type": "chap", "label": "chap3_2", "name": "悲叹的同面之镜 · 饰", "req": 30001}, # 两人都在“粉饰”太平
        {"type": "chap", "label": "chap3_3", "name": "悲叹的同面之镜 · 碎", "req": 30001}, # 坦白局，面具破碎
        {"type": "chap", "label": "chap3_4", "name": "悲叹的同面之镜 · 诉", "req": 30001}, # 睦第一次诉说“我也好疼”
        {"type": "chap", "label": "chap3_5", "name": "悲叹的同面之镜 · 鸣", "req": 30001}, # 灵魂深处的共鸣

        # 第四章：丰川祥子 (Oblivionis - 忘却) / 核心：斩断共生，剥离宿命
        {"type": "header", "text": "第四章：Oblivionis —— 忘却的宿命剪影 (Silhouette of Oblivion)"},
        {"type": "chap", "label": "chap4_1", "name": "忘却的宿命剪影 · 渊", "req": 30001}, # 直面最深的创伤（祥子）
        {"type": "chap", "label": "chap4_2", "name": "忘却的宿命剪影 · 缚", "req": 30001}, # 祥子试图用过去的羁绊束缚她
        {"type": "chap", "label": "chap4_3", "name": "忘却的宿命剪影 · 峙", "req": 30001}, # 主角作为墙壁，睦压制墨缇斯上前对峙
        {"type": "chap", "label": "chap4_4", "name": "忘却的宿命剪影 · 决", "req": 30001}, # 决断：“从来没有开心过”
        {"type": "chap", "label": "chap4_5", "name": "忘却的宿命剪影 · 涅", "req": 30001}, # 涅槃，彻底完成对祥子的独立

        # 第五章保持原样：内心的最终试炼
        {"type": "header", "text": "第五章： Singularity —— 毁灭与再生的二重奏 (Duo)"},
        {"type": "chap", "label": "chap5_1", "name": "毁灭与再生的二重奏 · 暮", "req": 30001}, # 暮色降临，内心世界崩塌
        {"type": "chap", "label": "chap5_2", "name": "毁灭与再生的二重奏 · 毣", "req": 30001}, # 毣 (迷惘/孤独)
        {"type": "chap", "label": "chap5_3", "name": "毁灭与再生的二重奏 · 沐", "req": 30001}, # 沐 (主角杀入内心世界的洗礼)
        {"type": "chap", "label": "chap5_4", "name": "毁灭与再生的二重奏 · 苜", "req": 30001}, # 苜 (找回最初的自己/黄瓜)
        {"type": "chap", "label": "chap5_5", "name": "毁灭与再生的二重奏 · 睦", "req": 30001}, # 睦 (和解，双重人格拥抱)

        # 后日谈保持原样
        {"type": "header", "text": "后日谈： It’s a Wonderful Everyday —— 致亲爱的[player] (Curtain Call)"},
        {"type": "chap", "label": "epilogue_1", "name": "美好的每一天 · 若叶睦（吉他睦）", "req": 30001},
        {"type": "chap", "label": "epilogue_2", "name": "美好的每一天 · 若叶睦（墨缇斯）", "req": 30001},
        {"type": "chap", "label": "epilogue_3", "name": "美好的每一天 · 若叶睦（苦瓜睦）", "req": 30001},
    ]

    book_content_side = [
        {"type": "header", "text": "甜蜜日常篇 (Coming Soon)"},
        {"type": "chap", "label": "date_01", "name": "第一次约会", "req": 999}, 
    ]

    def get_book_content(book_id):
        if book_id == "main_story":
            return book_content_main
        elif book_id == "side_story_love":
            return book_content_side
        else:
            return [] 

# ------------------------------------------------------------------
# 2. 样式与动画定义 (Style & Transform)
# ------------------------------------------------------------------

define gui.serif_font = "gui/font/SourceHanSerifCN-Bold.otf"

style bookshelf_bg is frame:
    background Solid("#1a1a1a") 
    xfill True yfill True

style book_spine_button is button:
    xsize 160 ysize 500
    background Frame(Solid("#fff"), 0, 0) 
    hover_yoffset -20 
    padding (15, 30)

style book_title_text is text:
    font gui.serif_font
    size 28
    color "#e6e6e6" 
    vertical True 
    xalign 0.5 yalign 0.1
    outlines [] 

# --- 滚动条样式 ---
style diary_vscrollbar is vscrollbar:
    xsize 8 
    base_bar Frame(Solid("#e0e0e0"), 0, 0) 
    thumb Frame(Solid("#8fbc8f"), 0, 0) 
    unscrollable "hide" 


# 1. 书架进场动画：整体稍微向上浮动并淡入
transform slide_up_fade:
    on show:
        alpha 0.0 yoffset 50
        easein 0.5 alpha 1.0 yoffset 0

# 2. 纸张展开动画：像翻开书一样稍微放大淡入
transform paper_open_effect:
    on show:
        alpha 0.0 zoom 0.95
        easein 0.3 alpha 1.0 zoom 1.0
    on hide:
        easeout 0.2 alpha 0.0 zoom 0.95


# 3. 界面 I：书架总览

screen bookshelf_menu():
    tag menu
    modal True

    add Solid("#0f1215")
    
    text "Mutsumi's Library":
        font gui.serif_font
        size 60
        color "#ffffff10" 
        align (0.5, 0.04)
        outlines []
        # 给标题也加一点点延迟显示的动画
        at transform:
            alpha 0.0
            pause 0.2
            easein 0.5 alpha 1.0
    
    text "我们的回忆":
        font gui.serif_font
        size 40
        color "#8fbc8f"
        align (0.5, 0.08)
        outlines []
        at transform:
            alpha 0.0
            pause 0.3
            easein 0.5 alpha 1.0

    hbox:
        align (0.5, 0.60)
        spacing 40
        
        at slide_up_fade

        for book in library_books:
            
            button:
                style "book_spine_button"
                background Frame(Solid(book["color"]), 0, 0)
                hover_background Frame(Solid(book["color"]), 0, 0) 
                
                at transform:
                    on hover:
                        linear 0.2 yoffset -20 matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0.1)
                    on idle:
                        linear 0.2 yoffset 0 matrixcolor IdentityMatrix()

                action [
                    If(not book["is_locked"],
                        # 【修改】加入 transition=dissolve 让打开书本更柔和
                        true=Show("book_content_view", transition=dissolve, current_book=book), 
                        false=Notify("这本书现在还打不开...（开发中）")
                    )
                ]

                vbox:
                    xfill True yfill True
                    add Solid("#cca3a3") xsize 4 ysize 40 xalign 0.5 alpha 0.5
                    null height 20

                    text book["title"]:
                        style "book_title_text"
                        layout "subtitle" 
                        text_align 0.5

                    text book["subtitle"]:
                        font gui.serif_font
                        size 14
                        color "#ffffff60"
                        xalign 0.5
                        yalign 1.0
                        vertical False 
                
                if book["is_locked"]:
                    frame:
                        background Solid("#00000080")
                        xfill True yfill True
                        align (0.5, 0.5)
                        text "🔒":
                            size 40
                            align (0.5, 0.15)
                            color "#ffffff80"

    # ── 对话回顾入口 ──
    button:
        align (0.5, 0.88)
        xsize 240 ysize 44
        background Solid("#d4a0ff22")
        hover_background Solid("#d4a0ff44")
        action Show("dialogue_replay_screen", transition=dissolve)
        at transform:
            alpha 0.0
            pause 0.4
            easein 0.5 alpha 1.0
        hbox:
            align (0.5, 0.5) spacing 10
            text "▶" size 14 color "#d4a0ff" yalign 0.5
            text "对话回顾" size 16 color "#d4a0ff" bold True yalign 0.5
            $ _rpf, _rpt = get_dialogue_progress()
            text "([_rpf]/[_rpt])" size 12 color "#d4a0ff88" yalign 0.5

    textbutton "退出睦の日记":
        align (0.5, 0.95)
        text_font gui.serif_font
        text_color "#666"
        text_hover_color "#fff"
        # 【修改】加入 With(dissolve) 让退出过程有淡出效果
        action [Return(), With(dissolve)]



screen book_content_view(current_book):
    tag menu # 保持 tag menu，确保它会替换书架
    modal True

    add Solid("#000000cc")
    
    frame:
        background Frame(Solid("#fdfbf7"), 0, 0)
        xsize 960 ysize 700
        align (0.5, 0.5)
        
        # 应用纸张展开动画
        at paper_open_effect
        
        $ content_list = get_book_content(current_book["id"])
        
        vbox:
            xfill True
            null height 40

            # --- 书籍抬头 ---
            hbox:
                xfill True
                yalign 0.5
                null width 50

                textbutton "← 返回书架":
                    text_font gui.serif_font
                    text_color "#8fbc8f"
                    text_hover_color "#556b2f"
                    text_outlines [] 
                    
                    # 【核心修复】: 
                    # 不要用 Hide，因为书架已经被替换掉了。
                    # 改用 Show("bookshelf_menu") 重新呼唤书架，它会自动替换掉当前这本书。
                    action Show("bookshelf_menu", transition=dissolve)

                null width 350

                text current_book["title"].replace("\n", " "): 
                    font gui.serif_font
                    size 30
                    color "#2f3a2f"
                    outlines [] 
                    xalign 1.0
                    yalign 0.5

            null height 10

            add Solid("#556b2f80") xsize 860 ysize 2 xalign 0.5

            null height 20

            # --- 内容列表 ---
            side "c r":
                xsize 880 
                ysize 520
                xalign 0.5 
                
                viewport id "book_vp":
                    draggable True
                    mousewheel True
                    
                    vbox:
                        spacing 15
                        xfill True
                        
                        if not content_list:
                            text "（这是一本无字天书……暂时没有内容）" font gui.serif_font color "#aaa" xalign 0.5 yoffset 200 outlines []

                        for item in content_list:
                            
                            if item["type"] == "header":
                                null height 10
                                text item["text"]:
                                    font gui.serif_font
                                    size 22
                                    color "#556b2f"
                                    outlines [] 
                                add Solid("#ddd") xsize 400 ysize 1
                            
                            elif item["type"] == "chap":
                                $ is_unlocked = persistent.gw_total >= item["req"]
                                
                                button:
                                    xfill True
                                    background None
                                    ysize 40
                                    action [
                                        If(is_unlocked,
                                            true=[SetVariable("main_story_mode", True), Jump(item["label"])],
                                            false=Notify("灵感（好感度）不足...")
                                        )
                                    ]
                                    
                                    hbox:
                                        spacing 15
                                        yalign 0.5
                                        
                                        if is_unlocked:
                                            text "●" size 14 color "#2f3a2f" yalign 0.5 outlines []
                                            text item["name"]:
                                                font gui.serif_font 
                                                size 20 
                                                color "#333" 
                                                hover_color "#000"
                                                outlines [] 
                                        else:
                                            text "○" size 14 color "#ccc" yalign 0.5 outlines []
                                            text "Locked Content":
                                                font gui.serif_font 
                                                size 20 
                                                color "#ccc"
                                                outlines []
                                            text "(Req. [item['req']])":
                                                font gui.serif_font 
                                                size 14 
                                                color "#eee" 
                                                yalign 0.5
                                                outlines []

                # --- 滚动条 ---
                vbar value YScrollValue("book_vp") style "diary_vscrollbar"

# ------------------------------------------------------------------
# 5. 入口跳转
# ------------------------------------------------------------------

label open_mutsumi_diary:
    hide screen phone_system
    hide screen main_interaction_ui
    $ quick_menu = False
    
    # 【修改】使用 dissolve 过渡进入书架，避免生硬跳出
    call screen bookshelf_menu with dissolve
    
    $ quick_menu = True
    show screen phone_system
    show screen main_interaction_ui
    jump sjdh