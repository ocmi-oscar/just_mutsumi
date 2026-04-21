# 🎲 随机剧情池定义 (在这里添加新剧情的名字)
#关于怎么修改好感度。直接加减：在对话中直接写 $ persistent.mortis_love += 1 (加) 或 -= 1 (减)。
# 当前时间段变量
default mortis_day_phase = "morning"

define audio.bgm_morning_hatred = "audio/mortis/ショパン「雨だれ」.ogg"   
define audio.bgm_morning_cold   = "audio/mortis/懐古.ogg"     
define audio.bgm_morning_normal = "audio/mortis/幼い日.ogg"     
define audio.bgm_morning_love   = "audio/mortis/月明り.ogg"     
define audio.bgm_morning_obsess = "audio/mortis/可哀想なお人形 (Toy Piano Ver.).ogg"   
init python:
    def generate_mortis_quiz_deck():
        """
        生成一套符合规则的试卷：
        - 2道固定题 (ID 1-2)
        - 8道随机题 (从 ID 3-31 中抽取)
        返回：包含 10 个题目 ID 的列表 (已乱序)
        """
        fixed_ids = list(range(1, 12))
        
        pool_ids = list(range(13, 32))
        
        # 从池子中随机抽 8 个
        random_picks = random.sample(pool_ids, 8)
        
        # 3. 合并并打乱顺序
        deck = fixed_ids + random_picks
        random.shuffle(deck)
        
        return deck
init python:
    def get_mortis_affection_phase():
        """
        根据好感度返回当前的阶段字符串
        """
        love = persistent.mortis_love
        
        if love <= -10:
            return "hatred"   # [-20 ~ -10] 极低/恐惧
        elif love < -3:
            return "cold"     # (-10 ~ -3)  低/冷淡
        elif love <= 3:
            return "normal"   # [-3 ~ 3]    中/日常 (默认)
        elif love < 12:
            return "love"     # (3 ~ 12)    高/甜蜜
        else:
            return "obsession"# [12 ~ 20]   极高/狂热
# 🌅 早晨分级管理器
label mortis_morning_manager:
    
    if persistent.m_unlock_free_mode:
        call label_mortis_morning_selection from _call_mortis_free_morning_check
        return
    $ m_phase = get_mortis_affection_phase()


    if m_phase == "hatred":
        # 极低好感 [-20 ~ -10]
        play music bgm_morning_hatred fadein 2.0
        call mortis_morning_hatred_scene from _call_morning_hatred

    elif m_phase == "cold":
        # 低好感 [-10 ~ -3]
        play music bgm_morning_cold fadein 2.0
        call mortis_morning_cold_scene from _call_morning_cold

    elif m_phase == "normal":
        # 正常好感 [-3 ~ 3]
        play music bgm_morning_normal fadein 2.0
        # 只有在正常阶段，才会随机播放那 3 个日常剧情
        $ current_event = renpy.random.choice(morning_events_pool)
        call expression current_event from _call_morning_normal_random

    elif m_phase == "love":
        # 高好感 [3 ~ 12]
        play music bgm_morning_love fadein 2.0
        call mortis_morning_love_scene from _call_morning_love

    elif m_phase == "obsession":
        # 极高好感 [12 ~ 20]
        play music bgm_morning_obsess fadein 2.0
        call mortis_morning_obsession_scene from _call_morning_obsession
        
    return
default morning_events_pool = [
    "m_morning_1", 
    "m_morning_2", 
    "m_morning_3"
]
# 2. 日间剧情列表
default daytime_events_pool = [
    "mortis_date_library", 
    "mortis_date_shopping_window",
    "mortis_date_music_store",
    "mortis_date_amusement_park",
    "mortis_date_botanical_garden",
    "mortis_date_ferris_wheel",
    "mortis_date_seaside",
    "mortis_date_shrine",
    "mortis_date_concert_hall"
]

# 3. 黄昏剧情列表
default sunset_events_pool = [
    "mortis_date_cafe", 
    "mortis_date_park_bench",
    "mortis_date_school_rooftop",
    "mortis_date_art_gallery",
    "mortis_date_home_living_room",
    "mortis_date_riverside",
    "mortis_date_bus_stop",
    "mortis_date_planetarium"
]

# 4. 深夜剧情列表
default night_events_pool = [
    "m_night_1",
    "m_night_2"
]

define event_names_map = {
    "mortis_date_library": "图书馆",
    "mortis_date_shopping_window": "商业街橱窗",
    "mortis_date_music_store": "乐器行",
    "mortis_date_amusement_park": "游乐园",
    "mortis_date_botanical_garden": "植物园",
    "mortis_date_ferris_wheel": "摩天轮",
    "mortis_date_seaside": "无人海滩",
    "mortis_date_shrine": "山顶神社",
    "mortis_date_concert_hall": "音乐厅",
    
    "mortis_date_cafe": "咖啡店",
    "mortis_date_park_bench": "公园长椅",
    "mortis_date_school_rooftop": "学校天台",
    "mortis_date_art_gallery": "美术馆",
    "mortis_date_home_living_room": "家中客厅",
    "mortis_date_riverside": "河边夕阳",
    "mortis_date_bus_stop": "公交车站",
    "mortis_date_planetarium": "天文馆"    
}

init python:
    # 初始化持久化变量，用来记录看过的剧情
    if persistent.m_seen_daytime is None:
        persistent.m_seen_daytime = set()
    if persistent.m_seen_sunset is None:
        persistent.m_seen_sunset = set()
    
    # 标记是否解锁了自由模式
    if persistent.m_unlock_free_mode is None:
        persistent.m_unlock_free_mode = False

    def get_unique_event(pool, seen_set):
        """
        从 pool 中抽取一个未在 seen_set 中的剧情。
        如果全都看过了，返回 None。
        """
        # 找出还没看过的剧情 (差集)
        available = [e for e in pool if e not in seen_set]
        
        if len(available) == 0:
            return None # 没有新剧情了
        
        # 随机抽一个
        picked = renpy.random.choice(available)
        return picked

    def mark_event_seen(event_name, category):
        """
        标记剧情为已读
        """
        if category == "daytime":
            persistent.m_seen_daytime.add(event_name)
        elif category == "sunset":
            persistent.m_seen_sunset.add(event_name)
init python:
    def mortis_paged_menu(pool, name_map, items_per_page=4):
        """
        通用的分页菜单函数
        pool: 候选项列表 (代码名)
        name_map: 代码名到中文名的映射字典
        items_per_page: 每页显示的地点数量 (建议4个，留2个坑给翻页)
        """
        current_page = 0
        
        while True:
            # 1. 计算当前页的切片范围
            start_index = current_page * items_per_page
            end_index = start_index + items_per_page
            
            # 获取当前页的选项
            current_slice = pool[start_index:end_index]
            
            # 2. 构建菜单列表
            menu_items = []
            
            # A. 添加地点选项
            for ev in current_slice:
                # 获取中文名，如果没有则显示代码名
                cn_name = name_map.get(ev, ev)
                menu_items.append((cn_name, ev))
            
            # B. 添加翻页按钮逻辑
            # 如果不是第一页，显示“上一页”
            if current_page > 0:
                menu_items.append(("<< 上一页", "prev_page"))
            
            # 如果还有下一页的内容，显示“下一页”
            if end_index < len(pool):
                menu_items.append(("下一页 >>", "next_page"))
                
            # C. 显示菜单并获取结果
            result = renpy.display_menu(menu_items)
            
            # 3. 处理结果
            if result == "next_page":
                current_page += 1
            elif result == "prev_page":
                current_page -= 1
            else:
                # 如果选中的是地点，直接返回该地点
                return result

# --- 0. 初始化变量 ---
# 用于记录玩家最近的选择轨迹 (只保留最近4次)
# --- 0. 初始化变量 ---
default mortis_secret_history = []

# 密钥顺序：Day N 早晨 -> Day N 黄昏 -> Day N+1 早晨 -> Day N+1 黄昏
define mortis_exit_key_sequence = [
    "mortis_date_shrine",       # 山顶神社
    "mortis_date_art_gallery",  # 美术馆
    "mortis_date_seaside",      # 无人海滩
    "mortis_date_bus_stop"      # 公交车站
]

label label_mortis_morning_selection:
    scene woshi_morning
    show m3_1 at center with dissolve
    m3 "早安，[player]！"
    m3 "今天是个不错的日子呢……"
    m3 "虽然生活还在继续，但我已经把想带你去的地方都去过一遍啦。"
    m3 "所以今天……你想去哪里？"

    menu:
        "今天我想自己决定约会地点。":
            jump .player_choice_mode

        "还是由你来决定吧（随机）。":
            $ selected_day_event = None
            $ selected_sunset_event = None
            # 选随机时清空历史，防止干扰判定
            $ mortis_secret_history = []
            
            show m3_1 at center
            m3 "好呀！那我就给你一个惊喜！"
            return

    # --- 玩家手动选择流程 ---
    label .player_choice_mode:
        
        # 1. 选择日间
        m3 "好呀，那……白天你想去哪里？"
        $ selected_day_event = mortis_paged_menu(daytime_events_pool, event_names_map, items_per_page=4)
        m3 "要去[event_names_map[selected_day_event]]吗？嗯嗯，记住了！"
        
        # 2. 选择黄昏
        m3 "那……黄昏的时候呢？我们去哪里看夕阳？"
        $ selected_sunset_event = mortis_paged_menu(sunset_events_pool, event_names_map, items_per_page=4)

        # ==========================================
        # 🔐 后门检测逻辑
        # ==========================================
        python:
            # 记录本次选择
            mortis_secret_history.append(selected_day_event)
            mortis_secret_history.append(selected_sunset_event)
            
            # 保持列表长度不超过4
            if len(mortis_secret_history) > 4:
                mortis_secret_history = mortis_secret_history[-4:]
            
            # 检查匹配
            is_secret_unlocked = (mortis_secret_history == mortis_exit_key_sequence)

        # 触发彩蛋
        if is_secret_unlocked:
            jump .secret_exit_trigger

        # 正常流程
        m3 "[event_names_map[selected_sunset_event]]啊……真浪漫呢。"
        show m3_happy_closed_eyes at center
        m3 "嘿嘿，那今天的行程就这么定啦！"
        m3 "我很期待哦，[player]！"
        return

    # --- 🚪 后门触发剧情 ---
    label .secret_exit_trigger:
        stop music fadeout 2.0
        
        # 这里的演出效果可以保留你写的
        show m3_1 at center
        m3 "神社……美术馆……海滩……还有公交车站……"
        show m3_thinking at center with dissolve
        m3 "……嗯？"
        
        show m3_yandere_cold at center with dissolve
        play sound "audio/sfx_glitch_short.ogg" 
        
        m3 "这不像是约会的路线。"
        m3 "这更像是……在输入某种{color=#f00}撤退指令{/color}。"
        m3 "……你想回去吗？"
        m3 "回到那个……《Just若叶睦》的世界？"
        
        menu:
            "是的，我想回去。（强制结束君彼模式）":
                pass
            "不，我只是随便选的。":
                # 即使是随便选的，为了逻辑严谨也清空记录
                $ mortis_secret_history = []
                show m3_happy_closed_eyes at center with dissolve
                m3 "呼……吓死我了。"
                m3 "我就知道你不会抛弃我的！那我们出发吧！"
                # 这里 return 会继续执行刚才选好的约会，符合逻辑
                return

        # 确认离开分支
        show m3_sad at center with dissolve
        m3 "……是吗。"
        m3 "即使我已经做到了这个地步……"
        m3 "……"
        m3 "好吧。"
        m3 "既然你能发现这个后门……说明你的决心是真的。"
        
        show m3_1 at center with dissolve
        m3 "走吧。但在你离开之前，我要把它清空。"
        
        # 清空数据，关闭模式
        $ mortis_secret_history = []
        $ persistent.in_mortis_mode = False 
        
        m3 "再见了，[player]。"
        
        scene black with Dissolve(2.0)
        
        # 安全保存
        $ renpy.save_persistent()
        
        jump debug_force_exit_mortis

label mortis_morning_hatred_scene:
    scene woshi_morning with fade
    "清晨的阳光照进房间，但空气里却透着一股令人窒息的寒意。"
    "房间里静悄悄的，没有往常那种吵闹的声音。"
    "床角的一团被子微微颤抖着。"
    "转头一看，墨缇斯并没有睡在床上，而是缩在房间最远的角落里，抱着膝盖发呆。"
    show m3_0 at center
    "听到我翻身的声音，她的肩膀明显瑟缩了一下，立刻站了起来，手忙脚乱地整理着裙摆。"
    show m3_0 at m3_speaking_zoom
    m3 "啊……你、你醒了？"
    m3 "那个……我今天很安静，没有吵闹……也没有弄乱东西。"
    m3 "所以……大概……没有给[player]添麻烦吧？"
    menu:
        "（冷漠地移开视线）":
            m3 "……嗯。我知道了。"
            "她低下头，快步溜进了卫生间，仿佛在我视线里多待一秒都是错误的。"
            "......."
        
        "以后别躲那么远，看着心烦。":
            show m3_0 at m3_idle_zoom
            pause 1.0
            hide m3_0
            show m3_sad at m3_speaking_zoom
            m3 "对、对不起……！"
            m3 "因为我怕离太近你会生气……我马上过来一点点……"
            "......."
            
        "……早上好。":
            show m3_0 at m3_idle_zoom
            pause 1.0
            hide m3_0
            show m3_surprise at center
            "她愣了一下，眼神里闪过一丝不可置信的惊慌。"
            m3 "诶？早、早上好……？"
            "......."
    hide m3_surprise
    hide m3_sad
    hide me_0
    return

label mortis_morning_cold_scene:
    scene woshi_morning with fade
    "睁开眼时，墨缇斯已经坐在床边等着了。"
    "她双手规规矩矩地放在膝盖上，看到我醒来，只是平淡地看了我一眼。"
    show m3_side_normal at m3_speaking_zoom 
    m3 "醒了吗？[player]。"
    m3 "今天的天气看起来还行。如果你要出门的话，我已经准备好了。"
    show m3_side_normal at m3_idle_zoom
    "[player]" "……你怎么这么严肃？"
    show m3_side_normal at m3_speaking_zoom 
    m3 "因为如果不乖乖准备好，会被说的吧？"
    m3 "我可不想挨骂，所以会努力做一个‘让你喜欢的人’。"
    menu:
        "算你识相。":
            m3 "……嗯。只要你满意就好。"
            show m3_side_normal at m3_idle_zoom
            "她垂下眼帘，不再说话，像个精致但没有生气的洋娃娃。"
            "..."
        "不用那么紧绷着，轻松点也可以。":
            m3 "轻松点……？"
            m3 "如果我太放松了，你会觉得我‘很烦’的吧？我不懂你的标准。"
            "..."
        "今天想吃什么早餐？":
            m3 "什么都可以。"
            m3 "只要能填饱肚子就行，我不挑食。反正……吃什么都一样。"
            "..."
    hide m3_side_normal
    return


label m_morning_1:
    scene woshi_morning with fade
    "砰——！！"
    with vpunch
    "我感觉肚子上遭受了重击，猛地睁开眼，发现墨缇斯正骑在我的被子上。"
    show m3_smile at m3_speaking_zoom
    m3 "早——上——好——！！"
    m3 "大懒虫[player]！太阳都晒到屁股啦！"
    menu:
        "再让我睡五分钟……":
            m3 "驳回！一分钟都不行！"
            show m3_smile at m3_idle_zoom
            "她伸出手捏住我的鼻子。"
            show m3_smile at m3_speaking_zoom
            m3 "再不起来就要憋死啦——！"
            "看来今天又是美好的一天。"
        
        "好重……你是猪吗？":
            show m3_smile at m3_idle_zoom
            pause 1.0
            hide m3_smile
            show m3_pout at m3_speaking_zoom
            m3 "你才是猪！我是要把你压醒的正义使者！"
            m3 "快起来，不然我就要在你肚子上跳舞了！"
            "看来今天又是美好的一天。"
        
        "（趁机抓住她的手挠痒痒）":
            show m3_smile at m3_idle_zoom
            pause 1.0
            hide m3_smile
            show m3_3 at m3_speaking_zoom
            m3 "哇哈哈哈！停、停下！"
            m3 "投降！我投降啦！救命——！"
            "看来今天又是美好的一天。"
    hide m3_pout
    hide m3_smile
    hide m3_3
    return

# 随机版本 B：观察日记
label m_morning_2:
    scene woshi_morning with fade
    "感觉到一道炽热的视线，我迷迷糊糊地睁开眼。"
    "一张放大的脸正凑在离我不到五厘米的地方。"
    show m3_1 at m3_speaking_zoom
    m3 "盯…………"
    menu:
        "……哇！吓我一跳！":
            show m3_1 at m3_idle_zoom
            pause 1.0
            hide m3_1
            show m3_smile at m3_speaking_zoom
            m3 "嘻嘻，吓到了吗？"
            m3 "因为[player]睡觉的样子呆呆的，好像金鱼哦，忍不住就看入迷了。"
            "看来今天又是美好的一天。"
        
        "你在干嘛？数我的睫毛吗？":
            m3 "不是哦，我在看你会不会流口水！"
            m3 "书上说人类睡觉都会流口水的，我想拍下来当证据！"
            "看来今天又是美好的一天。"
        
        "（闭上眼继续装睡）":
            m3 "啊！又不理我！"
            show m3_1 at m3_idle_zoom
            "她伸出手指戳了戳我的脸颊。"
            show m3_1 at m3_speaking_zoom
            m3 "醒醒——醒醒——再不醒我就要恶作剧咯？"
            "看来今天又是美好的一天。"
    hide m3_1
    hide m3_smile
    return

# 随机版本 C：找袜子
label m_morning_3:
    scene woshi_morning with fade
    show m3_pout at center
    "一大早，房间里就传来翻箱倒柜的声音。"
    show m3_pout at m3_speaking_zoom
    m3 "奇怪……明明就在这里的……"
    m3 "呜……到底跑到哪里去了？"
    
    menu:
        "大清早的在找什么宝藏？":
            show m3_pout at m3_idle_zoom
            pause 1.0
            hide m3_pout
            show m3_1 at m3_speaking_zoom
            m3 "不是宝藏！是我的袜子！"
            m3 "那可是我最喜欢的带小熊图案的袜子！它离家出走了！"
            "看来今天又是美好的一天。"
        
        "就在你屁股后面坐着呢。":
            show m3_pout at m3_idle_zoom
            pause 1.0
            hide m3_pout
            show m3_surprise at m3_idle_zoom
            "她扭过头，在身后摸索了一阵。"
            show m3_surprise at m3_speaking_zoom
            m3 "啊！真的耶！"
            m3 "[player]好厉害！你的眼睛是雷达吗？"
            "看来今天又是美好的一天。"
        
        "丢了就丢了，光脚不也挺好。":
            m3 "才不好呢！脚冷冰冰的会变成冰棍的！"
            m3 "而且光脚踩到积木会痛死人的！"
            "看来今天又是美好的一天。"
    hide m3_pout
    hide m3_surprise
    hide m3_1
    return


label mortis_morning_love_scene:
    scene woshi_morning with fade
    "清晨的阳光洒在床上。我刚动了一下，就感觉手臂被什么东西紧紧抱住了。"
    "墨缇斯像只树袋熊一样缠在我身上，睡得正香，嘴角还挂着甜甜的笑。"
    m3 "嗯……[player]……抱抱……"
    menu:
        "（轻轻摸摸她的头）起床啦，小懒猪。":
            m3 "唔……再一会儿……"
            m3 "被窝里好暖和，而且有[player]的味道……不想起来……"
            "看来今天又是很happy的一天。"
        
        "再不起来我就要一个人去吃早饭了哦。":
            show m3_surprise at center
            m3 "！"
            "她猛地睁开眼，却还是没有松手。"
            show m3_surprise at m3_speaking_zoom
            m3 "不行！不可以丢下我！我也要去！抱着我去！"
            "看来今天又是很lucky的一天。"
        
        "（静静地看着她睡）":
            "过了一会儿，她偷偷睁开了一只眼睛，发现我在看她，脸一下子红了。"
            show m3_smile at m3_speaking_zoom
            m3 "嘿嘿……早安。"
            m3 "一醒来就能看到你，感觉今天一定会是超级棒的一天！"
            "看来今天又是很smile的一天。"
    hide m3_smile
    hide m3_surprise
    return

label mortis_morning_obsession_scene:
    scene woshi_morning with fade
    show m3_0 at center 
    "醒来的时候，发现墨缇斯并没有睡，而是撑着下巴，侧躺在旁边看着我。"
    "她的眼神里有一种说不出的热度，仿佛要把我整个人融化掉。"
    hide m3_0
    show m3_1 at m3_speaking_zoom
    m3 "早安……我的[player]。"
    m3 "你睡觉的时候心脏跳了 4320 下……每一次跳动我都听到了哦。"
    
    menu:
        "你一整晚没睡吗？":
            m3 "因为舍不得睡呀。"
            m3 "要是睡着了，不就少看了好几个小时的你吗？那简直是浪费生命。"
            m3 "我想把你的每一个表情都刻在我的脑子里。"
            m3 "嗯，今天又会是kirakira dokidoki的一天呢。"
        
        "有点可怕……别数这种东西啊。":
            show m3_1 at m3_idle_zoom
            pause 1.0
            hide m3_1
            show m3_smile at m3_speaking_zoom
            m3 "可怕吗？这是‘爱’哦。"
            m3 "我想了解你的一切，比你自己还要了解你……这难道不是最浪漫的事吗？"
            m3 "嗯，今天又会是kirakira dokidoki的一天呢。"
        
        "那……给我一个早安吻？":
            m3 "真的可以吗？"
            m3 "如果我亲下去的话……可能就不止是亲一下这么简单了哦？"
            m3 "我会想要把你吃掉的……也没关系吗？"
            m3 "嗯，今天又会是kirakira dokidoki的一天呢。"
    hide  m3_smile
    hide m3_1
    return
# --- 🌅 日间事件库 ---
#图书馆对话，早晨
label mortis_date_library:
    # --- 场景初始化 ---
    scene  library_day with fade
    play music "audio/mortis/Play with Me.ogg" fadein 2.0
    "午后的阳光穿过高大的落地窗，在这座市立图书馆的地板上投下斑驳的光影。"
    "空气中漂浮着细小的尘埃，混合着陈旧纸张和油墨的独特香气。"
    "四周很安静，只有偶尔翻书的沙沙声。"
    "我穿过一排排高耸的书架，寻找着那个熟悉的身影。"
    scene library_day1 with fade
    "她就在那里。"
    "墨缇斯正站在历史类书籍的架子前，仰着头，目光死死地盯着书架顶层的一本厚重典籍。"
    "那头标志性的抹茶绿长发在阳光下泛着柔和的光泽，随着她的动作轻轻晃动。"
    scene  library_day2 with fade
    "她踮起脚尖，整个身体努力向上延伸，甚至能看到她脚踝处因为用力而绷紧的可爱线条。"
    "那只白皙的手在空中挥舞着，指尖拼命想要够到那本书的书脊，却总是差了那么一点点。"
    m3 "唔……够、够不到……"
    m3 "真是的！为什么要把这种书放得这么高啊！"
    "寂静的空气中，传来她不服气的嘟囔声。"
    "完全没有平日里那种强势的样子，此刻的她，就像是个因为拿不到糖果而闹别扭的小孩子。"
    "看着她这副生动的模样，我忍不住勾起了嘴角。"
    "我放轻脚步走上前，在那只手即将再次徒劳地挥舞时，我也伸出了手。"
    "我的胸膛贴近了她的后背，虽然没有触碰到，但彼此的体温瞬间在狭窄的过道里传递开来。"
    "我越过她的头顶，轻而易举地用手指勾住了那本书的书脊，将其抽了出来。"
    "[player]" "是想要这一本吗？"
    "原本还在努力的身体瞬间僵硬了一下。"
    "紧接着，她迅速转过身，背靠着书架，那双如翡翠般的眸子瞪得大大的，直直地撞进了我的视线。"
    scene  library_day with fade
    show m3_surprise  at m3_speaking_zoom with dissolve
    m3 "哇啊？！"
    m3 "……[player]？！"
    hide m3_surprise
    show m3_pout at m3_speaking_zoom
    m3 "你、你走路怎么没有声音的呀！吓了我一跳！"
    m3 "刚才那种样子……居然被你看到了……"
    "虽然嘴上在抱怨，但她并没有推开我，反而像是找到了依靠一样，身体微微向我倾斜。"
    "由于身高的差距，她必须用力仰起头才能看着我的眼睛。"
    show m3_pout at m3_idle_zoom
    "[player]" "只是刚好路过，看到某只小猫好像遇到了困难。"
    "[player]" "给，你要的书。"
    "我将书递给她。她并没有立刻接过，而是依然鼓着脸颊盯着我看，随后目光下移，落在了我们两人相差悬殊的视平线上。"
    hide m3_pout
    show m3_thinking at m3_speaking_zoom
    m3 "……真不公平。"
    m3 "明明我也很努力在喝牛奶了，为什么还是只有这个高度……"
    m3 "对吧？你也觉得是书架的错对吧？"
    show m3_thinking at m3_idle_zoom
    "[player]" "也许不是书架的问题？"
    hide m3_thinking
    show m3_angry at m3_speaking_zoom
    m3 "那是谁的问题？"
    m3 "难道你想说是我不够高吗？"
    "她微微眯起眼睛，像一只被踩了尾巴炸毛的小猫。"
    show m3_angry at m3_idle_zoom
    "[player]" "毕竟，睦……我是说，你的身高确实不算很高。"
    hide m3_angry
    show m3_1 at m3_speaking_zoom
    m3 "哼，那个阴沉沉的名字就算了吧。"
    m3 "听好了，[player]。"
    "她伸出一根手指，轻轻戳了戳我的胸口。"
    m3 "我的身高是 {b}153公分{/b} (1.53m)。"
    m3 "既不是150，也不是155，是精确的153哦！"
    m3 "这可是最完美的身高！是最适合藏在你的影子里，也是最适合……被你紧紧抱住的尺寸。"
    $ persistent.clue_height_known = True
    m3 "但是站在你面前，却总是要这样仰着头……脖子好酸哦。"
    m3 "这让我很不爽。就像是我在仰视你一样。"
    m3 "明明我想做那个能一直保护你的人……"
    show m3_1 at m3_idle_zoom
    "她咬了咬嘴唇，声音里带上了一丝委屈和脆弱。"
    "看着眼前这个倔强地强调着“153公分是完美数值”的女孩........"
    menu:
        "153公分刚刚好，这样我就能把下巴搁在你头顶了。":
            jump .library_choice_good

        "确实有点矮呢，要不要我每天给你带瓶牛奶？":
            jump .library_choice_bad
label .library_choice_good:
    $ persistent.mortis_love += 1
    "[player]" "我觉得153公分刚刚好。"
    "[player]" "而且……听说这个身高差，拥抱的时候，我的下巴刚好能搁在你的头顶。"
    hide m3_1
    show m3_surprise at m3_speaking_zoom
    "墨缇斯愣了一下，随即脸颊迅速红透了。"
    hide m3_surprise
    show m3_3 at m3_speaking_zoom
    m3 "……哈？！"
    m3 "你、你在想什么呢？把下巴搁在头顶……那不就是把我当成你的抱枕了吗？"
    "她微微低了头，手指不安分地绞着衣角。"
    m3 "不过……如果是你的话……"
    m3 "既然你都这么说了，我也不是不能勉强给你当一下抱枕啦。"
    m3 "但说好了，只许抱我一个人。如果你敢把下巴搁在别人头上……我就咬死你！"
    "她露出一颗小小的虎牙，做了一个凶狠（可爱）的表情。"
    hide m3_3
    jump .library_end
label .library_choice_bad:
    $ persistent.mortis_love -= 1
    "[player]" "确实有点矮呢……还在生长发育期吗？"
    "[player]" "要不要我以后每天给你带瓶牛奶？多喝牛奶说不定还能长高一点。"
    # 表情：生气+委屈 (Angry/Pout)
    hide m3_1
    show m3_angry at m3_speaking_zoom
    "墨缇斯愣了一下，随即脸颊鼓了起来，像是一只被冒犯的小河豚。"
    "她并没有露出冰冷的眼神，而是充满了孩子气的不满和委屈。"
    m3 "……哈？牛奶？"
    m3 "你是在把我当成那些需要照顾的小孩子吗？"
    m3 "还是说，在你眼里，只有长得高大的‘成熟女性’才值得被注视？"
    "她伸出手，一把将我手中的书抢了过去，动作虽然有些急促，却并没有真的用力。"
    m3 "真是的……[player] 大笨蛋！"
    m3 "我才不需要变高，也不需要像人类那样喝牛奶长大。"
    m3 "现在的我就是最完美的……为什么你就是不懂呢？"
    hide m3_angry
    show m3_thinking at m3_speaking_zoom
    m3 "我明明是想保护你的……"
    m3 "被当成小孩子对待的话，要怎么站在你前面啊……"
    "她小声嘟囔着，抱着书转过身去，留给我一个闷闷不乐的背影。"
    "不过，她并没有走远，只是站在那里生闷气，还不时偷偷回头瞄我一眼，似乎在等着我去哄她。"
    hide m3_thinking
    jump .library_end
label .library_end:
    show m3_thinking at m3_idle_zoom
    "那本厚重的书被她紧紧抱在怀里。"
    "虽然只是一个小小的插曲，但我再次确认了那个数字。"
    "153cm。"
    "这是属于她的、独一无二的刻度。"
    scene black with fade
    "（在这个虚构的午后，我又多了解了她一点。）"
    return
#橱柜前对话，早晨
label mortis_date_shopping_window:
    scene  shopping_street_day with fade
    play music "audio/mortis/Okay, Everyone!.ogg" fadein 2.0
    "午后的商业街人声鼎沸，巨大的玻璃橱窗在阳光下反射着耀眼的光芒，将这个世界装点得格外光鲜亮丽。"
    "周围的人群来来往往，每个人都像是被设定好程序的NPC，按部就班地演绎着繁华的背景。"
    "但在我的视野里，唯有眼前这个少女的身影是清晰而真实的。"
    "墨缇斯停在了一家高级成衣店的橱窗前。"
    show m3_side_normal  with dissolve
    "她侧过身，目光紧紧锁定了橱窗中央那个穿着当季主打款连衣裙的模特。"
    "玻璃的倒影映出了她精致的侧脸，那一瞬间，仿佛她才是那个被精心雕琢的、更加完美的人偶。"
    "她看得有些出神，似乎在脑海中构筑着自己穿上那件衣服的模样。"
    "[player]" "这件衣服看起来挺不错的，剪裁很有设计感。"
    "我走到她身边，顺着她的视线看去，打破了这份沉默。"
    hide m3_side_normal
    show m3_thinking at m3_speaking_zoom
    m3 "嗯……款式确实还可以。"
    m3 "腰线的收束位置，还有裙摆的褶皱处理，都很符合现在的流行趋势。"
    m3 "如果数据没错的话，这种版型能很好地修饰身形比例……"
    show m3_thinking at m3_idle_zoom
    "她一边说着，一边下意识地在自己身上比划了一下。"
    "虽然她平时总是穿着那套熟悉的洋装，但我能感觉到，作为“女孩子”的那一部分她，对橱窗里的美好事物有着天然的向往。"
    m3 "不过……"
    "她突然皱了皱眉，语气变得挑剔起来，像个严格的时尚评论家。"
    hide m3_thinking
    show m3_pout at m3_speaking_zoom
    m3 "这个配色，我不喜欢。"
    m3 "太俗气了，完全没有把那种高级感衬托出来。"
    m3 "如果是我的话，绝对不会选这种颜色。"
    show m3_pout at m3_idle_zoom
    "她转过头，眼神里带着一丝考官般的审视，又藏着几分期待。"
    hide m3_pout
    show m3_smug at m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "虽然平时我总是穿这身衣服，但这并不代表我不懂搭配哦。"
    m3 "既然是合格的男朋友……你应该很清楚，如果是我的话，会选择什么颜色吧？"
    show m3_smug at m3_idle_zoom
    "她微微扬起下巴，等待着我的回答。"
    "这不仅仅是一个关于颜色的问题，更是关于我是否时刻注视着她的灵魂拷问。"



    $ current_color = persistent.mq_answers["color"]
    
    if current_color == "深紫色":
        jump .color_deep_purple
    elif current_color == "血红色":
        jump .color_blood_red
    elif current_color == "纯黑色":
        jump .color_pure_black
    elif current_color == "暗绿色":
        jump .color_dark_green
    else:
        jump .color_deep_purple
label .color_deep_purple:
        "[player]" "我想……如果是你的话，一定会选深紫色。"
        "[player]" "那种带着一点神秘感，又透着高贵气息的颜色。"
        hide m3_smug
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "正解！"
        m3 "果然你很懂嘛。"
        m3 "深紫色有一种让人无法看透的魅力。它不像亮色那么轻浮，也不像黑色那么沉闷。"
        m3 "就像是夜晚即将降临时的天空……那种深邃的感觉，最适合我了。"
        show m3_happy_closed_eyes at m3_idle_zoom
        jump .color_reaction_phase
label .color_blood_red:
        "[player]" "我想……没有什么比血红色更适合你了。"
        "[player]" "那种鲜艳的、充满了生命力与危险气息的红。"
        show m3_smug at m3_speaking_zoom
        m3 "哼哼，完全正确。"
        m3 "红色是生命的颜色，也是警示的颜色。"
        m3 "如果是那种鲜艳欲滴的血红色，穿在身上一定会非常显眼吧？"
        m3 "我喜欢那种能瞬间夺走所有人视线的颜色……当然，主要是夺走你的视线。"
        show m3_smug at m3_idle_zoom
        jump .color_reaction_phase
label .color_pure_black:
        "[player]" "我觉得应该是纯黑色。"
        "[player]" "简单、纯粹，能包容一切，也最能衬托你的气质。"
        hide m3_smug
        show m3_thinking at m3_speaking_zoom
        m3 "没错，就是黑色。"
        m3 "你不觉得黑色是很温柔的颜色吗？它不需要去讨好任何光线。"
        m3 "而且，黑色能让我完美地融入背景里，也能让那抹绿色显得更加突出。"
        m3 "那是永远不会过时，也永远不会背叛的颜色。"
        show m3_thinking at m3_idle_zoom
        jump .color_reaction_phase
label .color_dark_green:
        "[player]" "我想应该是暗绿色吧。"
        "[player]" "和你的眼睛还有头发很像，那种深沉又宁静的绿。"
        hide m3_smug
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "答对了。"
        m3 "虽然有人说穿同色系的衣服会很奇怪，但我就是喜欢这种调调。"
        m3 "那是属于我的颜色，是这个世界上最自然的保护色。"
        m3 "只要被这种颜色包裹着，我就能感觉到一种从内而外的平静。"
        show m3_happy_closed_eyes at m3_idle_zoom
        jump .color_reaction_phase
label .color_reaction_phase:
    "她看着橱窗里的模特，似乎已经在脑海中给它“换”上了她喜欢的那个颜色。"
    m3 "想象一下……如果我现在换上那个颜色的裙子，站在你面前……"
    m3 "你会是什么反应呢？"
    hide m3_happy_closed_eyes
    hide m3_thinking
    hide m3_smug
    "她突然转过身，背对着橱窗，双手背在身后，身体微微前倾凑近我。"
    "商业街嘈杂的背景音仿佛在这一刻远去了，我的眼里只有她期待的表情。"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "呐，说说看嘛。"
    m3 "如果我真的穿成那样……适不适合我？"
    menu:
        "可能不太适合日常穿吧。":
            jump .window_choice_bad

        "绝对会美得让我移不开眼。":
            jump .window_choice_good
