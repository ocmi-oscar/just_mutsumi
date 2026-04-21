
# ❤️ 好感度系统核心逻辑 (M0.21 最终修复版 - 支持负数)

init offset = -1

define NAME_WAKABA = "若叶睦"
define NAME_GUITAR = "吉他睦"
define NAME_METIS = "墨缇斯"

# --- 2. 核心逻辑 ---
init python:
    import datetime
    
    # 变量初始化
    if persistent.gw_wakaba is None: persistent.gw_wakaba = 0.0
    if persistent.gw_guitar is None: persistent.gw_guitar = 0.0
    if persistent.gw_metis is None: persistent.gw_metis = 0.0
    if persistent.gw_total is None: persistent.gw_total = 0.0 
    
    if persistent.gw_event_flags is None: persistent.gw_event_flags = {}
    if persistent.gw_daily_counts is None: persistent.gw_daily_counts = {}
    if persistent.gw_last_date is None: persistent.gw_last_date = ""

    class MultiPersonalityGW(object):
        def __init__(self):
            self.max_val = 10000.0
            self.min_val = -100.0 # 允许负数

        # 刷新总分 (三者之和)
        def _refresh_total(self):
            persistent.gw_total = round(
                persistent.gw_wakaba + 
                persistent.gw_guitar + 
                persistent.gw_metis, 1
            )
            renpy.save_persistent()

        # 修改好感度核心函数
        def change(self, amount, target="mutsumi"):
            try:
                amount = round(float(amount), 1)
            except:
                amount = 0.0
                
            char_map = {
                "wakaba": "gw_wakaba", "若叶睦": "gw_wakaba", "睦": "gw_wakaba", 
                "苦瓜睦": "gw_wakaba", "古神睦": "gw_wakaba", NAME_WAKABA: "gw_wakaba",
                "guitar": "gw_guitar", "吉他睦": "gw_guitar", NAME_GUITAR: "gw_guitar",
                "metis": "gw_metis", "墨缇斯": "gw_metis", NAME_METIS: "gw_metis"
            }
            
            display_map = {
                "gw_wakaba": NAME_WAKABA, 
                "gw_guitar": NAME_GUITAR, 
                "gw_metis": NAME_METIS
            }
            
            attr_name = char_map.get(target, "gw_wakaba")
            old_val = getattr(persistent, attr_name)
            
            # 限制范围：最小值 self.min_val (-100), 最大值 self.max_val (10000)
            new_val = max(min(round(old_val + amount, 1), self.max_val), self.min_val)
            
            setattr(persistent, attr_name, new_val)
            self._refresh_total() # 同步更新总分
            
            # 只有数值变化不为0时才飘字
            if amount != 0:
                renpy.show_screen("gw_notify", amount=amount, target_name=display_map[attr_name])
            return True

        # 手动输入数值 (开发者工具用)
        def manual_input(self, var_name, label_name):
            current_val = getattr(persistent, var_name)
            res = renpy.input("输入 {} 的值 (-100 到 10000):".format(label_name), default=str(current_val), allow="-0123456789.")
            try:
                new_val = max(min(round(float(res.strip()), 1), self.max_val), self.min_val)
                setattr(persistent, var_name, new_val)
                self._refresh_total()
            except:
                pass
            renpy.restart_interaction()

    gw_tools = MultiPersonalityGW()

    # 快捷加分接口
    def add_hgd(char_name, amount, once_id=None, daily_id=None, max_daily=0):
        today_str = str(datetime.date.today())
        if persistent.gw_last_date != today_str:
            persistent.gw_last_date = today_str
            persistent.gw_daily_counts = {}

        if once_id:
            if persistent.gw_event_flags.get(once_id):
                return 
            persistent.gw_event_flags[once_id] = True

        if daily_id and max_daily > 0:
            current_count = persistent.gw_daily_counts.get(daily_id, 0)
            if current_count >= max_daily:
                return 
            persistent.gw_daily_counts[daily_id] = current_count + 1

        gw_tools.change(amount, char_name)

# ------------------------------------------------------------------------------
# 3. 视觉反馈：飘字动画
# ------------------------------------------------------------------------------
screen gw_notify(amount, target_name):
    zorder 300
    timer 2.0 action Hide("gw_notify")

    fixed:
        at transform:
            alpha 0.0 yoffset 30
            parallel:
                easein 0.5 alpha 1.0 yoffset 0
                pause 1.0
                easeout 0.5 alpha 0.0 yoffset -30

        $ prefix = "+" if amount > 0 else ""
        # 负数用红色，正数用绿色
        $ display_color = "#95e1d3" if amount > 0 else "#ff4444"
        
        hbox:
            align (0.5, 0.15)
            spacing 15
            text "[target_name]":
                size 22 color "#ffffff" outlines [(2, "#000", 0, 0)]
            text "[prefix][amount]%":
                size 30 color display_color bold True outlines [(2, "#000", 0, 0)]

