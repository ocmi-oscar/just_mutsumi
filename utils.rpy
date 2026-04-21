# ==============================================================================
# 💾 存档导入导出系统 (M0.3 完整重写版)
# 
# 改进内容：
#   1. 导出数据从17个字段扩展到覆盖全部 persistent 变量
#   2. 完美兼容 M0.2 (v0.21) 存档的导入
#   3. 人格重构数据迁移（苦瓜睦→吉他睦好感度合并）
#   4. 更安全的错误处理和数据校验
# ==============================================================================

init python:
    import json
    import zipfile
    import os
    import time
    import datetime
    from renpy import config

    # --- 1. 版本配置 ---
    EXPORT_FILENAME = "M030_SaveData.zip"
    CURRENT_GAME_VERSION = 0.3

    def parse_version(version_str):
        try:
            clean_str = str(version_str).upper().replace("M", "").replace("V", "")
            return float(clean_str)
        except:
            return 0.0

    def get_transfer_path():
        return config.basedir

    # --- 2. 安全读取工具 ---
    def _safe_get_persistent(attr, default=None):
        """安全读取 persistent 属性，不存在则返回默认值"""
        return getattr(persistent, attr, default)

    def _safe_set_persistent(attr, value):
        """安全设置 persistent 属性"""
        try:
            setattr(persistent, attr, value)
        except:
            pass

    # --- 3. 导出 ---
    def export_save_to_zip():
        try:
            save_dict = {
                "version": "M" + str(CURRENT_GAME_VERSION),
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),

                # ====== 玩家基础信息 ======
                "player_info": {
                    "name": _safe_get_persistent("playername", ""),
                    "gender": _safe_get_persistent("player_gender", "unknown"),
                    "bday_month": _safe_get_persistent("player_bday_month", 0),
                    "bday_day": _safe_get_persistent("player_bday_day", 0),
                },

                # ====== 游戏进度标记 ======
                "flags": {
                    "first_met": _safe_get_persistent("first_met", False),
                    "first_run": _safe_get_persistent("first_run", False),
                    "asked_birthday": _safe_get_persistent("asked_birthday", False),
                    "asked_gender": _safe_get_persistent("asked_gender", False),
                    "asked_real_name": _safe_get_persistent("asked_real_name", False),
                    "ghost_menu": _safe_get_persistent("ghost_menu", False),
                    "developer_mode": _safe_get_persistent("developer_mode", False),
                    "claimed_dev_gift": _safe_get_persistent("claimed_dev_gift", False),
                    "has_clicked_guitar_first_time": _safe_get_persistent("has_clicked_guitar_first_time", False),
                    "player_interested_guitar": _safe_get_persistent("player_interested_guitar", False),
                    "mutsumi_guitar_tutorial_done": _safe_get_persistent("mutsumi_guitar_tutorial_done", False),
                    "last_valentines_year": _safe_get_persistent("last_valentines_year", None),
                },

                # ====== 好感度系统 ======
                "goodwill": {
                    "wakaba": _safe_get_persistent("gw_wakaba", 0.0),
                    "guitar": _safe_get_persistent("gw_guitar", 0.0),
                    "metis": _safe_get_persistent("gw_metis", 0.0),
                    "total": _safe_get_persistent("gw_total", 0.0),
                    "event_flags": _safe_get_persistent("gw_event_flags", {}),
                    "daily_counts": _safe_get_persistent("gw_daily_counts", {}),
                    "last_date": _safe_get_persistent("gw_last_date", ""),
                    "rewards_claimed": _safe_get_persistent("gw_rewards_claimed", 0),
                },

                # ====== 抽卡系统 ======
                "gacha": {
                    "coins": _safe_get_persistent("mutsumi_coins", 0),
                    "pity_6": _safe_get_persistent("gacha_pity_counter", 0),
                    "pity_5": _safe_get_persistent("gacha_pity_5star", 0),
                    "guaranteed": _safe_get_persistent("gacha_guaranteed", False),
                    "inventory": _safe_get_persistent("player_inventory", {}),
                    "current_bg": _safe_get_persistent("current_bg_id", "default"),
                    "last_checkin": str(_safe_get_persistent("last_checkin_date", "")) if _safe_get_persistent("last_checkin_date") else None,
                },

                # ====== 对话系统 ======
                "dialogue": {
                    "seen_random_labels": _safe_get_persistent("seen_random_labels", []),
                    "random_talk_today_count": _safe_get_persistent("random_talk_today_count", 0),
                    "last_talk_reward_date": _safe_get_persistent("last_talk_reward_date", ""),
                    "last_greeting_date": _safe_get_persistent("last_greeting_date", ""),
                    "last_greeting_period": _safe_get_persistent("last_greeting_period", ""),
                    "last_login_date": _safe_get_persistent("last_login_date", ""),
                    "last_time_period_bonus": _safe_get_persistent("last_time_period_bonus", ""),
                    # M0.3新增
                    "last_random_persona": _safe_get_persistent("last_random_persona", "metis"),
                    "last_greeting_persona": _safe_get_persistent("last_greeting_persona", "metis"),
                },

                # ====== Mortis模式 ======
                "mortis": {
                    "love": _safe_get_persistent("mortis_love", 0),
                    "sanity": _safe_get_persistent("mortis_sanity", 100),
                    "loop_count": _safe_get_persistent("mortis_loop_count", 1),
                    "in_mortis_mode": _safe_get_persistent("in_mortis_mode", False),
                    "played_before": _safe_get_persistent("played_mortis_before", False),
                    "true_end_clear": _safe_get_persistent("mortis_true_end_phase1_clear", False),
                    "seen_ed": _safe_get_persistent("seen_mortis_ed", False),
                    "got_coins": _safe_get_persistent("got_mortis_coins", False),
                    "system_destroyed": _safe_get_persistent("system_destroyed", False),
                    "rewind_triggered": _safe_get_persistent("mortis_rewind_triggered", False),
                    "unlock_free_mode": _safe_get_persistent("m_unlock_free_mode", False),
                    "seen_daytime": _safe_get_persistent("m_seen_daytime", None),
                    "seen_sunset": _safe_get_persistent("m_seen_sunset", None),
                    # 问答系统
                    "mq_initialized": _safe_get_persistent("mq_initialized", False),
                    "mq_answers": _safe_get_persistent("mq_answers", {}),
                },

                # ====== 应用数据 ======
                "apps": {
                    "player_notes": _safe_get_persistent("player_notes", []),
                    "todo_list": _safe_get_persistent("todo_list", []),
                    "favorite_songs": _safe_get_persistent("favorite_songs", []),
                },

                # ====== 兑换码 ======
                "redeem": {
                    # set 不能直接 JSON 序列化，转为 list
                    "redeemed_codes": list(_safe_get_persistent("redeemed_codes", set())),
                },

                # ====== 进程检测 ======
                "process_detect": {
                    "last_process_date": _safe_get_persistent("last_process_date", ""),
                    "last_bgm_check_date": _safe_get_persistent("last_bgm_check_date", ""),
                },
            }

            file_path = os.path.join(get_transfer_path(), EXPORT_FILENAME)
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                json_str = json.dumps(save_dict, indent=2, ensure_ascii=False, default=str)
                zf.writestr("data.json", json_str)
                zf.writestr("说明.txt",
                    "这是《Just Mutsumi》M{} 版本的存档数据。\n".format(CURRENT_GAME_VERSION) +
                    "导出时间：{}\n".format(save_dict["date"]) +
                    "使用方法：将此ZIP文件放入游戏根目录，在游戏内点击'导入存档'。"
                )

            store.save_manager_msg = "导出成功！\n文件：" + EXPORT_FILENAME + "\n路径：" + get_transfer_path()

        except Exception as e:
            store.save_manager_msg = "导出失败: " + str(e)

        renpy.restart_interaction()

    # --- 4. 导入（兼容 M0.2 和 M0.3） ---
    def import_save_from_zip():

        # 尝试查找存档文件（优先M0.3，其次M0.2）
        path_m03 = os.path.join(get_transfer_path(), "M030_SaveData.zip")
        path_m02 = os.path.join(get_transfer_path(), "M021_SaveData.zip")

        if os.path.exists(path_m03):
            file_path = path_m03
        elif os.path.exists(path_m02):
            file_path = path_m02
        else:
            store.save_manager_msg = "未找到存档文件！\n请将 M030_SaveData.zip 或 M021_SaveData.zip\n放入游戏根目录。"
            renpy.restart_interaction()
            return

        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                if "data.json" not in zf.namelist():
                    store.save_manager_msg = "无效存档：缺少 data.json"
                    renpy.restart_interaction()
                    return

                json_bytes = zf.read("data.json")
                data = json.loads(json_bytes.decode('utf-8'))

                save_ver = parse_version(data.get('version', '0'))

                if save_ver > CURRENT_GAME_VERSION:
                    store.save_manager_msg = "版本不兼容：\n存档版本 (M{}) 高于游戏版本 (M{})".format(save_ver, CURRENT_GAME_VERSION)
                    renpy.restart_interaction()
                    return

                # ==========================================
                # 判断存档格式版本并分流处理
                # ==========================================
                if save_ver <= 0.21:
                    _import_v021(data)
                else:
                    _import_v030(data)

                renpy.save_persistent()
                store.save_manager_msg = "导入成功！\n来自 M{} 版本的存档已恢复。".format(save_ver)

        except Exception as e:
            store.save_manager_msg = "导入错误: " + str(e)

        renpy.restart_interaction()

    # --- 4a. M0.2 (v0.21) 格式导入 ---
    def _import_v021(data):
        """
        M0.2 存档结构：
        - player_info: {name, gender, bday_month, bday_day, flags: {asked_*, played_mortis_before}}
        - goodwill: {wakaba, guitar, metis}
        - assets: {money, inventory}
        - notebook: [...]
        - gacha: {coins, pity_6, pity_5, rewards_claimed, inventory, current_bg, last_checkin}
        
        M0.2 存档中 **缺失** 的重要数据：
        - gw_event_flags（一次性好感度记录）
        - seen_random_labels（已看对话记录）
        - first_met, redeemed_codes, todo_list, favorite_songs
        - 全部 mortis 相关数据
        - 全部日期记录
        """

        # ---- 玩家信息 ----
        p_info = data.get('player_info', {})
        persistent.playername = p_info.get('name', '')
        persistent.player_gender = p_info.get('gender', 'unknown')
        persistent.player_bday_month = p_info.get('bday_month', 0)
        persistent.player_bday_day = p_info.get('bday_day', 0)

        p_flags = p_info.get('flags', {})
        persistent.asked_birthday = p_flags.get('asked_birthday', False)
        persistent.asked_gender = p_flags.get('asked_gender', False)
        persistent.asked_real_name = p_flags.get('asked_real_name', False)
        persistent.played_mortis_before = p_flags.get('played_mortis_before', False)

        # 如果有玩家名字，说明肯定经历过初见
        if persistent.playername:
            persistent.first_met = True

        # ---- 好感度（★ 人格重构迁移 ★）----
        gw = data.get('goodwill', {})
        old_wakaba = gw.get('wakaba', 0.0)  # 旧的苦瓜睦
        old_guitar = gw.get('guitar', 0.0)  # 旧的吉他睦
        old_metis = gw.get('metis', 0.0)    # 墨缇斯

        # M0.3合并策略：若叶睦(新) = max(苦瓜睦, 吉他睦) + min(苦瓜睦, 吉他睦) * 0.5
        # 这样两个旧人格的好感度都不会被完全浪费
        persistent.gw_wakaba = round(max(old_wakaba, old_guitar) + min(old_wakaba, old_guitar) * 0.5, 1)
        persistent.gw_guitar = 0.0  # 废弃，保留变量防崩溃
        persistent.gw_metis = old_metis
        persistent.gw_total = round(persistent.gw_wakaba + persistent.gw_metis, 1)

        # ---- 抽卡系统 ----
        g_data = data.get('gacha', {})
        persistent.mutsumi_coins = g_data.get('coins', 0)
        persistent.gacha_pity_counter = g_data.get('pity_6', 0)
        persistent.gacha_pity_5star = g_data.get('pity_5', 0)
        persistent.gw_rewards_claimed = g_data.get('rewards_claimed', 0)
        persistent.player_inventory = g_data.get('inventory', {})
        persistent.current_bg_id = g_data.get('current_bg', 'default')

        date_str = g_data.get('last_checkin')
        if date_str:
            try:
                persistent.last_checkin_date = datetime.datetime.strptime(str(date_str), "%Y-%m-%d").date()
            except:
                persistent.last_checkin_date = None
        else:
            persistent.last_checkin_date = None

        # ---- 笔记 ----
        persistent.player_notes = data.get('notebook', [])

        # ---- M0.2中缺失的数据 → 不覆盖（保留当前游戏中的值）----
        # gw_event_flags, seen_random_labels, todo_list, favorite_songs,
        # redeemed_codes, mortis相关 → 全部不动，让 init 的默认值处理


    # --- 4b. M0.3 格式导入 ---
    def _import_v030(data):
        """M0.3 完整存档导入"""

        # ---- 玩家信息 ----
        p = data.get('player_info', {})
        persistent.playername = p.get('name', '')
        persistent.player_gender = p.get('gender', 'unknown')
        persistent.player_bday_month = p.get('bday_month', 0)
        persistent.player_bday_day = p.get('bday_day', 0)

        # ---- 进度标记 ----
        f = data.get('flags', {})
        persistent.first_met = f.get('first_met', False)
        persistent.first_run = f.get('first_run', False)
        persistent.asked_birthday = f.get('asked_birthday', False)
        persistent.asked_gender = f.get('asked_gender', False)
        persistent.asked_real_name = f.get('asked_real_name', False)
        persistent.ghost_menu = f.get('ghost_menu', False)
        persistent.developer_mode = f.get('developer_mode', False)
        persistent.claimed_dev_gift = f.get('claimed_dev_gift', False)
        persistent.has_clicked_guitar_first_time = f.get('has_clicked_guitar_first_time', False)
        persistent.player_interested_guitar = f.get('player_interested_guitar', False)
        persistent.mutsumi_guitar_tutorial_done = f.get('mutsumi_guitar_tutorial_done', False)
        persistent.last_valentines_year = f.get('last_valentines_year', None)

        # ---- 好感度 ----
        gw = data.get('goodwill', {})
        persistent.gw_wakaba = gw.get('wakaba', 0.0)
        persistent.gw_guitar = gw.get('guitar', 0.0)
        persistent.gw_metis = gw.get('metis', 0.0)
        persistent.gw_total = gw.get('total', 0.0)
        persistent.gw_event_flags = gw.get('event_flags', {})
        persistent.gw_daily_counts = gw.get('daily_counts', {})
        persistent.gw_last_date = gw.get('last_date', '')
        persistent.gw_rewards_claimed = gw.get('rewards_claimed', 0)

        # ---- 抽卡 ----
        g = data.get('gacha', {})
        persistent.mutsumi_coins = g.get('coins', 0)
        persistent.gacha_pity_counter = g.get('pity_6', 0)
        persistent.gacha_pity_5star = g.get('pity_5', 0)
        persistent.gacha_guaranteed = g.get('guaranteed', False)
        persistent.player_inventory = g.get('inventory', {})
        persistent.current_bg_id = g.get('current_bg', 'default')

        date_str = g.get('last_checkin')
        if date_str and date_str != "None":
            try:
                persistent.last_checkin_date = datetime.datetime.strptime(str(date_str), "%Y-%m-%d").date()
            except:
                persistent.last_checkin_date = None
        else:
            persistent.last_checkin_date = None

        # ---- 对话系统 ----
        d = data.get('dialogue', {})
        persistent.seen_random_labels = d.get('seen_random_labels', [])
        persistent.random_talk_today_count = d.get('random_talk_today_count', 0)
        persistent.last_talk_reward_date = d.get('last_talk_reward_date', '')
        persistent.last_greeting_date = d.get('last_greeting_date', '')
        persistent.last_greeting_period = d.get('last_greeting_period', '')
        persistent.last_login_date = d.get('last_login_date', '')
        persistent.last_time_period_bonus = d.get('last_time_period_bonus', '')
        persistent.last_random_persona = d.get('last_random_persona', 'metis')
        persistent.last_greeting_persona = d.get('last_greeting_persona', 'metis')

        # ---- Mortis模式 ----
        m = data.get('mortis', {})
        persistent.mortis_love = m.get('love', 0)
        persistent.mortis_sanity = m.get('sanity', 100)
        persistent.mortis_loop_count = m.get('loop_count', 1)
        persistent.in_mortis_mode = m.get('in_mortis_mode', False)
        persistent.played_mortis_before = m.get('played_before', False)
        persistent.mortis_true_end_phase1_clear = m.get('true_end_clear', False)
        persistent.seen_mortis_ed = m.get('seen_ed', False)
        persistent.got_mortis_coins = m.get('got_coins', False)
        persistent.system_destroyed = m.get('system_destroyed', False)
        persistent.mortis_rewind_triggered = m.get('rewind_triggered', False)
        persistent.m_unlock_free_mode = m.get('unlock_free_mode', False)
        persistent.m_seen_daytime = m.get('seen_daytime', None)
        persistent.m_seen_sunset = m.get('seen_sunset', None)
        persistent.mq_initialized = m.get('mq_initialized', False)
        persistent.mq_answers = m.get('mq_answers', {})

        # ---- 应用数据 ----
        apps = data.get('apps', {})
        persistent.player_notes = apps.get('player_notes', [])
        persistent.todo_list = apps.get('todo_list', [])
        persistent.favorite_songs = apps.get('favorite_songs', [])

        # ---- 兑换码 ----
        r = data.get('redeem', {})
        codes_list = r.get('redeemed_codes', [])
        persistent.redeemed_codes = set(codes_list) if isinstance(codes_list, list) else set()

        # ---- 进程检测 ----
        pd = data.get('process_detect', {})
        persistent.last_process_date = pd.get('last_process_date', '')
        persistent.last_bgm_check_date = pd.get('last_bgm_check_date', '')