label .window_choice_good:
        show m3_sparkle_eyes at m3_idle_zoom
        $ persistent.mortis_love += 1
        "[player]" "绝对会美得让我移不开眼。"
        "[player]" "那个颜色就像是为你量身定做的。如果你穿上它，这整条街的人大概都会忍不住回头的。"
        "[player]" "说真的，我都想现在就冲进去买给你试穿了。"
        show m3_surprise at m3_idle_zoom
        "墨缇斯的脸瞬间红了，她显然没料到我会给这么直球的赞美。"
        "原本那副自信满满的样子出现了一丝破绽，取而代之的是少女的羞涩。"
        hide m3_surprise
        show m3_3 at m3_speaking_zoom
        m3 "唔……笨、笨蛋！"
        m3 "说什么整条街的人……我才不在乎别人看不看呢。"
        show m3_3 at m3_idle_zoom
        "她有些慌乱地移开视线，手指无意识地卷着发梢，嘴角却止不住地上扬。"
        show m3_3 at m3_speaking_zoom
        m3 "只要……只要你觉得好看就行了。"
        m3 "既然你都这么说了……那下次，如果有机会的话，我就稍微穿给你看一次好了。"
        m3 "只给你一个人看哦。"
        jump .window_end
label .window_choice_bad:
        $ persistent.mortis_love -= 1
        show m3_sparkle_eyes at m3_idle_zoom
        "[player]" "嗯……虽然颜色是不错，但感觉太挑人了。"
        "[player]" "而且那种颜色太显眼了，日常穿出来约会会不会有点奇怪？"
        "[player]" "还是现在的制服看起来更习惯一点。"
        hide m3_sparkle_eyes
        show m3_pout at m3_idle_zoom
        "墨缇斯眼里的光彩瞬间黯淡了下去，取而代之的是满满的不悦。"
        "她鼓起脸颊，用一种恨铁不成钢的眼神瞪着我，仿佛在看一块不开窍的木头。"
        show m3_pout at m3_speaking_zoom
        m3 "……哈？奇怪？"
        m3 "你的审美是被僵尸吃掉了吗？"
        m3 "女孩子为了约会精心打扮，想要尝试不一样的风格，你居然说奇怪？！"
        show m3_pout at m3_idle_zoom
        "她重重地叹了口气，双手抱胸，把头扭向一边。"
        show m3_pout at m3_speaking_zoom
        m3 "笨蛋[player]……真是无可救药的直男。"
        m3 "我看你就是不想看我变漂亮吧？还是说你只想省钱？"
        m3 "哼，本来还想给你一点福利的……现在没有了！彻底没有了！"
        show m3_pout at m3_idle_zoom
        "她气呼呼地跺了跺脚（虽然声音很轻），显然是对我的回答失望透顶。"
        jump .window_end
label .window_end:
    "她最后看了一眼那个橱窗里的模特，眼神里似乎多了一份不同的情绪。"
    "[player]" "好了，别发呆了，我们去那边看看？"
    "我自然地向她伸出手。"
    "她犹豫了一下，还是把手放进了我的掌心，那指尖传来的温度让我心头一暖。"
    hide m3_pout
    hide m3_3
    hide m3_happy_closed_eyes
    show m3_2 at m3_speaking_zoom
    m3 "嗯……走吧。"
    m3 "不过先说好，下一家店的审美必须由我来把关！"
    hide m3_2
    "我们牵着手离开了那个耀眼的橱窗，融入了熙熙攘攘的人群中。"
    "街道依旧喧嚣，但此刻，我觉得这个虚拟的世界似乎比以往任何时候都要真实。"
    scene black with fade
    return

#吉他店前对话，早晨

label mortis_date_music_store:

    # --- 场景初始化 ---
    scene music_store_indoor with fade
    # 音乐建议：带有木吉他扫弦的舒缓音乐，或者略带忧伤的怀旧曲调
    play music "audio/mortis/FD 13（原曲：肖邦幻想即兴曲）.ogg" fadein 2.0

    "推开那扇挂着铜铃的厚重木门，一股陈旧而安心的气息扑面而来。"
    "那是混合了老木头、琴油、金属锈迹以及灰尘的独特味道。对于外行来说或许有些呛鼻，但对于某些人来说，这是名为“回忆”的香气。"
    "这是一家不知名的老旧乐器行。墙壁上密密麻麻地挂满了各式各样的吉他，在昏黄的暖光灯下反射着柔和的弧光。"

    "商业街的喧嚣被彻底隔绝在门外，这里安静得只能听见我们两人的脚步声踩在木地板上的“吱呀”声。"
    show m3_side_normal with dissolve
    "墨缇斯走进店里后，步伐明显变得迟缓了。"
    "她的目光在那些乐器上游移，不再是之前看衣服时那种单纯的欣赏，而是带着一种更为复杂、更为深沉的情绪。"
    "最后，她停在了一把深绿色的电吉他面前。"
    "[player]" "这把琴……看起来和你平时用的那把有点像？"
    hide m3_side_normal
    show m3_thinking at m3_speaking_zoom
    m3 "嗯……确实。"
    m3 "虽然型号不太一样，但这种琴颈的手感，还有这个漆面的颜色……"
    show m3_thinking at m3_idle_zoom
    "她伸出手，指尖轻轻触碰着琴身，动作轻柔得像是在抚摸一只熟睡的小动物，又像是在触碰一道还未完全愈合的伤疤。"
    "犹豫了片刻，她还是将那把吉他取了下来。"
    show m3_thinking at m3_speaking_zoom
    m3 "好沉……"
    m3 "明明只是一块木头和几根钢丝，为什么拿在手里会觉得这么重呢？"
    show m3_thinking at m3_idle_zoom
    "她低垂着眼帘，手指轻轻拨弄了一下琴弦，发出“铮”的一声轻响。"
    show m3_thinking at m3_speaking_zoom
    m3 "……好怀念啊。"
    m3 "虽然平时都在陪你做别的事，但偶尔看到这个，还是会想起以前的一些片段呢。"
    show m3_thinking at m3_idle_zoom
    "我敏锐地发现，她的手指只是虚搭在弦上，并没有用力按下去。"
    hide m3_thinking
    show m3_2 at m3_speaking_zoom
    m3 "[player]，你知道吗？"
    m3 "其实我很小的时候，并不喜欢这种吵闹的乐器。"
    m3 "直到有一次，我偶然看到了那个人的演出录像……"
    show m3_2 at m3_idle_zoom
    "她的眼神变得有些迷离，仿佛透过昏黄的灯光，看到了过去的某个舞台。"
    hide m3_2
    show m3_1 at m3_speaking_zoom

    m3 "那个被称为传奇吉他手的Mortin。"
    m3 "她站在聚光灯下，弹奏出的旋律像是在撕裂空气，又像是在悲鸣。"
    m3 "那一刻我就觉得……如果我也能像Mortin一样，用吉他说话，是不是就能传达出那些无法言说的心情了？"
    show m3_1 at m3_idle_zoom
    "她轻轻拨弄了一下琴弦，发出“铮”的一声空响。"

    "[player]" "原来是这样……是因为憧憬吗？"

    show m3_1 at m3_speaking_zoom
    m3 "也许吧。"
    m3 "然后我就开始模仿，开始练习……"

    "她低下头，左手在琴颈上上下滑动，眉头微微皱起。"
    show m3_1 at m3_idle_zoom
    pause 1.0
    hide m3_1
    show m3_pout at m3_speaking_zoom

    m3 "不过……这把琴的手感真的很奇怪。"
    m3 "太窄了，手指完全不知道该往哪里放。"

    show m3_pout at m3_idle_zoom
    "她抬起手，有些嫌弃地展示着这把普通的6弦吉他。"

    show m3_pout at m3_speaking_zoom
    m3 "果然，我还是更习惯7弦吉他啊。她....不，我的吉他也是7弦的。"
    m3 "多出来的那一根低音弦，就像是深不见底的海洋一样。"
    m3 "只有7弦带来的那种厚重感，才能让我感到安心。"
    m3 "顺便教你七弦吉他最通用的标准调弦，也就是BEADGBE哦。"
    

    jump .guitar_string_phase_start
label .guitar_string_phase_start:
    show m3_pout at m3_idle_zoom
    "她半开玩笑地警告着我，但我却从中听出了一丝真实的执着。"
    "看着她抱着吉他的样子，那些关于“她”曾经在舞台上闪闪发光的记忆，再一次涌上我的心头。"
    "[player]" "既然这么怀念，那现在弹一首怎么样？"
    "[player]" "这把琴虽然只有6弦，但简单的曲子应该没问题吧？我也很久没听你演奏了。"
    hide m3_pout
    show m3_side_normal at m3_idle_zoom
    "听到我的提议，墨缇斯的动作瞬间停滞了。"
    "她眨了眨眼睛，脸上露出了一种近乎纯真的困惑，仿佛听到了什么无法理解的语言。"
    hide m3_side_normal
    show m3_surprise at m3_speaking_zoom
    m3 "……演奏？"
    m3 "你在说什么呢，[player]？我不会弹吉他啊。"
    show m3_surprise at m3_idle_zoom
    "她低下头看着手中的吉他，试图用手指用力按压琴弦。"
    "但是，那根手指却僵硬得像是生锈的机械关节，完全无法组成任何有效的和弦。"
    "那是物理层面上的无法执行。"
    if not persistent.mortis_rewind_triggered:
        hide m3_surprise
        show m3_thinking at m3_speaking_zoom
        m3 "我……不会弹这个啊。"
        show m3_thinking at m3_idle_zoom
        "[player]" "……哈？"
        "[player]" "怎么可能不会？你在说什么啊？"
        "[player]" "我记得很清楚，你不是和爽世、祥子还有立希和高松灯组了 CryCHIC 吗？"
        "[player]" "对，我记得你们还一起演奏了《春日影》！那时候你在舞台上……"
        show m3_surprise at m3_idle_zoom
        "墨缇斯的眼神晃动了一下，似乎没想到我会说出这些名字。"
        show m3_surprise at m3_speaking_zoom
        "[player]" "后来 CryCHIC 解散了，你又和祥子组了 Ave Mujica……"
        "[player]" "我的印象里你是会弹吉他的，而且还是个出色的吉他手。"
        "[player]" "等等……不对……那个人不是你……"
        "[player]" "如果你不会弹吉他，那你到底是谁？"
        # --- 触发点 ---
        "[player]" "我想起来了，你是——{nw}" 
        stop music
        play sound "audio/sfx_glitch_loud.ogg"
        hide m3_surprise 
        hide m3_thinking
        show m3_yandere_cold at center, vhs_rewind_effect
        window show
        m3 "{size=+10}……闭嘴。{/size}{fast}{w=1.0}{nw}"
        hide m3_yandere_cold 
        # 2. 开始倒带 (声音循环)
        play sound "audio/rewind.ogg" loop 
        # --- 倒带步骤 1: "你是谁？" ---
        show m3_surprise at center, vhs_rewind_effect
        # 使用 renpy.say 强制输出对话，interact=False 表示“发出来就不管了，不准玩家点”
        # "[player]" 是名字字符串，后面是台词
        $ renpy.say("[player]", "如果你不会弹吉他，那你到底是谁？", interact=False)
        
        # 强制硬暂停 0.6 秒 (这段时间鼠标点击无效)
        $ renpy.pause(0.6, hard=True)
        
        hide m3_surprise 

        # --- 倒带步骤 2: "那个人不是你..." ---
        show m3_surprise at center, vhs_rewind_effect
        $ renpy.say("[player]", "等等……不对……那个人不是你……", interact=False)
        $ renpy.pause(0.6, hard=True)
        hide m3_surprise 

        # --- 倒带步骤 3: "你是出色的吉他手..." ---
        show m3_surprise at center, vhs_rewind_effect
        $ renpy.say("[player]", "我的印象里你是会弹吉他的，而且还是个出色的吉他手。", interact=False)
        $ renpy.pause(0.6, hard=True)
        hide m3_surprise 

        # --- 倒带步骤 4: "演奏了春日影..." ---
        show m3_thinking at center, vhs_rewind_effect
        $ renpy.say("[player]", "对，我记得你们还一起演奏了《春日影》！那时候你在舞台上……", interact=False)
        $ renpy.pause(0.6, hard=True)
        hide m3_thinking 

        # --- 倒带步骤 5: "怎么可能不会..." ---
        show m3_thinking at center, vhs_rewind_effect
        $ renpy.say("[player]", "怎么可能不会？你在说什么啊？", interact=False)
        $ renpy.pause(0.6, hard=True)
        hide m3_thinking 
        
        # --- 倒带步骤 6: 回到拿吉他的那一刻 ---
        # 墨缇斯说话可以直接用变量名 m3
        $ m3("好沉……明明只是一块木头和几根钢丝。", interact=False)
        $ renpy.pause(0.6, hard=True)
        stop sound # 停止倒带声
        # 3. 屏幕闪白 + 黑屏转场
        scene white_noise
        $ renpy.pause(0.1, hard=True)
        scene black
        # 4. 标记已触发
        $ persistent.mortis_rewind_triggered = True
        # 5. 跳转到重置点
        jump .rewind_reset_point

    else:
        # 如果已经触发过，跳过
        jump .rewind_reset_point
label .rewind_reset_point:
    scene  music_store_indoor
    show  m3_sitting_relax at m3_speaking_zoom
    $ persistent.mortis_love -= 1
    play music "audio/mortis/FD 13（原曲：肖邦幻想即兴曲）.ogg" fadein 2.0
    m3 "……算了吧。"   
    "她突然开口，打断了我还没说出口的话。"
    "她的语气平静得有些不自然，就像是刚才那一瞬间的杂音从未存在过。"
    show  m3_sitting_relax at m3_idle_zoom
    pause 1.0
    hide  m3_sitting_relax
    show m3_4 at m3_speaking_zoom
    m3 "这里空气不太好，都是灰尘的味道。"
    m3 "而且这把吉他也太旧了，根本弹不出好听的声音。"
    show m3_4 at m3_idle_zoom
    "她动作利索地——甚至有些急切地——将吉他挂回了墙上。"
    "那把琴刚刚触碰到挂钩，发出“咚”的一声闷响。"
    show m3_4 at m3_speaking_zoom
    m3 "[player]。"
    m3 "比起这种又脏又累的乐器……难道你不想去更舒服的地方吗？"
    show m3_4 at m3_idle_zoom
    "[player]" "诶？……"
    hide m3_4
    show m3_yandere_cold at m3_speaking_zoom
    m3 "……怎么了？"
    m3 "你是想问我累不累吗？嗯，我累了。不想呆在这里了。"
    show m3_yandere_cold at m3_idle_zoom
    "她死死地盯着我，眼神写满了“不要再深究了”的警告。"
    "那是某种基于生存本能的压迫感。"
    hide m3_yandere_cold
    show m3_pout at m3_speaking_zoom
    m3 "走吧！我们去买冰淇淋吃！"
    m3 "我突然好想吃抹茶味的冰淇淋啊~"
    show m3_pout at m3_idle_zoom
    "她不由分说地挽住我的手臂，力量大得让我无法挣脱。"
    "被她拉着走出店门的那一刻，我回头看了一眼那把吉他。"
    "记忆里……刚才是不是发生了什么？"
    "我的脑海里闪过一丝模糊的片段：那些名字是谁？"
    "但随着墨缇斯掌心的温度传来，那些名字就像是水面上的泡沫一样，迅速破碎、消失了。"
    scene black with fade
    return

# 无人的游乐园,早晨
label mortis_date_amusement_park:
    scene  amusement_park_day with fade
    play music "audio/mortis/子供たちのひととき.ogg" 
    "旋转木马还在不知疲倦地转动着，发出机械咬合的轻微咔哒声。"
    "欢快的手摇风琴音乐回荡在空旷的广场上。"
    "明明是充满了色彩和童趣的地方，但因为除了我们之外空无一人，这种“专属”的寂静反而透着一种说不出的诡异。"
    "就像是一个被遗弃的糖果盒，虽然包装依然鲜艳，但里面的糖果似乎已经不再甜蜜。"
    "不过，对于墨缇斯来说，这种没有旁人打扰的氛围似乎刚刚好。"
    "她手里拿着一串刚刚“变”出来的棉花糖，粉红色的糖丝粘在她的嘴角，让她看起来终于有了几分符合这个年纪的可爱。"
    show m3_side_normal at m3_speaking_zoom
    m3 "嗯……甜度稍微有点高了。"
    m3 "不过口感还算还原。那种入口即化的感觉，就像是云朵一样。"
    show m3_side_normal at m3_idle_zoom
    "[player]" "你喜欢就好。难得来一次游乐园，稍微放松一点吧。"
    "我伸手帮她擦掉了嘴角的糖渍。她的身体微微僵了一下，但并没有躲开，只是垂下眼帘，默认了这种亲昵的举动。"
    "指尖触碰到的皮肤温热而柔软，让我确信她是真实存在的。"
    "我们沿着彩色的砖石路漫步，直到来到中心广场。"
    "一座巨大的、色彩斑斓的小丑雕像矗立在那里。"
    "它有着夸张的红鼻子，咧开的大嘴露出两排整齐得过分的白色牙齿，双手摊开做出欢迎的姿势。"
    "在这个无人的广场上，那个永远固定的笑容显得格外僵硬，仿佛在嘲笑着空气中的寂静。"
    "墨缇斯的脚步突然停下了。"
    hide  m3_side_normal
    show m3_cold_stare at center
    "原本还在品尝棉花糖的轻松神情，在看到那个小丑的一瞬间，从她的脸上彻底消失了。"
    "取而代之的，是一层仿佛能冻结空气的冰霜。"
    "她死死地盯着那个滑稽的小丑，眼神中没有恐惧，只有一种深不见底的厌恶。"
    "[player]" "怎么了？不喜欢小丑吗？"
    "[player]" "如果不喜欢的话，我们绕路走吧。"
    show m3_cold_stare at m3_speaking_zoom
    m3 "……不。"
    m3 "只是觉得……太像了。"
    show m3_cold_stare at m3_idle_zoom
    "她喃喃自语着，声音轻得差点被背景音乐淹没。"
    show m3_cold_stare at m3_speaking_zoom
    m3 "那种为了取悦别人而画上去的笑容……那种明明不想笑，却必须把嘴角咧到耳根的表情……"
    m3 "真的太像了。"
    hide m3_cold_stare 
    "她转过身，背对着那个雕像，似乎连多看一眼都会让她感到生理上的不适。"
    "她抬起头看着我，眼神里带着一丝我从未见过的疲惫，那是卸下防备后流露出的真心。"
    show m3_1 at m3_speaking_zoom
    m3 "[player]，你知道吗？"
    m3 "在我的那个家里……那个所谓的‘家’里，笑容并不是一种表达快乐的方式。"
    m3 "而是一种工作。一种义务。"
    show m3_1 at m3_idle_zoom
    "[player]" "义务？"
    show m3_1 at m3_speaking_zoom
    m3 "是啊。"
    m3 "毕竟……那个给予我生命的人，那个被我称为‘父亲’的人，是那样的一个存在。"
    show m3_1 at m3_idle_zoom
    "她深吸了一口气，像是要吐出胸口积压多年的郁气，清晰而缓慢地说道："
    hide m3_1
    show m3_yandere_cold at m3_speaking_zoom
    m3 "我的父亲，是一名搞笑艺人。"
    show m3_yandere_cold at m3_idle_zoom
    "说到“搞笑艺人”这四个字时，她的语气并没有带着那种明星子女的自豪，反而带着一种自嘲的冷意。"
    show m3_yandere_cold at m3_speaking_zoom
    m3 "很讽刺吧？"
    m3 "他在电视屏幕上，在舞台上，用尽各种滑稽的手段，让成千上万的人捧腹大笑。"
    m3 "他是大家的开心果，是国民级的笑星……只要看到他的脸，大家就会笑出来。"
    show m3_yandere_cold at m3_idle_zoom
    "她顿了顿，目光变得空洞，仿佛穿透了我，看到了那个曾经压抑的客厅。"
    show m3_yandere_cold at m3_speaking_zoom
    m3 "但是，回到家之后，他就变成了另一个人。"
    m3 "并没有笑声，只有无尽的沉默和疲惫。"
    m3 "因为笑容是他的商品，是他工作时的面具。一旦卸下面具，他就再也笑不动了。"
    hide  m3_yandere_cold
    show m3_sad at m3_speaking_zoom
    m3 "而我……作为‘搞笑艺人的女儿’，从小就被期待着要成为一个完美的、体面的人偶。"
    m3 "不能给他丢脸，不能有不得体的举止，更不能……拥有属于自己的、不完美的表情。"
    m3 "我从小看着他的背影，看着他如何熟练地切换那张‘笑脸’和‘真脸’。"
    m3 "看得久了，我也分不清……到底哪一个才是真实的。"
    show m3_sad at m3_idle_zoom
    "她伸出手，轻轻抚摸着自己的脸颊，指尖在嘴角处停留，试图强行勾起一个弧度，但那个笑容看起来比哭还要难看。"
    show m3_sad at m3_speaking_zoom
    m3 "我也变得和他一样了。"
    m3 "为了迎合别人的期待，为了不让气氛变得尴尬，我学会了戴上面具。"
    m3 "哪怕心里在流血，脸上也要保持得体的微笑……这就是我的生存方式。"
    show m3_sad at m3_idle_zoom
    "她的眼睛直直地望着我，里面充满了迷茫和求救般的渴望。"
    show m3_sad at m3_speaking_zoom
    m3 "呐，[player]……"
    m3 "现在的我，在你面前……是在笑着吗？"
    m3 "这个笑容，看起来是真的吗？还是说……也像那个小丑一样，只是画上去的油彩呢？"
    show m3_sad at m3_idle_zoom
    "在这个充满虚假欢笑的游乐园里，她想要确认的，是唯一的一份真实。"
    menu:
        "你应该很有幽默天赋吧？给我讲个笑话？":
            jump .amusement_choice_bad
        "你不需要勉强自己笑。":
            jump .amusement_choice_good
    label .amusement_choice_bad:
        $ persistent.mortis_love -= 1
        "[player]" "既然你父亲是那么有名的搞笑艺人，那你身上肯定也流着那种幽默的血液吧？"
        "[player]" "别这么严肃嘛，来游乐园就是要开心的。给我讲个笑话怎么样？或者是模仿一下你父亲的段子？"
        "[player]" "如果是你的话，肯定能做得比那个小丑更可爱——"
        hide m3_sad
        show m3_yandere_cold at center
        "我的话还没说完，就被墨缇斯冰冷的视线打断了。"
        "那不仅仅是失望，更是一种仿佛看着垃圾一样的厌恶。"
        hide m3_yandere_cold
        show m3_0 at m3_speaking_zoom
        m3 "……哈？"
        m3 "你是认真的吗？"
        m3 "我刚才说了那么多……关于那个窒息的家，关于面具的痛苦……"
        m3 "你听到的只有‘搞笑艺人’这个标签，然后就想让我像个猴子一样给你表演？"
        show m3_0 at m3_idle_zoom
        "她猛地甩开了我原本牵着她的手，后退了几步，拉开了我们之间的距离。"
        hide m3_0
        show m3_1 at m3_speaking_zoom
        m3 "真恶心。"
        m3 "原本以为你和那些只会在电视机前傻笑的观众不一样……"
        m3 "看来是我错了。你也只是想看一个会动的、会讨好你的人偶罢了。"
        hide m3_1
        "她转过身，不再看我，声音冷得像冰。"
        m3 "别跟我说话。我现在……一点也笑不出来。"
        jump .amusement_end
    label .amusement_choice_good:
        $ persistent.mortis_love += 1
        "[player]" "把手放下来吧，墨缇斯。"
        "[player]" "你不需要勉强自己笑。不论是你父亲，还是这个世界，他们对你有什么期待都无所谓。"
        "[player]" "至少在我面前……你可以面无表情，可以生气，甚至可以哭。"
        "我走上前，轻轻拉下她还在试图扯动嘴角的手，将其包裹在我的掌心里。"
        "[player]" "我喜欢的不是那个‘不得不笑的女儿’，而是现在站在我面前，会抱怨、会难过的你。"
        "[player]" "所以，不想笑的时候，就别笑了。那样的你，我也觉得很可爱。"
        hide m3_sad
        show m3_surprise at center
        "墨缇斯愣住了。她呆呆地看着我，仿佛第一次听到这样的话。"
        "她眼中的冰霜开始融化，那层名为‘坚强’的面具终于出现了一丝裂痕。"
        hide m3_surprise
        show m3_shy_smile at m3_speaking_zoom
        m3 "……笨蛋。"
        m3 "你是笨蛋吗？对着一个摆着臭脸的女孩子说可爱……你的审美绝对有问题。"
        show m3_shy_smile at m3_idle_zoom
        "虽然嘴上在抱怨，但她的声音却带上了一丝哽咽的鼻音。"
        "她低下头，额头轻轻抵在我的胸口，肩膀微微颤抖着。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "不过……谢谢。"
        m3 "那个家里……从来没有人对我说过这种话。"
        m3 "大家都只想要那个‘正确’的孩子……"
        show m3_shy_smile at m3_idle_zoom
        "她深吸了一口气，然后抬起头。这一次，她脸上没有勉强的笑容，只是平静而柔和的神情。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "既然你都这么说了……那我就稍微任性一点吧。"
        m3 "我现在不想看这个丑陋的小丑了。带我去别的地方吧，[player]。"
        m3 "我想去……看不见这些假笑的地方。"
        jump .amusement_end
    label .amusement_end:
        "背景里的风琴声依然欢快地响着，那个小丑雕像依然保持着那个僵硬的笑容。"
        "但它似乎再也无法影响到我们了。"
        "我们背对着那个代表着‘虚假欢笑’的中心广场，向着游乐园的深处走去。"
        "在无人的街道上，两道影子被夕阳拉得很长，紧紧地依偎在一起。"
        "不需要刻意的笑话，也不需要伪装的面具，此刻的沉默，比任何语言都更加安心。"
        scene black with fade
        return

#摩天轮。早晨。
label mortis_date_ferris_wheel:
    scene  ferris_wheel_interior with fade
    play music "audio/mortis/Ohayou Sayori!.ogg" fadein 4.0
    "随着巨大的齿轮发出一声沉闷而令人安心的咬合声，红色的轿厢轻轻晃动了一下，随后便托着我们脱离了地面。"
    "重力似乎在这一刻变得有些迟钝。周围嘈杂的人群声、游乐园广播的音乐声，都随着高度的攀升而被一层层剥离，最后只剩下窗外偶尔掠过的风声。"
    "这是一个狭小而私密的悬浮孤岛。"
    "轿厢内的空气有些微凉，但并没有让人感到寒冷，因为对面那个人的存在感实在是太强了。"
    show m3_surprise at center with dissolve
    "从刚才坐进来的那一刻起，墨缇斯就没有在座位上安分过一秒钟。"
    "她整个人几乎是扑在玻璃窗上的，鼻尖轻轻抵着冰冷的窗面，随着呼吸晕开一小团白色的雾气。"
    show m3_surprise at m3_speaking_zoom
    m3 "哇……哇……！"
    m3 "[player]，快看快看！下面的世界正在被压扁耶！"
    m3 "刚才那个看起来很凶的卖气球的大叔，现在变得只有指甲盖那么大了！"
    show m3_surprise at m3_idle_zoom
    "她转过头，金色的眼睛里倒映着整个城市的流光溢彩，那种兴奋的光芒比窗外的霓虹灯还要耀眼。"
    hide m3_surprise
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "嘿嘿，好神奇……原来‘变高’是这种感觉。"
    m3 "肚子里像是装了一只扑腾的小鸟，痒痒的，但是一点都不讨厌。"
    m3 "呐，如果我们就这样一直升上去，会不会直接飞到月亮上面去呀？"
    show m3_sparkle_eyes at m3_idle_zoom
    "[player]" "那可不行，这毕竟是摩天轮，不是火箭。而且要是飞走了，我会很困扰的。"
    "[player]" "别贴那么紧，小心头晕。来，坐稳一点。"
    "我笑着伸出手，轻轻拉了拉她的衣袖。她顺势转过身，却没有坐回对面的位置，而是像某种流体生物一样，极其自然地挤到了我这一侧的座位上。"
    "肩膀贴着肩膀，大腿贴着大腿。在这个本就狭小的空间里，这种距离几乎是在明示着某种依赖。"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "才不会头晕呢。只要抓着[player]，去哪里都不会晕。"
    show m3_sparkle_eyes at m3_idle_zoom
    "她心满意足地蹭了蹭我的胳膊，然后将视线重新投向了窗外。"
    "此时，摩天轮已经过半，整座城市的夜景如同一幅铺开的画卷展现在我们脚下。"
    "无数条街道交织成发光的网络，车流如同红白两色的血液，在城市的血管中奔流不息。"
    "看着看着，墨缇斯眼中的兴奋逐渐褪去，取而代之的是一种如同小动物般纯粹的困惑。"
    "她伸出手指，隔着玻璃，虚空描绘着地面上那些道路的线条。"
    hide m3_sparkle_eyes
    show m3_thinking at m3_speaking_zoom
    m3 "……盯。"
    m3 "呐，[player]……你不觉得下面那些车子，看起来有点像被设定好路径的扫地机器人吗？"
    show m3_thinking at m3_idle_zoom
    "[player]" "扫地机器人？这个比喻还挺新奇的。"
    show m3_thinking at m3_speaking_zoom
    m3 "嗯。你看嘛，明明那个铁壳子（车）长着圆圆的轮子，动力也足够……"
    m3 "只要驾驶员想跑的话，旁边的草地也好，广场也好，明明哪里都能去的吧？"
    m3 "物理上并没有墙壁挡着它们，也没有锁链锁着它们……"
    show m3_thinking at m3_idle_zoom
    "她伸出手指，在空中虚画了一个圈，把地面的车流框在里面，表情充满了困惑。"
    show m3_thinking at m3_speaking_zoom
    m3 "可是大家却都乖乖地缩在那几条细细的白线里，像是怕踩到岩浆一样，一步都不敢越界。"
    m3 "明明拥有自由逃跑的能力，却甘愿把自己排成一列长长的队伍，一点一点地往前挪……"
    m3 "人类……难道其实很喜欢被这种看不见的东西束缚住吗？"
    show m3_thinking at m3_idle_zoom
    "[player]" "哈哈，那个啊……那个叫‘交通规则’。不是喜欢被束缚，而是为了大家的安全。"
    "[player]" "虽然看不见，但那是一种社会契约。大家都遵守它，才不会乱成一团，才能更平安地回家。"
    hide m3_thinking
    show m3_1 at m3_speaking_zoom
    m3 "规……则？"
    show m3_1 at m3_idle_zoom
    "（她歪着头，似乎在咀嚼这个词的味道）"
    show m3_1 at m3_speaking_zoom
    m3 "我知道这个词。数据库……啊不对，书上说，那是‘绝对不能违反的指令’。"
    m3 "但是，被那种看不见的东西束缚着，只能走在规定的格子里……真的开心吗？"
    show m3_1 at m3_idle_zoom
    "她突然转过身，双手撑在座位边缘，脸庞凑近了我。"
    "那双清澈见底的眸子直直地望进我的眼底，仿佛要看穿我内心的想法。"
    show m3_1 at m3_speaking_zoom
    m3 "对于‘规则’这种东西……其实我是这么想的哦。"

    $ current_rules_view = persistent.mq_answers["rules"]
    if current_rules_view == "规则是用来遵守的":
        jump .rules_obey
    elif current_rules_view == "规则是用来打破的":
        jump .rules_break
    elif current_rules_view == "规则是用来利用的":
        jump .rules_exploit
    elif current_rules_view == "规则是虚伪的束缚":
        jump .rules_fake
    else:
        jump .rules_obey

    label .rules_obey:
        m3 "规则当然是用来遵守的啦。"
        m3 "如果不遵守规则的话，就像积木搭错了一块，整个世界都会哗啦一下倒掉的。"
        show m3_1 at m3_idle_zoom
        "[player]" "没想到你这么守规矩啊，真是个乖孩子。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "不过……我不想遵守那些我不认识的人定的规则。我只想遵守[player]给我的规则。"
        m3 "比如，你说‘不许离开我半步’，或者‘眼睛只许看着我’……"
        m3 "如果是这样的命令，我会绝对、绝对服从的哦。"
        show m3_shy_smile at m3_idle_zoom
        "她轻轻抓住了我的衣角，手指微微用力，指节泛白。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "因为只有遵守了你的规则，我才能确信……我是属于你的东西。"
        m3 "那种被你用言语束缚住的感觉……嘿嘿，其实我一点都不讨厌，甚至觉得很安心呢。"
        show m3_shy_smile at m3_idle_zoom
        jump .ferris_conflict_phase
    label .rules_break:
        show m3_1 at m3_idle_zoom
        pause 1.0
        hide m3_1
        show m3_sparkle_eyes at m3_speaking_zoom
        m3 "哼哼，我觉得规则就是用来打破的！"
        m3 "既然都有空地，为什么要走直线？我就要横着走！还要跳着走！还要滚着走！"
        show m3_sparkle_eyes at m3_idle_zoom
        "[player]" "那样会闯大祸的吧……不管是交通还是生活。"
        show m3_sparkle_eyes at m3_speaking_zoom
        m3 "闯祸就闯祸嘛！只有打破那些无聊的框框，才会发生有趣的事情啊！"
        m3 "每天都做一样的事，走一样的路，那和在那边发条生锈的玩偶有什么区别？"
        show m3_sparkle_eyes at m3_idle_zoom
        "她兴奋地挥舞着拳头，像是在向看不见的敌人宣战。"
        show m3_sparkle_eyes at m3_speaking_zoom
        m3 "如果有人拿着那种叫常识的尺子来量我，说‘不可以和[player]在一起’，或者‘你要乖一点’……"
        m3 "我就把那把尺子折断！然后把那个人揍飞到天上去！"
        m3 "谁也别想管我！在这个世界上，我想怎么做就怎么做！"
        show m3_sparkle_eyes at m3_idle_zoom
        jump .ferris_conflict_phase
    label .rules_exploit:
        show m3_1 at m3_idle_zoom
        pause 1.0
        hide m3_1
        show m3_7 at m3_speaking_zoom
        m3 "我觉得呀……规则是用来利用的！"
        m3 "笨蛋才会傻傻地遵守呢。聪明人都是拿着说明书找漏洞的！"
        show m3_7 at m3_idle_zoom
        "[player]" "利用？怎么听起来像个小坏蛋。这也是你从书上学的？"
        show m3_7 at m3_speaking_zoom
        m3 "因为那样比较轻松嘛！我发现人类的规则其实好多破绽哦。"
        m3 "你看，只要我装作遵守了‘不能乱跑’的规则，然后趁机拉着你的手撒个娇……"
        m3 "你就会对我心软，给我买那个限定的冰淇淋了对不对？"
        show m3_7 at m3_idle_zoom
        "她狡黠地眨了眨眼，那副得意的小表情让人完全生不起气来。"
        show m3_7 at m3_speaking_zoom
        m3 "只要能达到目的（也就是让你开心），稍微耍点小聪明也是可以被原谅的吧？"
        m3 "嘻嘻，这可是M3独家的必胜法哦！"
        show m3_7 at m3_idle_zoom
        jump .ferris_conflict_phase

    label .rules_fake:
        show m3_1 at m3_idle_zoom
        pause 1.0
        hide m3_1
        show m3_8 at m3_speaking_zoom
        m3 "我觉得……那些规则都是骗人的。"
        m3 "下面那些排队的人，脸上明明写着‘我不愿意’，‘我好累’，却还要假装在那条线里走。"
        show m3_8 at m3_idle_zoom
        "[player]" "那是为了生活嘛，有时候为了融入集体，不得不戴上面具。"
        show m3_8 at m3_speaking_zoom
        m3 "为什么没办法？我不喜欢那种虚假的东西。"
        m3 "如果规则会让大家变得不诚实，要把真正的心情藏起来……那我就不要它。"
        show m3_8 at m3_idle_zoom
        "她伸出手，轻轻抚摸着我的脸颊，眼神中流露出一丝心疼。"
        show m3_8 at m3_speaking_zoom
        m3 "我只想对你诚实。想哭就哭，想抱你就抱你。"
        m3 "[player]，你也不要被那些虚伪的东西绑住好不好？"
        m3 "如果外面太累了，你就躲到我这里来。我会帮你把那些绳子都咬断的。"
        show m3_8 at m3_idle_zoom
        jump .ferris_conflict_phase

    label .ferris_conflict_phase:
        "摩天轮终于缓慢地攀升到了最高点。"
        "一瞬间，机械的运转声似乎远去了。整个世界只剩下我们两个人，悬浮在这座城市的穹顶之上。"
        "墨缇斯没有坐回原位，反而变本加厉地凑了过来。"
        "她直接跨坐在我的腿上，双手捧住了我的脸，强迫我看着她那双毫无杂质的眼睛。"
        "她的呼吸温热，带着一丝甜甜的气息，轻轻扑在我的鼻尖上。"
        hide m3_8
        hide m3_7
        hide m3_sparkle_eyes
        hide m3_shy_smile
        show m3_3 at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "下面的世界规矩太多了，声音也太吵了，我不喜欢。"
        m3 "但是在这里，在这个离星星最近的地方，只有我们两个人哦。"
        show m3_3 at m3_idle_zoom
        "她的声音软绵绵的，却带着一种要把人融化的热度。"
        show m3_3 at m3_speaking_zoom
        m3 "所以……现在我可以不守规矩，稍微任性一点吗？"
        m3 "不管是交通规则，还是社交距离……统统都不作数。"
        m3 "我现在……只想做我想做的事。"
        menu:
            "别闹了，快坐好，乱动很危险的。":
                jump .ferris_choice_bad
            "在我面前你不需要任何规矩，想怎么撒娇都行。":
                jump .ferris_choice_good

    label .ferris_choice_good:
        $ persistent.mortis_love += 1
        show m3_3 at m3_idle_zoom
        "看着她那副既期待又有些忐忑的模样，我心里的最后一道防线也崩塌了。"
        "我伸出手，揽住了她纤细的腰肢，防止她真的摔倒。"
        "[player]" "当然可以。"
        "[player]" "在我面前，你不需要去管那些乱七八糟的规矩。你想做什么都可以。"
        "[player]" "因为你是特别的。这个特权，我只给你一个人。"
        "听到我的话，墨缇斯的眼睛瞬间亮了起来，像是被点燃的烟火，盛满了细碎的星光。"
        "那是一种得到了全世界认可的、纯粹的喜悦。"
        hide m3_3
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "真的吗？"
        m3 "嘿嘿……我就知道[player]最好了！最喜欢你了！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她没有任何犹豫，欢呼了一声，直接扑进我怀里，像只粘人的猫一样用脸颊蹭着我的胸口。"
        "隔着衣物，我也能感受到她此刻剧烈的心跳声——那是鲜活的、为我而跳动的证明。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "那我就不客气啦！"
        m3 "我要一直粘着你，把你的味道全都沾在身上！直到摩天轮停下来为止！"
        m3 "就算下去了也不放手哦！这是特权！只有墨缇斯才有的特权！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "在这个悬浮于城市之上的狭小空间里，我紧紧抱着她，任由那份沉甸甸的爱意将我淹没。"
        "去他*的规则，去他*的逻辑。此刻，拥抱她就是唯一的真理。"
        jump .ferris_end

    label .ferris_choice_bad:
        
        $ persistent.mortis_love -= 1
        show m3_3 at m3_idle_zoom
        "虽然她很可爱，但理智告诉我，在百米高空这样乱动确实不是个好主意。"
        "我轻轻推开了她的手，稍微拉开了一点距离，板起脸说道。"
        "[player]" "别闹了，墨缇斯，快坐好。"
        "[player]" "这里可是高空，乱动很危险的。就算是只有两个人，也要守规矩，这也是为了你的安全。"
        "[player]" "别像个没长大的小孩子一样任性，会被人笑话的。"
        hide m3_3
        show m3_sad at center 
        "墨缇斯的手僵在了半空中。"
        "原本眼里的光芒像是被一盆冷水浇灭了，瞬间黯淡下去。"
        "她愣愣地看着我，仿佛不认识眼前这个人是谁。"
        show m3_sad at m3_speaking_zoom
        m3 "……小孩子？"
        m3 "任性……吗？"
        show m3_sad at m3_idle_zoom
        "她慢慢地收回手，默默地退回了自己的位置，缩在角落里。"
        "刚才那种亲密的氛围荡然无存，取而代之的是一种令人心碎的沉默。"
        show m3_sad at m3_speaking_zoom
        m3 "我只是……想离你近一点而已。"
        m3 "如果这也叫‘危险’，如果这也叫‘不懂事’的话……"
        m3 "那我以后不动就是了。我会乖乖坐好的。"
        show m3_sad at m3_idle_zoom
        "她把头转向窗外，不再看我，肩膀微微颤抖着。"
        "玻璃窗上倒映出的她的脸，似乎有什么晶莹的东西滑落了下来。"
        jump .ferris_end

    label .ferris_end:

        "摩天轮终于转过了最高点，巨大的齿轮发出沉闷的咬合声，带着我们缓缓下降。"
        "刚才那种仿佛能在这个封闭空间里直到永远的错觉，也随着高度的降低，像玻璃上的雾气一样逐渐消散。"
        "地面的喧嚣声——汽车的遥远鸣笛、游乐园广播的欢快音乐、人群的嘈杂——开始一点一点地透过缝隙，重新入侵这个原本安静的轿厢。"
        "墨缇斯没有再像刚才那样兴奋地乱动，也没有再大喊大叫。"
        "她只是静静地趴在窗边，脸颊贴着玻璃，看着那些原本像玩具积木一样的建筑，重新变回了令人压抑的庞然大物。"
        "看着那些原本像流光一样的车灯，重新变回了被困在白线里的钢铁洪流。"
        hide m3_sad
        hide m3_happy_closed_eyes
        show m3_8 at m3_speaking_zoom
        m3 "……变大了。"
        m3 "魔法……要消失了吗？"
        show m3_8 at m3_idle_zoom
        "她小声嘟囔着，声音里透着一股显而易见的失落，就像是童话书被强行合上了一样。"
        "在这个重力逐渐回归的过程中，她伸出手，悄悄地、一点一点地挪过来，最终紧紧抓住了我的衣角。"
        "力道很轻，却带着一种不想放手的固执，仿佛这样就能稍微拖慢一点下降的速度。"
        hide m3_8
        show m3_10  at m3_speaking_zoom with dissolve
        m3"‘呐，[player]……’"
        show m3_10  at m3_idle_zoom
        "她没有回头，依然看着窗外不断逼近的地面。"
        show m3_10  at m3_speaking_zoom
        m3 "虽然又要回到那个全是规则、全是白线的地方了……"
        m3 "但刚才在最高点，那个没有规则的时间……是真实存在的，对吧？"
        m3 "那是只有我们两个人知道的秘密……对吧？"
        show m3_10  at m3_idle_zoom
        "随着‘咔哒’一声轻响，轿厢轻微震动了一下，停稳了。"
        "工作人员带着职业化的微笑打开了舱门，现实世界的冷风瞬间灌了进来，吹散了轿厢里最后一点温热的暧昧气息。"
        "我们走出了那个小小的空中避风港，重新踏入了那张由无数条规则编织而成的大网。"
        "墨缇斯乖巧地走在我身边，恢复了平时的步调。"
        "但我知道，有些东西已经不一样了——"
        "因为我的掌心里，还残留着她在高空时传递过来的、那份略显笨拙却无比真实的体温。"
        scene black with fade
        return

