#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author:Zhang Shiwei
# @Date  :2020/5/20

import numpy as np
import tensorflow as tf
import pandas as pd

# 读取csv文件
data = pd.read_csv("data/data_6.csv", header=None, dtype=np.float32)
num = data.shape[0]  # 样本数量
features = data.iloc[:, :-1]
labels = data.iloc[:, [-1]]

# 手动去除噪声
d = dict()  # 以特征为key，存储所有对应的label
for i in range(num):
    feature = tuple(features.iloc[i])
    label = labels.iloc[i, 0]
    if feature in d:
        d[feature].append(label)
    else:
        d[feature] = []
        d[feature].append(label)
# 取众数作为正确的label
for key in d.keys():
    d[key] = max(d[key], key=d[key].count)
# 修改原来的label
for i in range(num):
    labels.iloc[i, 0] = d[tuple(features.iloc[i])]

# 创建训练集、验证集、测试集
features = np.array(features)
labels = np.array(labels)
train_x, train_y = features[:16000], labels[:16000, 0]
val_x, val_y = features[16000:18000], labels[16000:18000, 0]
test_x, test_y = features[18000:], labels[18000:, 0]

# 创建模型
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='tanh'))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['MAE'])
model.fit(train_x, train_y, epochs=200, shuffle=True, validation_data=(val_x, val_y))
