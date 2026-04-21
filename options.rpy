## 此文件包含有可自定义您游戏的设置。
##
## 以“##”开头的语句是注释，您不应该对其取消注释。以“#”开头的语句是注释掉的代码，
## 在适用的时候您可能需要对其取消注释。


## 基础 ##########################################################################

## 用户可读的游戏名称。此命令用来设置默认窗口标题，并且会在界面和错误报告中出
## 现。
##
## 带有 _() 的字符串表示其可被翻译。

init python:
    # 强制修改渲染器优先级
    # 建议顺序：'angle' (Windows最佳) -> 'gl2' -> 'gl' -> 'sw' (软件渲染，保底)
    config.renderer = "angle" 
    
    # 如果你想让 Ren'Py 自动选择但避开某些有问题的渲染器，可以使用：
    # config.gl_test_charts = [ ("angle", 1), ("gl2", 2), ("gl", 3), ("sw", 4) ]
    

define config.name = _("Just Mutsumi")


## 决定上面给出的标题是否显示在标题界面屏幕。设置为 False 来隐藏标题。

define gui.show_name = False


## 游戏版本号。

define config.version = "M0.22"


## 放置在游戏内“关于”屏幕上的文本。将文本放在三个引号之间，并在段落之间留出空
## 行。

define gui.about = _p("""《Just Mutsumi》是基于原作动画「BanG Dream! It's MyGO!!!!!」以及「BanG Dream! Ave Mujica」，以搞笑艺人若叶隆文与知名演员森美奈美的女儿「若叶睦」为主角的互动小说。
""")


## 在构建的发布版中，可执行文件和目录所使用的短名称。此处仅限使用 ASCII 字符，并
## 且不能包含空格、冒号或分号。

define build.name = "JustMutsumi"


## 音效和音乐 #######################################################################

# 控制设置菜单中的音量设置显示
# 音效，建议保留为 True
define config.has_sound = True

# 背景音乐，建议保留为 True
define config.has_music = True

# 语音，如果有语音则为 True，否则为 False
define config.has_voice = True


# 这里控制主菜单的背景音乐。
define config.main_menu_music = audio.bgm1


## 转场 ##########################################################################
##
## 这些变量用来控制某些事件发生时的转场。每一个变量都应设置成一个转场，或者是
## None 来表示无转场。



# 这是进入和退出游戏菜单时使用的转场。
# Dissolve(.2) 相当于转场特效。
# config.enter_transition 控制进入游戏菜单时使用的转场。
# config.exit_transition 控制退出游戏菜单 / 返回游戏时使用的转场。
define config.enter_transition = Dissolve(.2)
define config.exit_transition = Dissolve(.2)


## 在游戏结束之后进入主菜单时使用的转场。

define config.end_game_transition = Dissolve(.5)


## 用于控制在游戏开始标签不存在时转场的变量。作为替代，在显示初始化场景后使用
## with 语句。


## 窗口管理 ########################################################################
##
## 此命令控制对话框窗口何时显示。若为 show，对话框将总是显示。若为 hide，对话框
## 仅在对话出现时显示。若为 auto，对话框会在 scene 语句前隐藏，并在有新对话时重
## 新显示。
##
## 在游戏开始后，可以用 window show、window hide 和 window auto 语句来改变其状
## 态。

define config.window = "auto"


## 用于显示和隐藏对话框窗口的转场

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## 默认设置 ########################################################################

## 控制默认的文字显示速度。默认的 0 为瞬间，而其他数字则是每秒显示出的字符数。

default preferences.text_cps = 40


## 默认的自动前进延迟。数字越大，等待时间越长，有效范围为 0 - 30。

default preferences.afm_time = 15
default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.75

## 存档目录 ########################################################################
##
## 控制 Ren'Py 放置游戏存档的特定操作系统目录。存档文件将放置在：
##
## Windows：%APPDATA\RenPy\<config.save_directory>
##
## Macintosh：$HOME/Library/RenPy/<config.save_directory>
##
## Linux：$HOME/.renpy/<config.save_directory>
##
## 该语句通常不应变更，若要变更，应为有效字符串而不是表达式。

