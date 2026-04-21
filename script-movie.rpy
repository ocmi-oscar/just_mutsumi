label show_video:
    # 隐藏文本窗口
    stop music
    window hide
    $ renpy.movie_cutscene("movie/1.webm")
    # 视频播放结束后返回主菜单
    return
