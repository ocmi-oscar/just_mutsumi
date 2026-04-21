# ==============================================================================
# 🎸 音乐演奏系统 — Mutsumi Rhythm
#
# 下落式音游 + 自动谱面生成
# 特色：导入任意音乐自动生成谱面
#
# 4弦（D/F/J/K） 对应吉他的4根弦
# 睦弹主旋律，玩家弹伴奏节奏
# ==============================================================================

init python:
    import random as _rhy_rng
    import time as _rhy_time
    import struct as _rhy_struct
    import os as _rhy_os
    import math as _rhy_math

    # ── 游戏配置 ──
    RHY_LANES = 4
    RHY_KEYS = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
    RHY_KEY_NAMES = ["D", "F", "J", "K"]
    RHY_LANE_COLORS = ["#8FBC8F", "#6ab8d8", "#d4a0ff", "#ffd700"]
    RHY_SPEED = 400.0        # 像素/秒 下落速度
    RHY_HIT_Y = 620          # 判定线Y坐标
    RHY_SPAWN_Y = -20        # 生成位置
    RHY_WINDOW_PERFECT = 0.05  # ±50ms
    RHY_WINDOW_GREAT = 0.10   # ±100ms
    RHY_WINDOW_GOOD = 0.15    # ±150ms
    RHY_WINDOW_MISS = 0.25    # ±250ms 超过就miss

    # ── 预制谱面（游戏自带歌曲） ──
    # 格式: [(time_sec, lane), ...]
    RHY_BUILTIN_MAPS = {
        "tutorial": {
            "name": "练习曲",
            "artist": "若叶睦",
            "file": "",
            "bpm": 120,
            "notes": [],  # 自动生成简单练习谱
        },
    }

    def rhy_generate_tutorial():
        """生成简单的练习谱面"""
        notes = []
        bpm = 120
        beat = 60.0 / bpm
        t = 2.0  # 开始时间
        # 16小节练习
        for bar in range(16):
            base = t + bar * beat * 4
            if bar < 4:
                # 单键练习
                for i in range(4):
                    notes.append((base + i * beat, i % 4))
            elif bar < 8:
                # 交替练习
                for i in range(4):
                    notes.append((base + i * beat, (i * 2) % 4))
            elif bar < 12:
                # 快速
                for i in range(8):
                    notes.append((base + i * beat * 0.5, _rhy_rng.randint(0, 3)))
            else:
                # 混合
                for i in range(6):
                    notes.append((base + i * beat * 0.67, _rhy_rng.randint(0, 3)))
        return notes

    # ══════════════════════════════════════════════════════════
    #  自动谱面生成器（核心创新）
    # ══════════════════════════════════════════════════════════

    def rhy_analyze_audio(filepath):
        """分析音频文件，返回节拍时间点列表"""
        import wave

        try:
            wf = wave.open(filepath, 'rb')
        except:
            return None, "无法打开音频文件（仅支持WAV格式）"

        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()

        if sampwidth not in (1, 2):
            wf.close()
            return None, "不支持的音频位深"

        # 读取全部数据
        raw = wf.readframes(nframes)
        wf.close()

        # 转换为单声道数值
        samples = []
        if sampwidth == 2:
            fmt = "<" + "h" * (len(raw) // 2)
            try:
                values = _rhy_struct.unpack(fmt, raw)
            except:
                # 分块解包避免内存问题
                values = []
                chunk = 4096
                for i in range(0, len(raw), chunk * 2):
                    block = raw[i:i + chunk * 2]
                    if len(block) % 2 != 0:
                        block = block[:len(block) - 1]
                    if block:
                        values.extend(_rhy_struct.unpack("<" + "h" * (len(block) // 2), block))

            if channels == 2:
                samples = [(values[i] + values[i+1]) / 2 for i in range(0, len(values) - 1, 2)]
            else:
                samples = list(values)
        elif sampwidth == 1:
            values = [b - 128 for b in raw]
            if channels == 2:
                samples = [(values[i] + values[i+1]) / 2 for i in range(0, len(values) - 1, 2)]
            else:
                samples = values

        if not samples:
            return None, "音频数据为空"

        # 能量分析 — 按窗口计算RMS能量
        window_size = int(framerate * 0.02)   # 20ms窗口
        hop_size = int(framerate * 0.01)      # 10ms步长
        energies = []
        for i in range(0, len(samples) - window_size, hop_size):
            window = samples[i:i + window_size]
            rms = _rhy_math.sqrt(sum(s * s for s in window) / len(window))
            energies.append(rms)

        if not energies:
            return None, "音频过短"

        # 自适应阈值 — 局部平均的倍数
        local_window = 50  # 约0.5秒
        onsets = []
        for i in range(local_window, len(energies) - 1):
            local_avg = sum(energies[i - local_window:i]) / local_window
            threshold = local_avg * 1.6

            # 当前能量超过阈值 且 是局部峰值
            if energies[i] > threshold and energies[i] > energies[i-1] and energies[i] >= energies[i+1]:
                time_sec = i * hop_size / framerate
                onsets.append(time_sec)

        # 去除过密的onset（最小间隔150ms）
        filtered = []
        last_t = -1.0
        for t in onsets:
            if t - last_t >= 0.15:
                filtered.append(t)
                last_t = t

        return filtered, None

    def rhy_generate_beatmap(onset_times, difficulty="normal"):
        """将onset时间点转换为游戏谱面"""
        notes = []
        last_lane = -1

        for t in onset_times:
            # 分配轨道 — 避免连续同轨
            if difficulty == "easy":
                lane = _rhy_rng.choice([0, 1, 2, 3])
            elif difficulty == "normal":
                available = [l for l in range(4) if l != last_lane]
                lane = _rhy_rng.choice(available)
            else:  # hard
                # 更多双押
                if _rhy_rng.random() < 0.2 and notes:
                    lane1 = _rhy_rng.randint(0, 1)
                    lane2 = _rhy_rng.randint(2, 3)
                    notes.append((t, lane1))
                    notes.append((t, lane2))
                    last_lane = lane2
                    continue
                available = [l for l in range(4) if l != last_lane]
                lane = _rhy_rng.choice(available)

            notes.append((t, lane))
            last_lane = lane

        # easy模式减少音符密度
        if difficulty == "easy":
            notes = [n for i, n in enumerate(notes) if i % 2 == 0]

        return sorted(notes, key=lambda x: x[0])

    # ══════════════════════════════════════════════════════════
    #  游戏引擎
    # ══════════════════════════════════════════════════════════

    class RhythmGame(python_object):
        def __init__(self, notes, music_file=None):
            self.notes = notes          # [(time, lane), ...]
            self.music_file = music_file
            self.active_notes = []      # [{time, lane, hit, y}, ...]
            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.perfect = 0
            self.great = 0
            self.good = 0
            self.miss = 0
            self.total_notes = len(notes)
            self.next_note_idx = 0
            self.game_over = False
            self.started = False
            self.start_time = 0
            self.last_judge = ""
            self.last_judge_time = 0
            self.lane_flash = [0.0] * 4

        def start(self):
            self.started = True
            self.start_time = _rhy_time.time()
            if self.music_file:
                try:
                    if renpy.loadable(self.music_file):
                        renpy.music.play(self.music_file, channel="music", loop=False)
                except:
                    pass

        def get_time(self):
            if not self.started:
                return 0.0
            return _rhy_time.time() - self.start_time

        def update(self):
            """每帧调用"""
            if self.game_over or not self.started:
                return

            current_time = self.get_time()
            travel_time = (RHY_HIT_Y - RHY_SPAWN_Y) / RHY_SPEED

            # 生成新的可见音符
            while self.next_note_idx < len(self.notes):
                nt, nl = self.notes[self.next_note_idx]
                spawn_time = nt - travel_time
                if current_time >= spawn_time:
                    self.active_notes.append({
                        "time": nt,
                        "lane": nl,
                        "hit": False,
                        "missed": False,
                    })
                    self.next_note_idx += 1
                else:
                    break

            # 检查过期音符(miss)
            for n in self.active_notes:
                if not n["hit"] and not n["missed"]:
                    if current_time > n["time"] + RHY_WINDOW_MISS:
                        n["missed"] = True
                        self.miss += 1
                        self.combo = 0
                        self.last_judge = "MISS"
                        self.last_judge_time = current_time

            # 清理远离屏幕的音符
            self.active_notes = [n for n in self.active_notes
                                 if not (n["missed"] and current_time > n["time"] + 1.0)
                                 and not (n["hit"] and current_time > n["time"] + 0.5)]

            # 检查游戏结束
            if self.next_note_idx >= len(self.notes):
                all_done = all(n["hit"] or n["missed"] for n in self.active_notes)
                if all_done and not self.active_notes:
                    self.game_over = True

        def note_y(self, note_time):
            """计算音符的Y坐标"""
            ct = self.get_time()
            travel_time = (RHY_HIT_Y - RHY_SPAWN_Y) / RHY_SPEED
            progress = (ct - (note_time - travel_time)) / travel_time
            return int(RHY_SPAWN_Y + progress * (RHY_HIT_Y - RHY_SPAWN_Y))

        def hit_lane(self, lane):
            """玩家按下某轨道"""
            if self.game_over or not self.started:
                return

            ct = self.get_time()
            self.lane_flash[lane] = ct

            # 找到该轨道最近的未击中音符
            best = None
            best_diff = 999
            for n in self.active_notes:
                if n["lane"] == lane and not n["hit"] and not n["missed"]:
                    diff = abs(ct - n["time"])
                    if diff < best_diff:
                        best = n
                        best_diff = diff

            if best is None or best_diff > RHY_WINDOW_MISS:
                return

            best["hit"] = True
            if best_diff <= RHY_WINDOW_PERFECT:
                self.perfect += 1
                self.score += 300
                self.last_judge = "PERFECT"
            elif best_diff <= RHY_WINDOW_GREAT:
                self.great += 1
                self.score += 200
                self.last_judge = "GREAT"
            elif best_diff <= RHY_WINDOW_GOOD:
                self.good += 1
                self.score += 100
                self.last_judge = "GOOD"
            else:
                self.miss += 1
                self.combo = 0
                self.last_judge = "MISS"
                self.last_judge_time = ct
                return

            self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            self.score += self.combo * 10  # combo加分
            self.last_judge_time = ct

        def get_rank(self):
            if self.total_notes == 0:
                return "?"
            ratio = (self.perfect * 3 + self.great * 2 + self.good) / (self.total_notes * 3.0)
            if ratio >= 0.95 and self.miss == 0:
                return "S"
            elif ratio >= 0.9:
                return "A"
            elif ratio >= 0.75:
                return "B"
            elif ratio >= 0.6:
                return "C"
            else:
                return "D"

    # ══════════════════════════════════════════════════════════
    #  选歌 & 导入
    # ══════════════════════════════════════════════════════════

    _rhy_game = None
    _rhy_song_list = []
    _rhy_difficulty = "normal"
    _rhy_import_status = ""

    def rhy_scan_songs():
        """扫描可用歌曲"""
        songs = []
        # 预制练习曲
        songs.append({
            "id": "tutorial",
            "name": "练习曲 — 基础训练",
            "file": "",
            "notes": rhy_generate_tutorial(),
        })

        # 确保自定义音乐目录存在
        custom_dir = os.path.join(config.gamedir, "custom_music")
        if not os.path.isdir(custom_dir):
            try:
                os.makedirs(custom_dir)
            except:
                pass

        # 扫描游戏自带音乐
        music_dir = os.path.join(config.gamedir, "music")
        if os.path.isdir(music_dir):
            for fname in sorted(os.listdir(music_dir)):
                if fname.lower().endswith((".ogg", ".mp3", ".wav")):
                    songs.append({
                        "id": "music_" + fname,
                        "name": fname.rsplit(".", 1)[0],
                        "file": "music/" + fname,
                        "notes": None,
                    })

        # 扫描自定义导入
        if os.path.isdir(custom_dir):
            for fname in sorted(os.listdir(custom_dir)):
                if fname.lower().endswith(".wav"):
                    songs.append({
                        "id": "custom_" + fname,
                        "name": "[导入] " + fname.rsplit(".", 1)[0],
                        "file": "custom_music/" + fname,
                        "notes": None,
                    })

        store._rhy_song_list = songs

    def rhy_start_song(song_data):
        """开始一首歌"""
        notes = song_data.get("notes")
        music_file = song_data.get("file", "")

        if notes is None:
            # 需要自动生成谱面
            store._rhy_import_status = "正在分析音频节拍..."
            renpy.restart_interaction()

            full_path = os.path.join(config.gamedir, music_file)

            # 如果不是WAV，提示
            if not full_path.lower().endswith(".wav"):
                # 尝试直接用ogg（简化版：生成随机谱面）
                store._rhy_import_status = "非WAV格式，生成随机节奏谱面..."
                renpy.restart_interaction()
                notes = rhy_generate_random_map(180)  # 假设3分钟
            else:
                onsets, err = rhy_analyze_audio(full_path)
                if err:
                    store._rhy_import_status = "分析失败: " + err
                    renpy.restart_interaction()
                    return
                notes = rhy_generate_beatmap(onsets, store._rhy_difficulty)

        store._rhy_game = RhythmGame(notes, music_file)
        store._rhy_import_status = ""

    def rhy_generate_random_map(duration_sec):
        """为无法分析的音频生成随机谱面"""
        notes = []
        bpm = 130
        beat = 60.0 / bpm
        t = 2.0
        while t < duration_sec:
            lane = _rhy_rng.randint(0, 3)
            notes.append((t, lane))
            if store._rhy_difficulty == "easy":
                t += beat
            elif store._rhy_difficulty == "hard":
                t += beat * 0.5
            else:
                t += beat * 0.75
        return notes


# ==============================================================================
# 🎮 游戏Screen
# ==============================================================================

label start_rhythm_game:
    $ rhy_scan_songs()
    call screen rhythm_select_screen
    jump game_center_start

screen rhythm_select_screen():
    modal True zorder 200
    add Solid("#0a0a14")

    # 标题
    frame:
        xfill True ysize 70
        background Solid("#12122a")
        padding (30, 12)
        hbox:
            xfill True yalign 0.5
            vbox:
                spacing 2
                text "音乐演奏" size 22 color "#d4a0ff" bold True
                text "Mutsumi Rhythm" size 10 color "#ffffff33"
            textbutton "返回":
                action Return()
                text_size 14 text_color "#ffffff44" text_hover_color "#ffffff"
                xalign 1.0 yalign 0.5

    # 难度选择
    frame:
        ypos 74 xfill True ysize 36
        background Solid("#0d0d1a")
        padding (30, 4)
        hbox:
            spacing 20 yalign 0.5
            text "难度:" size 12 color "#ffffff55" yalign 0.5
            for _did, _dn, _dc in [("easy", "简单", "#8FBC8F"), ("normal", "普通", "#6ab8d8"), ("hard", "困难", "#ff6666")]:
                $ _da = (_rhy_difficulty == _did)
                textbutton "[_dn]":
                    action SetVariable("_rhy_difficulty", _did)
                    text_size 13
                    text_color (_dc if _da else "#ffffff33")
                    text_bold _da

    # 歌曲列表
    viewport:
        ypos 114 ysize 520
        xfill True mousewheel True scrollbars None

        vbox:
            spacing 4 xfill True

            text "操作说明:  D  F  J  K  对应四根弦" size 11 color "#ffffff33" xoffset 30

            null height 8

            for _si in range(len(_rhy_song_list)):
                $ _song = _rhy_song_list[_si]
                $ _sname = _song["name"]
                $ _sfile = _song.get("file", "")
                $ _has_notes = _song.get("notes") is not None

                button:
                    xsize 1000 ysize 64
                    xalign 0.5
                    background Solid("#ffffff08")
                    hover_background Solid("#d4a0ff15")
                    action Function(rhy_start_song, _song)

                    hbox:
                        spacing 16 yalign 0.5 xoffset 30

                        # 图标
                        frame:
                            xsize 40 ysize 40
                            background Solid("#d4a0ff33")
                            text "♪" align (0.5, 0.5) size 18 color "#d4a0ff"

                        vbox:
                            spacing 2 yalign 0.5
                            text "[_sname]" size 15 color "#ffffffcc"
                            if _has_notes:
                                text "预制谱面" size 10 color "#8FBC8F88"
                            elif _sfile:
                                text "自动生成谱面" size 10 color "#6ab8d888"
                            else:
                                text "练习模式" size 10 color "#ffd70088"

                add Solid("#ffffff06") xsize 1000 ysize 1 xalign 0.5

            null height 20

            # 导入提示
            frame:
                xsize 1000 xalign 0.5
                background Solid("#ffffff05")
                padding (30, 14)
                vbox:
                    spacing 4
                    text "如何导入自己的音乐" size 13 color "#ffffff55"
                    text "将 .wav 文件放入 game/custom_music/ 文件夹" size 11 color "#ffffff33"
                    text "重新进入选歌界面即可看到你的歌曲" size 11 color "#ffffff33"
                    text "系统会自动分析节拍并生成谱面" size 11 color "#d4a0ff55"

    if _rhy_import_status:
        frame:
            align (0.5, 0.5)
            background Solid("#000000dd")
            padding (40, 20)
            text "[_rhy_import_status]" size 16 color "#d4a0ff"

    # 如果游戏已就绪，跳转到游戏screen
    if _rhy_game and not _rhy_game.started:
        timer 0.1 action [Function(_rhy_game.start), ShowTransient("rhythm_play_screen")]


screen rhythm_play_screen():
    modal True zorder 300

    # 每帧更新
    timer 0.016 action Function(_rhy_game.update) repeat True

    $ rg = _rhy_game
    $ ct = rg.get_time()

    # 按键监听（必须用字符串字面量）
    key "K_d" action Function(rg.hit_lane, 0)
    key "K_f" action Function(rg.hit_lane, 1)
    key "K_j" action Function(rg.hit_lane, 2)
    key "K_k" action Function(rg.hit_lane, 3)

    # ── 背景 ──
    add Solid("#06060e")

    # ── 轨道 ──
    $ lane_w = 120
    $ total_w = lane_w * 4
    $ start_x = (1280 - total_w) // 2

    for _li in range(4):
        $ _lx = start_x + _li * lane_w
        $ _lc = RHY_LANE_COLORS[_li]

        # 轨道背景
        add Solid(_lc + "08") xpos _lx ypos 0 xsize lane_w ysize 720

        # 轨道分隔线
        if _li > 0:
            add Solid("#ffffff0a") xpos _lx ypos 0 xsize 1 ysize 720

        # 判定线闪光
        $ _flash = ct - rg.lane_flash[_li]
        if _flash < 0.15:
            add Solid(_lc + "44") xpos _lx ypos (RHY_HIT_Y - 20) xsize lane_w ysize 40

    # 判定线
    add Solid("#ffffff33") xpos start_x ypos RHY_HIT_Y xsize total_w ysize 3

    # 按键提示
    for _ki in range(4):
        $ _kx = start_x + _ki * lane_w
        $ _kn = RHY_KEY_NAMES[_ki]
        $ _kc = RHY_LANE_COLORS[_ki]
        frame:
            xpos _kx ypos (RHY_HIT_Y + 10) xsize lane_w ysize 50
            background Solid(_kc + "22")
            text "[_kn]" align (0.5, 0.5) size 20 color _kc bold True font "DejaVuSans.ttf"

    # ── 音符渲染 ──
    for _ni in range(len(rg.active_notes)):
        $ _n = rg.active_notes[_ni]
        if not _n["hit"] and not _n["missed"]:
            $ _ny = rg.note_y(_n["time"])
            $ _nl = _n["lane"]
            $ _nx = start_x + _nl * lane_w + 20
            $ _nc = RHY_LANE_COLORS[_nl]
            if -30 < _ny < 720:
                frame:
                    xpos _nx ypos _ny
                    xsize (lane_w - 40) ysize 24
                    background Solid(_nc)

    # ── 判定显示 ──
    if ct - rg.last_judge_time < 0.4 and rg.last_judge:
        $ _jc = "#ffd700" if rg.last_judge == "PERFECT" else ("#95e1d3" if rg.last_judge == "GREAT" else ("#6ab8d8" if rg.last_judge == "GOOD" else "#ff4444"))
        text "[rg.last_judge]" xalign 0.5 ypos 280 size 30 color _jc bold True

    # ── Combo ──
    if rg.combo >= 3:
        text "[rg.combo] COMBO" xalign 0.5 ypos 320 size 18 color "#ffd70088" bold True font "DejaVuSans.ttf"

    # ── 分数 ──
    frame:
        xpos 20 ypos 20
        background Solid("#00000066")
        padding (14, 8)
        vbox:
            spacing 2
            text "SCORE" size 10 color "#ffffff44"
            text "[rg.score]" size 22 color "#ffffff" bold True font "DejaVuSans.ttf"

    # ── 左侧：睦的提示 ──
    frame:
        xpos 20 ypos 120
        background None
        padding (0, 0)
        vbox:
            spacing 6
            text "睦在弹主旋律♪" size 10 color "#8FBC8F55"
            if rg.combo >= 10:
                text "很默契呢……" size 11 color "#8FBC8F88"
            elif rg.miss > 5:
                text "没关系，慢慢来。" size 11 color "#8FBC8F88"

    # ── 退出 ──
    textbutton "退出":
        xpos 20 ypos 680
        action [Function(renpy.music.stop), Hide("rhythm_play_screen"), SetVariable("_rhy_game", None)]
        text_size 12 text_color "#ffffff33" text_hover_color "#ff6666"

    # ── 结算画面 ──
    if rg.game_over:
        add Solid("#000000cc")

        frame:
            align (0.5, 0.45)
            xsize 460 ysize 320
            background Solid("#12122af5")
            padding (30, 25)

            $ _rank = rg.get_rank()
            $ _rank_color = "#ffd700" if _rank in ("S", "A") else ("#95e1d3" if _rank == "B" else "#ffffff88")

            vbox:
                spacing 12 xfill True

                text "演奏完毕" size 24 color "#d4a0ff" xalign 0.5 bold True
                add Solid("#d4a0ff33") xsize 200 ysize 2 xalign 0.5

                hbox:
                    xalign 0.5 spacing 30
                    vbox:
                        spacing 2
                        text "评级" size 11 color "#ffffff44" xalign 0.5
                        text "[_rank]" size 48 color _rank_color xalign 0.5 bold True font "DejaVuSans.ttf"
                    vbox:
                        spacing 2
                        text "分数" size 11 color "#ffffff44" xalign 0.5
                        text "[rg.score]" size 28 color "#ffffff" xalign 0.5 font "DejaVuSans.ttf"

                hbox:
                    xalign 0.5 spacing 16
                    text "P:[rg.perfect]" size 13 color "#ffd700"
                    text "Gr:[rg.great]" size 13 color "#95e1d3"
                    text "Go:[rg.good]" size 13 color "#6ab8d8"
                    text "M:[rg.miss]" size 13 color "#ff4444"

                text "最大连击: [rg.max_combo]" size 13 color "#ffffff66" xalign 0.5

                null height 4
                button:
                    xalign 0.5 xsize 160 ysize 40
                    background Solid("#d4a0ff33")
                    hover_background Solid("#d4a0ff55")
                    action [Function(renpy.music.stop), Hide("rhythm_play_screen"), SetVariable("_rhy_game", None)]
                    text "返回" align (0.5, 0.5) size 16 color "#d4a0ff"