define config.save_directory = "JustMutsumi-1766760565"


## 图标 ##########################################################################
##
## 在任务栏或 Dock 上显示的图标。

define config.window_icon = "gui/window_icon.png"
# This controls whether your mod allows skipping dialogue.
define config.allow_skipping = True

# This controls whether your mod saves automatically.
define config.has_autosave = False

# This controls whether you mod saves when quitting the game.
define config.autosave_on_quit = False

# This controls the number of slots auto-saving can use
define config.autosave_slots = 0

# This controls the layers of screens, images, and more. 
# Best not to leave this alone.
define config.layers = [ 'master', 'transient', 'screens', 'overlay', 'front' ]

## 构建配置 ########################################################################
##
## 此部分控制 Ren'Py 如何将您的项目转变为发行版文件。

init python:

    ## 以下函数接受文件模式。文件模式不区分大小写，并与基础目录的相对路径相匹配，
    ## 包括或不包括 /。如果多个模式匹配，则使用第一个模式。
    ##
    ## 在一个模式中：
    ##
    ## / 是目录分隔符。
    ##
    ## * 匹配所有字符，目录分隔符除外。
    ##
    ## ** 匹配所有字符，包括目录分隔符。
    ##
    ## 例如，“*.txt”匹配基础目录中的 txt 文件，“game/**.ogg”匹配游戏目录或任何子
    ## 目录中的 ogg 文件，“**.psd”匹配项目中任何位置的 psd 文件。

    ## 将文件列为 None 来使其从构建的发行版中排除。

## 基础排除（保持不变）
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## 资源打包进 archive.rpa
    build.classify('game/**.png', 'archive')
    build.classify('game/**.jpg', 'archive')
    build.classify('game/**.mp3', 'archive')
    build.classify('game/**.ogg', 'archive')
    
    ## 脚本加密核心：
    build.classify('game/**.rpyc', 'archive') # 打包编译后的二进制脚本
    build.classify('game/**.rpy', None)       # 彻底排除原始代码文件！极其重要
    build.classify('game/**.txt', None)       # 如果 txt 里有敏感信息，也设为 None

    ## 若要封装文件，需将其列为“archive”。

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## 匹配为文档模式的文件会在 Mac 应用程序构建中被复制，因此它们同时出现在 APP
    ## 和 ZIP 文件中。

    build.documentation('*.html')
    build.documentation('*.txt')


## 执行应用内购需要一个 Google Play 许可密钥。许可密钥可以在 Google Play 开发者
## 控制台的“Monetize” > “Monetization Setup” > “Licensing”页面找到。

# define build.google_play_key = "..."


## 与 itch.io 项目相关的用户名和项目名，以 / 分隔。

# define build.itch_project = "renpytom/test-project"

# 最好也不要动这一块。
#这些全是“引擎级性能/行为微调”：
#前两条（cache_size、predict_statements）在“多缓存、早加载”，让高清素材切图更流畅；
#第三条按开发/发行模式自动开关后退功能；
#第四条保证菜单弹出时不会残留 front 层的临时图；

define config.image_cache_size = 64
define config.predict_statements = 50
define config.rollback_enabled = config.developer
define config.menu_clear_layers = ["front"]


init python:
    if len(renpy.loadsave.location.locations) > 1: del(renpy.loadsave.location.locations[1])
    renpy.game.preferences.pad_enabled = False
    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s
    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)




init python:
    # 安全地禁用向下滚动 (推进对话)
    if 'mousedown_4' in config.keymap['dismiss']:
        config.keymap['dismiss'].remove('mousedown_4')
    if 'mousedown_5' in config.keymap['dismiss']:
        config.keymap['dismiss'].remove('mousedown_5')
    
    # 安全地禁用向上滚动 (回滚历史)
    if 'mousedown_4' in config.keymap['rollback']:
        config.keymap['rollback'].remove('mousedown_4')
    if 'mousedown_5' in config.keymap['rollback']:
        config.keymap['rollback'].remove('mousedown_5')

    # 注意：某些版本中滚轮向上/向下对应的数字可能反转
    # 这样写可以确保对话和回滚都不会被滚轮干扰