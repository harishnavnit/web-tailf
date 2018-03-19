#! /usr/bin/python

import time
import copy
import threading

from os.path import join, getmtime


class FileMonitor():

    log_data = []

    def __init__(self, log):
        self.running = False
        self.log_file = log
        self.log_data = []
        self.modified_data = []
        self.new_log_data = []

        self.read()

        thread = threading.Thread(target=self.watch, args=())
        thread.daemon = True
        thread.start()


    def read(self, max_lines=10):
        count = 0
        with open(self.log_file, 'r') as f:
            for line in reversed(f.readlines()):
                if count > max_lines: break
                FileMonitor.log_data.append(line.strip())
                count += 1
        f.close()


    def watch(self):
        self.running = True
        curr_time = prev_time = -1
        while True:
            curr_time = getmtime(self.log_file)
            if curr_time == prev_time:
                time.sleep(0.5)
            else:
                prev_time = curr_time
                print("File modified : ", curr_time)
                self.modified()


    def modified(self, max_lines=10):
        line_count = 0

        with open(self.log_file, 'r') as f:
            for line in reversed(f.readlines()):
                if line_count > max_lines: break
                self.new_log_data.append(line.strip())
                line_count += 1
        f.close()
        self.get_modified_data()


    def get_modified_data(self):
        if not self.running:
            self.watch()

        data = []
        print("Default data : ", FileMonitor.log_data)
        print("New data     : ", self.new_log_data)

        try:
            for index in range(len(self.new_log_data)):
                if FileMonitor.log_data[index] != self.new_log_data[index]:
                    data.append(self.new_log_data[index])
        except IndexError as err:
            pass

        self.modified_data = list(reversed(data))
        print("modified data : ", self.modified_data)

        # Clear the new data set
        self.new_log_data = []
        return self.modified_data


if __name__ == "__main__":
    log_file = join("./../data/data.log")
    fm = FileMonitor(log_file)
    fm.watch()