# ------------------------------------------------------------------------------
# 4. 主好感度界面 (Mutsumi Graph)
# ------------------------------------------------------------------------------
screen personality_goodwill_ui():
    tag menu
    modal True
    zorder 200

    fixed:
        at transform:
            on show:
                alpha 0.0 zoom 0.95
                easein_back 0.6 alpha 1.0 zoom 1.0
            on hide:
                easeout_back 0.5 alpha 0.0 zoom 0.92 yoffset 50

        if renpy.loadable("images/ui/goodwill_bg.png"):
            add "images/ui/goodwill_bg.png"
        else:
            add Solid("#0e1210")

        text "Mutsumi Graph":
            size 65 color "#d2b48c" italic True align (0.05, 0.05)

        hbox:
            align (0.5, 0.45)  
            spacing 60         
            use personality_card_final(NAME_WAKABA, "images/ui/head_wakaba.png", persistent.gw_wakaba, "#95e1d3", z_factor=1.5, y_off=40, x_off=-120)
            use personality_card_final(NAME_GUITAR, "images/ui/head_guitar_full.png", persistent.gw_guitar, "#f38181", z_factor=0.65, y_off=870, x_off=0)
            use personality_card_final(NAME_METIS, "images/ui/head_metis_full.png", persistent.gw_metis, "#95a5a6", z_factor=0.65, y_off=870, x_off=0)

        button:
            action Hide("personality_goodwill_ui", transition=dissolve)
            align (0.98, 0.98) 
            xsize 70 ysize 35  
            background Frame(Solid("#e8d3b9cc"), 4, 4)
            text "BACK" size 14 color "#779977" bold True align (0.5, 0.5)

        

screen personality_card_final(name, img, value, theme_color, z_factor=1.0, y_off=0, x_off=0):
    fixed:
        xsize 320 ysize 680 
        if renpy.loadable(img):
            add img align (0.5, 1.0) zoom z_factor yoffset y_off xoffset x_off

        vbox:
            align (0.5, 0.98) 
            spacing -10  
            text name size 18 color "#ffffff" outlines [(2, "#4a3a2e", 1, 1)] xalign 0.5
            
            $ val_rounded = round(float(value), 1)
            $ display_val = "{0:g}".format(val_rounded)
            text "[display_val]%":
                size 70 bold True color "#ffffff" outlines [(4, theme_color + "33", 0, 0), (2, "#4a3a2e", 0, 0)] xalign 0.5
            
            frame:
                xsize 110 ysize 22
                background Solid("#4a3a2e") 
                xalign 0.5
                text "甘え度" size 14 color "#e8d3b9" xalign 0.5 yalign 0.5


# 包装函数，用于处理领取并弹窗
init python:
    def claim_rewards_wrapper():
        amount = gacha_sys.claim_goodwill_rewards()
        if amount > 0:
            renpy.notify("成功领取 {} 枚睦币！".format(amount))
        else:
            renpy.notify("好感度不足，每获得30好感度可领取一次十连。")

# ------------------------------------------------------------------------------
screen debug_slider_item_pro(label_name, var_name, color_code):
    $ current_val = getattr(persistent, var_name)
    vbox:
        spacing 5
        hbox:
            xsize 550
            text label_name size 18 color "#eee" xalign 0.0
            button:
                xalign 1.0
                background Solid("#ffffff1a")
                padding (8, 4)
                action Function(gw_tools.manual_input, var_name, label_name)
                hbox:
                    $ val_str = "{0:g}".format(round(float(current_val), 1))
                    text "[val_str]" size 18 color color_code
                    text "%" size 16 color "#666" xoffset 5
        
        # 核心修改：支持负数范围
        # range = 总跨度 (从-100到10000，跨度是10100)
        # offset = 起始偏移量 (-100)
        bar value FieldValue(persistent, var_name, range=10100.0, offset=-100.0, max_is_zero=False):
            xsize 550
            ysize 30 
            left_bar Solid(color_code)
            right_bar Solid("#333")
            # 拖动滑块释放时自动刷新总分
            released Function(gw_tools._refresh_total)