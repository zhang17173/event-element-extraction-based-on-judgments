#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Author:Zhang Shiwei
# @Date  :2020/5/19

"""使用pkuseg工具直接对文本进行分词"""

import pkuseg

pkuseg.test("../01数据预处理/txt_files/cases.txt",
            "pku_result.txt", model_name="customized_model", user_dict="dict", nthread=10)

# pkuseg.test(readFile, outputFile, model_name = "default", user_dict = "default", postag = False, nthread = 10)
# 	readFile		输入文件路径。
# 	outputFile		输出文件路径。
# 	model_name		模型路径。同pkuseg.pkuseg
# 	user_dict		设置用户词典。同pkuseg.pkuseg
# 	postag			设置是否开启词性分析功能。同pkuseg.pkuseg
# 	nthread			测试时开的进程数。
