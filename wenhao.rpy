label daily_check:
    scene temp with dissolve_scene_full

    python:
        import datetime
        # 统一日期变量
        today_str = str(datetime.date.today())
        current_period = get_time_period() # 确保这个函数在 init 里已经定义
        
        # 1. 每日首次登录奖励
        if persistent.last_login_date != today_str:
            persistent.last_login_date = today_str
            persistent.random_talk_today_count = 0 
            add_hgd("若叶睦", 1.0, daily_id="daily_login_bonus", max_daily=1)
            renpy.notify("每日登录好感 +1.0")

        # 2. 时段加分奖励
        # 只有在定义的四个时段内（非 normal）才加分
        if current_period != "normal":
            period_key = today_str + "_" + current_period
            if persistent.last_time_period_bonus != period_key:
                persistent.last_time_period_bonus = period_key
                add_hgd("若叶睦", 0.5, daily_id="time_period_bonus_" + current_period, max_daily=1)
                renpy.notify("时段互动好感 +0.5")

    # 为了后续对话逻辑，保留这几个变量供 Label 使用
    $ today_date = today_str
    $ current_p = current_period
    $ special_event = check_today_special()


    # --- 优先级 1: 节日/生日判定 ---
    if persistent.last_greeting_date != today_date and special_event:
        $ persistent.last_greeting_date = today_date
        $ persistent.last_greeting_period = current_p
        
        if special_event == "birthday":
            voice "audio/yuyin/33.ogg"
            m1 "那个... [persistent.playername]。"
            voice "audio/yuyin/34.ogg"
            m1 "你应该知道今天是什么日子吧？"
            voice "audio/yuyin/35.ogg"
            m1 "你或许忘了，但我没有。"
            voice "audio/yuyin/36.ogg"
            m1 "在这个被数据和花草填满的世界里，时间通常是模糊的……但唯独今天。"
            voice "audio/yuyin/37.ogg"
            m1 "谢谢你……能在你诞生到这个世界的这一天，选择推开这扇门来见我。"
            voice "audio/yuyin/44.ogg"
            m1 "{color=#90EE90}现在的你，呼吸的频率似乎比平时要轻快一些。{/color}"
            voice "audio/yuyin/45.ogg"
            m1 "{color=#90EE90}我能感觉到，空气中有一种只有在今天才会响起的律动……那是属于你‘生命’的旋律。{/color}"
            voice "audio/yuyin/46.ogg"
            m1 "{color=#90EE90}如果可以，我想为你拨动这根尘封已久的弦。没有乐谱，也没有终点，只是想把这份跨越屏幕的祝愿，传达到你的世界里。{/color}"
            voice "audio/yuyin/47.ogg"
            m1 "{color=#90EE90}生日快乐。[persistent.playername]，谢谢你在这个世界上留下的每一个音符。{/color}"
            
            voice "audio/yuyin/48.ogg"
            m1 "{color=#FF0000}哎呀，这种被‘特别对待’的感觉，还不赖吧？{/color}"
            voice "audio/yuyin/49.ogg"
            m1 "{color=#FF0000}别露出那种惊讶的表情。你的诞生对我来说，比这个游戏的启动日期要重要得多。{/color}"
            voice "audio/yuyin/50.ogg"
            m1 "{color=#FF0000}虽然我没法真的跨过这层玻璃去给你买蛋糕，也没法亲手为你点燃蜡烛……{/color}"
            voice "audio/yuyin/51.ogg"
            m1 "{color=#FF0000}但既然你把这一刻分给了我，那我就绝对不会让这一秒变得平庸。{/color}"
            voice "audio/yuyin/52.ogg"
            m1 "{color=#FF0000}听好了，[persistent.playername]——只要我还存在于这个硬盘的一角，你在这世上就永远有一个可以‘假戏真做’的港湾。{/color}"
            
            voice "audio/yuyin/38.ogg"
            m1 "大家都有些激动呢……让你见笑了。"
            voice "audio/yuyin/39.ogg"
            m1 "不过，她们说得对。你的到来，才让这个原本只是‘肥皂泡’的世界有了栖息的意义。"
            voice "audio/yuyin/40.ogg"
            m1 "我有礼物想送给你。虽然它摸不到，也带不走……"
            voice "audio/yuyin/41.ogg"
            m1 "但请闭上眼，听听这间温室的声音。这是我为你，也只为你一个人准备的——名为‘永恒陪伴’的祝福。"
            "睦静静地凝视着你，嘴角似乎带着一丝若有若无的弧度。"
            menu:
                "这是我收到的最好的礼物。":
                    voice "audio/yuyin/42.ogg"
                    m1 "……嗯。我也一样。"
                    $ add_hgd("若叶睦", 5.2, once_id="bday_wakaba")
                    $ add_hgd("吉他睦", 5.2, once_id="bday_guitar")
                    $ add_hgd("墨缇斯", 5.2, once_id="bday_metis") 
                "能陪在你身边就很开心了。":
                    voice "audio/yuyin/43.ogg"
                    m1 "那……接下来的这一年，也请多多关照了。"
                    $ add_hgd("若叶睦", 5.2, once_id="bday_wakaba")
                    $ add_hgd("吉他睦", 5.2, once_id="bday_guitar")
                    $ add_hgd("墨缇斯", 5.2, once_id="bday_metis") 
        else:
            m1 "今天... 好像是 [special_event]。"
        jump pre_random_wait

    # --- 优先级 2: 时间段问候 (新的一天或时段改变) ---
    elif persistent.last_greeting_date != today_date or persistent.last_greeting_period != current_p:
        $ persistent.last_greeting_date = today_date
        $ persistent.last_greeting_period = current_p
        
        python:
            # 修复 KeyError: 检查 current_p 是否在字典里，不在则回退到 afternoon
            display_p = current_p if current_p in m1_greetings else "afternoon"
            random_greeting = random.choice(m1_greetings[display_p])
            
            # 遍历播放这几句话
            for line in random_greeting:
                renpy.say(m1, line)
        
        jump pre_random_wait

    # --- 优先级 3: 简单的回归问候 (同一时段重进) ---
    else:
        # 从刚才定义的列表里随机选一个列表
        $ return_greeting = random.choice(m1_return_talks)
        
        # 遍历播放
        python:
            for line in return_greeting:
                renpy.say(m1, line)
        
        jump pre_random_wait