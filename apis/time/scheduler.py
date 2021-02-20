import time
import sched
from datetime import datetime

# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def print_time(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    schedule.enter(inc, 0, print_time, (inc,))


# 默认参数60s
def main(inc=60):
    # enter四个参数分别为：
    # 间隔事件、
    # 优先级（用于同时间到达的两个事件同时执行时定序）、
    # 被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, print_time, (inc,))
    schedule.run()


# 10s 输出一次
main(10)
