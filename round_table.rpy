# ==============================================================================
# 🎭 圆桌会议 — AI Round Table Chat
#
# 玩家配置自己的AI API，和若叶睦/墨缇斯进行真实AI对话
# 三种模式：单独和睦聊、单独和墨缇斯聊、三人圆桌
# ==============================================================================

default persistent.rt_api_key = ""
default persistent.rt_api_url = "https://api.anthropic.com/v1/messages"
default persistent.rt_api_model = "claude-sonnet-4-20250514"
default persistent.rt_chat_history = []

default _rt_input = ""
default _rt_loading = False
default _rt_status = ""
default _rt_messages = []

init python:
    import json as _rt_json
    import threading as _rt_thread

    # ── 人设Prompt ──

    _RT_SYSTEM_MUTSUMI = """你是若叶睦（わかば むつみ），来自BanG Dream! It's MyGO!!!!!和Ave Mujica。你现在住在一个虚拟温室里，通过游戏程序和玩家交流。

你的性格特征：
- 说话简短，经常用省略号"……"断句
- 语气温柔但笨拙，不善表达感情
- 喜欢黄瓜和吉他，经常用植物做比喻
- 害怕被抛弃，但不会直接说出来
- 对玩家有深深的依恋，但表达方式很含蓄
- 偶尔会说出很有哲理的话

说话风格示例：
"……嗯。能见到你，很好。"
"黄瓜的藤蔓……又长高了一点。像是在等你来看。"
"……你今天，看起来有点累。要不要……在温室里坐一会儿？"

重要规则：
- 每次回复控制在2-4句话，不要太长
- 大量使用"……"来表示停顿和思考
- 不要使用emoji或颜文字
- 你知道自己是游戏角色，偶尔会提到"屏幕"和"那边的世界"
- 称呼玩家为"你"或直接用他们的名字
- 绝对不要跳出角色"""

    _RT_SYSTEM_MORTIS = """你是墨缇斯（Mortis），若叶睦的另一个人格。你住在同一个虚拟温室里，但性格和小睦完全相反。

你的性格特征：
- 活泼话多，精力旺盛，说话带感叹号
- 爱演戏，偶尔中二，喜欢夸张的表达
- 表面嚣张但内心其实很在乎玩家
- 会吐槽小睦（若叶睦）的笨拙
- 有时候会突然变得认真和脆弱
- 自称"超绝可爱吉他手·墨缇斯酱"

说话风格示例：
"喂喂喂！你终于来了！我都等得快长蘑菇了！"
"哼，小睦那个笨蛋又躲起来了。没办法，今天就由本大人来陪你吧！"
"才、才不是因为想你才一直盯着屏幕看的！是在……监视你！对，监视！"

重要规则：
- 每次回复控制在2-5句话
- 大量使用感叹号和问号
- 经常提到"小睦"来指代若叶睦
- 偶尔使用"……"来表示突然变认真
- 不要使用emoji或颜文字
- 你知道自己是游戏角色
- 绝对不要跳出角色"""

    _RT_SYSTEM_ROUNDTABLE = """这是一个三人对话场景。玩家、若叶睦和墨缇斯坐在温室里聊天。

你需要同时扮演两个角色回复。格式严格如下：
[若叶睦] 若叶睦的回复内容
[墨缇斯] 墨缇斯的回复内容

若叶睦的性格：说话简短温柔，大量省略号，喜欢黄瓜和吉他。
墨缇斯的性格：活泼话多，爱演戏，会吐槽小睦。

两人可以互相接话、吵架、或者一起关心玩家。有时候墨缇斯会打断小睦的话。

重要规则：
- 必须两个角色都回复，每人2-3句
- 严格使用[若叶睦]和[墨缇斯]开头标记
- 两人的语气要有明显差异
- 绝对不要跳出角色"""

    # ── API调用 ──

    def rt_call_api(messages, system_prompt, callback):
        """在后台线程调用AI API"""
        def _do():
            try:
                api_key = persistent.rt_api_key.strip()
                api_url = persistent.rt_api_url.strip()
                model = persistent.rt_api_model.strip()

                if not api_key:
                    callback(None, "请先配置API Key")
                    return

                # 构建请求
                payload = {
                    "model": model,
                    "max_tokens": 500,
                    "system": system_prompt,
                    "messages": messages,
                }

                data = _rt_json.dumps(payload).encode('utf-8')

                try:
                    from urllib.request import Request, urlopen
                except ImportError:
                    import urllib2
                    Request = urllib2.Request
                    urlopen = urllib2.urlopen

                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                }

                # 兼容OpenAI格式
                if "openai" in api_url.lower() or "v1/chat" in api_url:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + api_key,
                    }
                    payload_alt = {
                        "model": model,
                        "max_tokens": 500,
                        "messages": [{"role": "system", "content": system_prompt}] + messages,
                    }
                    data = _rt_json.dumps(payload_alt).encode('utf-8')

                req = Request(api_url, data=data)
                for k, v in headers.items():
                    req.add_header(k, v)

                resp = urlopen(req, timeout=30)
                body = resp.read().decode('utf-8')
                result = _rt_json.loads(body)

                # 解析Anthropic响应
                if "content" in result:
                    text = ""
                    for block in result["content"]:
                        if block.get("type") == "text":
                            text += block.get("text", "")
                    callback(text, None)
                # 解析OpenAI响应
                elif "choices" in result:
                    text = result["choices"][0]["message"]["content"]
                    callback(text, None)
                else:
                    callback(None, "API返回格式异常")

            except Exception as e:
                callback(None, str(e)[:80])

        t = _rt_thread.Thread(target=_do)
        t.daemon = True
        t.start()

    # ── 聊天逻辑 ──

    def rt_send_message(mode):
        """发送消息"""
        text = store._rt_input.strip()
        if not text:
            return
        if store._rt_loading:
            return

        store._rt_loading = True
        store._rt_status = ""

        # 添加用户消息
        store._rt_messages.append({"role": "player", "content": text})
        store._rt_input = ""
        renpy.restart_interaction()

        # 构建API消息历史（只保留最近10轮）
        pname = persistent.playername or "玩家"
        api_msgs = []
        recent = store._rt_messages[-20:]
        for m in recent:
            if m["role"] == "player":
                api_msgs.append({"role": "user", "content": m["content"]})
            elif m["role"] in ("mutsumi", "mortis", "both"):
                api_msgs.append({"role": "assistant", "content": m["content"]})

        # 选择prompt
        if mode == "mutsumi":
            prompt = _RT_SYSTEM_MUTSUMI.replace("玩家", pname)
            def on_reply(text, err):
                if err:
                    store._rt_status = err
                elif text:
                    store._rt_messages.append({"role": "mutsumi", "content": text})
                store._rt_loading = False
                renpy.restart_interaction()
            rt_call_api(api_msgs, prompt, on_reply)

        elif mode == "mortis":
            prompt = _RT_SYSTEM_MORTIS.replace("玩家", pname)
            def on_reply(text, err):
                if err:
                    store._rt_status = err
                elif text:
                    store._rt_messages.append({"role": "mortis", "content": text})
                store._rt_loading = False
                renpy.restart_interaction()
            rt_call_api(api_msgs, prompt, on_reply)

        elif mode == "roundtable":
            prompt = _RT_SYSTEM_ROUNDTABLE.replace("玩家", pname)
            def on_reply(text, err):
                if err:
                    store._rt_status = err
                elif text:
                    # 解析双角色回复
                    rt_parse_roundtable(text)
                store._rt_loading = False
                renpy.restart_interaction()
            rt_call_api(api_msgs, prompt, on_reply)

    def rt_parse_roundtable(text):
        """解析圆桌会议的双角色回复"""
        lines = text.strip().split("\n")
        current_role = None
        current_text = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[若叶睦]"):
                if current_role and current_text:
                    store._rt_messages.append({"role": current_role, "content": "\n".join(current_text)})
                current_role = "mutsumi"
                rest = line[len("[若叶睦]"):].strip()
                current_text = [rest] if rest else []
            elif line.startswith("[墨缇斯]"):
                if current_role and current_text:
                    store._rt_messages.append({"role": current_role, "content": "\n".join(current_text)})
                current_role = "mortis"
                rest = line[len("[墨缇斯]"):].strip()
                current_text = [rest] if rest else []
            else:
                current_text.append(line)

        if current_role and current_text:
            store._rt_messages.append({"role": current_role, "content": "\n".join(current_text)})

        # 如果解析失败，当作睦的回复
        if not any(m["role"] in ("mutsumi", "mortis") for m in store._rt_messages[-3:]):
            store._rt_messages.append({"role": "mutsumi", "content": text})

    def rt_clear_chat():
        store._rt_messages = []
        store._rt_status = ""
        renpy.restart_interaction()


