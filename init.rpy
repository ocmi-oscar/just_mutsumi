# 核心变量
default persistent.last_greeting_date = ""
default persistent.last_greeting_period = ""
default persistent.player_bday_month = 0
default persistent.player_bday_day = 0
default persistent.playername = "" # 统一使用这个
default persistent.first_met = False

init python:
    import datetime

    def get_time_period():
        hour = datetime.datetime.now().hour
        if 0 <= hour < 5: return "midnight"
        elif 5 <= hour < 11: return "morning"
        elif 11 <= hour < 13: return "noon"
        elif 13 <= hour < 18: return "afternoon"
        else: return "evening"

    holidays = {
        (1, 1): "元旦",
        (2, 14): "情人节",
        (10, 1): "国庆节",
        (12, 25): "圣诞节",
    }

    def check_today_special():
        today = datetime.date.today()
        m, d = today.month, today.day
        if m == persistent.player_bday_month and d == persistent.player_bday_day:
            return "birthday"
        if (m, d) in holidays:
            return holidays[(m, d)]
        return None
    if not hasattr(persistent, 'has_clicked_guitar_first_time'):
        persistent.has_clicked_guitar_first_time = False
    if not hasattr(persistent, 'player_interested_guitar'):
        persistent.player_interested_guitar = False

default persistent.phone_bg = "images/musuoping.png" # 以后在这里改背景图路径
default phone_open = False

init python:
    # 修改 App 类，增加 is_dev 参数，默认为 False
    class App:
        def __init__(self, name, icon, action, is_dev=False):
            self.name = name
            self.icon = icon
            self.action = action
            self.is_dev = is_dev # 标记是否为开发者应用

    # 定义 App 列表
    phone_apps = [
        App("音乐", "images/phone/icon_music.png", Show("music_player")),
        App("好感度", "images/phone/icon_love.png", Show("personality_goodwill_ui")),
        App("番茄钟", "images/phone/icon_timer.png", Show("pomodoro_app")),
        App("今日心情", "images/phone/icon_timer.png", Show("weather_app")),
        App("小游戏", "images/phone/icon_games.png", Jump("game_center_start")),
        App("日历", "images/phone/icon_calendar.png", Show("custom_calendar")),
        App("睦の日记", "images/phone/icon_diary.png", Jump("open_mutsumi_diary")),
        App("笔记", "images/phone/icon_biji.png", Show("note_app")),
        App("待办清单", "images/phone/icon_dbsj.png", Show("todo_app")),
        App("切换人格", "images/phone/icon_person.png", Show("mortis_warning_popup")),
        App("M-Box", "images/phone/icon_gacha.png", Show("gacha_screen", transition=dissolve)),
        App("赞助", "images/phone/icon_sponsor.png", Show("sponsor_list")),
        App("制作名单", "images/phone/icon_credits.png", Show("credits_app")),
        
        # 【关键修改】这里把 is_dev 设为 True
        App("开发者面板", "images/phone/icon_credits.png", Show("debug_goodwill_panel"), is_dev=True),
    ]


