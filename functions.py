import pandas as pd
import os
import json

from utils import csv_dir, csv_path

# 读写csv
def save_data_to_csv(data):
    # 尝试读取现有的数据，如果文件不存在，创建一个空的DataFrame
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
    else:
        # 若data文件夹不存在
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        df_existing = pd.DataFrame()
        # 创建header
        df_existing = df_existing.reindex(columns=['项目', '设计师', '对接人', '开始日期', '结束日期', '耗时/天', '业务类型', '价值', '备注'])

    # 创建新数据的DataFrame
    df_existing.loc[df_existing.shape[0]] = data.values()

    # 保存到文件
    df_existing.to_csv(csv_path, index=False, encoding='utf-8-sig')

def vp_to_json(vp, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(vp, f, ensure_ascii=False)

def json_to_vp(json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        vp = json.load(f)
    return vp