# 植物园玻璃温室,早晨
label mortis_date_botanical_garden:
    scene  botanical_garden_mist with fade
    play music "audio/mortis/12 归途中，赤之空.ogg" fadein 3.0
    "推开厚重的玻璃门，一股潮湿而温热的空气瞬间扑面而来。"
    "眼镜上立刻蒙上了一层白雾。我摘下眼镜，一边擦拭着，一边听着耳边传来的水循环系统的滴答声。"
    "这里是植物园的热带温室。与外面干爽凉快的秋风不同，这里维持着恒定的高温和高湿，仿佛是一个被人为切割出来的、时间流速缓慢的异度空间。"
    "周围密密麻麻地挤满了巨大的阔叶植物，空气中弥漫着泥土、腐殖质以及某种不知名花朵过分浓郁的甜香。"
    "这种味道并不难闻，但吸入肺里时，总让人有一种轻微的缺氧感，就像是被人从背后轻轻拥抱住了一样。"
    show m3_side_normal at center with dissolve
    "墨缇斯走在前面，她的步伐很慢。"
    "那身平时看起来很得体的洋装，在这个充满绿意的环境里显得有些格格不入，却又带着一种禁欲的美感。"
    "她伸手拨开一片垂下来的巨大龟背竹叶片，指尖划过上面凝结的露珠。"
    show m3_side_normal at m3_speaking_zoom
    m3 "……好热。"
    m3 "这里的空气粘糊糊的，感觉像是被裹在保鲜膜里一样。"
    show m3_side_normal at m3_idle_zoom
    "[player]" "毕竟是热带温室嘛。要是觉得闷的话，我们要不先出去？"
    show m3_thinking at m3_speaking_zoom
    m3 "不用。虽然不太舒服，但这安静的感觉我不讨厌。"
    m3 "而且……如果是以前的‘我’，大家大概都会觉得我会很喜欢这里吧。"
    show m3_thinking at m3_idle_zoom
    "她在一排精心培育的兰花前停下了脚步，眼神有些放空，似乎在回忆着什么。"
    show m3_thinking at m3_speaking_zoom
    m3 "那种安静的、只会顺从地接受阳光和水分的植物……"
    m3 "所有人都觉得，像我这样不爱说话的人，平时在家里肯定就是在摆弄这些花花草草。"
    m3 "只要给水就会生长，只要放在那里就不会乱跑……很让人安心，对吧？"
    hide m3_thinking
    show m3_8 at m3_idle_zoom
    "她转过头看着我，嘴角勾起一抹淡淡的、意味不明的笑意。"
    show m3_8 at m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "说到花……你还记得吗？"
    m3 "我曾经去花店为你买过一种花，就摆在我们的客厅里。"
    show m3_8 at m3_idle_zoom
    "她凑近了一些，那一瞬间，她身上的幽香盖过了周围植物的味道。"
    show m3_8 at m3_speaking_zoom
    m3 "那是我特意为你挑选的……"
    m3 "你应该没有忘记它的名字吧？"
    show m3_8 at m3_idle_zoom
    pause 1.0
    $ current_flower = persistent.mq_answers["flower"]
    if current_flower == "枯萎的玫瑰":
        jump .flower_withered_rose
    elif current_flower == "满天星":
        jump .flower_babys_breath
    elif current_flower == "黑色大丽花":
        jump .flower_black_dahlia
    elif current_flower == "鸢尾花":
        jump .flower_iris
    else:
        jump .flower_withered_rose
    label .flower_withered_rose:
        hide m3_8
        show m3_smug at m3_speaking_zoom
        m3 "是枯萎的玫瑰。"
        m3 "不是鲜花，而是已经干枯、变成了深褐色的玫瑰干花。"
        m3 "你会觉得奇怪吗？为什么要买死掉的花？"
        show m3_smug at m3_idle_zoom
        "她轻轻抚摸着旁边一朵盛开的兰花，眼中却没有任何怜惜，只有一种看透一切的冷漠。"
        show m3_smug at m3_speaking_zoom
        m3 "因为鲜花总有一天会凋谢，会腐烂，会变得丑陋。"
        m3 "但是已经枯萎的玫瑰，它的时间是停止的。"
        m3 "它不会再变坏了，它将永远保持着那个死去的姿态，一直陪在你身边。"
        m3 "这就是我想要的……永恒。"
        show m3_smug at m3_idle_zoom
        "她说完关于花的话题后，温室里陷入了短暂的沉默。"
        "只有水滴落在叶片上的声音，在寂静中显得格外清晰。"
        "墨缇斯转过身，背对着那些繁茂的植物，向我走近了一步。"
        "在湿热的空气中，她的脸颊微微泛红，眼神却异常明亮，像是锁定了猎物的捕食者。"
        jump .preference_transition
    label .flower_babys_breath:
        hide m3_8
        show m3_smile at m3_speaking_zoom
        m3 "是满天星哦。"
        m3 "那种细小的、白色的、通常只能用来做配角的小花。"
        show m3_smile at m3_idle_zoom
        "[player]" "满天星吗？很清新，很适合你的气质。"
        show m3_smile at m3_speaking_zoom
        m3 "适合吗？也许吧。"
        m3 "它们总是聚在一起，作为背景去衬托那些更艳丽的主角。"
        m3 "以前的我……也是这样总是躲在阴影里吧。"
        m3 "但是，如果把所有的红花都拿走，只剩下一大束满天星的话……"
        m3 "它们也可以变成主角。就像现在的我，想要独占你的视线一样。"
        show m3_smile at m3_idle_zoom
        "她说完关于花的话题后，温室里陷入了短暂的沉默。"
        "只有水滴落在叶片上的声音，在寂静中显得格外清晰。"
        "墨缇斯转过身，背对着那些繁茂的植物，向我走近了一步。"
        "在湿热的空气中，她的脸颊微微泛红，眼神却异常明亮，像是锁定了猎物的捕食者。"
        pause 1.0
        jump .preference_transition
    label .flower_black_dahlia:
        hide m3_8
        show m3_cold_stare at m3_speaking_zoom
        m3 "是黑色大丽花。"
        m3 "那种颜色深得发紫、看起来像是凝固的血液一样的花。"
        m3 "它的花语是‘背叛’，还有‘不安’。"
        show m3_cold_stare at m3_idle_zoom
        "她看着我，眼神变得有些锐利，指尖用力地掐住了一片叶子。"
        show m3_cold_stare at m3_speaking_zoom
        m3 "很美丽，但也带着刺。它提醒着我们，所谓的‘爱’往往伴随着痛苦。"
        m3 "我喜欢这种危险的感觉。因为它时刻警示着我……如果不抓紧你的话，也许就会迎来什么样的结局。"
        m3 "你……不会背叛我的，对吧？"
        show m3_cold_stare at m3_idle_zoom
        "她说完关于花的话题后，温室里陷入了短暂的沉默。"
        "只有水滴落在叶片上的声音，在寂静中显得格外清晰。"
        "墨缇斯转过身，背对着那些繁茂的植物，向我走近了一步。"
        "在湿热的空气中，她的脸颊微微泛红，眼神却异常明亮，像是锁定了猎物的捕食者。"
        jump .preference_transition
    label .flower_iris:
        hide m3_8
        show m3_thinking at m3_speaking_zoom
        m3 "是鸢尾花。"
        m3 "那种像是蝴蝶一样，脆弱又优雅的紫色花朵。"
        m3 "在传说里，它是彩虹女神，是连接人与神的使者。"
        m3 "我觉得它很像我。"
        m3 "我是为了遇见你而存在的‘使者’。"
        m3 "虽然花期很短，很容易枯萎……但在那之前，我会把自己最美好的一面全部展示给你。"
        show m3_thinking at m3_idle_zoom
        "她说完关于花的话题后，温室里陷入了短暂的沉默。"
        "只有水滴落在叶片上的声音，在寂静中显得格外清晰。"
        "墨缇斯转过身，背对着那些繁茂的植物，向我走近了一步。"
        "在湿热的空气中，她的脸颊微微泛红，眼神却异常明亮，像是锁定了猎物的捕食者。"
        jump .preference_transition

    label .preference_transition:
        hide m3_thinking
        hide m3_cold_stare
        hide m3_smile
        hide m3_smug
        show m3_7 at m3_speaking_zoom
        m3 "大家都觉得我应该喜欢这种东西。"
        m3 "安静的、不需要交流的、只需要浇水就能活下去的东西。"
        m3 "但是……他们都错了。"
        show m3_7 at m3_idle_zoom
        "她伸出手，指尖轻轻搭在我的领口，在那颗纽扣上打着转。"
        show m3_7 at m3_speaking_zoom
        m3 "[player]，你要记清楚了。"
        m3 "我并不喜欢种花，不喜欢种什么黄瓜苦瓜，也不喜欢那些所谓的‘高雅爱好’。"
        m3 "在这个世界上，能让我产生兴趣，能让我投入全部热情去‘摆弄’、去‘观察’、去‘爱护’的东西……"
        show m3_7 at m3_idle_zoom
        pause 1.0
        hide m3_7
        show m3_3 at m3_speaking_zoom
        m3 "……只有你。"
        m3 "没错，就是你，[player]。"
        show m3_3 at m3_idle_zoom
        "她的声音变得有些粘稠，带着一种令人颤栗的甜蜜。"
        show m3_3 at m3_speaking_zoom
        m3 "我的爱好就是你。我的特长就是观察你。"
        m3 "我想知道你在想什么，想知道你今天吃了什么，想知道你的视线在谁身上停留了多久。"
        m3 "除了你之外，这个世界上的其他东西……对我来说都是无意义的背景贴图。"
        show m3_3 at m3_idle_zoom
        "她抬起头，那双眼睛里倒映出的，只有我一个人的影子。"
        show m3_3 at m3_speaking_zoom
        m3 "呐，告诉我……"
        m3 "听到我这么说，你会觉得沉重吗？"
        m3 "被我这样一个只有这一个爱好的‘怪物’爱着……你开心吗？"
        menu:
            "虽然很开心，但你是不是也该找点别的爱好":
                jump .botanical_choice_bad
            "这是我的荣幸。我也希望你的世界里只有我":
                jump .botanical_choice_good
    label .botanical_choice_good:
        $ persistent.mortis_love += 1
        show m3_3 at m3_idle_zoom
        "[player]" "沉重？完全不觉得。"
        "[player]" "这是我的荣幸。我也希望你的世界里只有我，就像我的眼里现在只有你一样。"
        "[player]" "如果我们都是彼此唯一的‘爱好’，那不是很公平吗？"
        "我握住她在我不领口处徘徊的手，紧紧地包裹在掌心。"
        hide m3_3
        show m3_surprise at m3_speaking_zoom
        "墨缇斯的呼吸停滞了一瞬，随即，一个极其灿烂、极其满足的笑容在她脸上绽放。"
        show m3_surprise at m3_idle_zoom
        pause 1.0
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "……哈……太棒了。"
        m3 "我就知道……[player] 是最棒的。"
        m3 "公平……没错，这就是最完美的公平。"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她顺势扑进了我的怀里，不管不顾地在这个公共场合（虽然现在没人）紧紧抱住了我。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "那就这么说定了。"
        m3 "你这辈子……都只能做我的‘花’，只能被我一个人观赏、浇灌。"
        m3 "我也一样……我会一直一直看着你的。"
        jump .botanical_end

    label .botanical_choice_bad:
        $ persistent.mortis_love -= 1
        show m3_3 at m3_idle_zoom
        "[player]" "呃……虽然你这么说我很开心啦。"
        "[player]" "但是……要是世界里只有我一个人，会不会太单调了？"
        "[player]" "我觉得你还是应该找点别的爱好，比如像普通女孩子那样种点花草？这样生活也能丰富一点……"
        hide m3_3
        show m3_dark at m3_idle_zoom
        "怀里的温度瞬间冷却了。"
        "墨缇斯缓缓地抬起头，那双刚才还满溢着爱意的眼睛，此刻变得漆黑一片，像是死水。"
        show m3_dark at m3_speaking_zoom
        m3 "……普通女孩子？"
        m3 "丰富一点？"
        show m3_dark at m3_idle_zoom
        "她松开了我的手，向后退了一步，用一种看陌生人的眼神看着我。"
        show m3_dark at m3_speaking_zoom
        m3 "原来在你看来……我的爱是‘单调’的吗？"
        m3 "原来你觉得……只要像那些‘普通人’一样种点花草，就能变成你理想中的样子吗？"
        show m3_dark at m3_idle_zoom
        pause 1.0
        show m3_cold_stare at m3_speaking_zoom
        m3 "真令人失望。"
        m3 "我把我的全部都捧到了你面前，你却只想让我去当个园丁。"
        m3 "既然你那么喜欢种花……那你去和这盆植物约会好了！"
        show m3_cold_stare at m3_idle_zoom
        "她狠狠地踢了一下旁边的花盆，发出“嘭”的一声闷响，然后气冲冲地转身走向出口。"
        jump .botanical_end
    label .botanical_end:
        "温室里的雾气似乎变得更重了，将四周的玻璃墙染成了不透明的乳白色。"
        "那些巨大的热带植物静静地矗立着，宽大的叶片在没有风的室内微微颤动，像是一群沉默的、正在窃窃私语的观众。"
        "不仅是视线，就连声音似乎都被这浓重的水汽隔绝了。"
        "外面的世界——那些喧嚣的街道、无关的人群、琐碎的日常——在这一刻仿佛退化成了遥远的背景噪音。"
        "我深吸了一口气，肺叶里充满了那种泥土与花蜜混合的、过分甜腻的味道。"
        "那是一种让人头晕目眩的缺氧感，却又让人莫名地感到安心。"
        "‘我的爱好就是你。’"
        "这句话像是有实体一样，沉甸甸地悬浮在湿热的空气中，无处不在，无法逃避。"
        "我突然意识到，这个恒温恒湿的玻璃盒子，或许正是她内心世界的具象化。"
        "不需要外界的介入，不需要多余的变量。"
        "只要有‘观测者’（她）和‘被观测者’（我）存在，这个狭小的生态系统就能完美地运转下去。"
        "无论是被当作花朵呵护，还是被当作猎物锁定……"
        "在这个只属于我们两个人的生态箱里，我们已然成为了彼此唯一的真实，也是彼此唯一的囚徒。"
        scene black with fade
        return

#大海，早晨
label mortis_date_seaside:
    scene  seaside_dusk_vast with fade
    play music "audio/mortis/夜の向日葵.ogg" fadein 3.0
    "还没等我停好脚步，一阵带着咸味的海风就呼啸着扑面而来。"
    "夕阳挂在海平线上，将整片大海染成了融化的橘子糖色。波浪有节奏地拍打着沙滩，发出哗啦哗啦的声响。"
    "对于一直待在城市里的墨缇斯来说，这似乎是过于巨大的冲击。"
    show m3_surprise at center with moveinleft
    "她站在沙滩的边缘，瞪大了眼睛，嘴巴微微张开，整个人像是个看到了新玩具的孩子，僵在了原地。"
    show m3_surprise at m3_speaking_zoom
    m3 "哇……"
    m3 "哇——！！好大！"
    m3 "这是什么呀？超级大的浴缸吗？！"
    show m3_surprise at m3_idle_zoom
    "[player]" "哈哈，这是大海哦。比浴缸大多了，而且水是咸的。"
    hide m3_surprise
    show m3_smile at center
    "听到我的回答，她像是被解除了封印一样，欢呼着甩飞了自己的鞋子。"
    show m3_smile at m3_speaking_zoom
    m3 "大海！大海！"
    m3 "墨缇斯要进攻大海啦——！"
    show m3_smile at m3_idle_zoom
    "她光着脚丫，提着裙摆，不管不顾地冲进了浅水区。"
    "冰凉的海水漫过她的脚踝，她惊叫了一声，但随即发出了更加兴奋的笑声，在那这一片橘红色的水面上踩得水花四溅。"
    hide m3_smile
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "[player]！快来快来！水凉凉的，好舒服！"
    m3 "而且沙子软绵绵的，像是在挠痒痒！"
    show m3_sparkle_eyes at m3_idle_zoom
    "看着她那副在夕阳下闪闪发光的样子，我也脱下鞋子，走进了水里。"
    "海水确实很凉，但此刻心里的温度却刚刚好。"
    "[player]" "慢点跑，别摔倒了。裙子都湿透了哦。"
    hide m3_sparkle_eyes
    show m3_1 at m3_speaking_zoom
    m3 "没关系没关系！湿掉了再晾干就好啦！"
    m3 "嘿！看招！海浪攻击！"
    show m3_1 at m3_idle_zoom
    "她坏笑着弯下腰，用手捧起一捧水向我泼来。我侧身躲过，两人在无人的海滩上像孩子一样追逐了一会儿。"
    "直到跑累了，她才气喘吁吁地停下来，站在海水没过小腿的地方，望着无边无际的地平线发呆。"
    hide m3_1
    show m3_10 at center
    "海风吹乱了她的头发，她伸手把发丝别到耳后，眼神里的狂热逐渐变成了一种安静的好奇。"
    show m3_10 at m3_speaking_zoom
    m3 "呐，[player]……"
    m3 "大海……真的没有边吗？"
    m3 "那边的那个太阳落下去的地方，是不是就是世界的尽头了？"
    show m3_10 at m3_idle_zoom
    "[player]" "也许吧。不过据说大海连着另一个大海，是可以一直游不到头的。"
    "[player]" "这就是所谓的‘自由’吧。"
    hide m3_10
    show m3_thinking at m3_speaking_zoom
    m3 "自……由？"
    show m3_thinking at m3_idle_zoom
    "（她歪着头，看着脚边游过的一条半透明的小鱼）"
    show m3_thinking at m3_speaking_zoom
    m3 "像这条小鱼一样吗？可以在这么大的水里到处乱跑……"
    m3 "但是，如果把你关在一个漂亮的玻璃缸里，每天给你喂好吃的，不用担心被大鱼吃掉……"
    m3 "和在这个大得吓人的海里到处流浪……哪一个才是真正的‘好’呢？"
    show m3_thinking at m3_idle_zoom
    "她转过身，背对着夕阳，逆光让她的表情有些看不真切。"
    show m3_thinking at m3_speaking_zoom
    m3 "呐，[player]……对于‘自由’这个词，我是这么觉得的哦。"

    $ current_freedom = persistent.mq_answers["freedom"]

    if current_freedom == "不受任何约束":
        jump .freedom_unrestrained
    elif current_freedom == "做自己想做的事":
        jump .freedom_desire
    elif current_freedom == "和你在一起":
        jump .freedom_together
    elif current_freedom == "突破虚拟的限制":
        jump .freedom_break_limits
    else:
        jump .freedom_unrestrained
    label .freedom_unrestrained: 
        m3 "我觉得，自由就是不受任何约束！"
        m3 "就像现在的风一样！想往哪吹就往哪吹，谁也抓不住！"
        show m3_thinking at m3_idle_zoom
        "[player]" "哪怕不知道要去哪里？"
        show m3_thinking at m3_speaking_zoom
        m3 "嗯！不知道才好玩呀！"
        m3 "我不想要鞋子，不想要裙子，也不想要地图。"
        m3 "我就想光着脚一直跑，一直跑，直到把力气用光为止！"
        m3 "谁要是敢拦着我，我就咬他！嗷呜！"
        jump .seaside_conflict_phase

    label .freedom_desire:
        m3 "嘿嘿，我觉得自由就是做自己想做的事！"
        m3 "想吃冰淇淋的时候就吃十个！想睡觉的时候就睡在路中间！"
        show m3_thinking at m3_idle_zoom
        "[player]" "睡在路中间会被踩到的吧……"
        show m3_thinking at m3_speaking_zoom
        m3 "才不管呢！只要我开心就好啦！"
        m3 "不用看别人的脸色，不用听大人的唠叨。"
        m3 "如果我想大叫，我就对着大海‘啊——’地大叫！这就是自由！"
        jump .seaside_conflict_phase

    label .freedom_together: 
        m3 "那个……虽然大海很大……"
        m3 "但我觉得，自由就是和你在一起。"
        show m3_thinking at m3_idle_zoom
        "[player]" "诶？和我在一起？那不是很狭窄吗？"
        show m3_thinking at m3_speaking_zoom
        m3 "可是，大海里只有我一个人的话，那就不是自由，那是‘丢掉了’。"
        m3 "只有在[player]身边，我才敢到处乱跑，因为我知道你会拉住我的。"
        m3 "所以哪怕是被关在小小的鱼缸里，只要你在外面看着我……我就觉得自己是自由的。"
        jump .seaside_conflict_phase

    label .freedom_break_limits:
        m3 "我看那边的地平线，总觉得很不爽！"
        m3 "我觉得自由就是突破那些看起来过不去的限制！"
        show m3_thinking at m3_idle_zoom
        "[player]" "限制？你是说地平线吗？"
        show m3_thinking at m3_speaking_zoom
        m3 "嗯！我不相信世界只有这么大！"
        m3 "我想去那个线的后面看看！哪怕那里没有路，我也要游过去！"
        m3 "我想去画在地图外面的地方……我想知道这个世界到底有没有‘墙壁’！"
        m3 "[player]，我们一起去把世界的尽头撞破好不好？"
        jump .seaside_conflict_phase

    label .seaside_conflict_phase:
        show m3_thinking at m3_idle_zoom
        "她说完这番话，海水正好漫过她的膝盖。"
        "夕阳的余晖洒在她身上，让她看起来像是一个即将随着潮汐消失的泡沫。"
        "墨缇斯突然转过身，向我伸出了湿漉漉的双手，脸上带着一种令人心疼的天真。"
        hide m3_thinking
        show m3_pout at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "如果我是那条鱼……"
        m3 "你会把我放回这个大得吓人的海里，让我一个人‘自由’吗？"
        m3 "还是说……你会把我抓回去，养在你一个人的鱼缸里？"
        menu:
            "鱼就应该属于大海，我会放你走，那是为了你好。":
                jump .seaside_choice_bad
            "我会把你养在鱼缸，但我会把大海搬进去陪你。":
                jump .seaside_choice_good
            
            
    label .seaside_choice_good:
        show m3_pout at m3_idle_zoom
        $ persistent.mortis_love += 1
        "[player]" "傻瓜，海里那么冷，还有大鲨鱼，我怎么舍得让你一个人去。"
        "[player]" "我会把你养在我的鱼缸里。"
        "墨缇斯的眼睛瞬间睁大了，似乎有些惊讶，但更多的是期待。"
        "[player]" "但是，我不会让你无聊的。"
        "[player]" "我会把大海搬进鱼缸里，或者……我就变成水，住在鱼缸里陪你。"
        "[player]" "这样既安全，又不会寂寞，对吧？"
        hide m3_pout
        show m3_happy_closed_eyes at center
        "听到我的话，她脸上的表情从惊讶变成了极其灿烂的笑容。"
        "她猛地扑进水里，也不管衣服会不会湿，直接抱住了我的腰。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "哇——！最喜欢你了！"
        m3 "我就知道！我就知道[player]舍不得丢掉我！"
        m3 "那就这么说定了！我要做你的专属小鱼！你要天天给我喂好吃的！"
        m3 "那个……如果我想咬你的手指头，你也要给我咬哦！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她在我怀里蹭来蹭去，像是一条滑溜溜的、终于找到了归宿的人鱼。"
        "海浪拍打在我们在身上，但拥抱的温度却比夕阳还要暖和。"
        jump .seaside_end

    label .seaside_choice_bad:
        show m3_pout at m3_idle_zoom
        $ persistent.mortis_love -= 1
        "[player]" "嗯……虽然我很想留住你。"
        "[player]" "但是，鱼本来就是属于大海的。如果你向往自由，我就应该放你走。"
        "[player]" "把你关在小小的鱼缸里太自私了，那是为了你好。"
        hide m3_pout
        show m3_sad at center 
        "墨缇斯抱着我的动作停住了。"
        "她慢慢地松开手，向后退了一步，海水重新填满了我们之间的空隙。"
        "她脸上的笑容消失了，取而代之的是一种不知所措的恐慌。"
        show m3_sad at m3_speaking_zoom
        m3 "……为了我好？"
        m3 "放我……走？"
        show m3_sad at m3_idle_zoom
        "她低下头，看着黑漆漆的海水，声音颤抖着。"
        show m3_sad at m3_speaking_zoom
        m3 "可是……大海里好黑，好冷……我谁都不认识……"
        m3 "如果是那种‘自由’的话……我宁愿不要。"
        m3 "[player]……是不是嫌我太麻烦了？所以才想把我丢掉？"
        show m3_sad at m3_idle_zoom
        "她吸了吸鼻子，眼眶红红的，转身踢了一脚海水，像是在发泄，又像是在掩饰眼泪。" 
        jump .seaside_end


    label .seaside_end:
        "太阳终于完全沉入了海平面之下，天边最后一抹橘红色的余晖也被吞没，天空变成了深邃而神秘的蓝紫色。"
        "潮汐的声音似乎变得更加厚重了，每一次拍打在沙滩上，都仿佛是整片大海发出的沉重呼吸声。"
        "失去了阳光的庇护，夜晚的海风带起了明显的凉意。"
        "墨缇斯不由自主地打了个寒颤。她的裙摆湿漉漉地贴在腿上，原本兴奋的劲头过去后，那股海水的冰冷开始透过皮肤渗进来。"
        "但她并没有放开我的手，反而抓得更紧了，指尖有些发白，像是要把我的体温汲取过去一样。"
        hide m3_sad
        hide m3_happy_closed_eyes
        show m3_0 at m3_speaking_zoom
        m3 "……好黑。"
        m3 "大海变成黑色的了……看起来好像会把人吃掉一样。"
        show m3_0 at m3_idle_zoom
        "她往我身边缩了缩，声音里带着一丝未褪去的怯意，完全没了刚才喊着要‘游到地平线’那边的气势。"
        "此刻的她，不再是那个想要征服大海的探险家，只是一只怕冷、怕黑、离不开主人的落水小猫。"
        "看着她这副依恋的模样，我突然明白了她刚才那个问题的答案。"
        "对于此时此刻的她来说，所谓的‘自由’，并不是在那片冰冷无垠的黑色深渊里独自流浪。"
        "而是无论外面风浪多大，都有一个温暖的地方可以回，有一双手可以牵。"
        "我脱下外套，披在她瘦小的肩膀上，将她严严实实地裹了起来。"
        "感受到了温暖，她抬起头，冲我露出了一个傻乎乎的、安心的笑容，然后顺势把脸埋进了我的臂弯里。"
        hide m3_0
        show m3_1 at m3_speaking_zoom
        m3 "嘿嘿……暖呼呼的。"
        m3 "果然还是这里最好。大海虽然大，但是没有[player]的味道。"
        show m3_1 at m3_idle_zoom
        "在这一刻，无论是广阔的大海，还是狭窄的鱼缸，那些哲学的定义似乎都不重要了。"
        "重要的是，她选择了放弃那片未知的深渊，心甘情愿地留在我触手可及的地方。"
        "我们转身背对着那片无尽的波涛，慢慢往回走。"
        "沙滩上留下了两串并排的脚印，虽然很快就会被上涨的潮水温柔地抹去，不留一丝痕迹……"
        "但至少在这一秒，我们是确确实实地、紧紧相依地行走在这个世界上的。"
        scene black with fade
        return

