__author__ = 'ava-katushka'
import pandas as pd
import numpy as np


def get_feature(row, i):
    if i < 30:
        return row[' h' + str(i)]
    else:
        return row[' v' + str(i - 30)]


def write_array_to_row(file, array):
    for x in array[:-1]:
        file.write(str(x) + ", ")
    file.write(str(array[-1]) + "\n")


Location = 'line_detection_statistics.csv'
df = pd.read_csv(Location)
picture_points = np.array([0.] * 60)
sum_noisy_points = np.array([0.] * 60)
variance_sum = np.array([0.] * 60)
picture_num = 0
noisy_images = 9
for index, row in df.iterrows():
    if row[' Noise'] == 'no':
        picture_num += 1
        variance_sum += (picture_points - (sum_noisy_points / noisy_images)) ** 2
        sum_noisy_points = np.zeros(sum_noisy_points.shape)
        for i in xrange(60):
            picture_points[i] = get_feature(row, i)
    else:
        for i in xrange(60):
            sum_noisy_points[i] += get_feature(row, i)
var_in_all = df.var()
print var_in_all
variance_general = np.zeros(60)
for i in xrange(60):
    variance_general[i] = get_feature(var_in_all, i)
    print variance_general[i]

with open('line_detection_variation_results.csv', 'w+') as file:
    file.write("Name, ")
    for i in range(30):
        file.write("h" + str(i) + ", ")
    for j in range(29):
        file.write("v" + str(j) + ", ")
    file.write("v29\n")
    file.write("Average variance in picture, ")
    average_variance_picture = variance_sum / picture_num
    write_array_to_row(file, average_variance_picture)
    file.write("Average variance in set, ")
    write_array_to_row(file, variance_general)
    file.write("Quotient, ")
    write_array_to_row(file, average_variance_picture / variance_general)
