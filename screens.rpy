
## Initialization
################################################################################

init offset = -1

## Color Styles
################################################################################

# This controls the color of outlines in the game likeF
# text, say, navigation, labels and such.
define -2 text_outline_color = "#779977"

## Styles
################################################################################
style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

style default_monika is normal:
    slow_cps 30

style edited is default:
    font "gui/font/sourcehanserif.otf"
    kerning 8
    outlines [(10, "#000", 0, 0)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style normal is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style input:
    color gui.accent_color

style hyperlink_text:
    color "#fa82b6"
    hover_color gui.hover_color
    hover_underline True

style splash_text:
    size 24
    color "#000"
    font gui.default_font
    text_align 0.5
    outlines []

style poemgame_text:
    yalign 0.5
    font "gui/font/zhushi.ttf"
    size 30
    color "#000"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size


#style bar:
#    ysize gui.bar_size
#    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
#    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style bar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)

style scrollbar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True

style vscrollbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_invert True

#style vscrollbar:
#    xsize gui.scrollbar_size
#    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
#    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

################################################################################
## In-game screens
################################################################################
# 定义一个故障闪烁效果
transform glitch_appear:
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 0.1 alpha 0.2
    linear 0.1 alpha 1.0
    linear 0.1 alpha 0.5
    linear 0.1 alpha 1.0

## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        # ============================================================
        # 🎨 Mortis 模式 UI (V3.0 终极修正版)
        # ============================================================
        if persistent.in_mortis_mode:
            background Frame("gui/textbox_mortis.png", 20, 20) 

            xfill False 
            
            # 3. 强制居中定位
            xalign 0.5 
            
            yalign 0.97 
            xsize 950
            ysize 190
            
            # 6. 文字内边距 (上, 左, 下, 右)
            # 增加左边距，确保文字不会贴着左边框
            padding (20, 20, 20, 20)

            

        # 正常模式下，不写任何属性，让它自动读取 gui.rpy 的默认设置
        # 这样 ddlc 模式就不会坏掉
        # ============================================================

        text what id "what":
            # Mortis 模式下：文字内容居中
            if persistent.in_mortis_mode:
                font "fonts/mortis_font.otf"
                xalign 0.5        # 文本块在框内居中
                text_align 0.5    # 每一行文字都居中对齐
                color "#CCCCCC"   # 灰白色文字
                layout "subtitle" # 优化短句的居中显示

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                # 🏷️ 名字框逻辑
                if persistent.in_mortis_mode:
                    background None 
                    
                    xalign 0.5
                    yoffset 0
                    xfill False
                text who id "who":
                    if persistent.in_mortis_mode:
                        font "fonts/mortis_font.otf"
                        xalign 0.5
                        text_align 0.5
                        size 38      
                        color "#FF0000" 

    # 手机端不显示侧边头像
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    use quick_menu


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style window_monika is window:
    background Image("gui/textbox_monika.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    #outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]
    #outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

image input_caret:
    Solid("#779977")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xpos gui.text_xpos
            xanchor 0.5
            ypos gui.text_ypos

            text prompt style "input_prompt"
            input id "input"


style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

style input:
    caret "input_caret"
    xmaximum gui.text_width
    xalign 0.5
    text_align 0.5


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            if persistent.in_mortis_mode:
                textbutton i.caption action i.action:
                    style_prefix "mortis_choice" 
                    # 2. 自定义按钮背景 (黑底 + 红色细边框)
                    # Frame(..., 0, 0) 表示不进行九宫格拉伸，直接填满
                    # 如果你没有图，这里我用 Solid 代码画一个黑块
                    background Frame("gui/textbox_mortis.png", 20, 20)
                    hover_background Frame("gui/textbox_mortis.png", 20, 20)
                    xsize 1000        # 宽度
                    ysize 80          # 高度
                    xalign 0.5        # 居中
                    
                    text_xalign 0.5   # 文字水平居中
                    text_yalign 0.5   # 文字垂直居中
                    text_font "fonts/mortis_font.otf"
                    text_color "#CCCCCC"      # 默认灰色
                    text_hover_color "#FF0000" # 选中变红
                    text_size 35      # 字体大一点

            else:
                textbutton i.caption action i.action


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    idle_background Frame("gui/button/choice_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/choice_hover_background.png", gui.choice_button_borders)

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []


init python:
    def RigMouse():
        currentpos = renpy.get_mouse_pos()
        targetpos = [640, 345]
        if currentpos[1] < targetpos[1]:
            renpy.display.draw.set_mouse_pos((currentpos[0] * 9 + targetpos[0]) / 10.0, (currentpos[1] * 9 + targetpos[1]) / 10.0)

screen rigged_choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action
    
    timer 1.0/30.0 repeat True action Function(RigMouse)


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    idle_background Frame("gui/button/choice_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/choice_hover_background.png", gui.choice_button_borders)

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        # Add an in-game quick menu.
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995

            #textbutton _("Back") action Rollback()
            textbutton _("历史") action ShowMenu('history')
            textbutton _("快进") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("自动") action Preference("auto-forward", "toggle")
            textbutton _("存档") action ShowMenu('save')
            textbutton _("读档") action ShowMenu('load')
            #textbutton _("Q.存档") action QuickSave()
            #textbutton _("Q.读档") action QuickLoad()
            textbutton _("设置") action ShowMenu('preferences')
    


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
#init python:
#    config.overlay_screens.append("quick_menu")

default quick_menu = True

#style quick_button is default
#style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    outlines []


################################################################################
# Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

init python:
    def FinishEnterName():
        """处理名字输入的完成逻辑"""
        if not player or player.strip() == "":
            renpy.notify("请输入有效的名字")
            return "invalid"
        
        # 保存名字并提示成功
        persistent.playername = player.strip()
        renpy.notify("名字设置成功：{}".format(persistent.playername))
        return "success"


screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        if not persistent.autoload or not main_menu:

            if main_menu:

                textbutton _("Just若叶睦") action If(
                persistent.playername,
                true=Start(),
                false=Show(screen="name_input", message="请输入睦对你的称呼",ok_action=Function(FinishEnterName))
            )

            else:

                textbutton _("历史") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]

                textbutton _("保存") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None)]

            textbutton _("读取游戏") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None)]

            if _in_replay:

                textbutton _("结束回放") action EndReplay(confirm=True)



            textbutton _("设置") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]
   