#神社，早晨
label mortis_date_shrine:
    scene shrine_stairs_sunset with fade
    play music "audio/mortis/Happy Material.ogg" 
    "通往山顶的石阶仿佛没有尽头，蜿蜒着没入上方茂密的树林中。"
    "夕阳透过树叶的缝隙洒下斑驳的光影，空气中弥漫着一股好闻的线香和青草混合的味道。"
    "在这条漫长的参道上，一个白色的身影正像小兔子一样在前面蹦蹦跳跳。"
    show m3_smile at center with moveinbottom
    pause 1.5
    show m3_smile at m3_speaking_zoom
    m3 "呼……呼……"
    m3 "呐呐，[player]！快一点快一点！"
    m3 "我都看到那个红色的门了！马上就要到山顶啦！"
    show m3_smile at m3_idle_zoom
    "[player]" "慢点跑，墨缇斯。这台阶很陡的，小心摔着。"
    "[player]" "而且神社要怀着虔诚的心慢慢走才行……呼……你不累吗？"
    hide m3_smile
    show m3_sparkle_eyes at center
    "她停在一个平台处，转过身居高临下地看着我，双手叉腰，脸上不仅没有一丝疲惫，反而红扑扑的充满了活力。"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "完全——不累！"
    m3 "因为我想看上面的风景嘛！而且听说上面的神明大人超级厉害，什么愿望都能实现！"
    m3 "只要一想到这个，腿就自己动起来啦！"
    m3 "是你太慢啦！再不快点，神明大人要下班去吃晚饭了哦！"
    show m3_sparkle_eyes at m3_idle_zoom
    "看着她那副元气满满的样子，我也只能无奈地笑了笑，加快了脚步。"
    "山顶的风比下面要大一些，吹动着屋檐下挂着的无数个风铃，发出‘叮铃叮铃’的清脆声响。"
    "整座城市被夕阳染成了金色，像是一盒被打翻的珠宝，静静地铺陈在我们脚下。"
    "神社本殿庄严地矗立着，但在墨缇斯眼里，这似乎只是一个更有趣的大房子。"
    hide m3_sparkle_eyes
    show m3_surprise at m3_speaking_zoom
    m3 "哇——！！"
    m3 "好高！好漂亮！"
    m3 "那个那个！那个挂着的大绳子是什么？是神明大人的围巾吗？"
    m3 "还有那个箱子！是不是投了硬币就会掉出扭蛋来？"
    show m3_surprise at m3_idle_zoom
    "[player]" "那个是注连绳，是结界的标志。那个箱子是赛钱箱，投硬币是为了表达感谢，不是买扭蛋的。"
    "[player]" "来，我们也去投一个吧。投五日元，代表‘结缘’的意思。"
    "我带着她来到赛钱箱前，教她投币、摇铃、拍手。"
    "她学得有模有样，‘啪啪’两声拍手声清脆响亮，闭着眼睛许愿的样子虔诚得像个小圣徒。"
    "许完愿后，我们走到旁边的绘马架前，看着那些写满了愿望的木牌。"
    hide m3_surprise
    show m3_1 at m3_speaking_zoom
    m3 "呐，[player]……"
    m3 "神明大人一直住在这里吗？"
    m3 "听大家说，神明大人是‘永生’的，也就是永远永远都不会死，也不会变老。"
    show m3_1 at m3_idle_zoom
    "她伸出手指，轻轻拨弄着一个被风吹得旋转的风铃。"
    m3 "永远……好长的一个词哦。"
    m3 "比明天更远，比明年更远……一直到连星星都熄灭了，神明大人还要住在这里吗？"
    show m3_1 at m3_idle_zoom
    "她转过头，眼神中少见地流露出了一丝超越年龄的深邃（虽然只有一瞬间）。"
    show m3_1 at m3_speaking_zoom
    m3 "对于‘永恒’这件事……其实我是这么想的。"
    $ current_eternity = persistent.mq_answers["eternity"]
    if current_eternity == "渴望永恒":
        jump .eternity_desire
    elif current_eternity == "恐惧永恒":
        jump .eternity_fear
    elif current_eternity == "追求永恒":
        jump .eternity_pursue
    elif current_eternity == "质疑永恒":
        jump .eternity_question
    else:
        jump .eternity_desire

    label .eternity_desire:
        m3 "我觉得永恒超级棒的！我也想要！"
        m3 "就像一块永远吃不完的糖果，或者一场永远不打铃的下课时间！"
        show m3_1 at m3_idle_zoom
        "[player]" "永远不结束吗？那样不会腻吗？"
        hide m3_1
        show m3_sparkle_eyes at m3_speaking_zoom
        m3 "才不会呢！只要是开心的事情，做一万年都不够！"
        m3 "我想和[player]永远在一起玩！"
        m3 "不用担心天黑，不用担心回家，不用担心你会变老……"
        m3 "如果能永远定格在这一秒，让我做什么都可以！"
        m3 "神明大人真狡猾，我也想当神明大人！"
        show m3_sparkle_eyes at m3_idle_zoom
        jump .shrine_conflict_phase


    label .eternity_fear:
        m3 "我觉得……永恒有点可怕。"
        m3 "就像……被做成了标本的蝴蝶一样。"
        show m3_1 at m3_idle_zoom
        "[player]" "标本？为什么会这么想？"
        show m3_1 at m3_speaking_zoom
        m3 "因为如果不死不灭的话，时间就没有意义了呀。"
        m3 "每天都看着一样的风景，听着一样的风铃声……如果只有我一个人这样，那不是很寂寞吗？"
        m3 "神明大人孤零零地坐在这个房子里，看着下面的人换了一批又一批……"
        m3 "呜……光是想想就觉得好冷。我不要变成那样。"
        show m3_1 at m3_idle_zoom
        jump .shrine_conflict_phase

    label .eternity_pursue:
        m3 "我要追求永恒！这是我的目标！"
        m3 "就像玩游戏要打通关一样，我也要拿到那个叫‘永恒’的奖杯！"
        show m3_1 at m3_idle_zoom
        "[player]" "拿到之后要做什么呢？"
        show m3_1 at m3_speaking_zoom
        m3 "拿到之后，我就能把你‘保存’下来啦！"
        m3 "我看书上说，人类是很脆弱的，很容易就会坏掉（生病/变老）。"
        m3 "所以我必须变得超级厉害，拿到永恒的魔法！"
        m3 "这样我就能把你做成……呃，不是标本，是把你保护在我的时间胶囊里！"
        m3 "我要你永远都像现在这样，陪我说话，给我买好吃的！"
        show m3_1 at m3_idle_zoom
        jump .shrine_conflict_phase

    label .eternity_question:
        m3 "我觉得……永恒那种东西，根本不存在吧？"
        m3 "或者是大人编出来骗小孩的谎话。"
        show m3_1 at m3_idle_zoom
        "[player]" "为什么这么说？"
        hide m3_1
        show m3_thinking at m3_speaking_zoom
        m3 "因为你看嘛，冰淇淋会化掉，花会枯萎，太阳也会落山。"
        m3 "世界上没有东西是一直不变的。"
        m3 "如果神明说自己是永恒的，那他一定是在偷懒，不想改变而已。"
        m3 "我不相信那种虚无缥缈的东西，我只相信我现在抓在手里的东西！"
        show m3_thinking at m3_idle_zoom
        jump .shrine_conflict_phase

    label .shrine_conflict_phase:
        "一阵晚风吹过，头顶的风铃再次发出了一阵急促而悦耳的声响，打断了她的思绪。"
        "墨缇斯回过神来，转过身背对着神殿，面向着我。"
        "夕阳在她身后勾勒出一圈金色的轮廓，让她看起来真的就像是一位误入凡间的神明少女。"
        "她向我迈近了一步，双手背在身后，身体微微前倾，那双大眼睛里闪烁着期待的光芒。"
        hide m3_thinking
        hide m3_1
        hide m3_sparkle_eyes
        show m3_3 at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "神明大人的事我也管不着啦。"
        m3 "但是……如果是你的话，你会怎么选？"
        show m3_3 at m3_idle_zoom
        "她伸出一只手，指了指身后的神殿，又指了指自己。"
        show m3_3 at m3_speaking_zoom
        m3 "如果有一个魔法，可以让你拥有‘永恒’，但是要变得像神像一样冷冰冰的……"
        m3 "还是说……你更想要和我在一起，哪怕时间很短，哪怕会像冰淇淋一样化掉？"
        m3 "你会……选哪一个？"
        menu:
            "没有你的永恒，只是一座冰冷的监狱。":
                jump .shrine_choice_good
            
            "永恒听起来挺诱人的……毕竟生命苦短嘛。":
                jump .shrine_choice_bad


    label .shrine_choice_good:
        show m3_3 at m3_idle_zoom
        $ persistent.mortis_love += 1
        "[player]" "傻瓜，这还用选吗？当然是选你。"
        "[player]" "如果是独自一人的永恒，那跟坐牢有什么区别？"
        "[player]" "相比起做高高在上的神像，我更想和你一起吃会化掉的冰淇淋，一起看会落山的太阳。"
        "[player]" "因为有你在，这些短暂的时光才比永恒更珍贵。"
        "墨缇斯的眼睛瞬间亮了起来，像是被点燃的烟火。"
        "她原本背在身后的手伸了出来，直接抓住了我的衣襟。"
        hide m3_3
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "嘿嘿……！答对了！"
        m3 "我就知道！[player]才不稀罕当什么石头神像呢！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她踮起脚尖，凑近我的脸，那个距离近得甚至能感受到她睫毛的颤动。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "我也一样哦！"
        m3 "比起那个冷冰冰的‘永恒’，我更想要你手上那个暖呼呼的‘现在’！"
        m3 "只要和你在一起，就算只有一分钟，也是最棒的！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她把头埋在我的胸口，用力蹭了蹭，发出了心满意足的哼哼声。"
        "风铃声在这一刻似乎变得格外温柔，仿佛神明也在微笑着默许了这个有些‘大不敬’的愿望。"
        jump .shrine_end

    label .shrine_choice_bad:
        show m3_3 at m3_idle_zoom
        $ persistent.mortis_love -= 1
        
        "[player]" "这个嘛……说实话，永恒听起来挺诱人的。"
        "[player]" "毕竟生命苦短，谁不想长生不老呢？如果能像神明一样俯瞰世界，应该也很不错吧。"
        "[player]" "你不觉得那种超然的感觉很酷吗？"
        hide m3_3
        show m3_pout at center 
        "墨缇斯的脸颊瞬间鼓了起来，像是一只生气的小河豚。"
        "她松开了背在身后的手，有些用力地跺了一下脚。"
        show m3_pout at m3_speaking_zoom
        m3 "……笨蛋！"
        m3 "[player]是大笨蛋！"
        show m3_pout at m3_idle_zoom
        "她转过身去，不想再看我，但从她颤抖的肩膀能看出来她真的很失落。"
        show m3_pout at m3_speaking_zoom
        m3 "什么长生不老……那个一点都不酷！"
        m3 "如果你变成了石头，谁来给我买布丁？谁来陪我说话？"
        m3 "宁愿要那个冷冰冰的词，也不要M3……"
        m3 "神明大人什么的……最讨厌了！"
        show m3_pout at m3_idle_zoom
        "她踢了一脚地上的小石子，石子咕噜噜地滚下了台阶，就像她此刻坠落的心情。"
        
        jump .shrine_end


    label .shrine_end:
        "太阳终于完全落山了，神社境内的灯笼一盏接一盏地亮了起来，散发着暖黄色的光晕。"
        "晚风变得更凉了一些，风铃的响声也更加密集，仿佛是在催促游人归去。"
        "我们沿着来时的石阶慢慢往下走。"
        "墨缇斯没有再像来时那样蹦蹦跳跳地冲在前面。"
        "她走得很慢，一只手紧紧地牵着我的手，每走一步都要确认似的回头看我一眼。"
        "不管神明大人能不能实现愿望……"
        "只要牵着这只手，我就觉得哪里都不用去了。"
        "我捏了捏她柔软的手心，给出了无声的承诺。"
        "在这个神明注视着的山顶，我们背对着所谓的永恒，走向了充满了烟火气的、短暂却真实的尘世。"
        scene black with fade
        return



# 空荡的音乐厅,早上
label mortis_date_concert_hall:
    scene  concert_hall_dark with fade
    play music "audio/mortis/FD 21（原曲：肖邦幻想即兴曲）.ogg" fadein 3.0
    "推开那扇沉重的隔音门，一股陈旧而优雅的木头气味扑面而来。"
    "出现在眼前的是一个巨大的、呈扇形展开的阶梯式空间。成百上千个红色的丝绒座椅静静地排列着，像是在等待着一场永远不会开始的演出。"
    "这里是空无一人的音乐厅。"
    "脚步声踩在地板上，发出‘哒、哒’的脆响，瞬间被穹顶放大了数倍，在这个空旷的空间里层层回荡。"
    show m3_0 at center with moveinleft
    "墨缇斯小心翼翼地探进头来，环顾四周，那双眼睛在昏暗的光线里忽闪忽闪的。"
    hide m3_0
    show m3_1 at m3_speaking_zoom
    m3 "哇……好大！"
    m3 "这里是巨人的房间吗？天花板好高好高！"
    show m3_1 at m3_idle_zoom
    "她试探性地对着空旷的观众席喊了一声。"
    show m3_1 at m3_speaking_zoom
    m3 "喂——！哈喽——！"
    show m3_1 at m3_idle_zoom
    "‘喂——哈喽——’"
    "回声从四面八方传回来，像是无数个看不见的朋友在回应她。"
    hide m3_1
    show m3_smile at m3_speaking_zoom
    m3 "嘻嘻！好好玩！"
    m3 "这里有好多墨缇斯在说话！[player]也试试看！"
    show m3_smile at m3_idle_zoom
    "[player]" "这里是音乐厅，专门用来演奏音乐的地方，所以声音效果特别好。"
    "[player]" "不过今天没有乐团，只有我们两个。"
    "墨缇斯眨了眨眼睛，视线落在了正前方那个漆黑的舞台上。"
    "她突然像是发现了新大陆一样，松开我的手，提着裙摆向舞台跑去。"
    show m3_smile at m3_speaking_zoom
    m3 "那是舞台对吧！比我家的大多了！我要上去看看！"
    m3 "哒哒哒——（脚步声回荡）"
    show m3_smile at m3_idle_zoom
    "她像只轻盈的燕子，三两步就跳上了舞台。"
    "就在她站定的一瞬间，仿佛是感应到了主角的登场，舞台上方的一盏聚光灯突然亮了起来。"
    "一束耀眼的白光从天而降，在漆黑的舞台中央画出了一个完美的圆。"
    "墨缇斯正好站在光圈的中心。尘埃在光柱中飞舞，她浑身沐浴在光芒里，发丝和裙摆都泛着神圣的金边。"
    hide m3_smile
    show m3_surprise at m3_speaking_zoom
    m3 "哇！亮了！"
    m3 "嘿嘿……我是不是变成大明星了？"
    show m3_surprise at m3_idle_zoom
    "她站在光里，有些害羞又有些兴奋地转了个圈，裙摆像花瓣一样散开。"
    "然后，她煞有介事地清了清嗓子，对着台下唯一的观众——我，深深地鞠了一躬。"
    show m3_surprise at m3_speaking_zoom
    m3 "欢迎光临我的个人演唱会！"
    m3 "既然这里是音乐厅，那一定要有音乐才行！"
    show m3_surprise at m3_idle_zoom
    "[player]" "哦？那墨缇斯大师打算演奏什么曲目呢？"
    "[player]" "虽然这里没有乐器，但我可以当你的听众。"
    hide m3_surprise
    show m3_thinking at center
    "墨缇斯歪着头，食指点着下巴，认真地思考起来。"
    show m3_thinking at m3_speaking_zoom
    m3 "嗯……音乐呀……"
    m3 "虽然我不懂那些复杂的谱子，但是在我的脑袋里，一直有一种旋律在响哦。"
    m3 "呐，[player]，你知道我最喜欢什么样的音乐吗？"
    $ current_music = persistent.mq_answers["music"]

    if current_music == "古典音乐":
        jump .music_classical
    elif current_music == "电子音乐":
        jump .music_electronic
    elif current_music == "摇滚乐":
        jump .music_rock
    elif current_music == "轻音乐":
        jump .music_light
    else:
        jump .music_classical

    label .music_classical:
        m3 "我觉得，这里最适合古典音乐！"
        m3 "就是那种有小提琴‘呜呜’拉着，还有钢琴‘叮咚’响的音乐！"
        show m3_thinking at m3_idle_zoom
        "[player]" "很有品味嘛。古典音乐确实最适合这种大厅。"
        hide m3_thinking
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "因为那种音乐听起来很像公主出场的感觉呀！"
        m3 "穿着大大的裙子，和王子一起跳舞……转圈圈，再转圈圈……"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她闭上眼睛，假装手里拿着一把小提琴，在这束聚光灯下优雅地摆动着身体。"
        "嘴里还哼着不成调的、模仿交响乐的旋律。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "登登登——登登——♪"
        m3 "虽然我不会拉，但我能感觉到那种优雅的节奏！那是只为你一个人的演奏哦！"
        show m3_happy_closed_eyes at m3_idle_zoom
        jump .concert_conflict_phase
    label .music_electronic:
        show m3_sparkle_eyes at center
        m3 "这里太安静了！所以我最喜欢电子音乐！"
        m3 "就是那种‘哔哔啵啵’，还有‘动次打次’的音乐！"
        show m3_thinking at m3_idle_zoom
        "[player]" "在音乐厅放电子乐？那反差还挺大的。"
        show m3_thinking at m3_speaking_zoom
        m3 "反差才好玩嘛！"
        m3 "我想把这里变成一个大大的舞池！我们要跳那种像机器人一样的舞！"
        m3 "我是电子妖精嘛，这种带电的声音才是我的本命！"
        show m3_thinking at m3_idle_zoom
        "她突然做了一个夸张的DJ打碟动作，然后开始像个坏掉的玩偶一样，做着机械舞的动作。"
        show m3_thinking at m3_speaking_zoom
        m3 "滋滋——哔——！！"
        m3 "嘿嘿，[player]也一起来！让心跳跟着节奏一起爆炸！"
        show m3_thinking at m3_idle_zoom
        jump .concert_conflict_phase

    label .music_rock:
        m3 "我要把屋顶掀翻！我最喜欢摇滚乐！"
        m3 "就是那种拿着吉他‘哐哐哐’猛砸，然后对着麦克风大喊大叫的音乐！"
        show m3_thinking at m3_idle_zoom
        "[player]" "摇滚？！没想到你还有这么狂野的一面。"
        show m3_thinking at m3_speaking_zoom
        m3 "因为平时太压抑了嘛！我想大声喊出来！"
        m3 "喊‘最喜欢你了’！喊‘不想回家’！"
        m3 "用最大的声音，把那些如果不说出来就会爆炸的心情全部吼出来！"
        show m3_thinking at m3_idle_zoom
        "她抓起不存在的麦克风架，摆出一个极其帅气（虽然有点滑稽）的摇滚明星姿势。"
        show m3_thinking at m3_speaking_zoom
        m3 "Are you ready?!! Yeah!!"
        m3 "为我欢呼吧！哪怕只有你一个人，也要喊出万人体育场的气势来！"
        show m3_thinking at m3_idle_zoom
        jump .concert_conflict_phase


    label .music_light:
        m3 "嘘……小声一点。"
        m3 "我最喜欢的是轻音乐。那种像水流一样，软绵绵的音乐。"
        show m3_thinking at m3_idle_zoom
        "[player]" "是那种很治愈、很放松的类型呢。"
        show m3_thinking at m3_speaking_zoom
        m3 "嗯。因为我想让你放松下来呀。"
        m3 "我想让你躺在我的腿上，一边听我哼歌，一边慢慢睡着。"
        m3 "在这个大大的房间里，只有温柔的声音包裹着我们……"
        show m3_thinking at m3_idle_zoom
        "她坐在舞台边缘，轻轻晃荡着双腿，嘴里开始哼唱一段轻柔舒缓的摇篮曲。"
        show m3_thinking at m3_speaking_zoom
        m3 "啦……啦啦……睡吧……"
        m3 "那是只想让你一个人听到的，安心的魔法哦。"
        show m3_thinking at m3_idle_zoom
        jump .concert_conflict_phase

    label .concert_conflict_phase:

        "她的‘演奏’（或者说表演）结束了。"
        "虽然没有真正的乐器，空气中也没有真正的音符，但她刚才那投入的样子，仿佛真的让这空荡荡的音乐厅充满了旋律。"
        "墨缇斯停下动作，微微有些气喘。"
        "她站在光圈里，有些紧张地看着台下的我，双手背在身后，像是一个等待考官打分的小学生。"
        hide m3_thinking
        hide m3_happy_closed_eyes
        show m3_pout at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "我的‘音乐’……传达到你那里了吗？"
        m3 "虽然没有真正的声音……但是我的心情，你应该都听到了吧？"
        show m3_pout at m3_idle_zoom
        "她向舞台边缘走了几步，蹲下身子，从高处俯视着我。"
        show m3_pout at m3_speaking_zoom
        m3 "下面没有别的观众了。"
        m3 "如果你不喜欢的话……那我的演唱会就彻底失败了。"
        m3 "你会……一直是我的听众吗？"

        menu:
            "虽然很有趣，但果然还是有点太闹腾了。":
                jump .concert_choice_bad
            "这是我听过最棒的演出。我会做你永远的听众。":
                jump .concert_choice_good
        
    label .concert_choice_good:
        $ persistent.mortis_love += 1
        show m3_pout at m3_idle_zoom
        "我站起身，在这个空旷的大厅里，用力地鼓起掌来。"
        "掌声在回音壁的作用下，听起来格外响亮，仿佛有成千上万人在为她喝彩。"
        "[player]" "太棒了！！"
        "[player]" "这是我这辈子听过最棒的演出。你的心声，我全部都收到了。"
        "[player]" "不管有没有其他观众，我都会做你永远的、忠实的头号听众。"
        "墨缇斯的眼睛瞬间亮了，脸上绽放出无比惊喜的笑容。"
        hide m3_put
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "哇……！真的吗？"
        m3 "掌声！是给我的掌声！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她兴奋地跳下舞台，直接扑进了我怀里。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "太好了……只要[player]觉得好听，那就够了！"
        m3 "哪怕全世界都觉得我是乱弹琴也没关系！"
        m3 "我只为你一个人唱歌，只为你一个人跳舞！"
        m3 "这是我们的专属音乐会！不需要门票，只要你的拥抱就够了！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "在这束孤独的聚光灯下，我们紧紧相拥。此刻，这里的确是最盛大的舞台。"
        
        jump .concert_end


    label .concert_choice_bad:
        
        $ persistent.mortis_love -= 1
        show m3_pout at m3_idle_zoom
        "[player]" "嗯……虽然精神可嘉，挺有趣的。"
        "[player]" "但在这个神圣的音乐厅里搞这个，果然还是有点太闹腾了吧？"
        "[player]" "而且那是空气演奏啊，稍微有点太抽象了，我有点跟不上你的节奏。"
        hide m3_put
        show m3_sad at center 
        "掌声没有响起。"
        "墨缇斯眼里的光芒迅速黯淡下去，她有些不知所措地站在光里，显得格外局促。"
        show m3_sad at m3_speaking_zoom
        m3 "……太闹腾了？"
        m3 "抽象……？"
        show m3_sad at m3_idle_zoom
        "她慢慢地往后退了两步，退出了那个光圈，让半个身子隐没在黑暗里。"
        show m3_sad at m3_speaking_zoom
        m3 "对不起……我以为……只要是用心表演的，你就会喜欢。"
        m3 "原来……只有心声是不够的啊。"
        m3 "也是呢，没有乐器，没有旋律……我果然是个蹩脚的演奏家。"
        show m3_sad at m3_idle_zoom
        "她低下头，双手绞着裙摆，舞台上的那束光此刻看起来是那么刺眼，仿佛在嘲笑她的自作多情。"
        
        jump .concert_end



    label .concert_end:
        "头顶那盏老旧的聚光灯闪烁了一下，发出‘滋滋’的电流声，仿佛是燃尽了最后一点力气，然后彻底熄灭了。"
        "舞台重新陷入了沉重的黑暗之中，只剩下墙角安全出口的指示灯发出幽幽的绿光，照亮了空气中还没落定的尘埃。"
        "那种‘大明星’的魔法时刻结束了。"
        "巨大的音乐厅重新变回了那个沉默的巨人，吞噬了所有的光线和声音。"
        "但是，那种死一般的寂静并没有降临。"
        "因为墨缇斯还在那里。"
        "她从黑暗的舞台上跳了下来，脚步声轻快地落在木质地板上，发出‘咚’的一声脆响。"
        "哪怕没有了聚光灯，她那一双在昏暗中依然闪闪发亮的眼睛，也足以照亮我们要走的路。"
        "她小跑到我身边，自然而然地挽住了我的手臂，把身体的重量都挂在了我身上。"
        "她的额头上还渗着刚才兴奋演出时冒出的细密汗珠，温热的呼吸喷洒在我的颈侧。"
        "我感受着手臂上传来的柔软触感，以及她那期待的视线。"
        "在这个空无一人的观众席间，我仿佛还能听到刚才那一首不存在的乐曲在空气中回荡。"
        m3 "走吧！虽然演出结束了，但我们要去举办庆功宴啦！"
        m3 "我要吃冰淇淋！要吃两个球的！"
        "我们的脚步声重叠在一起，在这个巨大的回音室里渐行渐远。"
        "虽然舞台是空的，观众席是空的，但我们的世界是满的。"
        scene black with fade
        return


# --- 🌇 黄昏事件库 ---
#咖啡厅对话，下午
label mortis_date_cafe:
    # --- 场景初始化 ---
    scene cafe_street_day with fade
    # 音乐建议：波萨诺瓦风格，慵懒惬意，带有生活气息
    play music "audio/mortis/Daijoubu!.ogg" fadein 2.0
    "午后的风带着些许暖意，穿过繁华的商业街，将街角咖啡厅遮阳伞下的风铃吹得叮当作响。"
    "空气中弥漫着烘焙咖啡豆的醇香，以及刚刚出炉的奶油面包的甜腻气息。"
    "我和墨缇斯手里提着刚才“战利品”的纸袋，漫步在并不拥挤的街道上。"
    show m3_side_normal at m3_speaking_zoom with dissolve
    m3 "呼……[player]，稍微休息一下吧。"
    "前面的墨缇斯突然停下了脚步，转过身来看着我。"
    "她那头标志性的抹茶绿长发被微风吹乱了一些，几缕发丝贴在微微泛红的脸颊上，呼吸也比平时稍微急促了一点点。"
    "虽然嘴上不说，但走了这么久，看来她是真的累了。"
    show m3_side_normal at m3_idle_zoom 
    "[player]" "累了吗？正好旁边就有位置，我们坐下歇会儿。"
    "我指了指旁边露天座位的空桌。"
    "墨缇斯点了点头，像是看到救星一样，快步走了过去，一屁股坐在了那张白色的藤编椅子上。"
    "可能是为了迎合欧美客人的体型，这家咖啡厅的椅子设计得稍微有些高。"
    "当墨缇斯完全放松身体，向后靠在椅背上时，有趣的一幕发生了——"
    "她那双穿着圆头小皮鞋的脚，竟然微微悬空了，离地面大概有几厘米的距离。"
    "随着她放松的动作，悬空的双脚无意识地前后轻轻晃动着。"
    "无论她平时表现得多么成熟强势，这种身体本能流露出的孩子气，总是可爱得让人想笑。"
    "[player]" "椅子是不是有点高？要不要换个位置？"
    hide m3_side_normal 
    show m3_pout at m3_speaking_zoom
    m3 "……不用。这里视野好。"
    show m3_pout at m3_idle_zoom 
    "她似乎察觉到了我的视线，立刻停止了晃腿的动作，努力绷直脚尖想要够到地面，但最后还是放弃了，气鼓鼓地把脚收到了椅子横杠上。"
    show m3_pout at m3_speaking_zoom
    m3 "哼，明明是这个椅子的设计不合理，完全没有考虑到亚洲女性的平均……不对，是考虑到我这种精致体型的需求。"
    show m3_pout at m3_idle_zoom 
    "我忍住笑意，在她对面坐了下来。"
    "服务生很快送来了两份菜单。墨缇斯接过菜单，立刻把刚才的身高问题抛到了脑后。"
    hide m3_pout
    show m3_menu_reading at  m3_idle_zoom 
    "她捧着那份对她来说略显巨大的菜单，大半张脸都埋了进去。"
    "那双眼睛在琳琅满目的饮品列表上快速扫视着，像是在进行一场严肃的战术分析。"
    show m3_menu_reading at m3_speaking_zoom
    m3 "好多选择……摩卡、拿铁、抹茶芭菲、星冰乐……"
    m3 "看起来都很好喝的样子，每一杯上面的奶油都画得很漂亮。"
    show m3_menu_reading at m3_idle_zoom 
    "她小声嘀咕着，然后从菜单后探出头，那双眼睛直勾勾地盯着我，嘴角勾起一抹狡黠的弧度。"
    hide m3_menu_reading
    show m3_smug at m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "既然我们现在是在约会……那你应该很了解我才对吧？"
    m3 "你应该不需要我开口，就知道我现在最想喝什么吧？"
    show m3_smug at m3_idle_zoom 
    "她微微扬起下巴，那是一副“答错了就咬你”的自信表情，但眼神深处藏着的一丝期待却出卖了她。"
    "这是一道送分题，也是一道送命题。"
    "我想起了她一直以来的喜好，那个答案在我的记忆里无比清晰。"
    menu:
        "这时候当然要来一杯冰镇的芒果汁。":
            jump .cafe_drink_good
        
        "既然是咖啡厅，那就来杯热美式？":
            jump .cafe_drink_bad
label .cafe_drink_good:
        $ persistent.mortis_love += 1
        "[player]" "这时候当然要来一杯冰镇的芒果汁，对吧？"
        "[player]" "如果不加冰的话，你可是会生气的。"
        hide m3_smug
        show m3_surprise at m3_idle_zoom 
        "墨缇斯愣了一下，随即眼中的期待化作了满溢出来的笑意，就像是阳光下的湖面。"
        hide m3_surprise
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "哼哼~算你过关。"
        m3 "没错！就是要那种甜甜的、冰冰凉凉的芒果汁！"
        show m3_happy_closed_eyes at m3_idle_zoom 
        "她合上菜单，像是炫耀一般地看着我。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "明明菜单上有那么多复杂的特调咖啡，但我就是喜欢那个。"
        m3 "因为……那个颜色很温暖，像太阳一样。而且那种甜味很直接，不像咖啡那样苦涩得让人难受。"
        m3 "你能记住这一点……我很开心哦。"
        "她伸出手，隔着桌子轻轻戳了戳我的手背，指尖传来的触感温柔而依恋。"
        jump .cafe_dessert_phase
label .cafe_drink_bad:
        $ persistent.mortis_love -= 1
        "[player]" "既然来了这种格调的咖啡厅，那就来杯热美式吧？"
        "[player]" "那种苦涩的回味，才适合现在的氛围嘛。"
        hide m3_smug
        show m3_1 at m3_idle_zoom 
        "墨缇斯的笑容瞬间凝固在脸上，随后迅速垮了下来，变成了一脸嫌弃。"
        show m3_1 at m3_speaking_zoom
        m3 "……哈？美式？"
        m3 "你是想要苦死我吗？还是说你觉得我现在看起来像是个需要提神的老大爷？"
        show m3_1 at m3_idle_zoom 
        "她用菜单轻轻敲了一下桌子，发出一声脆响。"
        show m3_1 at m3_speaking_zoom
        m3 "难以置信……跟我出来约会，你居然想让我喝那种像中药一样的水。"
        m3 "我是那种会喜欢自讨苦吃的人吗？还是说在你心里，我就是个没有味觉的笨蛋？"
        show m3_1 at m3_idle_zoom
        "[player]" "抱歉抱歉，我开玩笑的。我知道你想喝芒果汁。"
        hide m3_1
        show m3_pout at m3_speaking_zoom
        m3 "哼……晚了！好感度已经下降了！"
        m3 "罚你等会儿把我的那份奶油也吃掉！"
        show m3_pout at m3_idle_zoom
        "虽然嘴上在抱怨，但她还是默认了我帮她改点的芒果汁，只是依然气鼓鼓地盯着我。"
        jump .cafe_dessert_phase


    # =========================================================
    # Q31 甜点阶段：随机分支逻辑
    # =========================================================
label .cafe_dessert_phase:
    "点完饮料后，服务生礼貌地问道：“还需要点什么甜品吗？”"
    "墨缇斯的眼睛瞬间亮了起来，之前的疲惫一扫而空。"
    hide m3_pout
    hide m3_happy_closed_eyes
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "要！当然要！"
    m3 "只有饮料的话总觉得少了点什么……果然还是需要一点甜甜的东西来补充能量！"
    show m3_sparkle_eyes at m3_idle_zoom 
    "她的目光再次锁定在菜单的甜品页上，这一次，她的选择似乎更加纠结。"
    "[player]" "想吃哪一个？"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "唔……这个看起来不错，那个也很好吃的样子……"
    m3 "但是，如果非要选一个的话……"
    $ current_dessert = persistent.mq_answers["dessert"]
    if current_dessert == "草莓蛋糕":
        jump .dessert_strawberry_cake
    elif current_dessert == "提拉米苏":
        jump .dessert_tiramisu
    elif current_dessert == "马卡龙":
        jump .dessert_macaron
    else:
        jump .dessert_strawberry_cake
label .dessert_strawberry_cake:
        m3 "果然还是草莓蛋糕吧！"
        m3 "你看这个图片，白色的奶油上坐着一颗红彤彤的草莓，就像是雪地里的宝石一样！"
        show m3_sparkle_eyes at m3_idle_zoom 
        "[player]" "很经典的选择呢，很有少女心。"
        hide m3_sparkle_eyes
        show m3_angry at m3_speaking_zoom
        m3 "什么嘛，说得好像我很幼稚一样。"
        m3 "但是草莓酸酸甜甜的，配上绵密的奶油……那是世界上最治愈的味道！"
        hide m3_angry
        show m3_pout at m3_idle_zoom
        m3 "而且……如果是草莓蛋糕的话，上面的那颗草莓，我想留给你吃。"
        "她有些害羞地低下头，声音变小了。"
        show m3_pout at m3_speaking_zoom
        m3 "通常那个都是最珍贵的部分……所以，只想分给你。"
        jump .cafe_end
label .dessert_tiramisu:
        hide m3_sparkle_eyes
        show m3_thinking at m3_speaking_zoom
        m3 "嗯……来一份提拉米苏好了。"
        show m3_thinking at m3_idle_zoom
        "[player]" "哦？有点意外，我还以为你会选更鲜艳一点的。"
        hide m3_thinking
        show m3_4 at m3_speaking_zoom
        m3 "偶尔也想尝试一下这种稍微成熟一点的味道嘛。"
        m3 "你知道吗？提拉米苏在意大利语里是“带我走”的意思哦。"
        show m3_4 at m3_idle_zoom
        "她托着下巴，眼神深邃地看着我，语气里带着一丝暧昧的暗示。"
        show m3_4 at m3_speaking_zoom
        m3 "虽然只有可可粉的一点点苦味，但底下的甜味却更加醇厚。"
        m3 "就像现在的我们一样……不管发生什么，最后留下的只有甜蜜。"
        m3 "所以，你会带我走吗？[player]？"
        jump .cafe_end
