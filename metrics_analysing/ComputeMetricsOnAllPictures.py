from metrics.Metrics import Metrics
from utils.Timing import timing

__author__ = 'ava-katushka'
import os
import numpy as np
import threading


class MetricsCounter:
    def __init__(self):
        self._SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.database_file = os.path.join(self._SCRIPT_ROOT, "picture_database.txt")
        # database file heading: "Id,SignOrd,Font,HorizontalDescription,VerticalDescription\n"
        self.reminder_num = 1000
        self.metrics_file = os.path.join(self._SCRIPT_ROOT, "metrics_database1.txt")
        self.metrics = Metrics.dameray_levenstein_distance_hist
        self._THREAD_NUMBER = 10
        self._PIC_NUM = 5000

    # returns set of pictures in format:
    # sign, (h_hist, v_hist)
    # takes 8 seconds on 70000 pictures
    @timing
    def upload_picture_database(self):
        result = []
        with open(self.database_file, "r") as file:
            # read heading
            line = file.readline()
            for line in file:
                description = line.split(",")
                id = description[0]
                h_hist = self.hist_to_array(description[3])
                v_hist = self.hist_to_array(description[4])
                result.append((id, (h_hist, v_hist)))
        return result

    def hist_to_array(self, hist):
        result = hist.replace(";", ",")
        return eval(result)

    def make_heading(self, file, n):
        file.write("Id,")
        for i in range(n - 1):
            file.write("Id" + str(i) + ",")
        file.write("Id" + str(n - 1) + "\n")

    def write_line(self, file, str1, str2):
        n = len(str1)
        for i in range(n - 1):
            file.write("(" + str(str1[i]) + ";" + str(str2[i]) + "),")
        file.write("(" + str(str1[n - 1]) + ";" + str(str2[n - 1]) + ")\n")

    def write_metrics_to_file(self, n, h_dist, v_dist):
        with open(self.metrics_file, "w+") as file:
            self.make_heading(file, n)
            for i in range(n):
                file.write(str(i) + ",")
                self.write_line(file, h_dist[i], v_dist[i])

    # 100 pictures takes 34 seconds
    # takes 44,5 minutes on 1000 pictures (2671 seconds)
    @timing
    def compute_metrics_database(self):
        pictures = self.upload_picture_database()
        pictures = pictures[:self._PIC_NUM]
        n = len(pictures)
        h_dist = np.zeros((n, n))
        v_dist = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                pic1 = pictures[i][1]
                pic2 = pictures[j][1]
                h_dist[i][j], v_dist[i][j] = self.metrics(pic1, pic2)
                # print i, ")", j, ")", h_dist[i][j], v_dist[i][j]
                h_dist[j][i], v_dist[j][i] = h_dist[i][j], v_dist[i][j]
            if i % 10 == 0:
                print "Writing string", i, "of", n
        self.write_metrics_to_file(n, h_dist, v_dist)



if __name__ == '__main__':
    metrics_counter = MetricsCounter()
    metrics_counter.compute_metrics_database()
