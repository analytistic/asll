import numpy as np
import pandas as pd

def date_dict(group, date_name, test):
    '''
    日期字典
    :param group:
    :return: 每位患者对应一个提交日期和记录的字典
    '''

    return group.groupby(date_name)[test].apply(list).to_dict()


def df_merge_dict(df, date_name, test):
    '''
    合并原表和提交记录字典
    :param df: 原始 DataFrame
    :param date_name: 日期列名
    :param test: 测试列名
    :return: 合并后的 DataFrame
    '''

    date_dicts = df.groupby('患者编号').apply(date_dict, date_name=date_name, test=test).reset_index(name=test+'提交记录')
    df_merged = df.merge(date_dicts, on='患者编号')
    return df_merged


if __name__=="__main__":
    pass









