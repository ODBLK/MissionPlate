import pandas as pd
import os
import json

from utils import dir_prefix, value_file, project_file

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


# 读写ProjectData, ValueData, flag传入'project'或'value'
def save_data_to_csv(data, flag):
    file_dict = {'project': project_file, 'value': value_file}
    col_dict = {'project': ['项目', '对接人', '设计师', '开始日期', '结束日期', '耗时/天', '业务类型', '价值', '备注'], 
                'value': ['业务', '价值', '占比']}
    # 文件保存路径
    file_path = os.path.join(dir_prefix, file_dict[flag])
    # 尝试读取现有的数据，如果文件不存在，创建一个空的DataFrame
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
    else:
        # 若data文件夹不存在
        if not os.path.exists(dir_prefix):
            os.mkdir(dir_prefix)
        df_existing = pd.DataFrame()
        # 创建header
        df_existing = df_existing.reindex(columns=col_dict[flag])

    # 创建新数据的DataFrame
    df_existing.loc[df_existing.shape[0]] = data.values()

    # 保存到文件
    df_existing.to_csv(file_path, index=False, encoding='utf-8-sig')

def vp_to_json(vp, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(vp, f, ensure_ascii=False)

def json_to_vp(json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        vp = json.load(f)
    return vp




