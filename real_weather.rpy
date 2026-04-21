# ==============================================================================
# 🌤 天气 — Real Weather App
# 使用 Open-Meteo API（免费、准确、有城市验证）
# ==============================================================================

default persistent.weather_city = ""
default persistent.weather_history = []
default _weather_data = None
default _weather_loading = False
default _weather_error = ""
default _weather_city_input = ""
default _weather_show_search = False

init python:
    import threading as _wt_threading
    import json as _wt_json

    _WEATHER_CITIES = [
        "北京", "上海", "广州", "深圳", "杭州",
        "成都", "武汉", "南京", "重庆", "西安",
        "长沙", "苏州", "天津", "郑州", "青岛",
        "东京", "大阪", "纽约", "伦敦", "巴黎",
    ]

    _OM_WEATHER_CODES = {
        0:  ("晴", "☀"),
        1:  ("基本晴朗", "🌤"),
        2:  ("局部多云", "⛅"),
        3:  ("阴", "☁"),
        45: ("雾", "🌫"),
        48: ("冻雾", "🌫"),
        51: ("毛毛雨", "🌦"),
        53: ("毛毛雨", "🌦"),
        55: ("毛毛雨", "🌦"),
        56: ("冻雨", "🌧"),
        57: ("冻雨", "🌧"),
        61: ("小雨", "🌧"),
        63: ("中雨", "🌧"),
        65: ("大雨", "🌧"),
        66: ("冻雨", "🌧"),
        67: ("冻雨", "🌧"),
        71: ("小雪", "🌨"),
        73: ("中雪", "🌨"),
        75: ("大雪", "❄"),
        77: ("雪粒", "🌨"),
        80: ("阵雨", "🌦"),
        81: ("阵雨", "🌧"),
        82: ("强阵雨", "🌧"),
        85: ("阵雪", "🌨"),
        86: ("强阵雪", "❄"),
        95: ("雷阵雨", "⛈"),
        96: ("雷阵雨夹冰雹", "⛈"),
        99: ("强雷暴夹冰雹", "⛈"),
    }

    def weather_om_get_icon(code):
        try:
            c = int(code)
            if c in _OM_WEATHER_CODES:
                return _OM_WEATHER_CODES[c]
        except:
            pass
        return ("未知", "❓")

    def weather_wind_dir(deg):
        if deg is None:
            return "—"
        try:
            dirs = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
            idx = int((float(deg) + 22.5) / 45) % 8
            return dirs[idx]
        except:
            return "—"

    # 中文城市名 → 拼音/英文 映射表（geocoding API的真实数据库名）
    _CN_CITY_MAP = {
        "北京": "Beijing", "上海": "Shanghai", "天津": "Tianjin",
        "重庆": "Chongqing", "石家庄": "Shijiazhuang", "唐山": "Tangshan",
        "秦皇岛": "Qinhuangdao", "邯郸": "Handan", "邢台": "Xingtai",
        "保定": "Baoding", "张家口": "Zhangjiakou", "承德": "Chengde",
        "沧州": "Cangzhou", "廊坊": "Langfang", "衡水": "Hengshui",
        "太原": "Taiyuan", "大同": "Datong", "阳泉": "Yangquan",
        "长治": "Changzhi", "晋城": "Jincheng", "朔州": "Shuozhou",
        "晋中": "Jinzhong", "运城": "Yuncheng", "忻州": "Xinzhou",
        "临汾": "Linfen", "吕梁": "Lvliang", "呼和浩特": "Hohhot",
        "包头": "Baotou", "乌海": "Wuhai", "赤峰": "Chifeng",
        "通辽": "Tongliao", "鄂尔多斯": "Ordos", "呼伦贝尔": "Hulunbuir",
        "巴彦淖尔": "Bayannur", "乌兰察布": "Ulanqab", "兴安盟": "Hinggan",
        "锡林郭勒": "Xilingol", "阿拉善": "Alxa", "沈阳": "Shenyang",
        "大连": "Dalian", "鞍山": "Anshan", "抚顺": "Fushun",
        "本溪": "Benxi", "丹东": "Dandong", "锦州": "Jinzhou",
        "营口": "Yingkou", "阜新": "Fuxin", "辽阳": "Liaoyang",
        "盘锦": "Panjin", "铁岭": "Tieling", "朝阳": "Chaoyang",
        "葫芦岛": "Huludao", "长春": "Changchun", "吉林": "Jilin",
        "四平": "Siping", "辽源": "Liaoyuan", "通化": "Tonghua",
        "白山": "Baishan", "松原": "Songyuan", "白城": "Baicheng",
        "延边": "Yanbian", "延吉": "Yanji", "哈尔滨": "Harbin",
        "齐齐哈尔": "Qiqihar", "鸡西": "Jixi", "鹤岗": "Hegang",
        "双鸭山": "Shuangyashan", "大庆": "Daqing", "伊春": "Yichun",
        "佳木斯": "Jiamusi", "七台河": "Qitaihe", "牡丹江": "Mudanjiang",
        "黑河": "Heihe", "绥化": "Suihua", "大兴安岭": "Daxinganling",
        "南京": "Nanjing", "无锡": "Wuxi", "徐州": "Xuzhou",
        "常州": "Changzhou", "苏州": "Suzhou", "南通": "Nantong",
        "连云港": "Lianyungang", "淮安": "Huai'an", "盐城": "Yancheng",
        "扬州": "Yangzhou", "镇江": "Zhenjiang", "泰州": "Taizhou",
        "宿迁": "Suqian", "杭州": "Hangzhou", "宁波": "Ningbo",
        "温州": "Wenzhou", "嘉兴": "Jiaxing", "湖州": "Huzhou",
        "绍兴": "Shaoxing", "金华": "Jinhua", "衢州": "Quzhou",
        "舟山": "Zhoushan", "丽水": "Lishui", "义乌": "Yiwu",
        "合肥": "Hefei", "芜湖": "Wuhu", "蚌埠": "Bengbu",
        "淮南": "Huainan", "马鞍山": "Ma'anshan", "淮北": "Huaibei",
        "铜陵": "Tongling", "安庆": "Anqing", "黄山": "Huangshan",
        "滁州": "Chuzhou", "阜阳": "Fuyang", "宿州": "Suzhou",
        "六安": "Lu'an", "亳州": "Bozhou", "池州": "Chizhou",
        "宣城": "Xuancheng", "福州": "Fuzhou", "厦门": "Xiamen",
        "莆田": "Putian", "三明": "Sanming", "泉州": "Quanzhou",
        "漳州": "Zhangzhou", "南平": "Nanping", "龙岩": "Longyan",
        "宁德": "Ningde", "南昌": "Nanchang", "景德镇": "Jingdezhen",
        "萍乡": "Pingxiang", "九江": "Jiujiang", "新余": "Xinyu",
        "鹰潭": "Yingtan", "赣州": "Ganzhou", "吉安": "Ji'an",
        "宜春": "Yichun", "抚州": "Fuzhou", "上饶": "Shangrao",
        "济南": "Jinan", "青岛": "Qingdao", "淄博": "Zibo",
        "枣庄": "Zaozhuang", "东营": "Dongying", "烟台": "Yantai",
        "潍坊": "Weifang", "济宁": "Jining", "泰安": "Tai'an",
        "威海": "Weihai", "日照": "Rizhao", "临沂": "Linyi",
        "德州": "Dezhou", "聊城": "Liaocheng", "滨州": "Binzhou",
        "菏泽": "Heze", "郑州": "Zhengzhou", "开封": "Kaifeng",
        "洛阳": "Luoyang", "平顶山": "Pingdingshan", "安阳": "Anyang",
        "鹤壁": "Hebi", "新乡": "Xinxiang", "焦作": "Jiaozuo",
        "濮阳": "Puyang", "许昌": "Xuchang", "漯河": "Luohe",
        "三门峡": "Sanmenxia", "南阳": "Nanyang", "商丘": "Shangqiu",
        "信阳": "Xinyang", "周口": "Zhoukou", "驻马店": "Zhumadian",
        "济源": "Jiyuan", "武汉": "Wuhan", "黄石": "Huangshi",
        "十堰": "Shiyan", "宜昌": "Yichang", "襄阳": "Xiangyang",
        "鄂州": "Ezhou", "荆门": "Jingmen", "孝感": "Xiaogan",
        "荆州": "Jingzhou", "黄冈": "Huanggang", "咸宁": "Xianning",
        "随州": "Suizhou", "恩施": "Enshi", "仙桃": "Xiantao",
        "潜江": "Qianjiang", "天门": "Tianmen", "长沙": "Changsha",
        "株洲": "Zhuzhou", "湘潭": "Xiangtan", "衡阳": "Hengyang",
        "邵阳": "Shaoyang", "岳阳": "Yueyang", "常德": "Changde",
        "张家界": "Zhangjiajie", "益阳": "Yiyang", "郴州": "Chenzhou",
        "永州": "Yongzhou", "怀化": "Huaihua", "娄底": "Loudi",
        "湘西": "Xiangxi", "广州": "Guangzhou", "韶关": "Shaoguan",
        "深圳": "Shenzhen", "珠海": "Zhuhai", "汕头": "Shantou",
        "佛山": "Foshan", "江门": "Jiangmen", "湛江": "Zhanjiang",
        "茂名": "Maoming", "肇庆": "Zhaoqing", "惠州": "Huizhou",
        "梅州": "Meizhou", "汕尾": "Shanwei", "河源": "Heyuan",
        "阳江": "Yangjiang", "清远": "Qingyuan", "东莞": "Dongguan",
        "中山": "Zhongshan", "潮州": "Chaozhou", "揭阳": "Jieyang",
        "云浮": "Yunfu", "南宁": "Nanning", "柳州": "Liuzhou",
        "桂林": "Guilin", "梧州": "Wuzhou", "北海": "Beihai",
        "防城港": "Fangchenggang", "钦州": "Qinzhou", "贵港": "Guigang",
        "玉林": "Yulin", "百色": "Baise", "贺州": "Hezhou",
        "河池": "Hechi", "来宾": "Laibin", "崇左": "Chongzuo",
        "海口": "Haikou", "三亚": "Sanya", "三沙": "Sansha",
        "儋州": "Danzhou", "成都": "Chengdu", "自贡": "Zigong",
        "攀枝花": "Panzhihua", "泸州": "Luzhou", "德阳": "Deyang",
        "绵阳": "Mianyang", "广元": "Guangyuan", "遂宁": "Suining",
        "内江": "Neijiang", "乐山": "Leshan", "南充": "Nanchong",
        "眉山": "Meishan", "宜宾": "Yibin", "广安": "Guang'an",
        "达州": "Dazhou", "雅安": "Ya'an", "巴中": "Bazhong",
        "资阳": "Ziyang", "阿坝": "Aba", "甘孜": "Garze",
        "凉山": "Liangshan", "贵阳": "Guiyang", "六盘水": "Liupanshui",
        "遵义": "Zunyi", "安顺": "Anshun", "毕节": "Bijie",
        "铜仁": "Tongren", "黔西南": "Qianxinan", "黔东南": "Qiandongnan",
        "黔南": "Qiannan", "昆明": "Kunming", "曲靖": "Qujing",
        "玉溪": "Yuxi", "保山": "Baoshan", "昭通": "Zhaotong",
        "丽江": "Lijiang", "普洱": "Puer", "临沧": "Lincang",
        "楚雄": "Chuxiong", "红河": "Honghe", "文山": "Wenshan",
        "西双版纳": "Xishuangbanna", "大理": "Dali", "德宏": "Dehong",
        "怒江": "Nujiang", "迪庆": "Diqing", "拉萨": "Lhasa",
        "日喀则": "Shigatse", "昌都": "Chamdo", "林芝": "Nyingchi",
        "山南": "Shannan", "那曲": "Nagqu", "阿里": "Ngari",
        "西安": "Xi'an", "铜川": "Tongchuan", "宝鸡": "Baoji",
        "咸阳": "Xianyang", "渭南": "Weinan", "延安": "Yan'an",
        "汉中": "Hanzhong", "榆林": "Yulin", "安康": "Ankang",
        "商洛": "Shangluo", "兰州": "Lanzhou", "嘉峪关": "Jiayuguan",
        "金昌": "Jinchang", "白银": "Baiyin", "天水": "Tianshui",
        "武威": "Wuwei", "张掖": "Zhangye", "平凉": "Pingliang",
        "酒泉": "Jiuquan", "庆阳": "Qingyang", "定西": "Dingxi",
        "陇南": "Longnan", "临夏": "Linxia", "甘南": "Gannan",
        "西宁": "Xining", "海东": "Haidong", "海北": "Haibei",
        "黄南": "Huangnan", "海南州": "Hainan", "果洛": "Golog",
        "玉树": "Yushu", "海西": "Haixi", "银川": "Yinchuan",
        "石嘴山": "Shizuishan", "吴忠": "Wuzhong", "固原": "Guyuan",
        "中卫": "Zhongwei", "乌鲁木齐": "Urumqi", "克拉玛依": "Karamay",
        "吐鲁番": "Turpan", "哈密": "Hami", "昌吉": "Changji",
        "博尔塔拉": "Bortala", "巴音郭楞": "Bayingolin", "阿克苏": "Aksu",
        "克孜勒苏": "Kizilsu", "喀什": "Kashgar", "和田": "Hotan",
        "伊犁": "Ili", "塔城": "Tacheng", "阿勒泰": "Altay",
        "石河子": "Shihezi", "阿拉尔": "Aral", "图木舒克": "Tumxuk",
        "五家渠": "Wujiaqu", "北屯": "Beitun", "香港": "Hong Kong",
        "澳门": "Macau", "台北": "Taipei", "新北": "New Taipei",
        "桃园": "Taoyuan", "台中": "Taichung", "台南": "Tainan",
        "高雄": "Kaohsiung", "基隆": "Keelung", "新竹": "Hsinchu",
        "嘉义": "Chiayi",
    }

    def weather_geocode(city):
        """通过Open-Meteo Geocoding验证城市并获取经纬度"""
        # 尝试中文映射 → 拼音
        query_names = []
        if city in _CN_CITY_MAP:
            query_names.append(_CN_CITY_MAP[city])
        query_names.append(city)
        # 去重保持顺序
        seen = set()
        query_names = [n for n in query_names if not (n in seen or seen.add(n))]

        for q in query_names:
            result = _weather_geocode_query(q, city)
            if result:
                return result
        return None

    def _weather_geocode_query(query, original_city):
        """单次查询"""
        try:
            import ssl as _wt_ssl
            ssl_ctx = _wt_ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = _wt_ssl.CERT_NONE

            from urllib.request import urlopen, Request
            from urllib.parse import quote

            url = "https://geocoding-api.open-meteo.com/v1/search?name={}&count=5&language=zh&format=json".format(quote(query))
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

            try:
                resp = urlopen(req, timeout=10, context=ssl_ctx)
            except:
                url_http = url.replace("https://", "http://")
                req2 = Request(url_http, headers={"User-Agent": "Mozilla/5.0"})
                resp = urlopen(req2, timeout=10)

            raw = resp.read().decode('utf-8')
            data = _wt_json.loads(raw)

            results = data.get("results")
            if not results or len(results) == 0:
                return None

            # 优先选择中国的结果
            r = None
            for candidate in results:
                if candidate.get("country_code") == "CN":
                    r = candidate
                    break
            if r is None:
                r = results[0]

            return {
                "name": original_city if original_city in _CN_CITY_MAP else r.get("name", original_city),
                "country": r.get("country", ""),
                "admin1": r.get("admin1", ""),
                "lat": r.get("latitude"),
                "lon": r.get("longitude"),
            }
        except:
            return None

    def weather_fetch(city):
        store._weather_loading = True
        store._weather_error = ""
        store._weather_data = None
        store._weather_show_search = False
        renpy.restart_interaction()

        def _do_fetch():
            geo = weather_geocode(city)
            if geo is None:
                store._weather_data = None
                store._weather_error = "找不到「{}」这个地方".format(city)
                store._weather_loading = False
                renpy.restart_interaction()
                return

            lat = geo["lat"]
            lon = geo["lon"]

            parts = [geo["name"]]
            if geo["admin1"] and geo["admin1"] != geo["name"]:
                parts.append(geo["admin1"])
            if geo["country"]:
                parts.append(geo["country"])
            display_name = " · ".join(parts)

            try:
                import ssl as _wt_ssl
                ssl_ctx = _wt_ssl.create_default_context()
                ssl_ctx.check_hostname = False
                ssl_ctx.verify_mode = _wt_ssl.CERT_NONE

                from urllib.request import urlopen, Request

                url = ("https://api.open-meteo.com/v1/forecast?"
                       "latitude={}&longitude={}"
                       "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                       "is_day,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl"
                       "&daily=weather_code,temperature_2m_max,temperature_2m_min"
                       "&timezone=auto&forecast_days=3").format(lat, lon)

                req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                try:
                    resp = urlopen(req, timeout=15, context=ssl_ctx)
                except:
                    url_http = url.replace("https://", "http://")
                    req2 = Request(url_http, headers={"User-Agent": "Mozilla/5.0"})
                    resp = urlopen(req2, timeout=15)

                raw = resp.read().decode('utf-8')
                data = _wt_json.loads(raw)
                data["_display_name"] = display_name
                data["_query_city"] = city

                persistent.weather_city = city
                hist = persistent.weather_history or []
                if city in hist:
                    hist.remove(city)
                hist.insert(0, city)
                persistent.weather_history = hist[:8]
                renpy.save_persistent()

                store._weather_data = data
                store._weather_error = ""
            except Exception as e:
                store._weather_data = None
                store._weather_error = "网络连接失败"

            store._weather_loading = False
            renpy.restart_interaction()

        t = _wt_threading.Thread(target=_do_fetch)
        t.daemon = True
        t.start()

    def weather_refresh():
        if persistent.weather_city:
            weather_fetch(persistent.weather_city)

    def weather_select_city(city):
        store._weather_city_input = city
        weather_fetch(city)

    def weather_search():
        c = store._weather_city_input.strip()
        if c:
            weather_fetch(c)

    def weather_open_search():
        store._weather_show_search = True
        store._weather_city_input = ""
        renpy.restart_interaction()

    def weather_close_search():
        store._weather_show_search = False
        renpy.restart_interaction()

    def weather_clear_history():
        persistent.weather_history = []
        renpy.save_persistent()
        renpy.restart_interaction()


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_weather():
    # 自动加载上次查询的城市
    if persistent.weather_city and not _weather_data and not _weather_loading and not _weather_error and not _weather_show_search:
        timer 0.1 action Function(weather_refresh)

    fixed:
        xfill True yfill True

        if _weather_show_search or (not persistent.weather_city and not _weather_loading and not _weather_data):
            # ══ 搜索 / 选择城市 ══
            frame:
                xfill True ysize 50
                background Solid("#1a2a3a")
                padding (14, 10)
                hbox:
                    xfill True yalign 0.5
                    vbox:
                        spacing 1
                        text "选择城市" size 14 color "#6ab8d8" bold True
                        text "输入或点击下方城市" size 9 color "#ffffff55"
                    if persistent.weather_city:
                        textbutton "返回":
                            action Function(weather_close_search)
                            text_size 11 text_color "#ffffff66" text_hover_color "#ffffff"
                            xalign 1.0 yalign 0.5

            # 搜索框
            frame:
                ypos 54 xfill True ysize 50
                background Solid("#0d1a22")
                padding (12, 8)
                hbox:
                    spacing 8 xfill True yalign 0.5
                    frame:
                        xsize 200 ysize 32
                        background Solid("#1a2a3a")
                        padding (10, 6)
                        input:
                            value VariableInputValue("_weather_city_input")
                            color "#ffffff" size 12
                            xsize 180 pixel_width 180
                    button:
                        xsize 60 ysize 32
                        background Solid("#6ab8d833")
                        hover_background Solid("#6ab8d855")
                        action Function(weather_search)
                        text "搜索" align (0.5, 0.5) size 12 color "#6ab8d8" bold True

            viewport:
                ypos 108 ysize 410
                xfill True mousewheel True scrollbars None

                vbox:
                    spacing 8 xfill True

                    if persistent.weather_history:
                        hbox:
                            xfill True
                            text "最近搜索" size 10 color "#ffffff55" xoffset 14
                            textbutton "清空":
                                action Function(weather_clear_history)
                                text_size 9 text_color "#ffffff33" text_hover_color "#ff8888"
                                xalign 1.0 xoffset -14

                        for _row_start in range(0, len(persistent.weather_history), 3):
                            hbox:
                                spacing 6 xoffset 14
                                for _hi in range(_row_start, min(_row_start + 3, len(persistent.weather_history))):
                                    $ _hcity = persistent.weather_history[_hi]
                                    button:
                                        xsize 84 ysize 32
                                        background Solid("#6ab8d815")
                                        hover_background Solid("#6ab8d833")
                                        action Function(weather_select_city, _hcity)
                                        text "[_hcity]" align (0.5, 0.5) size 11 color "#6ab8d8"

                        null height 6

                    text "常用城市" size 10 color "#ffffff55" xoffset 14

                    for _row_start in range(0, len(_WEATHER_CITIES), 3):
                        hbox:
                            spacing 6 xoffset 14
                            for _ci in range(_row_start, min(_row_start + 3, len(_WEATHER_CITIES))):
                                $ _city = _WEATHER_CITIES[_ci]
                                button:
                                    xsize 84 ysize 36
                                    background Solid("#1a2a3a")
                                    hover_background Solid("#2a4a5a")
                                    action Function(weather_select_city, _city)
                                    text "[_city]" align (0.5, 0.5) size 12 color "#ffffffcc"

        elif _weather_loading:
            # ══ 加载中 ══
            frame:
                xfill True yfill True
                background Solid("#0d1a22")
                padding (20, 20)
                vbox:
                    align (0.5, 0.45) spacing 14
                    frame:
                        xsize 80 ysize 80
                        background Solid("#1a3a4a")
                        xalign 0.5
                        text "☁" align (0.5, 0.5) size 40 color "#6ab8d8"
                    text "正在获取天气" size 16 color "#ffffff" xalign 0.5 bold True
                    text "请稍候……" size 11 color "#6ab8d888" xalign 0.5

        elif _weather_error:
            # ══ 错误 ══
            frame:
                xfill True yfill True
                background Solid("#0d1a22")
                padding (24, 24)

                vbox:
                    align (0.5, 0.4) spacing 14

                    frame:
                        xsize 80 ysize 80
                        background Solid("#3a1a1a")
                        xalign 0.5
                        text "✕" align (0.5, 0.5) size 36 color "#ff8888" bold True

                    text "找不到这个城市" size 16 color "#ffffff" xalign 0.5 bold True
                    null height 4

                    frame:
                        xsize 240
                        background Solid("#1a2a3a")
                        padding (12, 8)
                        xalign 0.5
                        text "[_weather_error]" size 10 color "#ffffff77" text_align 0.5 xalign 0.5

                    null height 6
                    text "请检查城市名是否正确" size 9 color "#ffffff44" xalign 0.5
                    null height 6

                    button:
                        xsize 160 ysize 38
                        xalign 0.5
                        background Solid("#6ab8d833")
                        hover_background Solid("#6ab8d855")
                        action Function(weather_open_search)
                        text "重新搜索" align (0.5, 0.5) size 14 color "#6ab8d8" bold True

                    if persistent.weather_city:
                        textbutton "返回上一个城市":
                            action Function(weather_refresh)
                            text_size 11 text_color "#ffffff66" text_hover_color "#ffffff"
                            xalign 0.5

        elif _weather_data:
            # ══ 天气显示 ══
            $ _wd = _weather_data
            $ _disp_name = _wd.get("_display_name", "")

            python:
                try:
                    _cur = _wd.get("current", {})
                    _temp = round(float(_cur.get("temperature_2m", 0)))
                    _feels = round(float(_cur.get("apparent_temperature", 0)))
                    _humidity = int(_cur.get("relative_humidity_2m", 0))
                    _wind_kmh = round(float(_cur.get("wind_speed_10m", 0)))
                    _wind_dir_deg = _cur.get("wind_direction_10m")
                    _wind_dir_str = weather_wind_dir(_wind_dir_deg)
                    _code = _cur.get("weather_code", 0)
                    _wdesc, _wicon = weather_om_get_icon(_code)
                    _pressure = int(float(_cur.get("pressure_msl", 0)))
                    _is_day = _cur.get("is_day", 1)

                    _daily = _wd.get("daily", {})
                    _d_dates = _daily.get("time", [])
                    _d_codes = _daily.get("weather_code", [])
                    _d_max = _daily.get("temperature_2m_max", [])
                    _d_min = _daily.get("temperature_2m_min", [])

                    _fc_list = []
                    for _di in range(min(3, len(_d_dates))):
                        _fdesc, _ficon = weather_om_get_icon(_d_codes[_di] if _di < len(_d_codes) else 0)
                        _fc_list.append({
                            "date": _d_dates[_di][5:] if len(_d_dates[_di]) >= 10 else _d_dates[_di],
                            "max": round(float(_d_max[_di])) if _di < len(_d_max) else "?",
                            "min": round(float(_d_min[_di])) if _di < len(_d_min) else "?",
                            "desc": _fdesc,
                            "icon": _ficon,
                        })
                except:
                    _temp = "?"
                    _feels = "?"
                    _humidity = "?"
                    _wind_kmh = "?"
                    _wind_dir_str = "—"
                    _wdesc = "未知"
                    _wicon = "❓"
                    _pressure = "?"
                    _is_day = 1
                    _fc_list = []

            # 整体纯色背景
            if _is_day:
                add Solid("#3a6a95")
            else:
                add Solid("#0f1530")

            # ══ 顶部 城市信息 ══
            frame:
                xfill True ysize 50
                background None
                padding (16, 12)
                ypos 0

                hbox:
                    xfill True yalign 0.5
                    vbox:
                        spacing 1
                        text "[_disp_name]" size 13 color "#ffffff" bold True
                        text "实时天气" size 9 color "#ffffffaa"
                    textbutton "搜索":
                        action Function(weather_open_search)
                        text_size 11 text_color "#ffffffaa" text_hover_color "#ffffff"
                        xalign 1.0 yalign 0.5

            # ══ 主温度区（纯垂直居中）══
            vbox:
                ypos 56 xfill True spacing 4

                # 大图标
                text "[_wicon]" size 70 xalign 0.5

                null height 4

                # 大温度数字
                text "[_temp]°" size 78 color "#ffffff" xalign 0.5 font "DejaVuSans.ttf"

                # 天气描述
                text "[_wdesc]" size 16 color "#ffffffdd" xalign 0.5

                # 体感温度
                text "体感温度 [_feels]°" size 11 color "#ffffff88" xalign 0.5

            # ══ 详情卡片 ══
            frame:
                ypos 290 xpos 12
                xsize 292 ysize 78
                background Solid("#ffffff15")
                padding (6, 8)

                hbox:
                    xfill True yalign 0.5

                    # 湿度
                    vbox:
                        xsize 71 yalign 0.5 spacing 3
                        text "湿度" size 9 color "#ffffffaa" xalign 0.5
                        text "[_humidity]%" size 16 color "#ffffff" xalign 0.5 font "DejaVuSans.ttf"

                    add Solid("#ffffff22") xsize 1 ysize 50

                    # 风速
                    vbox:
                        xsize 71 yalign 0.5 spacing 3
                        text "风速" size 9 color "#ffffffaa" xalign 0.5
                        hbox:
                            xalign 0.5 spacing 2
                            text "[_wind_kmh]" size 16 color "#ffffff" font "DejaVuSans.ttf" yalign 1.0
                            text "km/h" size 8 color "#ffffff88" yalign 1.0

                    add Solid("#ffffff22") xsize 1 ysize 50

                    # 风向
                    vbox:
                        xsize 71 yalign 0.5 spacing 3
                        text "风向" size 9 color "#ffffffaa" xalign 0.5
                        text "[_wind_dir_str]" size 16 color "#ffffff" xalign 0.5

                    add Solid("#ffffff22") xsize 1 ysize 50

                    # 气压
                    vbox:
                        xsize 71 yalign 0.5 spacing 3
                        text "气压" size 9 color "#ffffffaa" xalign 0.5
                        hbox:
                            xalign 0.5 spacing 2
                            text "[_pressure]" size 15 color "#ffffff" font "DejaVuSans.ttf" yalign 1.0
                            text "hPa" size 8 color "#ffffff88" yalign 1.0

            # ══ 三日预报卡片 ══
            frame:
                ypos 376 xpos 12
                xsize 292 ysize 138
                background Solid("#ffffff15")
                padding (14, 10)

                vbox:
                    spacing 6 xfill True

                    text "三日预报" size 10 color "#ffffffaa"
                    add Solid("#ffffff22") xsize 260 ysize 1
                    null height 2

                    if _fc_list:
                        for _fi in range(len(_fc_list)):
                            $ _fc = _fc_list[_fi]
                            $ _fdate = _fc["date"]
                            $ _fmax = _fc["max"]
                            $ _fmin = _fc["min"]
                            $ _fdesc = _fc["desc"]
                            $ _ficon = _fc["icon"]
                            $ _flabel = "今天" if _fi == 0 else ("明天" if _fi == 1 else "后天")

                            hbox:
                                xfill True ysize 28 yalign 0.5

                                # 日期标签（左）
                                vbox:
                                    spacing 0 xsize 48 yalign 0.5
                                    text "[_flabel]" size 11 color "#ffffff" bold True
                                    text "[_fdate]" size 8 color "#ffffff88"

                                # 图标
                                text "[_ficon]" size 20 yalign 0.5 xsize 32

                                # 描述
                                text "[_fdesc]" size 10 color "#ffffffcc" yalign 0.5 xsize 80

                                # 温度范围（右对齐）
                                hbox:
                                    spacing 4 xalign 1.0 yalign 0.5
                                    text "[_fmin]°" size 12 color "#ffffff88" font "DejaVuSans.ttf"
                                    text "/" size 10 color "#ffffff44"
                                    text "[_fmax]°" size 12 color "#ffffff" font "DejaVuSans.ttf"

                    else:
                        text "暂无预报数据" size 10 color "#ffffff44" xalign 0.5

            # ══ 底部 刷新 + 数据来源 ══
            frame:
                ypos 522 xfill True ysize 30
                background None
                padding (16, 4)
                hbox:
                    xfill True yalign 0.5
                    textbutton "刷新":
                        action Function(weather_refresh)
                        text_size 11 text_color "#ffffffaa" text_hover_color "#ffffff"
                        yalign 0.5
                    text "Open-Meteo" size 8 color "#ffffff44" xalign 1.0 yalign 0.5