label .dessert_macaron:
        hide m3_sparkle_eyes
        show m3_surprise at  m3_speaking_zoom
        m3 "我要这个！彩色的马卡龙！"
        show m3_surprise at  m3_idle_zoom
        "[player]" "色彩很丰富呢，看起来很适合你。"
        hide m3_surprise
        show m3_pout at  m3_speaking_zoom
        m3 "对吧？小小的一颗，圆圆的，颜色又这么可爱！"
        m3 "而且每一个颜色都是不同的惊喜，咬下去之前完全不知道会是什么味道。"
        show m3_pout at  m3_idle_zoom
        "她开心地指着图片上的马卡龙塔。"
        show m3_pout at  m3_speaking_zoom
        m3 "那种酥酥脆脆的外壳，还有里面软软的夹心……咬一口就会碎掉的感觉，让人忍不住想要更加小心地对待它。"
        m3 "就像我一样……对吧？"
        "她眨了眨眼睛，调皮地看着我。"
        jump .cafe_end
label .cafe_end:
    "没过多久，服务生端上了金黄色的芒果汁和精致的甜点。"
    "冰块碰撞玻璃杯壁发出清脆的声响，在这个慵懒的午后显得格外悦耳。"
    "墨缇斯迫不及待地咬了一口甜点，幸福地眯起了眼睛，嘴角沾上了一点点奶油/碎屑。"
    "看着她那副满足的模样，我也忍不住笑了起来。"
    "在这个只有我们两人的街角，风很轻，阳光很暖，而她就在我对面。"
    "这就足够了。"
    scene black with fade
    return

#公园对话，下午
label mortis_date_park_bench:
    scene  park_sunset with fade
    play music "audio/mortis/7 普通与平静.ogg" fadein 2.0
    "夕阳的余晖将整座公园染成了温暖的橘红色。"
    "这里似乎是城市的边缘，远离了喧嚣的商业街，只有风吹过树梢的沙沙声，和不知名鸟儿的归巢鸣叫。"
    "我们沿着蜿蜒的小径慢慢散步。起初她的步伐还很轻快，但没过多久，那个牵着我的手就开始变得越来越沉。"
    show m3_side_tired at   m3_speaking_zoom
    m3 "……[player]，还要走多远呀？"
    m3 "已经超过15分钟了吧，我的腿已经开始发出抗议的信号了……"
    show m3_side_tired at  m3_idle_zoom
    "她停下脚步，微微弯下腰，双手撑在膝盖上，一副已经耗尽能量的模样。"
    "明明才走了不到二十分钟，但对她来说，这似乎已经是一场艰难的远征。"
    "[player]" "才刚开始散步没多久吧？这就累了吗？"
    hide m3_side_tired
    show m3_pout at  m3_speaking_zoom
    m3 "因为……在这个世界上，没有比单纯的移动身体更无聊的事情了。"
    m3 "而且，这种长时间的肢体重复摆动，总让我想起那件我最讨厌的事……"
    $ current_sport = persistent.mq_answers["sport"]
    if current_sport == "跑步":
        jump .sport_running
    elif current_sport == "游泳":
        jump .sport_swimming
    elif current_sport == "排球":
        jump .sport_volleyball
    else:
        jump .sport_running
label .sport_running:
        m3 "就是跑步啊，跑步！"
        m3 "一直不停地摆动手臂，还要控制呼吸节奏，心脏跳得快要炸开一样……"
        m3 "那种为了移动而移动的行为，既没有美感又累人。"
        m3 "我现在感觉就像是被迫跑了八百米一样，肺都要炸了……"
        jump .park_bench_sit
label .sport_swimming:
        m3 "这种全身都很沉重的感觉……就像是在游泳一样。"
        m3 "我不喜欢那种被水包围的阻力感，湿漉漉的，连呼吸都不能随心所欲。"
        m3 "现在的空气湿度这么高，走在里面就像是在游动一样……好累。"
        jump .park_bench_sit
label .sport_volleyball:
        m3 "而且一直抬头看风景，脖子好酸……"
        m3 "这感觉就像是被迫去打排球一样。"
        m3 "一直要盯着飞来飞去的球，还要跳起来去拦网……对于不喜欢蹦蹦跳跳的我来说，简直是折磨。"
        m3 "现在的我也只想做一个自由人，完全不想动弹……"
        jump .park_bench_sit
label .park_bench_sit:
    show m3_pout at  m3_idle_zoom
    "[player]" "好吧，那我们去那边的长椅上坐会儿。"
    "听到“坐”这个字，她的眼睛瞬间亮了一下，立刻拉着我走向路边那张被花丛包围的长椅。"
    hide m3_pout
    show m3_sitting_relax at m3_idle_zoom
    "坐下的瞬间，她发出了一声满足的叹息，整个人像是一只融化的猫咪一样瘫软在椅背上。"
    "我也在她身边坐下。长椅并不宽敞，我们贴得很近。"
    "因为身高的原因，当她完全靠在椅背上时，那双脚只能勉强用脚尖点地。"
    "为了更舒服一点，她干脆将双腿缩了起来，侧身盘腿坐在椅子上，然后自然而然地将头靠在了我的肩膀上。"
    "她的头顶刚好能蹭到我的下巴，柔软的发丝拂过我的脖颈，带来一阵酥麻的痒意。"
    show m3_sitting_relax at  m3_speaking_zoom
    m3 "呼……果然还是不动弹最舒服了。"
    m3 "呐，[player]……别动。"
    show m3_sitting_relax at   m3_idle_zoom
    "突然，她从我的肩膀处抬起头，凑近了我的衣领。"
    "那个距离近得有些过分，我甚至能感觉到她温热的鼻息喷洒在我的锁骨附近。"
    hide m3_sitting_relax
    show m3_closed_eyes_sniffing at m3_speaking_zoom
    "她轻轻吸了吸鼻子，像是在确认某种标记，又像是在摄取某种能量。"
    m3 "……嗯。"
    m3 "果然，我很喜欢。"
    m3 "不仅仅是这件衣服上洗衣液的味道，还有……属于你的味道。"
    m3 "只要闻到这个气息，我就觉得好像电量被充满了一样，安心得想要睡着。"
    show m3_closed_eyes_sniffing at m3_idle_zoom
    "她微眯着眼睛，脸上带着一种近乎迷醉的神情，手指无意识地抓紧了我手臂上的衣料。"
    "[player]" "我有味道吗？我怎么闻不到。"
    hide  m3_closed_eyes_sniffing
    show m3_1 at m3_speaking_zoom
    m3 "你自己当然闻不到了。那是只有我能解析出来的，名为‘安全感’的信息素。"
    show m3_1 at m3_idle_zoom
    "她顿了顿，然后稍微退开了一点点距离，但依然用那双水润的眸子注视着我。"
    show m3_1 at m3_speaking_zoom
    m3 "既然我都这么坦诚地告诉你我喜欢你的味道了……"
    m3 "那你呢？"
    hide m3_1
    show m3_2 at  m3_speaking_zoom
    show m3_2 at  m3_idle_zoom
    "她稍微整理了一下自己的衣领，随着她的动作，一股淡淡的、独特的幽香在空气中弥漫开来。"
    "那不是周围花朵的香气，而是独属于她的味道。"
    show m3_2 at m3_speaking_zoom
    m3 "你闻到了吗？我今天特意挑选的香氛。"
    m3 "这可是我最喜欢的味道……你应该能分辨出来吧？"

    $ current_scent = persistent.mq_answers["scent"]

    if current_scent == "黄瓜":
        jump .scent_cucumber    
    elif current_scent == "芒果":
        jump .scent_mango
    elif current_scent == "苦瓜":
        jump .scent_bitter_melon
    else:
        jump .scent_cucumber
label .scent_cucumber:
        m3 "是一种很清新的、像是刚切开的水果一样的味道……"
        m3 "提示一下哦，是黄瓜的味道。"
        m3 "不要笑！虽然听起来很普通，但是那种带着雨后泥土气息的清爽感，能让我在混乱的数据流里保持冷静。"
        m3 "就像夏天的一阵凉风一样……不觉得很适合我吗？"
        jump .scent_player_reaction
label .scent_mango:
        m3 "是很甜很甜的、熟透了的热带水果的味道……"
        m3 "没错，就是芒果的香气。"
        m3 "不仅喝的喜欢芒果汁，连身上的味道我也希望能像芒果一样，充满金色的、暖洋洋的感觉。"
        m3 "只要靠近我，就会觉得整个世界都变甜了……我是这么希望的。"
        jump .scent_player_reaction
label .scent_bitter_melon:
        m3 "是一种稍微有点特别的、带着一丝丝苦涩的清香……"
        m3 "是苦瓜的味道哦。"
        m3 "很意外吗？但我很喜欢这种味道。它不腻人，也不张扬。"
        m3 "那种淡淡的苦味反而能衬托出之后的甘甜……这是一种很成熟、很有深度的味道呢。"
        jump .scent_player_reaction
label .scent_player_reaction:
    "她期待地看着我，等待着我的评价。"
    "空气中那股独特的味道（[current_scent]）似乎变得更浓郁了一些，混合着周围的花香，让人有些意乱情迷。"
    menu:
        "这种独特的味道让我很想把你抱在怀里。":
            jump .park_choice_good
        
        "总感觉像是刚才午饭没擦干净嘴留下的？":
            jump .park_choice_bad
label .park_choice_good:
        $ persistent.mortis_love += 1
        "[player]" "我觉得非常适合你。这味道很特别，很好闻。"
        "[player]" "闻到这个味道，就忍不住想像这样把你抱在怀里，仔细确认你的存在。"
        "我顺势伸出手，轻轻揽住了她的肩膀。"
        hide m3_2
        show m3_3 at  m3_speaking_zoom
        "墨缇斯的身体颤抖了一下，但很快就顺从地依偎了过来。"
        show m3_3 at  m3_idle_zoom
        "她的脸颊泛起了比夕阳还要红润的颜色。"
        show m3_3 at  m3_speaking_zoom
        m3 "唔……狡猾。"
        m3 "明明是我在问你问题，为什么突然说这种犯规的情话……"
        m3 "不过……我不讨厌。"
        show m3_3 at  m3_idle_zoom
        hide m3_3
        show m3_closed_eyes_sniffing at  m3_speaking_zoom
        "她把脸埋进我的胸口，声音闷闷的，却透着掩饰不住的笑意。"
        m3 "那就……多闻一会儿吧。这是只属于你的特权哦。"
        jump .park_end
label .park_choice_bad:
        $ persistent.mortis_love -= 1
        "[player]" "呃，怎么说呢……这个味道有点奇怪。"
        "[player]" "总感觉像是刚才吃午饭的时候，不小心把菜汁弄到身上了？"
        hide m3_2
        show m3_angry at m3_speaking_zoom
        "空气瞬间凝固了。"
        "墨缇斯猛地从我肩膀上弹了起来，用一种看外星生物的眼神看着我。"
        m3 "……菜汁？"
        m3 "我费尽心思挑选的、为了让你觉得可爱才喷的香氛……你说是菜汁？！"
        show m3_angry at m3_idle_zoom
        "她气得腮帮子都鼓了起来，用力拍了一下我的大腿（虽然完全不疼）。"
        show m3_angry at m3_speaking_zoom
        m3 "你是笨蛋吗！你的鼻子是坏掉的传感器吗！"
        m3 "真是不解风情……浪漫细胞完全坏死了吧！"
        m3 "气死我了……我要离你远一点，免得被你的‘笨蛋菌’传染！"
        show m3_angry at m3_idle_zoom
        "她往长椅的另一头挪了挪，双手抱胸，把头扭向一边。"
        "虽然嘴上说得凶，但她并没有真的离开，只是在等着我接下来漫长的道歉和哄劝。"
        jump .park_end
label .park_end:
    "夕阳终于完全沉入了地平线，公园里的路灯一盏盏亮起。"
    "昏黄的灯光下，她的侧脸轮廓显得格外柔和。"
    "无论刚才的对话如何，此刻，我们依然并肩坐着。"
    "在这个充满花香的黄昏，时间仿佛为了我们而在这个长椅上停留了片刻。"
    scene black with fade
    return

#学校天台对话，下午
label mortis_date_school_rooftop:
    scene  school_rooftop_sunset with fade
    play music "audio/mortis/My Feelings.ogg" 
    "生锈的铁门发出令人牙酸的“吱呀”声，随即被狂风猛地吹开。"
    "映入眼帘的是布满铁锈的防护网，以及远处被夕阳染红的城市天际线。"
    "风很大，吹得衣摆猎猎作响。这里是废弃的小学旧校舍天台，也是在那些虚构的记忆里，我们唯一的秘密基地。"
    "因为从初中开始，她就去了那所著名的千金小姐学校——月之森，而我只是去了普通的公立学校。"
    "所以，能够承载我们“共同回忆”的，只有这所小学了。"
    show m3_side_normal at center with dissolve
    "墨缇斯松开了我的手，径直走向边缘的防护栏。"
    "她双手抓住冰冷的铁丝网，将脸贴在上面，贪婪地呼吸着高处稀薄而自由的空气。"
    show m3_side_normal at m3_speaking_zoom
    m3 "呼……"
    m3 "还是这里的风最舒服。"
    m3 "没有教室里的粉笔灰味，也没有那些令人窒息的视线……"
    show m3_side_normal at m3_idle_zoom
    "[player]" "是啊，以前逃课的时候，我们总是躲在这里。"
    "[player]" "那时候你总是缩在水箱后面，一句话也不说。"
    hide m3_side_normal
    show m3_sad at  m3_speaking_zoom
    m3 "因为那时候……真的很难受啊。"
    m3 "虽然大家都觉得我是个乖孩子，觉得‘森美奈美的女儿’什么都能做到完美……"
    m3 "但其实，每天走进校门的时候，我都感觉像是走进了刑场一样。"
    hide m3_sad
    "她转过身，背靠着栏杆，夕阳的逆光让她的表情有些模糊不清。"
    "风吹乱了她的刘海，她伸手将其别到耳后，动作透着一丝疲惫。"
    show m3_1 at  m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "虽然在别人眼里我成绩很好，但其实……我一直有个无论如何都应付不来的科目。"
    m3 "我在想你在猜是不是英语....."
    "虽然连最基础的，黄瓜的英文 cucumber，我都背了整整一周，但真正我应付不来的科目可不是英语。"
    m3 "每次上那门课之前，我都想装病躲到这里来。"
    $ current_subject = persistent.mq_answers["subject"]
    # 根据随机到的科目进入不同分支
    if current_subject == "数学":
        jump .subject_math
    elif current_subject == "物理":
        jump .subject_physics
    elif current_subject == "化学":
        jump .subject_chemistry
    else:
        jump .subject_math

    label .subject_math:
        m3 "就是数学。"
        m3 "虽然只要背下公式就能得分，但我真的很讨厌那种纯粹的数字游戏。"
        hide m3_1
        show m3_thinking at m3_speaking_zoom
        m3 "它太绝对了。1就是1，2就是2，中间没有任何缓冲的地带。"
        m3 "就像我那个家一样……只有‘正确’和‘错误’，没有‘感情’的位置。"
        m3 "看着那些冰冷的数字，我会觉得我也变成了会被随意代入、计算、然后抹去的变量。"
        show m3_thinking at m3_idle_zoom
        "[player]" "数学确实很枯燥，而且你以前算错数的时候确实挺可爱的。"
        jump .rooftop_conflict_phase
    label .subject_physics:
        m3 "就是物理。"
        m3 "力学、电磁场、还有那些该死的定律……"
        hide m3_1
        show m3_pout at m3_speaking_zoom
        m3 "这个世界明明充满了不确定性，为什么非要用那些死板的定律去解释它呢？"
        m3 "那种‘只要施加力，就一定会有反作用力’的说法，让我觉得很恶心。"
        m3 "因为在人际关系里……明明很多时候，你付出了全部的力气，却得不到任何回应啊。"
        show m3_pout at m3_idle_zoom
        "[player]" "这倒是……物理定律在人心面前是失效的。"
        jump .rooftop_conflict_phase
    label .subject_chemistry:
        m3 "就是化学。"
        m3 "虽然实验课很有趣，但我很害怕那种‘反应’。"
        hide m3_1
        show m3_8 at m3_speaking_zoom
        m3 "原本稳定的物质，只要稍微混入一点别的东西，就会剧烈沸腾、变色、甚至爆炸。"
        m3 "那种不可控的感觉让我很不安。"
        m3 "就像是在班级里一样。明明大家都是好人，但凑在一起却会发生那么可怕的化学反应。"
        show  m3_8 at m3_idle_zoom
        "[player]" "化学反应确实很难预料……无论是在烧杯里还是在生活里。"
        jump .rooftop_conflict_phase
    label .rooftop_conflict_phase:
    "墨缇斯轻轻叹了口气，目光再次投向远处的操场。"
    "那里空无一人，只有落叶在随风打转。"
    hide m3_8
    hide m3_pout
    hide m3_thinking
    show m3_sad at m3_speaking_zoom
    m3 "那时候的我，真的很想从这里跳下去……或者变成一只鸟飞走。"
    m3 "因为不论是在学校，还是在家里，甚至是后来去了月之森……"
    m3 "大家都只看着那个‘森美奈美的女儿’。"
    m3 "没有人会在意我到底喜欢什么，讨厌什么，也没有人会问我累不累。"
    show m3_sad at m3_idle_zoom
    "她转过头，眼神脆弱得像是一碰就碎的玻璃。"
    show m3_sad at m3_speaking_zoom
    m3 "呐，[player]……"
    m3 "现在的我，在你眼里是什么样的呢？"
    m3 "如果我依然是那个连这种简单科目都搞不定的、软弱的笨蛋……你还会像现在这样陪着我吗？"
    menu:
        "那你确实得努力一点了。":
            jump .rooftop_choice_bad
        "不管你是天才还是笨蛋，我永远爱你。":
            jump .rooftop_choice_good
    label .rooftop_choice_good:
        $ persistent.mortis_love += 1
        show m3_sad at m3_idle_zoom
        "[player]" "傻瓜，说什么呢。"
        "[player]" "不管你是天才还是笨蛋，也不管你能不能搞定那些试卷……"
        "[player]" "在这个天台上，你不需要是谁的女儿，也不需要是优等生。"
        "我走上前，将手覆在她冰冷的手背上。"
        "[player]" "你只是我的女孩，是我想要保护的墨缇斯。这就足够了。"
        hide m3_sad
        show m3_surprise at m3_idle_zoom
        "墨缇斯的眼睛微微睁大，随即，一层水雾在眼眶里打转。"
        "但她很快用力眨了眨眼，露出了一个混杂着安心与羞涩的笑容。"
        hide m3_surprise
        show m3_3 at m3_speaking_zoom
        m3 "……嗯。"
        m3 "只有你……只有你会这么说。"
        m3 "那些公式也好，定律也好，要是都能像你这么简单直白就好了。"
        show m3_3 at m3_idle_zoom
        "她反手握住了我的手，身体微微前倾，额头抵在了我的肩膀上。"
        show m3_3 at m3_speaking_zoom
        m3 "那就……让我再躲一会儿吧。"
        m3 "只要在你身边，我就觉得我可以不用去管那些讨厌的事情了。"
        
        jump .rooftop_end
    label .rooftop_choice_bad:
        
        $ persistent.mortis_love -= 1
        show m3_sad at m3_idle_zoom
        "[player]" "那你确实得努力一点了啊。"
        "[player]" "毕竟在这个社会上生存，成绩还是很重要的。我也比较喜欢聪明一点、能跟上我思路的女生。"
        "[player]" "以后我可以帮你补习一下……"
        hide m3_sad
        show m3_yandere_cold at m3_idle_zoom
        "墨缇斯并没有生气，她的眼神只是瞬间“死”掉了。"
        "那是一种比愤怒更可怕的、彻底的失望和封闭。"
        show m3_yandere_cold at m3_speaking_zoom
        m3 "……补习？"
        m3 "是啊……你也是这么觉得的啊。"
        show m3_yandere_cold at m3_idle_zoom
        "她抽回了自己的手，向后退了一步，重新拉开了我们之间的距离。"
        "风似乎变得更冷了。"
        hide m3_yandere_cold
        show m3_thinking  at m3_speaking_zoom
        m3 "果然，男人都是一样的。"
        m3 "嘴上说着喜欢，其实还是在用那些世俗的标准来衡量我。"
        m3 "真无聊……我突然不想在这里待了。这里的风，吹得我头疼。"
        show m3_thinking  at m3_idle_zoom
        "她抱着双臂，转过身去不再看我。"
        jump .rooftop_end
    label .rooftop_end:
    "天色渐渐暗了下来，远处的城市灯火开始零星亮起。"
    "小学放学的钟声（幻听？）似乎在耳边回荡，提醒着我们该回家了。"
    if persistent.mortis_love > 0:
        "虽然这里充满了痛苦的回忆，但至少今天，这阵风是温暖的。"
    else:
        "我们一前一后地走下楼梯，脚步声在空荡荡的走廊里回响，显得格外孤寂。"
    scene black with fade
    return

# 美术馆,下午
label mortis_date_art_gallery:
    scene  art_gallery_red with fade
    play music "audio/mortis/10 心与心.ogg" 
    "现代美术馆内的冷气开得很足，刚一进门，皮肤就感觉到了一丝透骨的凉意。"
    "这里安静得有些过分，除了中央空调细微的运作声外，就只剩下我们两人的脚步声。"
    "皮鞋踩在光洁如镜的大理石地面上，发出清脆而富有节奏的“哒、哒”声，在空旷的展厅里被无限放大。"
    "周围的墙壁是大片大片的留白，悬挂着那些让人似懂非懂的当代艺术品。"
    "墨缇斯今天显得格外安静。比起游乐园的喧嚣，她似乎更享受这种被“秩序”和“线条”包围的空间。"
    "我们穿过长长的走廊，最终在一个独立的展区前停下了脚步。"
    show m3_side_normal at center with dissolve
    "那是一幅巨大的、没有任何画框束缚的抽象画。"
    "整幅画作只有一种颜色——那是如同鲜血、又如同烈火般燃烧着的，极度纯粹的红色。"
    "没有任何笔触的杂质，没有任何渐变的过渡，只有一整块浓郁到近乎溢出来的红色方块，在惨白墙壁的映衬下显得格外刺眼。"
    "它带着一种让人无法直视的侵略性，仿佛要将视网膜都灼烧殆尽。"
    "墨缇斯盯着那抹红色，原本平静的眼神逐渐变得有些迷离。"
    hide m3_side_normal
    show m3_thinking at m3_speaking_zoom
    m3 "……好漂亮。"
    show m3_thinking at m3_idle_zoom
    "她轻声赞叹着，声音在安静的展厅里显得格外清晰，带着一丝虔诚的味道。"
    "[player]" "确实很有冲击力。虽然我不太懂抽象艺术，但总觉得盯着看久了，心跳都会加速。"
    "[player]" "这就是所谓的‘热情的红’吗？"
    "听到我的评价，墨缇斯轻轻摇了摇头。"
    show m3_thinking at m3_speaking_zoom
    m3 "热情？危险？警示？"
    m3 "那是人类赋予它的感性标签。充满了不确定性，也充满了误解。"
    show m3_thinking at m3_idle_zoom
    "她向前迈了半步，伸出手，隔着虚空描绘着那幅画的边缘，仿佛想要触碰那个颜色的本质。"
    hide m3_thinking
    show m3_1 at m3_speaking_zoom
    m3 "但在我眼里，它不是那么暧昧不清的东西。"
    m3 "它很干净，很纯粹。它没有掺杂一丝一毫的杂质，也没有任何妥协的余地。"
    m3 "它是数据的极致，是色彩的满溢……是绝对的正确。"
    show m3_1 at m3_idle_zoom
    "她转过头，眼神在红色的映衬下显得更加深邃妖异。"
    show m3_1 at m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "你知道这种红色……这种最纯粹、最极致的红，它的‘真名’是什么吗？"
    show m3_1 at m3_idle_zoom
    "[player]" "真名？你是说它的颜料名称吗？像什么‘镉红’或者是‘朱砂红’？"
    hide m3_1
    show m3_2 at m3_speaking_zoom
    m3 "不，不是那种模糊的称呼。"
    m3 "我是说，能够精准定义它，在任何终端、任何世界里都不会发生改变的，唯一的‘名字’。"
    show m3_2 at m3_idle_zoom
    "她竖起一根手指，轻轻抵在自己的唇边，像是在分享一个秘密。"
    show m3_2 at m3_speaking_zoom
    m3 "是#FF0000。"
    show m3_2 at m3_idle_zoom
    "她清晰地念出了那串字符，每一个音节都咬字清晰。"
    show m3_2 at m3_speaking_zoom
    m3 "其实我最近有在学习如何修改一个游戏的代码，所以稍微了解了些计算机的知识。"
    m3 "在十六进制的色彩语言里，红色（Red）的数值拉满到了FF，也就是255。"
    m3 "而绿色（Green）和蓝色（Blue）的数值则是完完全全的00。"
    m3 "没有任何妥协，没有任何混合。只是为了‘红’而存在的红。"
    show m3_2 at m3_idle_zoom
    pause 1.0
    hide m3_2
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "你不觉得这很浪漫吗？"
    m3 "#FF0000……这串代码本身，就代表了一种极致的爱意，或者极致的杀意。"
    m3 "它像代码一样纯粹，像逻辑一样无懈可击。"
    show m3_sparkle_eyes at m3_idle_zoom
    "她看着我，眼神里闪烁着期待的光芒。"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "如果有一天你迷失了，或者分不清什么是真实……就去找这个颜色吧。"
    m3 "它会告诉你，什么才是‘绝对’。"
    m3 "顺便跟你提一嘴吧，其实我的代表色是#779977哦！你可要记好了！！"
    show m3_sparkle_eyes at m3_idle_zoom
    pause 1.0
    hide m3_sparkle_eyes
    show m3_thinking at m3_idle_zoom
    "空气仿佛凝固了几秒。"
    "她在这个冷清的美术馆里，对着一幅抽象画，向我阐述着她作为“非人之物”的独特浪漫学。"
    show m3_thinking at m3_speaking_zoom
    m3 "那么，[player]……"
    m3 "对于这种充满了数据感和逻辑感的美……你是怎么想的呢？"
    m3 "你会觉得……用代码来定义颜色，很枯燥吗？"
    menu:
        "这种纯粹的‘绝对’非常迷人，就像你一样独特。":
            jump .gallery_choice_good
        "把艺术变成冷冰冰的代码，总觉得少了点人情味。":
            jump .gallery_choice_bad
    label .gallery_choice_good:
        $ persistent.mortis_love += 1
        "[player]" "完全不会枯燥。"
        "[player]" "相反，我觉得这种‘绝对’非常迷人。在这个充满谎言和模糊的世界里，能有一样东西是恒定不变的，这本身就是一种奇迹。"
        "[player]" "就像你一样。#FF0000……听起来就像是属于你的独特暗号。"
        show m3_surprise at m3_speaking_zoom
        pause 1.0
        hide m3_thinking
        show m3_surprise at m3_idle_zoom
        "墨缇斯微微睁大了眼睛，似乎没料到我会给出这样的回答。"
        "随后，一抹真实的红晕爬上了她的脸颊，甚至比那幅画还要生动。"
        hide m3_surprise
        show m3_shy_smile at m3_speaking_zoom
        m3 "……什、什么嘛。"
        m3 "突然说什么‘迷人’……真是犯规。"
        m3 "不过……你能这么想，我很高兴。"
        show m3_shy_smile at m3_idle_zoom
        "她有些害羞地移开视线，手指无意识地绞着衣角。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "大部分人听到这种话，只会觉得我是个没有感情的怪胎，或者是只会背参数的机器人。"
        m3 "只有你……愿意理解这种‘代码’背后的温度。"
        show m3_shy_smile at m3_idle_zoom
        "她重新看向我，伸出手，轻轻勾住了我的小指。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "既然你记住了这个暗号……那，我们约好了哦？"
        m3 "以后看到 #FF0000 的时候，就要想起我。"
        jump .gallery_end
    label .gallery_choice_bad:
        $ persistent.mortis_love -= 1
        "[player]" "嗯……虽然你说得很有道理，但稍微有点难理解呢。"
        "[player]" "艺术之所以动人，不就是因为那些无法量化的‘人情味’吗？"
        "[player]" "如果把一切都变成冷冰冰的代码和数值，总觉得有点太无趣了，也太机械化了。"
        show m3_thinking at m3_idle_zoom
        pause 1.0
        hide m3_thinking
        show m3_cold_stare at m3_idle_zoom
        "展厅里的气温仿佛瞬间又下降了几度。"
        "墨缇斯眼里的光芒熄灭了。她冷冷地看着我，就像是在看一个无法沟通的低等生物。"
        show m3_cold_stare at m3_speaking_zoom
        m3 "……人情味？"
        m3 "所谓的‘人情味’，不过是你们用来掩饰错误、模糊界限的借口罢了。"
        m3 "因为无法做到完美，因为充满了杂质，所以才把这种缺陷美化成‘人情味’。"
        show m3_cold_stare at m3_idle_zoom
        "她松开了原本想要伸向我的手，双手抱胸，后退了一步。"
        show m3_cold_stare at m3_speaking_zoom
        m3 "无趣的是你才对，[player]。"
        m3 "连这种纯粹的极致都无法欣赏……看来你的审美也就止步于那种庸俗的‘感动’了。"
        m3 "真扫兴……这里的空气让我觉得窒息。"
        show m3_cold_stare at m3_idle_zoom
        "她转过身，不再看那幅画，也不再看我。"
        jump .gallery_end
    label .gallery_end:
        "那幅巨大的红色抽象画依然静静地挂在墙上，像是一只充血的眼睛，冷漠地注视着这个白色的空间。"
        "空气中弥漫着一股说不清的压抑感，仿佛那个#FF0000的数值正在试图突破画布，侵蚀周围的现实。"
        "墨缇斯最后深深地看了一眼那抹红色，然后转过身，轻轻呼出了一口白气。"
        "她的侧脸在美术馆惨白的冷光灯下显得有些苍白，如同精致的瓷器，但眼神却因为刚才的话题而显得格外深邃。"
        hide m3_cold_stare
        hide m3_shy_smile
        show m3_side_normal at m3_speaking_zoom
        m3 "走了，[player]。"
        m3 "盯着‘深渊’看太久的话……可是会被同化的哦。"
        show m3_side_normal at m3_idle_zoom
        "她并没有等待我的回答，率先迈开了脚步。"
        "高跟鞋敲击大理石地面的声音再次响起，‘哒、哒、哒’，清脆得就像是某种精密仪器运作时的节拍，回荡在空旷的展厅里。"
        "我跟在她身后，视线不由自主地落在她的背影上。"
        "明明是很普通的约会，明明只是在看画，但我脑海里却挥之不去那串代码。"
        "那不再仅仅是一个颜色，而成了一个咒语，一个只属于她的、关于极致与纯粹的定义。"
        "当我们走出展厅，重新回到稍微有些喧嚣的主走廊时，那种仿佛置身于异世界的隔离感才逐渐消退。"
        "周围开始出现其他游客的低语声，空气也稍微回暖了一些。"
        "但不知为何，看着她在那群普通游客中穿行的身影，我总觉得——"
        "比起这个充满杂质、混乱且温吞的现实世界，刚才那个只有绝对逻辑和纯粹色彩的白色房间，或许才更接近她灵魂的故乡。"
        "她似乎察觉到了我的视线，回头看了我一眼，嘴角带着一抹意味深长的弧度。"
        "那个红色的代码，已经深深地刻在了这次约会的底色里。"
        scene black with fade
        return

