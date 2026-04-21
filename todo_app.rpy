# --- 动画：滑入与滑出 ---
transform todo_card_appear:
    on show:
        xoffset 100 alpha 0.0
        easein_back 0.4 xoffset 0 alpha 1.0
    on hide:
        easeout_back 0.4 xoffset 100 alpha 0.0

init python:
    if persistent.todo_list is None:
        persistent.todo_list = []

    # 添加任务
    def add_todo_task(task_text):
        task = task_text.strip()
        if task:
            persistent.todo_list.insert(0, {"task": task, "done": False})
            renpy.save_persistent()
            store.new_task_text = ""
        renpy.restart_interaction()

    # 删除特定任务
    def remove_todo_task(item):
        if item in persistent.todo_list:
            persistent.todo_list.remove(item)
            renpy.save_persistent()
        renpy.restart_interaction()


# 辅助动画
transform d_fade:
    alpha 0.0
    linear 0.3 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

# 初始化
default new_task_text = ""