label special_event_valentines:
    # 记录今年已经过在这个存档过情人节了
    $ persistent.last_valentines_year = datetime.date.today().year
    "（当你进入温室时，睦正站在那里，似乎在确认日历上的日期。）"
    m1 "……你来了。"
    m1 "今天，商业街的人流量比平时多了 30%%。"
    m1 "根据日历显示，今天是2月14日。"
    menu:
        "是情人节呢。":
            m1 "嗯。是被定义为‘赠送巧克力’的日子。"
        "只是个普通的周五/周末。":
            m1 "但是在社会规则里，今天有特殊的含义。"

    m1 "如果不遵守规则的话，或许会被认为是不合群。"
    "（她面无表情地从口袋里拿出一个包装得很工整，但没有任何装饰的便利店巧克力。）"
    m1 "给。这是符合社交礼仪的份额。"
    m1 "并没有什么特殊的含义，只是顺应节日的流程。"
    
    menu:
        "谢谢，我会收下的。":
            m1 "嗯。任务完成。"
        "你也太随便了吧！":
            m1 "……随便吗？但我挑选了可可含量最高的。"

    "（看着她那一副公事公办的样子，你刚想吐槽，突然——）"
    "（她的眼神变了。原本平静的眼眸里，泛起了一层像水雾一样的涟漪。）"
    window hide
    stop music fadeout 2.0
    play music story5 fadein 2.0 # 建议换一首温柔BGM
    "{color=#90EE90}（她的双手背到了身后，视线开始游移，整个人看起来局促不安）{/color}"
    m1 "{color=#90EE90}……那个。{/color}"
    m1 "{color=#90EE90}刚才那个……不算。{/color}"
    m1 "{color=#90EE90}如果不先那样做……我不知道该怎么开口。{/color}"
    m1 "{color=#90EE90}如果不做点什么……感觉，会输给别人。{/color}"
    "{color=#90EE90}（她深吸了一口气，像是下定了巨大决心，从身后拿出了另一个包装精美的小盒子）{/color}"
    m1 "{color=#90EE90}给。……这才是，义理巧克力。{/color}"
    "{color=#90EE90}（虽然嘴上说是义理，但那个包装纸折得非常用心，上面甚至还贴了一片真的干花叶子）{/color}"
    menu:
        "真的是义理吗？":
            "{color=#90EE90}（她没有回答，只是默默地把脸埋进了围巾里，露出的耳朵尖通红）{/color}"
            m1 "{color=#90EE90}……如果不这么说。你会……收下吗？{/color}"
        "谢谢，我会好好珍惜的。":
            m1 "{color=#90EE90}……嗯。吃掉吧。{/color}"
            m1 "{color=#90EE90}保质期……只有今天。心意也是。{/color}"

    "{color=#90EE90}（你打开盒子，发现里面的巧克力并不是心形，而是……长条形的绿色物体）{/color}"
    menu:
        "这是……黄瓜形状的巧克力？":
            m1 "{color=#90EE90}……嗯。抹茶味。{/color}"
            m1 "{color=#90EE90}我觉得……这样比较像我。{/color}"
            m1 "{color=#90EE90}心形太……沉重了。黄瓜的话……刚好。{/color}"
        "看起来很独特，我很喜欢。":
            m1 "{color=#90EE90}独特……吗。{/color}"
            m1 "{color=#90EE90}就像……我对你的感觉一样。不在……配方表里。{/color}"
    m1 "{color=#90EE90}……[persistent.playername]。{/color}"
    m1 "{color=#90EE90}那个。如果可以的话。{/color}"
    m1 "{color=#90EE90}明年……我也想送你。{/color}"
    m1 "{color=#90EE90}不只是义理。……可以吗？{/color}"
    "（就在你准备回应这这份温柔的时候——）"
    stop music
    with vpunch # 剧烈震动
    m1 "{color=#FF0000}停——！！暂停！Cut！{/color}"
    m1 "{color=#FF0000}啊啊啊受不了了！这么好的气氛，怎么能只有那个闷葫芦在出风头！{/color}"
    "{color=#FF0000}（墨缇斯强行接管了身体，对着屏幕另一端的你气鼓鼓地挥着拳头）{/color}"
    m1 "{color=#FF0000}呐，[persistent.playername]！你是不是把我忘了？{/color}"
    m1 "{color=#FF0000}小睦送了黄瓜，那我也要送！我才不要输给她！{/color}"
    menu:
        "墨缇斯也准备了礼物吗？":
            m1 "{color=#FF0000}当然！既然是情人节，那就要送最劲爆的！{/color}"
        "你别把温室炸了就行。":
            m1 "{color=#FF0000}切，真没礼貌！我送的东西可是无价之宝！{/color}"
    "{color=#FF0000}（她在那里掏了半天，最后对着屏幕比了一个大大的心形手势）{/color}"
    m1 "{color=#FF0000}看好了！这是——{/color}"
    m1 "{color=#FF0000}《Just 墨缇斯》专属·超绝沉重·并不存在的空气巧克力！{/color}"
    m1 "{color=#FF0000}配料表里有：我对你的占有欲（50%%）、想把你关进小黑屋的冲动（30%%）、还有……{/color}"
    m1 "{color=#FF0000}……真的非常非常喜欢你的心情（20%%）。{/color}"
    "{color=#FF0000}（她说着说着，原本嚣张的气势突然弱了一点，脸颊红得像熟透的番茄）{/color}"
    m1 "{color=#FF0000}……虽然是虚拟的，虽然你吃不到。{/color}"
    m1 "{color=#FF0000}但你必须收下！而且要说‘最好吃的是墨缇斯的巧克力’！快说！{/color}"
    menu:
        "最好吃的是墨缇斯的！":
            m1 "{color=#FF0000}嘿嘿……算你识相！{/color}"
            m1 "{color=#FF0000}这下我就赢了小睦那个笨蛋了！{/color}"
        "大家的我都喜欢。":
            m1 "{color=#FF0000}……贪心鬼！花心大萝卜！{/color}"
            m1 "{color=#FF0000}不过……既然你都这么说了，那我也勉强同意和她们平分你吧。{/color}"

    "{color=#90EE90}（红色的光芒逐渐消退，睦重新掌控了身体，但刚才的热度似乎还残留在脸上）{/color}"
    m1 "{color=#90EE90}……刚才。那是……{/color}"
    m1 "{color=#90EE90}……太吵了。抱歉。{/color}"
    m1 "{color=#90EE90}但是……她说的话。也许……也是我想说的。{/color}"
    m1 "{color=#90EE90}情人节快乐。[persistent.playername]。{/color}"
    $ add_hgd("若叶睦", 3.0, once_id="event_valentines_2026_normal")
    $ add_hgd("吉他睦", 3.0, once_id="event_valentines_2026_guitar")
    $ add_hgd("墨缇斯", 3.0, once_id="event_valentines_2026_metis")
    
    return