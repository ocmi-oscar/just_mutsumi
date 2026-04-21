# --- 1. 变量定义 ---
default persistent.player_bday_month = 0
default persistent.player_bday_day = 0
default cal_year = 2026
default cal_month = 1

# --- 2. 动画增强 ---
transform cal_appear:
    alpha 0.0 zoom 0.95
    easein_back 0.3 alpha 1.0 zoom 1.0

transform cal_today_pulse:
    matrixcolor TintMatrix("#ffffff00")
    linear 1.0 matrixcolor TintMatrix("#ffffff44")
    linear 1.0 matrixcolor TintMatrix("#ffffff00")
    repeat

# --- 3. 逻辑处理 ---
init python:
    import calendar
    import datetime

    def get_holidays(year, month):
        base_holidays = {
            (1, 1): "元旦", (1, 14): "睦的生日", 
            (2, 14): "情人节", (2, 16): "除夕", (2, 17): "春节",(3, 3): "元宵节", (3, 12): "植树节", (4, 4): "清明节", (5, 1): "劳动节",
            (6, 1): "儿童节", (6, 19): "端午节",(8, 19): "七夕节",(9, 25): "中秋节",(10, 1): "国庆节", (12, 25): "圣诞节"
        }
        if persistent.player_bday_month == month:
            base_holidays[(month, persistent.player_bday_day)] = "你的生日"
        return base_holidays

    def adjust_calendar(delta):
        global cal_year, cal_month
        cal_month += delta
        if cal_month > 12:
            cal_month = 1
            cal_year += 1
        elif cal_month < 1:
            cal_month = 12
            cal_year -= 1
