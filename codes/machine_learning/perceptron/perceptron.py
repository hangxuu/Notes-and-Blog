"""
author: hangxuu@qq.com

"""

import numpy as np


def preceptron(x_data, y_label, iter_times=1000, accuracy: float = 1):
    """
    感知机是二分类的线性分类模型，属于判别模型。
    f(x) = sign(w•x + b)
    训练感知器模型，输入训练样本以及对应的分类，iter_times控制最大的迭代轮次数，accuracy为期望达到的精度
    x_data: type: m * n 矩阵
    y_label: type: m 维向量
    return: 训练得到的 w，b

    """
    # m为样本个数，n为特征个数
    m, n = x_data.shape
    # 初始化w和b为0值
    w = np.zeros(n)
    b = 0
    # 学习率，控制梯度下降的速率
    alpha = 0.001
    # 最大迭代次数，精确率，当迭代次数到达最大迭代次数或者准确率到达指定精度，训练结束，返回结果
    iter_times = iter_times
    accuracy = accuracy

    for iter_ in range(iter_times):
        count = 0
        for i, x in enumerate(x_data):
            y = y_label[i]
            # x @ w 求x 和 w的内积
            if y * (x @ w + b) <= 0:
                w += alpha * y * x
                b += alpha * y
                count += 1
        acc = (m - count) / m
        print('Round {}'.format(iter_), end=', ')
        print('accuracy =', acc)
        if acc > accuracy:
            break
    return w, b


if __name__ == "__main__":
    x = np.array([[3, 3], [4, 3], [1, 1]])
    y = np.array([1, 1, -1])
    preceptron(x, y, accuracy=0.97)