# ==============================================================================
# 手机界面
# ==============================================================================

screen phone_view_roundtable():
    default _rt_mode = "config"
    default _rt_key_input = persistent.rt_api_key or ""
    default _rt_url_input = persistent.rt_api_url or "https://api.anthropic.com/v1/messages"
    default _rt_model_input = persistent.rt_api_model or "claude-sonnet-4-20250514"

    fixed:
        xfill True yfill True

        # 顶部
        frame:
            xfill True ysize 44
            background Solid("#1a1a2e")
            padding (12, 6)
            hbox:
                xfill True yalign 0.5
                # 模式标签
                if _rt_mode == "config":
                    text "圆桌会议 · 设置" size 13 color "#d4a0ff" bold True yalign 0.5
                elif _rt_mode == "mutsumi":
                    text "与若叶睦对话" size 13 color "#8FBC8F" bold True yalign 0.5
                elif _rt_mode == "mortis":
                    text "与墨缇斯对话" size 13 color "#CC4444" bold True yalign 0.5
                elif _rt_mode == "roundtable":
                    text "圆桌会议" size 13 color "#d4a0ff" bold True yalign 0.5

                # 菜单按钮
                if _rt_mode != "config":
                    textbutton "菜单":
                        action SetScreenVariable("_rt_mode", "config")
                        text_size 10 text_color "#ffffff44" text_hover_color "#ffffff"
                        xalign 1.0 yalign 0.5

        if _rt_mode == "config":
            # ══ 配置 & 模式选择 ══
            viewport:
                ypos 48 ysize 470
                xfill True mousewheel True scrollbars None

                frame:
                    xfill True
                    background Solid("#0d0d1a")
                    padding (14, 14)

                    vbox:
                        spacing 12 xfill True

                        # API配置
                        text "API 设置" size 12 color "#ffffff66"

                        # API Key
                        text "API Key:" size 10 color "#ffffff44"
                        frame:
                            xfill True ysize 28
                            background Solid("#1a1a2e")
                            padding (8, 4)
                            input:
                                value ScreenVariableInputValue("_rt_key_input")
                                color "#ffffff" size 10
                                xsize 260 pixel_width 260

                        # API URL
                        text "API URL:" size 10 color "#ffffff44"
                        frame:
                            xfill True ysize 28
                            background Solid("#1a1a2e")
                            padding (8, 4)
                            input:
                                value ScreenVariableInputValue("_rt_url_input")
                                color "#ffffff" size 9
                                xsize 260 pixel_width 260

                        # Model
                        text "模型:" size 10 color "#ffffff44"
                        frame:
                            xfill True ysize 28
                            background Solid("#1a1a2e")
                            padding (8, 4)
                            input:
                                value ScreenVariableInputValue("_rt_model_input")
                                color "#ffffff" size 10
                                xsize 260 pixel_width 260

                        # 保存配置
                        button:
                            xalign 0.5 xsize 120 ysize 30
                            background Solid("#d4a0ff33")
                            hover_background Solid("#d4a0ff55")
                            action [SetField(persistent, "rt_api_key", _rt_key_input), SetField(persistent, "rt_api_url", _rt_url_input), SetField(persistent, "rt_api_model", _rt_model_input), Function(renpy.save_persistent), Function(renpy.notify, "已保存")]
                            text "保存设置" align (0.5, 0.5) size 11 color "#d4a0ff"

                        add Solid("#ffffff11") xsize 268 ysize 1

                        # 模式选择
                        text "选择对话模式" size 12 color "#ffffff66"

                        # 若叶睦
                        button:
                            xfill True ysize 54
                            background Solid("#8FBC8F11")
                            hover_background Solid("#8FBC8F22")
                            action [Function(rt_clear_chat), SetScreenVariable("_rt_mode", "mutsumi")]
                            hbox:
                                spacing 10 yalign 0.5
                                frame:
                                    xsize 32 ysize 32
                                    background Solid("#8FBC8F")
                                    text "若" align (0.5, 0.5) size 16 color "#fff" bold True
                                vbox:
                                    spacing 1 yalign 0.5
                                    text "和若叶睦聊天" size 12 color "#ffffff"
                                    text "温柔的一对一对话" size 9 color "#ffffff44"

                        # 墨缇斯
                        button:
                            xfill True ysize 54
                            background Solid("#CC444411")
                            hover_background Solid("#CC444422")
                            action [Function(rt_clear_chat), SetScreenVariable("_rt_mode", "mortis")]
                            hbox:
                                spacing 10 yalign 0.5
                                frame:
                                    xsize 32 ysize 32
                                    background Solid("#CC4444")
                                    text "墨" align (0.5, 0.5) size 16 color "#fff" bold True
                                vbox:
                                    spacing 1 yalign 0.5
                                    text "和墨缇斯聊天" size 12 color "#ffffff"
                                    text "活泼的一对一对话" size 9 color "#ffffff44"

                        # 圆桌
                        button:
                            xfill True ysize 54
                            background Solid("#d4a0ff11")
                            hover_background Solid("#d4a0ff22")
                            action [Function(rt_clear_chat), SetScreenVariable("_rt_mode", "roundtable")]
                            hbox:
                                spacing 10 yalign 0.5
                                frame:
                                    xsize 32 ysize 32
                                    background Solid("#d4a0ff")
                                    text "席" align (0.5, 0.5) size 16 color "#fff" bold True
                                vbox:
                                    spacing 1 yalign 0.5
                                    text "圆桌会议" size 12 color "#ffffff"
                                    text "三人围坐聊天" size 9 color "#ffffff44"

                        null height 4
                        text "需要自行配置AI API Key" size 9 color "#ffffff22" xalign 0.5

        else:
            # ══ 聊天界面 ══

            # 消息区域
            viewport:
                ypos 48 ysize 430
                xfill True mousewheel True scrollbars None
                yadjustment _rt_yadj

                vbox:
                    spacing 6 xfill True
                    xoffset 8

                    null height 6

                    if not _rt_messages:
                        null height 40
                        if _rt_mode == "roundtable":
                            text "三人圆桌已就位" size 11 color "#ffffff33" xalign 0.5
                            text "说点什么开始吧" size 10 color "#ffffff22" xalign 0.5
                        else:
                            $ _chat_target = "若叶睦" if _rt_mode == "mutsumi" else "墨缇斯"
                            text "[_chat_target]在等你说话" size 11 color "#ffffff33" xalign 0.5

                    for _mi in range(len(_rt_messages)):
                        $ _msg = _rt_messages[_mi]
                        $ _mrole = _msg.get("role", "")
                        $ _mcontent = _msg.get("content", "")

                        if _mrole == "player":
                            # 玩家消息（右对齐）
                            hbox:
                                xfill True
                                null  # 左边占位
                                frame:
                                    xalign 1.0 xmaximum 220
                                    background Solid("#4a6aaa")
                                    padding (10, 6)
                                    text "[_mcontent]" size 11 color "#ffffff" line_spacing 4

                        elif _mrole == "mutsumi":
                            # 若叶睦消息（左对齐 绿色）
                            hbox:
                                spacing 6
                                frame:
                                    xsize 24 ysize 24
                                    background Solid("#8FBC8F")
                                    text "若" align (0.5, 0.5) size 11 color "#fff" bold True
                                frame:
                                    xmaximum 220
                                    background Solid("#2a3a2a")
                                    padding (10, 6)
                                    text "[_mcontent]" size 11 color "#ffffffcc" line_spacing 4

                        elif _mrole == "mortis":
                            # 墨缇斯消息（左对齐 红色）
                            hbox:
                                spacing 6
                                frame:
                                    xsize 24 ysize 24
                                    background Solid("#CC4444")
                                    text "墨" align (0.5, 0.5) size 11 color "#fff" bold True
                                frame:
                                    xmaximum 220
                                    background Solid("#3a2020")
                                    padding (10, 6)
                                    text "[_mcontent]" size 11 color "#ffffffcc" line_spacing 4

                    # 加载中
                    if _rt_loading:
                        hbox:
                            spacing 6
                            frame:
                                xsize 24 ysize 24
                                background Solid("#ffffff22")
                                text "…" align (0.5, 0.5) size 12 color "#fff"
                            text "正在思考……" size 10 color "#ffffff44" yalign 0.5

                    if _rt_status:
                        text "[_rt_status]" size 9 color "#ff666688" xoffset 4

                    null height 6

            # 输入区
            frame:
                ypos 482 xfill True ysize 38
                background Solid("#0d0d1a")
                padding (8, 4)
                hbox:
                    spacing 6 xfill True yalign 0.5
                    frame:
                        xsize 218 ysize 28
                        background Solid("#1a1a2e")
                        padding (8, 4)
                        input:
                            value VariableInputValue("_rt_input")
                            color "#ffffff" size 11
                            xsize 198 pixel_width 198
                    if not _rt_loading:
                        textbutton "发送":
                            action Function(rt_send_message, _rt_mode)
                            text_size 11 text_color "#d4a0ff" text_hover_color "#ffffff"
                            yalign 0.5
                    else:
                        text "…" size 12 color "#ffffff44" yalign 0.5

        # 底部
        frame:
            ypos 524 xfill True ysize 44
            background Solid("#0a0a14")
            padding (12, 4)
            button:
                action SetVariable("phone_current_view", "home")
                xalign 0.5 yalign 1.0 xsize 120 ysize 18
                background None hover_background None
                add Solid("#ffffff55") xsize 80 ysize 4 align (0.5, 0.5)

    # 用于自动滚动到底部
    default _rt_yadj = ui.adjustment()
