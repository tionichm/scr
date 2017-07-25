import matplotlib.pyplot as plt
import numpy as np
import csv
from scr import *

f = "/home/tionichm/src/python/fridge/CO2_blank.txt"
p1 = []
p2 = []
temp = []

with open(f, 'r') as file:
    reader = csv.reader(file, skipinitialspace=True, delimiter=' ')
    next(reader, None)
    for row in reader:
        p1.append(row[1])
        p2.append(row[2])
        temp.append(row[3])
    file.close()

searcher = Snake_Searcher(p1, p2, length=10, verbose=False)
ss_results = searcher.SS_output()
print(ss_results)

chomper = Data_Chomper(ss_results)
print('\n')
fig = plt.figure()
ax = fig.add_subplot(111)
for key in chomper.output.keys():
    y = []
    x = []
    c = 1
    for val in chomper.output[key]:
        y.append(val[0])
        x.append(c)
        c += 1
    ax.plot(x, y)
plt.show()
# dc_results = chomper.DC_output()
