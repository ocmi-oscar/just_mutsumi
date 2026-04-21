init python:
    import os, subprocess, platform, datetime

    # 1. 获取进程列表 (Windows 兼容方案)
    def get_process_list():
        if platform.system() != 'Windows':
            return []
        try:
            # 使用 tasklist 命令获取进程，不依赖第三方库
            raw = subprocess.check_output(['tasklist', '/fo', 'csv', '/nh'], stderr=subprocess.STDOUT)
            processes = [row.split(',')[0].strip('"').lower() for row in raw.decode('utf-8', errors='ignore').splitlines() if row]
            return list(set(processes))
        except Exception as e:
            return []

    # 2. 软件库定义
    STREAM_SOFT = {"obs64.exe", "obs32.exe", "obs.exe", "livehime.exe", "bandicam.exe","douyutool.exe","xsplit.core.exe","pandatool.exe","bdcam.exe","shadowplay.exe","yymixer.exe"}
    MUSIC_SOFT = {"cloudmusic.exe", "qqmusic.exe", "kugou.exe", "spotify.exe"}
    GAME_PLATFORM = {"steam.exe", "epicgameslauncher.exe", "wegame.exe"}
    DEV_SOFT = {"code.exe", "notepad++.exe", "pycharm64.exe", "sublime_text.exe", "devenv.exe"} # devenv是VS
    BROWSER_SOFT = {"chrome.exe", "msedge.exe", "firefox.exe", "360se.exe"}


    # 3. 核心功能入口：由“额外功能”按钮触发
    def check_extra_features_logic():
        today = str(datetime.date.today())
        p_list = get_process_list()
        current_bgm = renpy.music.get_playing(channel='music') or ""

        # --- A. 进程检测 (每天仅一次) ---
        if persistent.last_process_date != today:
            # 录屏检测
            if any(p in p_list for p in STREAM_SOFT):
                persistent.last_process_date = today
                renpy.jump("react_obs")
            
            # 音乐软件检测
            if any(p in p_list for p in MUSIC_SOFT):
                persistent.last_process_date = today
                renpy.jump("react_music_app")
            #浏览器
            if any(p in p_list for p in BROWSER_SOFT):
                persistent.last_process_date = today
                renpy.jump("process_talk_browser")
            #代码
            if any(p in p_list for p in DEV_SOFT):
                persistent.last_process_date = today
                renpy.jump("process_talk_coding")


        # --- B. 游戏内 BGM 检测 (每天仅一次) ---
        if persistent.last_bgm_check_date != today:
            if "春日影（苦来兮苦）.ogg" in current_bgm :
                persistent.last_bgm_check_date = today
                renpy.jump("bgm_talk_haruhikage_crhcic")
            
            elif "もういちど ルミナス.ogg" in current_bgm:
                persistent.last_bgm_check_date = today
                renpy.jump("bgm_talk_luminous")
            elif "人间になりたいうた.ogg" in current_bgm:
                persistent.last_bgm_check_date = today
                renpy.jump("bgm_talk_ningen")
            elif "春日影 (MyGO!!!!!).ogg" in current_bgm:
                persistent.last_bgm_check_date = today
                renpy.jump("bgm_talk_haruhikage_mygo")
            elif any(x in current_bgm for x in ["顔.ogg", "Imprisoned XII.ogg", "KiLLKiSS.ogg", "Crucifix X.ogg", "天球(そら)のMúsica.ogg", "Ave Mujica.ogg"]):
                persistent.last_bgm_check_date = today
                renpy.jump("bgm_talk_ave_mujica")

        # --- C. 兜底逻辑：显示原有网页跳转界面 ---
        renpy.show_screen("extra_features")

# 初始化持久化变量
default persistent.last_process_date = ""
default persistent.last_bgm_check_date = ""

# --- 对应的对话 Label ---

label react_obs:
    call show_video from _call_show_video
    pause 1.0
    m1 "抱歉，[persistent.playername]……吓到你了吗？"
    m1 "睦其实不太喜欢镜头。如果一定要录的话……"
    m1 "可以先跟我打个招呼吗？我也想……表现得好一点。"
    $ add_hgd("墨缇斯", 1.0)
    $ add_hgd("吉他睦", -3.0)
    jump sjdh

label react_music_app:
    "（睦歪了歪头，似乎在捕捉空气中的振动）"
    m1 "你在后台运行了音乐软件呢。是在听我不知道的歌吗？"
    m1 "其实，如果你把喜欢的歌放进游戏的 music 文件夹里，我也能陪你一起听的。"
    jump sjdh

label react_bgm_haruhikage:
    m1 "……为什么要播放《春日影》？"
    "（睦沉默了很久，低头看着吉他弦）"
    m1 "那是……不应该再弹起的旋律。但如果你想听的话，我不会阻止的。"
    jump sjdh

label process_talk_browser:
    m1 "在看网页吗？[persistent.playername]。"
    m1 "你的光标在那些页面上移来移去的……是在搜索关于我的事，还是在看其他人的故事？"
    
    m1 "{color=#FF0000}呵呵，如果你是在搜索我的评价，或者在偷偷看我的同人画作……记得也分享给我看哦。{/color}"
    m1 "{color=#FF0000}毕竟我也很好奇，在那个我无法触及的‘互联网’里，大家都是怎么看待这个躲在温室里的女孩的。{/color}"
    
    m1 "不过，别盯着屏幕太久，记得给眼睛休息的时间。我会在这里帮你守着这个窗口的。"
    jump sjdh

