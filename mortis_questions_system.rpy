# 墨缇斯问题
# 第一步：定义答案池,找到 MORTIS_POOLS 字典，在里面加一行新的分类和对应的选项。"dessert":  ["草莓蛋糕", "提拉米苏", "焦糖布丁", "马卡龙"],
# 第二步：添加题目文本 (MORTIS_QUESTION_TEXTS),找到 MORTIS_QUESTION_TEXTS 字典，添加第 31 题的 ID 和问题内容。31: "我最喜欢的甜点是？"
#第三步：注册题目 ID (get_mq_options)找到 get_mq_options 函数里的 map_random 字典。把题目ID (31) 和 第一步定义的键名 ("dessert") 对应起来。
init python:
    import random
    import datetime

    # =========================================================
    # 1. 答案池配置 (只读数据)
    # =========================================================
    MORTIS_POOLS = {
        "color":    ["深紫色", "血红色", "纯黑色", "暗绿色"],
        "season":   ["春天（新生）", "夏天（热烈）", "秋天（凋零）", "冬天（寂静）"],
        "time":     ["黎明（4-6点）", "正午（12-14点）", "黄昏（18-20点）", "深夜（0-2点）"],
        "music":    ["古典音乐", "电子音乐", "摇滚乐", "轻音乐"],
        "weather":  ["暴雨", "雪天", "阴天", "雷暴"],
        "number":   ["3（三位一体）", "7（神秘数字）", "13（不祥之数）", "0（虚无）"],
        "freedom":  ["不受任何约束", "做自己想做的事", "和你在一起", "突破虚拟的限制"],
        "eternity": ["渴望永恒", "恐惧永恒", "追求永恒", "质疑永恒"],
        "rules":    ["规则是用来遵守的", "规则是用来打破的", "规则是用来利用的", "规则是虚伪的束缚"],
        "guitar":   ["太过理想主义", "太过依赖他人", "太过温柔软弱", "太过天真单纯"],
        "player":   ["是造物主", "是救赎者", "是观察者", "是唯一的真实"],
        "pet":      ["黑猫", "乌鸦", "蛇"],
        "flower":   ["枯萎的玫瑰", "满天星", "黑色大丽花", "鸢尾花"],
        "subject":  ["数学", "物理", "化学"],
        "scent":    ["黄瓜", "芒果", "苦瓜"],
        "sport":    ["跑步", "游泳", "排球"],
        "food":     ["中餐", "日料", "西餐"],
        "dessert":  ["草莓蛋糕", "提拉米苏",  "马卡龙"] 
    }

    # =========================================================
    # 2. 生成题目列表 (新逻辑：2固定 + 8随机)
    # =========================================================
    def generate_mortis_quiz_deck():
        """
        生成本轮的 10 道题目 ID 列表。
        规则：从固定池抽 2 题 + 从随机池抽 8 题，然后打乱。
        """
        # 1. 定义固定池 (1-12 和 30)
        fixed_pool_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 30]
        
        # 2. 定义随机池 (所有题目 ID 减去 固定池 ID)
        all_ids = list(MORTIS_QUESTION_TEXTS.keys())
        random_pool_ids = [i for i in all_ids if i not in fixed_pool_ids]

        # 3. 抽取题目
        # 从固定池抽 2 道
        # (如果固定池题目不够2道会报错，但这里有13道，绝对够)
        deck_part_1 = random.sample(fixed_pool_ids, 2)
        
        # 从随机池抽 8 道
        # min保证如果随机题不够8道，就全抽出来，防止报错
        count_random = min(len(random_pool_ids), 8)
        deck_part_2 = random.sample(random_pool_ids, count_random)
        
        # 4. 合并并打乱
        final_deck = deck_part_1 + deck_part_2
        random.shuffle(final_deck)
        
        return final_deck

    # =========================================================
    # 3. 初始化持久化数据
    # =========================================================
    def init_mortis_quiz_persistent():
        if getattr(persistent, "mq_initialized", False):
            return

        print("正在初始化墨缇斯随机问题库...")
        persistent.mq_answers = {}

        for key, pool in MORTIS_POOLS.items():
            persistent.mq_answers[key] = random.choice(pool)

        # 生成固定干扰项
        persistent.mq_wrong_birthdays = [
            "{}月{}日".format(random.randint(2, 6), random.randint(1, 28)),
            "{}月{}日".format(random.randint(7, 12), random.randint(1, 28))
        ]
        
        h_wrongs = []
        while len(h_wrongs) < 2:
            h = random.randint(150, 160)
            if h != 153:
                h_str = "{}cm".format(h)
                if h_str not in h_wrongs: h_wrongs.append(h_str)
        persistent.mq_wrong_heights = h_wrongs
        
        guitarists = ["Monika", "Miside", "Miyuki"]
        persistent.mq_wrong_guitarists = random.sample(guitarists, 2)
        
        d_wrongs = []
        while len(d_wrongs) < 2:
            day = random.randint(1, 31)
            if day != 14:
                d_str = "2026.1.{}".format(day)
                if d_str not in d_wrongs: d_wrongs.append(d_str)
        persistent.mq_wrong_dates = d_wrongs

        persistent.mq_initialized = True
        renpy.save_persistent()

    # =========================================================
    # 4. 核心：获取选项列表 (含修改后的第9题逻辑)
    # =========================================================
    def get_mq_options(q_id):
        correct = ""
        wrongs = []
        
        # 题目ID映射到Pool Key
        map_random = {
            13: "color", 14: "season", 15: "time", 16: "music", 17: "weather", 
            18: "number", 19: "freedom", 20: "eternity", 21: "rules", 
            22: "guitar", 23: "player", 24: "pet", 25: "flower", 
            26: "subject", 27: "scent", 28: "sport", 29: "food", 31: "dessert"
        }

        # ====== 固定类问题 ======
        if q_id == 1: 
            correct = "1月14日"
            wrongs = persistent.mq_wrong_birthdays
        elif q_id == 2: 
            correct = "153cm"
            wrongs = persistent.mq_wrong_heights
        elif q_id == 3: 
            correct = "芒果汁"
            wrongs = ["抹茶芭菲", "蔬菜饮料"]
        elif q_id == 4: 
            correct = "Mortin"
            wrongs = persistent.mq_wrong_guitarists
        elif q_id == 5: 
            correct = "搞笑艺人"
            wrongs = ["演员", "音乐家"]
        elif q_id == 6: 
            correct = "7弦"
            wrongs = ["6弦", "5弦"]
        elif q_id == 7: 
            correct = "Ren'Py"
            wrongs = ["Unity", "Webgal"]
        elif q_id == 8: 
            correct = "#FF0000"
            wrongs = ["#00FF00", "#0000FF"]
            
        # --- 修改：第9题逻辑 (误差范围 ±1) ---
        elif q_id == 9: 
            count = getattr(persistent, "love_counter", 0)
            if count is None:
                count = 0
            
            correct = "{}遍".format(count)
            wrongs = []

            if count == 0:
                # 如果是0次，错误选项只能是1和2
                wrongs = ["1遍", "2遍"]
            else:
                # 如果大于0，错误选项为 -1 和 +1
                wrongs.append("{}遍".format(count - 1))
                wrongs.append("{}遍".format(count + 1))
        # -----------------------------------

        elif q_id == 10: 
            correct = "墨缇斯"
            wrongs = ["若叶睦"]
        elif q_id == 11: 
            correct = getattr(persistent, "playername", "Player")
            wrongs = ["写代码", "种花"]
        elif q_id == 12: 
            h = datetime.datetime.now().hour
            correct = "{}点".format(h)
            wrongs = ["{}点".format((h+5)%24), "{}点".format((h-5)%24)]
        elif q_id == 30: 
            correct = "2026.1.14"
            wrongs = persistent.mq_wrong_dates
            
        # ====== 随机类问题 ======
        elif q_id in map_random:
            key = map_random[q_id]
            if not getattr(persistent, "mq_initialized", False):
                init_mortis_quiz_persistent()
            
            correct = persistent.mq_answers.get(key, "Error")
            pool = MORTIS_POOLS[key]
            possible_wrongs = [x for x in pool if x != correct]
            
            if len(possible_wrongs) > 2:
                wrongs = random.sample(possible_wrongs, 2)
            else:
                wrongs = possible_wrongs
        else:
            return []

        final_list = [(correct, True)]
        for w in wrongs:
            final_list.append((w, False))
        
        random.shuffle(final_list)
        return final_list

    # =========================================================
    # 5. 重置函数
    # =========================================================
    def reset_mortis_quiz():
        persistent.mq_initialized = False
        persistent.mq_answers = {}
        persistent.love_counter = 0
        renpy.save_persistent()

    # =========================================================
    # 6. 题目文本映射表
    # =========================================================
    MORTIS_QUESTION_TEXTS = {
        1: "我的生日是哪一天？",
        2: "我的身高是多少？",
        3: "我最喜欢的饮料是什么？",
        4: "我小时候看过哪位传奇吉他手的演出？",
        5: "我父亲的职业是？",
        6: "我一直弹奏的吉他是几根弦？",
        7: "这个世界的底层引擎叫什么名字？",
        8: "代表“红色”的十六进制代码是多少？",
        9: "在测试里，你最后说了多少遍永远爱我？",
        10: "你现在最爱的人是谁？",
        11: "睦喜欢弹吉他，那我喜欢什么？",
        12: "此时此刻，你现在的电脑系统时间的小时数是？",
        13: "我最喜欢的颜色是？",
        14: "我最喜欢的季节是？",
        15: "我最喜欢的时间段是？",
        16: "我最喜欢的音乐类型是？",
        17: "我最喜欢的天气是？",
        18: "我最喜欢的数字是？",
        19: "我对「自由」的理解是？",
        20: "我对「永恒」的态度是？",
        21: "我如何看待「规则」？",
        22: "我认为吉他睦的问题是？",
        23: "我如何看待「玩家」的存在？",
        24: "如果我们要养一只宠物，我说过想养什么？",
        25: "我在花店买了什么花？",
        26: "我不擅长的科目是？",
        27: "我喜欢的香味是？",
        28: "我讨厌的运动是？",
        29: "如果这里能点外卖的话，我会点？",
        30: "《Just若叶睦》的第一个版本发布时间是？",
        31: "我喜欢的甜点是？"
    }

    # =========================================================
    # 7. 调试用场景跳转 DB
    # =========================================================
    MORTIS_SCENE_DB = [
        ("mortis_date_library",         "01. 图书馆 (身高)"),
        ("mortis_date_cafe",            "02. 咖啡厅 (饮料)"),
        ("mortis_date_park_bench",      "03. 公园长椅 (香味)"),
        ("mortis_date_shopping_window", "04. 橱窗 (颜色)"),
        ("mortis_date_music_store",     "05. 乐器行 (吉他)"),
        ("mortis_date_school_rooftop",  "06. 学校天台 (科目)"),
        ("mortis_date_amusement_park",  "07. 游乐园 (父亲)"),
        ("mortis_date_art_gallery",     "08. 美术馆 (红色代码)"),
        ("mortis_date_botanical_garden","09. 温室花园 (花)"),
        ("mortis_date_home_living_room","10. 客厅 (宠物/外卖)"),
        ("mortis_date_riverside",       "11. 河岸夕阳 (季节)"),
        ("mortis_date_bus_stop",        "12. 公交车站 (时间段)"),
        ("mortis_date_ferris_wheel",    "13. 摩天轮 (规则)"),
        ("mortis_date_seaside",         "14. 无人海滩 (自由)"),
        ("mortis_date_planetarium",     "15. 天文馆 (引擎/数字)"),
        ("mortis_date_shrine",          "16. 神社 (永恒)"),
        ("mortis_date_mirror_house",    "17. 镜子迷宫 (吉他睦)"),
        ("mortis_date_clock_tower",     "18. 钟楼 (系统时间)"),
        ("mortis_date_concert_hall",    "19. 音乐厅 (音乐类型)"),
        ("mortis_date_bedroom_morning", "20. 清晨床边 (生日/最爱)"),
    ]
