import pandas as pd
import os
import json

from utils import csv_dir, csv_path

# 读取Json的配置文件
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found.")
        return None
    except json.JSONDecodeError:
        print("Error: config.json has invalid format.")
        return None

config = load_config()
if config:
    businessOptions = config.get("businessOptions", [])
    valueRanges = config.get("valueRanges", [])
else:
    # Provide default values or handle errors as needed
    businessOptions = []
    valueRanges = []


# 读写ProjectDate
def save_project_to_csv(data):
    # 尝试读取现有的数据，如果文件不存在，创建一个空的DataFrame
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
    else:
        # 若data文件夹不存在
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        df_existing = pd.DataFrame()
        # 创建header
        df_existing = df_existing.reindex(columns=['项目', '对接人', '设计师', '开始日期', '结束日期', '耗时/天', '业务类型', '价值', '备注'])

    # 创建新数据的DataFrame
    df_existing.loc[df_existing.shape[0]] = data.values()

    # 保存到文件
    df_existing.to_csv(csv_path, index=False, encoding='utf-8-sig')

#业务价值数据
def save_value_to_csv(value_percentages):
    # 尝试读取现有的数据，如果文件不存在，创建一个空的DataFrame
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
    else:
        # 若data文件夹不存在
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        df_existing = pd.DataFrame()
        # 创建header
        df_existing = df_existing.reindex(columns=['业务', '价值', '占比'])

    # 创建新数据的DataFrame
    df_existing.loc[df_existing.shape[0]] = value_percentages.values()

    # 保存到文件
    df_existing.to_csv(csv_path, index=False, encoding='utf-8-sig')
    