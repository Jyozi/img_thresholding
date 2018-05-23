#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
 
#グレイスケール関数
def make_gray(img):
     r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
     return 0.2989 * r + 0.5870 * g + 0.1140 * b
 
#データ格納変数
data = {}
 
#画像読み取り
img = cv2.imread(sys.argv[1])
 
#グレイスケール化
img = make_gray(img)
cv2.imwrite("gray_" + sys.argv[1], img)
 
#初期化
for i in range(0, 241, 2):
    data[i] = 0
 
#dataに格納
for i, line in enumerate(img):
    for k, p in enumerate(line):
        if p > 241:
            data[240] += 1
        elif p < 0:
            data[0] += 1
        elif int(p) % 2 == 0:
            data[int(p)] += 1
        else:
            data[int(p) - 1] += 1
 
#閾値算出
b = 0
st = 0
for t in range(0, 241, 2):
    n1 = 0
    u1 = 0
    u2 = 0
    n2 = 0
    for t1 in range(0, t+1, 2):
        n1 += data[t1]
        u1 += t1 * data[t1]
    if n1 == 0 or u1 == 0:
        continue
    else:
        u1 = u1 / n1
 
    for t2 in range(t+2, 241, 2):
        n2 += data[t2]
        u2 += t2 * data[t2]
    if n2 == 0 or u2 == 0:
        continue
    else:
        u2 = u2 / n2
 
    tmp = n1 * n2 * pow(u1-u2,2)
    if b < tmp:
        b = tmp
        st = t
print("閾値:%d" % st)
 
#グラフ表示
plt.bar(list(data.keys()),list(data.values()))
plt.plot([st, st],[0, max(data.values())], "red", alpha=0.8, linestyle=":")
plt.show()
 
#二値化
for i, line in enumerate(img):
    for k, p in enumerate(line):
        if p < st:
            img[i][k] = 0
        else:
            img[i][k] = 255
 
#書き出し
cv2.imwrite("threshold_" + sys.argv[1], img)

