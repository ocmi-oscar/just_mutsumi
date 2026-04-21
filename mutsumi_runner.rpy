################################################################################
#  小 睦 快 跑  —  Mutsumi Runner
#  Ren'Py 8.2.3  |  黑白像素风  |  五幕线型叙事跑酷
#
#  Round 1  教程   横2D(30s) → 竖2D(25s) → 伪3D(25s)
#  Round 2  伪3D   跑酷 + Boss 长崎爽世
#  Round 3  竖2D   弹幕 + Boss 丰川祥子
#  Round 4  横2D   跑酷 + Boss 墨缇斯(Mortis)
#  Round 5  横2D   结局致谢滚动
#
#  注意：screen 语言中 text / add 语句不能反斜杠续行，全部写成单行。
################################################################################

# ── 小睦快跑 专用样式（不影响主游戏）──────────────────────────────────────

style mr_text:
    font "run.otf"
    outlines []

style mr_button_text:
    font "run.otf"
    outlines []

style mr_label_text:
    font "run.otf"
    outlines []

style mr_input:
    font "run.otf"
    outlines []

style ed_text:
    font "end.ttf"

################################################################################
#  Python 逻辑层
################################################################################
init python:
    import random, time as _time, math

    # ── 屏幕常量 ─────────────────────────────────────────────
    SW, SH = 1280, 720

    # 横版2D
    H_GY   = 570
    H_PX   = 160
    H_PW   = 38
    H_PH_N = 52
    H_PH_D = 26
    H_GRAV = 1600.0
    H_JVY  = -760.0

    # 竖版弹幕
    V2_AREA_X = (SW - 480) // 2
    V2_AREA_W = 480
    V2_AREA_H = SH
    V2_SPD    = 260.0
    V2_PW     = 36
    V2_PH     = 36

    # 伪3D
    P3_LANES  = 3
    P3_LANE_W = 180
    P3_CX     = SW // 2
    P3_VPY    = 220
    P3_BOT_Y  = SH - 60


    # ══════════════════════════════════════════════════════════
    #  持久化存档（跨会话保存）
    # ══════════════════════════════════════════════════════════
    def _load_persistent():
        """从 Ren'Py persistent 对象读取存档数据"""
        if not hasattr(persistent, 'tutorial_cleared'):
            persistent.tutorial_cleared    = False
        if not hasattr(persistent, 'unlocked_hard'):
            persistent.unlocked_hard       = False
        if not hasattr(persistent, 'unlocked_extreme'):
            persistent.unlocked_extreme    = False
        if not hasattr(persistent, 'best_diff_cleared') or persistent.best_diff_cleared is None:
            persistent.best_diff_cleared   = -1
        if not hasattr(persistent, 'dev_unlocked'):
            persistent.dev_unlocked        = False

    def _save_persistent():
        renpy.save_persistent()

    _load_persistent()

    # ── 科乐美秘技解锁DEV模式 ─────────────────────────────
    # 序列：↑↑↓↓←←→→AB（键名列表）
    _KONAMI_SEQ = ["K_UP","K_UP","K_DOWN","K_DOWN",
                   "K_LEFT","K_RIGHT","K_LEFT","K_RIGHT",
                   "K_b","K_a","K_b","K_a"]
    store._konami_buf  = []   # 已输入的序列缓冲
    store._dev_popup   = False  # 是否显示确认弹窗

    def _quit_to_title():
        """停止死亡音乐，清空BGM状态，返回标题"""
        renpy.music.stop(fadeout=0.5)
        store._current_bgm     = None
        store._death_bgm_pos   = 0.0
        store._death_bgm_track = None
        GM.__init__()

    def _konami_input(key):
        """科乐美秘技输入处理"""
        if DEV.enabled: return
        buf = store._konami_buf
        if len(buf) >= len(_KONAMI_SEQ):
            store._konami_buf = []
            return
        expected = _KONAMI_SEQ[len(buf)]
        if key == expected:
            buf.append(key)
            if len(buf) == len(_KONAMI_SEQ):
                store._dev_popup = True   # 弹出确认弹窗，不直接开启
        else:
            store._konami_buf = [key] if key == _KONAMI_SEQ[0] else []

    # ══════════════════════════════════════════════════════════
    #  全局：难度系统
    # ══════════════════════════════════════════════════════════
    class DifficultySystem(python_object):
        """
        EASY   — 无限免费复活，难度同普通
        NORMAL — 消耗20黄瓜复活一次，标准难度
        HARD   — 消耗30黄瓜复活一次，速度更快，压力衰减更慢（需通关普通解锁）
        EXTREME— 无复活，压力不衰减（需通关困难解锁）
        """
        EASY    = 0
        NORMAL  = 1
        HARD    = 2
        EXTREME = 3

        NAMES = ["简单", "普通", "困难", "极限"]
        DESCS = [
            "无限复活  速度普通  压力正常",
            "消耗20🥒复活  速度普通  压力正常",
            "消耗30🥒复活  吃🥒降压  速度↑",
            "无复活  吃🥒降压  速度极限",
        ]

        def __init__(self):
            self.current       = self.NORMAL
            # 从 persistent 恢复解锁状态
            self.unlocked_hard    = persistent.unlocked_hard
            self.unlocked_extreme = persistent.unlocked_extreme

        def select(self, level):
            self.current = level

        def unlock_hard(self):
            self.unlocked_hard = True
            persistent.unlocked_hard = True
            _save_persistent()

        def unlock_extreme(self):
            self.unlocked_extreme = True
            persistent.unlocked_extreme = True
            _save_persistent()

        # ── 难度系数读取接口 ──────────────────────────────
        @property
        def h_spd_mult(self):
            """横版初速倍率"""
            return {self.EASY: 1.0, self.NORMAL: 1.0,
                    self.HARD: 1.31, self.EXTREME: 1.55}[self.current]

        @property
        def h_spd_max(self):
            """横版最高速度"""
            return {self.EASY: 700.0, self.NORMAL: 700.0,
                    self.HARD: 850.0, self.EXTREME: 950.0}[self.current]

        @property
        def h_spwn_mult(self):
            """横版生成间隔倍率（越小越密）"""
            return {self.EASY: 1.0, self.NORMAL: 1.0,
                    self.HARD: 0.65, self.EXTREME: 0.5}[self.current]

        @property
        def v2_wave_interval(self):
            """竖版波次间隔（秒）"""
            return {self.EASY: 2.5, self.NORMAL: 2.5,
                    self.HARD: 1.2, self.EXTREME: 0.85}[self.current]

        @property
        def v2_bullet_spd_mult(self):
            """竖版子弹速度倍率"""
            return {self.EASY: 1.0, self.NORMAL: 1.0,
                    self.HARD: 1.3, self.EXTREME: 1.5}[self.current]

        @property
        def p3_obs_spd_mult(self):
            """伪3D障碍速度倍率"""
            return {self.EASY: 1.0, self.NORMAL: 1.0,
                    self.HARD: 1.3, self.EXTREME: 1.6}[self.current]

        @property
        def pressure_decay(self):
            """压力衰减速率"""
            return {self.EASY: 2.0, self.NORMAL: 2.0,
                    self.HARD: 1.0, self.EXTREME: 0.0}[self.current]

        @property
        def revive_cost(self):
            """复活所需黄瓜数"""
            return {self.EASY: 0, self.NORMAL: 20,
                    self.HARD: 30, self.EXTREME: 9999}[self.current]

        @property
        def obs_pressure(self):
            """障碍物受击压力"""
            return {self.EASY: 18.0, self.NORMAL: 18.0,
                    self.HARD: 26.0, self.EXTREME: 30.0}[self.current]

        @property
        def bullet_pressure(self):
            """弹幕受击压力（墨缇斯）"""
            return {self.EASY: 12.0, self.NORMAL: 12.0,
                    self.HARD: 15.0, self.EXTREME: 18.0}[self.current]

        @property
        def invincible_dur(self):
            """受击无敌帧时长"""
            return {self.EASY: 1.8, self.NORMAL: 1.8,
                    self.HARD: 0.8, self.EXTREME: 0.5}[self.current]

        @property
        def invert_pressure_rate(self):
            """反转模式每秒压力"""
            return {self.EASY: 4.0, self.NORMAL: 4.0,
                    self.HARD: 6.0, self.EXTREME: 1.5}[self.current]

        @property
        def fake_cursor_pressure_rate(self):
            """假鼠标接近每秒压力"""
            return {self.EASY: 7.0, self.NORMAL: 7.0,
                    self.HARD: 10.0, self.EXTREME: 13.0}[self.current]

        @property
        def cuke_heals_pressure(self):
            """困难/极限模式：吃黄瓜降压值"""
            if self.current == self.EXTREME: return 2.0
            if self.current == self.HARD: return 1.0
            return 0.0

        @property
        def can_revive_free(self):
            """简单模式无限免费复活"""
            return self.current == self.EASY

        @property
        def has_revive_limit(self):
            """极限模式无复活"""
            return self.current == self.EXTREME

    DIFF = DifficultySystem()

    # ══════════════════════════════════════════════════════════
    #  开发者系统
    # ══════════════════════════════════════════════════════════
    class DevSystem(python_object):
        def __init__(self):
            self.enabled         = False
            self.god_mode        = False
            self.invincible      = False
            self.inf_cukes       = False
            self.no_pressure     = False
            self.force_tutorial  = False
            self._skip_cd        = 0.0
            self.demo_mode       = False
            self._demo_grid_cd   = 0.0
            self._demo_grid_path = []
            self._demo_sling_cd  = 0.0
            self._demo_invert_cd = 0.0
            self._demo_duck_held  = False
            self._demo_duck_timer = 0.0
            self.panel_open       = True  # 面板显示状态（图标永久，面板可收起）

        def tick(self, dt):
            if self.inf_cukes:
                CUKES.collected = 999
            if self.no_pressure or self.invincible:
                PRESSURE.value = 0.0
            if self._skip_cd > 0:
                self._skip_cd -= dt
            if self.demo_mode:
                self._demo_tick(dt)

        def _demo_tick(self, dt):
            """演示模式 AI：自动游玩所有场景"""
            import math as _dm
            p = GM.phase

            # ── 横版跑酷 AI ─────────────────────────────────
            if p in ("tut_h", "r2_h", "r3_h", "r4_h"):
                h = GM._h
                if h.dead or h.round_clear: return
                _px = getattr(h, 'px', H_PX)
                # 预判距离随速度动态调整，确保有足够时间反应
                _look      = h.spd * 0.65
                _jump_dist = h.spd * 0.38   # 在此距离内触发跳跃

                _need_jump   = False
                _need_duck   = False
                _do_invert   = False
                _do_uninvert = False

                # 场上是否还有反转墙在前方
                _invert_ahead = any(
                    e.invert_required and e.x > _px - 20
                    for e in h.obs if not e.is_cucumber
                )

                for e in h.obs:
                    if e.is_cucumber: continue
                    _dist = e.x - _px
                    _right_edge = e.x + e.w - _px

                    # ── 反转墙：临近时切换，过了立即还原 ──
                    if e.invert_required:
                        if 0 < _dist < _jump_dist and not invert_mode[0]:
                            _do_invert = True
                        if _right_edge < -30 and invert_mode[0] and not _invert_ahead:
                            _do_uninvert = True
                        continue

                    if not (0 < _dist < _look):
                        continue

                    _tag = getattr(e, 'tag', '')

                    if _tag == "air":
                        # 空中障碍：触发蹲并重置持续计时器
                        if _dist < _jump_dist:
                            _need_duck = True
                            # 根据障碍宽度计算需要蹲多久（宽度/速度 + 余量）
                            _duck_needed = (e.w + 60) / max(1.0, h.spd)
                            self._demo_duck_timer = max(self._demo_duck_timer, _duck_needed)
                    else:
                        # 地面障碍 / 文字墙 → 跳
                        if _dist < _jump_dist:
                            _need_jump = True

                # 执行反转操作（CD防抖）
                if self._demo_invert_cd > 0:
                    self._demo_invert_cd -= dt
                if (_do_invert or _do_uninvert) and self._demo_invert_cd <= 0:
                    toggle_invert()
                    self._demo_invert_cd = 0.4

                # 执行跳/蹲
                # 计时器倒计时
                if self._demo_duck_timer > 0:
                    self._demo_duck_timer -= dt
                    _need_duck = True

                if _need_jump and not h.jumping and not h.ducking:
                    # 墨缇斯阶段1/2：蹲着更安全，不要跳
                    if not (getattr(h, 'mortis_active', False) and getattr(h, 'mortis_phase', 0) in (1, 2)):
                        h.do_jump()
                if _need_duck:
                    self._demo_duck_held = True
                    if h.jumping:
                        h.vy = max(h.vy, H_GRAV * 0.55)
                else:
                    self._demo_duck_held = False
                    self._demo_duck_timer = 0.0

                # 跳跃后越过障碍立即快速落地
                if h.jumping and h.vy > 0:
                    _still_threat = any(
                        not e.is_cucumber and _px < e.x + e.w and e.x < _px + 80
                        for e in h.obs
                    )
                    if not _still_threat:
                        h.vy = max(h.vy, H_GRAV * 0.55)

                # Mortis战X轴移动——寻找最安全列 + 绿条排斥
                if getattr(h, 'mortis_active', False) and getattr(h, 'px_free', False):
                    import math as _dm_m
                    _bullets  = getattr(h, '_mortis_bullets', [])
                    _cx       = getattr(h, 'px', H_PX)
                    _mp_now   = getattr(h, 'mortis_phase', 0)
                    _prog     = getattr(h, '_progress_x', -60.0)

                    # ── 阶段一提前右靠（为阶段二留空间）──────────
                    if _mp_now == 1:
                        _target_x = SW * 0.72
                    elif _mp_now == 2:
                        # 阶段二安全区：绿条右侧200px起
                        _safe_left = max(_prog + 180, SW * 0.55)
                        _target_x  = min(float(SW - 100), _safe_left + 80)
                    else:
                        _target_x = SW * 0.5

                    # ── 扫描X轴，找威胁最低的目标列 ─────────────
                    # 把屏幕分成若干列，统计每列的弹幕威胁
                    _COLS      = 10
                    _col_w     = SW / _COLS
                    _col_threat= [0.0] * _COLS
                    _LOOK_AHEAD= 0.45   # 预判秒数

                    # 阶段二：绿条左侧的列直接标为极度危险
                    for _ci in range(_COLS):
                        _col_cx = (_ci + 0.5) * _col_w
                        if _mp_now == 2 and _col_cx < _prog + 120:
                            _col_threat[_ci] += 9999.0

                    for _bl in _bullets:
                        _bx  = _bl[0]; _by  = _bl[1]
                        _bvx = _bl[2]; _bvy = _bl[3]
                        if _by > H_GY + 20: continue
                        # 预测未来位置
                        _pbx = _bx + _bvx * _LOOK_AHEAD
                        _pby = _by + _bvy * _LOOK_AHEAD
                        # 只在即将到达玩家高度时才计入威胁
                        _player_y = h.py + H_PH_N * 0.5
                        if not (0 < _pby < _player_y + 80): continue
                        # 把威胁分摊到附近的列
                        for _col_i in range(_COLS):
                            _col_cx = (_col_i + 0.5) * _col_w
                            _dist   = abs(_pbx - _col_cx)
                            if _dist < _col_w * 1.5:
                                _col_threat[_col_i] += max(0.0, 1.0 - _dist / (_col_w * 1.5))

                    # 找安全区内威胁最低的列
                    _best_col  = -1
                    _best_score= 99999.0
                    for _ci in range(_COLS):
                        _col_cx = (_ci + 0.5) * _col_w
                        # 阶段二：必须在绿条右侧
                        if _mp_now == 2 and _col_cx < _prog + 120:
                            continue
                        # 距屏幕边缘太近也不选
                        if _col_cx < 80 or _col_cx > SW - 80:
                            continue
                        # 综合评分：威胁 + 距目标位置的偏差
                        _dist_target = abs(_col_cx - _target_x) / SW
                        _score = _col_threat[_ci] + _dist_target * 0.8
                        if _score < _best_score:
                            _best_score = _score
                            _best_col   = _ci

                    if _best_col >= 0:
                        _aim_x = (_best_col + 0.5) * _col_w
                    else:
                        _aim_x = _target_x

                    # 向目标列快速移动
                    _dx_to_aim = _aim_x - _cx
                    _accel = 1400.0 if abs(_dx_to_aim) > 80 else 600.0
                    h.pvx += (_dx_to_aim / max(1.0, abs(_dx_to_aim))) * _accel * dt
                    h.pvx *= 0.80   # 摩擦

                    # 蹲姿（阶段1/2缩小判定）
                    if _mp_now in (1, 2):
                        self._demo_duck_held = True
                    else:
                        self._demo_duck_held = False

                # Mortis阶段三弹弓自动射击
                if getattr(h, 'mortis_phase', 0) == 3 and not getattr(h, '_sling_held', False):
                    self._demo_sling_cd -= dt
                    if self._demo_sling_cd <= 0:
                        _targets = [bc for bc in h._boss_chars if bc["hp"] > 0]
                        if _targets:
                            _t = min(_targets, key=lambda b: b["hp"])
                            _tx = _t["x"] + 40; _ty = _t["y"] + 40
                            _ox = getattr(h, 'px', H_PX)
                            _oy = h.py + H_PH_N * 0.4
                            # 简单预判：往目标方向拉200px
                            _dx = _ox - _tx; _dy = _oy - _ty
                            _dist2 = max(1, _dm.hypot(_dx, _dy))
                            _pull = min(200.0, _dist2)
                            _spd_v = 380.0 + _pull * 1.5
                            h._cukes_flying.append([
                                float(_ox), float(_oy),
                                (_dx / _dist2) * _spd_v,
                                (_dy / _dist2) * _spd_v
                            ])
                            self._demo_sling_cd = 1.2

            # ── 竖版弹幕 AI ──────────────────────────────────
            elif p in ("tut_v2", "r2_v2", "r3_v2"):
                v2 = GM._v2
                if v2.dead or v2.round_clear: return
                _px2 = v2.px; _py2 = v2.py
                import math as _dm2

                # ── 预测式弹幕躲避 ──────────────────────────────
                # 对每颗子弹预判0.4秒后位置，构建危险力场
                _PREDICT = 0.4        # 预判时间
                _SAFE_R  = 55.0       # 安全距离（比致命半径18大很多）
                _AREA_W  = float(V2_AREA_W)
                _AREA_H  = float(V2_AREA_H)
                _MAX_PY  = _AREA_H * 0.70 - V2_PH if (
                    hasattr(v2, 'sakiko_boss') and v2.sakiko_boss.active
                    and v2.sakiko_boss.phase == 1) else (_AREA_H - V2_PH // 2)

                # 计算排斥力：离每颗危险弹越近，推力越大
                _fx_total = 0.0
                _fy_total = 0.0
                for b in v2.bullets:
                    _bx = b.x + b.w * 0.5
                    _by = b.y + b.h * 0.5
                    # 预测未来位置
                    _pbx = _bx + b.vx * _PREDICT
                    _pby = _by + b.vy * _PREDICT
                    # 用当前+预测中的最近点计算威胁
                    for _tx, _ty in [(_bx, _by), (_pbx, _pby)]:
                        _dx = _px2 - _tx
                        _dy = _py2 - _ty
                        _d  = _dm2.hypot(_dx, _dy)
                        if _d < _SAFE_R * 2.5 and _d > 0.1:
                            # 反平方力场：越近推力越强
                            _force = (_SAFE_R * 2.5 - _d) / (_SAFE_R * 2.5)
                            _force = _force * _force * 600.0
                            _fx_total += (_dx / _d) * _force
                            _fy_total += (_dy / _d) * _force

                # 祥子Boss阶段：把X轴中心引力替换成朝祥子方向的引力
                _sak_target_x = _AREA_W * 0.5
                if (hasattr(v2, 'sakiko_boss') and v2.sakiko_boss.active
                        and not getattr(v2.sakiko_boss, 'stunned', False)):
                    _sak_target_x = v2.sakiko_boss.sakiko_x

                # 加入向祥子x + 屏幕中心y的引力
                _cx2 = _sak_target_x
                _cy2 = _AREA_H * 0.55
                _fx_total += (_cx2 - _px2) * 1.2   # x轴强力跟随祥子
                _fy_total += (_cy2 - _py2) * 0.6

                # 归一化并应用移动
                _fmag = _dm2.hypot(_fx_total, _fy_total)
                if _fmag > 1.0:
                    _spd_ai = min(_fmag, 380.0)   # 限速
                    _mv_x = (_fx_total / _fmag) * _spd_ai * dt
                    _mv_y = (_fy_total / _fmag) * _spd_ai * dt
                    v2.move_player(_mv_x, _mv_y)

                # 祥子Boss AI
                sb = v2.sakiko_boss
                if sb.active and not sb.round_clear:
                    if sb.phase == 1:
                        # 走格子 AI：BFS找路走，优先未踩蓝格
                        self._demo_grid_cd -= dt
                        if self._demo_grid_cd <= 0:
                            _cr, _cc = sb.grid_cursor
                            _gr, _gc = sb.grid_slot
                            _haz = {tuple(hz) for hz in sb.hazards}
                            # 决定目标格：优先未踩蓝格
                            _blues_todo = []
                            for _bdef, _bvis in [
                                (sb.blue_cell,  sb.blue_visited),
                                (sb.blue_cell2, sb.blue_visited2),
                            ]:
                                if not _bvis and _bdef != [-1,-1]:
                                    _blues_todo.append(tuple(_bdef))
                            if getattr(sb, '_three_blue_active', False):
                                if not getattr(sb, 'blue_visited3', False) and sb.blue_cell3 != [-1,-1]:
                                    _blues_todo.append(tuple(sb.blue_cell3))
                            _target_cell = _blues_todo[0] if _blues_todo else (_gr, _gc)
                            # BFS
                            if (_cr, _cc) != _target_cell:
                                from collections import deque as _dq2
                                _q2  = _dq2([((_cr,_cc), [])])
                                _vis2 = {(_cr,_cc)}
                                _found2 = None
                                while _q2 and not _found2:
                                    (_r2,_c2), _pth = _q2.popleft()
                                    if (_r2,_c2) == _target_cell:
                                        _found2 = _pth; break
                                    for _ddr,_ddc in [(-1,0),(1,0),(0,-1),(0,1)]:
                                        _nr,_nc = _r2+_ddr, _c2+_ddc
                                        if 0<=_nr<5 and 0<=_nc<5 and (_nr,_nc) not in _vis2 and (_nr,_nc) not in _haz:
                                            _vis2.add((_nr,_nc))
                                            _q2.append(((_nr,_nc), _pth+[(_ddr,_ddc)]))
                                if _found2:
                                    sb.move_cursor(_found2[0][0], _found2[0][1])
                                    self._demo_grid_cd = 0.28
                                else:
                                    self._demo_grid_cd = 0.15  # 被堵住时快速重试
                    elif sb.phase == 2:
                        # 打字 AI
                        self._demo_grid_cd -= dt
                        if sb._cur_word and len(sb._typed) < len(sb._cur_word) and self._demo_grid_cd <= 0:
                            _next_ch = sb._cur_word[len(sb._typed)]
                            sb.type_key(str(_next_ch), v2)
                            self._demo_grid_cd = 0.08

                    # ── 移动到祥子正下方再发射 ────────────────────
                    # 祥子x坐标（弹幕区内归一化）
                    _sak_px = sb.sakiko_x   # 弹幕区内 px（0~V2_AREA_W）
                    _dist_to_sak = abs(v2.px - _sak_px)
                    _under_sak = _dist_to_sak < 55   # 55px以内视为"在祥子下方"

                    if sb.phase == 1 and sb.active and not getattr(sb, 'stunned', False):
                        # 走格子阶段：一直尝试移动到祥子下面
                        if not _under_sak:
                            _move_dx = (_sak_px - v2.px)
                            _step = min(abs(_move_dx), 180.0 * dt)
                            v2.move_player(_step if _move_dx > 0 else -_step, 0)
                        else:
                            # 在祥子正下方：如果格子任务完成（已踩完蓝格）则发射
                            _all_blue_done = (sb.blue_visited and sb.blue_visited2
                                and (not getattr(sb,'_three_blue_active',False)
                                     or getattr(sb,'blue_visited3',False)))
                            if _all_blue_done and sb._hit_cd <= 0:
                                sb.move_cursor(
                                    sb.grid_slot[0] - sb.grid_cursor[0],
                                    sb.grid_slot[1] - sb.grid_cursor[1]
                                ) if sb.grid_cursor != sb.grid_slot else None

            # ── 伪3D AI（r2_p3/r3_p3/tut_p3 障碍躲避）────────
            if p in ("tut_p3", "r2_p3", "r3_p3"):
                p3 = GM._p3
                if not (p3.dead or p3.round_clear):

                    _n      = getattr(p3, '_lane_count', P3_LANES)
                    _cur_l  = int(round(getattr(p3, 'target_l', 1.0)))
                    _cur_l  = max(0, min(_n - 1, _cur_l))
                    _depth  = getattr(p3, 'depth', 1.0)
                    _spd_z  = p3.OBS_SPD_Z * DIFF.p3_obs_spd_mult
                    if getattr(p3, '_boss_pincer', False):
                        _spd_z *= 1.3

                    p3.target_depth = getattr(p3, '_player_depth_target', p3.DEPTH_MAX)

                    _lane_danger = [0.0] * _n
                    for o in p3.obs:
                        if o.is_cucumber: continue
                        _ol = max(0, min(_n-1, int(o.x * _n)))
                        _dist_z = _depth - o.y
                        if 0 < _dist_z < 0.60:
                            _ttc = _dist_z / max(_spd_z, 0.01)
                            _lane_danger[_ol] += 1.0 / max(_ttc, 0.05)
                    _back_spd = _spd_z * 0.9
                    for _bo in getattr(p3, 'back_obs', []):
                        _ol = max(0, min(_n-1, int(_bo.x * _n)))
                        _dist_z = _bo.y - _depth
                        if 0 < _dist_z < 0.45:
                            _ttc = _dist_z / max(_back_spd, 0.01)
                            _lane_danger[_ol] += 0.9 / max(_ttc, 0.05)

                    _THRESH = 2.5
                    if _lane_danger[_cur_l] > _THRESH:
                        _best_lane  = _cur_l
                        _best_score = 99999.0
                        for _try in range(_n):
                            _direct  = abs(_try - _cur_l)
                            _wrap    = _n - _direct
                            _min_d   = min(_direct, _wrap)
                            _path_cost = 0.0
                            if _direct <= _wrap and _direct > 0:
                                _step = 1 if _try > _cur_l else -1
                                _r = _cur_l + _step
                                while _r != _try:
                                    _path_cost = max(_path_cost, _lane_danger[_r])
                                    _r += _step
                            _score = _lane_danger[_try] + _min_d * 0.6 + _path_cost * 0.4
                            if _score < _best_score:
                                _best_score = _score
                                _best_lane  = _try
                        if _best_lane != _cur_l:
                            _direct_d = abs(_best_lane - _cur_l)
                            _wrap_d   = _n - _direct_d
                            if _wrap_d < _direct_d and _n >= 4:
                                p3.target_l = float(_n - 1) if _cur_l <= _n // 2 else 0.0
                            else:
                                p3.target_l = float(_best_lane)
                            p3.SWITCH_SPD = min(13.0, 5.0 + _lane_danger[_cur_l] * 0.7)
                    else:
                        p3.SWITCH_SPD = 5.0

            # ── 爽世 Boss QTE AI ──────────────────────────────
            if GM.phase == "r2_p3":
                _sb = getattr(GM._p3, 'soyo_boss', None)
                if _sb and _sb.active and not _sb.stunned and not _sb.round_clear:
                    if not getattr(GM._p3, '_boss_pincer', False):
                        if not _sb.qte_active:
                            if CUKES.collected >= 2 and _sb._pb_cd <= 0:
                                _sb.activate_qte(int(round(GM._p3.lane)))
                        else:
                            _pos = _sb.qte_pos
                            _in_red   = _sb.qte_red_s <= _pos <= _sb.qte_red_s + _sb.qte_red_w
                            _in_green = _sb.qte_green_s <= _pos <= _sb.qte_green_s + _sb.qte_green_w
                            _should_fire = _in_red or (DIFF.current < DIFF.HARD and _in_green)
                            if _should_fire:
                                _sb.activate_qte(int(round(GM._p3.lane)))

        def skip_phase(self):
            """快速推进当前场景到结尾"""
            if self._skip_cd > 0: return
            self._skip_cd = 0.5
            p = GM.phase
            if p == "tut_h":
                GM._h.phase_timer = GM.TUT_H_DUR + 0.1
                GM._h.obs = [o for o in GM._h.obs if o.is_cucumber]
            elif p == "tut_v2":
                GM._v2.phase_timer = GM.TUT_V2_DUR + 0.1
                GM._v2.bullets.clear(); GM._v2.cukes.clear()
                GM._v2.wave_timer = -99.0
            elif p == "tut_p3":
                GM._p3.phase_timer = GM.TUT_P3_DUR + 0.1
                GM._p3.obs.clear()
            elif p in ("r2_h", "r3_h", "r4_h"):
                GM._h.phase_timer = GM.R_H_DUR + 0.1
                GM._h.obs = [o for o in GM._h.obs if o.is_cucumber]
            elif p in ("r2_v2", "r3_v2"):
                GM._v2.phase_timer = GM.R_V2_DUR + 0.1
                GM._v2.bullets.clear(); GM._v2.cukes.clear()
                GM._v2.wave_timer = -99.0
            elif p == "r2_p3":
                if not getattr(GM._p3, "_boss_phase", False):
                    # 跳过自由跑段，直接进入Boss
                    GM._p3._boss_phase = True
                    GM._p3.phase_timer = 0.0
                    GM._p3.soyo_boss.start()
                    GM._p3.spwn_cd = 10.5
                    # gate已删除
                    GM._p3._col_cd = 999999.0
                    renpy.music.play("audio/shuangshi.ogg", loop=True, fadein=1.0)
                    store._current_bgm = "audio/shuangshi.ogg"
                else:
                    GM._p3.round_clear = True
            elif p == "r3_p3":
                GM._p3.round_clear = True
            elif p == "trans":
                GM._tr.t = GM._tr.DURATION + 0.1

        def unlock_all(self):
            DIFF.unlock_hard()
            DIFF.unlock_extreme()
            persistent.tutorial_cleared = True
            _save_persistent()

        def jump_to_boss(self, boss):
            PRESSURE.value = 0.0
            CUKES.collected = max(CUKES.collected, 5)
            if boss == "soyo":
                GM._h.reset(); GM._v2.reset(); GM._p3.reset()
                GM._h.tutorial_mode = False
                GM.phase = "r2_p3"
                GM._p3.phase_timer = 0.0
                GM._p3._boss_phase  = True
                GM._p3.soyo_boss.start()
                GM._p3.spwn_cd = 10.5
                GM._p3._col_cd = 999999.0
                renpy.music.play("audio/shuangshi.ogg", loop=True, fadein=1.0)
                store._current_bgm = "audio/shuangshi.ogg"
            elif boss == "sakiko":
                GM._h.reset(); GM._v2.reset(); GM._p3.reset()
                GM._h.tutorial_mode = False
                GM.phase = "r3_v2"
                GM._v2.phase_timer = 0.0
                GM._v2.sakiko_boss.active = True
                GM._v2.sakiko_boss.start()
                renpy.music.play("audio/saki.ogg", loop=True, fadein=1.0)
                store._current_bgm = "audio/saki.ogg"
            elif boss == "mortis":
                GM._h.reset(); GM._v2.reset(); GM._p3.reset()
                GM._h.tutorial_mode = False
                GM._h.fake_ending_t      = 0.0
                GM._h.mortis_active      = False
                GM._h.mortis_burst_t     = 0.0
                GM._h.px_free            = False
                GM._h.px                 = float(H_PX)
                GM._h.desktop_ready      = False
                GM._h._dsk_shot_started  = False
                GM.phase = "r4_h"
                renpy.music.play("audio/ショパン「雨だれ」.ogg", loop=True, fadein=1.0)
                store._current_bgm = "audio/ショパン「雨だれ」.ogg"
            DIFF.unlock_hard()
            DIFF.unlock_extreme()
            persistent.tutorial_cleared = True
            _save_persistent()

        def reset_save(self):
            """清除所有存档"""
            persistent.tutorial_cleared    = False
            persistent.unlocked_hard       = False
            persistent.unlocked_extreme    = False
            persistent.best_diff_cleared   = -1
            persistent.dev_unlocked        = False
            DIFF.unlocked_hard             = False
            DIFF.unlocked_extreme          = False
            _save_persistent()

        @property
        def can_revive_override(self):
            return self.god_mode

    DEV = DevSystem()
    # 如果之前已解锁开发者模式，自动恢复（永久生效）
    if persistent.dev_unlocked:
        DEV.enabled = True

    # ══════════════════════════════════════════════════════════
    #  全局：黑白反转状态
    # ══════════════════════════════════════════════════════════
    invert_mode = [False]   # list 便于在函数内修改

    def toggle_invert():
        invert_mode[0] = not invert_mode[0]

    def bg_col():
        return "#000000" if invert_mode[0] else "#F0F0F0"

    def fg_col():
        return "#FFFFFF" if invert_mode[0] else "#535353"

    # ══════════════════════════════════════════════════════════
    #  全局：黄瓜收集系统
    # ══════════════════════════════════════════════════════════
    class CucumberSystem(python_object):
        BOMB_COST = 8
        # 复活费用由 DIFF.revive_cost 动态决定，无上限

        def __init__(self):
            self.collected   = 0
            self.revive_used = False   # 普通/困难限一次

        def reset(self):
            self.collected   = 0
            self.revive_used = False

        def collect_one(self):
            self.collected += 1
            # 极限模式：吃黄瓜降压2点
            if DIFF.cuke_heals_pressure > 0:
                PRESSURE.value = max(0.0, PRESSURE.value - DIFF.cuke_heals_pressure)

        @property
        def can_revive(self):
            if DIFF.has_revive_limit: return False       # 极限模式不能复活
            if DIFF.can_revive_free: return True         # 简单模式随时复活
            cost = DIFF.revive_cost
            used = self.revive_used
            return self.collected >= cost and not used

        def use_revive(self):
            if not self.can_revive: return False
            if DIFF.can_revive_free:
                return True                              # 简单不消耗黄瓜
            self.collected   -= DIFF.revive_cost
            self.revive_used  = True
            return True

        @property
        def can_bomb(self):
            # 仅检查黄瓜数（用于HUD显示"可以按B"）
            return self.collected >= self.BOMB_COST

        def use_bomb(self):
            if self.can_bomb:
                self.collected -= self.BOMB_COST
                return True
            return False

    CUKES = CucumberSystem()

    # ══════════════════════════════════════════════════════════
    #  全局：情感压力系统
    # ══════════════════════════════════════════════════════════
    _GLITCH_CHARS = ["睦", "陸", "陆", "墨", "睦", "陸", "X", "睦", "睦"]

    class PressureSystem(python_object):
        def __init__(self):
            self.value      = 0.0   # 0–100
            self.decay_rate = 2.0   # /s，可按场景动态调整
            self.shake_x    = 0.0
            self.shake_y    = 0.0
            self._shake_t   = 0.0
            self._gc_t      = 0.0   # glitch char 切换计时

        def reset(self):
            self.value      = 0.0
            self.decay_rate = 2.0
            self.shake_x    = 0.0
            self.shake_y    = 0.0
            self._shake_t   = 0.0

        def add(self, amt):
            if amt <= 0: return
            self.value = min(100.0, self.value + amt)

        def decay(self, dt):
            self.value = max(0.0, self.value - self.decay_rate * dt)

        def tick(self, dt):
            self.decay(dt)
            self._shake_t += dt
            self._gc_t    += dt
            if self.value > 40:
                amp = (self.value - 40) / 60.0 * 9.0
                import math as _m2
                self.shake_x = _m2.sin(self._shake_t * 24.1) * amp
                self.shake_y = _m2.cos(self._shake_t * 18.7) * amp
            else:
                self.shake_x = 0.0
                self.shake_y = 0.0

        @property
        def level(self):
            if self.value < 40:  return 0
            elif self.value < 70: return 1
            else:                 return 2

        def get_char(self):
            if self.level == 0:
                return "睦"
            elif self.level == 1:
                return random.choice(["睦", "睦", "陸"])
            else:
                return random.choice(_GLITCH_CHARS)

        @property
        def tilt_deg(self):
            if self.level == 0: return 0.0
            return (self.value - 40) / 60.0 * 4.0

        @property
        def noise_count(self):
            if self.level == 0: return 0
            elif self.level == 1: return 4
            else: return 10

    PRESSURE = PressureSystem()

    # ══════════════════════════════════════════════════════════
    #  全局：节奏判定系统（横版跑酷用）
    # ══════════════════════════════════════════════════════════
    class RhythmSystem(python_object):
        WINDOW = 0.10   # ±100ms 为 PERFECT 窗口

        def __init__(self):
            self._next_beat = 0.0   # 下一个节拍到达玩家的绝对时刻
            self._last_check = 0.0
            self.combo       = 0
            self.perfect_flash = 0.0  # 闪光倒计时
            self.multiplier    = 1

        def reset(self):
            self._next_beat    = 0.0
            self.combo         = 0
            self.perfect_flash = 0.0
            self.beat_flash    = 0.0   # 节拍接近时地面闪光
            self.multiplier    = 1

        def register_obstacle(self, dist_to_player, spd):
            """障碍物生成时登记其预计到达玩家的时刻"""
            import time as _t2
            arrival = _t2.time() + dist_to_player / max(spd, 1.0)
            self._next_beat = arrival

        def judge(self):
            """玩家跳跃/蹲下时调用，返回 'PERFECT'/'OK'/None"""
            import time as _t2
            now  = _t2.time()
            diff = abs(now - self._next_beat)
            if diff < self.WINDOW:
                self.combo += 1
                self.perfect_flash = 0.6
                self.multiplier = min(4, 1 + self.combo // 3)
                return "PERFECT"
            else:
                self.combo = 0
                self.multiplier = 1
                return None

        def tick(self, dt):
            import time as _t3
            self.perfect_flash = max(0.0, self.perfect_flash - dt)
            self.beat_flash    = max(0.0, self.beat_flash    - dt)
            # 节拍接近（±0.25s）时地面闪光提示
            now = _t3.time()
            if 0.0 < self._next_beat - now < 0.25:
                self.beat_flash = max(self.beat_flash, 0.18)

    RHYTHM = RhythmSystem()

    # ── 计时器 ───────────────────────────────────────────────
    _ts = [None]

    def _dt():
        now = _time.time()
        if _ts[0] is None:
            _ts[0] = now
            return 0.0
        dt = min(now - _ts[0], 0.05)
        _ts[0] = now
        return dt

    def _reset_ts():
        _ts[0] = None

    # ── AABB 碰撞 ────────────────────────────────────────────
    def aabb(ax, ay, aw, ah, bx, by, bw, bh):
        return ax < bx+bw and ax+aw > bx and ay < by+bh and ay+ah > by

    # ── 实体基类 ─────────────────────────────────────────────
    class Entity(python_object):
        def __init__(self, x, y, w, h, vx=0.0, vy=0.0, tag="",
                     invert_safe=False, is_cucumber=False,
                     collectible=False, char="", invert_required=False,
                     layer=-1):
            self.x = float(x); self.y = float(y)
            self.w = int(w);   self.h = int(h)
            self.vx = float(vx); self.vy = float(vy)
            self.tag             = tag
            self.invert_safe     = invert_safe      # 反转模式下变为平台
            self.invert_required = invert_required  # 必须反转才能通过（正常模式致命）
            self.is_cucumber     = is_cucumber      # 可收集的黄瓜
            self.collectible     = collectible      # 伪3D可收集音符
            self.char            = char             # 文字障碍用字符
            self.layer           = layer            # P3层级: -1=任意, 0=地面, 1=高空
        def move(self, dt):
            self.x += self.vx * dt
            self.y += self.vy * dt
        def on_screen(self):
            return -150 < self.x < SW+150 and -150 < self.y < SH+150

    # ── 飘字 ─────────────────────────────────────────────────
    class FloatText(python_object):
        def __init__(self, text, x, y, life=3.5, vy=-18.0, size=24, color="#FFFFFF", outline=False):
            self.text    = text
            self.x       = float(x)
            self.y       = float(y)
            self.life    = float(life)
            self.max_l   = float(life)
            self.vy      = float(vy)
            self.size    = size
            self.color   = color
            self.outline = outline  # True = 4方向黑色描边，用于桌面阶段
        def tick(self, dt):
            self.life -= dt
            self.y    += self.vy * dt
        @property
        def alpha(self):
            f = self.life / self.max_l
            if f > 0.8:    return (1.0 - f) / 0.2
            elif f < 0.25: return f / 0.25
            return 1.0
        @property
        def alive(self): return self.life > 0

    # ── 场景过渡动画 ─────────────────────────────────────────
    class SceneTransition(python_object):
        # kind: "h_v2" | "v2_p3" | "p3_h"
        DURATION = 1.1

        def __init__(self):
            self.kind      = ""
            self.t         = 0.0
            self.done      = False
            self.next_ph   = ""
            self._setup_fn = None   # 切换后要执行的初始化

        def start(self, kind, next_phase, setup_fn=None):
            self.kind      = kind
            self.t         = 0.0
            self.done      = False
            self.next_ph   = next_phase
            self._setup_fn = setup_fn

        def tick(self, dt):
            if self.done: return
            self.t = min(1.0, self.t + dt / self.DURATION)
            if self.t >= 1.0:
                self.done = True
                if self._setup_fn:
                    self._setup_fn()

        @staticmethod
        def ease(t):
            return t * t * (3 - 2 * t)   # smoothstep

    # ── 主界面动画状态 ────────────────────────────────────────
    class TitleAnim(python_object):
        def __init__(self):
            self.char_x   = -120.0
            self.done     = False
            self.fade_out = 0.0   # 睦冲出屏幕后白色淡出
        def start_enter(self):
            self.char_x   = -120.0
            self.done     = False
            self.fade_out = 0.0
        def tick(self, dt):
            if not self.done:
                # 先加速跑过整个屏幕（目标 SW+120=1400）
                self.char_x += 820.0 * dt
                if self.char_x >= 1400.0:
                    self.done = True
            else:
                # 睦冲出屏幕后白色背景快速淡出，切入游戏
                self.fade_out = min(1.0, self.fade_out + dt * 4.0)

    # ── 横版跑酷文字障碍台词库 ──────────────────────────────
    H_WORD_WALLS = [
        "春日影",
        "なんで！？",
        "バンド！",
        "やめろ！",
        "なんで春日影やったの！？",
        "バンド楽しいと思ったことない",
    ]
    H_PUNCTUATION = set("！？。、…!?.,")

    # ── 横版跑酷 ─────────────────────────────────────────────
    class HRunner(python_object):
        def __init__(self):
            self.tutorial_mode = True
            self.phase_dur     = 30.0
            self.reset()

        def reset(self):
            self.py          = float(H_GY - H_PH_N)
            self.vy          = 0.0
            self.jumping     = False
            self.duck_t      = 0.0
            self.obs         = []        # Entity 列表（含黄瓜/文字块）
            self.spwn_cd     = 2.8
            self.spd         = 290.0 * DIFF.h_spd_mult
            self.dist        = 0.0
            self.phase_timer = 0.0
            self.dead        = False
            self.round_clear = False
            self.float_texts = []
            self.invincible_t = 0.0      # 碰撞无敌帧（每次reset必须归零）
            self._word_cd    = random.uniform(12.0, 18.0)  # 文字墙冷却
            self._cuke_cd    = random.uniform(8.0, 14.0)   # 黄瓜冷却
            self._tut_fired  = set()
            # 假鼠标指针
            self._fake_cur_x  = float(SW // 2)
            self._fake_cur_y  = float(SH // 2)
            self._fake_cur_on = False   # 教程触发后才启用
            self._htut_q_dirty = True  # 难度变化后重建提示队列
            self._tut_q = []          # tick时按难度动态填入
            # Mortis Boss 专用字段（r4_h 阶段激活）
            self.mortis_active   = False
            self.mortis_hp       = 15 if DIFF.current >= DIFF.HARD else 9  # 困难=5×3=15，普通=3×3=9
            self.mortis_phase    = 0      # 1/2/3
            self.mortis_phase_t  = 0.0
            # X轴自由移动
            self.px_free         = False
            self.px              = float(H_PX)
            self.pvx             = 0.0
            # 假结局演出
            self.fake_ending_t   = 0.0
            self.credits_done    = False
            self.mortis_burst_t  = 0.0
            self.desktop_ready   = False
            self._dsk_shot_started = False
            # 阶段一/二：弹片墙
            self._frag_wall_cd   = 3.5
            self._p1_tip_shown   = False
            # 弹幕子弹（所有阶段）
            self._mortis_bullets = []    # [x, y, vx, vy]
            self._mbullet_cd     = 2.5   # 第一次发射冷却
            # 阶段二：未响应 + 进度条
            self._no_resp_t      = 0.0
            self._no_resp_cd     = 8.0
            self._progress_x     = -60.0
            self._progress_spd   = 28.0
            # 阶段三：弹弓黄瓜
            self._sling_held     = False
            self._sling_ox       = 0.0
            self._sling_oy       = 0.0
            self._sling_mx       = 0.0
            self._sling_my       = 0.0
            self._cukes_flying   = []    # [x, y, vx, vy]
            # Boss三字（普通每字3HP，困难每字5HP）
            _bc_hp  = 5 if DIFF.current >= DIFF.HARD else 3
            _bc_spd = 2.0 if DIFF.current == DIFF.EXTREME else (1.5 if DIFF.current >= DIFF.HARD else 1.0)
            self._boss_chars     = [
                {"ch":"墨","x":240.0,"y":80.0,"vx":48.0*_bc_spd,"vy":28.0*_bc_spd,"hp":_bc_hp,"hit_t":0.0,"dead_t":-1.0,"sine_t":0.0},
                {"ch":"提","x":580.0,"y":65.0,"vx":-38.0*_bc_spd,"vy":42.0*_bc_spd,"hp":_bc_hp,"hit_t":0.0,"dead_t":-1.0,"sine_t":1.2},
                {"ch":"斯","x":920.0,"y":90.0,"vx":52.0*_bc_spd,"vy":-32.0*_bc_spd,"hp":_bc_hp,"hit_t":0.0,"dead_t":-1.0,"sine_t":2.4},
            ]
            self._mortis_hp_max  = _bc_hp * 3

        @property
        def ducking(self): return self.duck_t > 0

        @property
        def score(self): return self.dist / 10.0

        def do_jump(self):
            if not self.jumping and not self.ducking and not self.dead:
                self.jumping = True
                self.vy = H_JVY

        def do_duck(self): pass
        def duck_release(self): pass

        def tick(self, dt):
            import pygame
            if self.dead or self.round_clear: return
            k  = pygame.key.get_pressed()
            mb = pygame.mouse.get_pressed()
            _duck_key = k[pygame.K_DOWN] or k[pygame.K_z] or k[pygame.K_s] or mb[2]
            # 演示模式：AI控制的蹲视为按键按下
            if getattr(DEV, 'demo_mode', False) and getattr(DEV, '_demo_duck_held', False):
                _duck_key = True
            if _duck_key and self.jumping:
                self.vy = max(self.vy, H_GRAV * 0.55)
            _duck_held = _duck_key and not self.jumping
            self.duck_t = 1.0 if _duck_held else 0.0
            self.phase_timer += dt
            self.dist        += self.spd * dt
            self.spd          = min(290.0 * DIFF.h_spd_mult + self.score * 1.6, DIFF.h_spd_max)
            RHYTHM.tick(dt)
            # 无敌帧递减
            if not hasattr(self, 'invincible_t'): self.invincible_t = 0.0
            self.invincible_t = max(0.0, self.invincible_t - dt)

            # ── 黑色模式（反转）持续增加压力 ────────────────
            if invert_mode[0]:
                PRESSURE.add(DIFF.invert_pressure_rate * dt)   # 反转模式压力

            # ── 假鼠标指针弹性追踪 ───────────────────────────
            if self._fake_cur_on:
                _mx2, _my2 = renpy.get_mouse_pos()
                # 墨缇斯阶段二：追踪速度按难度分级
                if getattr(self, 'mortis_active', False):
                    if DIFF.current == DIFF.EXTREME:
                        _spd_f2 = 0.05
                    elif DIFF.current >= DIFF.HARD:
                        _spd_f2 = 0.04
                    else:
                        _spd_f2 = 0.03
                else:
                    _spd_f2 = 0.02 + min(0.02, self.phase_timer * 0.0005)
                self._fake_cur_x += (_mx2 - self._fake_cur_x) * _spd_f2
                self._fake_cur_y += (_my2 - self._fake_cur_y) * _spd_f2
                # 判定：假光标与真实鼠标重合时增加压力
                _fc_dx = self._fake_cur_x - _mx2
                _fc_dy = self._fake_cur_y - _my2
                _fc_dist2 = _fc_dx * _fc_dx + _fc_dy * _fc_dy
                if _fc_dist2 < 30 * 30:   # 30px以内视为重合
                    PRESSURE.add(DIFF.fake_cursor_pressure_rate * dt)
                    if random.random() < 0.12:
                        self.float_texts.append(FloatText(
                            "！", int(self._fake_cur_x) + 18, int(self._fake_cur_y) - 10,
                            life=0.4, size=22, color=fg_col()))

            if self.jumping:
                self.vy += H_GRAV * dt
                self.py += self.vy * dt
                floor = float(H_GY - H_PH_N)
                if self.py >= floor:
                    self.py = floor; self.vy = 0.0; self.jumping = False

            # X轴自由移动（Mortis战解锁后）
            if getattr(self, 'px_free', False):
                import pygame as _pg2
                _k2 = _pg2.key.get_pressed()
                _ax = 0.0
                if _k2[_pg2.K_a] or _k2[_pg2.K_LEFT]:  _ax = -1.0
                if _k2[_pg2.K_d] or _k2[_pg2.K_RIGHT]: _ax =  1.0
                # 阶段二未响应时：加大惯性、降低加速度
                _no_resp = getattr(self, '_no_resp_t', 0.0) > 0
                _px_accel = 400.0 if _no_resp else 900.0
                _px_fric  = 0.92  if _no_resp else 0.82
                self.pvx += _ax * _px_accel * dt
                self.pvx *= _px_fric
                self.px  += self.pvx * dt
                self.px   = max(50.0, min(float(SW - 60), self.px))

            if self.tutorial_mode:
                # 教程固定以普通模式标准进行（无论当前选择的难度）
                if self._htut_q_dirty:
                    self._htut_q_dirty = False
                    self._tut_q = [
                        (3.0,  "睦开始奔跑了！  ——  教程以【普通模式】标准进行"),
                        (6.0,  "↑ / Space — 跳跃   ↓ / Z — 按住蹲下"),
                        (12.0, "🥒 收集黄瓜！  普通=20个复活  困难=30个复活  极限=吃🥒可降低压力值"),
                        (19.0, "Shift — 黑白反转！白框障碍必须反转才能通过"),
                        (24.0, "⚠ 反转模式下压力值会持续上升！必要时才用"),
                        (30.0, "压力槽升高时画面开始扭曲…注意右上角红条"),
                        (37.0, "！！！  某个东西出现了……"),
                    ]
                for (t, msg) in self._tut_q:
                    if t not in self._tut_fired and self.phase_timer >= t:
                        self._tut_fired.add(t)
                        self.float_texts.append(FloatText(msg, SW//2-200, 180, life=4.5, size=22))
                        if t == 19.0:
                            self.spwn_cd = 8.0
                            wall_h = 220
                            self.obs.append(Entity(float(SW + 900), H_GY - wall_h, 56, wall_h,
                                                   vx=-(self.spd * 0.50),
                                                   tag="ground", invert_safe=True,
                                                   invert_required=True))
                        elif t == 12.0:
                            for gi in range(3):
                                self.obs.append(Entity(float(SW + 80 + gi * 90),
                                                       float(H_GY - H_PH_N - 8),
                                                       28, 28, vx=-self.spd,
                                                       tag="cucumber", is_cucumber=True))
                        elif t == 37.0:
                            self.spwn_cd = 6.0
                            self._fake_cur_on = True
                            self.float_texts.append(FloatText(
                                "假鼠标指针在追踪你！  接近时压力值会上升",
                                SW//2 - 200, 150, life=4.0, size=22, color=fg_col()))

            # ── 生成普通障碍 ─────────────────────────────────
            self.spwn_cd -= dt
            if self.spwn_cd <= 0:
                self._spawn()
                if self.tutorial_mode:
                    self.spwn_cd = random.uniform(2.2, 3.5)
                else:
                    self.spwn_cd = max(0.9, random.uniform(1.4, 2.6) * (290.0 / self.spd) * DIFF.h_spwn_mult)

            # 文字墙已禁用（日文字体缺失会显示乱码）

            # ── 生成黄瓜（增量：每次1-3个，间隔缩短）───────
            self._cuke_cd -= dt
            if self._cuke_cd <= 0 and self.phase_timer > 5.0:
                count = random.randint(1, 3)
                for _ci in range(count):
                    _cx_off = _ci * 72   # 间隔72px成串
                    if random.random() < 0.5:
                        _cy = float(H_GY - H_PH_N - 10)
                    else:
                        _cy = float(H_GY - H_PH_N - random.randint(50, 110))
                    self.obs.append(Entity(float(SW + 60 + _cx_off), _cy, 28, 28,
                                           vx=-self.spd, tag="cucumber", is_cucumber=True))
                self._cuke_cd = random.uniform(4.5, 7.5) if DIFF.current >= DIFF.HARD else random.uniform(6.0, 10.0)

            # ── 移动所有实体 ─────────────────────────────────
            for e in self.obs: e.move(dt)
            self.obs = [e for e in self.obs if e.x > -200]
            for ft in self.float_texts: ft.tick(dt)
            self.float_texts = [ft for ft in self.float_texts if ft.alive]

            # ── 碰撞检测 ─────────────────────────────────────
            _hpx = int(getattr(self, 'px', H_PX))   # X轴：Mortis战用动态px，其余用固定H_PX
            hy = self.py + (H_PH_N - H_PH_D) if self.ducking else self.py
            hh = H_PH_D if self.ducking else H_PH_N
            for e in list(self.obs):
                if not aabb(_hpx, hy, H_PW, hh, e.x, e.y, e.w, e.h):
                    continue
                if e.is_cucumber:
                    CUKES.collect_one()
                    self.float_texts.append(FloatText("🥒 +1", H_PX+50, int(self.py)-20, life=0.7, size=20, color=fg_col()))
                    self.obs.remove(e)
                    continue
                # 黑白反转处理
                if e.invert_safe:
                    if invert_mode[0]:
                        # 反转模式：invert_safe 变平台，从上方踩安全
                        player_bottom = hy + hh
                        obs_top       = e.y
                        if self.vy >= 0 and player_bottom <= obs_top + 14:
                            self.py      = obs_top - (H_PH_D if self.ducking else H_PH_N)
                            self.vy      = 0.0
                            self.jumping = False
                            continue
                        else:
                            continue   # 侧面/下面碰撞：不死，跳过
                    else:
                        # 正常模式：invert_required 的障碍太高跳不过去 → 致命
                        # 普通 invert_safe（低矮）可以跳过，不强制反转
                        if e.invert_required:
                            if aabb(H_PX+4, hy+4, H_PW-8, hh-8, e.x+2, e.y+2, e.w-4, e.h-4):
                                if not DEV.god_mode and not DEV.invincible and self.invincible_t <= 0:
                                    PRESSURE.add(DIFF.obs_pressure)
                                    
                                    self.invincible_t = DIFF.invincible_dur
                            continue
                        # 低矮 invert_safe：当作普通障碍
                        pass  # 继续走下面的普通碰撞
                # 普通碰撞（文字char/标点特殊判定）
                if e.char and e.char in H_PUNCTUATION:
                    # 标点：只有从上方踩才安全，侧面也不死（弹开）
                    player_bottom = hy + hh
                    if self.vy >= 0 and player_bottom <= e.y + 14:
                        self.vy = H_JVY * 0.6   # 弹跳
                        self.jumping = True
                    continue
                # 普通致命障碍：加压力+无敌帧，压力满了才爆炸
                if aabb(H_PX+14, hy+6, H_PW-28, hh-12, e.x+2, e.y+2, e.w-4, e.h-4):
                    if DEV.god_mode or DEV.invincible: continue
                    if self.invincible_t <= 0:
                        PRESSURE.add(DIFF.obs_pressure)
                        
                        self.invincible_t = DIFF.invincible_dur
                        self.float_texts.append(FloatText(
                            "！+%d 压力" % int(DIFF.obs_pressure), int(H_PX), 220, life=0.8, size=22, color="#FF4444"))

        def _spawn(self):
            if self.tutorial_mode and self.phase_timer < 8.0: return
            roll = random.random()
            # ── 15%：必须反转才能通过的超高障碍 ─────────────
            if not self.tutorial_mode and roll < 0.15:
                h = random.randint(190, 220)   # > 180px 跳跃极限，跳不过去
                w = random.randint(28, 42)
                self.obs.append(Entity(SW+60, H_GY-h, w, h, vx=-self.spd,
                                       tag="ground", invert_safe=True,
                                       invert_required=True))
            # ── 教程模式：超高障碍较小（100px，提示反转）─────
            elif self.tutorial_mode and self.phase_timer >= 20.0 and roll < 0.25:
                h = random.randint(190, 210)
                w = random.randint(28, 38)
                self.obs.append(Entity(SW+60, H_GY-h, w, h, vx=-self.spd,
                                       tag="ground", invert_safe=True,
                                       invert_required=True))
            # ── 普通地面障碍 ───────────────────────────────────
            elif roll < 0.58 + 0.15:
                h = random.randint(40, 72); w = random.randint(22, 36)
                is_inv = (not self.tutorial_mode) and random.random() < 0.18
                self.obs.append(Entity(SW+60, H_GY-h, w, h, vx=-self.spd,
                                       tag="ground", invert_safe=is_inv))
                if not self.tutorial_mode and random.random() < 0.10:
                    h2 = random.randint(34, 56)
                    self.obs.append(Entity(SW+60+w+24, H_GY-h2, random.randint(18,30), h2,
                                           vx=-self.spd, tag="ground"))
            # ── 空中障碍 ───────────────────────────────────────
            else:
                self.obs.append(Entity(SW+60, float(H_GY - H_PH_N - random.randint(0,16)),
                                       44, 22, vx=-self.spd, tag="air"))

        def _spawn_word_wall(self):
            """生成文字墙：每个字符单独成为一个 Entity"""
            word = random.choice(H_WORD_WALLS)
            char_w = 38; char_h = 52
            gap    = 4
            total_w = (char_w + gap) * len(word)
            base_x  = float(SW + 80)
            for i, ch in enumerate(word):
                is_punc = ch in H_PUNCTUATION
                h = char_h if not is_punc else 44
                y = float(H_GY - h)
                ent = Entity(base_x + i * (char_w + gap), y, char_w, h,
                             vx=(-self.spd * 0.7),  # 文字墙比普通障碍慢
                             tag="word",
                             invert_safe=is_punc,    # 标点在反转模式也变平台
                             char=ch)
                self.obs.append(ent)

        def _spawn_cucumber(self):
            """在地面高度附近或悬浮处生成黄瓜"""
            # 交替地面和空中
            if random.random() < 0.5:
                y = float(H_GY - H_PH_N - 10)  # 地面
            else:
                y = float(H_GY - H_PH_N - random.randint(60, 120))  # 悬浮
            self.obs.append(Entity(float(SW + 60), y, 28, 28,
                                   vx=-self.spd, tag="cucumber", is_cucumber=True))

    # ── 竖版弹幕 ─────────────────────────────────────────────
    class SafeZone(python_object):
        """祥子战：伪安全区"""
        def __init__(self, x, y, r):
            self.x       = float(x)
            self.y       = float(y)
            self.r       = float(r)        # 半径
            self.t       = 0.0             # 已存在时间
            self.trap    = False           # True=已变陷阱
            self.warn_t  = 0.0             # 警告闪烁计时
        def tick(self, dt):
            self.t += dt
            if self.t >= 2.5 and not self.trap:
                self.trap   = True
                self.warn_t = 0.5
            if self.warn_t > 0:
                self.warn_t = max(0.0, self.warn_t - dt)
        def in_zone(self, px, py):
            dx = px - self.x; dy = py - self.y
            return dx*dx + dy*dy < self.r * self.r
        @property
        def alive(self): return self.t < 10.0   # 10秒后消失

    class V2Runner(python_object):
        GRAZE_HIT_R  = 18    # 致命半径
        GRAZE_OUT_R  = 40    # 擦弹外径

        def __init__(self):
            self.tutorial_mode = True
            self.phase_dur     = 25.0
            self.reset()

        def reset(self):
            self.px          = float(V2_AREA_W // 2)
            self.py          = float(V2_AREA_H - 120)
            self.bullets     = []
            self.cukes       = []       # 场内黄瓜
            self.safe_zones  = []       # 祥子伪安全区
            self.phase_timer = 0.0
            self.wave_timer  = 0.0
            self.wave        = 0
            self.dead        = False
            self.round_clear = False
            self.float_texts = []
            self.invincible  = 0.0
            # 擦弹系统
            self.graze_bar   = 0.0      # 0-100
            self.graze_flash = 0.0      # 白色边缘闪光倒计时
            # 大招系统
            self.bomb_active  = False
            self.bomb_t       = 0.0
            self.bomb_phase   = 0       # 0=空白, 1=台词, 2=爆炸
            # 伪安全区冷却
            self._sz_cd      = 6.0
            # 黄瓜生成
            self._cuke_cd    = random.uniform(10.0, 18.0)
            self._tut_fired  = set()
            self._tut_script_phase = 0
            self._tut_cuke_cd      = 0.0
            self._tut_cuke_sent    = 0
            self._tut_bomb_done    = False
            self._tut_bomb_used    = False
            self._tut_bomb_delay   = -1.0
            self._trans_notified   = False
            self._tut_q_dirty = True
            # Boss战
            self.sakiko_boss = SakikoBoss()

        def move_player(self, dx, dy):
            if self.dead or self.bomb_active: return
            self.px = max(float(V2_PW//2), min(float(V2_AREA_W - V2_PW//2), self.px + dx))
            # r3_v2 Phase1：玩家只能在上方70%区域活动
            if GM.phase == "r3_v2" and self.sakiko_boss.active and self.sakiko_boss.phase == 1:
                _max_y = V2_AREA_H * 0.70 - V2_PH
            else:
                _max_y = float(V2_AREA_H - V2_PH//2)
            self.py = max(float(V2_PH//2), min(_max_y, self.py + dy))

        def trigger_bomb(self):
            """消耗黄瓜释放断绝大招 — 需要graze_bar满(100)才可触发"""
            if self.bomb_active or self.dead: return
            # 教程模式下graze_bar由脚本控制（设为100后才允许），非教程同样需要满格
            if self.graze_bar < 100.0: return
            if not CUKES.use_bomb(): return
            self.graze_bar        = 0.0   # 消耗大招槽
            self.bomb_active      = True
            self.bomb_t           = 0.0
            self.bomb_phase       = 0
            self._tut_bomb_used   = True   # 标记大招确实被触发

        def tick(self, dt):
            if self.dead or self.round_clear: return

            # ── 根据难度动态构建教程提示队列 ─────────────
            if self.tutorial_mode and self._tut_q_dirty:
                self._tut_q_dirty = False
                if DIFF.can_revive_free:
                    _rv_hint = "简单模式：死亡后按 F 键可免费无限复活！"
                elif DIFF.has_revive_limit:
                    _rv_hint = "极限模式：无法复活！慎重行动"
                else:
                    _rv_hint = "集满 %d 个🥒后死亡可按 F 键复活（仅限一次）" % DIFF.revive_cost
                self._tut_q = [
                    (2.0,  "弹幕战！鼠标移动控制睦"),
                    (6.0,  _rv_hint),
                    (9.0,  "子弹从边缘擦过 = 擦弹！  积累右上角断绝槽"),
                    (12.0, "断绝槽积满100% 后，才能按 B 键释放大招清屏！"),
                    (14.0, "现在开始发黄瓜！集满 8 个，然后按 B 键大招清屏"),
                ]

            # ── 大招处理（期间暂停游戏逻辑）────────────────
            if self.bomb_active:
                self.bomb_t += dt
                # 大招期间继续 tick 飘字，防止文字倒计时停止积累叠字
                for _ft in self.float_texts: _ft.tick(dt)
                self.float_texts = [_ft for _ft in self.float_texts if _ft.alive]
                if self.bomb_phase == 0 and self.bomb_t >= 0.3:
                    self.bomb_phase = 1
                elif self.bomb_phase == 1 and self.bomb_t >= 1.1:
                    self.bomb_phase = 2
                elif self.bomb_phase == 2 and self.bomb_t >= 2.0:
                    self.bomb_active = False
                    self.bullets.clear()
                    self.invincible = 1.5
                    PRESSURE.value  = 0.0   # 大招清屏，压力同步清零
                    self.graze_bar  = 0.0   # 断绝槽同步清空
                    self.float_texts.clear()
                return

            self.phase_timer += dt
            self.wave_timer  += dt
            self.invincible   = max(0.0, self.invincible - dt)
            self.graze_flash  = max(0.0, self.graze_flash - dt)

            if self.tutorial_mode:
                for (t, msg) in self._tut_q:
                    if t not in self._tut_fired and self.phase_timer >= t:
                        self._tut_fired.add(t)
                        self.float_texts.append(FloatText(msg, V2_AREA_W//2-80, 60, life=3.0, size=24))

            # ── 教程脚本阶段控制 ─────────────────────────
            if self.tutorial_mode:
                if self._tut_script_phase == 0:
                    # 普通弹幕
                    if self.wave_timer >= 2.5:
                        self.wave_timer = 0.0
                        self._emit()
                        self.wave += 1
                    # 14秒提示触发 → 等屏幕弹幕清空后再进入黄瓜阶段（大招已完成则跳过）
                    if 14.0 in self._tut_fired and self._tut_script_phase == 0 and not self._tut_bomb_done:
                        if len(self.bullets) == 0:
                            self._tut_script_phase = 1
                            self._tut_cuke_cd  = 1.2
                            self._tut_cuke_sent = 0
                            CUKES.collected = 0
                            self.float_texts.append(FloatText("——黄瓜来了！——", V2_AREA_W//2-60, SH//2-20, life=2.0, size=28, color="#FFFFFF"))
                        else:
                            # 弹幕还在，等自然清空，但停止发新弹幕
                            self.wave_timer = 0.0

                elif self._tut_script_phase == 1:
                    # 发黄瓜阶段：每0.9秒发一个，发满8个
                    self._tut_cuke_cd -= dt
                    if self._tut_cuke_cd <= 0 and self._tut_cuke_sent < 8:
                        cx = random.uniform(60, V2_AREA_W - 60)
                        self.cukes.append(Entity(cx, -20, 28, 28, vx=0, vy=110.0, tag="v2cuke", is_cucumber=True))
                        self._tut_cuke_sent += 1
                        self._tut_cuke_cd = 0.9
                    # 黄瓜集满8个 → 进入弹幕轰炸阶段
                    if CUKES.collected >= 8 and self._tut_script_phase == 1:
                        self._tut_script_phase = 2
                        self.graze_bar         = 100.0
                        self._tut_bomb_used    = False  # 重置，等玩家按B
                        self._tut_bomb_delay   = 0.6    # 明确赋值（不靠hasattr）
                        self.cukes.clear()
                        self.float_texts.append(FloatText("——大招准备好了！  按 B ——", V2_AREA_W//2-120, SH//2-30, life=3.0, size=26, color="#FFFFFF"))

                elif self._tut_script_phase == 2:
                    # 弹幕轰炸阶段：0.6s 延迟后炸
                    if self._tut_bomb_delay > 0:
                        self._tut_bomb_delay -= dt
                        if self._tut_bomb_delay <= 0:
                            self._tut_bomb_explode()
                    # 大招演出结束后回阶段0（用专属flag，不靠CUKES.collected）
                    if not self.bomb_active and self._tut_bomb_used:
                        self._tut_script_phase = 0
                        self._tut_bomb_done    = True
                        self._tut_bomb_used    = False
                        self.wave_timer = 0.0
                        self.wave = 0
                        self.float_texts.append(FloatText("——大招成功！战斗继续——", V2_AREA_W//2-120, SH//2-20, life=2.5, size=26, color="#FFFFFF"))
            else:
                # 非教程模式正常发波
                if self.wave_timer >= DIFF.v2_wave_interval:
                    self.wave_timer = 0.0
                    self._emit()
                    self.wave += 1

            # 伪安全区已废弃（祥子Boss战改用推箱子机制，SafeZone不再生成）
            self.safe_zones = []   # 确保不渲染残留

            # ── 祥子Boss tick（r3_v2 专属）────────────────
            if GM.phase == "r3_v2":
                self._tick_sakiko(dt)

            # ── 黄瓜生成（仅非教程模式）──────────────────
            if not self.tutorial_mode:
                self._cuke_cd -= dt
                if self._cuke_cd <= 0 and self.phase_timer > 4.0:
                    cx = random.uniform(40, V2_AREA_W - 40)
                    self.cukes.append(Entity(cx, -20, 24, 24, vx=0, vy=120.0, tag="v2cuke", is_cucumber=True))
                    # 一次生成2个，随机横向位置
                    cx2 = random.uniform(40, V2_AREA_W - 40)
                    self.cukes.append(Entity(cx2, -20, 24, 24, vx=0, vy=120.0, tag="v2cuke", is_cucumber=True))
                    self._cuke_cd = random.uniform(3.5, 6.0) if DIFF.current >= DIFF.HARD else random.uniform(5.0, 8.0)

            # ── 移动子弹和黄瓜 ────────────────────────────
            for b in self.bullets: b.move(dt)
            for c in self.cukes:   c.move(dt)
            self.bullets = [b for b in self.bullets if -60 <= b.y <= V2_AREA_H+60]
            # 黄瓜碰撞
            for c in list(self.cukes):
                if not (-60 <= c.y <= V2_AREA_H+60): self.cukes.remove(c); continue
                dx2 = (c.x + c.w//2) - self.px
                dy2 = (c.y + c.h//2) - self.py
                if dx2*dx2 + dy2*dy2 < 30*30:
                    CUKES.collect_one()
                    self.float_texts.append(FloatText("🥒 +1", V2_AREA_W//2-20, 80, life=0.7, size=20, color="#FFFFFF"))
                    self.cukes.remove(c)

            for ft in self.float_texts: ft.tick(dt)
            self.float_texts = [ft for ft in self.float_texts if ft.alive]

            # ── 碰撞/擦弹检测 ─────────────────────────────
            if self.invincible <= 0:
                _grazed_this_frame = False
                _hit_this_frame    = False   # 每帧只判定一次命中，防多弹叠压
                for b in list(self.bullets):
                    bcx = b.x + b.w//2; bcy = b.y + b.h//2
                    ddx = bcx - self.px; ddy = bcy - self.py
                    dist2 = ddx*ddx + ddy*ddy
                    if dist2 < self.GRAZE_HIT_R * self.GRAZE_HIT_R:
                        if not _hit_this_frame:
                            _hit_this_frame = True
                            if self.tutorial_mode:
                                PRESSURE.add(33.0)
                                CUKES.collected = 0
                                self.invincible = 0.6
                                if PRESSURE.value >= 100.0:
                                    self._tut_reset_from_pressure()
                                return
                            else:
                                if DEV.invincible: continue
                                PRESSURE.add(22.0)
                                
                                self.invincible = DIFF.invincible_dur
                                self.float_texts.append(FloatText(
                                    "！+22 压力", int(self.px)-20, int(self.py)-30,
                                    life=0.8, size=20, color="#FF4444"))
                                if PRESSURE.value >= 100.0:
                                    self.dead = True
                                return
                    elif dist2 < self.GRAZE_OUT_R * self.GRAZE_OUT_R:
                        # 擦弹：每帧最多触发一次
                        if not _grazed_this_frame:
                            self.graze_bar   = min(100.0, self.graze_bar + 0.8)
                            self.graze_flash = 0.12
                            _grazed_this_frame = True

        def _tick_sakiko(self, dt):
            """r3_v2 Boss tick — 由 GM 保证只在 active=True 时调用"""
            sb = self.sakiko_boss
            if not sb.active: return
            sb.tick(dt, self)
            # 光柱期间：清除命中列的所有子弹
            if sb._beam_t > 0:
                beam_x_min = (sb._beam_col * V2_AREA_W / sb.GRID_W)
                beam_x_max = beam_x_min + V2_AREA_W / sb.GRID_W
                self.bullets = [b for b in self.bullets
                                if not (beam_x_min <= b.x <= beam_x_max)]

        def _tut_reset_from_pressure(self):
            """教程模式压力值满：清空弹幕并重置教程脚本阶段"""
            PRESSURE.reset()
            CUKES.collected = 0
            self.bullets.clear()
            self.cukes.clear()
            self.bomb_active       = False   # 确保大招不残留
            self._tut_script_phase = 0
            self._tut_fired.clear()
            self.phase_timer       = 0.0
            self.wave_timer        = 0.0
            self.wave              = 0
            self.invincible        = 1.5
            self._tut_cuke_cd      = 0.0
            self._tut_cuke_sent    = 0
            self._tut_bomb_done    = False
            self._tut_bomb_used    = False
            self._tut_bomb_delay   = -1.0
            self._trans_notified   = False
            self._tut_q_dirty      = True    # 重建队列
            self.graze_bar         = 0.0
            self.float_texts.clear()
            self.float_texts.append(FloatText(
                "压力过高！教程重新开始", V2_AREA_W//2-120, SH//2-20,
                life=2.5, size=26, color="#FFFFFF"))

        def _tut_bomb_explode(self):
            """教程轰炸：全屏密集弹幕"""
            cx = float(V2_AREA_W // 2)
            # 四个方向展开
            for i in range(16):
                ang = math.radians(i * 22.5)
                self.bullets.append(Entity(cx, V2_AREA_H//2, 14, 14,
                                           vx=math.cos(ang)*180, vy=math.sin(ang)*180, tag="bullet"))
            # 竖向雨
            for i in range(9):
                self.bullets.append(Entity(30.0 + i * 50, -20, 14, 14,
                                           vx=0, vy=220.0, tag="bullet"))
            # 两侧斜射
            for i in range(5):
                self.bullets.append(Entity(0.0, 100.0 + i*80, 14, 14,
                                           vx=160.0, vy=random.uniform(60,120), tag="bullet"))
                self.bullets.append(Entity(float(V2_AREA_W), 100.0 + i*80, 14, 14,
                                           vx=-160.0, vy=random.uniform(60,120), tag="bullet"))

        def _spawn_safe_zone(self):
            x = random.uniform(80, V2_AREA_W - 80)
            y = random.uniform(100, V2_AREA_H - 200)
            self.safe_zones.append(SafeZone(x, y, 70.0))

        def _emit(self):
            cx  = float(V2_AREA_W // 2)
            idx = self.wave % 6
            sm  = DIFF.v2_bullet_spd_mult  # 速度倍率
            if idx == 0:
                for a in range(-3, 4):
                    ang = math.radians(90 + a * 18)
                    self.bullets.append(Entity(cx, -20, 14, 14, vx=math.cos(ang)*160*sm, vy=math.sin(ang)*160*sm, tag="bullet"))
            elif idx == 1:
                for side in [-1, 1]:
                    for i in range(3):
                        self.bullets.append(Entity(cx+side*80, -20, 14, 14, vx=side*random.uniform(30,80)*sm, vy=random.uniform(140,200)*sm, tag="bullet"))
            elif idx == 2:
                for i in range(7):
                    self.bullets.append(Entity(30+i*60, -20, 14, 14, vx=0, vy=random.uniform(150,220)*sm, tag="bullet"))
            elif idx == 3:
                for i in range(8):
                    ang = math.radians(i*45 + self.wave*30)
                    self.bullets.append(Entity(cx, -20, 14, 14, vx=math.cos(ang)*140*sm, vy=abs(math.sin(ang))*140*sm+80, tag="bullet"))
            elif idx == 4:
                for i in range(5):
                    self.bullets.append(Entity(random.uniform(20, V2_AREA_W-20), -20, 12, 12, vx=random.uniform(-20,20)*sm, vy=random.uniform(180,260)*sm, tag="bullet"))
            else:
                for a in range(-2, 3):
                    ang = math.radians(90 + a*22)
                    self.bullets.append(Entity(cx, -20, 14, 14, vx=math.cos(ang)*140*sm, vy=math.sin(ang)*140*sm, tag="bullet"))
                for i in range(4):
                    self.bullets.append(Entity(60+i*90, -20, 12, 12, vx=0, vy=200*sm, tag="bullet"))


    class SakikoBoss(python_object):
        """
        Round 3 Boss — 丰川祥子
        Phase 1: 5x5走格子（左半屏）+ 弹幕躲避（右半屏）（血量3）
        Phase 2: 左手打字防空炮（血量5）
        """
        # ── Phase 1 走格子 ────────────────────────────────
        GRID_W      = 5
        GRID_H      = 5

        @property
        def P1_MAX_HP(self):
            return 7 if DIFF.current >= DIFF.HARD else 5

        @property
        def P2_MAX_HP(self):
            return 7 if DIFF.current >= DIFF.HARD else 5

        # 阶段二词库（纯左手 QWERTASDFGZXCVB，分难度层级）
        WORDS_T1 = ["SAD", "BAD", "WAR", "RAW"]
        WORDS_T2 = ["FEAR", "SCAR", "FADE", "STAR",
                    "TEAR", "RAGE", "FACE", "CRAZE"]
        WORDS_T3 = ["SECRET", "REGRET", "DEFEAT",
                    "STRESS", "CRAFTS"]
        WORDS_T4 = ["FEARLESS", "DARKNESS", "STRANGER",
                    "WEAKNESS", "CARELESS"]   # 7~8字母 - 困难专属终结词

        # 阶段一 Boss 弹幕波次（较规律，偏圆形扩散）
        def __init__(self):
            self.active      = False
            self.phase       = 1       # 1 or 2
            self.p1_hp       = self.P1_MAX_HP
            self.p2_hp       = self.P2_MAX_HP
            self.round_clear = False
            self.float_texts = []
            # ── 阶段一：5x5走格子 ─────────────────────────
            self.grid_cursor = [2, 2]   # [row, col] 起点中央
            self.cursor_start= [2, 2]   # 被红块击中后复位点
            self.grid_slot   = [0, 0]   # 目标（金块）
            self.hazards     = []       # 危险红块列表
            self.blue_cell   = [0, 0]   # 必须经过的蓝色格子1
            self.blue_cell2  = [0, 0]   # 必须经过的蓝色格子2
            self.blue_cell3  = [0, 0]   # 必须经过的蓝色格子3（低血量激活）
            self.blue_visited= False    # 是否已踩过蓝格1
            self.blue_visited2=False    # 是否已踩过蓝格2
            self.blue_visited3=False    # 是否已踩过蓝格3
            self._three_blue_active = False  # 第三蓝格是否激活
            self.path_history= []       # 玩家已走路径 [[r,c], ...]
            self._hit_cd     = 0.0      # 踩红块后的复位冷却（防连判）
            # ── 一阶段祥子横移 ─────────────────────────────
            self.sakiko_x    = float(V2_AREA_W // 2)   # 祥子x坐标（弹幕区内）
            self._sakiko_vx  = 160.0 if DIFF.current == DIFF.EXTREME else (140.0 if DIFF.current >= DIFF.HARD else 90.0)
            self._last_px    = float(V2_AREA_W // 2)
            self._beam_t     = 0.0
            self._beam_col   = 0
            self._enter_t    = 0.0
            self._enter_done = False
            self._p1_wave_t  = 0.0
            self._p1_wave    = 0
            # ── 阶段二：打字 ────────────────────────────────
            self._cur_word   = ""
            self._typed      = ""
            self._word_show_t= 0.0
            self._p2_wave_t  = 0.0
            self._p2_wave    = 0
            self._blast_anim = []
            self._p2_hits    = 0
            self._p2_dir     = 1.0
            self._p2_fake_cd = random.uniform(2.0, 3.5)
            self._p2_fake_fl = 0.0
            self._p2_clear_t = 0.0
            self._trans_t    = 0.0
            self._wall_cd    = 0.0
            self._penalty_cd = 0.0
            self._grid_timer = 0.0
            self._word_timer = 0.0
            self.P1_TIMEOUT  = 9999.0   # 无限制
            self.P2_TIMEOUT  = 9999.0   # 无限制
            self._p2_elapsed = 0.0
            self._junk_words = []

            self._reset_grid()

        def _grid_has_path(self, start, goal, haz_set):
            """BFS：检查 start → goal 是否有路（绕开红块）"""
            queue   = [tuple(start)]
            visited = {tuple(start)}
            while queue:
                r, c   = queue.pop(0)
                if r == goal[0] and c == goal[1]:
                    return True
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr2, nc2 = r+dr, c+dc
                    if 0 <= nr2 < self.GRID_H and 0 <= nc2 < self.GRID_W:
                        if (nr2, nc2) not in visited and (nr2, nc2) not in haz_set:
                            visited.add((nr2, nc2))
                            queue.append((nr2, nc2))
            return False

        def _reset_grid(self):
            """重置5x5走格子：蓝格数量根据 _three_blue_active 决定（2或3个），BFS保证全部可达"""
            use3 = getattr(self, '_three_blue_active', False)

            def _inner_cells():
                """返回非边缘格坐标列表（1~3行，1~3列），共3x3=9个安全位置"""
                return [(r, c) for r in range(1, self.GRID_H-1) for c in range(1, self.GRID_W-1)]

            def _adj(r, c):
                """返回(r,c)四邻格坐标集合"""
                return {(r+dr, c+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
                        if 0 <= r+dr < self.GRID_H and 0 <= c+dc < self.GRID_W}

            inner = _inner_cells()

            for _attempt in range(400):
                # 起点：任意位置
                cr = random.randint(0, self.GRID_H - 1)
                cc = random.randint(0, self.GRID_W - 1)
                # 蓝格和金块只能放内部格（非边缘），避免角落死局
                _inner_pool = [pos for pos in inner if pos != (cr, cc)]
                if len(_inner_pool) < (4 if use3 else 3): continue
                random.shuffle(_inner_pool)
                (br, bc)   = _inner_pool[0]
                (br2, bc2) = _inner_pool[1]
                (sr, sc)   = _inner_pool[2]
                if use3:
                    if len(_inner_pool) < 4: continue
                    (br3, bc3) = _inner_pool[3]
                else:
                    br3, bc3 = -1, -1

                used = {(cr,cc),(sr,sc),(br,bc),(br2,bc2)}
                if use3: used.add((br3,bc3))

                # 红块禁止出现在蓝格/金块的紧邻位置
                _safe_cells  = set(used)
                for (r, c) in list(used):
                    _safe_cells |= _adj(r, c)

                hazards = []
                n_haz = random.randint(1, 2)
                inner_attempts = 0
                while len(hazards) < n_haz and inner_attempts < 60:
                    hr = random.randint(0, self.GRID_H - 1)
                    hc = random.randint(0, self.GRID_W - 1)
                    inner_attempts += 1
                    if (hr, hc) not in _safe_cells:
                        _safe_cells.add((hr, hc))
                        hazards.append([hr, hc])
                if len(hazards) < 1: continue
                haz_set = set(tuple(h) for h in hazards)
                # BFS验证所有节点可达
                if not self._grid_has_path([cr,cc],  [br,bc],   haz_set): continue
                if not self._grid_has_path([cr,cc],  [br2,bc2], haz_set): continue
                if not self._grid_has_path([br,bc],  [br2,bc2], haz_set): continue
                if use3:
                    if not self._grid_has_path([cr,cc],  [br3,bc3], haz_set): continue
                    if not self._grid_has_path([br,bc],  [br3,bc3], haz_set): continue
                    if not self._grid_has_path([br2,bc2],[br3,bc3], haz_set): continue
                    if not self._grid_has_path([br3,bc3],[sr,sc],   haz_set): continue
                else:
                    if not self._grid_has_path([br,bc],  [sr,sc],   haz_set): continue
                    if not self._grid_has_path([br2,bc2],[sr,sc],   haz_set): continue
                break
            self.cursor_start  = [cr, cc]
            self.grid_cursor   = [cr, cc]
            self.grid_slot     = [sr, sc]
            self.blue_cell     = [br, bc]
            self.blue_cell2    = [br2, bc2]
            self.blue_cell3    = [br3, bc3] if use3 else [-1, -1]
            self.blue_visited  = False
            self.blue_visited2 = False
            self.blue_visited3 = False
            self.path_history  = [[cr, cc]]
            self.hazards       = hazards
            self._hit_cd       = 0.0
            self._grid_timer   = 0.0   # 重置超时计时器

        def _next_word(self):
            hits = getattr(self, '_p2_hits', 0)
            if DIFF.current == DIFF.EXTREME:
                # 极限：全程5~8字母长词
                pool = self.WORDS_T4 if hits >= 3 else self.WORDS_T3
            elif DIFF.current >= DIFF.HARD:
                if hits < 3:
                    pool = self.WORDS_T2
                elif hits < 4:
                    pool = self.WORDS_T3
                else:
                    pool = self.WORDS_T4
            else:
                if hits < 2:
                    pool = self.WORDS_T1
                elif hits < 4:
                    pool = self.WORDS_T2
                else:
                    pool = self.WORDS_T3
            self._cur_word    = random.choice(pool)
            self._typed       = ""
            self._word_show_t = 0.0
            self._word_timer  = 0.0

        def start(self):
            self.active = True
            self._enter_t = 0.0

        def move_cursor(self, dr, dc):
            """走格子：移动游标，踩红块复位，踩蓝块标记，踩金块触发击中"""
            if self.phase != 1 or not self.active: return
            if getattr(self, '_hit_cd', 0.0) > 0: return  # 复位冷却中
            nr = self.grid_cursor[0] + dr
            nc = self.grid_cursor[1] + dc
            # 边界检查
            if not (0 <= nr <= self.GRID_H - 1): return
            if not (0 <= nc <= self.GRID_W - 1): return
            # 踩到红块：复位到起点 + 压力惩罚 + 路径清空
            if [nr, nc] in self.hazards:
                self.grid_cursor   = list(self.cursor_start)
                self.blue_visited  = False
                self.blue_visited2 = False
                self.blue_visited3 = False
                self.path_history  = [list(self.cursor_start)]
                self._hit_cd = 0.5
                PRESSURE.add(10.0)
                self.float_texts.append(FloatText(
                    "！踩到红块 +10压力", V2_AREA_W//2-100, 60,
                    life=1.0, size=18, color="#FF4444"))
                return
            # 踩到蓝格1
            if [nr, nc] == self.blue_cell and not self.blue_visited:
                self.blue_visited = True
                self.grid_cursor = [nr, nc]
                if len(self.path_history) >= 2 and [nr, nc] == self.path_history[-2]:
                    self.path_history.pop()
                else:
                    self.path_history.append([nr, nc])
                _need = (0 if self.blue_visited2 else 1) + (0 if (self.blue_visited3 or self.blue_cell3 == [-1,-1]) else 1)
                self.float_texts.append(FloatText(
                    ("✓ 蓝格1！还差%d个！" % _need) if _need else "✓ 全踩了！去踩金块！",
                    V2_AREA_W//2-140, 60, life=1.2, size=17, color="#44AAFF"))
                return
            # 踩到蓝格2
            if [nr, nc] == self.blue_cell2 and not self.blue_visited2:
                self.blue_visited2 = True
                self.grid_cursor = [nr, nc]
                if len(self.path_history) >= 2 and [nr, nc] == self.path_history[-2]:
                    self.path_history.pop()
                else:
                    self.path_history.append([nr, nc])
                _need2 = (0 if self.blue_visited else 1) + (0 if (self.blue_visited3 or self.blue_cell3 == [-1,-1]) else 1)
                self.float_texts.append(FloatText(
                    ("✓ 蓝格2！还差%d个！" % _need2) if _need2 else "✓ 全踩了！去踩金块！",
                    V2_AREA_W//2-140, 60, life=1.2, size=17, color="#44AAFF"))
                return
            # 踩到蓝格3（低血量激活时）
            if self.blue_cell3 != [-1,-1] and [nr, nc] == self.blue_cell3 and not self.blue_visited3:
                self.blue_visited3 = True
                self.grid_cursor = [nr, nc]
                if len(self.path_history) >= 2 and [nr, nc] == self.path_history[-2]:
                    self.path_history.pop()
                else:
                    self.path_history.append([nr, nc])
                _need3 = (0 if self.blue_visited else 1) + (0 if self.blue_visited2 else 1)
                self.float_texts.append(FloatText(
                    ("✓ 蓝格3！还差%d个！" % _need3) if _need3 else "✓ 全踩了！去踩金块！",
                    V2_AREA_W//2-140, 60, life=1.2, size=17, color="#44AAFF"))
                return
            # 踩到金块：必须先经过所有蓝格
            if [nr, nc] == self.grid_slot:
                _need_all = (0 if self.blue_visited else 1) + (0 if self.blue_visited2 else 1) + (0 if (self.blue_visited3 or self.blue_cell3 == [-1,-1]) else 1)
                if _need_all > 0:
                    self.float_texts.append(FloatText(
                        "还有%d个蓝格没踩！" % _need_all, V2_AREA_W//2-80, 60,
                        life=1.0, size=20, color="#FF8844"))
                    return
                self.grid_cursor = [nr, nc]
                if len(self.path_history) >= 2 and [nr, nc] == self.path_history[-2]:
                    self.path_history.pop()
                else:
                    self.path_history.append([nr, nc])
                self._on_box_clear()
                return
            # 正常移动
            self.grid_cursor = [nr, nc]
            if len(self.path_history) >= 2 and [nr, nc] == self.path_history[-2]:
                self.path_history.pop()
            else:
                self.path_history.append([nr, nc])
                if len(self.path_history) > 30:
                    self.path_history = self.path_history[-30:]

        def _on_box_clear(self):
            """踩中金块：检查是否命中祥子，发射光柱，扣Boss血，重置网格"""
            v2 = getattr(self, '_v2_ref', None)
            self._beam_t   = 1.2
            self._beam_col = self.grid_slot[1]
            # 命中判定：玩家x与祥子x距离在70px以内才算命中
            hit = abs(self._last_px - self.sakiko_x) < 70
            if not hit:
                self.float_texts.append(FloatText(
                    "打空了！找准祥子再射！", V2_AREA_W//2-130, 30,
                    life=1.5, size=22, color="#FF8844"))
                self._reset_grid()
                return
            self.p1_hp -= 1
            self.float_texts.append(FloatText(
                "💥 击中白祥！ HP %d/%d" % (self.p1_hp, self.P1_MAX_HP),
                V2_AREA_W//2-120, 30, life=2.0, size=24, color="#00FF88"))
            if self.p1_hp <= 0:
                # 进入阶段二（黑祥）：清空弹幕 + 减压 + 启动过渡动画
                self.phase   = 2
                self._trans_t = 0.001   # 启动过渡
                if v2: v2.bullets.clear()
                PRESSURE.value = max(0.0, PRESSURE.value - 50.0)
                self.float_texts.append(FloatText(
                    "丰川祥子……黑化了", V2_AREA_W//2-120, 60,
                    life=3.0, size=26, color="#000000"))
                self.float_texts.append(FloatText(
                    "压力 -50", V2_AREA_W//2-60, 90,
                    life=2.0, size=22, color="#44AAFF"))
                self._next_word()
            else:
                # 血量≤2（普通）或≤3（困难/极限）时激活第三蓝格
                _three_blue_thresh = 3 if DIFF.current >= DIFF.HARD else 2
                if self.p1_hp <= _three_blue_thresh and not getattr(self, '_three_blue_active', False):
                    self._three_blue_active = True
                    self.float_texts.append(FloatText(
                        "祥子发怒！蓝格增加！", V2_AREA_W//2-130, 55,
                        life=2.0, size=20, color="#FF6644"))
                self._reset_grid()

        def type_key(self, key_char, v2):
            """阶段二：键盘输入处理（打完整个单词才发射激光，需命中祥子才扣血）"""
            if self.phase != 2 or not self.active: return
            if getattr(self, '_p2_clear_t', 0.0) > 0: return   # 胜利淡出期间不接受输入
            c = key_char.upper()
            if not self._cur_word: return
            expected = self._cur_word[len(self._typed)] if len(self._typed) < len(self._cur_word) else ""
            if c == expected:
                self._typed += c
                self._word_show_t = 0.0
                # ── 单词完成：发射激光，命中才扣血 ──
                if self._typed == self._cur_word:
                    px = float(v2.px); py = float(v2.py)
                    self._blast_anim.append([px, py, 0.7])
                    self._beam_t   = 1.2
                    self._beam_col = 0
                    # 命中判定：玩家x与黑祥x距离在70px以内
                    hit = abs(v2.px - self.sakiko_x) < 70
                    if hit:
                        self._p2_hits = getattr(self, '_p2_hits', 0) + 1
                        self.p2_hp -= 1
                        v2.float_texts.append(FloatText(
                            "💥 击中黑祥！ HP %d/%d" % (self.p2_hp, self.P2_MAX_HP),
                            V2_AREA_W//2-120, 40, life=2.0, size=24, color="#00BB55"))
                        if self.p2_hp <= 0:
                            # 胜利：开始淡出计时
                            self._p2_clear_t = 0.01   # 开始计时（>0表示进入淡出）
                            v2.bullets.clear()
                            CUKES.collected += 10
                            v2.float_texts.append(FloatText(
                                "丰川祥子……消失了", V2_AREA_W//2-130, SH//2-60,
                                life=4.0, size=30, color="#333333"))
                            v2.float_texts.append(FloatText(
                                "🥒 ×10", V2_AREA_W//2-40, SH//2,
                                life=3.0, size=28, color="#1A7A00"))
                        else:
                            self._next_word()
                    else:
                        v2.float_texts.append(FloatText(
                            "打空了！对准祥子！", V2_AREA_W//2-110, 40,
                            life=1.5, size=22, color="#FF8844"))
                        self._next_word()
            else:
                # ── 打错惩罚 ──
                if getattr(self, '_penalty_cd', 0.0) <= 0:
                    self._typed = ""
                    self._penalty_cd = 0.3
                    _pen_pressure = 15.0 if DIFF.current >= DIFF.HARD else 10.0
                    PRESSURE.add(_pen_pressure)
                    _pen_msg = "×  进度清零 +%d压" % int(_pen_pressure)
                    v2.float_texts.append(FloatText(
                        _pen_msg, int(v2.px)-60, int(v2.py)-30,
                        life=0.8, size=22, color="#FF4444"))
                    cx = float(V2_AREA_W // 2)
                    dx = v2.px - cx; dy = v2.py - 60
                    dist = max(1, math.sqrt(dx*dx+dy*dy))
                    if DIFF.current == DIFF.EXTREME:
                        # 极限：直接砸向玩家的红色惩罚弹
                        v2.bullets.append(Entity(cx, 0.0, 16, 16,
                            vx=dx/dist*400, vy=dy/dist*400, tag="bullet"))
                        v2.float_texts.append(FloatText(
                            "惩罚弹！快躲！", int(v2.px)-40, int(v2.py)-55,
                            life=0.6, size=18, color="#FF0000"))
                    else:
                        v2.bullets.append(Entity(cx, 60, 14, 14,
                            vx=dx/dist*250, vy=dy/dist*250, tag="bullet"))

        def tick(self, dt, v2):
            if not self.active or self.round_clear: return

            # 保存v2引用供 _on_box_clear 等内部方法使用
            self._v2_ref  = v2
            # 记录玩家当前x（用于命中判定）
            self._last_px = v2.px

            # 一阶段：祥子动态移动（血越少越快，含假动作）
            if self.phase == 1:
                # HP越低速度越快：6HP=70, 1HP=160
                _dmg_now = self.P1_MAX_HP - self.p1_hp   # 0~5
                _spd_now = 70.0 + _dmg_now * 18.0
                # _sakiko_vx 只作为方向符号（+1 或 -1）
                if not hasattr(self, '_sak_dir'):
                    self._sak_dir   = 1.0   # +1=向右, -1=向左
                    self._fake_cd   = random.uniform(2.5, 4.0)
                    self._fake_flash= 0.0
                self._fake_cd   -= dt
                self._fake_flash = max(0.0, self._fake_flash - dt)
                if self._fake_cd <= 0:
                    # 假动作：只翻转方向，不改变速度大小
                    self._sak_dir  = -self._sak_dir
                    self._fake_cd  = random.uniform(2.0, 4.0 - _dmg_now * 0.3)
                    self._fake_flash = 0.3
                self.sakiko_x += self._sak_dir * _spd_now * dt
                if self.sakiko_x >= V2_AREA_W - 20:
                    self.sakiko_x  = float(V2_AREA_W - 20)
                    self._sak_dir  = -1.0
                elif self.sakiko_x <= 20:
                    self.sakiko_x  = 20.0
                    self._sak_dir  = 1.0

            # 飘字
            for ft in list(self.float_texts):
                ft.tick(dt)
            self.float_texts = [ft for ft in self.float_texts if ft.alive]

            # 出场动画
            if not self._enter_done:
                self._enter_t += dt
                if self._enter_t >= 2.0:
                    self._enter_done = True
                    self.float_texts.append(FloatText(
                        "WASD 走格子！踩蓝格再踩金块！", V2_AREA_W//2-160, 55,
                        life=4.0, size=18, color="#FFFFFF"))
                    self.float_texts.append(FloatText(
                        "瞄准祥子位置再发射！", V2_AREA_W//2-100, 80,
                        life=4.0, size=18, color="#CCCCCC"))
                return

            # 光柱动画计时
            if self._beam_t > 0:
                self._beam_t = max(0.0, self._beam_t - dt)

            # 防空炮气浪动画
            for b in self._blast_anim:
                b[2] -= dt
            self._blast_anim = [b for b in self._blast_anim if b[2] > 0]

            # 踩红块复位冷却
            if getattr(self, '_hit_cd', 0.0) > 0:
                self._hit_cd -= dt

            # 过渡动画计时（phase 1→2 黑→白渐变，持续1.2s）
            if getattr(self, '_trans_t', 0.0) > 0:
                self._trans_t = min(1.0, self._trans_t + dt / 1.2)

            # ── 一阶段超时惩罚（仅普通/简单模式）──
            if self.phase == 1 and DIFF.current < DIFF.HARD:
                self._grid_timer += dt
                if self._grid_timer >= self.P1_TIMEOUT:
                    self._grid_timer = 0.0
                    _p1_pen = 20.0
                    PRESSURE.add(_p1_pen)
                    self.float_texts.append(FloatText(
                        "⏰ 太慢了！+%d压力" % int(_p1_pen), V2_AREA_W//2-130, 50,
                        life=1.5, size=20, color="#FF6600"))

            # 阶段二各逻辑
            if self.phase == 2:
                # 胜利淡出期间：只推进计时，2秒后切场景
                if getattr(self, '_p2_clear_t', 0.0) > 0:
                    self._p2_clear_t += dt
                    if self._p2_clear_t >= 2.8:
                        self.round_clear = True
                        v2.round_clear   = True
                    return   # 淡出期间不执行其他逻辑
                # 二阶段总时间（用于弹幕密度递增）
                self._p2_elapsed += dt
                # ── 二阶段超时惩罚（6秒没打完单词 +25压力+换词）──
                self._word_timer += dt
                if self._word_timer >= self.P2_TIMEOUT:
                    self._word_timer = 0.0
                    PRESSURE.add(18.0)
                    self.float_texts.append(FloatText(
                        "⏰ 太慢了！+18压力", V2_AREA_W//2-130, 50,
                        life=1.5, size=20, color="#FF4400"))
                    self._next_word()
                # 黑祥横移（血越少越快，含假动作）
                _p2_dmg = self.P2_MAX_HP - self.p2_hp   # 0~4
                _p2_spd = 80.0 + _p2_dmg * 25.0         # 80→180
                self._p2_fake_cd -= dt
                self._p2_fake_fl  = max(0.0, self._p2_fake_fl - dt)
                if self._p2_fake_cd <= 0:
                    self._p2_dir     = -self._p2_dir
                    self._p2_fake_cd = random.uniform(1.5, 3.5 - _p2_dmg * 0.4)
                    self._p2_fake_fl = 0.3
                self.sakiko_x += self._p2_dir * _p2_spd * dt
                if self.sakiko_x >= V2_AREA_W - 20:
                    self.sakiko_x = float(V2_AREA_W - 20); self._p2_dir = -1.0
                elif self.sakiko_x <= 20:
                    self.sakiko_x = 20.0;                  self._p2_dir =  1.0
                # 单词超时换词
                self._word_show_t += dt
                if self._word_show_t > 8.0 and self._typed == "":
                    self._next_word()
                # 打错惩罚冷却
                if getattr(self, '_penalty_cd', 0.0) > 0:
                    self._penalty_cd -= dt

            # ── 发射弹幕（两个阶段都有，动态间隔）──
            if self.phase == 1:
                _p1_dmg = self.P1_MAX_HP - self.p1_hp
                wave_interval = max(0.8, 2.0 - _p1_dmg * 0.22)
            else:
                # 黑祥：血越少+时间越久弹幕越频繁
                _p2_dmg2 = self.P2_MAX_HP - self.p2_hp
                _time_factor = min(0.3, self._p2_elapsed * 0.008)   # 最多再缩短0.3s（约37秒后达到上限）
                wave_interval = max(0.55, 1.4 - _p2_dmg2 * 0.14 - _time_factor)

            # ── 乱码扰视词（p2_hp≤2激活，大字横穿屏幕）──
            _junk_threshold = 4 if DIFF.current >= DIFF.HARD else 2
            if self.phase == 2 and self.p2_hp <= _junk_threshold and getattr(self, '_p2_clear_t', 0.0) <= 0:
                if not hasattr(self, '_junk_cd'):
                    self._junk_cd = 0.0
                self._junk_cd -= dt
                if self._junk_cd <= 0:
                    self._junk_cd = random.uniform(1.2, 2.2)
                    _junk_pool = [
                        "DESPAIR", "HOPELESS", "崩壊", "絶望", "Oblivionis",
                        "FAKE", "LIAR", "XQWZJK", "##ERROR##", "失格",
                        "あなたには", "WORTHLESS", "GIVE UP", "消えろ", "ZXQ##"
                    ]
                    _jw_txt  = random.choice(_junk_pool)
                    _jw_size = random.randint(40, 80)
                    _jw_from_left = random.random() > 0.5
                    _jw_x  = -200.0 if _jw_from_left else float(V2_AREA_W + 50)
                    _jw_vx = random.uniform(120, 200) * (1 if _jw_from_left else -1)
                    _jw_y  = random.uniform(60, SH - 120)
                    self._junk_words.append([_jw_x, _jw_y, _jw_vx, _jw_txt,
                                             random.uniform(0.09, 0.16), _jw_size, 4.0])
            # 推进乱码词位置
            for _jw in list(getattr(self, '_junk_words', [])):
                _jw[0] += _jw[2] * dt
                _jw[6] -= dt
            if hasattr(self, '_junk_words'):
                self._junk_words = [j for j in self._junk_words if j[6] > 0]
            if self.phase == 1:
                self._p1_wave_t += dt
                if self._p1_wave_t >= wave_interval:
                    self._p1_wave_t = 0.0
                    self._emit_p1(v2)
                    self._p1_wave += 1
            else:
                self._p2_wave_t += dt
                if self._p2_wave_t >= wave_interval:
                    self._p2_wave_t = 0.0
                    self._emit_p2(v2)
                    self._p2_wave += 1

        def _emit_p1(self, v2):
            """阶段一：动态弹幕——HP越低子弹越多越快"""
            cx = float(V2_AREA_W // 2)
            idx = self._p1_wave % 4
            # 动态倍率：6HP=1.0，1HP=1.8
            dmg = self.P1_MAX_HP - self.p1_hp   # 0~5
            sm  = 1.0 + dmg * 0.16              # 1.0~1.8
            # 额外子弹数（低血时多发）
            extra = max(0, dmg - 2)             # 0~3
            if idx == 0:
                # 圆形扩散（低血时更密，角速度更小）
                n_bullets = 12 + extra * 3
                for i in range(n_bullets):
                    ang = math.radians(i * (360.0 / n_bullets))
                    v2.bullets.append(Entity(cx, 80, 12, 12,
                        vx=math.cos(ang)*120*sm, vy=math.sin(ang)*120*sm, tag="bullet"))
            elif idx == 1:
                # 竖向雨（低血时更密）
                n_rain = 7 + extra * 2
                for i in range(n_rain):
                    v2.bullets.append(Entity(20 + i*(V2_AREA_W-40)//max(1,n_rain-1), -20, 12, 12,
                        vx=random.uniform(-20,20)*sm, vy=140*sm, tag="bullet"))
            elif idx == 2:
                # 左右夹击（低血时多行）
                n_rows = 4 + extra
                for i in range(n_rows):
                    v2.bullets.append(Entity(0, 60+i*70, 12, 12,
                        vx=130*sm, vy=random.uniform(20,60)*sm, tag="bullet"))
                    v2.bullets.append(Entity(V2_AREA_W, 60+i*70, 12, 12,
                        vx=-130*sm, vy=random.uniform(20,60)*sm, tag="bullet"))
            else:
                # 正弦波 + 低血时追踪弹
                n_wave = 6 + extra
                for i in range(n_wave):
                    v2.bullets.append(Entity(20 + i*(V2_AREA_W-40)//max(1,n_wave-1), -20, 12, 12,
                        vx=math.sin(i*1.2)*40*sm, vy=150*sm, tag="bullet"))
                if dmg >= 3:
                    # 追踪弹（血少于4时额外追踪）
                    dx = v2.px - cx; dy = v2.py - 80
                    dist = max(1, math.sqrt(dx*dx + dy*dy))
                    spd = 160 * sm
                    v2.bullets.append(Entity(cx, 80, 13, 13,
                        vx=dx/dist*spd, vy=dy/dist*spd, tag="bullet"))

        def _emit_p2(self, v2):
            """阶段二：弹幕按击杀进度升级（1-2击规律，3-4击追踪，5击收缩墙）"""
            if getattr(self, '_wall_phase', False): return   # 墙阶段不发普通弹
            cx = float(V2_AREA_W // 2)
            idx = self._p2_wave % 5
            hits = getattr(self, '_p2_hits', 0)
            sm  = 1.0 + hits * 0.22   # 随击杀数加速（第1击1.0，第4击约1.66）
            if idx == 0:
                if hits < 2:
                    # 初期：圆形扩散（规律，偏慢）
                    for i in range(10):
                        ang = math.radians(i * 36)
                        v2.bullets.append(Entity(cx, 80, 12, 12,
                            vx=math.cos(ang)*110*sm, vy=math.sin(ang)*110*sm, tag="bullet"))
                else:
                    # 后期：高速追踪
                    dx = v2.px - cx; dy = v2.py - 60
                    dist = max(1, math.sqrt(dx*dx+dy*dy))
                    spd = 220*sm
                    v2.bullets.append(Entity(cx, 60, 14, 14,
                        vx=dx/dist*spd, vy=dy/dist*spd, tag="bullet"))
                    v2.bullets.append(Entity(cx-40, 60, 12, 12,
                        vx=(dx/dist*spd*0.8+50), vy=dy/dist*spd*0.8, tag="bullet"))
                    v2.bullets.append(Entity(cx+40, 60, 12, 12,
                        vx=(dx/dist*spd*0.8-50), vy=dy/dist*spd*0.8, tag="bullet"))
            elif idx == 1:
                # 高速扇形
                for i in range(-3, 4):
                    ang = math.radians(90 + i*14)
                    v2.bullets.append(Entity(cx, -20, 13, 13,
                        vx=math.cos(ang)*200*sm, vy=math.sin(ang)*200*sm, tag="bullet"))
            elif idx == 2:
                # 高速水平横扫
                for i in range(5):
                    v2.bullets.append(Entity(0, 60+i*60, 12, 12,
                        vx=260*sm, vy=random.uniform(-20,40), tag="bullet"))
            elif idx == 3:
                # 全屏密集雨
                for i in range(10):
                    v2.bullets.append(Entity(20+i*43, -20, 11, 11,
                        vx=random.uniform(-30,30), vy=random.uniform(200,280)*sm, tag="bullet"))
            else:
                # 螺旋
                for i in range(8):
                    ang = math.radians(i*45 + self._p2_wave*22)
                    v2.bullets.append(Entity(cx, 80, 12, 12,
                        vx=math.cos(ang)*180*sm, vy=abs(math.sin(ang))*160*sm+60, tag="bullet"))

    class SoyoBoss(python_object):
        """
        Round 2 Boss — 长崎爽世
        114 秒时间轴，绑定《春日影》
        """
        TOTAL_DUR   = 114.0

        @property
        def MAX_SHIELD(self):
            return 7 if DIFF.current >= DIFF.HARD else 5

        @property
        def STUN_DUR(self):
            if DIFF.current == DIFF.EXTREME: return 4.0
            return 4.5 if DIFF.current >= DIFF.HARD else 8.0

        BULLET_SPD  = 1.8

        @property
        def PHASES(self):
            if DIFF.current == DIFF.EXTREME:
                return [
                    (  0,   2, 0.00, "这个，不需要了"),
                    (  2,  30, 0.50, None),
                    ( 30,  60, 0.80, None),
                    ( 45, 114, 1.00, None),
                ]
            if DIFF.current >= DIFF.HARD:
                return [
                    (  0,   3, 0.00, "这个，不需要了"),
                    (  3,  40, 0.40, None),
                    ( 40,  70, 0.70, None),
                    ( 50, 114, 1.00, None),
                ]
            return [
                (  0,  10, 0.00, "这个，不需要了"),
                ( 10,  45, 0.30, None),
                ( 45,  75, 0.60, None),
                ( 75, 114, 1.00, None),
            ]

        GATE_TIMES = [48.0, 58.0, 68.0]

        def __init__(self):
            self.active       = False
            self.t            = 0.0
            self.shield       = 5   # 初始值，start()时会用MAX_SHIELD覆盖
            self.stunned      = False
            self.stun_t       = 0.0
            self.round_clear  = False
            # 玩家子弹（黄瓜）列表：z 值 0→1
            self.p_bullets    = []
            self._pb_cd       = 0.0
            # QTE判定条系统
            self.qte_active   = False
            self.qte_t        = 0.0
            self.qte_dir      = 1
            self.qte_pos      = 0.0
            self.qte_green_s  = 0.0
            self.qte_green_w  = 0.0
            self.qte_red_s    = 0.0
            self.qte_red_w    = 0.0
            # 台词飘字
            self.float_texts  = []
            self._fired       = set()
            self._enter_t     = 0.0
            self._enter_done  = False

        def reset(self):
            self.__init__()

        def start(self):
            self.active = True
            self.t      = 0.0
            self.shield = self.MAX_SHIELD

        def activate_qte(self, lane):
            """按Z/J键：若无QTE则唤出判定条；若有QTE则结算"""
            if not self.active or self.stunned: return
            if self._pb_cd > 0: return
            if CUKES.collected < 1: return
            # 前后夹击阶段禁止攻击
            if getattr(GM._p3, '_boss_pincer', False): return

            if not self.qte_active:
                # 唤出 QTE 判定条，随机生成绿区/红区
                self.qte_active = True
                self.qte_t      = 0.0
                self.qte_pos    = 0.0
                self.qte_dir    = 1
                # 绿区随机位置(30%宽度)，红区贴边(10%宽度)
                gs = random.uniform(0.05, 0.55)
                gw = random.uniform(0.28, 0.38)
                # 红区随机在绿区左侧或右侧边缘
                if random.random() < 0.5:
                    rs = max(0.0, gs - 0.10)
                    rw = 0.10
                else:
                    rs = min(0.90, gs + gw)
                    rw = 0.10
                self.qte_green_s = gs
                self.qte_green_w = gw
                self.qte_red_s   = rs
                self.qte_red_w   = rw
                self._qte_lane   = float(lane)
                self._pb_cd      = 0.1
            else:
                # 结算：判定指针位置
                p = self.qte_pos
                self._settle_qte(p, self._qte_lane)
                self.qte_active = False
                self._pb_cd     = 0.5

        def _settle_qte(self, p, lane):
            """根据指针位置决定射击结果"""
            in_red   = (self.qte_red_s <= p <= self.qte_red_s + self.qte_red_w)
            in_green = (self.qte_green_s <= p <= self.qte_green_s + self.qte_green_w)
            if in_red:
                # 红区暴击：消耗2黄瓜发2颗
                shots_r = min(2, CUKES.collected)
                CUKES.collected = max(0, CUKES.collected - shots_r)
                _pd_fire = getattr(GM._p3, "_player_depth_target", 1.0)
                for _ in range(shots_r):
                    self.p_bullets.append([0.0, lane + random.uniform(-0.08, 0.08), _pd_fire])
                self.float_texts.append(FloatText(
                    "⚡ 暴击！×%d" % shots_r, SW//2-80, 80, life=2.0, size=30, color="#FF4400"))
            elif in_green:
                if DIFF.current == DIFF.EXTREME:
                    # 极限：绿区反击！爽世发射3颗追踪弹
                    CUKES.collected -= 1
                    _p3_ref = GM._p3
                    _px_c = getattr(_p3_ref, 'px', SW//2)
                    _py_c = getattr(_p3_ref, 'py', 360)
                    import math as _qm
                    for _qi in range(3):
                        _ang_c = _qm.radians(90 + (_qi - 1) * 25)
                        _p3_ref.obs.append(Entity(
                            float(SW//2), 0.0, 14, 14,
                            vx=_qm.cos(_ang_c)*220, vy=_qm.sin(_ang_c)*220,
                            tag="bullet"))
                    self.float_texts.append(FloatText(
                        "反击！爽世发射追踪弹！", SW//2-150, 90, life=2.0, size=22, color="#FF4444"))
                elif DIFF.current >= DIFF.HARD:
                    # 困难：绿区只给黄瓜，不扣护盾
                    CUKES.collected += 1
                    self.float_texts.append(FloatText(
                        "绿区！+🥒（需命中红区破盾）", SW//2-140, 90, life=1.8, size=22, color="#AAFFAA"))
                else:
                    # 普通：绿区造1点伤害
                    CUKES.collected -= 1
                    _pd_fire2 = getattr(GM._p3, "_player_depth_target", 1.0)
                    self.p_bullets.append([0.0, lane, _pd_fire2])
                    self.float_texts.append(FloatText(
                        "命中！", SW//2-40, 90, life=1.5, size=28, color="#00DD55"))
            else:
                # 失败：消耗1黄瓜，增加压力
                CUKES.collected -= 1
                PRESSURE.add(8.0)
                self.float_texts.append(FloatText(
                    "哑火… +8压力", SW//2-80, 90, life=1.5, size=22, color="#888888"))

        def shoot(self, lane):
            """向后兼容：直接等同于activate_qte"""
            self.activate_qte(lane)

        def tick(self, dt, p3):
            if not self.active or self.round_clear: return
            self.t += dt
            self._pb_cd = max(0.0, self._pb_cd - dt)

            # QTE 指针来回移动
            if self.qte_active:
                if DIFF.current == DIFF.EXTREME:
                    _qte_spd = 3.5
                elif DIFF.current >= DIFF.HARD:
                    _qte_spd = 2.8
                else:
                    _qte_spd = 1.8
                self.qte_pos += self.qte_dir * _qte_spd * dt
                if self.qte_pos >= 1.0:
                    self.qte_pos = 1.0; self.qte_dir = -1
                elif self.qte_pos <= 0.0:
                    self.qte_pos = 0.0; self.qte_dir = 1

            # ── 出场动画（前2秒：立绘浮现 + 台词）─────────
            if not self._enter_done:
                self._enter_t += dt
                if self._enter_t >= 2.0:
                    self._enter_done = True
                return

            # ── 前奏阶段(0-10s)：丢黄瓜囤弹药 ────────────
            if self.t < 10.0:
                if not hasattr(self, '_intro_cuke_cd'):
                    self._intro_cuke_cd = 0.9
                    self._intro_tip_sent = False   # 延迟发操作提示
                # 操作提示延迟4秒再出现（避免和"这个，不需要了"重叠）
                if not getattr(self, '_intro_tip_sent', False) and self.t >= 4.0:
                    self._intro_tip_sent = True
                    self.float_texts.append(FloatText(
                        "左键点击射击爽世！",
                        SW//2-240, 130, life=5.0, size=22, color="#333333"))
                self._intro_cuke_cd -= dt
                if self._intro_cuke_cd <= 0:
                    # 归一化坐标：(lane + 0.5) / n
                    _n_now = getattr(p3, '_lane_count', P3_LANES)
                    for _ci in range(_n_now):
                        _cx = (_ci + 0.5) / float(_n_now)
                        p3.obs.append(Entity(_cx, 0.0, 1, 1,
                                             tag="p3cuke", is_cucumber=True, layer=-1))
                    self._intro_cuke_cd = 1.2

            # ── 晕厥状态 ───────────────────────────────────
            if self.stunned:
                self.stun_t -= dt
                # 摇摆平滑归零
                p3._wobble_intensity = max(0.0, p3._wobble_intensity - dt * 0.6)
                if self.stun_t <= 0:
                    self.stunned  = False
                    self.shield   = self.MAX_SHIELD
                    # 恢复当前阶段应有的摇摆强度
                    for (s, e, wi, _) in self.PHASES:
                        if s <= self.t < e:
                            p3._wobble_intensity = wi
                            break
                    self.float_texts.append(FloatText(
                        "爽世回过神来！", SW//2-80, 130, life=2.5, size=26, color="#FFFFFF"))
                return

            # ── 时间轴事件 ─────────────────────────────────
            for (s, e, wi, txt) in self.PHASES:
                key = ("phase", s)
                if key not in self._fired and self.t >= s:
                    self._fired.add(key)
                    p3._wobble_intensity = wi
                    if txt:
                        self.float_texts.append(FloatText(
                            txt, SW//2-200, 120, life=4.0, size=28, color="#222222"))

            # ── 75秒：等场上obs清空后触发前后夹击 ────────
            if self.t >= 75.0 and "pincer" not in self._fired:
                # 先停止生成新障碍
                p3.spwn_cd = 9999.0
                if not hasattr(self, '_pincer_pending'): self._pincer_pending = True
                # 等场上障碍物全部自然飞出（obs为空）再正式激活
                if getattr(self, '_pincer_pending', False) and len(p3.obs) == 0:
                    self._fired.add("pincer")
                    self._pincer_pending = False
                    p3._boss_pincer = True
                    # 强制结束未结算的攻击条，防止卡死
                    self.qte_active = False
                    self._pb_cd     = 0.0
                    if hasattr(p3, 'back_obs'): p3.back_obs.clear()
                    p3._back_spwn_cd = 3.0
                    # 夹击阶段前方障碍间隔缩短（0.8~1.5s），恢复正常生成
                    p3.spwn_cd = random.uniform(0.8, 1.5)
                    # 夹击阶段强制扩展为5道
                    p3._lane_count     = 5
                    p3._lane_shrink_t  = 99999.0
                    p3._lane_expand_cd = 99999.0
                    _old_l = int(round(p3.lane))
                    _new_l = _old_l * 2
                    p3.lane     = float(_new_l)
                    p3.target_l = float(_new_l)
                    self.float_texts.append(FloatText(
                        "为什么……要演奏春日影！？",
                        SW//2-250, SH//2-80, life=4.0, size=34, color="#222222"))
                    self.float_texts.append(FloatText(
                        "腹背受敌！", SW//2-60, SH//2, life=2.5, size=26, color="#222222"))

            # 桥段(48/58/68s)：加大障碍频率（选项门已删除）
            for i, gt in enumerate(self.GATE_TIMES):
                key = ("gate", i)
                if key not in self._fired and self.t >= gt:
                    self._fired.add(key)
                    # 桥段小爆发：短暂加速障碍生成
                    p3.spwn_cd = min(p3.spwn_cd, 1.2)

            # 114秒结束
            if self.t >= self.TOTAL_DUR:
                if "clear" not in self._fired:
                    self._fired.add("clear")
                    p3.obs.clear()
                    p3.collapses.clear()
                    p3._wobble_intensity = 0.0
                    self.float_texts.append(FloatText(
                        "春日影……停了", SW//2-100, SH//2-40,
                        life=3.0, size=36, color="#222222"))
                if self.t >= self.TOTAL_DUR + 3.0:
                    # 立绘淡出：通过标记让渲染端做渐隐
                    if not getattr(self, '_clear_fade_started', False):
                        self._clear_fade_started = True
                        self._clear_fade_t = 0.0
                        # 奖励10个黄瓜
                        CUKES.collected += 10
                        self.float_texts.append(FloatText(
                            "🥒 ×10  春日影的代价……",
                            SW//2-180, SH//2-60, life=3.5, size=26, color="#1A7A00"))
                        renpy.music.stop(fadeout=2.0)
                    self._clear_fade_t = getattr(self, '_clear_fade_t', 0.0) + 0.016  # approx dt
                    if self._clear_fade_t >= 2.0:   # 立绘淡出2秒后再切场景
                        self.round_clear = True
                        p3.round_clear   = True
                return

            # ── 玩家子弹移动 + 命中判定 ────────────────────
            for pb in list(self.p_bullets):
                pb[0] += self.BULLET_SPD * dt
                if pb[0] >= 0.98:
                    self.p_bullets.remove(pb)
                    self._on_hit(p3)

            # ── floattext tick ─────────────────────────────
            for ft in self.float_texts: ft.tick(dt)
            self.float_texts = [ft for ft in self.float_texts if ft.alive]

        def _on_hit(self, p3):
            self.shield -= 1
            self.float_texts.append(FloatText(
                "HIT！护盾 %d/%d" % (self.shield, self.MAX_SHIELD),
                SW//2-80, 100, life=1.5, size=24, color="#CC0000"))
            if self.shield <= 0:
                self.stunned  = True
                self.stun_t   = self.STUN_DUR
                p3.obs.clear()

    # ── 伪3D跑酷 ─────────────────────────────────────────────
    class LaneCollapse(python_object):
        """单条跑道崩塌状态"""
        COLLAPSE_DUR = 1.5
        RECOVER_DUR  = 8.0

        def __init__(self, lane_idx):
            self.lane    = lane_idx
            self.t       = 0.0       # 崩塌进度 0→1
            self.alive   = True      # True=崩塌中, False=已完全崩
            self.recover = 0.0       # 恢复倒计时

        def tick(self, dt):
            if self.t < 1.0:
                self.t = min(1.0, self.t + dt / self.COLLAPSE_DUR)
                if self.t >= 1.0:
                    self.alive   = False
                    self.recover = self.RECOVER_DUR
            elif self.recover > 0:
                self.recover = max(0.0, self.recover - dt)

        @property
        def passable(self):
            return self.t < 0.6   # 60%进度前还能跑

        @property
        def done(self):
            return not self.alive and self.recover <= 0.0

    class P3Runner(python_object):
        SWITCH_SPD  = 8.0
        OBS_SPD_Z   = 0.42
        DEPTH_MIN   = 0.40    # 最远（高空）
        DEPTH_MAX   = 1.00    # 最近（地面）
        DEPTH_SPD   = 4.0     # 深度追踪速度
        LAYER_THRESH = 0.62   # 小于此值=高空层，大于=地面层

        def __init__(self):
            self.tutorial_mode = True
            self.phase_dur     = 25.0
            self.reset()

        def reset(self):
            self.lane        = 1.0
            self.target_l    = 1.0
            self.depth       = 1.0
            self.target_depth = 1.0
            self.obs         = []
            self.phase_timer = 0.0
            self.spwn_cd     = 2.5
            self.dead        = False
            self._explode_t  = 0.0   # 爆炸动画计时
            self._invincible_t = 0.0 # 碰撞后无敌帧
            self.round_clear = False
            self.float_texts = []
            # 收集音符计数
            # note_count已删除
            # 崩塌系统已删除（字段保留供兼容）
            self.collapses   = []
            self.lane_alive  = [True, True, True]
            self._col_cd     = 999999.0
            # 黄瓜
            self._cuke_cd    = random.uniform(10.0, 18.0)
            # r2_p3 背景渐白
            self._bg_white   = 0.0
            # 第四面墙干扰
            self.wall4_t     = 0.0
            self._wall4_noise = []
            self._wall4_tears = []
            self._noise_cd   = 0.06
            # ── 消失点摇摆（Boss专属）──────────────────────
            self.vp_offset_x      = 0.0
            self.vp_offset_y      = 0.0
            self._wobble_intensity = 0.0   # 0=关, 1.0=最强
            self._wobble_t        = 0.0
            # 选项门已删除
            # ── Boss战 ──────────────────────────────────────
            self.soyo_boss   = SoyoBoss()   # Round 2 爽世
            self._boss_phase = False  # True=Boss已激活，False=还在自由跑路段
            # ── 教程脚本 ────────────────────────────────────
            self._tut_fired        = set()
            self._tut_script_phase = 0
            self._tut_cuke_cd      = 0.0
            self._tut_cuke_sent    = 0
            # _tut_gate_spawned已删除
            # 莫比乌斯环闪白
            self._wrap_flash = 0.0
            # 编队系统
            self._pending_spawns = []  # [(delay, lane)]等待生成的队列
            # 道宽变化
            self.lane_widths  = [1.0, 1.0, 1.0]    # 三道宽度因子，sum=3.0
            self._lw_target   = [1.0, 1.0, 1.0]
            self._lw_cd       = random.uniform(8.0, 14.0)  # 下次变化倒计时
            # ── 前后夹击系统（爽世Boss 75s后）──────────────
            self._boss_pincer          = False
            self._player_depth_target  = 1.0
            self.back_obs              = []
            self._back_spwn_cd         = 1.5
            self._bot_y                = float(P3_BOT_Y)
            # 3/5道动态扩展
            self._lane_count  = 3       # 当前道数（整数，碰撞/生成用）
            self._lane_count_f = 3.0    # 渲染用浮点，平滑lerp到_lane_count
            self._lane_expand_cd = random.uniform(20.0, 28.0)
            self._lane_shrink_t  = 0.0

            self._tut_q = [
                (2.0,  "伪3D跑道！  全程用鼠标控制睦"),
                (5.0,  "鼠标左右移动换道  躲开飞来的障碍物"),
                (14.0, "🥒 黄瓜出现了！移到对应跑道收集"),
                (30.0, "白色方块 — 必须换道才能躲！"),
            ]

        def move_left(self):
            if self.dead: return
            n = getattr(self, '_lane_count', P3_LANES)
            cur = int(round(self.target_l))
            if cur <= 0:
                self.target_l = float(n - 1)
                self.lane     = float(n - 1)
                self._wrap_flash = 0.35
            else:
                self.target_l = float(cur - 1)

        def move_right(self):
            if self.dead: return
            n = getattr(self, '_lane_count', P3_LANES)
            cur = int(round(self.target_l))
            if cur >= n - 1:
                self.target_l = 0.0
                self.lane     = 0.0
                self._wrap_flash = 0.35
            else:
                self.target_l = float(cur + 1)

        def tick(self, dt):
            if self.dead or self.round_clear: return
            self.phase_timer += dt

            # 无敌帧递减
            self._invincible_t = max(0.0, self._invincible_t - dt)

            # 莫比乌斯闪白递减
            if not hasattr(self, '_wrap_flash'): self._wrap_flash = 0.0
            self._wrap_flash = max(0.0, self._wrap_flash - dt * 2.5)

            # 编队延迟队列
            if not hasattr(self, '_pending_spawns'): self._pending_spawns = []
            _next = []
            for (_pd2, _pl) in self._pending_spawns:
                _pd2 -= dt
                if _pd2 <= 0:
                    # _pl 已是归一化坐标 [0,1]
                    self.obs.append(Entity(_pl, 0.0, 1, 1, tag="p3obs", layer=-1))
                else:
                    _next.append((_pd2, _pl))
            self._pending_spawns = _next

            # 道宽渐变（Lerp，0.6/s）
            if not hasattr(self, 'lane_widths'):
                self.lane_widths = [1.0, 1.0, 1.0]
                self._lw_target  = [1.0, 1.0, 1.0]
                self._lw_cd      = 10.0
            if not self.tutorial_mode:
                self._lw_cd -= dt
                if self._lw_cd <= 0:
                    self._lw_cd = random.uniform(9.0, 16.0)
                    # 随机选一种宽度组合（三道之和始终=3.0）
                    _lw_presets = [
                        [1.0, 1.0, 1.0],   # 均等（常态）
                        [0.65, 1.70, 0.65], # 中道宽，两侧窄（压迫感）
                        [1.70, 0.65, 0.65], # 左宽
                        [0.65, 0.65, 1.70], # 右宽
                        [1.35, 0.95, 0.70], # 左偏宽
                        [0.70, 0.95, 1.35], # 右偏宽
                        [1.0, 1.0, 1.0],    # 回均等（权重高）
                        [1.0, 1.0, 1.0],
                    ]
                    self._lw_target = random.choice(_lw_presets)
                for _li in range(3):
                    self.lane_widths[_li] += (self._lw_target[_li] - self.lane_widths[_li]) * min(1.0, dt * 0.55)

            # ── 3/5道动态扩展 ───────────────────────────────
            if not self.tutorial_mode:
                if not hasattr(self, '_lane_count'):
                    self._lane_count   = 3
                    self._lane_count_f = 3.0
                    self._lane_expand_cd = 20.0
                    self._lane_shrink_t  = 0.0
                if self._lane_shrink_t > 0:
                    self._lane_shrink_t -= dt
                    if self._lane_shrink_t <= 0:
                        # 收缩：玩家lane从[0-4]映射回[0-2]，障碍x不用动（归一化坐标）
                        old_l = int(round(self.lane))
                        new_l = min(2, int(round(old_l * 2.0 / 4.0)))
                        self.target_l = float(new_l)
                        self.lane     = float(new_l)
                        self._lane_count = 3
                        self._lane_expand_cd = random.uniform(18.0, 26.0)
                        self.float_texts.append(FloatText(
                            "道路收缩！", SW//2-60, 140, life=1.5, size=22, color="#AAAAAA"))
                else:
                    self._lane_expand_cd -= dt
                    if self._lane_expand_cd <= 0:
                        # 扩张：玩家lane从[0-2]映射到[0-4]，障碍x不用动
                        old_l = int(round(self.lane))
                        new_l = old_l * 2
                        self.target_l = float(new_l)
                        self.lane     = float(new_l)
                        self._lane_count = 5
                        self._lane_shrink_t = random.uniform(12.0, 18.0)
                        self.float_texts.append(FloatText(
                            "道路扩宽！", SW//2-60, 140, life=1.5, size=22, color="#FFFFFF"))
                # _lane_count_f 平滑 lerp 到 _lane_count（约0.8秒完成）
                _lc_target = float(self._lane_count)
                _lc_f = getattr(self, '_lane_count_f', 3.0)
                if abs(_lc_f - _lc_target) < 0.02:
                    self._lane_count_f = _lc_target
                else:
                    self._lane_count_f = _lc_f + (_lc_target - _lc_f) * min(1.0, dt * 2.8)

            # ── 横向换道（连续平滑）──────────────────────────
            diff = self.target_l - self.lane
            self.lane = self.target_l if abs(diff) < 0.02 else self.lane + diff * self.SWITCH_SPD * dt
            _lc = getattr(self, '_lane_count', P3_LANES)
            self.lane = max(0.0, min(float(_lc - 1), self.lane))

            # ── 深度移动（鼠标Y控制）────────────────────────
            ddiff = self.target_depth - self.depth
            self.depth = self.target_depth if abs(ddiff) < 0.004 else self.depth + ddiff * self.DEPTH_SPD * dt
            self.depth = max(self.DEPTH_MIN, min(self.DEPTH_MAX, self.depth))

            # ── r2_p3 背景渐白（Boss段开始即开始淡白）──────
            if GM.phase == "r2_p3" and getattr(self, "_boss_phase", False):
                # Boss段：进入后2秒内从黑渐变到白
                self._bg_white = min(1.0, self.soyo_boss.t / 2.0) if self.soyo_boss.active else self._bg_white
            else:
                self._bg_white = 0.0

            # ── 消失点摇摆更新 ───────────────────────────────
            if self._wobble_intensity > 0:
                self._wobble_t += dt
                self.vp_offset_x = math.sin(self._wobble_t * 2.3) * self._wobble_intensity * 130
                self.vp_offset_y = math.cos(self._wobble_t * 1.7) * self._wobble_intensity * 45
                # 深度接近地面时摇摆增压
                if self.depth >= 0.85:
                    _wobble_rate = 1.0 if DIFF.current == DIFF.EXTREME else (3.0 if DIFF.current >= DIFF.HARD else 1.5)
                    PRESSURE.add(_wobble_rate * dt * self._wobble_intensity)
            else:
                self.vp_offset_x = self.vp_offset_x * max(0.0, 1.0 - dt * 6.0)
                self.vp_offset_y = self.vp_offset_y * max(0.0, 1.0 - dt * 6.0)

            # ── 教程飘字触发 ─────────────────────────────────
            if self.tutorial_mode:
                for (t, msg) in self._tut_q:
                    if t not in self._tut_fired and self.phase_timer >= t:
                        self._tut_fired.add(t)
                        self.float_texts.append(FloatText(msg, SW//2-160, 160, life=3.5, size=24))
                        if t == 19.0:
                            self._tut_script_phase = 1
                            self.spwn_cd = 999.0
                            CUKES.collected = 0
                            self._tut_cuke_cd   = 2.5
                            self._tut_cuke_sent = 0
                        elif t == 28.0:
                            # 选择门已删除，28秒时做一次短暂清场
                            self.spwn_cd = 3.0
                            self.obs = [o for o in self.obs if o.is_cucumber]

                # ── 脚本阶段处理 ──────────────────────────
                if self._tut_script_phase == 1:
                    self._tut_cuke_cd -= dt
                    if self._tut_cuke_cd <= 0 and self._tut_cuke_sent < 8:
                        lane = self._tut_cuke_sent % P3_LANES
                        norm_c = (lane + 0.5) / float(P3_LANES)
                        self.obs.append(Entity(norm_c, 0.0, 1, 1,
                                               tag="p3cuke", is_cucumber=True))
                        self._tut_cuke_sent += 1
                        self._tut_cuke_cd = 0.8
                    if CUKES.collected >= 8 and self._tut_script_phase == 1:
                        # 崩塌演示已删除，黄瓜收集完后直接恢复正常生成
                        self._tut_script_phase = 0
                        self.spwn_cd = 1.5
                        self.float_texts.append(FloatText("黄瓜全部收集！继续前进", SW//2-100, 160, life=2.0, size=22, color="#FFFFFF"))

            # 跑道崩塌系统已删除

            # ── 黄瓜生成 ─────────────────────────────────────
            self._cuke_cd -= dt
            if self._cuke_cd <= 0 and self.phase_timer > 5.0:
                n_now = getattr(self, '_lane_count', P3_LANES)
                cuke_lane = random.randint(0, n_now-1)
                ent = Entity((cuke_lane + 0.5) / float(n_now), 0.0, 1, 1, tag="p3cuke", is_cucumber=True, layer=-1)
                self.obs.append(ent)
                other_lane = (cuke_lane + random.randint(1, n_now-1)) % n_now
                self.obs.append(Entity((other_lane + 0.5) / float(n_now), 0.0, 1, 1, tag="p3cuke", is_cucumber=True, layer=-1))
                self._cuke_cd = random.uniform(4.5, 7.5) if DIFF.current >= DIFF.HARD else random.uniform(6.0, 10.0)

            # 选项门已删除

            # ── 第四面墙干扰 ─────────────────────────────────
            if GM.phase == "r4_h":
                self.wall4_t += dt
                self._noise_cd -= dt
                if self._noise_cd <= 0:
                    self._noise_cd = 0.08
                    intensity = min(1.0, self.wall4_t / 20.0)
                    n = int(intensity * 14)
                    self._wall4_noise = [(random.randint(0,SW-8), random.randint(0,SH-8),
                                         random.randint(2,8), random.randint(2,8),
                                         random.choice(["#FFFFFF","#AAAAAA","#DDDDDD"])) for _ in range(n)]
                    self._wall4_tears = [random.randint(0, SW) for _ in range(int(intensity * 3))]
            else:
                self.wall4_t = 0.0
                self._wall4_noise = []
                self._wall4_tears = []

            # ── 移动障碍 ─────────────────────────────────────
            _fwd_spd = self.OBS_SPD_Z * DIFF.p3_obs_spd_mult
            if getattr(self, '_boss_pincer', False): _fwd_spd *= 1.3    # 夹击阶段前方障碍加速30%
            for o in self.obs: o.y += _fwd_spd * dt
            self.obs = [o for o in self.obs if o.y <= 1.08]

            # ── 生成障碍 ─────────────────────────────────────
            self.spwn_cd -= dt
            if self.spwn_cd <= 0:
                _pincer_now = getattr(self, '_boss_pincer', False)
                # 夹击时限制场上前方障碍数（防卡顿/连堆）
                if not _pincer_now or len(self.obs) < 7:
                    self._spawn()
                if _pincer_now:
                    self.spwn_cd = random.uniform(0.9, 1.5)
                else:
                    self.spwn_cd = random.uniform(1.4, 2.8)

            for ft in self.float_texts: ft.tick(dt)
            self.float_texts = [ft for ft in self.float_texts if ft.alive]

            # ── 碰撞检测（深度感知版）────────────────────────
            _n_coll = getattr(self, '_lane_count', P3_LANES)
            cur = int(round(self.lane))
            for o in list(self.obs):
                if abs(o.y - self.depth) > 0.14: continue
                # o.x 是归一化坐标 [0,1]，转为当前道数下的lane index
                obs_lane = int(o.x * _n_coll)
                obs_lane = max(0, min(_n_coll - 1, obs_lane))
                if obs_lane != cur: continue
                # 层级系统已删除：所有障碍均有效
                if o.is_cucumber:
                    CUKES.collect_one()
                    # Boss战白背景时飘字改深色
                    _cft_col = "#1A7A00" if getattr(self, "_bg_white", 0.0) > 0.5 else "#FFFFFF"
                    self.float_texts.append(FloatText("🥒 +1", SW//2-20, 160, life=0.7, size=22, color=_cft_col))
                    self.obs.remove(o)
                    continue
                if o.collectible:
                    # note已改为普通障碍，直接忽略（不会生成）
                    self.obs.remove(o)
                    continue
                # 碰撞：加压力+无敌帧，不直接死（不清空黄瓜）
                if self._invincible_t <= 0 and not DEV.god_mode and not DEV.invincible:
                    PRESSURE.add(25.0)
                    self._invincible_t = 1.5
                    self.float_texts.append(FloatText(
                        "！+25 压力", SW//2-30, 180, life=0.8, size=22, color="#FF4444"))

            # 选项门碰撞已删除

            # 跑道崩塌惩罚已删除

            # ── 前后夹击系统 tick ─────────────────────────
            _pincer = getattr(self, '_boss_pincer', False)
            # _bot_y 平滑 lerp：夹击时扩展到屏幕底部
            _bot_target = float(SH) if _pincer else float(P3_BOT_Y)
            _bot_cur    = getattr(self, '_bot_y', float(P3_BOT_Y))
            if abs(_bot_cur - _bot_target) < 0.5:
                self._bot_y = _bot_target
            else:
                self._bot_y = _bot_cur + (_bot_target - _bot_cur) * min(1.0, dt * 1.2)
            # _player_depth_target 平滑切换
            _pd_target = 0.55 if _pincer else 1.0
            _pd_cur    = getattr(self, '_player_depth_target', 1.0)
            if abs(_pd_cur - _pd_target) < 0.005:
                self._player_depth_target = _pd_target
            else:
                self._player_depth_target = _pd_cur + (_pd_target - _pd_cur) * min(1.0, dt * 1.0)

            if _pincer:
                # 后方障碍：从z=1.0向玩家z=0.55逼近（速度约为前方的65%）
                BACK_SPD = self.OBS_SPD_Z * 0.9 * DIFF.p3_obs_spd_mult    # 后方障碍速度
                for o in list(getattr(self, 'back_obs', [])):
                    o.y -= BACK_SPD * dt
                    if o.y < 0.05:        # 飞过消失点
                        self.back_obs.remove(o)
                # 后方障碍碰撞
                _pd_now = self.depth
                _n_bc   = getattr(self, '_lane_count', P3_LANES)
                _cur_bc = int(round(self.lane))
                for o in list(getattr(self, 'back_obs', [])):
                    if abs(o.y - _pd_now) > 0.13: continue
                    obs_l = int(o.x * _n_bc)
                    obs_l = max(0, min(_n_bc-1, obs_l))
                    if obs_l != _cur_bc: continue
                    self.back_obs.remove(o)
                    if self._invincible_t <= 0 and not DEV.god_mode and not DEV.invincible:
                        PRESSURE.add(22.0)
                        self._invincible_t = 1.5
                        self.float_texts.append(FloatText(
                            "！+22 追尾！", SW//2-40, SH//2 - 60, life=0.8, size=22, color="#FF6622"))
                # 后方障碍生成（随机单道，每1.8~2.8s一次）
                if not hasattr(self, '_back_spwn_cd'): self._back_spwn_cd = 1.5
                self._back_spwn_cd -= dt
                if self._back_spwn_cd <= 0:
                    _n_bk = getattr(self, '_lane_count', P3_LANES)
                    if not hasattr(self, 'back_obs'): self.back_obs = []
                    # 每次生成1条，最多4个后方障碍同时存在（防卡顿）
                    if len(getattr(self, 'back_obs', [])) < 4:
                        _bl = random.randint(0, _n_bk - 1)
                        _bnx = (_bl + 0.5) / float(_n_bk)
                        self.back_obs.append(Entity(_bnx, 1.0, 1, 1, tag="p3back", layer=-1))
                    self._back_spwn_cd = random.uniform(1.0, 1.8)

            # ── Boss战：SoyoBoss tick ──────────────────────
            if GM.phase == "r2_p3" and self.soyo_boss.active:
                self.soyo_boss.tick(dt, self)
                # 爽世Boss战不使用崩塌机制（已在GDD中删除）



        # ── 编队定义（lane列表+各delay，保证至少一条安全道）──
        _FORMATIONS = [
            # 单道（高权重，节奏呼吸用）
            ([0],         [0.0],              10),
            ([1],         [0.0],              10),
            ([2],         [0.0],              10),
            # 双封锁：明确指向唯一安全道
            ([0, 1],      [0.0, 0.0],          6),   # →右
            ([1, 2],      [0.0, 0.0],          6),   # →左
            ([0, 2],      [0.0, 0.0],          6),   # →中
            # Z字形：要求连续换道两次
            ([0, 2],      [0.0, 0.55],         5),   # 先躲左再躲右
            ([2, 0],      [0.0, 0.55],         5),   # 先躲右再躲左
            ([0, 1],      [0.0, 0.55],         4),   # L→R连续步
            ([2, 1],      [0.0, 0.55],         4),   # R→L连续步
            # 三道扫荡（有节拍感，但永远留一道空挡）
            ([0, 1, 2],   [0.0, 0.50, 1.0],    3),   # 全扫从左
            ([2, 1, 0],   [0.0, 0.50, 1.0],    3),   # 全扫从右
        ]

        def _pick_formation(self):
            """加权随机选编队，并根据当前phase过滤"""
            pool = []
            for (lanes, delays, wt) in self._FORMATIONS:
                # 教程模式只用单道
                if self.tutorial_mode and len(lanes) > 1: continue
                # 前15秒只用单道
                if self.phase_timer < 15.0 and len(lanes) > 1: continue
                pool.append((lanes, delays, wt))
            if not pool:
                return [random.randint(0, P3_LANES-1)], [0.0]
            total_w = sum(w for _, _, w in pool)
            r = random.random() * total_w
            cum = 0
            for (lanes, delays, wt) in pool:
                cum += wt
                if r <= cum:
                    return lanes, delays
            return pool[-1][0], pool[-1][1]

        def _spawn(self):
            """每次生成一个编队（x存归一化坐标 [0,1]，切换道数时障碍位置自动平滑）"""
            if self.tutorial_mode and self.phase_timer < 5.0: return
            lanes, delays = self._pick_formation()
            n = getattr(self, '_lane_count', P3_LANES)
            for (ln, dl) in zip(lanes, delays):
                mapped = int(round(ln * (n - 1) / max(1, P3_LANES - 1)))
                mapped = max(0, min(n - 1, mapped))
                # 归一化：中心位置 = (mapped + 0.5) / n，范围 [0, 1]
                norm_x = (mapped + 0.5) / float(n)
                if dl <= 0.005:
                    self.obs.append(Entity(norm_x, 0.0, 1, 1, tag="p3obs", layer=-1))
                else:
                    self._pending_spawns.append((dl, norm_x))

    # ── 全局管理器 ───────────────────────────────────────────
    class GameManager(python_object):
        # 各过渡段时长（秒）
        TUT_H_DUR  = 50.0
        TUT_V2_DUR = 38.0
        TUT_P3_DUR = 42.0
        R_H_DUR    = 35.0   # Round2/3 横版过渡段
        R_V2_DUR   = 30.0   # Round2/3 弹幕过渡段

        def __init__(self):
            self.phase = "title"
            self._h    = HRunner()
            self._v2   = V2Runner()
            self._p3   = P3Runner()
            self._ta   = TitleAnim()
            self._tr   = SceneTransition()
            CUKES.reset()
            PRESSURE.reset()
            RHYTHM.reset()
            invert_mode[0] = False
            # DIFF.current 不重置（保留玩家选择的难度）

        def _reset_sub(self, tut=False):
            self._h.reset();  self._h.tutorial_mode  = tut
            self._v2.reset(); self._v2.tutorial_mode = tut
            self._p3.reset(); self._p3.tutorial_mode = tut

        def start_game(self):
            # 已通关教程 → 任何难度都直接从 Round 2 开始（教程只需过一遍）
            _can_skip = (persistent.tutorial_cleared
                         and not DEV.force_tutorial)
            if _can_skip:
                self._reset_sub(tut=False)
                self._h.phase_dur = self.R_H_DUR
                self._go("r2_h")
            else:
                self._reset_sub(tut=True)
                self._h.phase_dur  = self.TUT_H_DUR
                self._v2.phase_dur = self.TUT_V2_DUR
                self._p3.phase_dur = self.TUT_P3_DUR
                self._go("tut_h")

        def _go(self, p):
            self.phase = p; _reset_ts()
            # ── BGM 自动切换 ──────────────────────────────────
            _BGM = {
                "title":       "audio/ショパン「雨だれ」.ogg",
                "title_anim":  "audio/ショパン「雨だれ」.ogg",
                "tut_h":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r2_h":   "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r3_h":   "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r4_h":   "audio/ショパン「雨だれ」.ogg",
                "tut_v2": "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r2_v2":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r3_v2":  "audio/saki.ogg",
                "tut_p3": "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                "r2_p3":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",  # boss激活时才换春日影
                "r3_p3":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
            }
            if p in ("ending",):
                renpy.music.play("audio/His Theme.ogg", loop=True, fadein=2.0)
                store._current_bgm = "audio/His Theme.ogg"
            elif p in _BGM:
                _target = _BGM[p]
                if getattr(store, '_current_bgm', None) != _target:
                    renpy.music.play(_target, loop=True, fadein=1.5)
                    store._current_bgm = _target

        def _go_trans(self, kind, next_phase, setup_fn=None):
            """启动过渡动画，完成后跳到 next_phase"""
            self._tr.start(kind, next_phase, setup_fn)
            self.phase = "trans"
            _reset_ts()

        def _h_dead_reset(self, tut):
            self._h.reset(); self._h.tutorial_mode = tut; _reset_ts()
            PRESSURE.reset()

        def _v2_dead_reset(self, tut):
            self._v2.reset(); self._v2.tutorial_mode = tut; _reset_ts()
            PRESSURE.reset()

        def _p3_dead_reset(self, tut):
            self._p3.reset(); self._p3.tutorial_mode = tut; _reset_ts()
            PRESSURE.reset()

        def retry_current(self):
            p = self.phase
            # 死亡音乐停止，清除所有BGM状态
            renpy.music.stop(fadeout=0.3)
            store._current_bgm     = None
            store._death_bgm_pos   = 0.0
            store._death_bgm_track = None
            if p == "tut_h":
                self._h_dead_reset(tut=True)
                self._go("tut_h")
            elif p == "tut_v2":
                self._v2_dead_reset(tut=True)
                self._go("tut_v2")
            elif p == "tut_p3":
                self._p3_dead_reset(tut=True)
                self._go("tut_p3")
            elif p in ("r2_h", "r3_h"):
                self._h_dead_reset(tut=False)
                self._go(p)
            elif p == "r4_h":
                self._h.reset(); self._h.tutorial_mode = False
                self._h.phase_dur = self.R_H_DUR
                self._v2.reset(); self._p3.reset()
                PRESSURE.reset()
                self._go("r2_h")
                _reset_ts()
            elif p in ("r2_v2", "r2_p3", "r3_v2", "r3_p3"):
                self._h.reset(); self._h.tutorial_mode = False
                self._h.phase_dur = self.R_H_DUR
                self._v2.reset(); self._p3.reset()
                PRESSURE.reset()
                self._go("r2_h")
                _reset_ts()

        def tick(self):
            dt = _dt()
            if dt == 0.0: return
            p = self.phase

            # ── 全局系统 tick ─────────────────────────────────
            # 按场景 × 难度 调整压力衰减速度
            if DIFF.current == DIFF.EXTREME:
                PRESSURE.decay_rate = 0.0           # 极限：永不衰减
            elif GM.phase == "r2_p3":
                PRESSURE.decay_rate = 2.0           # 爽世Boss战：衰减（2.0/s）
            elif GM.phase in ("tut_v2", "r2_v2", "r3_v2"):
                PRESSURE.decay_rate = 0.8 * (DIFF.pressure_decay / 2.0)
            elif GM.phase in ("tut_p3", "r3_p3"):
                PRESSURE.decay_rate = 1.5 * (DIFF.pressure_decay / 2.0)
            else:
                PRESSURE.decay_rate = DIFF.pressure_decay
            PRESSURE.tick(dt)
            DEV.tick(dt)
            # 爆炸动画计时递减（getattr兜底，防旧存档对象缺属性）
            for _rr in (self._h, self._v2, self._p3):
                if not hasattr(_rr, '_explode_t'):
                    _rr._explode_t = 0.0
                if not hasattr(_rr, '_invincible_t'):
                    _rr._invincible_t = 0.0
                if _rr._explode_t > 0:
                    _rr._explode_t = max(0.0, _rr._explode_t - dt)

            # ── 压力满100 → 爆炸死亡 ─────────────────────────
            def _on_death():
                """死亡时：保存BGM位置并切死亡音乐"""
                _pos = renpy.music.get_pos() or 0.0
                store._death_bgm_pos = _pos
                store._death_bgm_track = getattr(store, '_current_bgm', None)
                renpy.music.play("audio/death.ogg", loop=False, fadein=0.0)
                store._current_bgm = "audio/death.ogg"

            def _check_pressure_overflow():
                if PRESSURE.value < 99.5: return
                if DEV.no_pressure or DEV.god_mode or DEV.invincible: return
                if p in ("tut_h","r2_h","r3_h","r4_h") and not self._h.dead:
                    self._h.dead = True
                    self._h._explode_t = 0.7
                    CUKES.collected = 0
                    _on_death()
                elif p in ("tut_v2","r2_v2","r3_v2") and not self._v2.dead:
                    self._v2.dead = True
                    self._v2._explode_t = 0.7
                    CUKES.collected = 0
                    _on_death()
                elif p in ("tut_p3","r2_p3","r3_p3") and not self._p3.dead:
                    self._p3.dead = True
                    self._p3._explode_t = 0.7
                    CUKES.collected = 0
                    _on_death()
            _check_pressure_overflow()

            # ── 复活检测（任意场景死亡后按F消耗黄瓜复活）────
            import pygame as _pg2
            _fkey = _pg2.key.get_pressed()[_pg2.K_f]
            if _fkey:
                def _resume_bgm():
                    _track = getattr(store, '_death_bgm_track', None)
                    # 备用：根据当前场景找对应BGM
                    _PHASE_BGM = {
                        "tut_h":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r2_h":   "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r3_h":   "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r4_h":   "audio/ショパン「雨だれ」.ogg",
                        "tut_v2": "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r2_v2":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r3_v2":  "audio/saki.ogg",
                        "tut_p3": "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                        "r2_p3":  "audio/shuangshi.ogg",
                        "r3_p3":  "audio/可哀想なお人形 (Toy Piano Ver.).ogg",
                    }
                    if not _track or _track == "audio/death.ogg":
                        _track = _PHASE_BGM.get(p, "audio/可哀想なお人形 (Toy Piano Ver.).ogg")
                    # 墨缇斯Boss战中复活用Heartache
                    if p == "r4_h" and getattr(self._h, 'mortis_active', False):
                        _track = "audio/Heartache.ogg"
                    renpy.music.play(_track, loop=True, fadein=0.5)
                    store._current_bgm    = _track
                    store._death_bgm_pos  = 0.0
                    store._death_bgm_track = None
                if self._h.dead and CUKES.use_revive():
                    self._h.dead = False
                    self._h._explode_t = 0.0
                    if hasattr(self._h, 'invincible_t'): self._h.invincible_t = 2.5
                    PRESSURE.reset()
                    # 墨缇斯阶段二：复活位置移到进度条右侧安全区
                    if (getattr(self._h, 'mortis_active', False)
                            and getattr(self._h, 'mortis_phase', 0) == 2):
                        _prog = getattr(self._h, '_progress_x', -60.0)
                        _safe_x = max(float(_prog + 120), float(SW * 0.75))
                        self._h.px  = min(_safe_x, float(SW - 80))
                        self._h.pvx = 0.0
                    _resume_bgm()
                elif self._v2.dead and CUKES.use_revive():
                    self._v2.dead = False
                    self._v2._explode_t = 0.0
                    self._v2.invincible = 2.5
                    PRESSURE.reset()
                    _resume_bgm()
                elif self._p3.dead and CUKES.use_revive():
                    self._p3.dead = False
                    self._p3._explode_t = 0.0
                    if hasattr(self._p3, '_invincible_t'): self._p3._invincible_t = 2.0
                    PRESSURE.reset()
                    _resume_bgm()

            # ── 场景过渡动画 ─────────────────────────────────
            if p == "trans":
                self._tr.tick(dt)
                if self._tr.done:
                    self._go(self._tr.next_ph)
                return

            # ── 主界面进场动画 ────────────────────────────────
            elif p == "title_anim":
                self._ta.tick(dt)
                if self._ta.done and self._ta.fade_out >= 1.0:
                    self.start_game()

            # ══════════════════════════════════════════════════
            #  Round 1  教程：横2D → 竖2D → 伪3D
            # ══════════════════════════════════════════════════
            elif p == "tut_h":
                self._h.tick(dt)
                _check_pressure_overflow()   # 捕捉本帧碰撞推满压力
                if self._h.dead: return  # 停止tick，等弹窗
                elif self._h.phase_timer >= self.TUT_H_DUR:
                    # 等屏幕上的障碍物全部跑过去再切场景，避免突兀
                    _h_safe = all(e.is_cucumber for e in self._h.obs)
                    if _h_safe:
                        def _s():
                            self._v2.reset(); self._v2.tutorial_mode = True
                            self._v2.phase_dur = self.TUT_V2_DUR
                        self._go_trans("h_v2", "tut_v2", _s)
                    else:
                        # 停止再生成新障碍，等现有的自然离场
                        self._h.spwn_cd = max(self._h.spwn_cd, 4.0)

            elif p == "tut_v2":
                self._v2.tick(dt)
                _check_pressure_overflow()
                if self._v2.dead: return  # 停止tick，等弹窗
                elif self._v2.phase_timer >= self.TUT_V2_DUR:
                    # 停止发新弹幕、强制结束大招残留、等屏幕清空
                    self._v2.wave_timer   = -99.0
                    self._v2.bomb_active  = False  # 兜底：大招不阻塞过渡
                    _v2_safe = (len(self._v2.bullets) == 0
                                and not self._v2.cukes)
                    # 超时兜底：满进度条后8秒还没清空，强制清场过渡
                    _overtime = self._v2.phase_timer >= self.TUT_V2_DUR + 8.0
                    if _v2_safe or _overtime:
                        if _overtime:
                            self._v2.bullets.clear()
                            self._v2.cukes.clear()
                        if not self._v2._trans_notified:
                            self._v2._trans_notified = True
                            self._v2.float_texts.clear()
                            self._v2.float_texts.append(FloatText(
                                "——进入第三场景——", V2_AREA_W//2-80, SH//2-20,
                                life=0.8, size=28, color="#FFFFFF"))
                        def _s():
                            self._p3.reset(); self._p3.tutorial_mode = True
                            self._p3.phase_dur = self.TUT_P3_DUR
                        self._go_trans("v2_p3", "tut_p3", _s)

            elif p == "tut_p3":
                self._p3.tick(dt)
                _check_pressure_overflow()
                if self._p3.dead: return  # 停止tick，等弹窗
                elif self._p3.phase_timer >= self.TUT_P3_DUR:
                    # 教程结束：先显示完成提示，等1秒再过渡
                    if "tut_done_msg" not in self._p3._tut_fired:
                        self._p3._tut_fired.add("tut_done_msg")
                        self._p3.float_texts.append(FloatText(
                            "好的，你已经学会这个游戏的所有操作了，是时候开始正式游戏啦",
                            SW//2 - 260, SH//2 - 30, life=3.5, size=24, color="#FFFFFF"))
                    if self._p3.phase_timer >= self.TUT_P3_DUR + 3.0:
                        if DIFF.current in (DIFF.EASY, DIFF.NORMAL):
                            persistent.tutorial_cleared = True
                            _save_persistent()
                        def _s():
                            self._h.reset(); self._h.tutorial_mode = False
                            self._h.phase_dur = self.R_H_DUR
                        self._go_trans("p3_h", "r2_h", _s)

            # ══════════════════════════════════════════════════
            #  Round 2：横2D → 竖2D → 伪3D + Boss爽世
            # ══════════════════════════════════════════════════
            elif p == "r2_h":
                self._h.tick(dt)
                _check_pressure_overflow()
                if self._h.dead: return  # 停止tick，等弹窗
                elif self._h.phase_timer >= self.R_H_DUR:
                    _h_safe = all(e.is_cucumber for e in self._h.obs)
                    _overtime = self._h.phase_timer >= self.R_H_DUR + 6.0
                    if _h_safe or _overtime:
                        if not _h_safe: self._h.obs.clear()
                        def _s():
                            self._v2.reset(); self._v2.tutorial_mode = False
                            self._v2.phase_dur = self.R_V2_DUR
                        self._go_trans("h_v2", "r2_v2", _s)
                    else:
                        self._h.spwn_cd = max(self._h.spwn_cd, 4.0)

            elif p == "r2_v2":
                self._v2.tick(dt)
                _check_pressure_overflow()
                if self._v2.dead: return  # 停止tick，等弹窗
                elif self._v2.phase_timer >= self.R_V2_DUR:
                    # 停止发弹，等场上弹幕全部离屏
                    self._v2.wave_timer  = -99.0
                    self._v2.bomb_active = False
                    _v2_safe   = len(self._v2.bullets) == 0 and not self._v2.cukes
                    _overtime2 = self._v2.phase_timer >= self.R_V2_DUR + 8.0
                    if _v2_safe or _overtime2:
                        if _overtime2:
                            self._v2.bullets.clear(); self._v2.cukes.clear()
                        def _s():
                            self._p3.reset(); self._p3.tutorial_mode = False
                        self._go_trans("v2_p3", "r2_p3", _s)

            elif p == "r2_p3":
                # r2_p3 分两段：
                #   前段（_boss_phase=False）：自由跑TUT_P3_DUR秒，让玩家熟悉操作
                #   后段（_boss_phase=True）：SoyoBoss战
                if not getattr(self._p3, '_boss_phase', False):
                    # ── 前段：普通伪3D自由跑 ──────────────────
                    self._p3.tick(dt)
                    _check_pressure_overflow()
                    if self._p3.dead: return
                    elif self._p3.phase_timer >= self.TUT_P3_DUR:
                        # 等障碍物全部离场，然后激活Boss
                        _p3_safe   = all(e.is_cucumber for e in self._p3.obs)
                        _p3_overt  = self._p3.phase_timer >= self.TUT_P3_DUR + 6.0
                        if _p3_safe or _p3_overt:
                            # 切换到Boss段
                            self._p3._boss_phase = True
                            self._p3.phase_timer  = 0.0   # 重置计时给Boss用
                            self._p3.soyo_boss.start()
                            self._p3.spwn_cd      = 10.5
                            # gate已删除
                            self._p3._col_cd      = 999999.0
                            self._p3.obs          = [o for o in self._p3.obs if o.is_cucumber]
                            self._p3.float_texts.clear()
                            # 播放爽世Boss战音乐
                            renpy.music.play("audio/shuangshi.ogg", loop=True, fadein=1.0)
                            store._current_bgm = "audio/shuangshi.ogg"
                        else:
                            self._p3.spwn_cd = max(self._p3.spwn_cd, 4.0)
                else:
                    # ── 后段：Boss爽世战 ─────────────────────
                    self._p3.tick(dt)
                    _check_pressure_overflow()
                    if self._p3.dead: return
                    elif self._p3.soyo_boss.round_clear or self._p3.round_clear:
                        self._p3.round_clear = True
                        def _s():
                            self._h.reset(); self._h.tutorial_mode = False
                            self._h.phase_dur = self.R_H_DUR
                        self._go_trans("p3_h", "r3_h", _s)

            # ══════════════════════════════════════════════════
            #  Round 3：横2D → 竖2D + Boss祥子 → 伪3D
            # ══════════════════════════════════════════════════
            elif p == "r3_h":
                self._h.tick(dt)
                _check_pressure_overflow()
                if self._h.dead: return  # 停止tick，等弹窗
                elif self._h.phase_timer >= self.R_H_DUR:
                    _h_safe = all(e.is_cucumber for e in self._h.obs)
                    _overtime = self._h.phase_timer >= self.R_H_DUR + 6.0
                    if _h_safe or _overtime:
                        if not _h_safe: self._h.obs.clear()
                        def _s():
                            self._v2.reset(); self._v2.tutorial_mode = False
                        self._go_trans("h_v2", "r3_v2", _s)
                    else:
                        self._h.spwn_cd = max(self._h.spwn_cd, 4.0)

            elif p == "r3_v2":
                # 竖2D + Boss祥子（round_clear 由 Boss 击败触发）
                # 首次进入：激活SakikoBoss
                if not self._v2.sakiko_boss.active:
                    self._v2.sakiko_boss.start()
                    self._v2.wave_timer = -99.0   # 暂停普通弹幕，由Boss控制
                self._v2.tick(dt)
                _check_pressure_overflow()
                if self._v2.dead: return  # 停止tick，等弹窗
                elif self._v2.round_clear:
                    self._v2.wave_timer  = -99.0
                    self._v2.bomb_active = False
                    # Boss通关后：强制清场子弹（可能有乱码弹残留）
                    self._v2.bullets.clear()
                    self._v2.cukes.clear()
                    def _s():
                        self._p3.reset(); self._p3.tutorial_mode = False
                    self._go_trans("v2_p3", "r3_p3", _s)

            elif p == "r3_p3":
                self._p3.tick(dt)
                _check_pressure_overflow()
                if self._p3.dead: return  # 停止tick，等弹窗
                elif self._p3.phase_timer >= self.TUT_P3_DUR:
                    def _s():
                        self._h.reset(); self._h.tutorial_mode = False
                    self._go_trans("p3_h", "r4_h", _s)

            # ══════════════════════════════════════════════════
            #  Round 4：横2D + Boss墨缇斯
            # ══════════════════════════════════════════════════
            elif p == "r4_h":
                self._h.tick(dt)
                _check_pressure_overflow()
                if self._h.dead: return

                # ── 假结局演出阶段 ──────────────────────────
                if not self._h.fake_ending_t:
                    # 刚进入r4_h：清空障碍物，开始假结局
                    self._h.obs.clear()
                    self._h.spwn_cd      = 9999.0
                    self._h.fake_ending_t = 0.001
                    self._h.desktop_ready = False
                    self._h._dsk_shot_started = False   # 防重复截图

                self._h.fake_ending_t += dt

                # 1.5s 后画面已全黑：主线程最小化 + 后台用本地mss截图
                if (self._h.fake_ending_t >= 1.5
                        and not self._h._dsk_shot_started):
                    self._h._dsk_shot_started = True
                    # iconify必须在主线程（SDL限制）
                    try:
                        import pygame_sdl2 as _pg_icon
                        _pg_icon.display.iconify()
                    except:
                        pass
                    import threading, os as _os_ss2, sys as _sys_ss
                    _dsk_out2 = _os_ss2.path.join(config.gamedir, "desktop_cache.png")
                    # 把本地 python-packages 目录加入搜索路径
                    _pkg_dir = _os_ss2.path.join(config.basedir, "python-packages")
                    if _pkg_dir not in _sys_ss.path:
                        _sys_ss.path.insert(0, _pkg_dir)
                    def _do_shot(_out=_dsk_out2):
                        try:
                            import time as _t2; _t2.sleep(0.8)   # 等最小化动画完成
                            from mss import mss as _mss2
                            with _mss2() as _sc:
                                _sc.shot(mon=1, output=_out)
                            self._h.desktop_ready = True
                        except:
                            # mss失败则尝试PIL ImageGrab兜底
                            try:
                                from PIL import ImageGrab as _IG2
                                _IG2.grab().save(_out)
                                self._h.desktop_ready = True
                            except:
                                self._h.desktop_ready = False
                    threading.Thread(target=_do_shot, daemon=True).start()

                # 扑脸前逐渐淡出音乐（fake_ending_t >= 9.5 时开始3s淡出）
                if (self._h.fake_ending_t >= 9.5
                        and not getattr(self._h, '_music_fadeout_done', False)):
                    self._h._music_fadeout_done = True
                    renpy.music.stop(fadeout=2.5)
                    store._current_bgm = None

                # 撕裂演出后进入Boss战
                if self._h.mortis_burst_t > 0:
                    self._h.mortis_burst_t += dt
                    if self._h.mortis_burst_t >= 3.0 and not self._h.mortis_active:
                        self._h.mortis_active = True
                        self._h.px_free       = True
                        self._h.mortis_phase  = 1
                        self._h.spd           = 160.0
                        self._h.obs.clear()
                        renpy.music.play("audio/Heartache.ogg", loop=True, fadein=0.5)
                        store._current_bgm = "audio/Heartache.ogg"

                if self._h.mortis_active:
                    _mp = self._h.mortis_phase
                    self._h.mortis_phase_t += dt
                    # 动态难度倍率（血越少越快）
                    _hp_ratio  = max(0.0, self._h.mortis_hp / float(getattr(self._h, '_mortis_hp_max', 9)))
                    if DIFF.current >= DIFF.HARD:
                        _diff_mult = 1.5 + (1.0 - _hp_ratio) * 0.7   # 1.5 → 2.2
                    else:
                        _diff_mult = 1.0 + (1.0 - _hp_ratio) * 0.6   # 1.0 → 1.6

                    # ── 通用：弹幕发射（全三阶段有效）─────────────
                    self._h._mbullet_cd -= dt
                    if self._h._mbullet_cd <= 0:
                        _px_now = float(int(getattr(self._h, 'px', H_PX)))
                        _py_now = float(self._h.py + H_PH_N // 2)
                        _bspd_base = 300.0 if DIFF.current == DIFF.EXTREME else 160.0
                        _bspd = (_bspd_base + (1.0 - _hp_ratio) * 80.0) * (1.3 if DIFF.current >= DIFF.HARD else 1.0)
                        if _mp == 1:
                            import math as _bm
                            _src_x = float(SW // 2); _src_y = 50.0
                            _aimed = _bm.atan2(_py_now - _src_y, _px_now - _src_x)
                            if DIFF.current >= DIFF.HARD:
                                # 困难：追踪5发 + 散射9发 = 14发
                                for _ao in (-30, -15, 0, 15, 30):
                                    _a = _aimed + _ao * _bm.pi / 180.0
                                    self._h._mortis_bullets.append(
                                        [_src_x, _src_y, _bm.cos(_a)*_bspd, _bm.sin(_a)*_bspd])
                                for _ao2 in (-60,-40,-20,0,20,40,60,80,-80):
                                    _a2 = _bm.pi/2 + _ao2 * _bm.pi / 180.0
                                    self._h._mortis_bullets.append(
                                        [_src_x, _src_y, _bm.cos(_a2)*_bspd*0.9, _bm.sin(_a2)*_bspd*0.9])
                                self._h._mbullet_cd = 1.5 / _diff_mult
                            else:
                                # 普通：追踪3发 + 散射5发 = 8发
                                for _ao in (-20, 0, 20):
                                    _a = _aimed + _ao * _bm.pi / 180.0
                                    self._h._mortis_bullets.append(
                                        [_src_x, _src_y, _bm.cos(_a)*_bspd, _bm.sin(_a)*_bspd])
                                for _ao2 in (-45, -22, 0, 22, 45):
                                    _a2 = _bm.pi/2 + _ao2 * _bm.pi / 180.0
                                    self._h._mortis_bullets.append(
                                        [_src_x, _src_y, _bm.cos(_a2)*_bspd*0.85, _bm.sin(_a2)*_bspd*0.85])
                                self._h._mbullet_cd = 2.8 / _diff_mult
                        elif _mp == 2:
                            # 弹扇形：普通5发，困难6发，极限7发
                            import math as _bm2
                            _src_x = float(SW // 2); _src_y = 55.0
                            if DIFF.current == DIFF.EXTREME:
                                _p2_offsets = (-48, -24, -8, 8, 24, 48, 0)
                            elif DIFF.current >= DIFF.HARD:
                                _p2_offsets = (-45, -22, -5, 5, 22, 45)
                            else:
                                _p2_offsets = (-40, -20, 0, 20, 40)
                            for _ang_off in _p2_offsets:
                                _ang2 = _bm2.atan2(_py_now - _src_y, _px_now - _src_x)
                                _ang2 += _ang_off * _bm2.pi / 180.0
                                self._h._mortis_bullets.append(
                                    [_src_x, _src_y, _bm2.cos(_ang2)*_bspd, _bm2.sin(_ang2)*_bspd])
                            self._h._mbullet_cd = (1.5 if DIFF.current >= DIFF.HARD else 2.5) / _diff_mult
                        elif _mp == 3:
                            # 每个存活的字各发一颗朝向玩家
                            import math as _bm3
                            for _bc_s in self._h._boss_chars:
                                if _bc_s["hp"] <= 0: continue
                                _bx_s = _bc_s["x"] + 40; _by_s = _bc_s["y"] + 40
                                _ang3 = _bm3.atan2(_py_now - _by_s, _px_now - _bx_s)
                                self._h._mortis_bullets.append(
                                    [_bx_s, _by_s, _bm3.cos(_ang3)*_bspd, _bm3.sin(_ang3)*_bspd])
                            self._h._mbullet_cd = 2.8 / _diff_mult

                    # 子弹推进
                    for _bl in self._h._mortis_bullets:
                        _bl[0] += _bl[2] * dt
                        _bl[1] += _bl[3] * dt
                    self._h._mortis_bullets = [b for b in self._h._mortis_bullets
                                                if -20 < b[0] < SW+20 and b[1] < SH+20]
                    # 子弹碰撞：击中玩家 → 压力+12
                    _hpx_b = int(getattr(self._h, 'px', H_PX))
                    _hpy_b = int(self._h.py)
                    _hhb   = H_PH_D if self._h.ducking else H_PH_N
                    _hit_w = max(6, int(H_PW * 0.22))  # 判定框缩至22%
                    _hit_h = max(6, int(_hhb  * 0.42))
                    _hit_ox = (_hit_w) // 2            # 中心对齐偏移
                    for _bl2 in list(self._h._mortis_bullets):
                        if (abs(_bl2[0] - (_hpx_b + H_PW//2)) < _hit_w and
                                (_hpy_b + int(_hhb*0.2)) < _bl2[1] < (_hpy_b + int(_hhb*0.2) + _hit_h)):
                            if self._h.invincible_t <= 0:
                                PRESSURE.add(DIFF.bullet_pressure)
                                self._h.invincible_t = DIFF.invincible_dur
                                self._h.float_texts.append(FloatText(
                                    "！", _hpx_b + 20, _hpy_b - 10,
                                    life=0.5, size=20, color="#FF0000", outline=True))
                            try: self._h._mortis_bullets.remove(_bl2)
                            except: pass

                    # ── 阶段一：弹幕战（存活30秒） ─────────────
                    if _mp == 1:
                        if not self._h._p1_tip_shown:
                            self._h._p1_tip_shown = True
                            self._h.float_texts.append(FloatText(
                                "A / D 键  ←  左右移动  →", SW//2 - 130, SH//2 - 40,
                                life=9.0, size=20, color="#FFFF44", vy=0.0, outline=True))
                        if self._h.mortis_phase_t >= 30.0:
                            self._h.mortis_phase   = 2
                            self._h.mortis_phase_t = 0.0
                            self._h.obs.clear()
                            self._h._progress_x    = -60.0
                            self._h._no_resp_cd    = 6.0
                            self._h._mbullet_cd    = 1.5
                            # 阶段二激活假鼠标：追踪延迟更大、更有压迫感
                            self._h._fake_cur_on = True
                            self._h._fake_cur_x  = float(SW // 2)
                            self._h._fake_cur_y  = float(SH // 2)
                            self._h.float_texts.append(FloatText(
                                "⚠ 阶段二  —  进程阻断", SW//2 - 120, SH//2 - 30,
                                life=3.0, size=22, color="#FF4400", outline=True))
                            self._h.float_texts.append(FloatText(
                                "假光标出现了！  别让它追上你！", SW//2 - 160, SH//2 + 10,
                                life=3.5, size=18, color="#FF8800", outline=True))

                    # ── 阶段二：未响应 + 进度条追击（撑40秒） ─────
                    elif _mp == 2:
                        _prog_spd = 50.0 if DIFF.current == DIFF.EXTREME else (42.0 if DIFF.current >= DIFF.HARD else self._h._progress_spd)
                        self._h._progress_x += _prog_spd * _diff_mult * dt
                        self._h._no_resp_cd -= dt
                        _resp_interval_lo = 4.0 if DIFF.current >= DIFF.HARD else 6.0
                        _resp_interval_hi = 6.0 if DIFF.current >= DIFF.HARD else 10.0
                        _resp_dur = 3.5 if DIFF.current >= DIFF.HARD else 3.0
                        if self._h._no_resp_cd <= 0 and self._h._no_resp_t <= 0:
                            self._h._no_resp_t  = _resp_dur
                            self._h._no_resp_cd = random.uniform(_resp_interval_lo, _resp_interval_hi) / _diff_mult
                        if self._h._no_resp_t > 0:
                            self._h._no_resp_t -= dt
                        # 弹片墙（空隙只剩1个）
                        self._h._frag_wall_cd -= dt
                        if self._h._frag_wall_cd <= 0:
                            self._h._frag_wall_cd = max(2.5, 5.0 / _diff_mult)
                            _SLOT_W2 = SW // 4
                            _gap_slot2 = random.randint(0, 3)
                            _wall_type2 = random.choice(["jump", "duck", "mixed"])
                            for _si2 in range(4):
                                if _si2 == _gap_slot2: continue
                                if _wall_type2 == "jump":
                                    _fw3 = _SLOT_W2 - 14; _fh3 = 55
                                    _fy3 = float(H_GY - _fh3)
                                elif _wall_type2 == "duck":
                                    _fw3 = _SLOT_W2 - 14; _fh3 = H_GY - 42
                                    _fy3 = 0.0
                                else:
                                    if _si2 % 2 == 0:
                                        _fw3 = _SLOT_W2 - 14; _fh3 = 55
                                        _fy3 = float(H_GY - _fh3)
                                    else:
                                        _fw3 = _SLOT_W2 - 14; _fh3 = H_GY - 42
                                        _fy3 = 0.0
                                _fe3 = Entity(float(SW + 30 + _si2 * _SLOT_W2), _fy3,
                                              _fw3, _fh3, vx=-self._h.spd * 0.9, vy=0.0,
                                              tag="mortis_frag")
                                _fe3.crop_x = random.randint(0, max(1, SW - _fw3))
                                _fe3.crop_y = random.randint(0, max(1, 400))
                                self._h.obs.append(_fe3)
                        self._h.obs = [o for o in self._h.obs if o.x > -200]
                        # 进度条上限：普通50%，困难60%，极限70%
                        _prog_cap = int(SW * (0.70 if DIFF.current == DIFF.EXTREME else (0.60 if DIFF.current >= DIFF.HARD else 0.50)))
                        if self._h._progress_x > _prog_cap:
                            self._h._progress_x = float(_prog_cap)
                        if self._h._progress_x >= getattr(self._h, 'px', H_PX) - 20:
                            self._h.dead = True
                        if self._h.mortis_phase_t >= 40.0:
                            self._h.mortis_phase   = 3
                            self._h.mortis_phase_t = 0.0
                            self._h.obs.clear()
                            self._h._progress_x    = -999.0
                            self._h._mbullet_cd    = 1.0
                            self._h._fake_cur_on   = False   # 阶段三关闭假鼠标，让玩家专心瞄准
                            self._h.float_texts.append(FloatText(
                                "⚠ 阶段三  —  愤怒的黄瓜", SW//2 - 130, SH//2 - 30,
                                life=3.0, size=22, color="#FF4400"))

                    # ── 阶段三：弹弓黄瓜 ──────────────────────────
                    elif _mp == 3:
                        import pygame as _pg3
                        _mb3 = _pg3.mouse.get_pressed()
                        _mx3, _my3 = renpy.get_mouse_pos()
                        _bt_dt = dt * 0.2 if self._h._sling_held else dt

                        # 按住左键开始拉弓
                        if _mb3[0] and not self._h._sling_held:
                            self._h._sling_held = True
                            self._h._sling_ox   = float(int(getattr(self._h,'px',H_PX)))
                            self._h._sling_oy   = float(self._h.py + H_PH_N * 0.4)
                        self._h._sling_mx = float(_mx3)
                        self._h._sling_my = float(_my3)
                        # 松开左键发射
                        if not _mb3[0] and self._h._sling_held:
                            self._h._sling_held = False
                            _dx = self._h._sling_ox - _mx3
                            _dy = self._h._sling_oy - _my3
                            import math as _sm
                            _dist_raw = _sm.hypot(_dx + 0.001, _dy + 0.001)
                            _pull = min(_dist_raw, 280.0)   # 最大拉力280px
                            if _pull > 12.0:
                                # 单位向量 × 速度（速度随拉力线性增长）
                                _spd_v = 380.0 + _pull * 1.5
                                _vx_f  = (_dx / _dist_raw) * _spd_v
                                _vy_f  = (_dy / _dist_raw) * _spd_v
                                self._h._cukes_flying.append(
                                    [self._h._sling_ox, self._h._sling_oy, _vx_f, _vy_f])

                        # 推进飞行黄瓜
                        _GRAV_C3 = 480.0
                        for _ck in self._h._cukes_flying:
                            _ck[0] += _ck[2] * _bt_dt
                            _ck[1] += _ck[3] * _bt_dt
                            _ck[3] += _GRAV_C3 * _bt_dt
                        self._h._cukes_flying = [c for c in self._h._cukes_flying
                                                  if -20 < c[0] < SW+20 and c[1] < SH+20]

                        # Boss三字飘动（速度随难度提升）
                        for _bc in self._h._boss_chars:
                            if _bc["hp"] <= 0:
                                if _bc["dead_t"] >= 0: _bc["dead_t"] += dt
                                continue
                            if _bc["hit_t"] > 0: _bc["hit_t"] -= dt
                            _spd_m = _diff_mult * 1.1
                            _bc["sine_t"] = _bc.get("sine_t", 0.0) + _bt_dt
                            _st = _bc["sine_t"]
                            if DIFF.current == DIFF.EXTREME:
                                # 极限：8字形（李萨如）高频闪避
                                import math as _lm
                                _bc["x"] += _bc["vx"] * _bt_dt * _spd_m
                                _lissajous_y = _lm.sin(_st * 4.2) * 55.0 * _bt_dt
                                _lissajous_x = _lm.cos(_st * 2.8) * 35.0 * _bt_dt
                                _bc["x"] += _lissajous_x
                                _bc["y"] += (_bc["vy"] * _bt_dt * _spd_m) + _lissajous_y
                            elif DIFF.current >= DIFF.HARD:
                                import math as _sm2
                                _bc["x"] += _bc["vx"] * _bt_dt * _spd_m
                                _sine_offset = _sm2.sin(_st * 2.8) * 38.0 * _bt_dt
                                _bc["y"] += (_bc["vy"] * _bt_dt * _spd_m) + _sine_offset
                            else:
                                _bc["x"] += _bc["vx"] * _bt_dt * _spd_m
                                _bc["y"] += _bc["vy"] * _bt_dt * _spd_m
                            if _bc["x"] < 60 or _bc["x"] > SW - 110:
                                _bc["vx"] *= -1
                            if _bc["y"] < 20 or _bc["y"] > SH * 0.42:
                                _bc["vy"] *= -1

                        # 碰撞：黄瓜命中Boss字
                        for _ck2 in list(self._h._cukes_flying):
                            for _bc2 in self._h._boss_chars:
                                if _bc2["hp"] <= 0: continue
                                if (abs(_ck2[0] - (_bc2["x"] + 40)) < 55 and
                                        abs(_ck2[1] - (_bc2["y"] + 40)) < 55):
                                    _bc2["hp"]   -= 1
                                    _bc2["hit_t"] = 0.25
                                    self._h.mortis_hp -= 1
                                    if _bc2["hp"] <= 0:
                                        _bc2["dead_t"] = 0.0
                                        self._h.float_texts.append(FloatText(
                                            "💥 " + _bc2["ch"] + " 击碎！",
                                            int(_bc2["x"]), int(_bc2["y"]),
                                            life=1.2, size=22, color="#FF4400"))
                                    else:
                                        self._h.float_texts.append(FloatText(
                                            "hit! " + "♥"*_bc2["hp"],
                                            int(_bc2["x"]), int(_bc2["y"]),
                                            life=0.8, size=18, color="#FFAA00"))
                                    try: self._h._cukes_flying.remove(_ck2)
                                    except: pass
                                    break
                        if self._h.mortis_hp <= 0 and not self._h.round_clear:
                            self._h.round_clear = True

                elif self._h.fake_ending_t >= 12.0 and not self._h.mortis_burst_t:
                    # 8秒后触发撕裂
                    self._h.mortis_burst_t = 0.001

                if self._h.round_clear:
                    if not getattr(self._h, '_ending_cd', False):
                        self._h._ending_cd = 2.2   # 等待2.2秒再切屏（期间可渲染淡黑）
                    self._h._ending_cd -= dt
                    if self._h._ending_cd <= 0:
                        if DIFF.current == DIFF.NORMAL:
                            DIFF.unlock_hard()
                        elif DIFF.current == DIFF.HARD:
                            DIFF.unlock_extreme()
                        if DIFF.current > (persistent.best_diff_cleared or -1):
                            persistent.best_diff_cleared = DIFF.current
                            _save_persistent()
                        store.ed_phase = 0
                        store.ed_t     = 0.0
                        store.ed_di    = 0
                        store.ed_chars = 0.0
                        store.ed_wait  = 0.0
                        self._go("ending")

    GM = GameManager()

    # ── 弹幕持续按键 ─────────────────────────────────────────
    _keys = {"left": False, "right": False, "up": False, "down": False}

    def _v2_move_tick():
        import pygame
        v2 = GM._v2
        dt = 0.016
        if v2.dead or v2.round_clear: return

        # 演示模式下跳过鼠标追踪，由AI控制
        if getattr(DEV, 'demo_mode', False): return

        # ── 鼠标直接定位（主要操作方式）────────────────────────
        mx, my = renpy.get_mouse_pos()
        lx = float(mx - V2_AREA_X)
        ly = float(my)
        lx = max(float(V2_PW//2), min(float(V2_AREA_W - V2_PW//2), lx))
        ly = max(float(V2_PH//2), min(float(V2_AREA_H - V2_PH//2), ly))
        v2.px = lx
        v2.py = ly

        # 仅鼠标控制，无键盘辅助移动

    def _kset(k, v): _keys[k] = v

    def _dev_add_cukes():
        CUKES.collected += 100

    def _p3_depth_up():
        GM._p3.target_depth = GM._p3.DEPTH_MIN

    def _p3_depth_down():
        GM._p3.target_depth = GM._p3.DEPTH_MAX

    # ── 伪3D 鼠标四方向控制 ──────────────────────────────────
    def _p3_move_tick():
        p3 = GM._p3
        if p3.dead or p3.round_clear: return

        # 演示模式下跳过鼠标追踪，由AI控制
        if getattr(DEV, 'demo_mode', False): return

        mx, my = renpy.get_mouse_pos()

        # X 轴 → 横向换道，映射到当前道数（3或5）
        _n  = float(getattr(p3, '_lane_count', P3_LANES))
        _mx = max(0.0, min(1.0, (mx - 160) / 960.0))  # 0~1归一化
        raw_lane = _mx * (_n - 1)
        # 莫比乌斯边缘区
        if mx < 125:
            if abs(p3.target_l - (_n - 1)) > 0.3:
                p3.target_l = _n - 1
                p3.lane     = _n - 1
                if not hasattr(p3, '_wrap_flash'): p3._wrap_flash = 0.0
                p3._wrap_flash = 0.35
        elif mx > 1155:
            if abs(p3.target_l) > 0.3:
                p3.target_l = 0.0
                p3.lane     = 0.0
                if not hasattr(p3, '_wrap_flash'): p3._wrap_flash = 0.0
                p3._wrap_flash = 0.35
        else:
            p3.target_l = max(0.0, min(_n - 1, raw_lane))

        # 深度目标：夹击阶段移到跑道中段，其余时间锁定底部
        p3.target_depth = getattr(p3, '_player_depth_target', p3.DEPTH_MAX)

    # ── 伪3D透视辅助函数（动态VP，支持消失点摇摆） ──────────
    def p3_vp_x():
        return P3_CX + GM._p3.vp_offset_x

    def p3_vp_y():
        return P3_VPY + GM._p3.vp_offset_y

    def p3_lane_cx(norm_x, zr):
        """障碍/分割线用：norm_x是归一化坐标[0,1]，直接线性映射到路面宽度"""
        vpx     = p3_vp_x()
        total_w = P3_LANE_W * 3 * zr
        left    = vpx - total_w / 2
        return left + norm_x * total_w

    def p3_player_cx(lane_float, zr):
        """玩家专用：lane_float在[0, n_f-1]范围，用_lane_count_f转归一化再映射"""
        n_f = getattr(GM._p3, '_lane_count_f', float(P3_LANES))
        n_f = max(1.0, n_f)
        norm = (lane_float + 0.5) / n_f
        norm = max(0.0, min(1.0, norm))
        return p3_lane_cx(norm, zr)

    def p3_lane_y(zr):
        vpy  = p3_vp_y()
        boty = getattr(GM._p3, '_bot_y', P3_BOT_Y)
        return vpy + (boty - vpy) * zr


################################################################################
#  Ren'Py 入口 — 直接跳到我们的主界面
################################################################################
label mutsumi_runner_start:
    $ store._current_bgm = None
    $ renpy.music.play("audio/ショパン「雨だれ」.ogg", loop=True, fadein=1.5)
    $ store._current_bgm = "audio/ショパン「雨だれ」.ogg"
    call screen scr_title
    return

label mutsumi_runner_title_anim:
    $ GM._ta.start_enter()
    $ GM.phase = "title_anim"
    $ _reset_ts()
    call screen scr_router
    return


################################################################################
#  路由画面
################################################################################
screen scr_router():
    style_prefix "mr"
    modal True
    key "K_ESCAPE" action NullAction()
    key "K_F12"    action Function(setattr, DEV, "panel_open", not DEV.panel_open)

    timer 0.016 repeat True action Function(GM.tick)

    # ── 子场景（先渲染，DEV 层叠在最上面）────────────────
    if GM.phase == "title_anim":
        use scr_title_anim
    elif GM.phase == "trans":
        use scr_transition
    elif GM.phase in ("tut_h", "r2_h", "r3_h", "r4_h"):
        use scr_hrunner
    elif GM.phase in ("tut_v2", "r2_v2", "r3_v2"):
        use scr_v2runner
    elif GM.phase in ("tut_p3", "r2_p3", "r3_p3"):
        use scr_p3runner
    elif GM.phase == "ending":
        use scr_ending

    # ── DEV 徽标（已解锁时始终显示，点击切换面板）────────
    if DEV.enabled:
        add Solid("#FFFF00") xpos 1220 ypos 0 xsize 60 ysize 22
        text "DEV" xpos 1228 ypos 3 size 15 color "#000000"
        button xpos 1220 ypos 0 xsize 60 ysize 22 action Function(setattr, DEV, "panel_open", not DEV.panel_open) style "empty_button"

    # ── DEV 面板 ──────────────────────────────────────────
    if DEV.enabled and DEV.panel_open:
        use scr_dev_panel


################################################################################
#  自定义主界面  ── 白屏黑字 + 难度选择
################################################################################
screen scr_title():
    style_prefix "mr"
    add Solid("#FFFFFF")
    # 进入主界面时确保BGM正确
    on "show" action Function(renpy.music.play, "audio/ショパン「雨だれ」.ogg", loop=True, fadein=1.5)

    # ── 标题区 ────────────────────────────────────────────
    text "小 睦 快 跑" xalign 0.5 ypos 90 size 110 color "#000000"

    # ── 操作说明 ──────────────────────────────────────────
    add Solid("#EEEEEE") xalign 0.5 ypos 258 xsize 480 ysize 1
    text "需要鼠标 + 键盘游玩" xalign 0.5 ypos 268 size 18 color "#888888"
    add Solid("#EEEEEE") xalign 0.5 ypos 294 xsize 480 ysize 1

    # ── 难度选择区 ────────────────────────────────────────
    text "选择难度" xalign 0.5 ypos 316 size 20 color "#555555"

    python:
        _d = DIFF.current
        _btn_y   = 350
        _btn_w   = 220
        _btn_h   = 64
        _btn_gap = 14
        _total_w = _btn_w * 4 + _btn_gap * 3
        _btn_x0  = (1280 - _total_w) // 2
        _bxs = [_btn_x0 + i * (_btn_w + _btn_gap) for i in range(4)]
        _locked = [False, False, False, False]   # 全部开放
        _border_cols = ["#000000", "#000000", "#555500", "#550000"]
        _bg_selected  = "#000000"
        _bg_normal    = "#F8F8F8"
        _bg_locked    = "#EEEEEE"

    # 四个难度按钮
    for _bi in range(4):
        python:
            _bx   = _bxs[_bi]
            _bsel = (_d == _bi)
            _blck = _locked[_bi]
            _bbg  = _bg_selected if _bsel else (_bg_locked if _blck else _bg_normal)
            _btxt = "#FFFFFF" if _bsel else ("#AAAAAA" if _blck else "#000000")
            _bsub = "#888888" if _bsel else ("#CCCCCC" if _blck else "#666666")
            _bord = _border_cols[_bi] if _bsel else ("#CCCCCC" if _blck else "#CCCCCC")
            _bname = DIFF.NAMES[_bi]
            _bdesc = DIFF.DESCS[_bi]
            _bact  = Function(DIFF.select, _bi)
        # 边框
        add Solid(_bord) xpos _bx ypos _btn_y xsize _btn_w ysize _btn_h
        add Solid(_bbg) xpos (_bx+2) ypos (_btn_y+2) xsize (_btn_w-4) ysize (_btn_h-4)
        # 难度名
        text _bname xpos (_bx+12) ypos (_btn_y+8) size 28 color _btxt
        # 说明
        if _blck:
            pass
        else:
            text _bdesc xpos (_bx+8) ypos (_btn_y+40) size 11 color _bsub
        # 可点击区域
        button xpos _bx ypos _btn_y xsize _btn_w ysize _btn_h action _bact style "empty_button"

    # ── 当前难度说明 ──────────────────────────────────────
    python:
        _cur_desc = {
            0: "可无限免费复活，难度与普通相同",
            1: "消耗 20 个🥒可复活一次（仅限一次）",
            2: "速度更快，吃🥒可降低压力（-1），需 30🥒复活",
            3: "压力不随时间恢复，吃🥒可降压，无法复活",
        }[DIFF.current]
    add Solid("#F0F0F0") xpos 320 ypos 432 xsize 640 ysize 44
    text _cur_desc xpos 328 ypos 443 size 16 color "#444444"

    # ── 开始按钮 ──────────────────────────────────────────
    add Solid("#000000") xpos 490 ypos 500 xsize 300 ysize 56
    text "点 击 开 始" xpos 546 ypos 514 size 30 color "#FFFFFF"
    button xpos 490 ypos 500 xsize 300 ysize 56 action [Function(GM.__init__), Jump("mutsumi_runner_title_anim")] style "empty_button"
    key "K_RETURN" action [Function(GM.__init__), Jump("mutsumi_runner_title_anim")]
    key "K_SPACE"  action [Function(GM.__init__), Jump("mutsumi_runner_title_anim")]

    # ── 返回小游戏中心 ────────────────────────────────────
    add Solid("#00000066") xpos 20 ypos 20 xsize 120 ysize 40
    text "← 返回" xpos 36 ypos 28 size 20 color "#999999" font "run.otf"
    button xpos 20 ypos 20 xsize 120 ysize 40 action Jump("game_center_start") style "empty_button"
    key "K_ESCAPE" action Jump("game_center_start")

    # 键盘快捷选难度
    key "K_1" action Function(DIFF.select, 0)
    key "K_2" action Function(DIFF.select, 1)
    key "K_3" action Function(DIFF.select, 2)
    key "K_4" action Function(DIFF.select, 3)
    key "K_F12" action Function(setattr, DEV, "panel_open", not DEV.panel_open)

    # 科乐美秘技按键捕获
    key "K_UP"    action Function(_konami_input, "K_UP")
    key "K_DOWN"  action Function(_konami_input, "K_DOWN")
    key "K_LEFT"  action Function(_konami_input, "K_LEFT")
    key "K_RIGHT" action Function(_konami_input, "K_RIGHT")
    key "K_a"     action Function(_konami_input, "K_a")
    key "K_b"     action Function(_konami_input, "K_b")

    # ── DEV 徽标（永久显示，无法隐藏，点击/F12 切换面板）──
    if DEV.enabled:
        add Solid("#FFFF00") xpos 1220 ypos 0 xsize 60 ysize 22
        text "DEV" xpos 1228 ypos 3 size 15 color "#000000"
        button xpos 1220 ypos 0 xsize 60 ysize 22 action Function(setattr, DEV, "panel_open", not DEV.panel_open) style "empty_button"
        if DEV.panel_open:
            use scr_dev_panel

    # ── DEV解锁确认弹窗（秘籍输完后弹出）──────────────────
    if store._dev_popup:
        add Transform(Solid("#000000"), alpha=0.6) xpos 0 ypos 0 xsize 1280 ysize 720
        add Solid("#111111") xpos 390 ypos 240 xsize 500 ysize 240
        add Solid("#FF4400") xpos 390 ypos 240 xsize 500 ysize 3
        text "开启开发者模式？" xpos 500 ypos 258 size 26 color "#FFFFFF"
        text "⚠  开启后将无法再次关闭" xpos 430 ypos 298 size 18 color "#FF8800"
        text "此模式仅供开发测试使用" xpos 440 ypos 322 size 16 color "#888888"
        add Solid("#004400") xpos 430 ypos 368 xsize 180 ysize 44
        text "确认开启" xpos 466 ypos 380 size 20 color "#88FF88"
        button xpos 430 ypos 368 xsize 180 ysize 44 action [
            Function(setattr, DEV, "enabled", True),
            Function(setattr, persistent, "dev_unlocked", True),
            Function(renpy.save_persistent),
            Function(setattr, store, "_dev_popup", False),
            Function(setattr, store, "_konami_buf", [])
        ] style "empty_button"
        add Solid("#440000") xpos 670 ypos 368 xsize 180 ysize 44
        text "取  消" xpos 718 ypos 380 size 20 color "#FF8888"
        button xpos 670 ypos 368 xsize 180 ysize 44 action [
            Function(setattr, store, "_dev_popup", False),
            Function(setattr, store, "_konami_buf", [])
        ] style "empty_button"

style empty_button:
    background None


################################################################################
#  进场动画画面（睦从左滑入，然后游戏开始）
################################################################################
screen scr_title_anim():
    style_prefix "mr"
    add Solid("#FFFFFF")
    # 标题居中
    text "小 睦 快 跑" xalign 0.5 ypos 200 size 110 color "#000000"
    text "— 丰川财集团、弦卷集团都在玩的游戏！ —" xalign 0.5 ypos 340 size 22 color "#888888"
    # 地面线
    add Solid("#535353") xpos 0 ypos 580 xsize 1280 ysize 2
    # 睦从左侧一路跑到右侧消失
    text "睦" xpos int(GM._ta.char_x) ypos 494 size 80 color "#000000"
    # 淡出白幕（睦冲出屏幕后快速盖白）
    if GM._ta.done:
        add Solid("#FFFFFF") alpha GM._ta.fade_out


################################################################################
#  场景过渡动画
#
#  h_v2 : 横版地面线逆时针旋转为竖线，场景变黑，竖边框从两侧滑入
#  v2_p3: 竖边框向外延伸直到消失，伪3D消失点射线从中心射出
#  p3_h : 伪3D射线向右倒，仅保留一条横线，场景亮回来
################################################################################
screen scr_transition():
    style_prefix "mr"
    python:
        import math as _math
        _tr  = GM._tr
        _t   = _tr.t
        _e   = _tr.ease(_t)
        _ef  = _tr.ease(min(1.0, _t * 2.0))       # 前半段 0→1
        _eb  = _tr.ease(max(0.0, _t * 2.0 - 1.0)) # 后半段 0→1
        _k   = _tr.kind
        _CX  = SW // 2

        # ── 各模式睦的起点/终点坐标 ─────────────────────
        # 横版: x=146, y=518, size=52, fg=#535353, bg=#F0F0F0
        # 竖版: x=622, y=600, size=36, fg=#FFFFFF,  bg=#000000
        # 伪3D: x=610, y=602, size=58, fg=#FFFFFF,  bg=#000000
        _H_CX, _H_CY, _H_SZ = 146, H_GY - H_PH_N, 52
        _V_CX, _V_CY, _V_SZ = V2_AREA_X + V2_AREA_W//2 - 18, SH - 120, 36
        _P_CX, _P_CY, _P_SZ = SW//2 - 30, P3_BOT_Y - 58, 58

        def _lerp(a, b, t): return int(a + (b - a) * t)
        def _lerpf(a, b, t): return a + (b - a) * t

        if _k == "h_v2":
            # 睦：从横版位置移动到竖版位置
            _cx = _lerp(_H_CX, _V_CX, _e)
            _cy = _lerp(_H_CY, _V_CY, _e)
            _sz = int(_lerpf(_H_SZ, _V_SZ, _e))
            _fg = "#535353" if _e < 0.5 else "#FFFFFF"
            _line_angle = _e * 90.0
            _lborder_x  = int(_eb * V2_AREA_X)
            _rborder_x  = int(SW - _eb * (SW - V2_AREA_X - V2_AREA_W))

        elif _k == "v2_p3":
            # 睦：从竖版位置移到伪3D位置（两者很近，y轻微上移）
            _cx = _lerp(_V_CX, _P_CX, _e)
            _cy = _lerp(_V_CY, _P_CY, _e)
            _sz = int(_lerpf(_V_SZ, _P_SZ, _e))
            _fg = "#FFFFFF"
            _lborder_x  = int(V2_AREA_X * (1.0 - _e))
            _rborder_x  = int(V2_AREA_X + V2_AREA_W + (SW - V2_AREA_X - V2_AREA_W) * _e)

        else:  # p3_h
            # 睦：从伪3D底部移到横版地面，同时向左移动
            _cx = _lerp(_P_CX, _H_CX, _e)
            _cy = _lerp(_P_CY, _H_CY, _e)
            _sz = int(_lerpf(_P_SZ, _H_SZ, _e))
            _fg = "#FFFFFF" if _e < 0.5 else "#535353"
            _line_angle = 90.0 * (1.0 - _e)
            _horizon_y  = int(P3_VPY + (H_GY - P3_VPY) * _e)

    # 纯黑底
    add Solid("#000000")

    # ─── h_v2 ──────────────────────────────────────────────
    if _k == "h_v2":
        # 浅灰背景淡出
        add Transform(Solid("#F0F0F0"), alpha=(1.0 - _e)) xpos 0 ypos 0 xsize SW ysize SH
        # 地面线旋转（以睦脚下为轴心 → _cx位置，H_GY高度）
        add Transform(Solid("#535353"), xsize=1400, ysize=3, rotate=_line_angle) xpos _CX ypos H_GY xanchor 0.5 yanchor 0.5
        # 睦
        text "睦" xpos _cx ypos _cy size _sz color _fg
        # 后半段竖边框滑入
        if _t > 0.5:
            add Solid("#444444") xpos _lborder_x ypos 0 xsize 3 ysize SH
            add Solid("#444444") xpos _rborder_x ypos 0 xsize 3 ysize SH

    # ─── v2_p3 ─────────────────────────────────────────────
    # 节奏：
    #   0.00–0.45  V2 双边框向中心收拢，面板淡出，形成一条竖线
    #   0.45–0.55  全黑短暂停顿
    #   0.55–1.00  P3 跑道从消失点向下展开（复刻真实 P3 路面渲染）
    elif _k == "v2_p3":
        python:
            import math as _m3
            _t01 = _tr.t
            # 三段缓动
            _t_close = _tr.ease(min(1.0, _t01 / 0.45))
            _t_pause = max(0.0, min(1.0, (_t01 - 0.45) / 0.10))
            _t_open  = _tr.ease(max(0.0, min(1.0, (_t01 - 0.55) / 0.45)))

            # ── 段1：V2 边框向中线收拢 ──────────────────────
            # 起点：左边框在 V2_AREA_X，右边框在 V2_AREA_X+V2_AREA_W
            # 终点：两者都在 SW//2（中央一条线）
            _lb = int(V2_AREA_X + (SW//2 - V2_AREA_X) * _t_close)
            _rb = int(V2_AREA_X + V2_AREA_W + (SW//2 - V2_AREA_X - V2_AREA_W) * _t_close)
            _panel_a = max(0.0, 1.0 - _t_close * 1.2)

            # ── 段3：P3 跑道从消失点向下逐层展开 ────────────
            VPX2 = P3_CX; VPY2 = P3_VPY; BOT2 = P3_BOT_Y; LW2 = P3_LANE_W
            _road_t = []
            if _t_open > 0:
                _reveal_y = int(VPY2 + (BOT2 - VPY2) * _t_open)
                for _ri2 in range(48):
                    _zr  = (_ri2 + 1) / 48.0
                    _zr0 = _ri2 / 48.0
                    _y1  = int(VPY2 + (BOT2 - VPY2) * _zr)
                    _y2  = int(VPY2 + (BOT2 - VPY2) * _zr0)
                    if _y2 > _reveal_y:
                        break
                    _y1c = min(_y1, _reveal_y)
                    _hw2  = int(LW2 * 3 / 2 * _zr)
                    _lum2 = int(30 + 80 * _zr)
                    _c2   = "#{0:02X}{0:02X}{0:02X}".format(_lum2)
                    _road_t.append((VPX2 - _hw2, _y2, _hw2 * 2, max(1, _y1c - _y2), _c2))

            # 分割线（随展开逐步出现）
            _divs_t = []
            if _t_open > 0:
                for _ln2 in [1, 2]:
                    for _st2 in range(20):
                        _zr2 = (_st2 + 1) / 20.0
                        if _zr2 > _t_open:
                            break
                        _hw3 = LW2 * 3 / 2 * _zr2
                        _lf2 = VPX2 - _hw3
                        _divs_t.append((int(_lf2 + _ln2 * LW2 * _zr2),
                                        int(VPY2 + (BOT2 - VPY2) * _zr2)))

        # 全黑底
        add Solid("#000000")

        # 段1：V2 面板残留淡出
        if _t_close < 1.0:
            add Transform(Solid("#0D0D0D"), alpha=_panel_a) xpos V2_AREA_X ypos 0 xsize V2_AREA_W ysize SH
            add Solid("#555555") xpos _lb ypos 0 xsize 3 ysize SH
            add Solid("#555555") xpos _rb ypos 0 xsize 3 ysize SH

        # 段3：P3 跑道逐层展开
        for (_rx2, _ry2, _rw2, _rh2, _rc2) in _road_t:
            add Solid(_rc2) xpos _rx2 ypos _ry2 xsize _rw2 ysize _rh2
        for (_dx2, _dy2) in _divs_t:
            add Solid("#FFFFFF") alpha 0.3 xpos _dx2 ypos _dy2 xsize 2 ysize 5

        # 消失点处小十字（焦点）
        if _t_open > 0.1:
            add Transform(Solid("#FFFFFF"), alpha=min(1.0, _t_open * 2)) xpos (P3_CX-8) ypos (P3_VPY-1) xsize 16 ysize 2
            add Transform(Solid("#FFFFFF"), alpha=min(1.0, _t_open * 2)) xpos (P3_CX-1) ypos (P3_VPY-8) xsize 2 ysize 16

        # 睦（全程）
        text "睦" xpos _cx ypos _cy size _sz color _fg

    # ─── p3_h ──────────────────────────────────────────────
    else:
        # 前半段：透视线渐隐
        if _t < 0.55:
            python:
                _ar = max(0.0, 1.0 - _t / 0.55)
            add Transform(Solid("#FFFFFF"), alpha=(_ar * 0.5)) xpos V2_AREA_X ypos P3_VPY xsize 3 ysize (P3_BOT_Y - P3_VPY)
            add Transform(Solid("#FFFFFF"), alpha=(_ar * 0.5)) xpos (V2_AREA_X + V2_AREA_W) ypos P3_VPY xsize 3 ysize (P3_BOT_Y - P3_VPY)
            add Transform(Solid("#FFFFFF"), alpha=(_ar * 0.3)) xpos _CX ypos P3_VPY xsize 2 ysize (P3_BOT_Y - P3_VPY)
        # 地平线从 P3_VPY 旋转降落到 H_GY
        add Transform(Solid("#535353"), xsize=1400, ysize=3, rotate=_line_angle) xpos _CX ypos _horizon_y xanchor 0.5 yanchor 0.5
        # 浅灰场景亮起
        add Transform(Solid("#F0F0F0"), alpha=_e) xpos 0 ypos 0 xsize SW ysize SH
        # 确保地面线始终清晰
        if _e > 0.5:
            add Solid("#535353") xpos 0 ypos H_GY xsize SW ysize 3
        # 睦
        text "睦" xpos _cx ypos _cy size _sz color _fg


################################################################################
#  横版 2D 跑酷
################################################################################
screen scr_hrunner():
    style_prefix "mr"
    python:
        import math as _math
        _h     = GM._h
        _label = {
            "tut_h": "Round 1  教程",
            "r2_h":  "Round 2",
            "r3_h":  "Round 3",
            "r4_h":  "",  # Round 4 不显示标签（墨缇斯战）
        }.get(GM.phase, "")
        _osn   = list(_h.obs)
        _ftn   = list(_h.float_texts)
        _pdy   = int(_h.py + (H_PH_N - H_PH_D)) if _h.ducking else int(_h.py)
        _psz   = 32 if _h.ducking else 52
        _pdx   = H_PX - _psz // 4
        _inv   = invert_mode[0]
        _BG    = "#000000" if _inv else "#F0F0F0"
        _FG    = "#FFFFFF" if _inv else "#535353"
        _CLOUD = "#444444" if _inv else "#D8D8D8"
        _DASH  = "#666666" if _inv else "#9E9E9E"
        _pchar = PRESSURE.get_char()
        _shx   = int(PRESSURE.shake_x)
        _shy   = int(PRESSURE.shake_y)

    add Solid(_BG)

    python:
        _goff = int(_h.dist) % 24
        _cloud_spd_offset = int(_h.dist * 0.25)
        _clouds = []
        _cloud_defs = [
            (300, 108, 80, 22, 44, 20),
            (800,  90, 68, 20, 38, 18),
            (1200, 136, 60, 18, 34, 16),
        ]
        for (bx, by, w1, h1, w2, h2) in _cloud_defs:
            cx = (bx - _cloud_spd_offset) % 1500 - 120
            _clouds.append((int(cx), by,     w1, h1))
            _clouds.append((int(cx)+20, by-16, w2, h2))
        _dashes = []
        _x2 = -_goff
        while _x2 < SW + 24:
            _dashes.append(int(_x2)); _x2 += 24

    for (_cx, _cy, _cw, _ch) in _clouds:
        add Solid(_CLOUD) xpos (_cx + _shx) ypos (_cy + _shy) xsize _cw ysize _ch

    add Solid(_FG) xpos 0 ypos (H_GY + _shy) xsize SW ysize 2
    for _dx in _dashes:
        add Solid(_DASH) xpos _dx ypos (H_GY+4+_shy) xsize 8 ysize 2

    # 障碍物（文字/黄瓜/反转必须/反转安全/普通）
    for _o in _osn:
        if _o.is_cucumber:
            text "🥒" xpos int(_o.x) ypos int(_o.y) size 26 color _FG
        elif _o.char:
            python:
                _oc2 = ("#888888" if _inv else "#777777") if _o.invert_safe else _FG
            text _o.char xpos int(_o.x) ypos int(_o.y) size 42 color _oc2
        elif _o.invert_required:
            # 必须反转才能过：白底+粗黑边框，正常模式下顶部显示"!" 警告
            python:
                _ir_bg = "#FFFFFF" if not _inv else "#000000"
                _ir_fg = "#000000" if not _inv else "#FFFFFF"
            add Solid(_ir_bg) xpos int(_o.x) ypos int(_o.y) xsize _o.w ysize _o.h
            add Solid(_ir_fg) xpos int(_o.x) ypos int(_o.y) xsize _o.w ysize 3
            add Solid(_ir_fg) xpos int(_o.x) ypos int(_o.y) xsize 3 ysize _o.h
            add Solid(_ir_fg) xpos (int(_o.x)+_o.w-3) ypos int(_o.y) xsize 3 ysize _o.h
            if not _inv:
                text "!" xpos (int(_o.x)+_o.w//2-6) ypos int(_o.y) size 22 color _ir_fg
        elif _o.invert_safe:
            add Solid("#888888") xpos int(_o.x) ypos int(_o.y) xsize _o.w ysize _o.h
        else:
            add Solid(_FG) xpos int(_o.x) ypos int(_o.y) xsize _o.w ysize _o.h

    # 玩家（Mortis战时X坐标动态）
    python:
        _is_r4 = (GM.phase == "r4_h")
        _hpx_draw = int(getattr(_h, 'px', H_PX)) if getattr(_h, 'px_free', False) else H_PX
        _px_draw = _hpx_draw - _psz//4 + _shx
        _py_draw = _pdy + _shy
        _use_stroke = getattr(_h, 'mortis_active', False)
    # 描边只在墨缇斯桌面阶段启用（桌面背景不可控）
    if _use_stroke:
        text _pchar xpos (_px_draw - 3) ypos  _py_draw      size _psz color "#000000"
        text _pchar xpos (_px_draw + 3) ypos  _py_draw      size _psz color "#000000"
        text _pchar xpos  _px_draw      ypos (_py_draw - 3) size _psz color "#000000"
        text _pchar xpos  _px_draw      ypos (_py_draw + 3) size _psz color "#000000"
    # 主体
    text _pchar xpos _px_draw ypos _py_draw size _psz color _FG

    # ── Round 4 墨缇斯专用演出 ───────────────────────────────
    if _is_r4:
        python:
            _fet  = getattr(_h, 'fake_ending_t', 0.0)
            _mbt  = getattr(_h, 'mortis_burst_t', 0.0)
            _mact = getattr(_h, 'mortis_active', False)
            import os as _os4
            _dsk_path   = _os4.path.join(config.gamedir, "desktop_cache.png").replace("\\", "/")
            _dsk_exists = getattr(_h, 'desktop_ready', False) and _os4.path.exists(_dsk_path)
            _dsk_ok     = _dsk_exists  # 文件在game/目录内，直接用绝对路径加载
            _mb_ok      = renpy.loadable("mortis_burst.png")

        # ── 假结局阶段（0~12s）：字幕 + 制作人名单滚动 ──
        if _fet > 0 and _mbt == 0:
            python:
                _fade_in = min(1.0, _fet / 1.5)
            add Transform(Solid("#000000"), alpha=_fade_in) xpos 0 ypos 0 xsize SW ysize SH
            if _fet > 1.8:
                python:
                    _sub_a = min(1.0, (_fet - 1.8) / 1.0)
                add Transform(Text("小睦成功击败了爽世、祥子……", size=26, color="#CCCCCC"), alpha=_sub_a) xpos 320 ypos 210
                if _fet > 4.0:
                    python:
                        _sub2_a = min(1.0, (_fet - 4.0) / 1.0)
                    add Transform(Text("春日影的旋律，终于停止了。游戏已经接近尾声，接下来就是久违的谢幕表了。", size=20, color="#666666"), alpha=_sub2_a) xpos 380 ypos 258
                # 制作人名单（5.5s后开始滚动）
                if _fet > 5.5:
                    python:
                        _scroll   = (_fet - 5.5) * 48.0
                        _cred_a   = min(1.0, (_fet - 5.5) / 0.6)
                        _credits  = [
                            ("", "小   睦   快   跑", 28, "#FFFFFF"),
                            ("", "", 10, "#000000"),
                            ("项目企划", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("脚本剧情", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("程序架构", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("交互逻辑", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("素材润色", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("环境渲染", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("", "", 14, "#000000"),
                            ("游戏测试", "缄默奥斯卡",   18, "#AAAAAA"),
                            ("游戏测试", "肆肆",          18, "#AAAAAA"),
                            ("游戏测试", "K-Angelati Jessica~喵", 18, "#AAAAAA"),
                            ("游戏测试", "夜鹭pixy",      18, "#AAAAAA"),
                            ("", "", 14, "#000000"),
                            ("", "— Special Thanks —", 14, "#555555"),
                            ("", "TRPG群的朋友们", 16, "#444444"),
                            ("", "以及正在游玩的你", 16, "#444444"),
                            ("", "", 20, "#000000"),
                            ("", "谢谢游玩", 22, "#888888"),
                        ]
                        _base_y   = 680
                        _line_gap = 38
                    for _ci2, (_crole, _cname, _csz, _ccol) in enumerate(_credits):
                        python:
                            _cy3 = int(_base_y + _ci2 * _line_gap - _scroll)
                        if _cy3 > -40 and _cy3 < SH + 10:
                            if _crole:
                                add Transform(Text(_crole, size=13, color="#555555"), alpha=_cred_a) xpos 480 ypos _cy3
                                add Transform(Text(_cname, size=_csz, color=_ccol), alpha=_cred_a) xpos 600 ypos (_cy3 - 2)
                            else:
                                add Transform(Text(_cname, size=_csz, color=_ccol), alpha=_cred_a) xpos (SW//2 - len(_cname)*_csz//4) ypos _cy3

        # ── 撕裂演出（mortis_burst_t 计时）──────────────────
        # 节奏：
        #  0.00~0.20  黑底 + 中央红裂缝扩张
        #  0.20~0.50  白色闪光
        #  0.50~1.30  桌面左右撕裂分开 + 墨缇斯从中央横向冲出
        #  1.30~2.20  墨缇斯全屏 + 画面震动 + "抓·到·你·了"
        #  2.20~3.00  过渡至桌面背景
        if _mbt > 0 and not _mact:
            # 阶段一：红裂缝
            if _mbt < 0.20:
                python:
                    _crack_w = int(_mbt / 0.20 * 8) + 1
                    _crack_a = min(1.0, _mbt / 0.10)
                add Solid("#000000") xpos 0 ypos 0 xsize SW ysize SH
                add Transform(Solid("#FF2200"), alpha=_crack_a) xpos (SW//2 - _crack_w//2) ypos 0 xsize _crack_w ysize SH
                # 裂缝周围光晕
                add Transform(Solid("#FF4400"), alpha=(_crack_a * 0.3)) xpos (SW//2 - 30) ypos 0 xsize 60 ysize SH

            # 阶段二：白闪
            elif _mbt < 0.50:
                python:
                    _fl_a = min(1.0, (_mbt - 0.20) / 0.15)
                add Solid("#000000") xpos 0 ypos 0 xsize SW ysize SH
                add Transform(Solid("#FFFFFF"), alpha=_fl_a) xpos 0 ypos 0 xsize SW ysize SH

            # 阶段三：左右撕裂（带旋转）+ 墨缇斯横向冲出
            elif _mbt < 1.30:
                python:
                    # 撕裂进度：0~0.2s内完成（easein：慢启动，t²加速）
                    _tt     = min(1.0, (_mbt - 0.50) / 0.20)
                    _ease_t = _tt * _tt   # easein cubic
                    _off    = int(_ease_t * 300)
                    _rot    = _ease_t * 5.0
                    # 墨缇斯冲入进度（0.50s起，0.05s内alpha到1，0.1s easeout zoom到1.15，再0.1s easein到1.1）
                    _mb_t   = max(0.0, _mbt - 0.50)
                    _mb_a   = min(1.0, _mb_t / 0.05)
                    if _mb_t < 0.1:
                        _mb_zoom = 0.9 + (_mb_t / 0.1) * (1.15 - 0.9)   # easeout: 0.9→1.15
                    elif _mb_t < 0.2:
                        _mb_zoom = 1.15 - ((_mb_t - 0.1) / 0.1) * (1.15 - 1.1)  # easein: 1.15→1.1
                    else:
                        _mb_zoom = 1.1
                # 左半桌面：向左推开 + 轻微逆时针旋转
                if _dsk_ok:
                    add Transform(
                        Crop((0, 0, SW//2, SH), Image(_dsk_path)),
                        xoffset=-_off, yoffset=0, rotate=-_rot,
                        transform_anchor=True, anchor=(1.0, 0.5)
                    )
                else:
                    add Transform(Solid("#111122"), xoffset=-_off, rotate=-_rot,
                                  transform_anchor=True, anchor=(1.0, 0.5)) xpos 0 ypos 0 xsize (SW//2) ysize SH
                # 右半桌面：向右推开 + 顺时针旋转
                if _dsk_ok:
                    add Transform(
                        Crop((SW//2, 0, SW//2, SH), Image(_dsk_path)),
                        xoffset=(SW//2 + _off), yoffset=0, rotate=_rot,
                        transform_anchor=True, anchor=(0.0, 0.5)
                    )
                else:
                    add Transform(Solid("#111122"), xoffset=_off, rotate=_rot,
                                  transform_anchor=True, anchor=(0.0, 0.5)) xpos (SW//2) ypos 0 xsize (SW//2) ysize SH
                # 中央黑色裂口
                add Solid("#000000") xpos (SW//2 - _off) ypos 0 xsize (_off * 2) ysize SH
                # 墨缇斯从中央冲出（anchor中心，zoom冲击感）
                if _mb_ok:
                    add Transform(
                        Image("mortis_burst.png"),
                        alpha=_mb_a, zoom=_mb_zoom,
                        transform_anchor=True,
                        anchor=(0.5, 0.5),
                        xpos=SW//2, ypos=SH//2
                    )
                else:
                    add Transform(
                        Text("抓·到·你·了", size=90, color="#FF0000"),
                        alpha=_mb_a, zoom=_mb_zoom,
                        transform_anchor=True, anchor=(0.5, 0.5),
                        xpos=SW//2, ypos=SH//2
                    )

            # 阶段四：墨缇斯全屏 + 震动 + 台词
            elif _mbt < 2.20:
                python:
                    _t4     = (_mbt - 1.30) / 0.90
                    _shk2   = int(math.sin(_mbt * 55) * max(0, (1.0 - _t4 * 1.5)) * 8)
                    _txt_a  = min(1.0, (_mbt - 1.50) / 0.30)
                if _mb_ok:
                    add Transform(Image("mortis_burst.png")) xpos _shk2 ypos 0
                else:
                    add Solid("#0A0A0A") xpos 0 ypos 0 xsize SW ysize SH
                    add Transform(Text("抓·到·你·了", size=90, color="#FF0000"), alpha=1.0) xpos (320 + _shk2) ypos 250
                # "抓·到·你·了" 系统级红字
                add Transform(
                    Text("抓  ·  到  ·  你  ·  了", size=36, color="#FF2200"),
                    alpha=_txt_a
                ) xpos (SW//2 - 200 + _shk2) ypos (SH - 120)

            # 阶段五：过渡至桌面背景
            else:
                python:
                    _fade_desk = min(1.0, (_mbt - 2.20) / 0.60)
                if _dsk_ok:
                    add im.Scale(_dsk_path, SW, SH) xpos 0 ypos 0
                else:
                    add Solid("#0A0A12") xpos 0 ypos 0 xsize SW ysize SH
                if _mb_ok:
                    add Transform(Image("mortis_burst.png"), alpha=(1.0 - _fade_desk)) xpos 0 ypos 0

        # ── Mortis战：桌面滚动背景 + 三阶段视觉 ──
        if _mact:
            python:
                _mp2      = getattr(_h, 'mortis_phase', 1)
                _scroll_off = int(_h.dist) % SW
                _bt_active  = getattr(_h, '_sling_held', False)  # 子弹时间
            # 桌面背景循环滚动（子弹时间时放慢）
            if _dsk_ok:
                add im.Scale(_dsk_path, SW, SH) xpos (-_scroll_off) ypos 0
                add im.Scale(_dsk_path, SW, SH) xpos (SW - _scroll_off) ypos 0
            else:
                add Solid("#1A1A2E") xpos 0 ypos 0 xsize SW ysize SH
            # 子弹时间：白色半透明蒙版
            if _bt_active:
                add Transform(Solid("#FFFFFF"), alpha=0.12) xpos 0 ypos 0 xsize SW ysize SH

            # 地面线
            add Solid("#FF4444") alpha 0.8 xpos 0 ypos H_GY xsize SW ysize 3


            # ── 阶段二：未响应蒙版 + 进度条 ──
            if _mp2 == 2:
                python:
                    _nr_t   = getattr(_h, '_no_resp_t', 0.0)
                    _prog_x = int(getattr(_h, '_progress_x', -60))
                # 未响应白霜
                if _nr_t > 0:
                    python:
                        _nr_a = min(0.35, _nr_t * 0.12)
                    add Transform(Solid("#FFFFFF"), alpha=_nr_a) xpos 0 ypos 0 xsize SW ysize SH
                    add Transform(
                        Text("Mutsumi_Runner.exe  （未响应）", size=16, color="#333333"),
                        alpha=min(1.0, _nr_t)
                    ) xpos (SW//2 - 180) ypos 18
                # 进度条
                if _prog_x > -50:
                    add Transform(Solid("#22BB22"), alpha=0.9) xpos 0 ypos 0 xsize _prog_x ysize SH
                    add Transform(Solid("#44FF44"), alpha=0.6) xpos (_prog_x - 4) ypos 0 xsize 4 ysize SH
                    add Transform(
                        Text("正在删除  Mutsumi.exe…", size=14, color="#003300"),
                        alpha=0.9
                    ) xpos max(8, _prog_x - 220) ypos (SH//2 - 10)

            # ── 阶段三：弹弓界面 ──
            if _mp2 == 3:
                python:
                    _sling  = getattr(_h, '_sling_held', False)
                    _sox    = int(getattr(_h, '_sling_ox', 0))
                    _soy    = int(getattr(_h, '_sling_oy', 0))
                    _smx    = int(getattr(_h, '_sling_mx', 0))
                    _smy    = int(getattr(_h, '_sling_my', 0))
                    _GRAV_C = 600.0
                # 拉弓中：绘制抛物线预测
                if _sling:
                    python:
                        _dvx = (_sox - _smx) * 2.2
                        _dvy = (_soy - _smy) * 2.2
                        _pts = []
                        _px2 = float(_sox); _py2 = float(_soy)
                        _vx2 = _dvx;        _vy2 = _dvy
                        for _ti in range(25):
                            _pts.append((int(_px2), int(_py2)))
                            _step = 0.06
                            _px2 += _vx2 * _step
                            _py2 += _vy2 * _step
                            _vy2 += _GRAV_C * _step
                            if _py2 > SH: break
                    for _pi in range(0, len(_pts) - 1, 2):
                        python:
                            _dot_a = 1.0 - _pi / 26.0
                        add Transform(Solid("#FFEE00"), alpha=_dot_a) xpos (_pts[_pi][0]-3) ypos (_pts[_pi][1]-3) xsize 6 ysize 6
                # 弹弓拉力线
                if _sling:
                    add Transform(Solid("#FF8800"), alpha=0.7) xpos min(_sox,_smx) ypos min(_soy,_smy) xsize max(2,abs(_smx-_sox)) ysize 2
                # 飞行中的黄瓜（带黑色描边，在桌面上清晰可见）
                for _ck3 in list(getattr(_h, '_cukes_flying', [])):
                    python:
                        _ckx = int(_ck3[0]) - 14
                        _cky = int(_ck3[1]) - 14
                    text "🥒" xpos (_ckx - 2) ypos  _cky      size 28 color "#000000"
                    text "🥒" xpos (_ckx + 2) ypos  _cky      size 28 color "#000000"
                    text "🥒" xpos  _ckx      ypos (_cky - 2) size 28 color "#000000"
                    text "🥒" xpos  _ckx      ypos (_cky + 2) size 28 color "#000000"
                    text "🥒" xpos _ckx ypos _cky size 28

                # Boss三字靶（飘动）
                for _bc3 in getattr(_h, '_boss_chars', []):
                    python:
                        _bx3  = int(_bc3["x"]); _by3 = int(_bc3["y"])
                        _bhp3 = _bc3.get("hp", 0)
                        _bht3 = _bc3.get("hit_t", 0.0)
                        _bdt3 = _bc3.get("dead_t", -1.0)
                    if _bhp3 <= 0:
                        # 粉碎动画
                        if 0.0 <= _bdt3 < 0.9:
                            python:
                                _shatter_a = 1.0 - _bdt3 / 0.9
                                _shatter_s = int(80 + _bdt3 * 80)
                            add Transform(Text(_bc3["ch"], size=_shatter_s, color="#FF2200"),
                                alpha=_shatter_a) xpos (_bx3 - 20) ypos (_by3 - 20)
                    else:
                        python:
                            _pulse   = 0.85 + 0.15 * math.sin(_h.phase_timer * 3.0)
                            _b_col   = "#FFFFFF" if _bht3 > 0 else "#CC0000"  # 受击白闪
                            _b_size  = 80
                        # 描边
                        add Transform(Text(_bc3["ch"], size=_b_size, color="#000000"),
                            alpha=_pulse) xpos (_bx3 - 3) ypos _by3
                        add Transform(Text(_bc3["ch"], size=_b_size, color="#000000"),
                            alpha=_pulse) xpos (_bx3 + 3) ypos _by3
                        add Transform(Text(_bc3["ch"], size=_b_size, color="#000000"),
                            alpha=_pulse) xpos _bx3 ypos (_by3 - 3)
                        add Transform(Text(_bc3["ch"], size=_b_size, color="#000000"),
                            alpha=_pulse) xpos _bx3 ypos (_by3 + 3)
                        add Transform(Text(_bc3["ch"], size=_b_size, color=_b_col),
                            alpha=_pulse) xpos _bx3 ypos _by3
                        # 每字HP小格
                        add Transform(Solid("#FF2200"), alpha=0.9) xpos _bx3 ypos (_by3 - 14) xsize 22 ysize 8
                        add Transform(Solid("#FF2200"), alpha=(0.9 if _bhp3 >= 2 else 0.2)) xpos (_bx3+24) ypos (_by3 - 14) xsize 22 ysize 8
                        add Transform(Solid("#FF2200"), alpha=(0.9 if _bhp3 >= 3 else 0.2)) xpos (_bx3+48) ypos (_by3 - 14) xsize 22 ysize 8

                # 拉弓预测轨迹（物理与实际完全一致）
                python:
                    _sling_on = getattr(_h, '_sling_held', False)
                if _sling_on:
                    python:
                        import math as _tm
                        _sox2 = getattr(_h, '_sling_ox', 0.0)
                        _soy2 = getattr(_h, '_sling_oy', 0.0)
                        _smx2 = getattr(_h, '_sling_mx', 0.0)
                        _smy2 = getattr(_h, '_sling_my', 0.0)
                        _ddx  = _sox2 - _smx2; _ddy = _soy2 - _smy2
                        _pull2 = min(_tm.hypot(_ddx, _ddy), 280.0)
                        _GRAV_P = 480.0
                        _traj_pts = []
                        if _pull2 > 12.0:
                            _dist_r2 = _tm.hypot(_ddx + 0.001, _ddy + 0.001)
                            _spd_v2 = 380.0 + _pull2 * 1.5
                            _tvx = (_ddx / _dist_r2) * _spd_v2
                            _tvy = (_ddy / _dist_r2) * _spd_v2
                            _tx = float(_sox2); _ty = float(_soy2)
                            _step2 = 1.0 / 60.0
                            for _ti in range(36):
                                _traj_pts.append((int(_tx), int(_ty)))
                                _tx += _tvx * _step2
                                _ty += _tvy * _step2
                                _tvy += _GRAV_P * _step2
                                if _ty > SH: break
                    for _pi2 in range(0, len(_traj_pts) - 1, 2):
                        python:
                            _dot_a2 = max(0.15, 1.0 - _pi2 / 38.0)
                            _dot_x2 = _traj_pts[_pi2][0] - 4
                            _dot_y2 = _traj_pts[_pi2][1] - 4
                            # 三个难度均全部显示轨迹
                            _dot_visible = True
                        if _dot_visible:
                            add Transform(Solid("#FFEE00"), alpha=_dot_a2) xpos _dot_x2 ypos _dot_y2 xsize 8 ysize 8

                # 提示
                if _h.mortis_phase_t < 4.0:
                    python:
                        _tip_a = min(1.0, 4.0 - _h.mortis_phase_t)
                    add Transform(Text("按住鼠标左键瞄准  松开发射🥒", size=18, color="#000000"),
                        alpha=(_tip_a * 0.7)) xpos (SW//2 - 163) ypos (SH - 81)
                    add Transform(Text("按住鼠标左键瞄准  松开发射🥒", size=18, color="#FFFF88"),
                        alpha=_tip_a) xpos (SW//2 - 160) ypos (SH - 80)

            # 玩家（带描边，在桌面背景上清晰可见）
            python:
                _p_col    = "#FFFF44" if _bt_active else "#FFFFFF"
                _p_stroke = "#000000"
                _px_m  = _hpx_draw - _psz//4 + _shx
                _py_m  = _pdy + _shy
            # 黑色描边4方向
            text _pchar xpos (_px_m - 3) ypos  _py_m      size _psz color _p_stroke
            text _pchar xpos (_px_m + 3) ypos  _py_m      size _psz color _p_stroke
            text _pchar xpos  _px_m      ypos (_py_m - 3) size _psz color _p_stroke
            text _pchar xpos  _px_m      ypos (_py_m + 3) size _psz color _p_stroke
            # 主体
            text _pchar xpos _px_m ypos _py_m size _psz color _p_col

            # ── 弹幕子弹（所有阶段）──
            python:
                _bullets = getattr(_h, '_mortis_bullets', [])
            for _bl3 in _bullets:
                python:
                    _blx = int(_bl3[0]); _bly = int(_bl3[1])
                # 黑色底层描边
                add Solid("#000000") xpos (_blx - 7) ypos (_bly - 7) xsize 14 ysize 14
                # 红色菱形弹幕
                add Transform(Solid("#FF1111"), rotate=45) xpos (_blx - 5) ypos (_bly - 5) xsize 10 ysize 10
                add Transform(Solid("#FF8888"), rotate=45) xpos (_blx - 2) ypos (_bly - 2) xsize 4 ysize 4

            # ── 墨缇斯名字（阶段一/二悬浮）──
            if _mp2 in (1, 2):
                python:
                    _name_bob = int(math.sin(_h.phase_timer * 1.8) * 6)
                    _name_a   = 0.7 + 0.3 * math.sin(_h.phase_timer * 2.5)
                # 描边
                add Transform(Text("墨缇斯", size=36, color="#000000"),
                    alpha=_name_a) xpos (SW//2 - 57) ypos (28 + _name_bob)
                add Transform(Text("墨缇斯", size=36, color="#000000"),
                    alpha=_name_a) xpos (SW//2 - 51) ypos (28 + _name_bob)
                add Transform(Text("墨缇斯", size=36, color="#000000"),
                    alpha=_name_a) xpos (SW//2 - 54) ypos (26 + _name_bob)
                add Transform(Text("墨缇斯", size=36, color="#000000"),
                    alpha=_name_a) xpos (SW//2 - 54) ypos (32 + _name_bob)
                add Transform(Text("墨缇斯", size=36, color="#FF0000"),
                    alpha=_name_a) xpos (SW//2 - 54) ypos (30 + _name_bob)

            # 通关淡黑遮罩
            python:
                _ecd = getattr(_h, '_ending_cd', -1)
                _fade_out_a = max(0.0, min(1.0, 1.0 - (_ecd / 2.2))) if (_ecd > 0 and _h.round_clear) else 0.0
            if _fade_out_a > 0:
                add Transform(Solid("#000000"), alpha=_fade_out_a) xpos 0 ypos 0 xsize SW ysize SH
            python:
                _hp_left9 = max(0, getattr(_h, 'mortis_hp', 9))
                _hp_max9  = getattr(_h, '_mortis_hp_max', 9)
                _hp_str   = "♥" * _hp_left9 + "♡" * (_hp_max9 - _hp_left9)
            add Transform(Text("BOSS  " + _hp_str, size=16, color="#000000"),
                alpha=0.9) xpos (SW//2 - 85) ypos (SH - 37)
            add Transform(Text("BOSS  " + _hp_str, size=16, color="#FF2200"),
                alpha=0.9) xpos (SW//2 - 84) ypos (SH - 36)



    # 飘字（mortis桌面阶段强制加描边）
    for _ft in _ftn:
        python:
            _ft_outline = getattr(_ft, 'outline', False) or _h.mortis_active
        if _ft_outline:
            for _ox, _oy in ((-3,0),(3,0),(0,-3),(0,3)):
                add Transform(Text(_ft.text, size=_ft.size, color="#000000"),
                    alpha=(_ft.alpha * 0.9)) xpos (int(_ft.x)+_shx+_ox) ypos (int(_ft.y)+_shy+_oy)
        add Transform(Text(_ft.text, size=_ft.size, color=(_ft.color if _h.mortis_active else _FG)),
            alpha=_ft.alpha) xpos (int(_ft.x)+_shx) ypos (int(_ft.y)+_shy)

    # 假鼠标指针（教程阶段）
    if _h._fake_cur_on:
        python:
            _fcx = int(_h._fake_cur_x)
            _fcy = int(_h._fake_cur_y)
            # 墨缇斯战：桌面背景，光标用红色更显眼
            if getattr(_h, 'mortis_active', False):
                _fc_col = "#FF2200"
                _fc_bg  = "#000000"
            elif not _inv:
                _fc_col = "#535353"
                _fc_bg  = "#000000"
            else:
                _fc_col = "#FFFFFF"
                _fc_bg  = "#000000"
        # 像素风箭头光标：主体 + 黑色轮廓
        add Solid(_fc_bg)  xpos (_fcx-1) ypos (_fcy-1) xsize 18 ysize 4
        add Solid(_fc_bg)  xpos (_fcx-1) ypos (_fcy-1) xsize 4  ysize 18
        add Solid(_fc_bg)  xpos (_fcx+7) ypos (_fcy+7) xsize 10 ysize 4
        add Solid(_fc_bg)  xpos (_fcx+7) ypos (_fcy+7) xsize 4  ysize 10
        add Solid(_fc_col) xpos _fcx     ypos _fcy     xsize 16 ysize 3
        add Solid(_fc_col) xpos _fcx     ypos _fcy     xsize 3  ysize 16
        add Solid(_fc_col) xpos (_fcx+8) ypos (_fcy+8) xsize 8  ysize 3
        add Solid(_fc_col) xpos (_fcx+8) ypos (_fcy+8) xsize 3  ysize 8
        # 中心点
        add Solid(_fc_col) xpos (_fcx+1) ypos (_fcy+1) xsize 2  ysize 2

    # 压力噪点
    if PRESSURE.noise_count > 0:
        python:
            _nc = "#FFFFFF" if not _inv else "#000000"
            _npts = [(random.randint(0,SW-4), random.randint(0,SH-4)) for _ in range(PRESSURE.noise_count)]
        for (_nx, _ny) in _npts:
            add Solid(_nc) xpos _nx ypos _ny xsize 3 ysize 3

    # HUD
    if _label != "":
        text _label xpos 20 ypos 24 size 18 color _DASH
    text "🥒×%d" % CUKES.collected xpos 20 ypos 50 size 18 color _FG
    if CUKES.can_revive:
        text "[[F]] 复活" xpos 20 ypos 74 size 16 color _FG
    # 压力槽：黑底，红条从左往右
    python:
        _pw2     = int(160 * PRESSURE.value / 100.0)
        _pbar_c  = "#FF0000" if PRESSURE.value >= 80 else "#CC2222"
        _pbar_a  = (0.7 + 0.3 * math.sin(_h.phase_timer * 14.0)) if PRESSURE.value >= 80 else 1.0
    add Solid("#222222") xpos (SW-182) ypos 54 xsize 162 ysize 14
    if _pw2 > 0:
        add Transform(Solid(_pbar_c), alpha=_pbar_a) xpos (SW-180) ypos 56 xsize _pw2 ysize 10
    if PRESSURE.value >= 80:
        add Transform(Text("DANGER", size=10, color="#FF2222"), alpha=_pbar_a) xpos (SW-182) ypos 70
    else:
        text "PRESSURE" xpos (SW-182) ypos 70 size 10 color "#888888"
    # 接近 invert_required 障碍时在屏幕右侧闪烁提示
    python:
        _ir_near = any(e.invert_required and e.x < SW * 0.65 for e in _osn)
    if _ir_near and not _inv:
        python:
            _hint_a = 0.5 + 0.5 * _math.sin(_h.phase_timer * 8.0)
        add Transform(Text("[[Shift]] 反转！", size=26, color=_FG), alpha=_hint_a) xpos (SW-260) ypos (SH//2-20)
    if invert_mode[0]:
        text "◈ INVERT  压力上升中" xpos (SW//2-70) ypos 8 size 14 color _FG

    if GM.phase == "tut_h":
        python:
            _tp = min(_h.phase_timer / GM.TUT_H_DUR, 1.0)
            _bw = int(300 * _tp)
        add Solid(_DASH) xpos (SW//2-150) ypos 64 xsize 300 ysize 6
        add Solid(_FG)   xpos (SW//2-150) ypos 64 xsize _bw ysize 6
        text "TUTORIAL" xpos (SW//2-150) ypos 74 size 12 color _DASH

    if _h.dead:
        if getattr(_h, "_explode_t", 0.0) > 0:
            # 爆炸动画：画面闪白 + 睦字乱码
            python:
                _exp_a  = getattr(_h, "_explode_t", 0.0) / 0.7
                _glitch_chars = ["睦","X","✕","#","睦","!","陸","@","睦"]
                import random as _rnd2
                _exp_ch = _rnd2.choice(_glitch_chars)
            add Transform(Solid("#FFFFFF"), alpha=min(0.95, _exp_a)) xpos 0 ypos 0 xsize SW ysize SH
            text _exp_ch xpos 580 ypos 260 size 120 color "#FF0000"
        else:
            # 弹窗
            add Solid(_BG) alpha 0.88
            add Solid("#1A0000") xpos 340 ypos 220 xsize 600 ysize 260
            add Solid("#CC2222") xpos 340 ypos 220 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 476 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 220 xsize 4 ysize 260
            add Solid("#CC2222") xpos 936 ypos 220 xsize 4 ysize 260
            text "睦 的 压 力 爆 炸 了 ！" xpos 420 ypos 248 size 32 color "#FF4444"
            add Solid("#FFFFFF") xpos 360 ypos 292 xsize 560 ysize 1
            if CUKES.can_revive:
                python:
                    _rv_cost = "∞" if DIFF.can_revive_free else ("🥒×%d" % DIFF.revive_cost)
                # 复活按钮
                add Solid("#002200") xpos 370 ypos 308 xsize 240 ysize 80
                add Solid("#00AA44") xpos 370 ypos 308 xsize 240 ysize 3
                text "[[F]]  复活" xpos 418 ypos 322 size 26 color "#00FF88"
                text _rv_cost xpos 440 ypos 358 size 18 color "#AAFFAA"
            # 重新开始按钮
            add Solid("#1A1A00") xpos 670 ypos 308 xsize 240 ysize 80
            add Solid("#AAAA00") xpos 670 ypos 308 xsize 240 ysize 3
            text "[[R]]  重试" xpos 714 ypos 322 size 26 color "#FFFF44"
            text "重新开始" xpos 692 ypos 358 size 15 color "#AAAAAA"
            # 返回标题
            text "[[Q]]  返回标题" xpos 560 ypos 408 size 20 color "#555555"

    key "K_SPACE"     action Function(_h.do_jump)
    key "K_UP"        action Function(_h.do_jump)
    key "K_x"         action Function(_h.do_jump)
    key "K_w"         action Function(_h.do_jump)
    key "mousedown_1" action Function(lambda: None if (getattr(GM._h, 'mortis_phase', 0) == 3) else GM._h.do_jump())
    key "K_LSHIFT"    action Function(toggle_invert)
    key "K_RSHIFT"    action Function(toggle_invert)
    key "K_r"         action Function(GM.retry_current)
    key "K_q"         action [Function(_quit_to_title), Jump("game_center_start")]


################################################################################
#  竖版 2D 弹幕
################################################################################
screen scr_v2runner():
    style_prefix "mr"
    timer 0.016 repeat True action Function(_v2_move_tick)

    python:
        _v2    = GM._v2
        _label = {
            "tut_v2": "Round 1  教程",
            "r2_v2":  "Round 2",
            "r3_v2":  "Round 3  — 丰川祥子",
        }.get(GM.phase, "")
        _bsn   = list(_v2.bullets)
        _ftn   = list(_v2.float_texts)
        _csn   = list(_v2.cukes)
        _szn   = list(_v2.safe_zones)
        _ax    = V2_AREA_X
        _aw    = V2_AREA_W
        _vpx   = int(_ax + _v2.px - V2_PW // 2)
        _vpy   = int(_v2.py - V2_PH // 2)
        _pchar_v2  = PRESSURE.get_char()
        _shx_v2    = int(PRESSURE.shake_x)
        _shy_v2    = int(PRESSURE.shake_y)

    add Solid("#000000")
    add Solid("#333333") xpos (_ax-3) ypos 0 xsize 3 ysize SH
    add Solid("#333333") xpos (_ax+_aw) ypos 0 xsize 3 ysize SH
    add Solid("#0D0D0D") xpos _ax ypos 0 xsize _aw ysize SH

    # 网格横线
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 0   xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 50  xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 100 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 150 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 200 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 250 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 300 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 350 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 400 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 450 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 500 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 550 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 600 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 650 xsize _aw ysize 1
    add Solid("#FFFFFF") alpha 0.03 xpos _ax ypos 700 xsize _aw ysize 1

    # 祥子伪安全区已废弃——不渲染

    # 子弹
    for _b in _bsn:
        add Solid("#FFFFFF") xpos int(_ax + _b.x) ypos int(_b.y) xsize _b.w ysize _b.h

    # 黄瓜
    for _c in _csn:
        text "🥒" xpos int(_ax + _c.x) ypos int(_c.y) size 22 color "#FFFFFF"

    # 玩家（祥子Boss战中用睦的代表色#779977）
    python:
        _v2_p_col = "#779977" if GM.phase == "r3_v2" else "#FFFFFF"
        _v2_p_txt = "#000000"
    add Solid(_v2_p_col) xpos (_vpx+_shx_v2) ypos (_vpy+_shy_v2) xsize V2_PW ysize V2_PH
    text _pchar_v2 xpos (_vpx+_shx_v2) ypos (_vpy+_shy_v2) size 36 color _v2_p_txt
    add Solid("#000000") xpos int(_ax + _v2.px - 5) ypos int(_v2.py - 5) xsize 10 ysize 10

    # 擦弹闪光（边缘）
    if _v2.graze_flash > 0:
        add Transform(Solid("#FFFFFF"), alpha=(_v2.graze_flash / 0.12 * 0.3)) xpos _ax ypos 0 xsize 3 ysize SH
        add Transform(Solid("#FFFFFF"), alpha=(_v2.graze_flash / 0.12 * 0.3)) xpos (_ax+_aw) ypos 0 xsize 3 ysize SH

    # 飘字（白底背景前先不渲染，黑祥阶段在r3_v2块之后统一渲染）
    if GM.phase != "r3_v2":
        for _ft in _ftn:
            add Transform(Text(_ft.text, size=_ft.size, color=_ft.color), alpha=_ft.alpha) xpos int(_ax + _ft.x) ypos int(_ft.y + 80)

    # 断绝大招演出
    if _v2.bomb_active:
        if _v2.bomb_phase == 0:
            add Solid("#FFFFFF") alpha 0.95
        elif _v2.bomb_phase == 1:
            add Solid("#000000")
            # NOTE: 原日文台词「バンド、楽しいって思ったこと一度もない」
            # run.otf 不含日文字形；如要显示日文请在 game/ 目录加入日文字体
            # 并在 text 标签加 font="your_japanese_font.ttf" 参数
            text "乐队这件事……" xpos 380 ypos 240 size 50 color "#FFFFFF"
            text "我从来没觉得快乐过" xpos 200 ypos 310 size 50 color "#FFFFFF"
            text "— 若叶睦" xpos 820 ypos 390 size 28 color "#888888"
        elif _v2.bomb_phase == 2:
            add Transform(Solid("#FFFFFF"), alpha=max(0.0, 1.0 - (_v2.bomb_t - 1.1) / 0.9)) xpos 0 ypos 0 xsize SW ysize SH

    # HUD
    add Solid("#000000") alpha 0.75 xpos 0 ypos 0 xsize SW ysize 52
    text _label xpos 20 ypos 14 size 18 color "#777777"
    text "WAVE" xpos (SW-200) ypos 8 size 16 color "#666666"
    text "%d" % _v2.wave xpos (SW-140) ypos 10 size 30 color "#FFFFFF"
    # Boss战时中央黄瓜数与boss名字重叠，boss战中隐藏（guide panel里已有显示）
    if not (GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False)):
        # r3_v2时黄瓜数显示在格子区标题旁
        if GM.phase != "r3_v2":
            text "🥒×%d" % CUKES.collected xpos (SW//2-30) ypos 10 size 18 color "#FFFFFF"
    if CUKES.can_revive:
        python:
            _v2_rv_s = "[[F]]复活∞" if DIFF.can_revive_free else ("[[F]]复活🥒×%d" % DIFF.revive_cost)
        text _v2_rv_s xpos (SW//2+50) ypos 12 size 14 color "#FFFFFF"
    # 擦弹槽
    if _v2.graze_bar > 0:
        python:
            _gb = int(120 * _v2.graze_bar / 100.0)
        add Solid("#333333") xpos (_ax-3) ypos (SH-18) xsize 120 ysize 10
        add Solid("#FFFFFF") xpos (_ax-3) ypos (SH-18) xsize _gb ysize 10
        text "断绝" xpos (_ax-3) ypos (SH-32) size 12 color "#AAAAAA"
    if CUKES.can_bomb and _v2.graze_bar >= 100.0:
        text "[[B]] 大招 就绪！" xpos 20 ypos (SH-50) size 16 color "#FFFFAA"
    elif CUKES.can_bomb:
        text "[[B]] 大招 (擦弹槽未满)" xpos 20 ypos (SH-50) size 14 color "#888866"

    if GM.phase == "tut_v2":
        python:
            _tp = min(_v2.phase_timer / GM.TUT_V2_DUR, 1.0)
            _bw = int(260 * _tp)
        add Solid("#333333") xpos (SW//2-130) ypos 58 xsize 260 ysize 8
        add Solid("#FFFFFF") xpos (SW//2-130) ypos 58 xsize _bw ysize 8

    # ── 祥子 Boss HUD + 分屏渲染（r3_v2 专属）─────────────
    if GM.phase == "r3_v2":
        python:
            _sb2    = _v2.sakiko_boss
            _sb2_fts= list(_sb2.float_texts) if _sb2.active else []
            _V2X    = V2_AREA_X
            _V2W    = V2_AREA_W
            _BOUND  = int(V2_AREA_H * 0.70)   # 分界线 y 坐标
            _GCW    = _V2W // _sb2.GRID_W      # 单格宽度
            _GCH    = int(V2_AREA_H * 0.30) // _sb2.GRID_H  # 单格高度
            _GRID_Y = _BOUND                   # 推箱子区起始y

        if _sb2.active:
            # ── 全局主题色：白祥=黑底白字，黑祥=白底黑字 ──
            python:
                _sak_is_p2   = (_sb2.phase == 2)
                _sak_bg      = "#FFFFFF" if _sak_is_p2 else "#000000"
                _sak_fg      = "#000000" if _sak_is_p2 else "#FFFFFF"
                _sak_name    = "丰川祥子"
                _sak_subtitle= "— 黑 祥 —" if _sak_is_p2 else "— 白 祥 —"
            # 弹幕区背景覆盖（过渡动画 + 黑祥白底）
            python:
                _trans_prog = getattr(_sb2, '_trans_t', 0.0)     # 0~1
                _white_alpha = _trans_prog if _trans_prog > 0 else (1.0 if _sak_is_p2 else 0.0)
            if _white_alpha > 0:
                add Transform(Solid("#EEEEEE"), alpha=_white_alpha) xpos V2_AREA_X ypos 0 xsize V2_AREA_W ysize SH
            if _sak_is_p2 or _trans_prog > 0.5:
                # 重新渲染子弹为黑色
                for _b2p in _bsn:
                    python:
                        _b2_alpha = min(1.0, (_trans_prog - 0.4) / 0.4) if _trans_prog > 0 else 1.0
                    add Transform(Solid("#222222"), alpha=max(0.0, _b2_alpha)) xpos int(V2_AREA_X + _b2p.x) ypos int(_b2p.y) xsize _b2p.w ysize _b2p.h
            if _sak_is_p2 or _trans_prog > 0.3:
                # 重绘玩家（深色轮廓保证白底可见）
                python:
                    _vpx_r = int(V2_AREA_X + _v2.px - V2_PW // 2) + _shx_v2
                    _vpy_r = int(_v2.py - V2_PH // 2) + _shy_v2
                    _p_border_a = min(1.0, _trans_prog / 0.4) if _trans_prog > 0 else 1.0
                add Transform(Solid("#334433"), alpha=_p_border_a) xpos (_vpx_r - 2) ypos (_vpy_r - 2) xsize (V2_PW + 4) ysize (V2_PH + 4)
                add Transform(Solid("#779977"), alpha=_p_border_a) xpos _vpx_r ypos _vpy_r xsize V2_PW ysize V2_PH
                text _pchar_v2 xpos _vpx_r ypos _vpy_r size 36 color "#000000"
                add Solid("#112211") xpos int(V2_AREA_X + _v2.px - 5 + _shx_v2) ypos int(_v2.py - 5 + _shy_v2) xsize 10 ysize 10
            # 祥子名字（一阶段跟随sakiko_x移动）
            python:
                _sak_nx = V2_AREA_X + int(_sb2.sakiko_x) - 30
                _sak_nx = max(V2_AREA_X, min(V2_AREA_X + V2_AREA_W - 80, _sak_nx))
                _sak_hit_range_a = 0.5 + 0.4 * math.sin(_v2.phase_timer * 6.0)
            if _sb2.phase == 1:
                # 白祥名字跟随 sakiko_x，假动作时变红
                python:
                    _fake_a = getattr(_sb2, '_fake_flash', 0.0)
                    _p1_name_col = "#FF4444" if _fake_a > 0 else _sak_fg
                text _sak_name xpos _sak_nx ypos 12 size 26 color _p1_name_col
                text _sak_subtitle xpos (_sak_nx + 4) ypos 42 size 14 color _p1_name_col
                if _fake_a > 0:
                    text "！" xpos (_sak_nx + 10) ypos 65 size 40 color "#FF4444"
            else:
                # 黑祥名字跟随 sakiko_x，假动作时变红
                python:
                    _sak2_nx = V2_AREA_X + int(_sb2.sakiko_x) - 30
                    _sak2_nx = max(V2_AREA_X, min(V2_AREA_X + V2_AREA_W - 80, _sak2_nx))
                    _p2_fl   = getattr(_sb2, '_p2_fake_fl', 0.0)
                    _sak2_col = "#FF3333" if _p2_fl > 0 else _sak_fg
                text _sak_name xpos _sak2_nx ypos 12 size 26 color _sak2_col
                text _sak_subtitle xpos (_sak2_nx + 4) ypos 42 size 14 color _sak2_col

            if _sb2.phase == 1:
                # ── 左侧走格子区（左半屏） ───────────────────
                python:
                    _GX    = 20
                    _GY    = 70
                    _GW    = V2_AREA_X - 40
                    _GH    = SH - _GY - 90    # 底部留90px给大招提示和操作说明
                    _GCW2  = _GW // _sb2.GRID_W
                    _GCH2  = _GH // _sb2.GRID_H
                    _flash_a = max(0.0, 1.0 - getattr(_sb2, '_beam_t', 0.0) / 1.2) if _sb2._beam_t > 0 else 0.0
                # 格子区背景
                add Solid("#111111") xpos _GX ypos _GY xsize _GW ysize _GH
                # 外框
                add Solid("#444444") xpos _GX ypos _GY xsize _GW ysize 2
                add Solid("#444444") xpos _GX ypos (_GY+_GH) xsize _GW ysize 2
                add Solid("#444444") xpos _GX ypos _GY xsize 2 ysize _GH
                add Solid("#444444") xpos (_GX+_GW) ypos _GY xsize 2 ysize _GH
                # 竖格线
                for _gi in range(1, _sb2.GRID_W):
                    python:
                        _gx2 = _GX + _gi * _GCW2
                    add Solid("#333333") xpos _gx2 ypos _GY xsize 1 ysize _GH
                # 横格线
                for _gj in range(1, _sb2.GRID_H):
                    python:
                        _gy2 = _GY + _gj * _GCH2
                    add Solid("#333333") xpos _GX ypos _gy2 xsize _GW ysize 1
                # 危险红块
                for _hz in _sb2.hazards:
                    python:
                        _hx = _GX + _hz[1] * _GCW2 + 3
                        _hy = _GY + _hz[0] * _GCH2 + 3
                    add Solid("#AA0000") xpos _hx ypos _hy xsize (_GCW2-6) ysize (_GCH2-6)
                    add Solid("#FF3333") alpha 0.4 xpos (_hx+4) ypos (_hy+4) xsize 8 ysize 8
                # 蓝色必经格（闪烁）
                python:
                    _blue_a = 0.6 + 0.3 * math.sin(_v2.phase_timer * 5.0)
                    _bx2 = _GX + _sb2.blue_cell[1] * _GCW2 + 3
                    _by2 = _GY + _sb2.blue_cell[0] * _GCH2 + 3
                    _blue_txt_col = "#FFFFFF" if _sb2.blue_visited else "#000000"
                    _blue_label   = "✓必经" if _sb2.blue_visited else "必经"
                    _blue_bg      = "#0055AA" if not _sb2.blue_visited else "#003366"
                add Transform(Solid(_blue_bg), alpha=_blue_a) xpos _bx2 ypos _by2 xsize (_GCW2-6) ysize (_GCH2-6)
                add Solid("#44AAFF") xpos _bx2 ypos _by2 xsize (_GCW2-6) ysize 3
                add Solid("#44AAFF") xpos _bx2 ypos (_by2+_GCH2-9) xsize (_GCW2-6) ysize 3
                add Solid("#44AAFF") xpos _bx2 ypos _by2 xsize 3 ysize (_GCH2-6)
                add Solid("#44AAFF") xpos (_bx2+_GCW2-9) ypos _by2 xsize 3 ysize (_GCH2-6)
                text _blue_label xpos (_bx2 + _GCW2//2 - 14) ypos (_by2 + _GCH2//4) size 12 color _blue_txt_col
                # 蓝色必经格2（橙蓝色区分）
                python:
                    _blue2_a = 0.6 + 0.3 * math.sin(_v2.phase_timer * 5.0 + 1.5)
                    _bx3 = _GX + _sb2.blue_cell2[1] * _GCW2 + 3
                    _by3 = _GY + _sb2.blue_cell2[0] * _GCH2 + 3
                    _blue2_txt_col = "#FFFFFF" if _sb2.blue_visited2 else "#000000"
                    _blue2_label   = "✓必经2" if _sb2.blue_visited2 else "必经2"
                    _blue2_bg      = "#005588" if not _sb2.blue_visited2 else "#003355"
                add Transform(Solid(_blue2_bg), alpha=_blue2_a) xpos _bx3 ypos _by3 xsize (_GCW2-6) ysize (_GCH2-6)
                add Solid("#2288CC") xpos _bx3 ypos _by3 xsize (_GCW2-6) ysize 3
                add Solid("#2288CC") xpos _bx3 ypos (_by3+_GCH2-9) xsize (_GCW2-6) ysize 3
                add Solid("#2288CC") xpos _bx3 ypos _by3 xsize 3 ysize (_GCH2-6)
                add Solid("#2288CC") xpos (_bx3+_GCW2-9) ypos _by3 xsize 3 ysize (_GCH2-6)
                text _blue2_label xpos (_bx3 + _GCW2//2 - 18) ypos (_by3 + _GCH2//4) size 11 color _blue2_txt_col
                # 蓝色必经格3（仅低血量激活时渲染，橙红色区分）
                if getattr(_sb2, '_three_blue_active', False) and _sb2.blue_cell3 != [-1,-1]:
                    python:
                        _blue3_a = 0.6 + 0.3 * math.sin(_v2.phase_timer * 5.0 + 3.0)
                        _bx4 = _GX + _sb2.blue_cell3[1] * _GCW2 + 3
                        _by4 = _GY + _sb2.blue_cell3[0] * _GCH2 + 3
                        _blue3_txt_col = "#FFFFFF" if _sb2.blue_visited3 else "#000000"
                        _blue3_label   = "✓必经3" if _sb2.blue_visited3 else "必经3"
                        _blue3_bg      = "#885500" if not _sb2.blue_visited3 else "#553300"
                    add Transform(Solid(_blue3_bg), alpha=_blue3_a) xpos _bx4 ypos _by4 xsize (_GCW2-6) ysize (_GCH2-6)
                    add Solid("#FFAA33") xpos _bx4 ypos _by4 xsize (_GCW2-6) ysize 3
                    add Solid("#FFAA33") xpos _bx4 ypos (_by4+_GCH2-9) xsize (_GCW2-6) ysize 3
                    add Solid("#FFAA33") xpos _bx4 ypos _by4 xsize 3 ysize (_GCH2-6)
                    add Solid("#FFAA33") xpos (_bx4+_GCW2-9) ypos _by4 xsize 3 ysize (_GCH2-6)
                    text _blue3_label xpos (_bx4 + _GCW2//2 - 18) ypos (_by4 + _GCH2//4) size 11 color _blue3_txt_col
                # 玩家路径连线（每两个相邻节点之间画横/竖线）
                python:
                    _ph = getattr(_sb2, 'path_history', [])
                for _pi in range(len(_ph) - 1):
                    python:
                        _pa = _ph[_pi];   _pb_cell = _ph[_pi+1]
                        _pax = _GX + _pa[1] * _GCW2 + _GCW2 // 2
                        _pay = _GY + _pa[0] * _GCH2 + _GCH2 // 2
                        _pbx = _GX + _pb_cell[1] * _GCW2 + _GCW2 // 2
                        _pby = _GY + _pb_cell[0] * _GCH2 + _GCH2 // 2
                        _p_lx = min(_pax, _pbx); _p_ly = min(_pay, _pby)
                        _p_lw = max(3, abs(_pbx - _pax)); _p_lh = max(3, abs(_pby - _pay))
                        _p_trail_a = 0.4 + 0.35 * (_pi + 1) / max(1, len(_ph))
                    add Transform(Solid("#00CCFF"), alpha=_p_trail_a) xpos _p_lx ypos _p_ly xsize _p_lw ysize _p_lh
                # 目标金块（闪烁）
                python:
                    _slot_a = 0.55 + 0.35 * math.sin(_v2.phase_timer * 4.0)
                    _sx2 = _GX + _sb2.grid_slot[1] * _GCW2 + 3
                    _sy2 = _GY + _sb2.grid_slot[0] * _GCH2 + 3
                add Transform(Solid("#FFFF44"), alpha=_slot_a) xpos _sx2 ypos _sy2 xsize (_GCW2-6) ysize (_GCH2-6)
                text "目标" xpos (_sx2 + _GCW2//2 - 14) ypos (_sy2 + _GCH2//4) size 13 color "#000000"
                # 游标（绿色实心+亮边框）
                python:
                    _cx2 = _GX + _sb2.grid_cursor[1] * _GCW2 + 3
                    _cy2 = _GY + _sb2.grid_cursor[0] * _GCH2 + 3
                add Solid("#003322") xpos _cx2 ypos _cy2 xsize (_GCW2-6) ysize (_GCH2-6)
                add Solid("#00FF88") xpos _cx2 ypos _cy2 xsize (_GCW2-6) ysize 3
                add Solid("#00FF88") xpos _cx2 ypos (_cy2+_GCH2-9) xsize (_GCW2-6) ysize 3
                add Solid("#00FF88") xpos _cx2 ypos _cy2 xsize 3 ysize (_GCH2-6)
                add Solid("#00FF88") xpos (_cx2+_GCW2-9) ypos _cy2 xsize 3 ysize (_GCH2-6)
                # 操作说明 + Boss HP
                text "WASD — 踩蓝格再踩金块！" xpos _GX ypos (_GY+_GH+4) size 11 color "#AAAAAA"
                text "瞄准祥子位置再发射！" xpos _GX ypos (_GY+_GH+20) size 11 color "#888888"
                python:
                    _hp_str = "白祥 HP: " + "█" * _sb2.p1_hp + "░" * (_sb2.P1_MAX_HP - _sb2.p1_hp)
                text _hp_str xpos _GX ypos (_GY-22) size 16 color "#FF8888"
                # 分界竖线（格子区和弹幕区之间）
                add Solid("#555555") xpos (V2_AREA_X-2) ypos 0 xsize 2 ysize SH

            elif _sb2.phase == 2:
                # ── 阶段二：打字界面 ─────────────────────
                # 背景词语（浮现单词）
                if _sb2._cur_word:
                    python:
                        _wlen    = len(_sb2._cur_word)
                        _typed   = _sb2._typed
                        _wrem    = _sb2._cur_word[len(_typed):]
                        _w_cx    = _V2X + _V2W//2
                    # 已打部分（绿色）
                    if _typed:
                        text _typed xpos (_w_cx - len(_sb2._cur_word)*18) ypos (SH//2-40) size 48 color ("#007733" if _sak_is_p2 else "#00FF88")
                    # 未打部分（黑祥白底时用深色）
                    add Transform(Text(_wrem, size=48, color=_sak_fg), alpha=0.9) xpos (_w_cx - len(_wrem)*18 + len(_typed)*18) ypos (SH//2-40)
                    # 下一个字母提示
                    if _wrem:
                        python:
                            _next_ch = _wrem[0]
                        text _next_ch xpos (_w_cx - len(_wrem)*18 + len(_typed)*18 - 4) ypos (SH//2+20) size 26 color ("#AA8800" if _sak_is_p2 else "#FFFF44")
                    # 拼写进度横条
                    python:
                        _prog_total = len(_sb2._cur_word)
                        _prog_done  = len(_sb2._typed)
                        _prog_bw    = int(200 * _prog_done / max(1, _prog_total))
                    add Solid("#333333") xpos (_w_cx - 100) ypos (SH//2+20) xsize 200 ysize 6
                    if _prog_bw > 0:
                        add Solid("#00DD55") xpos (_w_cx - 100) ypos (SH//2+20) xsize _prog_bw ysize 6
                    # Boss HP
                    python:
                        _hp2_str = "Oblivionis  " + "█" * _sb2.p2_hp + "░" * (_sb2.P2_MAX_HP - _sb2.p2_hp)
                    text _hp2_str xpos (SW//2-110) ypos (SH-40) size 16 color "#FF4444"
                    text "左手键盘打字 — 每字母消弹  打完单词重击！" xpos (SW//2-180) ypos (SH-22) size 13 color "#AAAAAA"

                # 防空炮气浪动画（大小按duration区分：0.45=小，0.7=大）
                for _bl in list(_sb2._blast_anim):
                    python:
                        _bl_max_r = 80 if _bl[2] > 0.5 else 50
                        _bl_dur   = 0.7 if _bl[2] > 0.5 else 0.45
                        _bl_prog  = max(0.01, 1.0 - _bl[2]/_bl_dur)
                        _bl_r = int(_bl_max_r * _bl_prog)
                        _bl_a = (1.0 - _bl_prog) * 0.7
                        _bl_x = int(_V2X + _bl[0] - _bl_r)
                        _bl_y = int(_bl[1] - _bl_r)
                    add Transform(Solid("#AAFFAA"), alpha=_bl_a) xpos _bl_x ypos _bl_y xsize (_bl_r*2) ysize (_bl_r*2)
                # ── 右侧操作说明面板（黑祥专属，x>880空余区域）──
                python:
                    _rp_x = V2_AREA_X + V2_AREA_W + 20   # 880+20=900
                    _rp_w = SW - _rp_x - 10               # ~370px
                    _rp_hits = getattr(_sb2, '_p2_hits', 0)
                    _rp_blink = 0.6 + 0.4 * math.sin(_v2.phase_timer * 3.0)
                # 面板背景框
                add Solid("#111111") xpos _rp_x ypos 80 xsize _rp_w ysize 440
                add Solid("#333333") xpos _rp_x ypos 80 xsize _rp_w ysize 2
                add Solid("#333333") xpos _rp_x ypos 520 xsize _rp_w ysize 2
                add Solid("#333333") xpos _rp_x ypos 80 xsize 2 ysize 440
                add Solid("#333333") xpos (SW - 12) ypos 80 xsize 2 ysize 440
                # 标题
                text "— 黑 祥 作 战 —" xpos (_rp_x + 20) ypos 90 size 18 color "#AAAAAA"
                add Solid("#444444") xpos (_rp_x + 10) ypos 116 xsize (_rp_w - 20) ysize 1
                # 操作说明：打字
                text "左手键盘输入英文" xpos (_rp_x + 14) ypos 126 size 15 color "#FFFFFF"
                text "打对字母→积累进度" xpos (_rp_x + 14) ypos 148 size 13 color "#BBBBBB"
                text "打完单词→发射激光！" xpos (_rp_x + 14) ypos 168 size 13 color "#BBBBBB"
                text "激光须命中祥子才扣血！" xpos (_rp_x + 14) ypos 188 size 13 color "#FFAA44"
                add Solid("#444444") xpos (_rp_x + 10) ypos 192 xsize (_rp_w - 20) ysize 1
                # 当前单词提示
                text "当前词：" xpos (_rp_x + 14) ypos 200 size 13 color "#888888"
                if _sb2._cur_word:
                    python:
                        _rp_typed  = _sb2._typed
                        _rp_remain = _sb2._cur_word[len(_rp_typed):]
                    if _rp_typed:
                        text _rp_typed xpos (_rp_x + 14) ypos 220 size 28 color "#779977"
                    add Transform(Text(_rp_remain, size=28, color="#FFFFFF"), alpha=0.9) xpos (_rp_x + 14 + len(_sb2._typed)*17) ypos 220
                    if _rp_remain:
                        add Transform(Text(_rp_remain[0], size=22, color="#FFFF44"), alpha=_rp_blink) xpos (_rp_x + 14 + len(_sb2._typed)*17 - 2) ypos 256
                        text "← 下一个" xpos (_rp_x + 14 + len(_sb2._typed)*17 + 16) ypos 258 size 12 color "#666666"
                add Solid("#444444") xpos (_rp_x + 10) ypos 296 xsize (_rp_w - 20) ysize 1
                # 进度
                text "击杀进度：%d / %d" % (_rp_hits, _sb2.P2_MAX_HP) xpos (_rp_x + 14) ypos 304 size 14 color "#CCCCCC"
                python:
                    _rp_hp_str = "█" * _sb2.p2_hp + "░" * (_sb2.P2_MAX_HP - _sb2.p2_hp)
                text _rp_hp_str xpos (_rp_x + 14) ypos 326 size 18 color "#FF4444"
                add Solid("#444444") xpos (_rp_x + 10) ypos 356 xsize (_rp_w - 20) ysize 1
                # 瞄准提示
                text "对准祥子 再完成单词！" xpos (_rp_x + 14) ypos 364 size 13 color "#779977"
                text "打空了不扣血 重新瞄准！" xpos (_rp_x + 14) ypos 384 size 13 color "#888888"
                text "压力满100 → 爆炸！" xpos (_rp_x + 14) ypos 404 size 13 color "#AA3333"
                # 激光提示（打完单词时闪烁）
                if _sb2._beam_t > 0 and _sb2.phase == 2:
                    python:
                        _laser_a = min(1.0, _sb2._beam_t / 0.4)
                    add Transform(Solid("#779977"), alpha=_laser_a * 0.3) xpos _rp_x ypos 80 xsize _rp_w ysize 440
                    add Transform(Text("⚡ 激光命中！", size=22, color="#779977"), alpha=_laser_a) xpos (_rp_x + 20) ypos 410

            # 激光动画：用🥒 emoji垂直排列代替色块
            if _sb2._beam_t > 0:
                python:
                    _beam_a  = min(1.0, _sb2._beam_t / 0.4) * 0.95
                    _beam_bx = V2_AREA_X + int(_v2.px) - 16
                    _beam_bx = max(V2_AREA_X, min(V2_AREA_X + V2_AREA_W - 32, _beam_bx))
                    _cuke_size = 28
                    _cuke_gap  = 30
                    _cuke_count = SH // _cuke_gap + 2
                for _ci in range(_cuke_count):
                    add Transform(Text("🥒", size=_cuke_size), alpha=_beam_a) xpos _beam_bx ypos (_ci * _cuke_gap - _cuke_gap)

            # 黑祥胜利淡出（祥子名字逐渐消失）
            if _sb2.phase == 2 and getattr(_sb2, '_p2_clear_t', 0.0) > 0:
                python:
                    _fade_t   = _sb2._p2_clear_t
                    _fade_a   = max(0.0, 1.0 - _fade_t / 2.0)
                    _sak_nx_f = V2_AREA_X + int(_sb2.sakiko_x) - 30
                    _sak_nx_f = max(V2_AREA_X, min(V2_AREA_X + V2_AREA_W - 80, _sak_nx_f))
                add Transform(Text("丰川祥子", size=26, color=_sak_fg), alpha=_fade_a) xpos _sak_nx_f ypos 12
                add Transform(Text("— 黑 祥 —", size=14, color=_sak_fg), alpha=_fade_a) xpos (_sak_nx_f + 4) ypos 42
                # 白色化效果（背景渐白）
                add Transform(Solid("#FFFFFF"), alpha=min(0.7, _fade_t * 0.35)) xpos _V2X ypos 0 xsize _V2W ysize SH

            # ── 乱码扰视词渲染（p2_hp≤2，半透明大字横穿）──
            if _sb2.phase == 2 and _sb2.p2_hp <= (4 if DIFF.current >= DIFF.HARD else 2):
                for _jw in getattr(_sb2, '_junk_words', []):
                    python:
                        _jw_screen_x = V2_AREA_X + int(_jw[0])
                        _jw_col = "#AA0000" if _jw[3] in ("DESPAIR","HOPELESS","崩壊","絶望","WORTHLESS","GIVE UP","消えろ","失格","あなたには") else "#004400"
                    add Transform(Text(_jw[3], size=int(_jw[5]), color=_jw_col), alpha=_jw[4]) xpos _jw_screen_x ypos int(_jw[1])

            # Boss飘字
            for _sbft2 in _sb2_fts:
                add Transform(Text(_sbft2.text, size=_sbft2.size, color=_sbft2.color), alpha=_sbft2.alpha) xpos int(_V2X + _sbft2.x) ypos int(_sbft2.y)

    if _v2.dead:
        if getattr(_v2, "_explode_t", 0.0) > 0:
            python:
                _exp_a2 = getattr(_v2, "_explode_t", 0.0) / 0.7
                import random as _rnd3
                _exp_ch2 = _rnd3.choice(["睦","X","✕","#","睦","!","陸","@"])
            add Transform(Solid("#FFFFFF"), alpha=min(0.95, _exp_a2)) xpos 0 ypos 0 xsize SW ysize SH
            text _exp_ch2 xpos 580 ypos 260 size 120 color "#FF0000"
        else:
            add Solid("#000000") alpha 0.88
            add Solid("#1A0000") xpos 340 ypos 220 xsize 600 ysize 260
            add Solid("#CC2222") xpos 340 ypos 220 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 476 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 220 xsize 4 ysize 260
            add Solid("#CC2222") xpos 936 ypos 220 xsize 4 ysize 260
            text "睦 的 压 力 爆 炸 了 ！" xpos 420 ypos 248 size 32 color "#FF4444"
            add Solid("#FFFFFF") xpos 360 ypos 292 xsize 560 ysize 1
            if CUKES.can_revive:
                python:
                    _rv_cost2 = "∞" if DIFF.can_revive_free else ("🥒×%d" % DIFF.revive_cost)
                add Solid("#002200") xpos 370 ypos 308 xsize 240 ysize 80
                add Solid("#00AA44") xpos 370 ypos 308 xsize 240 ysize 3
                text "[[F]]  复活" xpos 418 ypos 322 size 26 color "#00FF88"
                text _rv_cost2 xpos 440 ypos 358 size 18 color "#AAFFAA"
            add Solid("#1A1A00") xpos 670 ypos 308 xsize 240 ysize 80
            add Solid("#AAAA00") xpos 670 ypos 308 xsize 240 ysize 3
            text "[[R]]  重试" xpos 714 ypos 322 size 26 color "#FFFF44"
            text "重新开始" xpos 692 ypos 358 size 15 color "#AAAAAA"
            text "[[Q]]  返回标题" xpos 560 ypos 408 size 20 color "#555555"

    # ── 压力槽 + 飘字：统一在最后渲染，保证覆盖在所有背景之上 ──
    python:
        _pw_v2   = int(120 * PRESSURE.value / 100.0)
        _pbar2_c = "#FF0000" if PRESSURE.value >= 80 else "#EE3333"
        _pbar2_a = (0.7 + 0.3 * math.sin(_v2.phase_timer * 14.0)) if PRESSURE.value >= 80 else 1.0
        _sak_is_p2_pb = (GM.phase == "r3_v2" and _v2.sakiko_boss.active and _v2.sakiko_boss.phase == 2)
        _pb_x = V2_AREA_X + V2_AREA_W - 126
    # 衬底（保证白底/黑底都可见）
    add Solid("#000000") alpha 0.65 xpos _pb_x ypos (SH-38) xsize 132 ysize 28
    add Solid("#330000") xpos (_pb_x+6) ypos (SH-22) xsize 120 ysize 12
    add Transform(Text("压力" if PRESSURE.value < 80 else "DANGER", size=12,
                       color=("#FF5555" if _sak_is_p2_pb else ("#FF3333" if PRESSURE.value >= 80 else "#CC5555"))),
                  alpha=_pbar2_a) xpos (_pb_x+6) ypos (SH-34)
    if _pw_v2 > 0:
        add Transform(Solid(_pbar2_c), alpha=_pbar2_a) xpos (_pb_x+6) ypos (SH-22) xsize _pw_v2 ysize 12
    # r3_v2阶段的飘字也在这里渲染（确保在白色背景之上）
    if GM.phase == "r3_v2":
        for _ft in _ftn:
            python:
                _ft_col = _ft.color
                # 黑祥白底时，白色飘字改成深色
                if _sak_is_p2_pb and _ft_col in ("#FFFFFF", "#EEEEEE", "#AAAAAA"):
                    _ft_col = "#222222"
            add Transform(Text(_ft.text, size=_ft.size, color=_ft_col), alpha=_ft.alpha) xpos int(_ax + _ft.x) ypos int(_ft.y + 80)

    # 祥子Boss推箱子：WASD键绑定（仅r3_v2 Phase1）
    if GM.phase == "r3_v2" and _v2.sakiko_boss.active and _v2.sakiko_boss.phase == 1:
        key "K_w" action Function(_v2.sakiko_boss.move_cursor, -1, 0)
        key "K_s" action Function(_v2.sakiko_boss.move_cursor,  1, 0)
        key "K_a" action Function(_v2.sakiko_boss.move_cursor,  0,-1)
        key "K_d" action Function(_v2.sakiko_boss.move_cursor,  0, 1)
        key "K_UP"    action Function(_v2.sakiko_boss.move_cursor, -1, 0)
        key "K_DOWN"  action Function(_v2.sakiko_boss.move_cursor,  1, 0)
        key "K_LEFT"  action Function(_v2.sakiko_boss.move_cursor,  0,-1)
        key "K_RIGHT" action Function(_v2.sakiko_boss.move_cursor,  0, 1)
    # 阶段二：字母键绑定（左手区 Q W E R T A S D F G Z X C V B）
    if GM.phase == "r3_v2" and _v2.sakiko_boss.active and _v2.sakiko_boss.phase == 2:
        key "K_q" action Function(_v2.sakiko_boss.type_key, "Q", _v2)
        key "K_w" action Function(_v2.sakiko_boss.type_key, "W", _v2)
        key "K_e" action Function(_v2.sakiko_boss.type_key, "E", _v2)
        key "K_r" action Function(_v2.sakiko_boss.type_key, "R", _v2)
        key "K_t" action Function(_v2.sakiko_boss.type_key, "T", _v2)
        key "K_a" action Function(_v2.sakiko_boss.type_key, "A", _v2)
        key "K_s" action Function(_v2.sakiko_boss.type_key, "S", _v2)
        key "K_d" action Function(_v2.sakiko_boss.type_key, "D", _v2)
        key "K_f" action Function(_v2.sakiko_boss.type_key, "F", _v2)
        key "K_g" action Function(_v2.sakiko_boss.type_key, "G", _v2)
        key "K_z" action Function(_v2.sakiko_boss.type_key, "Z", _v2)
        key "K_x" action Function(_v2.sakiko_boss.type_key, "X", _v2)
        key "K_c" action Function(_v2.sakiko_boss.type_key, "C", _v2)
        key "K_v" action Function(_v2.sakiko_boss.type_key, "V", _v2)
        key "K_b" action Function(_v2.sakiko_boss.type_key, "B", _v2)

    if not (GM.phase == "r3_v2" and _v2.sakiko_boss.active):
        key "K_b"     action Function(_v2.trigger_bomb)
    if not (GM.phase == "r3_v2" and _v2.sakiko_boss.active and _v2.sakiko_boss.phase == 2):
        key "K_r"     action Function(GM.retry_current)
    key "K_q"     action [Function(_quit_to_title), Jump("game_center_start")]


################################################################################
#  伪 3D 跑酷
################################################################################
screen scr_p3runner():
    style_prefix "mr"
    # 鼠标四方向控制：每帧 tick
    timer 0.016 repeat True action Function(_p3_move_tick)

    python:
        _p3    = GM._p3
        _label = {
            "tut_p3": "Round 1  教程",
            "r2_p3":  "Round 2  — 长崎爽世",
            "r3_p3":  "Round 3",
        }.get(GM.phase, "")
        _ftn   = list(_p3.float_texts)
        _osn   = sorted(list(_p3.obs), key=lambda o: o.y)
        # _cols已删除（崩塌系统移除）
        # _gates已删除（选项门移除）
        VPX    = int(p3_vp_x())
        VPY    = int(p3_vp_y())
        BOT    = int(getattr(_p3, '_bot_y', P3_BOT_Y))
        LW     = P3_LANE_W
        _is_pincer = getattr(_p3, '_boss_pincer', False)
        _pd    = _p3.depth         # 当前深度
        _pcx   = p3_player_cx(_p3.lane, _pd)
        _pcy   = p3_lane_y(_pd)
        # 玩家大小：夹击时固定为略小于正常底部大小（避免太小看不清）
        _psz_base = max(18, int(58 * _pd))
        _psz   = max(32, _psz_base) if _is_pincer else _psz_base
        _pchar_p3 = PRESSURE.get_char()
        _shx_p3   = int(PRESSURE.shake_x)
        _shy_p3   = int(PRESSURE.shake_y)

        # 预计算跑道面（48条横带）
        # Boss段背景变白时路面配色自动反转保持对比度
        _is_boss_pre = (GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False))
        _bg_w_pre    = getattr(_p3, "_bg_white", 0.0) if _is_boss_pre else 0.0
        _road = []
        _road_bands = 64 if _is_pincer else 48   # 夹击时延伸跑道，用更多横带
        for _ri in range(_road_bands):
            _zr  = (_ri + 1) / float(_road_bands)
            _zr0 = _ri       / float(_road_bands)
            _y1  = int(p3_lane_y(_zr))
            _y2  = int(p3_lane_y(_zr0))
            _hw  = int(LW * 3 / 2 * _zr)
            # 黑背景：近亮远暗；白背景：近暗远亮（始终和背景对比）
            _lum_dark  = int(30 + 80  * _zr)          # 黑背景版
            _lum_white = int(210 - 170 * _zr)         # 白背景版（近端深，远端浅）
            _lum = int(_lum_dark * (1 - _bg_w_pre) + _lum_white * _bg_w_pre)
            _col = "#{0:02X}{0:02X}{0:02X}".format(max(0, min(255, _lum)))
            _road.append((VPX - _hw, _y2, _hw * 2, max(1, _y1 - _y2), _col))

        # 跑道分割线（用_lane_count_f浮点，分割线位置平滑过渡）
        _n_lanes  = getattr(_p3, '_lane_count', P3_LANES)       # 整数，决定条数
        _n_lanes_f = getattr(_p3, '_lane_count_f', float(P3_LANES))  # 浮点，决定位置
        _divs = []
        for _st in range(20):
            _zr2  = (_st + 1) / 20.0
            _totw = LW * 3 * _zr2
            _lf2  = VPX - _totw / 2
            # 分割线条数用整数，位置用浮点n插值 → 切换时分割线平滑滑动
            for _ln2 in range(1, _n_lanes):
                _norm_div = _ln2 / _n_lanes_f
                _divs.append((int(_lf2 + _norm_div * _totw), int(p3_lane_y(_zr2))))

        # 崩塌视觉已删除

        # ── 障碍物预计算（近大远小 + 判定阶段着色）─────
        # z>0.82 → 警告(橙边)；z>0.90 → 危险(红边+红晕)；z>1.05 → 通过
        _DEPTH_PLAYER = _p3.DEPTH_MAX   # 1.0
        _obs_draw = []
        _hit_zone_lanes = []            # 当前帧处于判定区的道编号
        for _o in _osn:
            _oz   = _o.y
            if _oz < 0.07: continue
            _ocx  = p3_lane_cx(_o.x, _oz)
            _floor_y = int(p3_lane_y(_oz))
            _lane_w_at_z = (LW * 3 * _oz) / max(1.0, _n_lanes_f)
            _bsz  = max(8, int(_lane_w_at_z * 0.88))
            if _o.is_cucumber:
                _csz = max(12, int(_bsz * 0.65))
                _obs_draw.append(("cuke",
                    int(_ocx - _csz//2), _floor_y - _csz, _csz))
            else:
                # 判定阶段
                if _oz >= 0.90:
                    _stage = "danger"      # 红色，判定区
                    _hit_zone_lanes.append(_hit_lane)
                elif _oz >= 0.82:
                    _stage = "warn"        # 橙色，预警区
                else:
                    _stage = "normal"
                _hit_lane = int(_o.x * _n_lanes)
                _hit_lane = max(0, min(_n_lanes - 1, _hit_lane))
                _obs_draw.append(("obs",
                    int(_ocx - _bsz//2), _floor_y - _bsz, _bsz, _stage))

        # 道指示器（底部小方块，N道通用）
        _ind = []
        for _i in range(_n_lanes):
            _active = abs(_p3.lane - _i) < 0.5
            _ic = "#FFFFFF" if _active else "#333333"
            _norm_i = (_i + 0.5) / float(_n_lanes)
            _ind.append((int(p3_lane_cx(_norm_i, 1.0)) - 10, BOT + 20, _ic))

        # 深度指示条已删除（层级系统移除）

    # 背景：r2_p3 Boss段渐白，其余固定黑
    python:
        _is_boss_phase = (GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False))
        _bg_w   = getattr(_p3, "_bg_white", 0.0) if _is_boss_phase else 0.0
        _bg_lum = int(8 + 247 * _bg_w)
        _bg_hex = "#{0:02X}{0:02X}{0:02X}".format(_bg_lum)
    add Solid(_bg_hex)

    # 天空渐变
    add Solid("#FFFFFF") alpha 0.04 xpos 0 ypos 0   xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.03 xpos 0 ypos 27  xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.02 xpos 0 ypos 54  xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.02 xpos 0 ypos 81  xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.01 xpos 0 ypos 108 xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.01 xpos 0 ypos 135 xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.01 xpos 0 ypos 162 xsize SW ysize 27
    add Solid("#FFFFFF") alpha 0.01 xpos 0 ypos 189 xsize SW ysize 27

    # 消失点十字（VP摇摆时可见）
    if _p3._wobble_intensity > 0.1:
        add Transform(Solid("#FFFFFF"), alpha=min(0.6, _p3._wobble_intensity)) xpos (VPX-12) ypos VPY xsize 24 ysize 2
        add Transform(Solid("#FFFFFF"), alpha=min(0.6, _p3._wobble_intensity)) xpos VPX ypos (VPY-12) xsize 2 ysize 24

    # 跑道
    for (_rx, _ry, _rw, _rh, _rc) in _road:
        add Solid(_rc) xpos _rx ypos _ry xsize _rw ysize _rh



    # 分割线（Boss白背景时改为深色）
    python:
        _div_col = "#000000" if _bg_w > 0.5 else "#FFFFFF"
        _div_a   = 0.4
    for (_dx, _dy) in _divs:
        add Transform(Solid(_div_col), alpha=_div_a) xpos _dx ypos _dy xsize 2 ysize 5

    # 障碍物渲染（三阶段判定配色 + 白/黑背景自适应）
    python:
        _is_white_bg  = _bg_w > 0.5
        _cuke_col     = "#000000" if _is_white_bg else "#FFFFFF"
        _hud_txt_col  = "#222222" if _is_white_bg else "#FFFF44"   # HUD文字颜色，白背随背景反转
        _hud_dim_col  = "#555555" if _is_white_bg else "#BBBBBB"   # 次要HUD文字
        _p3_timer_sin = math.sin(_p3.phase_timer * 8.0)
    for _od in _obs_draw:
        if _od[0] == "cuke":
            text "🥒" xpos _od[1] ypos _od[2] size _od[3] color _cuke_col
        elif _od[0] == "obs":
            python:
                _stage   = _od[4] if len(_od) > 4 else "normal"
                _ox, _oy, _os = _od[1], _od[2], _od[3]
                # 填充色：正常=白/黑；预警=淡橙晕；危险=淡红晕
                if _stage == "danger":
                    _fill   = "#331111" if not _is_white_bg else "#FFCCCC"
                    _border = "#FF3333"
                    _bw     = max(2, _os // 8)   # 危险时边框加粗
                elif _stage == "warn":
                    _fill   = "#221400" if not _is_white_bg else "#FFF0E0"
                    _border = "#FF8833"
                    _bw     = max(2, _os // 12)
                else:
                    _fill   = "#000000" if _is_white_bg else "#FFFFFF"
                    _border = "#FFFFFF" if _is_white_bg else "#000000"
                    _bw     = 2
            add Solid(_fill)   xpos _ox ypos _oy xsize _os ysize _os
            add Solid(_border) xpos _ox ypos _oy xsize _os ysize _bw
            add Solid(_border) xpos _ox ypos (_oy+_os-_bw) xsize _os ysize _bw
            add Solid(_border) xpos _ox ypos _oy xsize _bw ysize _os
            add Solid(_border) xpos (_ox+_os-_bw) ypos _oy xsize _bw ysize _os

    # 判定线：玩家脚下，只在当前道有危险方块时闪烁
    python:
        _pcur_lane = int(round(_p3.lane))
        _show_hitline = _pcur_lane in _hit_zone_lanes and _p3._invincible_t <= 0
        _hl_alpha = (0.5 + 0.5 * _p3_timer_sin) * 0.85 if _show_hitline else 0.0
        _hl_col   = "#FF0000" if not _is_white_bg else "#CC0000"
        _hl_norm  = (_pcur_lane + 0.5) / float(getattr(_p3, '_lane_count', P3_LANES))
        _hl_cx    = int(p3_lane_cx(_hl_norm, 1.0))
        _hl_w     = max(30, int(LW * 3.0 / _n_lanes * 0.8))
        _hl_x     = _hl_cx - _hl_w // 2
    if _hl_alpha > 0.05:
        add Transform(Solid(_hl_col), alpha=_hl_alpha) xpos _hl_x ypos (BOT - 6) xsize _hl_w ysize 4

    # 玩家（深度决定大小和位置）
    python:
        _ppx = int(_pcx - _psz // 2) + _shx_p3
        _ppy = int(_pcy - _psz) + _shy_p3

    text _pchar_p3 xpos _ppx ypos _ppy size _psz color "#FFFFFF"

    # ── 后方障碍渲染（夹击阶段，从屏幕底部逼近，红色标识）────
    if _is_pincer:
        python:
            _back_list = list(getattr(_p3, 'back_obs', []))
            # 按z排序：z小的（靠近消失点）先画，z大的（靠近玩家）后画
            _back_list.sort(key=lambda o: -o.y)
        for _bo in _back_list:
            python:
                _boz    = _bo.y
                _bocx   = p3_lane_cx(_bo.x, _boz)
                _bof_y  = int(p3_lane_y(_boz))
                _back_lane_w = (LW * 3 * _boz) / max(1.0, _n_lanes_f)
                _bosiz  = max(8, int(_back_lane_w * 0.88))
                _box    = int(_bocx - _bosiz // 2)
                _boy    = _bof_y - _bosiz
                # 颜色：背景白时用深红+白边，背景黑时用纯红+白边
                _bo_fill   = "#440000" if not _is_white_bg else "#CC0000"
                _bo_border = "#FF3333"
                _bo_bw     = max(3, _bosiz // 6)   # 红边加粗，醒目
            # 后方障碍：填充+红框（和前方白框形成鲜明对比）
            add Solid(_bo_fill)   xpos _box ypos _boy xsize _bosiz ysize _bosiz
            add Solid(_bo_border) xpos _box ypos _boy xsize _bosiz ysize _bo_bw
            add Solid(_bo_border) xpos _box ypos (_boy+_bosiz-_bo_bw) xsize _bosiz ysize _bo_bw
            add Solid(_bo_border) xpos _box ypos _boy xsize _bo_bw ysize _bosiz
            add Solid(_bo_border) xpos (_box+_bosiz-_bo_bw) ypos _boy xsize _bo_bw ysize _bosiz

    # 莫比乌斯环绕闪白（"穿越"感）
    if getattr(_p3, '_wrap_flash', 0.0) > 0.01:
        python:
            _wf_a = min(0.7, _p3._wrap_flash * 2.0)
        add Transform(Solid("#FFFFFF"), alpha=_wf_a)

    # 道指示器（底部，N道通用）
    for (_ii, (_ix, _iy, _ic)) in enumerate(_ind):
        python:
            _iw   = max(6, int(60 / _n_lanes))  # 5道时更窄
            _ix_c = _ix - _iw // 2
            # 危险道：当前道且有方块在判定区 → 橙色闪
            _ind_col = _ic
            if _ii == _pcur_lane and _ii in _hit_zone_lanes:
                _ind_col = "#FF6622"
        add Solid(_ind_col) xpos _ix_c ypos _iy xsize _iw ysize 7

    # 深度指示条已删除

    # 爽世立绘（r2_p3 Boss段）
    # 放置在消失点处（路的尽头），随时间从小变大，营造"向玩家走来"的压迫感
    if GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False):
        python:
            _bg_w_soyo = getattr(_p3, "_bg_white", 0.0)
            # 背景完全变白(>=0.98)后才渐显立绘，在0.98~1.0区间淡入
            _soyo_alpha = max(0.0, (_bg_w_soyo - 0.98) / 0.02)
            # 胜利后渐隐：_clear_fade_t从0→2秒，alpha从1→0
            _soyo_fade_t = getattr(_p3.soyo_boss, '_clear_fade_t', 0.0)
            if getattr(_p3.soyo_boss, '_clear_fade_started', False):
                _soyo_alpha *= max(0.0, 1.0 - _soyo_fade_t / 2.0)
            # 随Boss进度从消失点小图变大（t=0→高SH*0.18，t=114→高SH*0.72）
            _sb_t = getattr(_p3.soyo_boss, "t", 0.0)
            _sb_prog = min(1.0, _sb_t / 114.0)   # 0~1进度
            _soyo_h = int(SH * (0.38 + 0.44 * _sb_prog))  # 初始38%→最终82%（略大）
            _soyo_x = VPX - 10     # 消失点略左
            _soyo_y = VPY
        if _soyo_alpha > 0.01 and renpy.loadable("soyo_boss.png"):
            add Transform("soyo_boss.png",
                          xanchor=0.5, yanchor=1.0,
                          xpos=_soyo_x, ypos=_soyo_y,
                          alpha=_soyo_alpha,
                          xsize=int(_soyo_h * 0.62),
                          ysize=_soyo_h,
                          fit="contain")

    # 飘字
    for _ft in _ftn:
        add Transform(Text(_ft.text, size=_ft.size, color=_ft.color), alpha=_ft.alpha) xpos int(_ft.x) ypos int(_ft.y)

    # 第四面墙：雪花噪点 + 撕裂线
    for (_nx, _ny, _nw, _nh, _nc) in _p3._wall4_noise:
        add Solid(_nc) xpos _nx ypos _ny xsize _nw ysize _nh
    for _tx2 in _p3._wall4_tears:
        add Solid("#FFFFFF") alpha 0.18 xpos _tx2 ypos 0 xsize 2 ysize SH

    # HUD
    add Solid("#000000") alpha 0.75 xpos 0 ypos 0 xsize SW ysize 52
    if GM.phase == "r4_h" and _p3.wall4_t > 5:
        python:
            _hud_wave_str = str(random.randint(0, 9999)) if random.random() < 0.15 else ("%.0f" % _p3.phase_timer)
        text _label xpos 20 ypos 14 size 18 color "#777777"
        text "TIME" xpos (SW-220) ypos 8 size 16 color "#666666"
        text _hud_wave_str xpos (SW-155) ypos 10 size 30 color "#FFFFFF"
    else:
        text _label xpos 20 ypos 14 size 18 color "#777777"
        text "TIME" xpos (SW-220) ypos 8 size 16 color "#666666"
        text "%.0f" % _p3.phase_timer xpos (SW-155) ypos 10 size 30 color "#FFFFFF"
    # Boss战时中央黄瓜数与boss名字重叠，boss战中隐藏（guide panel里已有显示）
    if not (GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False)):
        # r3_v2时黄瓜数显示在格子区标题旁
        if GM.phase != "r3_v2":
            text "🥒×%d" % CUKES.collected xpos (SW//2-30) ypos 10 size 18 color "#FFFFFF"
    if CUKES.can_revive:
        python:
            _p3_rv_s = "[[F]]复活∞" if DIFF.can_revive_free else ("[[F]]复活🥒×%d" % DIFF.revive_cost)
        text _p3_rv_s xpos (SW//2+50) ypos 12 size 14 color "#FFFFFF"

    # 压力槽
    python:
        _pw_p3   = int(160 * PRESSURE.value / 100.0)
        _pbar3_c = "#FF0000" if PRESSURE.value >= 80 else "#CC2222"
        _pbar3_a = (0.7 + 0.3 * math.sin(_p3.phase_timer * 14.0)) if PRESSURE.value >= 80 else 1.0
    add Transform(Text("压力" if PRESSURE.value < 80 else "DANGER", size=12,
                       color=("#AA4444" if PRESSURE.value < 80 else "#FF2222")),
                  alpha=_pbar3_a) xpos (SW-184) ypos 58
    add Solid("#1A0000") xpos (SW-184) ypos 74 xsize 160 ysize 10
    if _pw_p3 > 0:
        add Transform(Solid(_pbar3_c), alpha=_pbar3_a) xpos (SW-184) ypos 74 xsize _pw_p3 ysize 10

    if GM.phase == "tut_p3":
        python:
            _tp = min(_p3.phase_timer / GM.TUT_P3_DUR, 1.0)
            _bw = int(260 * _tp)
        add Solid("#333333") xpos (SW//2-130) ypos 58 xsize 260 ysize 8
        add Solid("#FFFFFF") xpos (SW//2-130) ypos 58 xsize _bw ysize 8

    # ── SoyoBoss HUD（r2_p3 Boss段专属）───────────────
    if GM.phase == "r2_p3" and getattr(_p3, "_boss_phase", False):
        python:
            _sb = _p3.soyo_boss
            _sb_fts = list(_sb.float_texts) if _sb.active else []
        if _sb.active:
            python:
                # 护盾格渲染数据
                _sb_shield_boxes = []
                for _si in range(_sb.MAX_SHIELD):
                    _sx = SW//2 - (_sb.MAX_SHIELD * 22)//2 + _si * 22
                    _sc = "#DD2222" if _si < _sb.shield else "#333333"
                    _sb_shield_boxes.append((_sx, _sc))
                # 时间轴进度
                _sb_prog = min(_sb.t / _sb.TOTAL_DUR, 1.0) if not _sb.stunned else 1.0
                _sb_pw   = int(260 * _sb_prog)
                # 倒计时
                _sb_remain = max(0.0, _sb.TOTAL_DUR - _sb.t)
                _sb_min = int(_sb_remain // 60)
                _sb_sec = int(_sb_remain % 60)

            # 爽世名字
            text "长崎爽世" xpos (SW//2-52) ypos 6 size 22 color _hud_txt_col
            # 护盾格
            for (_sx2, _sc2) in _sb_shield_boxes:
                add Solid(_sc2) xpos _sx2 ypos 34 xsize 18 ysize 18
            # 时间轴进度条
            add Solid("#333333") xpos (SW//2-130) ypos 56 xsize 260 ysize 6
            add Solid("#FFFF44") xpos (SW//2-130) ypos 56 xsize _sb_pw ysize 6
            # 倒计时
            text ("%d:%02d" % (_sb_min, _sb_sec)) xpos (SW//2+140) ypos 50 size 18 color _hud_txt_col
            # 晕厥状态标示
            if _sb.stunned:
                python:
                    _stun_a = 0.5 + 0.5 * math.sin(_p3.phase_timer * 8.0)
                add Transform(Solid("#00FF88"), alpha=_stun_a) xpos (SW//2-100) ypos 68 xsize 200 ysize 28
                text "STUNNED!" xpos (SW//2-56) ypos 74 size 20 color "#000000"
            # ── 左侧操作说明面板（晕厥期间隐藏避免和飘字重叠）──
            python:
                _guide_x  = 14
                _guide_y  = 70
                _g_title  = _hud_txt_col
                _g_body   = _hud_dim_col
                _g_key    = "#FF4444" if not _is_white_bg else "#CC0000"
                _g_green  = "#00CC55" if not _is_white_bg else "#007733"
                _g_red    = "#FF6600" if not _is_white_bg else "#CC3300"
                _g_pincer_show = _is_pincer
            if not _sb.stunned:
                text "— 攻击爽世 —  🥒×%d" % CUKES.collected xpos _guide_x ypos _guide_y size 16 color _g_title
                text "左键点击" xpos _guide_x ypos (_guide_y+24) size 13 color _g_key
                text "  唤出 / 结算判定条" xpos _guide_x ypos (_guide_y+40) size 13 color _g_body
                python:
                    _gline_col = "#333333" if not _is_white_bg else "#AAAAAA"
                add Solid(_g_green) xpos _guide_x ypos (_guide_y+58) xsize 10 ysize 10
                text " 绿区  命中 −1护盾" xpos (_guide_x+10) ypos (_guide_y+56) size 13 color _g_body
                add Solid(_g_red)   xpos _guide_x ypos (_guide_y+74) xsize 10 ysize 10
                text " 红区  暴击 最多−3" xpos (_guide_x+10) ypos (_guide_y+72) size 13 color _g_body
                if _g_pincer_show:
                    add Solid(_gline_col) xpos _guide_x ypos (_guide_y+90) xsize 170 ysize 1
                    text "⚠ 腹背受敌！" xpos _guide_x ypos (_guide_y+96) size 14 color _g_key
                    text "红框 = 后方来袭" xpos _guide_x ypos (_guide_y+114) size 13 color _g_body
                    text "白框 = 前方来袭" xpos _guide_x ypos (_guide_y+130) size 13 color _g_body
                    text "此阶段无法攻击爽世" xpos _guide_x ypos (_guide_y+146) size 13 color _g_key
                    text "专注躲避！" xpos _guide_x ypos (_guide_y+162) size 13 color _g_body
            else:
                python:
                    _gline_col = "#333333" if not _is_white_bg else "#AAAAAA"

            # QTE 判定条
            if not _sb.stunned and _sb._enter_done:
                if not _sb.qte_active:
                    pass
                else:
                    # QTE判定条：夹击阶段在玩家头顶，否则在屏幕底部
                    python:
                        _qx  = SW//2 - 160
                        _qy  = (int(_pcy) - 80) if _is_pincer else (SH - 120)
                        _qy  = max(60, _qy)   # 不超出屏幕顶部
                        _qw  = 320
                        _qh  = 28
                        # 灰色底
                        _gs  = int(_sb.qte_green_s  * _qw)
                        _gw2 = int(_sb.qte_green_w  * _qw)
                        _rs  = int(_sb.qte_red_s    * _qw)
                        _rw2 = int(_sb.qte_red_w    * _qw)
                        _pp  = int(_sb.qte_pos      * _qw)
                    add Solid("#333333") xpos _qx ypos _qy xsize _qw ysize _qh
                    # 绿区
                    add Solid("#00BB44") xpos (_qx+_gs) ypos _qy xsize _gw2 ysize _qh
                    # 红区
                    add Solid("#FF3300") xpos (_qx+_rs) ypos _qy xsize _rw2 ysize _qh
                    # 指针（白色竖条）
                    add Solid("#FFFFFF") xpos (_qx+_pp-2) ypos (_qy-4) xsize 4 ysize (_qh+8)
                    # 边框
                    add Solid("#FFFFFF") xpos (_qx-1) ypos (_qy-1) xsize (_qw+2) ysize 1
                    add Solid("#FFFFFF") xpos (_qx-1) ypos (_qy+_qh) xsize (_qw+2) ysize 1
                    text "再按 [[Z]]/[[J]]/左键 结算！" xpos (_qx+60) ypos (_qy+_qh+4) size 16 color _hud_txt_col
            # 玩家子弹渲染（白色圆点从近端飞向消失点）
            for _pb in list(_sb.p_bullets):
                python:
                    _pb_z    = _pb[0]
                    _pb_l    = _pb[1]
                    _pb_pd   = _pb[2] if len(_pb) > 2 else _pd   # 发射时的玩家depth
                    _pb_n    = getattr(_p3, '_lane_count', P3_LANES)
                    _pb_norm = (_pb_l + 0.5) / float(_pb_n)
                    # zr从_pb_pd（玩家位置）线性降到0（消失点=爽世位置）
                    _pb_zr   = max(0.001, _pb_pd * (1.0 - _pb_z))
                    _pb_size = max(3, int(22 * _pb_zr))   # 接近VP时变小
                    _pb_cx   = int(p3_lane_cx(_pb_norm, _pb_zr))
                    _pb_cy   = int(p3_lane_y(_pb_zr))
                # 子弹：圆形黄绿色，靠近VP时加拖尾感
                add Solid("#88FF44") xpos (_pb_cx - _pb_size//2) ypos (_pb_cy - _pb_size//2) xsize _pb_size ysize _pb_size
                if _pb_size > 6:
                    add Transform(Solid("#AAFFAA"), alpha=0.4) xpos (_pb_cx - _pb_size//2) ypos (_pb_cy - _pb_size//4 * 3) xsize _pb_size ysize (_pb_size//2)
            # Boss 飘字
            for _sbft in _sb_fts:
                add Transform(Text(_sbft.text, size=_sbft.size, color=_sbft.color), alpha=_sbft.alpha) xpos int(_sbft.x) ypos int(_sbft.y)

    if _p3.dead:
        if getattr(_p3, "_explode_t", 0.0) > 0:
            python:
                _exp_a3 = getattr(_p3, "_explode_t", 0.0) / 0.7
                import random as _rnd4
                _exp_ch3 = _rnd4.choice(["睦","X","✕","#","睦","!","陸","@"])
            add Transform(Solid("#FFFFFF"), alpha=min(0.95, _exp_a3)) xpos 0 ypos 0 xsize SW ysize SH
            text _exp_ch3 xpos 580 ypos 260 size 120 color "#FF0000"
        else:
            add Solid("#000000") alpha 0.88
            add Solid("#1A0000") xpos 340 ypos 220 xsize 600 ysize 260
            add Solid("#CC2222") xpos 340 ypos 220 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 476 xsize 600 ysize 4
            add Solid("#CC2222") xpos 340 ypos 220 xsize 4 ysize 260
            add Solid("#CC2222") xpos 936 ypos 220 xsize 4 ysize 260
            text "睦 的 压 力 爆 炸 了 ！" xpos 420 ypos 248 size 32 color "#FF4444"
            add Solid("#FFFFFF") xpos 360 ypos 292 xsize 560 ysize 1
            if CUKES.can_revive:
                python:
                    _rv_cost3 = "∞" if DIFF.can_revive_free else ("🥒×%d" % DIFF.revive_cost)
                add Solid("#002200") xpos 370 ypos 308 xsize 240 ysize 80
                add Solid("#00AA44") xpos 370 ypos 308 xsize 240 ysize 3
                text "[[F]]  复活" xpos 418 ypos 322 size 26 color "#00FF88"
                text _rv_cost3 xpos 440 ypos 358 size 18 color "#AAFFAA"
            add Solid("#1A1A00") xpos 670 ypos 308 xsize 240 ysize 80
            add Solid("#AAAA00") xpos 670 ypos 308 xsize 240 ysize 3
            text "[[R]]  重试" xpos 714 ypos 322 size 26 color "#FFFF44"
            text "重新开始" xpos 692 ypos 358 size 15 color "#AAAAAA"
            text "[[Q]]  返回标题" xpos 560 ypos 408 size 20 color "#555555"

    # Z/J 键 — Boss战射击（消耗1黄瓜）
    if GM.phase == "r2_p3":
        key "K_z" action Function(_p3.soyo_boss.activate_qte, int(round(_p3.lane)))
        key "K_j" action Function(_p3.soyo_boss.activate_qte, int(round(_p3.lane)))
        key "mousedown_1" action Function(_p3.soyo_boss.activate_qte, int(round(_p3.lane)))

    # A/D 键作为备用换道（W/S 键切换层级）
    key "K_LEFT"  action Function(_p3.move_left)
    key "K_RIGHT" action Function(_p3.move_right)
    key "K_a"     action Function(_p3.move_left)
    key "K_d"     action Function(_p3.move_right)
    key "K_w"     action Function(_p3_depth_up)
    key "K_s"     action Function(_p3_depth_down)
    key "K_UP"    action Function(_p3_depth_up)
    key "K_DOWN"  action Function(_p3_depth_down)
    key "K_r"     action Function(GM.retry_current)
    key "K_q"     action [Function(_quit_to_title), Jump("game_center_start")]
################################################################################
#  开发者面板
################################################################################
screen scr_dev_panel():
    style_prefix "mr"
    # 半透明背景板（右上角）
    add Transform(Solid("#000000"), alpha=0.88) xpos 870 ypos 0 xsize 410 ysize 720

    python:
        _dv = DEV
        _ph = GM.phase
        _clr_tut  = persistent.tutorial_cleared
        _best     = persistent.best_diff_cleared
        _best_str = {-1:"未通关", 0:"简单", 1:"普通", 2:"困难", 3:"极限"}.get(_best, "?")
        _diff_str = DIFF.NAMES[DIFF.current]
        _prs_str  = "%.1f" % PRESSURE.value

    # 标题
    add Solid("#FFFF00") xpos 870 ypos 0 xsize 410 ysize 3
    text "DEV MODE" xpos 882 ypos 8 size 22 color "#FFFF00"
    text "[[F12]] 关闭" xpos 1160 ypos 12 size 14 color "#888888"

    # ── 状态信息 ──────────────────────────────────────────
    add Solid("#333333") xpos 876 ypos 36 xsize 398 ysize 1
    text "状态" xpos 882 ypos 42 size 13 color "#AAAAAA"
    text ("场景: " + _ph)             xpos 882 ypos 58  size 14 color "#FFFFFF"
    text ("难度: " + _diff_str)       xpos 882 ypos 76  size 14 color "#FFFFFF"
    text ("压力: " + _prs_str)        xpos 882 ypos 94  size 14 color "#FFFFFF"
    text ("黄瓜: ×%d" % CUKES.collected) xpos 882 ypos 112 size 14 color "#FFFFFF"
    text ("教程通关: " + ("✓" if _clr_tut else "✗")) xpos 882 ypos 130 size 14 color ("#88FF88" if _clr_tut else "#FF8888")
    text ("最高通关: " + _best_str)   xpos 882 ypos 148 size 14 color "#FFFFFF"
    text ("困难解锁: " + ("✓" if DIFF.unlocked_hard else "✗"))    xpos 1080 ypos 130 size 14 color ("#88FF88" if DIFF.unlocked_hard else "#FF8888")
    text ("极限解锁: " + ("✓" if DIFF.unlocked_extreme else "✗")) xpos 1080 ypos 148 size 14 color ("#88FF88" if DIFF.unlocked_extreme else "#FF8888")

    # ── 开关类 ────────────────────────────────────────────
    add Solid("#333333") xpos 876 ypos 170 xsize 398 ysize 1
    text "开关" xpos 882 ypos 176 size 13 color "#AAAAAA"

    python:
        _toggles = [
            ("神模式(无限复活)", "god_mode",       190),
            ("无敌模式(不受伤)", "invincible",      218),
            ("无限黄瓜×999",    "inf_cukes",       246),
            ("压力锁零",         "no_pressure",     274),
            ("强制教程",         "force_tutorial",  302),
            ("🎬 演示模式(AI)",  "demo_mode",       330),
        ]
    for (_tn, _tk, _ty) in _toggles:
        python:
            _tv  = getattr(DEV, _tk)
            _tc  = "#00FF88" if _tv else "#555555"
            _tbc = "#005533" if _tv else "#222222"
        add Solid(_tbc) xpos 876 ypos _ty xsize 390 ysize 24
        text ("[[ON]] " if _tv else "[[OFF]]") xpos 882 ypos (_ty+4) size 14 color _tc
        text _tn xpos 926 ypos (_ty+4) size 14 color "#DDDDDD"
        button xpos 876 ypos _ty xsize 390 ysize 24 action Function(setattr, DEV, _tk, not _tv) style "empty_button"

    # ── 操作类 ────────────────────────────────────────────
    add Solid("#333333") xpos 876 ypos 360 xsize 398 ysize 1
    text "操作" xpos 882 ypos 366 size 13 color "#AAAAAA"

    python:
        _actions = [
            ("⏩ 跳过当前场景",    Function(DEV.skip_phase),  380),
            ("🔓 解锁全难度+教程", Function(DEV.unlock_all),  408),
            ("🗑  清除全部存档",    Function(DEV.reset_save),  436),
            ("➕ 添加100黄瓜",     Function(_dev_add_cukes),  464),
            ("💥 压力值拉满",      Function(setattr, PRESSURE, 'value', 100.0), 492),
            ("✨ 压力值清零",      Function(PRESSURE.reset),  520),
        ]
    for (_an, _aa, _ay) in _actions:
        add Solid("#222222") xpos 876 ypos _ay xsize 390 ysize 24
        text _an xpos 882 ypos (_ay+4) size 14 color "#DDDDDD"
        button xpos 876 ypos _ay xsize 390 ysize 24 action _aa style "empty_button"

    # ── Boss直跳 ──────────────────────────────────────────
    add Solid("#333333") xpos 876 ypos 580 xsize 398 ysize 1
    text "Boss直跳" xpos 882 ypos 586 size 13 color "#AAAAAA"
    python:
        _bosses = [
            ("🎵 爽世",   "soyo",   "#4466FF", 600),
            ("⚔ 祥子",   "sakiko", "#AA4400", 600),
            ("💀 墨缇斯", "mortis", "#CC0044", 600),
        ]
    for (_bn, _bk, _bc, _by) in _bosses:
        python:
            _b_idx  = ["soyo","sakiko","mortis"].index(_bk)
            _b_ypos = 600 + _b_idx * 30
            _b_active = (
                (_bk == "soyo"   and GM.phase in ("r2_p3",)) or
                (_bk == "sakiko" and GM.phase == "r3_v2") or
                (_bk == "mortis" and GM.phase == "r4_h")
            )
            _b_bg = "#221133" if _b_active else "#111111"
        add Solid(_b_bg) xpos 876 ypos _b_ypos xsize 390 ysize 26
        if _b_active:
            add Solid(_bc) alpha 0.25 xpos 876 ypos _b_ypos xsize 390 ysize 26
        text _bn xpos 888 ypos (_b_ypos + 5) size 14 color _bc
        text ("← 当前" if _b_active else "点击跳转") xpos 1160 ypos (_b_ypos + 7) size 11 color ("#AAAAAA" if not _b_active else _bc)
        button xpos 876 ypos _b_ypos xsize 390 ysize 26 action Function(DEV.jump_to_boss, _bk) style "empty_button"

    # ── 直达结局 ───────────────────────────────────────────
    python:
        _end_active = (GM.phase == "ending")
    add Solid("#221122" if _end_active else "#111111") xpos 876 ypos 694 xsize 390 ysize 26
    if _end_active:
        add Solid("#AA44CC") alpha 0.25 xpos 876 ypos 694 xsize 390 ysize 26
    text "🎬 直达结局" xpos 888 ypos 699 size 14 color "#CC88FF"
    text ("← 当前" if _end_active else "点击跳转") xpos 1160 ypos 701 size 11 color ("#CC88FF" if _end_active else "#AAAAAA")
    button xpos 876 ypos 694 xsize 390 ysize 26 style "empty_button" action [
        Function(setattr, store, 'ed_phase', 0),
        Function(setattr, store, 'ed_t',     0.0),
        Function(setattr, store, 'ed_di',    0),
        Function(setattr, store, 'ed_chars', 0.0),
        Function(GM._go, "ending"),
    ]
    add Solid("#333333") xpos 876 ypos 726 xsize 398 ysize 1
    text "难度切换（开发直通）" xpos 882 ypos 730 size 13 color "#AAAAAA"
    python:
        _dn_cols = ["#FFFFFF","#AAFFAA","#FFCC44","#FF6666"]
    for _di in range(4):
        python:
            _dname = DIFF.NAMES[_di]
            _dsel  = (DIFF.current == _di)
            _dcol  = _dn_cols[_di]
            _dbg   = "#003300" if _dsel else "#111111"
        add Solid(_dbg) xpos (876 + _di*98) ypos 746 xsize 94 ysize 26
        text _dname xpos (884 + _di*98) ypos 752 size 14 color _dcol
        button xpos (876 + _di*98) ypos 746 xsize 94 ysize 26 action Function(setattr, DIFF, 'current', _di) style "empty_button"

################################################################################
#  结局（占位）
################################################################################
screen scr_ending():
    style_prefix "ed"
    # 状态全部存在store里，screen default和store是两套不同变量

    timer 0.016 repeat True action Function(renpy.restart_interaction)

    python:
        import math as _em
        # 首次进入初始化
        if not hasattr(store, 'ed_phase'): store.ed_phase = 0
        if not hasattr(store, 'ed_t'):     store.ed_t     = 0.0
        if not hasattr(store, 'ed_di'):    store.ed_di    = 0
        if not hasattr(store, 'ed_chars'): store.ed_chars = 0.0
        if not hasattr(store, 'ed_wait'):  store.ed_wait  = 0.0
        # 本地别名方便读写
        ed_phase = store.ed_phase
        ed_t     = store.ed_t
        ed_di    = store.ed_di
        ed_chars = store.ed_chars
        ed_wait  = store.ed_wait
        # ── 对话数据 ──────────────────────────────────────────
        _ED_LINES = [
            # (speaker, text, color, size)
            ("墨缇斯", "为什么……宁愿踩碎这个世界的规则……也要往前跑？",    "#FF6666", 26),
            ("墨缇斯", "外面……明明只有她们的争吵，和无尽的痛苦……",    "#FF9999", 26),
            ("墨缇斯", "留在这个为你打造的、安静的循环里……不好吗？",        "#FFCCCC", 26),
            ("【系统】", "警告：系统底层逻辑已崩溃。",                      "#FF4444", 20),
            
            # 屏幕完全变黑，节奏放缓，开始内心独白
            ("",        '> \u201c爽世的引力很重。总是想把一切拉回回不去的过去。\u201d',  "#DDDDDD", 24),
            ("",        '\u201c祥子的话语很痛。像子弹一样，把天空都撕裂了。\u201d',     "#DDDDDD", 24),
            ("",        '\u201c在这片没有受伤的循环里，或许真的是个完美的避风港。\u201d', "#CCCCCC", 24),
            ("",        '\u201c但是……\u201d',                                "#FFFFFF", 26),
            

            ("小睦",    "如果不一直不出去的话……",                          "#AADDAA", 26),
            ("小睦",    "黄瓜……就不新鲜了。",                              "#AADDAA", 26),

            ("小睦",    "我不会说话。",                                   "#AADDAA", 24),
            ("小睦",    "所以，只能离开这里。",                               "#AADDAA", 26),
            ("小睦",    "去把它们，亲手交到她们手上。",                       "#AADDAA", 26),
            ("【系统】", "正在重新连接至现实世界……",                         "#88FF88", 20),
            ("",    "（此时应该要升华主题，但鉴于奥斯卡的文笔太差，就不强行升华主题了。感谢游玩！）", "#888888", 20),
        ]
        _CREDITS = [
            ("项目企划",  "缄默奥斯卡"),
            ("脚本剧情",  "缄默奥斯卡"),
            ("程序架构",  "缄默奥斯卡"),
            ("交互逻辑",  "缄默奥斯卡"),
            ("素材润色",  "缄默奥斯卡"),
            ("环境渲染",  "缄默奥斯卡"),
            ("游戏测试",  "缄默奥斯卡"),
            ("游戏测试",  "肆肆"),
            ("游戏测试",  "杰西不太卡_秽土转生"),
            ("游戏测试",  "夜鹭pixy"),
            ("游戏测试",  "忧郁仲夏夜"),
        ]
        _THANKS_AFDIAN = ["爱发电用户_5bad0", "普莱瑟尔", "肆肆"]
        _THANKS_HIGH = [
            "AliyaAriya","bili_87774915029","Pixy621","Tiaotiao跳","wangpai0798",
            "XYKerman","Y0ung杨杨杨杨",
            "黃鶴樓","户山今日澄_","杰西不太卡_秽土转生","卯涩","梦溪沈谈",
            "手可揽星夜","双手黄瓜睦偶人","肆肆_SiSi44","小困nemui",
            "雪mint星","汛哥_official","夜鹭pixy","一架路过的F117","要赢过生活哦",
        ]
        _THANKS_BASE = [
            "363unknown","_苏暮曦_","_氷芽川_四糸乃","astropine","bili_87774915029",
            "leihsing","mygoanon单推人","pendor-潘德","サンサ-ラ","Utoarch","Y0ung杨杨杨杨",
            "彼时之人","苍松不是松树","仓田真白圣经bot","简静岚",
            "蓝桥121","零时廻","路人甲零號",
            "马洛斯使者_","莫伊思特","睦子米小睦",
            "前田茜","是七夜嗷","颂乐小睦",
            "万物之母黑山羊","无敌了神人","星光灿烂starlight","喜你清晨",
            "一条猫猫鱼awa","夜鹭pixy","亦安安e","原神代肝睿初泽咲","转作子",
        ]
        _THANKS_CUSTOM= [
            "_苏暮曦_","bili_87774915029","mika_036","pendor-潘德","XYKerman",
            "路人甲零號","飘荡的尘",
        ]

        # ── 阶段推进（每帧调用） ──────────────────────────────
        _DT = 0.016
        ed_t  += _DT

        if ed_phase == 0:
            if ed_t >= 1.8:
                ed_phase = 1
                ed_t     = 0.0
                ed_chars = 0.0

        elif ed_phase == 1:
            if ed_di < len(_ED_LINES):
                _line_len = len(_ED_LINES[ed_di][1])
                ed_chars = min(float(_line_len), ed_chars + _DT * 28)
                if ed_wait > 0:
                    ed_wait -= _DT
            else:
                ed_phase = 2
                ed_t     = 0.0

        elif ed_phase == 2:
            if ed_t >= 2.5:
                ed_phase = 3
                ed_t     = 0.0

        elif ed_phase == 3:
            if ed_t >= 3.5:
                ed_phase = 4
                ed_t     = 0.0

        # ── 写回store ─────────────────────────────────────────
        store.ed_phase = ed_phase
        store.ed_t     = ed_t
        store.ed_di    = ed_di
        store.ed_chars = ed_chars
        store.ed_wait  = ed_wait
        store._ed_lines_ref = _ED_LINES

        # 估算名单总高度（用于判断滚动完成）
        _CREDITS_TOTAL_H = (
            60 + 60 + 60 + 80 +                          # 标题区 null
            len(_CREDITS) * 40 +                          # 制作名单
            80 + 20 + 8 + len(_THANKS_AFDIAN) * 30 +
            40 + 8 + len(_THANKS_HIGH) * 30 +
            40 + 8 + len(_THANKS_BASE) * 30 +
            40 + 8 + len(_THANKS_CUSTOM) * 30 +
            100 + 60 + 16 + 300                           # 结尾padding
        )

        # ── 点击/Space推进对话 ───────────────────────────────
        def _ed_advance():
            if store.ed_phase != 1: return
            _lines = store._ed_lines_ref
            _line_len = len(_lines[store.ed_di][1])
            if store.ed_chars < float(_line_len):
                store.ed_chars = float(_line_len)
            else:
                store.ed_di   += 1
                store.ed_chars = 0.0
            store.ed_wait = 0.0

        # ── 渲染 ─────────────────────────────────────────────
        _fade_a  = min(1.0, ed_t / 1.8) if ed_phase == 0 else 1.0
        _cuke_a  = max(0.0, (ed_t - 0.5) / 1.5) if ed_phase == 2 else (1.0 if ed_phase >= 3 else 0.0)
        _trans_a = min(1.0, ed_t / 1.0) if ed_phase == 3 else (1.0 if ed_phase >= 4 else 0.0)
        _scroll_y= max(0.0, (ed_t - 0.5) * 42) if ed_phase == 4 else 0.0
        # 滚动完成判定：内容全部滚过屏幕顶部后等2秒，返回标题
        _scroll_done = ed_phase == 4 and _scroll_y > (_CREDITS_TOTAL_H + 720)
        if _scroll_done:
            ed_phase = 5   # 标记完成，防止重复触发
            store.ed_phase = 5

    # ─────────── 黑色背景 ───────────
    add Transform(Solid("#000000"), alpha=_fade_a) xpos 0 ypos 0 xsize 1280 ysize 720

    # ─────────── 阶段1：对话区 ───────────
    if ed_phase in (1, 2):
        if ed_di < len(_ED_LINES):
            python:
                _sp, _txt, _col, _sz = _ED_LINES[ed_di]
                _shown = _txt[:int(ed_chars)]
                _cursor = "█" if int(ed_chars) < len(_txt) else ""
            if _sp:
                add Transform(Text(_sp + "：", size=18, color="#888888"),
                    alpha=0.9) xpos 320 ypos 280
            add Transform(Text(_shown + _cursor, size=_sz, color=_col),
                alpha=0.95) xpos 320 ypos 310
            # 已显示完时的提示
            if int(ed_chars) >= len(_ED_LINES[ed_di][1]) and ed_di < len(_ED_LINES) - 1:
                python:
                    _blink = 0.6 + 0.4 * math.sin(ed_t * 5.0)
                add Transform(Text("▼", size=16, color="#FFFFFF"),
                    alpha=_blink) xpos 620 ypos 346

    # ─────────── 黄瓜微光（阶段2起） ───────────
    if _cuke_a > 0:
        python:
            _ck_glow = 0.15 + 0.1 * math.sin(ed_t * 2.5)
        add Transform(Text("🥒", size=72), alpha=_cuke_a) xpos 588 ypos 240

    # ─────────── 阶段3：过渡语 ───────────
    if _trans_a > 0 and ed_phase in (3, 4):
        add Transform(
            Text("奔跑结束了。谢谢你，陪我走到这里的你。", size=28, color="#FFFFFF"),
            alpha=_trans_a) xpos 280 ypos 320

    # ─────────── 阶段4：名单滚动 ───────────
    if ed_phase == 4:
        python:
            _cr_a    = min(1.0, ed_t / 1.2)
            _cr_yoff = int(720 - _scroll_y)
        add Transform(Solid("#000000"), alpha=_cr_a) xpos 0 ypos 0 xsize 1280 ysize 720
        frame:
            background Solid("#00000000")
            xpos 0 xsize 1280 ypos _cr_yoff
            yfill False
            vbox:
                xalign 0.5
                spacing 8
                null height 60
                text "T H A N K S   F O R   P L A Y I N G" size 40 color "#FFFFFF" xalign 0.5
                null height 20
                text "奔跑结束了。谢谢你，陪我走到这里的你。" size 26 color "#CCCCCC" xalign 0.5
                null height 60
                text "【 制作名单 】" size 36 color "#A3E4D7" xalign 0.5
                null height 16
                for _role, _name in _CREDITS:
                    hbox:
                        xalign 0.5
                        spacing 40
                        text _role size 24 color "#CCCCCC" minwidth 160 xalign 1.0
                        text _name size 24 color "#FFFFFF" minwidth 160
                null height 80
                text "【 致谢 】" size 36 color "#E0AAFF" xalign 0.5
                null height 20
                text "— 爱发电赞助 —" size 28 color "#FF88AA" xalign 0.5
                null height 8
                for _sp in _THANKS_AFDIAN:
                    text _sp size 22 color "#FFFFFF" xalign 0.5
                null height 40
                text "— 高档赞助 —" size 28 color "#FFDD88" xalign 0.5
                null height 8
                for _sp in _THANKS_HIGH:
                    text _sp size 22 color "#FFFFFF" xalign 0.5
                null height 40
                text "— 基础赞助 —" size 28 color "#88CCFF" xalign 0.5
                null height 8
                for _sp in _THANKS_BASE:
                    text _sp size 22 color "#FFFFFF" xalign 0.5
                text "睦祱" size 22 color "#FFFFFF" xalign 0.5 font "siyuan.ttf"
                null height 40
                text "— 自定义赞助 —" size 28 color "#FF88CC" xalign 0.5
                null height 8
                for _sp in _THANKS_CUSTOM:
                    text _sp size 22 color "#FFFFFF" xalign 0.5
                null height 100
                text "小睦快跑" size 50 color "#AADDAA" xalign 0.5
                null height 16
                text "感谢游玩" size 30 color "#FFFFFF" xalign 0.5
                null height 300

    # ─────────── 结尾滚完后返回标题 ───────────
    if ed_phase == 5:
        timer 2.5 action [
            Function(renpy.music.stop, fadeout=2.0),
            Function(setattr, store, '_current_bgm', None),
            Function(setattr, store, 'ed_phase', 0),
            Jump("game_center_start")
        ] repeat False

    # ─────────── 输入 ───────────
    if ed_phase == 1:
        key "K_SPACE"     action Function(_ed_advance)
        key "K_RETURN"    action Function(_ed_advance)
        key "mousedown_1" action Function(_ed_advance)