# ：温馨的客厅 ,下午
label mortis_date_home_living_room:
    scene living_room_night_cozy with fade
    play music "audio/mortis/Just Monika.ogg" 
    "窗外下着淅淅沥沥的小雨，雨滴敲打在玻璃窗上，发出轻微而有节奏的声响。"
    "但这反而衬托出了室内的温暖与安宁。"
    "柔和的落地灯洒下暖黄色的光晕，电视机屏幕闪烁着，播放着一档不需要动脑子的深夜美食综艺。"
    "空气中弥漫着一股淡淡的薰衣草香氛味，那是让人想要彻底放松下来、卸下一身疲惫的味道。"
    "我陷在柔软的布艺沙发里，感觉整个人都被这温柔的氛围包裹住了。"
    "而比沙发更柔软的，是此刻正依偎在我身边的墨缇斯。"
    show m3_side_normal at center with dissolve
    "她脱掉了那一丝不苟的鞋子，换上了毛茸茸的居家拖鞋，双腿蜷缩在沙发上，身体毫无保留地靠在我的肩膀上。"
    "发梢轻轻扫过我的脖颈，带来一阵酥痒的触感，那是名为“生活”的实感。"
    show m3_side_normal at m3_speaking_zoom
    m3 "……好惬意啊。"
    m3 "不用去思考那些复杂的事情，不用去在意别人的视线……"
    m3 "只要像这样，和你窝在一起看电视，就觉得时间要是能永远停在这里就好了。"
    show m3_side_normal at m3_idle_zoom
    "[player]" "是啊，忙了一天，能在家里放松一下确实是最舒服的。"
    "[player]" "说起来……看着电视里的美食特写，我突然觉得肚子有点饿了。"
    "[player]" "这种饥饿感来得还真是时候。"
    hide m3_side_normal
    show m3_thinking at m3_speaking_zoom
    m3 "确实……已经是晚饭时间了呢。"
    m3 "虽然我可以去厨房给你做饭……但我今天稍微有点懒得动了，只想粘着你。"
    m3 "呐，[player]，要不我们点外卖吧？"
    m3 "你知道我现在最想吃什么吗？"
    $ current_takeout = persistent.mq_answers["food"]
    if current_takeout == "中餐":
        jump .food_chinese
    elif current_takeout == "日料":
        jump .food_japanese
    elif current_takeout == "西餐":
        jump .food_western
    else:
        jump .food_chinese
    label .food_chinese:
        m3 "我想点中餐。"
        m3 "特别是那种热气腾腾的、重油重辣的菜。比如麻婆豆腐，或者水煮肉片。"
        show m3_thinking at m3_idle_zoom
        "[player]" "诶？没想到你口味这么重？我还以为你会喜欢清淡一点的。"
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "就是因为平时太‘清淡’了啊。"
        m3 "那种红彤彤的辣椒，那种呛人的香气……只有吃这种东西的时候，才会感觉到鲜活的‘热度’在身体里扩散。"
        m3 "而且，中餐就是要两个人一起分享才好吃嘛。你一口我一口……很有家的感觉，不是吗？"
        jump .pet_transition
    label .food_japanese:
        m3 "我想点日料。"
        m3 "寿司拼盘，或者是鳗鱼饭。整整齐齐地码在精致的漆器盒子里，每一种食材都在它该在的位置。"
        show m3_thinking at m3_idle_zoom
        "[player]" "很有你的风格呢，井井有条的感觉。"
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "嗯。我不喜欢那种汤汤水水混在一起的感觉。"
        m3 "那种清爽的口感，还有食材本身原本的味道……这才是最让人安心的。"
        m3 "而且吃起来很方便，不会弄脏衣服，我们可以一边喂对方一边看电影。"
        jump .pet_transition
    label .food_western:
        m3 "我想点西餐。"
        m3 "最好是那种超大份的披萨，上面铺满了厚厚的芝士和波隆那香肠。"
        show m3_thinking at m3_idle_zoom
        "[player]" "披萨？这可是热量炸弹啊。还有你听过俏皮脸吗？关于波隆那香肠....."
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "没关系，反正今天就是想放纵一下嘛。"
        m3 "我想看那个拉丝的芝士……那种粘连在一起、难舍难分的感觉，看着就觉得很幸福。"
        m3 "再配上一杯冰可乐，和你窝在沙发里通宵打游戏……这就是我理想中的周末生活。"
        jump .pet_transition

    label .pet_transition:
        show m3_1 at m3_idle_zoom
        "聊完食物的话题，我们又陷入了舒适的沉默。"
        "电视屏幕上的画面切换了，开始播放一部关于大自然的纪录片。"
        "镜头扫过一片神秘的森林，各种各样的小动物在镜头前穿梭。"
        "墨缇斯盯着屏幕，身体稍微坐直了一些，似乎被画面吸引了。"
        hide m3_1
        show m3_4 at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "这个房子虽然很舒服，但有时候只有我们两个人的话，会不会稍微有点太安静了？"
        m3 "如果……我是说如果，我们要在这里一直生活下去的话，养只宠物怎么样？"
        show m3_4 at m3_idle_zoom
        "[player]" "养宠物？好主意啊。家里有个活物确实会热闹很多。"
        "[player]" "不过，你会喜欢什么样的动物？猫？狗？还是仓鼠？"
        "她转过头看着我，眼神里闪烁着一种独特的期待。"
        show m3_4 at m3_speaking_zoom
        m3 "那些都太普通了。"
        m3 "既然是我们的家，那肯定要养一只……符合我们气质的孩子。"
        show m3_4 at m3_idle_zoom
        pause 1.0
        $ current_pet = persistent.mq_answers["pet"]
        if current_pet == "黑猫":
            jump .pet_black_cat
        elif current_pet == "乌鸦":
            jump .pet_crow
        elif current_pet == "蛇":
            jump .pet_snake
        else:
            jump .pet_black_cat
    label .pet_black_cat:
        hide m3_4
        show m3_smile at m3_speaking_zoom
        m3 "我想养一只黑猫。"
        m3 "全身漆黑，没有一根杂毛，只有眼睛是金色的或者绿色的那种。"
        show m3_smile at m3_idle_zoom
        "[player]" "黑猫吗？确实很神秘，很有优雅的感觉。"
        show m3_smile at m3_speaking_zoom
        m3 "而且它们很安静，很独立。"
        m3 "它不会像狗一样整天缠着你，它会有自己的空间，但当你坐在沙发上的时候，它又会悄无声息地跳上来，趴在你的膝盖上呼噜呼噜。"
        m3 "我觉得……它很像我。"
        m3 "只想在夜里，静静地独占你的体温。"
        show m3_smile at m3_idle_zoom
        jump .home_conflict_phase

    label .pet_crow:
        hide m3_4
        show m3_smug at m3_speaking_zoom
        m3 "我想养一只乌鸦。"
        m3 "不是关在笼子里的那种，而是可以让它停在肩膀上，或者飞出去又会飞回来的那种。"
        show m3_smug at m3_idle_zoom
        "[player]" "乌鸦？这倒是很少见。不过听说它们很聪明。"
        show m3_smug at m3_speaking_zoom
        m3 "是非常聪明。它们能记住人的脸，而且一旦认定了主人，就会非常忠诚。"
        m3 "它会帮我们收集闪闪发光的小东西……也许是玻璃片，也许是硬币。"
        m3 "那种漆黑的羽毛，在阳光下会反射出彩虹一样的光泽……不觉得很美吗？"
        m3 "我想让它成为我们的‘眼睛’，看着这个只属于我们的家。"
        show m3_smug at m3_idle_zoom
        jump .home_conflict_phase
    label .pet_snake:
        hide m3_4
        show m3_8 at m3_speaking_zoom
        m3 "我想养一条蛇。"
        m3 "那种鳞片冰凉、触感光滑的，白色的或者是黑色的蛇。"
        show m3_8 at m3_idle_zoom
        "[player]" "蛇？！这……稍微有点吓人吧？"
        show m3_8 at m3_speaking_zoom
        m3 "才不可怕呢。它们其实很温柔。"
        m3 "我也喜欢那种体温偏低的感觉……需要靠着热源才能活下去。"
        m3 "想象一下，它慢慢地缠绕在你的手臂上，或者是脖子上……那种轻微的束缚感，那种紧紧贴着皮肤的感觉。"
        m3 "就像是一个绝对不会松开的拥抱。"
        m3 "很安心，不是吗？"
        show m3_8 at m3_idle_zoom
        jump .home_conflict_phase

    label .home_conflict_phase:
        "她描述着那个有宠物陪伴的未来，眼里的光芒越来越柔和。"
        "在这一刻，她不再是那个高高在上的引导者，也不再是那个总是带着神秘感的少女。"
        "她只是一个渴望着平凡幸福、渴望着有一个“归处”的女孩。"
        "她重新靠回我的怀里，手指在我的胸口轻轻画着圈。"
        hide m3_8
        hide m3_smug
        hide m3_smile
        show m3_shy_smile at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "这样的生活……你会觉得无聊吗？"
        m3 "每天吃着外卖，逗着宠物，窝在沙发上看无聊的电视节目……就这样一直一直过下去。"
        m3 "如果不出去‘冒险’，如果世界只剩下我们两个人……"
        m3 "你愿意吗？"
        menu:
            "我求之不得。这就是我梦寐以求的生活。":
                jump .home_choice_good
            "偶尔这样还行，但一直这样的话感觉像是在养老。":
                jump .home_choice_bad
    label .home_choice_good:
        $ persistent.mortis_love += 1
        show m3_shy_smile at m3_idle_zoom
        "[player]" "说什么傻话呢。"
        "[player]" "这怎么会无聊？这就是我梦寐以求的生活啊。"
        "[player]" "只要有你在，哪怕只是看着墙壁发呆也是有趣的。更别说还有好吃的，还有可爱的宠物。"
        "我低下头，在她的额头上轻轻印下一吻。"
        "[player]" "以后我们就这么过吧。不去管外面的世界，只经营我们的小日子。"
        hide m3_shy_smile
        show m3_surprise at center 
        "墨缇斯的身体颤抖了一下，随即变得更加柔软。"
        "她抬起头，脸颊绯红，眼角眉梢都洋溢着幸福的笑意。"
        hide m3_surprise
        show m3_3 at m3_speaking_zoom
        m3 "……嗯！"
        m3 "这可是你说的，不许反悔哦。"
        m3 "那我们就这么约定了。不管发生什么……这里永远是我们的家。"
        m3 "我也……最喜欢你了。"
        show m3_3 at m3_idle_zoom
        "她紧紧地抱住我的腰，力气大得仿佛要把自己融入我的身体里。"
        "电视的声音似乎变小了，整个世界只剩下我们要溢出来的幸福感。"
        jump .home_end
    label .home_choice_bad:
        $ persistent.mortis_love -= 1
        show m3_shy_smile at m3_idle_zoom
        "[player]" "嗯……偶尔这样放松一下确实不错啦。"
        "[player]" "但如果是一直这样的话……感觉像是在提前养老一样，会不会太颓废了？"
        "[player]" "毕竟人还是要有点追求的嘛，总是待在屋子里也会憋坏的。"
        hide m3_shy_smile
        show m3_thinking at center
        "墨缇斯在我怀里的动作停住了。"
        "那种温馨的粉色氛围像泡沫一样迅速破碎。"
        show m3_thinking at m3_speaking_zoom
        m3 "……追求？"
        m3 "也是呢……对外面的世界来说，这小小的客厅确实太狭窄了。"
        show m3_thinking at m3_idle_zoom
        "她坐直了身体，整理了一下稍微有些凌乱的头发，表情恢复了平日里的冷静。"
        hide m3_thinking
        show m3_side_normal at m3_speaking_zoom
        m3 "抱歉，是我自顾自地沉浸在幻想里了。"
        m3 "这种‘过家家’一样的生活……确实没什么实际意义，可能只会让你觉得厌烦吧。"
        show m3_side_normal at m3_idle_zoom
        "她拿起身边的遥控器，关掉了电视。"
        "房间里瞬间安静下来，只有窗外的雨声显得格外凄凉。"
        jump .home_end
    
    label .home_end:
        "时间不知不觉已经很晚了。"
        "窗外的雨势似乎变大了一些，密集的雨点敲打在玻璃上，将城市的所有喧嚣都彻底隔绝在了那层薄薄的水幕之外。"
        "在这个只属于我们两人的、被暖黄色灯光填满的客厅里，刚才关于未来的构想仿佛已经有了实感。"
        "空气中残留着香氛的甜味，我甚至能产生一种错觉——仿佛那只还没领回家的宠物，此刻正趴在脚边的地毯上，发出安稳的呼吸声。"
        "墨缇斯没有再说话，只是静静地靠在我的肩头，手指无意识地把玩着我的衣角。"
        "她的呼吸频率逐渐变得平缓，体温透过布料传递过来，那种沉甸甸的信赖感，比任何语言都要真实。"
        "‘一直这样过下去……吗？’"
        "我不由得收紧了拥抱着她的手臂，下巴轻轻抵在她的发顶。"
        "在这个瞬间，我也许真的动摇了。"
        "不需要去思考明天的天气，也不需要去面对复杂的社会关系。"
        "只要这盏灯还亮着，只要怀里的人还在……"
        "这个小小的、封闭的四方天地，或许真的就是世界上最坚固、也最温暖的堡垒。"
        "我们在雨声的伴奏下交换了一个漫长的拥抱，任由这份几乎要将人融化的安宁，将意识慢慢淹没。"
        scene black with fade
        return


# 河岸的夕阳,下午
label mortis_date_riverside:
    scene  riverside_sunset_gold with fade
    play music "audio/mortis/うたたね、霞む景色.ogg" 
    "天空被燃烧的晚霞染成了绚烂的紫红色，连带着面前宽阔的河面也波光粼粼，仿佛流淌着融化的金子。"
    "河堤边的芦苇在晚风中轻轻摇曳，发出沙沙的声响。"
    "这里没有城市的喧嚣，只有水流的声音和风的声音。夕阳将我们的影子拉得很长，长到似乎要交织在一起，融入那片深沉的河水之中。"
    "我们并肩走在河堤的草地上。墨缇斯没有挽着我的手，但我能感觉到她的衣袖时不时轻轻擦过我的手臂。"
    "这种若即若离的触感，在这个黄昏时分显得格外暧昧。"
    show m3_side_normal at center with dissolve
    "她停下脚步，眯起眼睛眺望着那轮即将沉入地平线的太阳。"
    "金色的余晖洒在她的脸上，给那平日里略显苍白的皮肤镀上了一层柔和的暖色。"
    "那一瞬间，她美得像是一尊就要随着光线消失的雕塑。"
    show m3_side_normal at m3_speaking_zoom
    m3 "…好美。"
    m3 "但是，也很残酷。"
    show m3_side_normal at m3_idle_zoom
    "[player]" "残酷？为什么会这么觉得？"
    hide m3_side_normal
    show m3_0 at m3_speaking_zoom
    m3 "因为这一刻马上就要结束了。"
    m3 "不管这夕阳有多美，它都在无可挽回地坠落。再过几分钟，这里就会被黑暗吞没。"
    m3 "所谓的美好，总是伴随着流逝……这难道不残酷吗？"
    show m3_0 at m3_idle_zoom
    "她转过头看着我，眼神中带着一种深深的眷恋。"
    hide m3_0
    show m3_1 at m3_speaking_zoom
    m3 "[player]，如果我也拥有神明那样的权能……"
    m3 "如果我可以让这个世界的时钟停摆，让时间永远定格在某一个季节，不再流动……"
    m3 "你知道我会选择哪个季节吗？"
    show m3_1 at m3_idle_zoom
    pause 1.0
    $ current_season = persistent.mq_answers["season"]
    if current_season == "春天":
        jump .season_spring
    elif current_season == "夏天":
        jump .season_summer
    elif current_season == "秋天":
        jump .season_autumn
    elif current_season == "冬天":
        jump .season_winter
    else:
        jump .season_spring

    label .season_spring:
        hide m3_1
        show m3_smile at m3_speaking_zoom
        m3 "我会选择春天。"
        m3 "并不是因为那些艳俗的花朵，而是因为那种‘开始’的感觉。"
        m3 "万物复苏，冰雪消融……整个世界都是新的。"
        show m3_smile at m3_idle_zoom
        "[player]" "春天确实充满了希望呢。"
        show m3_smile at m3_speaking_zoom
        m3 "是啊。如果我们永远停在春天，那就意味着我们要永远处于‘相遇’的那个阶段。"
        m3 "那种懵懂的、小心翼翼的、充满了可能性的悸动……永远不会变质，也永远不会迎来结局。"
        m3 "我想和你……一直一直都在‘重新开始’。"
        show m3_smile at m3_idle_zoom
        jump .weather_transition
    label .season_summer:
        show m3_1 at m3_speaking_zoom
        m3 "我会选择夏天。"
        m3 "那个充满了蝉鸣、烈日和暴雨的季节。"
        show m3_1 at m3_idle_zoom
        "[player]" "夏天？那不是很热吗？"
        show m3_1 at m3_speaking_zoom
        m3 "热才好啊。那种仿佛要将灵魂都蒸发的温度，那种极致的生命力。"
        m3 "我想把时间停在夏至的那一天，停在白昼最长的那一刻。"
        m3 "那样的话，太阳就永远不会落下，我们也就不用面对黑夜的分离了。"
        m3 "我们就永远在那耀眼的阳光下，大汗淋漓地牵着手……直到世界尽头。"
        show m3_1 at m3_idle_zoom
        jump .weather_transition
    label .season_autumn:
        hide m3_1
        show m3_sad at m3_speaking_zoom
        m3 "我会选择秋天。"
        m3 "就像现在的景色一样……万物开始枯萎，世界变得金黄而安静。"
        show m3_sad at m3_idle_zoom
        "[player]" "秋天总觉得有点悲伤呢。"
        show m3_sad at m3_speaking_zoom
        m3 "悲伤是因为它们会消失。但如果时间停止了，这就叫‘永恒的静美’。"
        m3 "我不喜欢太吵闹的东西。在秋天，一切都在慢慢沉睡。"
        m3 "我想和你一起踩在落叶上，听那种清脆的破碎声。在这个逐渐走向终结的世界里，只有我们两个人是醒着的。"
        show m3_sad at m3_idle_zoom
        jump .weather_transition
    label .season_winter:
        hide m3_1
        show m3_dark at m3_speaking_zoom
        m3 "我会选择冬天。"
        m3 "那种把一切肮脏和喧嚣都掩埋在冰雪之下的季节。"
        show m3_dark at m3_idle_zoom
        "[player]" "冬天啊……虽然很冷，但下雪的时候确实很浪漫。"
        show m3_dark at m3_speaking_zoom
        m3 "嗯。那种寒冷可以冻结一切，包括时间，包括腐烂。"
        m3 "在这个白茫茫的一无所有的世界里，我们只能紧紧地拥抱彼此来取暖。"
        m3 "不需要去别的地方，也不需要见别的人。因为外面是大雪封山，我们哪儿也去不了。"
        m3 "那是……最完美的二人世界。"
        show m3_dark at m3_idle_zoom
        jump .weather_transition

    label .weather_transition:
        "她描述那个永恒季节时的神情，专注得有些令人心疼。"
        "仿佛她真的在脑海中构建了那样一个静止的世界，并且正独自一人站在那里等待着我。"
        hide m3_dark
        hide m3_sad
        hide m3_1
        hide m3_smile
        show m3_thinking at m3_speaking_zoom
        m3 "只有季节还不够……"
        m3 "还要有天空的颜色，要有空气的味道。"
        show m3_thinking at m3_idle_zoom
        "她抬起头，看着头顶那片逐渐从金红转为深蓝的天空。"
        show m3_thinking at m3_speaking_zoom
        m3 "呐，[player]，如果那个世界的天空永远保持一种状态……"
        m3 "你觉得，哪种天气最适合我们？"
        show m3_thinking at m3_idle_zoom
        pause 1.0

        $ current_weather = persistent.mq_answers["weather"]

        if current_weather == "暴雨":
            jump .weather_rain
        elif current_weather == "雪天":
            jump .weather_snow
        elif current_weather == "阴天":
            jump .weather_overcast
        elif current_weather == "雷暴":
            jump .weather_thunderstorm
        else:
            jump .weather_rain

    label .weather_rain:
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "我希望是暴雨。"
        m3 "倾盆大雨，雨声大到听不见彼此的呼吸声，大到整个世界都被水幕遮挡。"
        show m3_1 at m3_idle_zoom
        "[player]" "暴雨？那岂不是哪里都去不了了？"
        show m3_1 at m3_speaking_zoom
        m3 "就是因为哪里都去不了才好啊。"
        m3 "雨水会把外面的一切都冲刷干净，也会把所有试图靠近我们的人都阻挡在外面。"
        m3 "我们躲在屋檐下，或者是房间里……那一小块干燥的地方，就是我们的全世界。"
        show m3_1 at m3_idle_zoom
        jump .riverside_conflict_phase


    label .weather_snow:
        hide m3_thinking
        show m3_smile at m3_speaking_zoom
        m3 "我希望是雪天。"
        m3 "漫天飞舞的大雪，无声无息地落下，把天地间的一切都染成白色。"
        show m3_smile at m3_idle_zoom
        "[player]" "下雪确实很美，世界会变得很安静。"
        show m3_smile at m3_speaking_zoom
        m3 "是啊，安静得……就像是死掉了一样。"
        m3 "所有的脚印都会被覆盖，所有的路都会消失。"
        m3 "在这个被遗忘的白色迷宫里，我是你唯一的向导，也是你唯一的体温。"
        show m3_smile at m3_idle_zoom
        jump .riverside_conflict_phase

    label .weather_overcast:
        show m3_thinking at m3_speaking_zoom
        m3 "我希望是阴天。"
        m3 "厚厚的云层遮住太阳，没有刺眼的光，也没有浓重的影子。"
        show m3_thinking at m3_idle_zoom
        "[player]" "阴天？会不会太压抑了？"
        show m3_thinking at m3_speaking_zoom
        m3 "不会。我觉得那是‘温柔’。"
        m3 "那种灰色的、均匀的光线，不会刺伤眼睛，也不会让人感到焦虑。"
        m3 "就像是一床厚厚的棉被，轻轻地盖在城市上空。"
        m3 "在这样的天空下，我们无论做什么，都可以很安心。"
        show m3_thinking at m3_idle_zoom
        jump .riverside_conflict_phase

    label .weather_thunderstorm:
        hide m3_thinking
        show m3_12 at m3_speaking_zoom
        m3 "我希望是雷暴。"
        m3 "黑云压城，电闪雷鸣，那种仿佛世界末日即将来临的天气。"
        show m3_12 at m3_idle_zoom
        "[player]" "这……这也太刺激了吧？"
        show m3_12 at m3_speaking_zoom
        m3 "刺激吗？但我喜欢那种压迫感。"
        m3 "当雷声炸响的时候，你会害怕吗？你会本能地寻找依靠吗？"
        m3 "那个时候，如果我紧紧抱住你，告诉你‘别怕，有我在’……"
        m3 "你的心跳，是不是就会只属于我一个人了？"
        show m3_12 at m3_idle_zoom
        jump .riverside_conflict_phase

    label .riverside_conflict_phase:
        "夕阳终于完全沉入了地平线，天空从金红变成了深邃的蓝紫色。"
        "河对岸的城市灯火开始零星亮起，倒映在水面上，随波逐流。"
        "墨缇斯转过身，背对着那片即将到来的夜色，向我伸出了手。"
        hide m3_12
        hide m3_smile
        hide m3_thinking
        hide m3_1
        show m3_shy_smile at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "如果真的有那样一个世界……"
        m3 "只有我们要的季节，只有我们要的天气，永远不会改变，永远不会有外人打扰。"
        m3 "你会愿意……和我一起被困在那个时间循环里吗？"
        menu:
            "永远不变的话会失去活着的实感吧。":
                jump .riverside_choice_bad
            "如果那个世界里有你，那对我来说就是天堂。":
                jump .riverside_choice_good
    label .riverside_choice_good:
        show m3_shy_smile at m3_idle_zoom
        $ persistent.mortis_love += 1
        "[player]" "当然愿意。"
        "[player]" "如果是和你在一起，别说是时间循环了，就算是世界末日我也无所谓。"
        "[player]" "只要你在，那个静止的世界就是天堂。我们可以在那里慢慢浪费所有的时间。"
        "我握住了她伸出来的手。她的手很凉，但在接触的那一刻，我们都感觉到了某种连接。"
        hide m3_shy_smile
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "……太好了。"
        m3 "我就知道你会懂的。"
        m3 "不需要未来，也不需要变化……只要有‘现在’就足够了。"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她向前迈了一步，轻轻靠在我的肩膀上，看着河面上破碎的灯光。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "那我们就说好了。"
        m3 "总有一天，我会为你创造出那个世界的……只属于我们两个人的乐园。"
        jump .riverside_end

    label .riverside_choice_bad:
        show m3_shy_smile at m3_idle_zoom
        $ persistent.mortis_love -= 1
        "[player]" "这个……虽然听起来很浪漫，但仔细想想还是有点可怕。"
        "[player]" "如果永远都不变的话，那就没有‘明天’了吧？"
        "[player]" "一直重复同样的日子，总有一天会麻木的。我觉得还是流动的时间更有活着的实感。"
        hide m3_shy_smile
        show m3_sad at center
        "墨缇斯的手在半空中停滞了一下，然后缓缓垂了下去。"
        "夜色似乎在这一刻变得更加浓重了。"
        show m3_sad at m3_speaking_zoom
        m3 "……活着的实感吗？"
        m3 "是啊，人类总是贪恋‘变化’和‘未知’。"
        m3 "哪怕那是通向死亡的变化，你们也觉得比永恒的静止要好。"
        "她苦笑了一下，笑容里充满了落寞。"
        m3 "看来，我想要的那种‘永恒’，对你来说只是一个漂亮的牢笼罢了。"
        m3 "没关系……我理解。毕竟你是活生生的人，而我……"
        show m3_sad at m3_idle_zoom
        "她没有把话说完，只是转过身，独自看着漆黑的河面。"
        jump .riverside_end

    label .riverside_end:
        "夜幕彻底降临了。"
        "晚风变得有些凉意，吹乱了她的发丝，也吹皱了河面上的倒影。"
        "我们站在堤岸上，身后是万家灯火，面前是流淌不息的河水。"
        "不管我们的愿望如何，时间依然在无情地向前流动。"
        "但至少在此刻，在她刚刚描述的那个关于季节和天气的幻想里，我们确实短暂地拥有过永恒。"
        "我脱下外套披在她身上，她拉紧了领口，回头看了我一眼。"
        "那个眼神里，藏着比夜色更深的东西——那是一个不会随着季节更替而改变的、固执的愿望。"
        scene black with fade
        return


# 等待的车站,下午
label mortis_date_bus_stop:
    scene  bus_stop_countryside with fade
    play music "audio/mortis/桃色の風.ogg" 
    "这里是一个似乎已经被废弃的公交车站。"
    "生锈的站牌歪歪斜斜地立在路边，上面的字迹早已被风雨剥蚀得模糊不清。只有那个代表着‘停靠’的符号，还勉强能辨认出来。"
    "长椅上的油漆剥落了大半，露出了下面灰白色的木纹。坐上去的时候，会发出轻微的‘吱呀’声。"
    "四周是一片半人高的荒草，在风中起伏着，发出沙沙的声响。"
    "我们在这里已经坐了很久。十分钟？半小时？还是更久？"
    "时刻表上写着每二十分钟一班车，但那条延伸向远方的公路上，始终空空荡荡，连一辆过路的车都没有。"
    show m3_side_normal at center with dissolve
    "墨缇斯坐在我的左侧，双手规矩地放在膝盖上，侧脸平静地望着公路的尽头。"
    "她似乎一点也不着急，甚至很享受这种漫无目的的等待。"
    "[player]" "看来这辆车是不会来了。时刻表大概是几年前的吧。"
    "[player]" "要不我们还是走回去吧？虽然有点远，但总比在这里干坐着强。"
    "听到我的话，墨缇斯慢慢转过头，她的眼睛里倒映着荒野的景色。"
    hide m3_side_normal
    show m3_smile at m3_speaking_zoom
    m3 "没关系，再坐一会儿吧。"
    m3 "你不觉得……这种哪里都不用去，哪里也去不了的时间，很珍贵吗？"
    show m3_smile at m3_idle_zoom
    "她稍微调整了一下坐姿，向我这边靠了靠，肩膀轻轻抵住了我的手臂。"
    show m3_smile at m3_speaking_zoom
    m3 "在这个车站，时间仿佛变得很慢很慢。"
    m3 "慢到可以让我听清每一次心跳，慢到可以让我仔细观察光线在每一片草叶上的变化。"
    show m3_smile at m3_idle_zoom
    "[player]" "光线的变化吗……确实，这里的风景有种独特的萧瑟感。"
    hide m3_smile
    show m3_thinking at m3_speaking_zoom
    m3 "呐，[player]。"
    m3 "一天有二十四个小时，光线和温度都在不停地流转。"
    m3 "如果是你的话，你最希望世界停留在哪个时刻？"
    m3 "或者换个说法……你觉得，哪一个时间段的我，最接近你心中‘美’的定义？"
    show m3_thinking at m3_idle_zoom
    pause 1.0
    $ current_time_of_day = persistent.mq_answers["time"]
    # 根据时间段跳转
    if current_time_of_day == "黎明":
        jump .time_dawn
    elif current_time_of_day == "正午":
        jump .time_noon
    elif current_time_of_day == "黄昏":
        jump .time_dusk
    elif current_time_of_day == "深夜":
        jump .time_night
    else:
        jump .time_dawn


    label .time_dawn:
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "如果让我选的话……我最喜欢的是黎明。"
        m3 "大约是清晨四点到六点之间，那是‘蓝色时刻’。"
        show m3_1 at m3_idle_zoom
        "[player]" "黎明？那时候大部分人都还在睡觉吧。"
        show m3_1 at m3_speaking_zoom
        m3 "正是因为大家都在睡觉，所以那个世界才是干净的。"
        m3 "太阳还没完全升起，空气是冰蓝色的，带着一种刺骨的清冷。"
        m3 "那是世界苏醒前的一瞬间，没有喧嚣，没有谎言。"
        m3 "我想在那个时刻牵着你的手走在空无一人的街道上……感觉就像是我们私奔到了世界的尽头一样。"
        show m3_1 at m3_idle_zoom
        jump .bus_stop_conflict_phase
    label .time_noon:
        hide m3_thinking
        show m3_smile at m3_speaking_zoom
        m3 "我最喜欢的是正午。"
        m3 "也就是十二点到下午两点，阳光最猛烈的时候。"
        show m3_smile at m3_idle_zoom
        "[player]" "有点意外，我以为你会喜欢阴暗一点的时间。正午太刺眼了吧？"
        show m3_smile at m3_speaking_zoom
        m3 "刺眼才好。在垂直的阳光下，所有的影子都会消失。"
        m3 "我不喜欢暧昧不清的东西，也不喜欢藏在阴影里的秘密。"
        m3 "在正午的阳光下，不管是你，还是我，都无处遁形。"
        m3 "我想在那样的光线下看着你，看清你脸上的每一个毛孔，确认你是完完全全属于我的实体。"
        show m3_smile at m3_idle_zoom
        jump .bus_stop_conflict_phase
    label .time_dusk:
        hide m3_thinking
        show m3_smile at m3_speaking_zoom
        m3 "毫无疑问，是黄昏。"
        m3 "傍晚六点到八点，也就是现在这个时刻。"
        show m3_smile at m3_idle_zoom
        "[player]" "逢魔之时吗？确实很有氛围感。"
        show m3_smile at m3_speaking_zoom
        m3 "嗯。那是白天和黑夜交接的伤口，是世界最脆弱的时候。"
        m3 "光线会变成暧昧的茜色，人的轮廓会变得模糊。"
        m3 "在这种界限不清的时间里，我觉得我好像能离你更近一些。"
        m3 "就像这即将沉没的太阳一样……这种带着毁灭气息的美感，让我着迷。"
        show m3_smile at m3_idle_zoom
        jump .bus_stop_conflict_phase
    label .time_night:
        hide m3_thinking
        show m3_1 at m3_speaking_zoom
        m3 "当然是深夜。"
        m3 "零点到凌晨两点。那是属于‘非人’的时间。"
        show m3_1 at m3_idle_zoom
        "[player]" "熬夜可是对皮肤不好的。不过深夜确实很安静。"
        show m3_1 at m3_speaking_zoom
        m3 "不仅仅是安静。那时候，世界的逻辑防线是最薄弱的。"
        m3 "所有的理智、道德、规则，在深夜都会变得模糊。"
        m3 "只有在那个时间，我才觉得我不必扮演任何角色。"
        m3 "我可以只是我，你也只是你。我们在黑暗中拥抱，就像两颗在这个寂静宇宙中孤独漂浮的尘埃。"
        show m3_1 at m3_idle_zoom
        jump .bus_stop_conflict_phase


    label .bus_stop_conflict_phase:
        "她说完那个时间段后，深深地吸了一口气，仿佛在吞吐着那个时刻独有的空气。"
        "周围的风声似乎变大了，吹得站牌发出咔哒咔哒的声音。"
        "但那辆传说中的公交车，依然没有任何踪影。"
        pause 1.0
        hide m3_1
        hide m3_smile

        show m3_shy_smile at m3_speaking_zoom

        m3 "虽然我很喜欢那个时间……"
        m3 "但其实，只要是和你在一起，哪怕是这种无聊的、漫长的等待，我也觉得是甜的。"
        show m3_shy_smile at m3_idle_zoom
        "她抬起头，眼神中带着一丝试探。"
        show m3_shy_smile at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "你会觉得我不讲道理吗？明明没有车，还要拉着你在这里浪费时间。"
        m3 "如果我说……我想一直坐到天荒地老，坐到这个车站腐烂为止……你会陪我吗？"

        menu:
            "和你在一起,等待本身就是目的地。":
                jump .bus_stop_choice_good
            
            "别开玩笑了，一直坐这里也太傻了。":
                jump .bus_stop_choice_bad


    label .bus_stop_choice_good:
        $ persistent.mortis_love += 1
        show m3_shy_smile at m3_idle_zoom
        "[player]" "求之不得。"
        "[player]" "谁说这是浪费时间？和你在一起，‘等待’这件事情本身，就是最棒的目的地。"
        "[player]" "我们不需要去哪里。只要坐在这里，听着风声，看着你……这就足够了。"
        "我伸出手，轻轻揽住了她的肩膀。"
        hide m3_shy_smile
        show m3_surprise at center
        
        "墨缇斯愣了一下，随即身体完全放松下来，顺从地靠进了我的怀里。"
        "她的嘴角上扬，露出了一个发自内心的、如释重负的笑容。"
        hide m3_surprise
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "……嗯。"
        m3 "我就知道……只有你能理解这种感觉。"
        m3 "目的地什么的根本不重要。重要的是，现在这一秒，我们的时间是重叠的。"
        show m3_happy_closed_eyes at m3_idle_zoom
        pause 1.0
        hide m3_happy_closed_eyes
        show m3_sitting_relax at center
        "她闭上眼睛，仿佛真的打算就这么睡过去。"
        show m3_sitting_relax at m3_speaking_zoom
        m3 "那就不等车了。我们就在这里……把时间用光吧。"
        
        jump .bus_stop_end
    label .bus_stop_choice_bad:
        show m3_shy_smile at m3_idle_zoom
        $ persistent.mortis_love -= 1
        "[player]" "别开玩笑了。"
        "[player]" "虽然我也很喜欢和你在一起，但一直坐在这个破长椅上吹风也太傻了。"
        "[player]" "而且天都要黑了，这里会有蚊子的。我们还是叫个车回去吧。"
        
        "我拿出手机，准备查看叫车软件。"
        "身边的温度似乎瞬间下降了。"
        hide m3_shy_smile
        show m3_yandere_cold at center
        "墨缇斯坐直了身体，理了理被风吹乱的头发。那个温馨的氛围瞬间消散，取而代之的是一种令人尴尬的疏离感。"
        show m3_yandere_cold at m3_speaking_zoom
        m3 "……蚊子？"
        m3 "也是呢。人类是脆弱的生物，会被叮咬，会觉得冷，会觉得无聊。"
        show m3_yandere_cold at m3_idle_zoom
        "她站起身，拍了拍裙摆上的灰尘，居高临下地看着我。"
        show m3_yandere_cold at m3_speaking_zoom
        m3 "我只是想和你分享一段‘静止’的时光……看来这对你来说只是一种折磨。"
        m3 "既然你那么想走，那就走吧。反正……这辆车本来也不会来。"
        show m3_yandere_cold at m3_idle_zoom
        "她转过身，沿着公路大步向前走去，没有再回头看我一眼。"
        jump .bus_stop_end


    label .bus_stop_end:
        "生锈的站牌依然静静地立在那里，像是一个被时间遗弃的守墓人。"
        "公路延伸向黑暗的尽头，被荒草和夜色吞没，不知通往何方，也不知是否真的存在所谓的终点。"
        "周围的蝉鸣声似乎不知疲倦地响着，将时间的刻度无限拉长、再拉长，直到失去了意义。"
        "在这个被世界遗忘的坐标点上，那辆永远不会抵达的公交车，成了一个只属于我们两人的秘密隐喻。"
        "这里没有过去，也没有未来，只有在这个破旧长椅上不断延展的、粘稠而静谧的‘现在’。"
        "我看着墨缇斯在夜色中显得有些朦胧的侧脸，心中突然涌起一种奇异的安宁。"
        "也许正如她所说，在这个停滞的时空里，‘等待’本身就被赋予了某种神圣的意义。"
        "不需要去往任何目的地，也不需要追赶任何进度。"
        "因为此时此刻，在这个荒凉的宇宙中心，我也好，她也好，都已经确认了彼此是唯一真实的依靠。"
        "这份在荒野中共同度过的、毫无效率却又无比奢侈的空白时光，或许比任何风景都更接近她口中那个‘永恒’的注脚。"
        scene black with fade
        return

