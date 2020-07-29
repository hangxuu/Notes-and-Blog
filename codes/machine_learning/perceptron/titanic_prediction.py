"""
author: hangxuu@qq.com

"""


import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from perceptron import preceptron
from sklearn.linear_model import Perceptron


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attr_names):
        self.attr_names = attr_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attr_names]


class MostFrequentImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.most_frequent_ = pd.Series([X[c].value_counts().index[0] for c in X],
                                        index=X.columns)
        return self

    def transform(self, X):
        return X.fillna(self.most_frequent_)


def load_data(file_name='titanic/train.csv'):
    train_data = pd.read_csv(file_name)
    return train_data


def preprocessing_data(data):
    num_pipeline = Pipeline([
        ("numetic", DataFrameSelector(["Age", "SibSp", 'Parch', "Fare"])),
        ("imputer", SimpleImputer(strategy='median')),
        # ("std_scaler", StandardScaler()),
    ])
    # num_pipeline.fit_transform(data)
    cat_pipeline = Pipeline([
        ("select_cat", DataFrameSelector(["Sex", "Pclass", "Embarked"])),
        ("imputer", MostFrequentImputer()),
        ("cat_encoder", OneHotEncoder(sparse=False))
    ])
    # cat_pipeline.fit_transform(data)
    preprocess_pipeline = FeatureUnion(transformer_list=[
        ("num_pipeline", num_pipeline),
        ("cat_pipeline", cat_pipeline),
    ])
    x_data = preprocess_pipeline.fit_transform(data)

    return x_data


def train(x_data, y_label, iter_times=5000, accuracy=0.97):
    w, b = preceptron(x_data, y_label, iter_times, accuracy)
    return w, b


def predict(x_test, w, b):
    rst = x_test @ w + b
    rst[rst > 0] = 1
    rst[rst < 0] = 0
    rst = rst.astype(np.int64)
    return rst


def main():
    train_data = load_data(file_name='titanic/train.csv')
    test_data = load_data(file_name='titanic/test.csv')
    train_y_label = train_data['Survived']
    train_y_label.loc[train_y_label == 0] = -1
    train_y_label = train_y_label.values
    train_data_preprocess = preprocessing_data(train_data)
    test_data_preprocess = preprocessing_data(test_data)
    w, b = preceptron(train_data_preprocess, train_y_label, iter_times=1000, accuracy=0.75)
    ans = predict(test_data_preprocess, w, b)
    result = pd.DataFrame({"PassengerId": test_data['PassengerId'], "Survived": ans})
    print(result)
    result.to_csv('my_submission.csv', index=False)
    # 最终得分0.73684
    # 精确度最后也就到0.73左右，说明该数据集并非线性可分，用感知机模型会出现欠拟合。

    # sklearn Perceptron，得分0.62左右。
    clf = Perceptron()
    clf.fit(train_data_preprocess, train_y_label)
    ans = clf.predict(test_data_preprocess)
    ans[ans > 0] = 1
    ans[ans < 0] = 0
    ans = ans.astype(np.int64)
    result = pd.DataFrame({"PassengerId": test_data['PassengerId'], "Survived": ans})
    print(result)
    result.to_csv('my_submission.csv', index=False)

    # 这么看来自己实现的模型比sklearn实现的效果好？哈哈，当然不敢这么说。这个数据集数据还是太少！


if __name__ == "__main__":
    main()
