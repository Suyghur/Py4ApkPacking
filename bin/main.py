# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-25.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys
import time
import goto

from goto import with_goto

# 定时间隔
INTERVAL = 10


@with_goto
def start():
    impl = fcore.impl_manager.ImplManager()
    last_task_id = ''
    # 循环标记
    label.begin
    print("---------------> 开始查询任务，上一任务ID=" + last_task_id)
    task = fcore.impl_manager.ImplManager.get_task(last_task_id)
    print("---------------> 结束查询任务")
    if task == None or task.task_info == None or task.task_info.task_id == '':
        print("---------------> 无打包任务，进入定时查询")
        # 定时查询
        start = time.time()
        time.sleep(INTERVAL)
        end = time.time()
        print("执行时间：" + str(end - start))
        goto.begin
    else:
        last_task_id = task.task_info.task_id
        print("---------------> 进入打包任务：" + last_task_id)

        try:
            impl.execute(task)
        except Exception as e:
            msg = "打包异常：" + str(e)
            fcore.impl_manager.ImplManager.api_send_msg_2_wx(msg)
            print(msg)

        goto.begin
    label.end


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    import fcore.impl_manager
    start()