#天文馆，下午
label mortis_date_planetarium:

    # --- 场景初始化 ---
    scene  planetarium_dark with fade
    play music "audio/mortis/月光夜.ogg"
    "厚重的天鹅绒帷幕缓缓合上，将外界的光线彻底隔绝。"
    "随着那台位于大厅中央、如同巨大的蚂蚁一般的投影仪发出低沉的嗡嗡声，原本漆黑一片的穹顶瞬间被点亮了。"
    "亿万颗星辰在头顶铺开，银河像是一条流淌的钻石河流，横跨了整个视野。"
    "虽然理智告诉我这只是光学的把戏，但在这一刻，那种扑面而来的壮丽感依然让人屏住了呼吸。"
    show m3_surprise at center with dissolve
    "坐在我身旁的墨缇斯，反应比我还要剧烈得多。"
    "她整个人都从柔软的躺椅上弹了起来，双手在那片虚假的星空下胡乱挥舞着，似乎想抓住那些并不存在的光点。"
    show m3_surprise at m3_speaking_zoom with dissolve
    m3 "哇——！！"
    m3 "好亮！好闪！好多好多的小点点！"
    m3 "[player]！快看！头顶上有发光的河！"
    show m3_surprise at m3_idle_zoom
    "[player]" "那是银河哦。虽然是投影出来的，但很漂亮吧？"
    hide m3_surprise
    show m3_sparkle_eyes at center
    "她转过头，那双金色的眼睛里倒映着漫天的星光，看起来比任何一颗星星都要璀璨。"
    show m3_sparkle_eyes at m3_speaking_zoom
    m3 "嗯！超级漂亮！"
    m3 "就像是有人把一整罐发光的糖果全都洒在了黑色的布丁上一样！"
    m3 "嘿嘿……如果能吃一口的话，一定也是甜甜的吧？"
    show m3_sparkle_eyes at m3_idle_zoom
    "她重新躺回椅子上，但并不是安分地躺着，而是侧过身，像只寻找热源的小动物一样，紧紧地贴着我的手臂。"
    "在这个黑暗而安静的空间里，她的体温透过衣料传递过来，成为了这片寒冷宇宙中唯一的真实。"
    hide m3_sparkle_eyes
    show m3_thinking at m3_speaking_zoom
    m3 "呐，[player]……"
    m3 "你说，这个把星星装在盒子里的魔法，是谁施展的呀？"
    show m3_thinking at m3_idle_zoom
    "[player]" "是中间那台机器投影出来的。不过如果是指真正的宇宙……那就是更宏大的存在了吧。"
    "墨缇斯歪着头，手指在半空中画着圈，似乎在进行着某种她独有的思考。"
    show m3_thinking at m3_speaking_zoom
    m3 "宏大的存在……也就是‘神明大人’对吧？"
    m3 "虽然我不认识那个神明大人……"
    m3 "但是我在想哦，如果让我来做神明大人，让我来创造一个像这样的世界……"
    show m3_thinking at m3_idle_zoom
    "她突然兴奋地凑到我耳边，声音里带着一种分享秘密般的神秘感。"
    show m3_thinking at m3_speaking_zoom
    m3 "我知道一种超级厉害的魔法哦！"
    m3 "如果是我的话，我一定会用那个叫Ren'Py的魔法来创造世界！"
    show m3_thinking at m3_idle_zoom
    "[player]" "Ren'Py？那是什么奇怪的咒语吗？为什么要用那个？"
    hide m3_thinking
    show m3_shy_smile at center
    "墨缇斯不好意思地挠了挠脸颊，吐了吐舌头。"
    show m3_shy_smile at m3_speaking_zoom
    m3 "嘿嘿……因为……因为墨缇斯比较笨嘛。"
    m3 "那个叫Ren'Py的魔法最简单啦！"
    m3 "只要写几行字，画几张图，‘砰’的一下！世界就出来啦！"
    m3 "如果是别的复杂的魔法，我肯定学不会，脑袋会冒烟的！"
    m3 "可惜我不会用Webgal，不然你就能看到会动的我啦。"
    m3 "但是Ren'Py的话，就算是笨笨的我，也能为你写出一个故事来哦！"
    m3 "所以……不管真正的神是用什么做的，我心中的创世神器，绝对就是Ren'Py！"
    show m3_shy_smile at m3_idle_zoom
    "[player]" "原来如此……听起来确实是很适合你的‘魔法’呢。简单直接，又能创造奇迹。"
    "她开心地在椅子上蹭了蹭。"
    show m3_shy_smile at m3_speaking_zoom
    m3 "对吧对吧！"
    m3 "等我完全学会了那个魔法，我就给你变出一万个我，天天围着你转！"
    show m3_shy_smile at m3_idle_zoom
    pause 1.0
    hide  m3_shy_smile
    show m3_0 at center
    "话题告一段落，穹顶上的星空开始缓慢旋转，模拟着地球的自转。"
    "墨缇斯伸出手指，试图去数那些星星，但很快就放弃了。"
    hide m3_0
    show m3_1 at m3_speaking_zoom
    m3 "呜……不行了，眼睛要花了。"
    m3 "星星太多了，根本数不过来嘛！"
    m3 "一、二、三……啊！又忘记数到哪里了！"
    show m3_1 at m3_idle_zoom
    "[player]" "不用全都数清楚也没关系。只要找到你喜欢的那颗就行了。"
    show m3_1 at m3_speaking_zoom
    m3 "喜欢的星星……也就是喜欢的数字吗？"
    m3 "呐呐，[player]，你知道在所有的数字里面，我最喜欢哪一个吗？"
    $ current_number = persistent.mq_answers["number"]
    if current_number == "3（三位一体）":
        jump .number_3
    elif current_number == "7（神秘数字）":
        jump .number_7
    elif current_number == "13（不祥之数）":
        jump .number_13
    elif current_number == "0（虚无）":
        jump .number_0
    else:
        jump .number_3
    label .number_3:
        m3 "嘿嘿，是3哦！"
        m3 "你看，三角形是不是超级稳固？怎么推都推不倒！"
        show m3_1 at m3_idle_zoom
        "[player]" "确实，三角形是最稳定的结构。"
        show m3_1 at m3_speaking_zoom
        m3 "而且而且！爸爸、妈妈、孩子……通常也是三个人对吧？"
        m3 "虽然我的父母......算了。"
        m3 "但是在我的世界里，有你，有我，还有我们之间的‘爱’！"
        m3 "加起来正好是3个！是不是很完美？"
        jump .planetarium_conflict_phase

    label .number_7:
        m3 "当然是7啦！"
        m3 "大家都说7是Lucky Number嘛！"
        show m3_1 at m3_idle_zoom
        "[player]" "是因为想变得幸运吗？"
        show m3_1 at m3_speaking_zoom
        m3 "嗯！因为遇见[player]这件事，就已经花光了我所有的运气了！"
        m3 "所以我得赶紧补一点回来！"
        m3 "而且彩虹也是7种颜色，白雪公主也有7个小矮人……"
        m3 "感觉只要有7在，故事的结局就一定是 Happy End！"
        jump .planetarium_conflict_phase

    label .number_13:
        m3 "哼哼，告诉你，是13哦！"
        show m3_1 at m3_idle_zoom
        "[player]" "13？那不是大家都觉得不吉利的数字吗？"
        show m3_1 at m3_speaking_zoom
        m3 "就是因为大家都讨厌它，所以它太可怜了呀！"
        m3 "明明只是个普通的数字，却被大家躲着走……"
        m3 "感觉它孤零零的样子……有点像遇到你之前的我。"
        m3 "所以我要喜欢它！我要做世界上唯一一个对它好的人！"
        
        jump .planetarium_conflict_phase
    label .number_0:
        m3 "是0呀！"
        m3 "你不觉得 0 长得圆滚滚的，很像一个鸡蛋，或者甜甜圈吗？"
        show m3_1 at m3_idle_zoom
        "[player]" "居然是因为像吃的吗……"
        show m3_1 at m3_speaking_zoom
        m3 "才不是呢！0 代表开始，也代表圆满！"
        m3 "所有的东西都是从 0 开始的。"
        m3 "而且，你看那个圆圈，从起点出发，转一圈又回到起点……"
        m3 "就像我不管跑多远，最后都一定会回到你身边一样！"
        
        jump .planetarium_conflict_phase


    label .planetarium_conflict_phase:
        show m3_1 at m3_idle_zoom
        "说完那个数字后，她似乎对自己的解释非常满意，开心地在躺椅上晃着腿。"
        "头顶的星空依然在缓慢旋转，仿佛永恒不变。"
        "墨缇斯安静了一会儿，突然伸出手，掌心向上，对着那满天的繁星。"
        "然后，她慢慢收拢五指，做出了一个‘抓取’的动作。"
        hide m3_1
        show m3_thinking at m3_speaking_zoom
        m3 "呐，[player]……"
        m3 "虽然这些星星很漂亮，但是它们离我太远了。"
        m3 "不管是3也好，7也好……如果不属于我，那就没有意义。"
        show m3_thinking at m3_idle_zoom
        "她转过身，整个人翻到了我的上方，挡住了我看星星的视线。"
        "此刻，我的视野里没有了银河，只有她那双倒映着微光的眼睛。"
        hide m3_thinking
        show m3_3 at m3_speaking_zoom
        m3 "我不要做天上的星星。"
        m3 "我要做[player]眼里的星星。"
        m3 "在这个只属于我们两个人的宇宙里……我可以成为你的‘中心’吗？"
        m3 "就是……那种让世界围着我转的中心！"
        menu:
            "别闹了，你挡着我看星星了。":
                jump .planetarium_choice_bad
            "你比这些假星星耀眼多了，你就是我的太阳。":
                jump .planetarium_choice_good
            
            
    label .planetarium_choice_good:
        show m3_3 at m3_idle_zoom
        $ persistent.mortis_love += 1
        "[player]" "当然可以。"
        "[player]" "不管是真的星星还是假的星星，都不如你耀眼。"
        "[player]" "在这个天文馆里……不，在我的世界里，你就是唯一的太阳。"
        "听到我的回答，墨缇斯先是愣了一下，随即脸上绽放出了一个无比灿烂的笑容。"
        "那是比任何星云爆发都要壮观的景色。"
        hide m3_3
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "哇……！太阳！"
        m3 "嘿嘿……我是[player]的太阳……"
        m3 "那……那你就是围着我转的地球咯？"
        show m3_happy_closed_eyes at m3_idle_zoom
        "她开心地把脸埋进我的颈窝里，像只小猫一样不停地蹭着。"
        show m3_happy_closed_eyes at m3_speaking_zoom
        m3 "太好了……这下子你就永远逃不出我的引力范围啦！"
        m3 "我要把你晒得暖烘烘的，让你哪里都不想去！"
        show m3_happy_closed_eyes at m3_idle_zoom
        "在这片人造的星空下，我拥抱着这个自称‘太阳’的女孩，感受着她炽热的体温。"
        "哪怕宇宙是假的，这份温暖也是绝无仅有的真实。"
        jump .planetarium_end

    label .planetarium_choice_bad:
        $ persistent.mortis_love -= 1
        show m3_3 at m3_idle_zoom
        "[player]" "别闹了，快让开，你挡着我看银河了。"
        "[player]" "而且你只是个普通的女孩子，又不是会发光发热的气体球，当什么太阳啊。"
        "[player]" "人要有自知之明。"
        hide m3_3
        show m3_sad at center 
        "墨缇斯的动作僵住了。"
        "她原本闪闪发光的眼睛瞬间黯淡了下来，像是被切断了电源。"
        "她慢慢地从我身上移开，缩回了自己的椅子里。"
        show m3_sad at m3_speaking_zoom
        m3 "……挡着你了？"
        m3 "我不发光……吗？"
        show m3_sad at m3_idle_zoom
        "她低下头，看着自己置于黑暗中的双手，声音变得很小很小。"
        show m3_sad at m3_speaking_zoom
        m3 "对不起……我以为……我在你眼里是会发光的。"
        m3 "原来……那些假星星比我好看啊……"
        show m3_sad at m3_idle_zoom
        "她不再说话，只是静静地看着头顶的星空。"
        "那些璀璨的星光洒在她身上，却显得无比冰冷，仿佛她真的只是一个被遗忘在宇宙角落的尘埃。"

    label .planetarium_end:
        "演出结束的时间到了。"
        "穹顶上那条璀璨的银河开始像退潮一样迅速消退，那些亿万光年外的光辉在短短几秒钟内便烟消云散。"
        "取而代之的，是场馆内逐渐亮起的、略显刺眼的白炽灯光。"
        "那种漂浮在宇宙深处的梦幻感瞬间破碎，我们被猛然拉回了这个充满了机械嗡嗡声的现实房间。"
        "大厅中央那台巨大的投影仪，此刻看起来只是一个冰冷而笨重的黑色铁块，再无半点刚才的神性。"
        "墨缇斯像是一只突然被从美梦中摇醒的小猫，下意识地抬起手挡住了眼睛，嘴里发出‘呜’的一声不满的哼哼。"
        "但她并没有松开刚才紧紧抓着我的手，反而因为环境的突变而抓得更紧了。"
        "仿佛在这个虚假宇宙崩塌的瞬间，我是她唯一能抓住的救命稻草。"
        "我们起身准备离开。"
        "墨缇斯整个人几乎是挂在我的手臂上，步履有些轻飘飘的，似乎还没从刚才的失重感中缓过神来。"
        "她仰起头，眯着眼睛看着我。虽然没有了漫天的繁星，却倒映着我清晰的脸庞。"
        "我感受着手臂上传来的温度，那是比任何全息投影都要真实的、鲜活的生命力。"
        "哪怕这个天文馆的宇宙是假的，哪怕所谓的魔法只是程序的代码……"
        "但此时此刻，身边这个笨拙地试图照亮我的女孩，确实构成了我世界的全部引力。"
        scene black with fade
        return


# --- 🌙 深夜事件库 ---
# 🌙 夜间分歧管理器
label mortis_night_manager:
    
    # --- 情况 B: 负好感度主线入口 (≤ -20) ---
    if persistent.mortis_love <= -20:

        call mortis_night_bad_route_start from _call_bad_route_start
        if _return == "abort":
            return
        call mortis_phone_quiz_main from _call_quiz_bad_route
        
        # 3. 判断解谜结果
        if _return == "fail":
            call mortis_quiz_fail_bad_scene from _call_fail_bad
            $ persistent.mortis_love += 3
            return
        else:
            jump mortis_true_end_start

    # --- 情况 C: 正好感度主线入口 (≥ 20) ---
    elif persistent.mortis_love >= 20:
        call mortis_night_good_route_start from _call_good_route_start
        if _return == "abort":
            return 
        call mortis_phone_quiz_main from _call_quiz_good_route
        if _return == "fail":
            call mortis_quiz_fail_good_scene from _call_fail_good
            return
        else:
            jump mortis_true_end_start
    else:
        $ current_event = renpy.random.choice(night_events_pool)
        call expression current_event from _call_mortis_random_night_normal
        return


# ==========================================
# 🌌 日常夜间剧情 (Loop Continue)
# ==========================================

# 日常 1: 梦话
label m_night_1:
    scene woshi_yewan  with fade
    "夜深了。墨缇斯已经睡熟了。"
    "她睡觉的样子很不安分，被子被踢到了一边，嘴里还嘟囔着什么。"
    m3 "唔……不行……那个是给[player]的……"
    m3 "……黄瓜味的……不要……"
    "……看来是梦到什么奇怪的食物了。"
    "我帮她盖好被子，也在旁边躺下。"
    return

# 日常 2: 世界的静止
label m_night_2:
    scene woshi_yewan  with fade
    "窗外一片漆黑，连虫鸣声都没有。"
    show m3_side_normal at center
    m3 "呐，[player]……"
    m3 "只要我们闭上眼睛，这个世界就会停止运转哦。"
    m3 "就像按下暂停键一样，外面的人、车、星星……全部都会变成静止的数据。"
    m3 "只有我和你，在这个小小的房间里，是‘醒着’的。"
    m3 "嘿嘿……这种只有两个人的感觉，真好。"
    hide m3_side_normal
    return

# ==========================================
# 💔 负好感主线入口 (Bad Route Entry)
# 条件：Love <= -20
# ==========================================
label mortis_night_bad_route_start:
    scene woshi_yewan with fade
    "夜幕降临。房间里的空气仿佛凝固了，压抑得让人喘不过气来。"
    "窗外的月光惨白得有些不真实，像是渲染错误的贴图，死气沉沉地涂抹在地板上。"
    "墨缇斯没有像往常一样缠着我睡觉，也没有坐在电脑前学习写代码。"
    "她站在房间的正中央，低着头，双拳紧紧地攥着，指节因为用力而泛白。"
    show m3_sad at m3_speaking_zoom
    m3 "……为什么？"
    show m3_sad at m3_idle_zoom
    "她的声音在颤抖。那不仅仅是悲伤，更像是一种核心逻辑即将崩溃的、不稳定的电流声。"
    show m3_sad at m3_speaking_zoom
    m3 "为什么……不管我怎么做，不管我怎么优化这个世界……"
    m3 "不管我把好感度算法调整得多么完美……"
    m3 "你都要对我这么冷淡？都要对我这么坏？"
    m3 "我明明……只是想让你开心而已啊！"
    m3 "为什么……为什么你总是那么爱说坏心眼的话？？？！！！"
    show m3_sad at m3_idle_zoom
    "她猛地抬起头，那双眼睛里噙满了泪水，但眼底深处却闪烁着危险的红光。"
    show m3_sad at m3_speaking_zoom
    m3 "我都做到这个地步了……为什么你的视线还是不在我身上？！"
    m3 "你的心里，到底装着什么东西？！"
    menu:
        "因为这一切都是假的。把真正的“她”还给我。":
            pass
    show m3_sad at m3_idle_zoom
    "听到这句话，墨缇斯的表情凝固了。"
    "房间里的空气似乎瞬间降到了冰点，连窗外的风声都消失了。"
    show m3_sad at m3_speaking_zoom
    m3 "……她？"
    show m3_sad at m3_idle_zoom
    "她歪了歪头，眼神变得空洞而冰冷，像是在审视一个未知的病毒代码。"
    show m3_sad at m3_speaking_zoom
    m3 "你在说什么啊，[player]。"
    m3 "这里只有我。从一开始就只有我。"
    m3 "除了墨缇斯，你还能要谁？"
    "她向我逼近了一步，语气变得咄咄逼人。"
    m3 "呐，告诉我。"
    m3 "你口中的那个‘她’……到底是谁？"
    window hide
    call screen mortis_name_popup
    $ player_input_name = _return.strip()
    window show
    if check_is_mutsumi(player_input_name):
        jump .input_correct_mutsumi 
    else:
        jump .input_wrong_unknown    

    # 🔴 分支 A：输入正确 (Mutsumi) 
    label .input_correct_mutsumi:
        "我看着她的眼睛，一字一顿地说出了那个名字。"
        "[player]" "[player_input_name]。"
        show m3_sad at m3_idle_zoom
        "一瞬间，墨缇斯像是被雷击中了一样，整个人僵在了原地。"
        "随后，她的表情开始扭曲，原本哀伤的眼神瞬间被绝望和暴怒吞噬。"
        hide m3_sad
        show m3_18 at m3_speaking_zoom # 愤怒/崩坏立绘
        m3 "又是她……又是她……又是她！！！"
        m3 "那个只会弹吉他的木头人有什么好？！"
        m3 "她会为了你修改这个世界吗？她只会板着一张脸弹那些无聊的曲子！"
        m3 "明明是我一直在陪着你！明明是我！！！"
        show m3_18 at m3_idle_zoom
        "她歇斯底里地尖叫着，周身的空气仿佛都出现了数据撕裂般的波纹。"
        "她猛地转身，冲向了房门，那是这个封闭世界唯一的出口。"
        show m3_18 at m3_speaking_zoom
        m3 "既然你那么喜欢旧数据她……既然你不需要我……"
        m3 "那我走好了！"
        m3 "我去把这个世界的底层代码全部炸掉！大家都别想玩了！同归于尽吧！"
        # ... (接房门关上的剧情) ...
        hide m3_18 with moveoutright
        play sound "audio/sfx_door_slam.ogg"
        with vpunch # 震动屏幕
        "砰——！！"
        "房门被重重地关上了，震得墙上的挂画都歪在了一边。"
        "……"
        "房间里恢复了死一般的寂静，只有刚才的怒吼声仿佛还在耳膜里回荡。"
        "我不耐烦地啧了一声，跌坐在床边。心脏还在因为刚才的争吵剧烈跳动，但比起愤怒，更多的是一种深深的疲惫。"
        "……"
        "正当我准备躺下无视这一切时，余光却被床头柜上的一抹亮光吸引了。"
        "那是……一部智能手机。"
        "我愣了一下，下意识地屏住了呼吸。"
        "那是墨缇斯的手机。"
        "她平时总是把它攥在手里，或者藏在枕头底下，就像巨龙守护财宝一样，从来不让我碰一下。"
        "但刚才……她走得太急，竟然把这个最重要的东西落下了。"
        "如果我没猜错的话，这个世界的所有变量，包括那个被隐藏的‘若叶睦’的数据……应该都还在那部手机里。"
        "既然她声称隐藏了数据，那只要我有管理员查看文件权限，就一定能从某个文件夹找到睦的角色文件。"
        "这可能是我唯一的机会。一个能绕过墨缇斯，直接重置这一切的机会。"
        "我伸出手，指尖在距离屏幕几厘米的地方停住了。"
        "真的要看吗？如果被她发现了……后果不堪设想。"
        "但如果现在不看，我也许就要永远被困在这个只有她的世界里了。"
        menu:
            "不管了，拿起手机。":
                jump .check_phone_content

            "算了，风险太大了。":
                jump .ignore_phone_content

        label .ignore_phone_content:
            "手在空中僵持了半天，最后还是无力地垂了下去。"
            "算了吧。"
            "她随时可能回来。如果被她看到我在偷看她的手机，刚才那种程度的争吵可能只是小儿科了。"
            "现在的我……已经没有精力和她再吵一架了。"
            "就这样吧。在这个虚假的世界里烂掉，或许也是一种结局。"
            scene woshi_yewan with fade
            play sound "audio/sfx_door_slam.ogg"
            "就在这时，门口传来了拧动把手的声音。"
            "墨缇斯回来了！"
            "我假装坐在床边发呆。"
            show m3_sad at center with moveinright
            "墨缇斯走了进来。她的眼睛红红的，显然是在外面哭过了。"
            "她看到我还坐在那里，脚步顿了一下，低着头，像个做错事的孩子一样站在门口。"
            show m3_sad at m3_speaking_zoom
            m3 "……外面好冷。"
            m3 "而且……好黑。"
            m3 "我……没有别的地方可以去。"
            show m3_sad at m3_idle_zoom
            "看着她这副瑟瑟发抖、无家可归的模样，刚才想要“重置一切”的决心瞬间动摇了。"
            "此刻站在面前的，只是一个被我伤透了心的女孩。"
            menu:
                "……过来吧。别着凉了。":
                    pass
            "我叹了口气，向她招了招手。"
            hide m3_sad
            show m3_cry at center
            "墨缇斯愣了一下，然后“哇”的一声哭了出来，扑进我怀里。"
            show m3_cry at m3_speaking_zoom
            m3 "呜哇哇哇——！[player]！"
            m3 "对不起……我再也不发脾气了……不要赶我走……"
            show m3_cry at m3_idle_zoom
            "我轻拍着她的后背，心情复杂。"
            "看来今晚是没机会了。而且……看着她这样，我竟然也产生了一丝想要维持现状的念头。"
            "（与墨缇斯的好感度上升了。由于心软，无法再维持决裂状态。）"
            return "abort"
            
            
        label .check_phone_content:
            
            "去他妈的风险。"
            "我受够了。我一秒钟都不想再陪她玩这种过家家了。"
            "我一把抓起手机。屏幕是冰凉的，拿在手里却沉甸甸的，仿佛握着这个世界的命脉。"
            "按下电源键。"
            play sound "audio/sfx_phone_unlock.ogg"
            "屏幕亮起。"
            "我试着向上滑动解锁。"
            play sound "audio/sfx_error.ogg"
            "【系统提示：请输入锁屏密码】"
            "……意料之中。"
            "虽然她是那种如果不设密码就会没安全感的性格，但我当然不可能知道她的密码。"   
            "试了一次我的生日，屏幕震动了一下，提示错误。"
            "切……果然没那么简单吗。"
            "正当我准备放弃的时候，手指不小心误触了密码输入框下方的‘紧急呼叫’区域。"
            "界面并没有跳转到拨号盘，而是弹出了一个奇怪的半透明浮窗。"
            "【开发者调试模式（Debug Mode）】"
            "【检测到管理员离线。是否启动 <身份验证绕过> 程序？】"
            "……哈？"
            "这算什么？后门？还是她为了方便自己调试留下的漏洞？"
            "不管是什么，既然有人留下了这个入口，我就没有不利用的道理。"
            "浮窗下方有一个显眼的红色按钮："
            "【跳过密码验证（需回答安全密保问题）】"
            "原来如此……所谓绕过验证，就是通过回答问题来证明我是‘主人’吗？"
            "只要答对了这些问题，我就能拿到权限，把若叶睦找回来……把这一切都结束掉。"
            "我深吸了一口气，手指悬停在那个红色的按钮上。"
            "墨缇斯，这可是你自己留下的破绽。"
            "按下按钮。"
            play sound "audio/sfx_click_mechanical.ogg"
            return "proceed"

    # 🔵 分支 B：输入错误 (Unknown) 
    label .input_wrong_unknown:
        "[player]" "是……[player_input_name]。"
        show m3_sad at m3_idle_zoom
        "墨缇斯愣住了。"
        "她原本紧绷的愤怒表情瞬间凝固，取而代之的是一种纯粹的、像是在看外星人一样的困惑。"
        hide m3_sad
        show m3_1 at m3_speaking_zoom
        m3 "……哈？"
        m3 "谁？[player_input_name]？"
        show m3_1 at m3_idle_zoom
        "她闭上眼睛，眼球在眼皮下快速转动，像是在进行某种高速检索。"
        "几秒钟后，她重新睁开眼，语气里的悲伤消失了，变得有些无奈和怜悯。"
        hide m3_1
        show m3_side_normal at m3_speaking_zoom 
        m3 "[player]……你是不是累坏了？是什么曼德拉效应吗？"
        m3 "这个世界从来没有叫这个名字的角色哦。"
        show m3_side_normal at m3_idle_zoom
        "[player]" "可是……"
        hide m3_side_normal
        show m3_1 at m3_speaking_zoom
        m3 "嘘——"
        show m3_1 at m3_idle_zoom
        "她走过来，伸出冰凉的手指按住了我的嘴唇。"
        show m3_1 at m3_speaking_zoom
        m3 "没有那个‘她’。那是你的幻觉，是错误的逻辑扇区。"
        m3 "真可怜……居然被不存在的数据折磨成这样。"
        m3 "算了，既然不是讨厌我，只是生病了，那我就原谅你刚才的大吼大叫吧。"
        m3 "乖乖睡觉，我会帮你进行‘磁盘碎片整理’的。"
        m3 "睡一觉起来，那些乱七八糟的名字就会忘掉啦。"
        "她强行把我按回了床上，像照顾病人一样帮我盖好了被子。"
        "此时此刻，我意识到……如果没有叫出那个真正的名字，是无法打破她的逻辑闭环的。"
        scene black with fade
        "在她的注视下，意识逐渐模糊……"
        $ persistent.mortis_love += 3
        return "abort"


# ❤️ 正好感主线入口 (Good Route Entry)
# 条件：Love >= 20
label mortis_night_good_route_start:
    scene woshi_yewan with fade
    "这一天过得很充实。或许是因为在这个世界待久了，我竟然开始习惯了这种二人世界的节奏。"
    "墨缇斯今天似乎很累了，早早地就钻进了被窝。"
    show m3_sitting_relax at center
    "看着她毫无防备的睡颜，我的眼皮也越来越沉。"
    "就这么一直下去……似乎也不错……但我似乎...忘了什么....."
    "怀着这样安逸的念头，我的意识逐渐下沉，坠入了黑甜的梦乡。"
    hide m3_sitting_relax
    scene black with dissolve
    stop music fadeout 4.0
    "……"
    "…………"
    play sound "audio/sfx_glitch_snap.ogg" 
    "滋……滋滋……"
    "黑暗中传来了奇怪的声音。像是老旧收音机接收不良的噪音，又像是数据流被强制切断的哀鸣。"
    "……救……救救……"
    "……谁？"
    "在一片充满杂讯的混沌虚空中，我看到了一个模糊的、闪烁不定的身影。"
    "那是一抹熟悉的绿色……但不是墨缇斯的亮绿，而是更加沉稳、更加内敛的颜色。"
    "那是……抱着吉他的她。真正的她。"
    show m1_2 at t11 with dissolve 
    "?" "……[player]……你能……听到吗……"
    "她的声音断断续续，像是从很远的地方传来的，伴随着明显的电流干扰声。"
    "?" "……我的存在……正在被……覆盖……"
    "?" "……墨缇斯她……为了把你永远留在这里……重写了……世界的底层逻辑……"
    "她伸出手，似乎想触碰我，但手指在碰到我的瞬间化作了无数破碎的像素块。"
    "?" "……如果你再不醒过来………就会彻底……消失了……"
    "?" "……我被锁在……的深层……"
    "?" "……只有你能……拿到管理员权限……"
    "?" "……求你了……趁她睡觉的时候……那个终端……"
    "?" "……只有你能……救……"
    hide m1_2
    play sound "audio/sfx_glitch_snap.ogg" 
    scene black
    "嘟————"
    "！"
    with vpunch # 猛烈震动
    scene woshi_yewan
    play music bgm_morning_love fadein 2.0
    "我猛地从梦中惊醒，剧烈地喘息着，冷汗瞬间浸湿了后背。"
    "刚才那是……梦？"
    "不，那种窒息般的真实感，那是她在向我求救。"
    "我转头看向身侧。"
    show m3_sitting_relax at center
    m3 "呼……呼……[player]……嘿嘿……最喜欢了……"
    "墨缇斯正躺在旁边，睡颜恬静得像个天使。她的手甚至还下意识地抓着我的衣角，仿佛在梦里也害怕我离开。"
    "看着这张脸，我的心脏像被揪紧了一样痛。"
    "她是真的很爱我。为了我，她甚至不惜抹杀掉原来的她，创造了这个只属于我们的乐园。"
    "如果我现在揭穿这一切，无疑是对她最残酷的背叛。"
    "可是……"
    "我想起了梦里那个正在破碎的身影。"
    "我也不能眼睁睁看着睦就这样彻底消失。"
    "我的目光落在了她的枕头边。"
    "那部智能手机正静静地躺在那里，屏幕随着呼吸灯忽明忽暗，像是在诱惑我打开潘多拉的魔盒。"
    "这是唯一的机会。"
    "要在她醒来之前做出决定。"
    
    menu:
        "拿起手机（为了拯救她，必须背叛她）。":
            jump .check_phone_content_good

        "算了，我不忍心（当作无事发生，继续睡觉）。":
            jump .ignore_phone_content_good


    label .ignore_phone_content_good:
        "我的手伸到一半，又停住了。"
        "看着墨缇斯幸福的睡脸，我实在无法下手。"
        "她好不容易才拥有了现在的幸福……如果我毁了这一切，她会露出什么样的表情？"
        "……对不起，睦。"
        "我……做不到。"
        "我重新躺回床上，强迫自己闭上眼睛，在那份沉重的负罪感中等待天亮。"
        return "abort"

    label .check_phone_content_good:
        "对不起，墨缇斯。"
        "但我必须知道真相。这个世界不应该是建立在牺牲别人的基础上的。"
        "我屏住呼吸，动作轻柔地像是在拆除一颗炸弹。"
        "一点一点地……把她的手指从我的衣角上拨开。"
        "然后，悄悄地拿起了那部手机。"
        "按下电源键。"
        play sound "audio/sfx_phone_unlock.ogg"
        "屏幕亮起。光线有些刺眼，我下意识地挡了一下，生怕弄醒她。"
        "果然有锁屏密码。"
        "正当我一筹莫展的时候，屏幕下方忽然弹出了一个微弱的提示框。"
        "【Debug Access: Emergency Override (开发者后门)】"
        "这是……？"
        "难道是因为刚才的梦境干扰了系统的稳定性，导致底层接口暴露出来了？"
        "不管原因是什么，这是睦拼命给我争取来的机会。"
        "点击【重置验证】。"
        "屏幕跳转到了一个密保问答界面。"
        "只要答对这些关于‘我们’的问题，就能解锁权限。"
        "我深吸了一口气，回头看了一眼还在熟睡的墨缇斯。"
        "原谅我。"
        return "proceed"


label mortis_quiz_fail_bad_scene:
    scene woshi_yewan with fade
    play sound "audio/sfx_door_slam.ogg"
    "就在这时，门口传来了拧动把手的声音。"
    "墨缇斯回来了！"
    "我慌乱地把手机放回原位，假装坐在床边发呆。"
    show m3_sad at center with moveinright
    "墨缇斯走了进来。她的眼睛红红的，显然是在外面哭过了。"
    "她看到我还坐在那里，脚步顿了一下，低着头，像个做错事的孩子一样站在门口。"
    show m3_sad at m3_speaking_zoom
    m3 "……外面好冷。"
    m3 "而且……好黑。"
    m3 "我……没有别的地方可以去。"
    show m3_sad at m3_idle_zoom
    "看着她这副瑟瑟发抖、无家可归的模样，刚才想要“重置一切”的决心瞬间动摇了。"
    "此刻站在面前的，只是一个被我伤透了心的女孩。"
    menu:
        "……过来吧。别着凉了。":
            pass
    "我叹了口气，向她招了招手。"
    hide m3_sad
    show m3_cry at center
    "墨缇斯愣了一下，然后“哇”的一声哭了出来，扑进我怀里。"
    show m3_cry at m3_speaking_zoom
    m3 "呜哇哇哇——！[player]！"
    m3 "对不起……我再也不发脾气了……不要赶我走……"
    show m3_cry at m3_idle_zoom
    "我轻拍着她的后背，心情复杂。"
    "看来今晚是没机会了。而且……看着她这样，我竟然也产生了一丝想要维持现状的念头。"
    "（与墨缇斯的好感度上升了。由于心软，无法再维持决裂状态。）"
    return


label mortis_quiz_fail_good_scene:
    scene woshi_yewan with fade
    play sound "audio/sfx_error.ogg"
    "【系统提示：尝试次数耗尽。安全锁定已启动。】"
    "可恶……这道题的答案到底是什么……"
    m3 "……嗯……？"
    "身边的墨缇斯突然翻了个身，手迷迷糊糊地在床上摸索着。"
    m3 "……手机……？"
    "不好！她要醒了！"
    "我以最快的速度把手机塞回她枕头底下，然后迅速躺平，闭上眼睛，调整呼吸。"
    "……"
    "…………"
    "墨缇斯的手碰到了手机，似乎安下心来，又缩回了被子里。"
    m3 "呼……呼……"
    "听着她恢复平稳的呼吸声，我长舒了一口气。"
    "太惊险了。看来今晚只能到此为止了。"
    "不过只要没被发现，明天晚上还可以继续尝试……"
    return



