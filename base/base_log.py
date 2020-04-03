import os

class LogTool():
    def __init__(self, log_file_path, need_print=False):
        self.need_print = need_print
        self.log_file_path = log_file_path
        self.file = open(log_file_path, 'ab+')

    def log(self, text:str):
        if self.need_print:
            print(text)
        self.file.write((text+'\n').encode('utf-8'))

    def close_file(self):
        self.file.close()
