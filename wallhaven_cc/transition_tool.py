
import threading
import time


class Task:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def print(self):
        print('this task is name = {0}'.format(self.name))


class TaskHandleTread (threading.Thread):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task

    def run(self):
        time.sleep(2)
        self.task.print()

    def set_task(self, task: Task):
        self.task = task


class TransitionThreadPool:
    def __init__(self):
        self.handler_count = 10
        self.handler_list = []

    def handle_task(self, task: Task):
        if len(self.handler_list) > self.handler_count:
            return False
        print('start handle task')
        return True


class TransitionManager:
    def __init__(self):
        self.task_list = []

    def add_task(self, task: Task):
        self.task_list.append(task)

    def get_task(self):
        return self.task_list

    def get_task_length(self):
        return len(self.task_list)