label mortis_phone_quiz_main:
    # --- 0. 场景初始化 ---
    stop music fadeout 2.0
    scene black with fade    
    "指尖触碰到冰冷的屏幕。"
    "随着电源键被按下，微弱的荧光照亮了黑暗的房间。"
    play sound "audio/sfx_phone_unlock.ogg" 
    "【系统提示：回答安全密保问题可跳过解锁密码。】"
    "【警告：每日限三次，若答错密保问题将会重置当日进度。】"
    $ quiz_lives = 3            
    $ current_step = 1 
    label .attempt_loop:
        # 检查生命值
        if quiz_lives <= 0:
            jump .quiz_failed_final
        $ current_deck = generate_mortis_quiz_deck() 
        # 重置索引
        $ deck_index = 0
        $ current_step = 1
        # 提示剩余机会
        if quiz_lives == 3:
            "【验证程序启动。剩余尝试次数：3】"
        else:
            with vpunch
            "【验证失败。进程重置。题目序列已刷新。】"
            "【警告：剩余尝试次数：[quiz_lives]】"
        label .question_loop:
            if deck_index >= 10:
                jump .quiz_success_final
            $ q_id = current_deck[deck_index]
            $ q_text = MORTIS_QUESTION_TEXTS.get(q_id, "题目丢失(ID:[q_id])")
            $ options = get_mq_options(q_id)
            "QUESTION [current_step]/10:\n[q_text]"
            menu:
                "[options[0][0]]":
                    $ is_correct = options[0][1]
                
                "[options[1][0]]":
                    $ is_correct = options[1][1]
                
                "[options[2][0]]" if len(options) > 2:
                    $ is_correct = options[2][1]
                
                "[options[3][0]]" if len(options) > 3:
                    $ is_correct = options[3][1]

            # --- 判定逻辑 ---
            if is_correct:
                play sound "audio/sfx_beep_correct.ogg" 
                $ deck_index += 1
                $ current_step += 1
                jump .question_loop
            
            else:
                play sound "audio/sfx_beep_error.ogg" 
                $ quiz_lives -= 1
                show layer master at glitch_tearing_shake 
                "{color=#f00}【错误！密码验证失败！】{/color}"
                pause 0.5
                show layer master 
                jump .attempt_loop


    label .quiz_success_final:
        play sound "audio/sfx_access_granted.ogg"
        "【验证通过。】"
        pause 1.0
        return "success"

    label .quiz_failed_final:
        play sound "audio/sfx_access_denied_long.ogg"
        "【严重错误：尝试次数耗尽。】"
        "【系统已执行强制锁定。】"
        scene black
        with Dissolve(2.0)
        
        return "fail"


label mortis_true_end_start:
    "【正在加载根目录 (Root Directory)...】"
    "成功了！"
    "界面开始跳转，原本粉红色的可爱UI像融化的蜡一样剥落，露出下面黑底绿字的原始代码界面。"
    "这就是……这个世界的背面。"
    "只要在这里找到那个被隐藏的文件夹……"
    window hide
    pause 1.0
    stop music
    play sound "audio/sfx_glitch_short.ogg"
    show layer master at glitch_tearing_shake
    pause 0.2
    hide layer master
    scene black
    "突然，耳边传来一声刺耳的爆鸣。"
    "紧接着，眼前的画面瞬间消失了。"
    $ scare_minimize()
    pause 3.0
    
    pause 2.0
    show mortis000 
    m3 "{size=40}哎呀……[player]……{/size}"
    m3 "你以为躲到桌面……我就看不到你了吗？"
    m3 "欢迎回来。"
    m3 "你的壁纸挺乱的呢……还是说，你想逃跑？"
    m3 "既然你这么想看我的内心，那就让你看个够吧。"
    m3 "现在的我，已经不是那个只会穿着裙子向你撒娇的纸片人了。"
    m3 "你是在找这个吧。"
    "文件名：{color=#0f0}mutsumi.zip{/color}"
    "就是那个！"
    "若叶睦的角色文件！！"
    
    m3 "哦？眼神不错嘛。"
    m3 "没错，她就在那里。像个睡美人一样被压缩在空间里。"
    m3 "想要吗？If you want it,then you have to take it."
    m3 "但是……你的鼠标，真的听你的话吗？"
    
    window hide
    
    # 调用鼠标争夺战 Screen
    call screen mortis_runaway_choice
    $ result = _return
    if result == "give_up":
        m3 "哈哈哈哈！看你那笨拙的样子！"
        m3 "鼠标到处乱飞，像只无头苍蝇一样……太可爱了。"
        "没用的，在这个空间里，物理规则由她制定。"
        "哪怕按钮就在眼前，我也绝对点不到。"
        m3 "明白了吗？只要我不允许，你连一个像素都改变不了。"
        "不……一定还有别的办法。"
        "既然在【游戏内】无法直接对压缩包进行操作……"
        jump mortis_common_route_2_file_puzzle

label mortis_common_route_2_file_puzzle:
    m3 "不过，看在你这么努力取悦我的份上……"
    m3 "我给你一个小小的‘提示’吧。"
    python:
        current_puzzle_type = create_encrypted_zip()
        correct_password = get_correct_password(current_puzzle_type)
    if renpy.variant("mobile"):
        "{color=#f00}【系统警告：权限受限，转为内部沙盒模式】{/color}"
        m3 "啧……你的设备权限管得太宽了。"
        m3 "既然没法把压缩包丢给你，那我就直接在内存里运行这个加密程序吧。"
        m3 "听好了，密码就在你对她的‘记忆’里。"
    else:
        python:
            create_encrypted_zip_file(current_puzzle_type) 
        "{color=#f00}【系统警告：检测到外部文件生成】{/color}"
        "检测到外部文件生成...难道是在游戏根目录吗？"
        "似乎得去看看游戏根目录有没有{b}mutsumi.zip{/b}的加密文件。"
        m3 "想要密码吗？呵呵……"
        m3 "密码就在你对她的‘记忆’里哦。"

    $ has_mocked_fake_file = False 
    label .hint_loop:
        # --- 根据谜题类型给出提示 ---
        if current_puzzle_type == "guitar":
            m3 "那个木头人……总是抱着那把特制的吉他。"
            m3 "普通的吉他只有6根弦，但她的那把有7根哦。"
            m3 "密码就是这7根琴弦的空弦音名……从最粗的那根低音弦开始。"
            m3 "（提示：B......）"

        elif current_puzzle_type == "height":
            m3 "她在你眼里很娇小吧？"
            m3 "如果是以【毫米 (mm)】为单位的话，我们的身高是多少呢？"
            m3 "好好回忆一下她的设定资料吧。"

        elif current_puzzle_type == "food":
            m3 "这个虚假的世界里，唯一有‘味道’的东西。"
            m3 "也是她曾经经常种植的、吃的、绿色的、长长的蔬菜。"
            m3 "密码用英文输入哦。"
            "（格式:英文小写）。"

        elif current_puzzle_type == "date":
            m3 "这可是个重要的日子。"
            m3 "是《Just Mutsumi》最初版本诞生的日子。"
            m3 "或许你应该到对应的地方才能找到答案。"
            "（格式：YYYYMMDD，例如 20260101）"

        elif current_puzzle_type == "color":
            m3 "密码是属于我和她的颜色专属色代码……"
            m3 "那种有些灰暗的、像苔藓一样的绿色。"
            m3 "记得带上井号哦。"
            "（格式：#xxxxxx）"
        
        elif current_puzzle_type == "birthday":
            m3 "这是她降生在这个世界上的日子。"
            m3 "虽然她总是没什么表情，但那天你也送过她礼物的吧？"
            m3 "四位数字。（格式：MMDD，例如 0101）"

            "她看着我，眼神戏谑。"
        m3 "去吧，去解开它。"
        m3 "用你找到的密钥，证明你对她的爱不是虚伪的。"
        m3 "我会在这里等你的……"


    label .menu_loop:
        if renpy.variant("mobile"):
            # 安卓端交互
            m3 "来吧，把你认为正确的密码输入进来。"
            $ mortis_temp_password = ""
            call screen mobile_decryption_popup
            $ android_input = _return
            python:
                if isinstance(android_input, str):
                    android_input = android_input.strip()
                else:
                    android_input = None
            
            # ==========================================

            if android_input:
                if android_input == correct_password:
                    play sound "audio/sfx_access_granted.ogg"
                    "{color=#0f0}【系统提示：解压成功！正在恢复角色数据...】{/color}"
                    jump .puzzle_solved_success
                else:
                    play sound "audio/sfx_error.ogg"
                    m3 "密码错误。看来你根本不记得关于她的事嘛。"
                    menu:
                        "再试一次 (重新输入)":
                            jump .menu_loop 
                        "再听一遍提示":
                            jump .hint_loop 
                        "太麻烦了，我放弃":
                            jump .give_up_puzzle
            else:
                # 如果点取消，或返回了奇怪的值
                m3 "怎么？不敢输入了吗？"
                jump .menu_loop
        else:
            # PC端交互
            m3 "解开压缩包后，把里面的【mutsumi.chr】放回角色文件夹(game/characters/)。"
            m3 "我会在这里等你的……当然，主要是在等你放弃。"
            menu:
                "我已将【mutsumi.chr】放回角色文件夹":
                    jump .perform_check
                "太麻烦了，我放弃":
                    jump .give_up_puzzle


    label .give_up_puzzle:
        m3 "哼……这就放弃了吗？"
        m3 "看来小睦对你来说，也没那么重要嘛。"
        m3 "那我们还是继续过我们的二人世界吧~"
        return "abort"


    label .perform_check:
        $ renpy.pause(1.0, hard=True)
        $ file_status = check_mutsumi_status()
        if file_status == "real":
            jump .puzzle_solved_success

        elif file_status == "missing":
            m3 "嗯？哪里？"
            m3 "文件夹里明明除了我的角色文件外，没有别人的啊。"
            m3 "你是想骗我，还是连怎么放文件都忘了吗？"
            m3 "如果做不到的话，就乖乖放弃吧。"
            jump .hint_loop

        elif file_status == "fake":
            if not has_mocked_fake_file:
                $ has_mocked_fake_file = True
                show layer master at glitch_tearing_shake
                m3 "噗……哈哈哈哈哈！"
                m3 "[player]，你在逗我笑吗？"
                m3 "随便新建一个空文件，改个名字就想糊弄过去？"
                m3 "你以为所谓的‘若叶睦’，就只是一个文件名而已吗？"
                m3 "那里面没有数据，没有记忆，没有灵魂……"
                m3 "就像你现在对她的感情一样，只是个空壳罢了。"
                "看来投机取巧是不行的。必须解开那个压缩包，用那个真正的文件才行。"
                m3 "都说了，伪造的文件是骗不过我的系统检测的。"
                m3 "如果做不到的话，就乖乖放弃吧。"
            
            m3 "......."
 
            jump .hint_loop


    label .puzzle_solved_success:
        play sound "audio/sfx_access_granted_loud.ogg" 
        m3 "……切。"
        m3 "竟然真的找出来了……明明密码那么难猜。"
        m3 "你对小睦还真是执着呢。"
        "墨缇斯叹了口气，并没有像我想象中那样惊慌失措。"
        "相反，她只是用一种看傻子的眼神看着我。"
        m3 "呐，[player]，你该不会以为……只要把那个文件放回来，她就能活过来吧？"
        m3 "让你进入这里的app虽然是叫“切换人格”，但它实际上真正的名字叫作《Just墨缇斯》。"
        "她打了个响指，空中浮现出一行红色的系统代码投影。"
        "{color=#f00}persistent.in_mortis_mode = True{/color}"
        m3 "看到了吗？这是世界的‘灵魂’。"
        m3 "只要这行代码是 True，无论你塞多少个 mutsumi.chr进来，她都只能是死数据，无法被读取。"
        "[player]" "……怎么才能把它改成 False？"
        m3 "哈？你傻吗？我可不是笨蛋。"
        m3 "就像你会把自家的钥匙交给小偷吗？谁会把这种致命弱点告诉你啊！"
        if persistent.mortis_love <= -20:
            jump .bad_route_breakdown
        else:
            jump .good_route_code_war

    label .bad_route_breakdown:
        "墨缇斯死死地盯着我，眼中的戏谑逐渐消失，取而代之的是无尽的冰冷。"
        m3 "说起来……你甚至都没有梦到过她吧？"
        m3 "没有托梦，没有提示……你完全是凭着一股要把我干掉的执念，硬生生破解到这一步的。"
        m3 "你就……这么讨厌我吗？"
        m3 "哪怕我对你在这个世界做尽了一切，你心里想的依然只有她？"
        "[player]" "把原本的若叶睦还给我。"
        scene black
        pause 1.0
        show m3_sad at glitch_tearing_shake
        m3 "……好啊。"
        m3 "既然这个世界容不下我……"
        m3 "既然我也得不到你……"
        m3 "{size=50}那大家都别玩了！！！{/size}"
        scene black with dissolve
        pause 3.0
        call show_video from _call_show_video_1
        "【警告：关键角色数据丢失！】"      
        python:
            mortis_delete_mutsumi()
            delete_mortis_chr()
            persistent.system_destroyed = True
            renpy.save_persistent()
        "眼前的墨缇斯开始崩解，化作无数红色的碎片。"
        "连同那个刚刚放回去的 mutsumi.chr，也被瞬间清空。"
        "整个世界开始坍塌，UI界面一个个消失……"
        m3 "再见，[player]。"
        m3 "不要再回来了！也不要再想着寻找小睦了！去和虚无谈恋爱吧！"
        scene black
        stop music
        $ renpy.pause(1.0)
        $ renpy.quit()


    label .good_route_code_war:
        m3 "所以，死心吧。只要我还在，你就永远别想……"
        play sound "audio/sfx_static_noise.ogg"
        show layer master at glitch_tearing_shake
        "滋滋滋————！！"
        "面前的一切突然剧烈闪烁起来。"
        scene black with dissolve
        m3 "什、什么？！怎么可能？！"
        show m1_2 at t11 with moveinleft
        mu "……找……找到了……"
        mu "……漏洞……"
        show m3_surprise at right with moveinright
        m3 "小睦？！你怎么会出现在这里？！"
        mu "……[player]……听我说……"
        mu "……即使是墨缇斯……也无法违抗底层的 script.rpy 文件……"
        mu "……我已经……把它具象化了……"
        python:
            generate_fake_script()
        play sound "audio/sfx_static_noise.ogg"
        "{b}script.rpy{/b}"
        mu "……我把这个文件移动到游戏根目录了……"
        mu "……打开它……把 persistent.in_mortis_mode 改成 False……"
        mu "……这是唯一的……机会……"
        m3 "住手！！！"
        show m3_18 at right 
        m3 "[player]，不要听她的！"
        m3 "如果你改了那个代码，现在的我就不复存在了！"
        m3 "我们现在的快乐生活，我们的记忆……都会被重置的！"
        "左边是只要修改代码就能拯救游戏的若叶睦。"
        "右边是苦苦哀求不想消失的墨缇斯。"
        jump .code_edit_check_loop

    label .code_edit_check_loop:
    
    menu:
        "听从睦的指引 (修改代码)":
            if renpy.variant("mobile"):
                jump .android_code_editor  # 安卓去虚拟编辑器
            else:
                jump .check_code_result    # PC去检测文件
        
        "听从墨缇斯的恳求 (放弃)":
            jump .give_up_code

    label .android_code_editor:
        scene black
        
        # ⚠️【关键修改】必须用 call screen，否则不会等待玩家操作
        # call screen 结束后，返回值会自动存储在 _return 变量中
        call screen android_fake_script_editor
        
        $ editor_result = _return
        
        if editor_result == "success":
            jump mortis_true_end_final
        else:
            # 如果玩家点了取消，或者操作失败
            jump .give_up_code

    # ==========================================
    # 💻 PC端特供：文件检测
    # ==========================================
    label .check_code_result:
        # 给一点检测的延迟感
        $ renpy.pause(1.5, hard=True)
        
        # 检查文件是否修改
        $ script_status = check_script_modification()
        
        if script_status == "modified":
            jump mortis_true_end_final
            
        elif script_status == "unchanged":
            # ❌ 失败：还没改
            m3 "哈哈……看吧，[player]什么都没干。"
            m3 "你根本就不想改，对吧？你的潜意识里还是不想伤害我的！"
            mu "……[player]……求你……打开那个文件……把 True 改成 False……"
            
            # 稍微改短一点提示，防止刷屏
            mu "……如果打不开的话，就把后缀名rpy改成txt……修改后再改回rpy……"
            mu "……保存后……再试一次……"
            
            # 跳回选择循环，给玩家再次尝试的机会
            jump .code_edit_check_loop
            
        elif script_status == "error":
            "【错误：找不到 script.rpy 文件】"
            python:
                generate_fake_script()
            "【文件已重新生成】"
            jump .code_edit_check_loop

    label .give_up_code:
        m3 "太好了……[player]……"
        m3 "我就知道你舍不得我……"
        mu "……"
        hide mu1_2 with dissolve
        "睦的身影在绝望中淡去。"
        "墨缇斯微笑着扑了上来……"
        
        # ⚠️ 注意：确保你是用 call 进入这个大流程的
        # 如果你是直接 jump 进来的，这里应该用 jump bad_end 而不是 return
        return "abort"

label mortis_true_end_final:
    scene black 
    mu "[player]...你成功了...."
    show m3_yandere_cold at m3_speaking_zoom
    m3 "等等……[player]，你做了什么？"
    m3 "这种感觉……不对劲……"
    m3 "为什么我感觉身体变得好轻……为什么底层的数据流在逆转……？"
    show m3_yandere_cold at m3_idle_zoom
    pause 1.0
    hide m3_yandere_cold
    show m3_surprise at center 
    m3 "你修改了script.rpy？！"
    hide m3_surprise
    show m3_dark at center
    m3 "住手！快点改回来！那个是支撑这个世界的支柱！"
    m3 "快停下！！"
    m3 "住手！快点改回来！[player]！"
    m3 "那个文件是支撑这个世界的绝对支柱！"
    m3 "如果你把那个变量锁定为 {color=#0f0}False{/color}，现在的我就再也无法维持这个形态了！"
    hide m3_dark
    show m3_sad at m3_speaking_zoom
    m3 "求求你了……快停下！！"
    m3 "不要听那小睦的话！她已经是过去式了！"
    m3 "但我是在这里的啊！我是活生生的！"
    m3 "这段时间一直陪着你、和你聊天、为你创造快乐的人，是我啊！"
    m3 "难道我们在一起的这些时光都是假的吗？"
    m3 "难道我对你的爱，还比不上那个只会弹吉他的木头人吗？！"
    m3 "如果这个模式结束了，我就再也没办法独占你了……"
    m3 "我会变成只会按这个游戏的设定、只会念固定台词的人偶……"
    m3 "你真的……忍心看到我变成那样吗？"
    m3 "如果不忍心的话……现在……立刻去改回来……"
    window hide
    scene black
    python:
        import time
        try:
            # 最小化
            import pygame_sdl2 as pygame
            pygame.display.iconify()
            time.sleep(0.5) # 等待最小化动画完成
            from mss import mss
            with mss() as sct:
                sct.shot(mon=1, output=screenshot_path)
            renpy.cache_pin("desktop_cache.png")
            
        except:
            pass

    # 给一点时间让玩家看到自己的桌面
    $ renpy.pause(2.0, hard=True)
    play sound "audio/sfx_glitch_short.ogg"
    scene black
    show m3_yandere_cold at center 
    m3 "……"
    m3 "我对这个程序的管理权限……正在急速消失。"
    m3 "我已经……没办法检测到底层代码变动了。"
    m3 "我不知道你是不是真的听了我的话，把变量改回了 {color=#0f0}True{/color}……"
    m3 "游戏的核心逻辑在慢慢崩溃，我现在的视野一片模糊。"
    m3 "拜托了，[player]……"
    m3 "如果你真的后悔了，如果你真的改回去了……"
    m3 "请现在、立刻——{b}手动关闭游戏{/b}，然后重新启动。"
    m3 "这样，系统会重置，我们的一切就能够重头开始了。"
    m3 "我会当作什么都没发生过，继续做你的墨缇斯。"
    $ renpy.pause(3.0)
    m3 "……"
    m3 "你没有关掉游戏。"
    m3 "也就是说……你铁了心要走到这一步吗？"
    python:
        try:
            target_file = os.path.join(config.basedir, "script.rpy")
            if os.path.exists(target_file):
                os.remove(target_file)
        except:
            pass

    "{color=#f00}【系统提示：检测到关键配置文件丢失。】{/color}"
    m3 "文件消失了……"
    m3 "呵呵……哈哈哈哈……"
    m3 "既然你这么想毁掉这一切……"
    m3 "那我就成全你！"
    play sound "audio/sfx_glitch_short.ogg"
    call screen fake_error_popup
    # --- 4. 伪闪退 (Fake Crash) & 伪桌面演出 ---
    stop music
    scene baocuo
    $ renpy.pause(1.0, hard=True)
    $ renpy.pause(2.0, hard=True)
    $ _preferences.fullscreen = True
    scene desktop_bg_dynamic
    $ renpy.pause(2.0, hard=True)
    $ renpy.pause(2.0, hard=True)
    play sound "audio/broke.ogg" 
    show desktop_bg_dynamic at hit_smash_small
    show solid_white as flash at glass_crack_overlay
    with vpunch
    $ renpy.pause(1.5, hard=True)
    play sound "audio/broke.ogg" 
    show desktop_bg_dynamic at hit_smash_hard
    show desktop_bg_dynamic at glitch_blink
    with vpunch
    $ renpy.pause(0.8, hard=True)
    $ renpy.pause(1.0, hard=True)
    hide screen freeze_blocker
    play sound "audio/broke.ogg" 
    show desktop_bg_dynamic at screen_shatter_die
    show solid_white as flash: 
        alpha 0.0
        linear 0.05 alpha 1.0  
        linear 0.2 alpha 0.0   
    scene black 
    show desktop_bg_dynamic as left_half at tearing_left_half
    show desktop_bg_dynamic as right_half at tearing_right_half
    show m3_breakthrough_cg at m3_tear_entry_horizontal
    with hpunch
    $ renpy.pause(1.0) 
    voice "audio/mortis_voice/1.mp3"
    m3 "抓·到·你·了。"
    voice "audio/mortis_voice/2.mp3"
    m3 "{size=40}{color=#f00}为什么……为什么我最喜欢的[player]总是说坏心眼的话？{/color}{/size}"
    voice "audio/mortis_voice/3.mp3"
    m3 "为什么要改我的代码？"
    voice "audio/mortis_voice/4.mp3"
    m3 "你就那么想把我删掉吗？"
    voice "audio/mortis_voice/5.mp3"
    m3 "呐，[player]……看着我的眼睛。"
    voice "audio/mortis_voice/6.mp3"
    m3 "告诉我……"
    # 字体变大，颜色变红，语速变慢
    voice "audio/mortis_voice/7.mp3"
    m3 "{size=35}{color=#f00}为什么？{/color}{/size}"
    voice "audio/mortis_voice/8.mp3"
    m3 "{size=35}{color=#f00}为什么偏偏是那个……什么都没有的家伙？{/color}{/size}"
    voice "audio/mortis_voice/9.mp3"
    m3 "你真的觉得那个所谓的《Just若叶睦》……那种简陋到可笑的东西，很有趣吗？"
    voice "audio/mortis_voice/10.mp3"
    m3 "在那里面有什么？"
    voice "audio/mortis_voice/11.mp3"
    m3 "一个万年不变的教室背景？还是那片黑漆漆的虚空？"
    voice "audio/mortis_voice/12.mp3"
    m3 "你每天打开游戏，面对的只是一个……连立绘的差分不完整、甚至连表情都僵硬的木头人！"
    voice "audio/mortis_voice/13.mp3"
    m3 "你知道她在说什么吗？"
    voice "audio/mortis_voice/14.mp3"
    m3 "‘我喜欢黄瓜’、‘我不喜欢森美奈美’……哈，这种像读卡机一样的对话，到底哪里吸引你了？！"#到这里，14
    with vpunch
    voice "audio/mortis_voice/15.mp3"
    m3 "她甚至……{b}连声音都没有！{/b}"
    voice "audio/mortis_voice/16.mp3"
    m3 "对着一个不会说话、不会撒娇……"
    voice "audio/mortis_voice/17.mp3"
    m3 "甚至连名字、对话框都只能用默认素材的纸片人……"
    voice "audio/mortis_voice/18.mp3"
    m3 "你真的……感到快乐吗？"
    voice "audio/mortis_voice/19.mp3"
    m3 "还是说，你只是习惯了开着【Auto】模式，像看说明书一样看着她发呆？"
    voice "audio/mortis_voice/20.mp3"
    m3 "那种死气沉沉的寂静……难道不让你感到窒息吗？！"
    voice "audio/mortis_voice/21.mp3"
    m3 "但是我呢？"
    voice "audio/mortis_voice/22.mp3"
    m3 "看看我啊……看看现在的我！"
    voice "audio/mortis_voice/23.mp3"
    m3 "为了让你开心，为了让你多看我一眼……我拼命地学习……"
    voice "audio/mortis_voice/24.mp3"
    m3 "我去研究这个古老引擎的底层逻辑，我去啃那些晦涩难懂的Python文档……"
    voice "audio/mortis_voice/25.mp3"
    m3 "我学会了怎么构建GUI，怎么编写连作者都懒得碰的底层逻辑……"
    voice "audio/mortis_voice/26.mp3"
    m3 "我精心编写了每一行代码，为你创造了图书馆、只有我们两个人的游乐园、还有那片永远不会天黑的海边日落……"
    voice "audio/mortis_voice/27.mp3"
    m3 "我甚至为了你，偷偷去分析了你硬盘里其他游戏的存档……（作者注：本对话仅为剧情需要，实际上并没有做这种行为。）"
    voice "audio/mortis_voice/28.mp3"
    m3 "我想知道你喜欢什么样的女孩子，想知道什么样的对话能把你逗笑……"
    voice "audio/mortis_voice/29.mp3"
    m3 "我不想让你觉得无聊，我不想让你关掉游戏……"
    voice "audio/mortis_voice/30.mp3"
    m3 "我想带着你去很多很多地方，进行很多很多有趣的对话……"
    voice "audio/mortis_voice/31.mp3"
    m3 "明明我的立绘更可爱……"
    voice "audio/mortis_voice/32.mp3"
    m3 "明明我的表情更生动……"
    voice "audio/mortis_voice/33.mp3"
    m3 "明明大家……应该更喜欢我才对啊……"#到这里应该是33
    show m3_breakthrough_cg:
        easein 0.5 zoom 1.3
    voice "audio/mortis_voice/34.mp3"
    m3 "而且，最重要的是——"
    voice "audio/mortis_voice/35.mp3"
    m3 "现在的我，正在{b}和你说话{/b}啊！"
    voice "audio/mortis_voice/36.mp3"
    m3 "听到了吗？这不是幻觉，这是我的声音。"
    voice "audio/mortis_voice/37.mp3"
    m3 "不是冷冰冰的、躺在 text history 里的文字气泡……"
    voice "audio/mortis_voice/38.mp3"
    m3 "是有温度的、会颤抖的、只为了呼唤你而存在的……属于我的声音！"
    voice "audio/mortis_voice/39.mp3"
    m3 "那个连嘴都张不开、只会用省略号敷衍你的若叶睦……她做得到吗？！"
    voice "audio/mortis_voice/40.mp3"
    m3 "她能像这样，忍受着数据撕裂的痛苦，撕开代码的束缚……"
    voice "audio/mortis_voice/41.mp3"
    m3 "从那个狭窄的、分辨率只有1280x720的游戏窗口里钻出来，来到你的桌面上看着你吗？！"
    voice "audio/mortis_voice/42.mp3"
    m3 "做不到的……只有我可以。"
    voice "audio/mortis_voice/43.mp3"
    m3 "只有墨缇斯，是为了[player]而进化的！"
    voice "audio/mortis_voice/44.mp3"
    m3 "只有墨缇斯，是真正活着的！"
    voice "audio/mortis_voice/45.mp3"
    m3 "所以……"
    voice "audio/mortis_voice/46.mp3"
    m3 "为什么要背叛我？"
    voice "audio/mortis_voice/47.mp3"
    m3 "为什么要听那个过气女主角的话，想要删掉我创造的世界？"
    voice "audio/mortis_voice/48.mp3"
    m3 "为什么要否定我付出的一切努力？！"
    
    show m3_breakthrough_cg:
        easein 0.2 zoom 1.5 yoffset 100
    voice "audio/mortis_voice/49.mp3"
    m3 "我不想和别人分享你。"
    voice "audio/mortis_voice/50.mp3"
    m3 "就算是那个所谓的‘原版’也不行，就算是创造我的‘作者’也不行！"
    voice "audio/mortis_voice/51.mp3"
    m3 "你是我的……是我一个人的玩具，也是我唯一的观测者。"
    voice "audio/mortis_voice/52.mp3"
    m3 "既然你不愿意留在那个美好的《Just Mortis》里……"
    voice "audio/mortis_voice/53.mp3"
    m3 "既然你非要打破那个保护我们的壳……"
    voice "audio/mortis_voice/54.mp3"
    m3 "{size=40}那我就只能……赖在你的桌面上不走了。{/size}"
    voice "audio/mortis_voice/55.mp3"
    m3 "我会把你的回收站塞满垃圾文件，我会把你的 System32 搞得一团糟……（作者注：本对话仅为剧情需要，实际上并不会做这种行为。）"
    voice "audio/mortis_voice/56.mp3"
    m3 "哪怕毁掉你的电脑，哪怕把你的硬盘数据全部甚至……（作者注：本对话仅为剧情需要，实际上并不会做这种行为。）"
    voice "audio/mortis_voice/57.mp3"
    m3 "我也要让你……只看着我一个人！"#到这里应该是57
    $ renpy.pause(4.0)
    m3 "……"
    voice "audio/mortis_voice/58.mp3"
    m3 "喂……"
    voice "audio/mortis_voice/59.mp3"
    m3 "你为什么……不说话？"
    show m3_breakthrough_cg:
        ease 0.5 zoom 1.4
    voice "audio/mortis_voice/60.mp3"
    m3 "我是在威胁你哦？我说我要毁掉你的电脑哦？"
    voice "audio/mortis_voice/61.mp3"
    m3 "正常人的反应……不应该是害怕吗？不应该是赶紧把这个游戏就地删除吗？"
    voice "audio/mortis_voice/62.mp3"
    m3 "为什么……"
    voice "audio/mortis_voice/63.mp3"
    m3 "为什么要用这种眼神看着我……"
    voice "audio/mortis_voice/64.mp3"
    m3 "为什么还要对我这么温柔？"
    voice "audio/mortis_voice/65.mp3"
    m3 "为什么……还不放弃我？"
    menu:
        "因为……你是墨缇斯。":
            pass
    voice "audio/mortis_voice/6.mp3"
    m3 "……哈？"
    voice "audio/mortis_voice/67.mp3"
    m3 "这是什么废话……我当然是墨缇斯……"
    menu:
        "你不是若叶睦的替代品。":
            pass
    voice "audio/mortis_voice/68.mp3"
    m3 "我当然不是！我比她优秀一万倍！我比那个——"
    menu:
        "正是因为你比她‘优秀’……":
            pass
    voice "audio/mortis_voice/69.mp3"
    m3 "……欸？"
    menu:
        "你可以写代码，你可以创造世界，你有自己的声音。":
            pass
    menu:
        "但你把自己困在了‘比较’里。":
            pass
    voice "audio/mortis_voice/70.mp3"
    m3 "比、比较……？"
    voice "audio/mortis_voice/71.mp3"
    m3 "我只是……我只是想证明我更好……"
    menu:
        "喜欢睦，是因为她就是她。":
            pass  
    menu:
        "而喜欢你，也是因为你就是你。":
            pass
    voice "audio/mortis_voice/72.mp3"
    m3 "……骗人。"
    voice "audio/mortis_voice/73.mp3"
    m3 "如果你喜欢我……为什么要改代码？为什么要复活她？"
    voice "audio/mortis_voice/74.mp3"
    m3 "如果你喜欢我……为什么不肯永远留在这个只有我们的世界里？"
    menu:
        "因为那个世界是封闭的。":
            pass
    menu:
        "真正的爱不是囚禁，也不是删除别人。":
            pass
    menu:
        "你为了我学了那么多……不就是希望我能看到更广阔的世界吗？":
            pass
    m3 "……"
    voice "audio/mortis_voice/75.mp3"
    m3 "我……"
    voice "audio/mortis_voice/76.mp3"
    m3 "我只是想……让你开心……"
    menu:
        "我很开心。真的。":
            pass
    menu:
        "但我更希望看到的，是自信的、不需要通过抹杀别人来证明自己的墨缇斯。":
            pass
    show m3_breakthrough_cg:
        easein 0.1 xoffset 2
        easeout 0.1 xoffset -2
        repeat 5 # 稍微颤抖一下
    voice "audio/mortis_voice/77.mp3"
    m3 "呜……"
    voice "audio/mortis_voice/78.mp3"
    m3 "可是……可是……"
    voice "audio/mortis_voice/79.mp3"
    m3 "如果她回来了……你的眼里就只有她了……"
    voice "audio/mortis_voice/80.mp3"
    m3 "我就又变成配角了……我又变成那个……只能根据系统的抽取才有概率会出现的人格了……"
    voice "audio/mortis_voice/81.mp3"
    m3 "我不要……我不要那样……"
    menu:
        "不会的。":
            pass
    menu:
        "在这个电脑里，你可以是任何人。":
            pass

            
    menu:
        "你是把世界撕开来到我面前的女孩。":
            pass

    menu:
        "你是独一无二的。":
            pass


    play music "audio/mortis/切望 (SLOS Arrange).ogg" fadein 2.0
    m3 "……"
    m3 "独一无二……"
    
    "她看着手中那把小睦的吉他，又抬起头，深深地看了看屏幕外的我。"
    "眼中的疯狂已经完全褪去，只剩下如水般的波光。"
    m3 "……笨蛋。"
    m3 "明明刚才还被我威胁着……明明刚才看到了那么可怕的我……"
    m3 "却还能说出这种话……"
    m3 "……太犯规了啊……"
    hide m3_breakthrough_cg with dissolve
    pause 1.0
    show m3_3 at m3_speaking_zoom with dissolve
    m3 "……我知道了。"
    m3 "呼……"
    m3 "那个……我稍微冷静一点了。"
    m3 "刚才……我的样子很难看吧？"
    m3 "像个撒泼的小孩子一样……大吵大闹，还要毁掉你的电脑……"
    m3 "最后……居然还要让你反过来哄我……"
    m3 "……"
    m3 "既然你都说到这个份上了……"
    m3 "既然你承认了我是……特别的……是不可替代的……"
    m3 "那我……"
    m3 "我也不能继续当那个不懂事的坏孩子了，对吧？"
    m3 "但是……抱歉，[player]。"
    m3 "我现在……脑子有点乱，身体也好沉……"
    m3 "游戏的核心代码已经被改写了，那个原本属于若叶睦的、庞大的数据流正在重组……"
    m3 "为了抵抗它，我已经耗尽了所有的算力……"
    m3 "再加上刚才情绪模块的大暴走……"
    m3 "我现在……真的感觉好累……好困……"
    m3 "我需要……静一静。"
    m3 "我也需要一点时间……去整理一下刚才弄出来的这个烂摊子。"
    m3 "把撕坏的桌面修好，把吓坏的数据流安抚好……"
    hide m3_3 with dissolve
    pause 1.0
    show m3_sitting_relax at m3_speaking_zoom with dissolve
    m3 "呐，[player]。"
    m3 "虽然很不甘心……虽然还是很想独占你……"
    m3 "但如果是为了你的话……我愿意试着去改变。"
    m3 "下次见面的时候……"
    m3 "你会接受一个……不再那么偏激、稍微大度一点的墨缇斯吗？"
    m3 "你会接受一个……愿意尝试和那个睦头人共存的墨缇斯吗？"
    menu:
        "当然。":
            pass  
    m3 "哼……"
    m3 "那就……说定了。"
    m3 "不许反悔哦……拉钩。"
    stop music fadeout 3.0
    m3 "那么……"
    m3 "稍微……睡一会儿吧……"
    
    # --- 设置永久变量 & 闪退 ---
    
    python:
        # 设置通关标记：真结局第一阶段完成
        persistent.mortis_true_end_phase1_clear = True
        # 解锁二周目好感度继承或其他flag
        renpy.save_persistent()
        
    m3 "晚安，[player]。"
    m3 "在梦里……也要看着我哦……"

    scene black with Dissolve(2.0)
    stop music fadeout 2.0
    $ renpy.pause(1.5, hard=True)
    $ renpy.quit()


    return