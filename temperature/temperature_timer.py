import time
import sched
from datetime import datetime


def record_temperature_task(schedule: sched.scheduler, duration):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('start record')
    schedule.enter(duration, 0, record_temperature_task)


def main():
    duration = 60
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(0, 0, record_temperature_task, (schedule, duration))
    schedule.run()


if __name__ == "__main__":
    main()