# screens.rpy










style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/zcoolkuaile.ttf"
    color "#fff"
    outlines [(4, text_outline_color, 0, 0), (2, text_outline_color, 2, 2)]
    #outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu
screen main_menu():
    



    ## 此语句可确保替换掉任何其他菜单屏幕。
    tag menu

    add gui.main_menu_background
    add "menu_art_m1"

    ## 此空框可使标题菜单变暗。
    frame:
        style "main_menu_frame"

    ## use 语句将其他的屏幕包含进此屏幕。标题屏幕的实际内容在导航屏幕中。
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_frame:
    xsize 310
    yfill True

    background "menu_nav"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_text_size


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When this
## screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None):
    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background




    frame:

        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation



    textbutton _("返回"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    font "gui/font/zcoolkuaile.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, text_outline_color, 0, 0), (3, text_outline_color, 2, 2)]
    #outlines [(6, "#b59", 0, 0), (3, "#b59", 2, 2)]
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.






## This is redefined in options.rpy to add text to the about screen.
# define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("存档"))


screen load():

    tag menu

    use file_slots(_("读档"))

init python:
    def FileActionMod(name, page=None, **kwargs):
        if renpy.current_screen().screen_name[0] == "save":
            return Show(
                screen="dialog",
                message="没有存档的必要。\n睦不会离开你的。",
                ok_action=Hide("dialog")
            )
        # 其余情况正常存档/读档
        else:
            return FileAction(name, page, **kwargs)



screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            # The page name, which can be edited by clicking on a button.

            button:
                style "page_label"

                #key_events True
                xalign 0.5
                #action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                #textbutton _("{#auto_page}A") action FilePage("auto")

                #textbutton _("{#quick_page}Q") action FilePage("quick")

                # range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")
    outlines []

style slot_button:
    properties gui.button_properties("slot_button")
    idle_background Frame("gui/button/slot_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/slot_hover_background.png", gui.choice_button_borders)

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    color "#666"
    outlines []


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences
default save_manager_msg = ""

screen preferences():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("设置"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("显示")
                        textbutton _("窗口") action Preference("display", "window")
                        textbutton _("全屏") action Preference("display", "fullscreen")

            ## Additional vboxes of type "radio_pref" or "check_pref" can be
            ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("文字速度")

                    #bar value Preference("text speed")
                    bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20)

                    label _("自动前进时间")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("音乐音量")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("音效音量")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("语音音量")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("全部静音"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"
                    
                    # --------- 【新增区域：存档管理】 ---------
                    null height (2 * gui.pref_spacing) 
                    
                    label _("数据迁移") 
                    
                    hbox:
                        spacing 20
                        
                        textbutton _("导出存档(.zip)"):
                            action Function(export_save_to_zip)
                        
                        textbutton _("导入存档(.zip)"):
                            action Function(import_save_from_zip)
                    # ----------------------------------------

    # --------- 【新增区域：结果弹窗】 ---------
    # 这个放在 use game_menu 外面，保证弹窗在最上层，不会被遮挡
    if save_manager_msg:
        frame:
            xalign 0.5 yalign 0.5
            padding (40, 40)
            background "#000000e6" # 深黑色半透明背景
            
            vbox:
                spacing 30
                # 显示具体的成功/失败信息
                text "[save_manager_msg]" color "#ffffff" size 28 xalign 0.5 text_align 0.5
                
                # 关闭按钮
                textbutton _("确定"):
                    action SetScreenVariable("save_manager_msg", "")
                    xalign 0.5
                    text_size 30
                    text_color "#ffcccc" # 稍微带点粉色，符合你的UI风格
    # ----------------------------------------

    text "当前版本:[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"
style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    font "gui/font/zcoolkuaile.ttf"
    size 24
    color "#fff"
    outlines [(3, "#779977", 0, 0), (1, "#779977", 1, 1)]
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")
    font "gui/font/zhushi.ttf"
    outlines []

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")
    font "gui/font/zhushi.ttf"
    outlines []

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


## 历史屏幕 ########################################################################
##
## 这是一个向用户显示对话历史的屏幕。虽然此屏幕没有什么特别之处，但它必须访问储
## 存在 _history_list 中的对话历史记录。
##
## https://www.renpy.cn/doc/history.html

screen history():
    tag menu
    predict False

    use game_menu(_("历史"), scroll=("vpgrid" if gui.history_height else "viewport")):
        style_prefix "history"
        for h in _history_list:
            window:
                has fixed:
                    yfit True
                if h.who:
                    label h.who:
                        style "history_name"
                        if "color" in h.who_args:
                            text_color h.who_args["color"]
                $ what = filter_text_tags(h.what, allow=set([]))
                text what:
                    substitute False
        if not _history_list:
            label _("这里没有对话历史记录。")
            
python early:
    import renpy.text.textsupport as textsupport
    from renpy.text.textsupport import TAG, PARAGRAPH
    def filter_text_tags(s, allow=None, deny=None):
        if (allow is None) and (deny is None):
            raise Exception("Only one of the allow and deny keyword arguments should be given to filter_text_tags.")
        if (allow is not None) and (deny is not None):
            raise Exception("Only one of the allow and deny keyword arguments should be given to filter_text_tags.")
        tokens = textsupport.tokenize(unicode(s))
        rv = [ ]
        for tokentype, text in tokens:
            if tokentype == PARAGRAPH:
                rv.append("\n")
            elif tokentype == TAG:
                kind = text.partition("=")[0]
                if kind and (kind[0] == "/"):
                    kind = kind[1:]
                if allow is not None:
                    if kind in allow:
                        rv.append("{" + text + "}")
                else:
                    if kind not in deny:
                        rv.append("{" + text + "}")
            else:
                rv.append(text)
        return "".join(rv)
 
style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5




screen name_input(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("player") length 12

            #hbox:
            #    xalign 0.5
            #    style_prefix "radio_pref"
            #    textbutton "Male" action NullAction()
            #    textbutton "Female" action NullAction()
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("确认") action ok_action

screen dialog(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("好的") action ok_action

image confirm_glitch:
    "gui/overlay/confirm_glitch.png"
    pause 0.02
    "gui/overlay/confirm_glitch2.png"
    pause 0.02
    repeat

screen confirm(message, yes_action, no_action):

    ## 确保模态
    modal True
    zorder 200
    style_prefix "confirm"

    # =========================================================
    # 💀 Mortis 模式：二阶段 Meta 欺诈弹窗
    # =========================================================
    if persistent.in_mortis_mode:
        
        # --- 变量定义 ---
        default confirm_phase = 1          # 1=欺骗阶段, 2=追逐阶段
        
        # 阶段1变量：控制文字变化
        default left_hover = False         # 左按钮悬停状态
        default right_hover = False        # 右按钮悬停状态
        
        # 阶段2变量：控制逃跑
        default runner_count = 0
        default runner_x = 0.5
        default runner_y = 0.55
        
        # 全屏遮罩
        add Solid("#000000E6")

        # --- 黑色小方框 ---
        frame:
            background Solid("#1a0505")
            align (0.5, 0.5)
            xsize 500 
            ysize 300 
            
            # 红线装饰
            add Solid("#FF0000") xsize 1.0 ysize 2 align (0.5, 0.0)
            add Solid("#FF0000") xsize 1.0 ysize 2 align (0.5, 1.0)

            # -------------------------------------------------
            # [阶段 1] 真的要离开我吗？
            # 左边：是 -> 否 (点击无效)
            # 右边：否 -> 是 (点击进下一关)
            # -------------------------------------------------
            if confirm_phase == 1:
                
                text "真的要离开我吗？":
                    font "fonts/mortis_font.otf"
                    size 45
                    color "#FF0000"
                    align (0.5, 0.3)
                    outlines [(2, "#000000", 0, 0)]

                # === 左边按钮 (陷阱) ===
                button:
                    # 【关键】强制透明背景，去掉默认绿框
                    background None 
                    padding (0, 0)
                    align (0.3, 0.7)
                    xysize (100, 60)
                    
                    # 悬停逻辑
                    hovered SetScreenVariable("left_hover", True)
                    unhovered SetScreenVariable("left_hover", False)
                    
                    # 点击效果：留在原地 (no_action)
                    action no_action 
                    
                    text ("否" if left_hover else "是"):
                        font "fonts/mortis_font.otf"
                        size 35
                        # 没悬停时是暗淡的，悬停变红
                        color ("#FF0000" if left_hover else "#666666")
                        align (0.5, 0.5)

                # === 右边按钮 (入口) ===
                button:
                    background None 
                    padding (0, 0)
                    align (0.7, 0.7)
                    xysize (100, 60)
                    
                    # 悬停逻辑
                    hovered SetScreenVariable("right_hover", True)
                    unhovered SetScreenVariable("right_hover", False)
                    
                    # 点击效果：进入第二阶段
                    action SetScreenVariable("confirm_phase", 2)
                    
                    text ("是" if right_hover else "否"):
                        font "fonts/mortis_font.otf"
                        size 35
                        # 没悬停时是亮的，悬停变红
                        color ("#FF0000" if right_hover else "#FFFFFF")
                        align (0.5, 0.5)
                        bold True

            # -------------------------------------------------
            # [阶段 2] 你确定吗？ (是按钮会逃跑)
            # -------------------------------------------------
            elif confirm_phase == 2:
                
                text "你确定吗？":
                    font "fonts/mortis_font.otf"
                    size 50
                    color "#FF0000"
                    bold True
                    align (0.5, 0.3)
                    outlines [(2, "#000000", 0, 0)]

                # === 会逃跑的"是"按钮 ===
                button:
                    background None
                    padding (0, 0)
                    
                    # 动态位置
                    align (runner_x, runner_y)
                    xysize (100, 50)
                    
                    if runner_count < 6:
                        hovered [
                            # 随机瞬移 (范围限制在框内 0.1~0.9)
                            SetScreenVariable("runner_x", renpy.random.uniform(0.1, 0.9)),
                            SetScreenVariable("runner_y", renpy.random.uniform(0.4, 0.9)),
                            SetScreenVariable("runner_count", runner_count + 1)
                        ]
                        action NullAction()
                    else:
                        # 跑够了，可以点击退出
                        action yes_action 
                    
                    text "是":
                        font "fonts/mortis_font.otf"
                        size 35
                        color "#FF0000"
                        align (0.5, 0.5)
                        bold True

                # === 放弃按钮 (返回) ===
                button:
                    background None
                    padding (0, 0)
                    align (0.9, 0.9)
                    action no_action
                    
                    text "否":
                        font "fonts/mortis_font.otf"
                        size 25
                        color "#888888"
                        align (0.5, 0.5)
                        hover_color "#FFFFFF"

    # =========================================================
    # 🌸 普通模式 (保持原样)
    # =========================================================
    else:
        add "gui/overlay/confirm.png"

        frame:
            vbox:
                xalign .5
                yalign .5
                spacing 30

                label _(message):
                    style "confirm_prompt"
                    xalign 0.5

                hbox:
                    xalign 0.5
                    spacing 100

                    textbutton _("是") action yes_action
                    textbutton _("否") action no_action

    key "game_menu" action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style confirm_button_text is navigation_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator
screen fake_skip_indicator():
    use skip_indicator
screen skip_indicator():

    zorder 100
    style_prefix "skip"

    if config.skipping:

        if persistent.in_mortis_mode:
            
            # 1. 定义怨言池 (变量只在这个 screen 内部有效)
            default complaint_pool = [
                "你是觉得我很烦吗？",
                "不想听我说话吗？",
                "你要去哪里？",
                "别逃。",
                "看着我。",
                "我还没说完。",
                "没用的。",
                "你无法逃离这里。",
                "慢一点……",
                "为什么？为什么？"
            ]
            default current_complaint = renpy.random.choice(complaint_pool)
            timer 0.2 repeat True action SetScreenVariable("current_complaint", renpy.random.choice(complaint_pool))

            # 4. 显示框
            frame:
                background Frame(Solid("#000000E6"), 0, 0)
                align (0.05, 0.05) 
                padding (30, 15)
                
                hbox:
                    spacing 10
                    text "[current_complaint]":
                        font "fonts/mortis_font.otf" 
                        color "#FF0000"              
                        size 35
                        bold True
                        outlines [(2, "#000", 0, 0)] 
                        at transform:
                            zoom 1.0
                            linear 0.2 zoom 1.05
                            linear 0.2 zoom 0.95
                            repeat
        else:
            frame:

                hbox:
                    spacing 9

                    text _("正在快进")
                    text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
                    text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
                    text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

    
init python:
    # 校验输入的函数
    def check_love_input_func():
        # 获取当前输入框的内容
        input_val = store.love_input_value.strip()
        
        # 目标字符串
        target = "永远爱你"
        
        if input_val == target:
            # 输入正确：次数+1，清空输入框
            store.love_counter += 1
            store.love_input_value = ""
            
            # 播放一个开心的音效 (可选)
            # renpy.play("audio/sfx_correct.ogg") 
            
            # 检查是否触发作者注 (30次)
            if store.love_counter >= 30 and not renpy.get_screen("mortis_author_note"):
                renpy.show_screen("mortis_author_note")
                
        else:
            # 输入错误：给出提示
            renpy.notify("只能输入“永远爱你”哦……别想敷衍我。")

# 初始化变量
default love_counter = 0
default love_input_value = ""

# =========================================================
# 📝 10000遍爱你的专用输入屏幕
screen mortis_love_input_screen():
    modal True 
    zorder 200
    add Solid("#000000E6")
    
    vbox:
        align (0.5, 0.4)
        spacing 30
        
        # 墨缇斯的提示
        text "请输入“永远爱你” (还剩 [10000 - love_counter] 遍)":
            size 30
            color "#FF0000"
            outlines [(2, "#000", 0, 0)]
            xalign 0.5
            
        # 输入框
        frame:
            xalign 0.5
            padding (20, 20)
            background Solid("#333")
            
            input:
                value VariableInputValue("love_input_value")
                length 20 # 限制长度
                allow "永远爱你abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890" # 允许输入的字符
                color "#fff"
                size 40
        
        # 确认按钮
        textbutton ("确认" if love_counter == 0 else "我好开心啊，再说 {} 遍".format(10000 - love_counter)):
            xalign 0.5
            style "button"
            text_size 35
            text_color "#FF0000"
            text_bold True
            action Function(check_love_input_func)
            text_hover_color "#FFFFFF"

screen mortis_author_note():
    zorder 300
    frame:
        align (1.0, 0.0) # 右上角
        offset (-20, 20)
        padding (20, 10)
        background Solid("#000000CC")
        
        text "{color=#ffff00}【作者注】{/color}\n善良的作者的提醒\n其实你真的打完一万遍也没有额外内容\n这时候的正确做法应该是：\n{b}直接退出游戏然后重进，\n更改选项。{/b}":
            size 22
            color "#fff"
            line_spacing 4

## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font "DejaVuSans.ttf"


## 通知屏幕 ########################################################################
##
## 通知屏幕用于向用户显示消息。（例如，当游戏快速保存或进行截屏时。）
##
## https://www.renpy.cn/doc/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    size gui.notify_text_size

## NVL 模式屏幕 ####################################################################
##
## 此屏幕用于 NVL 模式的对话和菜单。
##
## https://www.renpy.cn/doc/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## 显示菜单，如果给定的话。如果 config.narrator_menu 设置为 True，则菜单
        ## 可能显示不正确。
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## 此语句控制一次可以显示的 NVL 模式条目的最大数量。
## once.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")


################################################################################
## 移动设备界面
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## 由于可能没有鼠标，我们将快捷菜单替换为一个使用更少、更大按钮的版本，这样更容
## 易触摸。
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("回退") action Rollback()
            textbutton _("快进") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("自动") action Preference("auto-forward", "toggle")
            textbutton _("菜单") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

init python:
    # 右键 = 游戏菜单
    config.keymap['game_menu'].append('mouseup_3')

screen main_interaction_ui():
    zorder 60
    # modal True # 如果你希望这个 UI 打开时完全拦截背景点击，可以取消这一行的注释

    # 1. 核心修复：更新逻辑状态，增加对 menu 选项 (choice) 的检测
    # 只要在说话 (say)、弹出选项 (choice)、主动对话中、手机打开，全部禁用按钮
    $ is_locked = (
        renpy.get_screen("say") or 
        renpy.get_screen("choice") or 
        talking_to_mutsumi or 
        phone_open
    )

    # 2. 睦的吉他按钮
    # 1. 先获取当前的布局数据 (x, y, zoom, rotate)
    $ g_x, g_y, g_zoom, g_angle = get_guitar_layout()

    imagebutton:
        idle "images/mutsumi_guitar.png"
        hover "images/mutsumi_guitar_hover.png"

        # 【核心修改】这里使用变量，而不是死数字
        xpos g_x 
        ypos g_y
        
        xanchor 0.5 yanchor 0.5
        
        at transform:
            # 【核心修改】缩放和旋转也跟着变
            zoom g_zoom  
            rotate g_angle
            
            # 锁定状态下半透明显示
            alpha (0.4 if is_locked else 1.0)

        # 锁定逻辑 (保持不变)
        if not is_locked:
            action Jump("guitar_entry_logic")
        else:
            action None

        sensitive not is_locked

    # 3. 左侧菜单按钮
    vbox:
        align (0.02, 0.95)
        spacing 10
        style_prefix "mutsumi_menu"

        # 聊天按钮：增加状态锁定判定
        textbutton "聊天":
            action [SetVariable("talking_to_mutsumi", True), Show("talk_category_screen")] 
            sensitive not is_locked

        # 故事按钮：进入书架/日记界面
        textbutton "故事":
            action Jump("open_mutsumi_diary")
            sensitive not is_locked

        # 额外功能按钮
        textbutton "额外功能":
            action Function(check_extra_features_logic) 
            sensitive not is_locked
init python:
    def set_guitar_interaction_active(state):
        store.talking_to_mutsumi = state # 我们之前用这个变量来暂停主循环计时
screen talk_category_screen():
    modal True
    zorder 70
    
    # --- 快捷键支持 ---
    # 点击右键 (mouseup_3) 或 按下键盘 ESC，关闭界面并恢复循环
    key "mouseup_3" action [Hide("talk_category_screen"), SetVariable("talking_to_mutsumi", False)]
    key "K_ESCAPE" action [Hide("talk_category_screen"), SetVariable("talking_to_mutsumi", False)]

    # 背景遮罩（点击空白处也可以退出）
    button:
        action [Hide("talk_category_screen"), SetVariable("talking_to_mutsumi", False)]
        background Solid("#00000077")
        xfill True yfill True

    # 主面板
    frame:
        background Frame(Solid("#779977dd"), 4, 4) 
        align (0.5, 0.4) 
        xsize 900 ysize 650
        padding (30, 30)

        hbox:
            spacing 40
            
            # --- 左侧：分类列 ---
            vbox:
                xsize 200
                spacing 10
                label "话题分类" xalign 0.5:
                    text_size 24 
                    text_color "#fff"
                null height 10
                
                # 分类列表
                vbox:
                    spacing 5
                    for cat in categories:
                        textbutton cat:
                            style "mutsumi_cat_button"
                            action SetVariable("current_category", cat)
                            selected (current_category == cat)

                # --- 新增：返回按钮 ---
                null height 20 # 留一点空隙
                textbutton "返回":
                    style "mutsumi_back_button"
                    # 点击效果同关闭菜单
                    action [Hide("talk_category_screen"), SetVariable("talking_to_mutsumi", False)]
                    xalign 0.5

            # --- 分割线 ---
            add Solid("#ffffff33") xsize 2 ysize 550 yalign 0.5

            # --- 右侧：话题列表 ---
            vbox:
                xsize 580
                spacing 10
                label "[current_category]" xalign 0.1 text_size 24 text_color "#fff"
                
                viewport id "topic_vp":
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    
                    vbox:
                        spacing 8
                        xfill True
                        for t in all_topics:
                            if t.category == current_category:
                                textbutton t.title:
                                    style "mutsumi_topic_item"
                                    action [
                                        Hide("talk_category_screen"), 
                                        SetVariable("talking_to_mutsumi", False), 
                                        Jump(t.label)
                                    ]

# --- 新增：返回按钮的样式 ---
style mutsumi_back_button:
    background Solid("#a94442") # 使用暗红色表示返回/关闭
    hover_background "#d9534f"
    padding (10, 20)
    xsize 180

style mutsumi_back_button_text:
    color "#fff"
    size 20
    xalign 0.5
    bold True

# --- 话题按钮样式 ---
style mutsumi_topic_item:
    background Solid("#ffffff11")      # 默认半透明白
    hover_background "#ffffff33"       # 悬停时变亮
    padding (12, 12)
    xfill True                         # 横向撑满

style mutsumi_topic_item_text:
    color "#fff"                       # 文字白色
    hover_color "#2c3e50"              # 悬停时文字变深色
    size 18
    xalign 0.0                         # 文字左对齐

# --- 分类按钮样式 ---
style mutsumi_cat_button:
    background Solid("#4a664a")        # 睦绿色
    hover_background "#a0c0a0"         # 悬停浅绿色
    selected_background "#ffffff"      # 选中时变白色
    padding (10, 15)
    xfill True

style mutsumi_cat_button_text:
    color "#ccc"                       # 默认灰色
    hover_color "#000"                 # 悬停黑色
    selected_color "#4a664a"           # 选中时变成睦绿色
    size 20
    xalign 0.5                         # 文字居中

# --- 返回按钮样式 ---
style mutsumi_back_button:
    background Solid("#a94442")        # 暗红色
    hover_background "#d9534f"         # 亮红色
    padding (10, 20)
    xsize 180

style mutsumi_back_button_text:
    color "#fff"
    size 20
    xalign 0.5
    bold True

style mutsumi_menu_button:
    background Solid("#4a664aa1")
    hover_background "#779977"
    # 当按钮被锁定（insensitive）时的颜色
    insensitive_background Solid("#222222aa") 
    xsize 150
    padding (10, 5)

style mutsumi_menu_button_text:
    color "#fff"
    hover_color "#000"
    # 当按钮被锁定（insensitive）时的文字颜色
    insensitive_color "#666666" 
    size 22


# ---------------- 额外功能弹窗 ----------------
screen extra_features():
    modal True
    zorder 200
    
    # 增加半透明背景蒙层
    add Solid("#000000aa")
    
    frame:
        # 稍微调高一点高度（原本300 -> 380），给测试按钮留位置
        xsize 450 ysize 380 
        align (0.5, 0.5)
        background Solid("#1a1a1ae5") # 深色背景
        padding (20, 20)
        
        vbox:
            align (0.5, 0.5)
            spacing 30 # 稍微缩小间距
            
            # 台词部分
            text "若叶睦：\n“……要和我一起，学习高数吗？”":
                size 24
                color "#ffffff"
                text_align 0.5
                xalign 0.5
            
            # 按钮排列
            hbox:
                xalign 0.5
                spacing 80 # 两个按钮之间的间距
                
                # “是”按钮
                button:
                    action [OpenURL("https://space.bilibili.com/391616943/lists/6622123?type=season"), Hide("extra_features")]
                    xsize 120 ysize 50
                    background Solid("#2c3e50") 
                    hover_background Solid("#95e1d3") 
                    
                    text "是":
                        align (0.5, 0.5)
                        size 20
                        idle_color "#fff"
                        hover_color "#000"

                # “否”按钮
                button:
                    action Hide("extra_features")
                    xsize 120 ysize 50
                    background Solid("#2c3e50")
                    hover_background Solid("#ff6b6b")
                    
                    text "再想想":
                        align (0.5, 0.5)
                        size 20
                        idle_color "#fff"
                        hover_color "#000"



# -----------------------------------------------------------
# 📱 手机端对话框强制修正补丁 (修复版)
# -----------------------------------------------------------
# 注意：variant "small" 必须直接写在 style 声明的同一行
style window variant "small":
    
    # 1. 【关键】强制容器宽度等于你的图片宽度
    xsize 816  
    
    # 2. 【关键】禁止自动填满屏幕
    xfill False 
    
    # 3. 高度设置 (对应你的图片高度)
    ysize 146
    
    # 4. 背景图设置 (确保路径对，如果没有 gui/phone 文件夹，就改回 gui/textbox.png)
    background Frame("gui/phone/textbox.png", 0, 0)

    # -------------------------------------------------------
    # 🎮 位置控制
    # -------------------------------------------------------
    
    # 方案：完全靠右，贴底
    xalign 0.5
    yalign 1.0
    
    # 如果觉得贴得太死，可以用 padding 或 offset 微调
    # xoffset -20  # 向左微调 20 像素
    # yoffset -20  # 向上微调 20 像素