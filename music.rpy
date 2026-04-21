# -----------------------------------------------------------
# 变量初始化
# -----------------------------------------------------------
default playlist_view = "base"   # "base" 为全部, "fav" 为收藏

init python:
    import os
    import shutil
    import random

    # -----------------------------------------------------------------
    # 1. 基础配置
    # -----------------------------------------------------------------
    MUSIC_EXTENSIONS = ('.mp3', '.ogg', '.opus', '.wav')
    
    # 播放模式: 0:顺序, 1:随机, 2:单曲循环
    play_mode = 0 
    mode_names = ["顺序", "随机", "循环"]
    
    current_playing_song = "未在播放"
    
    if not hasattr(persistent, 'favorite_songs') or persistent.favorite_songs is None:
        persistent.favorite_songs = []

    # -----------------------------------------------------------------
    # 2. 路径与文件扫描
    # -----------------------------------------------------------------
    def get_writable_music_dir():
        if renpy.android:
            path = os.path.join(config.savedir, "user_music")
        else:
            path = os.path.join(config.basedir, "user_music")
        
        if not os.path.exists(path):
            try: os.makedirs(path)
            except: pass
        return path

    def get_music_files():
        file_list = []
        # A. 扫描用户目录
        user_dir = get_writable_music_dir()
        if os.path.exists(user_dir):
            try:
                for f in os.listdir(user_dir):
                    if f.lower().endswith(MUSIC_EXTENSIONS):
                        # 🟢【路径修复】强制把反斜杠 \ 换成正斜杠 /，防止Windows报错
                        full_path = os.path.join(user_dir, f).replace("\\", "/")
                        file_list.append({"name": f, "type": "user", "path": full_path})
            except: pass

        # B. 扫描游戏自带目录
        sys_music_path = os.path.join(config.gamedir, "music")
        if os.path.exists(sys_music_path):
            try:
                for f in os.listdir(sys_music_path):
                    if f.lower().endswith(MUSIC_EXTENSIONS):
                        # 相对路径也要确保没有反斜杠
                        rel_path = ("music/" + f).replace("\\", "/")
                        file_list.append({"name": f, "type": "sys", "path": rel_path})
            except: pass
        
        file_list.sort(key=lambda x: x["name"])
        return file_list

    def get_clean_song_name(file_data):
        if isinstance(file_data, dict):
            return os.path.splitext(file_data["name"])[0]
        elif isinstance(file_data, str):
            return os.path.splitext(file_data)[0]
        return str(file_data)

    # -----------------------------------------------------------------
    # 3. 核心播放逻辑 (改为：一次性排队机制)
    # -----------------------------------------------------------------
    def play_user_music(file_data):
        # 1. 解析目标歌曲路径
        target_path = ""
        target_name = ""
        
        if isinstance(file_data, dict):
            target_path = file_data["path"]
            target_name = file_data["name"]
        elif isinstance(file_data, str):
            target_path = "music/" + file_data
            target_name = file_data # 假设只有文件名
        
        if not target_path:
            return

        # 2. 更新当前播放的歌名
        store.current_playing_song = get_clean_song_name(file_data)

        # 3. 准备播放列表 (用于排队下一首)
        # 重新获取当前应该播放的列表 (全部 or 收藏)
        all_songs = get_music_files()
        current_playlist = []
        
        if store.playlist_view == "fav":
            # 筛选出收藏夹里的歌
            current_playlist = [s for s in all_songs if s["name"] in persistent.favorite_songs]
        else:
            current_playlist = all_songs

        # 4. 根据模式执行播放
        # --- 模式 2: 单曲循环 ---
        if play_mode == 2:
            renpy.music.play(target_path, channel="music", loop=True, if_changed=True)
            
        # --- 模式 0 & 1: 顺序/随机 (使用 queue 排队) ---
        else:
            # 先立即播放选中的这一首 (loop=False)
            renpy.music.play(target_path, channel="music", loop=False, if_changed=True)
            
            # 如果列表里只有这一首歌，那就不用排队了
            if len(current_playlist) <= 1:
                return

            # 找到后续要播放的歌曲列表
            queue_list = []
            
            # (A) 顺序播放: 找到当前歌的位置，把后面的歌全排进去，再把前面的歌排到最后(形成循环)
            if play_mode == 0:
                # 找索引
                idx = -1
                for i, s in enumerate(current_playlist):
                    # 通过路径判断是否是当前歌
                    if s["path"] == target_path:
                        idx = i
                        break
                
                if idx != -1:
                    # 队列 = [当前歌后面的歌] + [当前歌前面的歌]
                    # 这样就形成了一个无限循环列表：A -> B -> C -> A -> B ...
                    raw_queue = current_playlist[idx+1:] + current_playlist[:idx]
                    # 提取路径
                    queue_list = [s["path"] for s in raw_queue]

            # (B) 随机播放: 把除了当前歌以外的歌，打乱排队
            elif play_mode == 1:
                # 排除当前歌
                other_songs = [s for s in current_playlist if s["path"] != target_path]
                random.shuffle(other_songs)
                queue_list = [s["path"] for s in other_songs]

            # 5. 执行排队
            if queue_list:
                # 把这一大串歌扔给播放器，告诉它“播完当前这首，就按这个顺序继续播”
                # loop=True 表示整个队列播完后，从头再来 (实现列表循环)
                # 注意：Ren'Py 的 queue 如果列表很长也没关系，它处理得很快
                renpy.music.queue(queue_list, channel="music", loop=True)

    # -----------------------------------------------------------------
    # 4. 其他功能
    # -----------------------------------------------------------------
    def toggle_favorite(song_name):
        if not isinstance(persistent.favorite_songs, list):
            persistent.favorite_songs = []
        if song_name in persistent.favorite_songs:
            persistent.favorite_songs.remove(song_name)
        else:
            persistent.favorite_songs.append(song_name)
        renpy.save_persistent()
        renpy.restart_interaction()

    def toggle_pause():
        is_paused = renpy.music.get_pause(channel='music')
        renpy.music.set_pause(not is_paused, channel='music')
        renpy.restart_interaction()

    def import_music_action():
        """
        弹出系统文件选择对话框，导入音乐文件到 user_music 目录。
        Windows：ctypes 调用 Win32 GetOpenFileNameW（不依赖 tkinter）
        Mac：osascript
        Android：扫描 Download 目录
        """
        target_dir = get_writable_music_dir()

        # ── Android ──
        if renpy.android:
            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                renpy.notify("未找到下载文件夹")
                renpy.restart_interaction()
                return
            count = 0
            try:
                for f in os.listdir(download_path):
                    if f.lower().endswith(MUSIC_EXTENSIONS):
                        src = os.path.join(download_path, f)
                        dst = os.path.join(target_dir, f)
                        if not os.path.exists(dst):
                            shutil.copyfile(src, dst)
                            count += 1
            except: pass
            renpy.notify(f"已导入 {count} 首" if count > 0 else "没找到新音乐")
            renpy.restart_interaction()
            return

        # ── Windows：ctypes 调用 GetOpenFileNameW ──
        if renpy.windows:
            selected = _win_open_file_dialog()
            if selected is None:
                renpy.notify("未选择文件")
                renpy.restart_interaction()
                return
            count, skipped = 0, 0
            for src in selected:
                fname = os.path.basename(src)
                dst = os.path.join(target_dir, fname)
                if os.path.exists(dst):
                    skipped += 1
                    continue
                try:
                    shutil.copyfile(src, dst)
                    count += 1
                except Exception as e:
                    print(f"导入失败: {fname} — {e}")
            if count > 0:
                msg = f"已导入 {count} 首"
                if skipped:
                    msg += f"（{skipped} 首已存在跳过）"
                renpy.notify(msg)
            elif skipped:
                renpy.notify("选中文件已全部存在，无需重复导入")
            else:
                renpy.notify("导入失败，请检查文件")
            renpy.restart_interaction()
            return

        # ── Mac：osascript ──
        if renpy.macintosh:
            selected = _mac_open_file_dialog()
            if selected:
                count, skipped = 0, 0
                for src in selected:
                    fname = os.path.basename(src)
                    dst = os.path.join(target_dir, fname)
                    if os.path.exists(dst):
                        skipped += 1
                        continue
                    try:
                        shutil.copyfile(src, dst)
                        count += 1
                    except: pass
                msg = f"已导入 {count} 首" if count > 0 else "没有新文件"
                if skipped:
                    msg += f"（{skipped} 已存在）"
                renpy.notify(msg)
            else:
                renpy.notify("未选择文件")
            renpy.restart_interaction()
            return

        # ── 兜底：打开文件夹 ──
        try:
            os.startfile(target_dir)
            renpy.notify("已打开音乐文件夹，请手动放入文件")
        except:
            renpy.notify("请手动将音乐文件放入 user_music 文件夹")
        renpy.restart_interaction()

    def _win_open_file_dialog():
        """
        ctypes 调用 Win32 GetOpenFileNameW，弹出原生多选文件对话框。
        返回选中路径列表，取消返回 None。
        用 c_void_p 存所有指针字段，避免 c_wchar_p/buffer 类型不兼容。
        """
        try:
            import ctypes
            import ctypes.wintypes as wt

            # ── 过滤字符串（nul分隔，结尾双nul）──
            filter_pairs = [
                ("音频文件 (mp3/ogg/wav/opus)", "*.mp3;*.ogg;*.wav;*.opus"),
                ("MP3", "*.mp3"),
                ("OGG / Opus", "*.ogg;*.opus"),
                ("WAV", "*.wav"),
                ("所有文件", "*.*"),
            ]
            filter_parts = []
            for desc, ext in filter_pairs:
                filter_parts.append(desc)
                filter_parts.append(ext)
            filter_parts.append("")   # 末尾空字符串产生结束的双nul
            # create_unicode_buffer 用 nul 连接各段
            filter_buf = ctypes.create_unicode_buffer(chr(0).join(filter_parts) + chr(0))

            # ── 结果缓冲区 ──
            buf_size = 32767
            file_buf = ctypes.create_unicode_buffer(buf_size)

            # ── OPENFILENAMEW 结构体（全部指针字段用 c_void_p）──
            class OPENFILENAMEW(ctypes.Structure):
                _fields_ = [
                    ("lStructSize",       wt.DWORD),
                    ("hwndOwner",         wt.HWND),
                    ("hInstance",         wt.HINSTANCE),
                    ("lpstrFilter",       ctypes.c_void_p),
                    ("lpstrCustomFilter", ctypes.c_void_p),
                    ("nMaxCustFilter",    wt.DWORD),
                    ("nFilterIndex",      wt.DWORD),
                    ("lpstrFile",         ctypes.c_void_p),
                    ("nMaxFile",          wt.DWORD),
                    ("lpstrFileTitle",    ctypes.c_void_p),
                    ("nMaxFileTitle",     wt.DWORD),
                    ("lpstrInitialDir",   ctypes.c_void_p),
                    ("lpstrTitle",        ctypes.c_void_p),
                    ("Flags",             wt.DWORD),
                    ("nFileOffset",       wt.WORD),
                    ("nFileExtension",    wt.WORD),
                    ("lpstrDefExt",       ctypes.c_void_p),
                    ("lCustData",         ctypes.c_ssize_t),
                    ("lpfnHook",          ctypes.c_void_p),
                    ("lpTemplateName",    ctypes.c_void_p),
                    ("pvReserved",        ctypes.c_void_p),
                    ("dwReserved",        wt.DWORD),
                    ("FlagsEx",           wt.DWORD),
                ]

            OFN_ALLOWMULTISELECT = 0x00000200
            OFN_EXPLORER         = 0x00080000
            OFN_FILEMUSTEXIST    = 0x00001000
            OFN_PATHMUSTEXIST    = 0x00000800
            OFN_HIDEREADONLY     = 0x00000004

            # ── 标题字符串 buffer ──
            title_buf = ctypes.create_unicode_buffer("选择要导入的音乐文件（可多选）")

            ofn = OPENFILENAMEW()
            ofn.lStructSize  = ctypes.sizeof(OPENFILENAMEW)
            ofn.lpstrFilter  = ctypes.addressof(filter_buf)
            ofn.nFilterIndex = 1
            ofn.lpstrFile    = ctypes.addressof(file_buf)
            ofn.nMaxFile     = buf_size
            ofn.lpstrTitle   = ctypes.addressof(title_buf)
            ofn.Flags        = (OFN_EXPLORER | OFN_ALLOWMULTISELECT |
                                OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_HIDEREADONLY)

            ok = ctypes.windll.comdlg32.GetOpenFileNameW(ctypes.byref(ofn))
            if not ok:
                return None   # 用户取消

            # ── 解析结果缓冲区 ──
            # 多选：第一段=目录，后续=文件名，单选：直接是完整路径
            # 逐字符扫描 nul 分隔片段
            parts = []
            cur = []
            for i in range(buf_size):
                ch = file_buf[i]
                if ch == chr(0):
                    if cur:
                        parts.append("".join(cur))
                        cur = []
                    else:
                        break   # 连续两个 nul，结束
                else:
                    cur.append(ch)

            if not parts:
                return None
            if len(parts) == 1:
                return [parts[0]]               # 单选，直接是完整路径
            else:
                folder = parts[0]
                return [os.path.join(folder, fn) for fn in parts[1:]]   # 多选

        except Exception as e:
            print(f"_win_open_file_dialog 出错: {e}")
            return None

    def _mac_open_file_dialog():
        """Mac 用 osascript 弹出 Finder 文件选择"""
        try:
            import subprocess
            script = (
                'set theFiles to choose file with prompt "选择音乐文件" '
                'of type {"mp3", "ogg", "wav", "opus"} with multiple selections allowed\n'
                'set out to ""\n'
                'repeat with f in theFiles\n'
                '  set out to out & POSIX path of f & linefeed\n'
                'end repeat\n'
                'return out'
            )
            result = subprocess.check_output(
                ["osascript", "-e", script],
                stderr=subprocess.DEVNULL, timeout=120
            ).decode("utf-8").strip()
            if not result:
                return []
            return [p for p in result.splitlines() if p.strip()]
        except Exception as e:
            print(f"_mac_open_file_dialog 出错: {e}")
            return []