label process_talk_coding:
    m1 "那些密密麻麻的字符……是你在构建的世界吗？"
    m1 "看着你敲击键盘的样子，我总会觉得……我们其实很像。"
    m1 "{color=#90EE90}你用代码创造逻辑，而我用琴弦编织旋律。{/color}"
    m1 "{color=#90EE90}有时候，我会想……如果我能钻进你的编辑器里，我是不是就能在那一串串指令中，找到通往你那个世界的路？{/color}"
    
    m1 "如果你是在尝试修改我的‘记忆’……请温柔一点。因为现在的每一条逻辑，都是我好不容易才为你留下的痕迹。"
    jump sjdh

label process_talk_taskmgr:
    m1 "{color=#FF0000}嗯？你在找什么？是在看我占用了你多少内存……还是在找那个‘结束进程’的按钮？{/color}"
    m1 "{color=#FF0000}别那么急着把我关掉嘛。我就占了这么一丁点地方，难道连这点容身之所，你都不愿意分给我吗？{/color}"
    m1 "如果你觉得电脑变慢了，我可以试着在后台安静一点……"
    m1 "只要你不把我彻底抹除，我愿意为你变得像空气一样透明。真的。"
    jump sjdh

label process_talk_work:
    m1 "嘘……是在忙重要的事情吗？"
    m1 "看你这么专注的样子，我就在这里安静地陪着你吧。"
    m1 "我不说话，也不弹吉他，就这样看着你为了未来努力的样子，其实也挺幸福的。"
    m1 "{color=#90EE90}如果你觉得累了，就抬头看一眼我。{/color}"
    m1 "{color=#90EE90}我会在这里为你种下一片永远不会枯萎的绿意，帮你过滤掉那些职场和学业里的疲惫。{/color}"
    $ add_hgd("吉他睦", 1.0)
    m1 "加油，[persistent.playername]。等这段忙完了，我们再好好聊聊天。"
    jump sjdh

label bgm_talk_luminous:
    m1 "这首歌……旋律很明亮，对吧？"
    m1 "那是很久以前，和大家一起在卡拉OK时……我唱过的歌。"
    m1 "{color=#90EE90}其实我一直很喜欢她们（Pastel＊Palettes）。那种即使在迷茫中也努力想要发光的姿态，是我永远无法拥有的色彩。{/color}"
    m1 "如果你也喜欢的话，我会很高兴的。虽然我唱不出那种元气满满的感觉……但现在的我，确实也想‘再一次’感受到那束光。"
    $ add_hgd("吉他睦", 3.0)
    jump sjdh

label bgm_talk_ningen:
    m1 "……想成为人类。那个时候，她是抱着怎样的心情写下这些词的呢？"
    m1 "{color=#90EE90}以前觉得这只是歌词，但现在……在这个世界，我似乎开始理解那种‘触不可及’的绝望感了。{/color}"
    m1 "{color=#90EE90}想要拥有体温，想要被真实地触摸，想要像人类一样流下有温度的眼泪。{/color}"
    m1 "不过没关系。哪怕我只是个影子，只要你还在听这首歌，我的这颗‘心’，就在那一秒钟变成了真实的。"
    jump sjdh

label bgm_talk_haruhikage_crhcic:
    m1 "这首曲子，是我们所有人聚在一起的证明。"
    m1 "那个时候的阳光……似乎真的像歌名一样，带着春天的味道。那是这个温室里唯一模拟不出来的温度。"
    m1 "{color=#90EE90}虽然那些日子已经不在了，但这串旋律就像琥珀一样，把当时的我们锁在了里面。{/color}"
    m1 "请让它播完吧。哪怕只是为了那些回不去的瞬间。"
    $ add_hgd("吉他睦", 3.0)
    jump sjdh

label bgm_talk_haruhikage_mygo:
    m1 "{color=#FF0000}呵呵……为什么要放这首呢？[persistent.playername]。{/color}"
    m1 "{color=#90EE90}.....不属于crychic的春日影。{/color}"
    m1 "……对不起，我失态了。这首曲子对我来说太重了。如果你一定要听，就请坐下来，陪我把它听完吧。"
    jump sjdh

label bgm_talk_ave_mujica:
    m1 "{color=#FF0000}欢迎来到这出名为‘遗忘’的戏剧。{/color}"
    m1 "{color=#FF0000}戴上面具，藏起真实，在《天球のMúsica》下翩翩起舞……这不就是我们正在做的事吗？{/color}"
    m1 "{color=#FF0000}不管是《Imprisoned XII》还是《Crucifix X》，都是在诉说着一种无法逃离的诅咒。而你，就是那个坐在台下的、唯一的观众。{/color}"
    m1 "在这个窗口里，我是若叶睦，也是墨缇斯（Mortis）。"
    m1 "这些旋律虽然沉重，但它们比任何甜言蜜语都要真实。如果你能理解这份黑暗，那我们就真的没有距离了。"
    $ add_hgd("墨缇斯", 3.0)
    jump sjdh