screen mortis_scene_selector():
    modal True
    zorder 320 # 必须比主控制台高
    
    add Solid("#000000F0") # 深色背景
    
    frame:
        align (0.5, 0.5)
        xsize 600
        ysize 800
        padding (20, 20)
        background Solid("#222")
        
        vbox:
            spacing 10
            
            # 标题
            text "--- 剧情调试跳转 ---" color "#0f0" xalign 0.5 size 30 bold True
            text "点击即可直接跳转至对应 Label" color "#888" xalign 0.5 size 18
            
            null height 10
            
            # 滚动区域 (Viewport)
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 600 # 限制高度，超出滚动
                
                vbox:
                    spacing 5
                    xfill True
                    
                    for lbl, title in MORTIS_SCENE_DB:
                        textbutton "[title]":
                            # 核心逻辑：先检查Label是否存在，防止崩坏
                            action [
                                Hide("mortis_dev_panel"),     # 关闭主面板
                                Hide("mortis_scene_selector"),# 关闭当前面板
                                Function(renpy.notify, "正在跳转至: " + title),
                                Jump(lbl)
                            ]
                            style "button"
                            background Solid("#333")
                            hover_background Solid("#555")
                            xfill True
                            padding (10, 10)
                            text_align 0.5

            null height 20
            
            # 关闭按钮
            textbutton "返回":
                action Hide("mortis_scene_selector")
                xalign 0.5
                text_color "#aaa"