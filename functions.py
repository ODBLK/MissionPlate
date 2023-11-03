import pandas as pd
import os
import json

from utils import dir_prefix, value_file, project_file

# 读取Json的配置文件
def load_config():
    # 获取config.json的绝对路径
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        print("Error: {config_path} not found.")
        return None
    except json.JSONDecodeError:
        print("Error: config.json has invalid format.")
        return None

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

# data:{"业务"：{"价值1":15%, "价值2":20%, ...}, ...}
# def save_value_to_data(data):
#     value_file_path = os.path.join(dir_prefix, value_file)
#     if not os.path.exists(value_file_path):
#         # 初始文件不存在，报错
#         pass
#     value_csv = pd.read_csv(value_file_path)
#     for i in range(value_csv.shape[0]):
#         if value_csv.loc[i]["业务"] == data[0]:
#             pass


#由json生成value_percentages
def generate_value_percentages(config):
    value_percentages = {}
    for business in config.get("businessOptions", []):
        value_percentages[business] = {}
        for value in config.get("valueRanges", []):
            value_percentages[business][value] = 0
    return value_percentages

# def init_value_csv():
#     config_data = load_config()  # 初始加载配置数据
#     value_percentages = generate_value_percentages(config_data)
#     # 初始化df
#     value_csv = pd.DataFrame()
#     value_csv = value_csv.reindex(columns=["业务", "价值", "占比"])
#     for i in value_percentages.keys():
#         for j in value_percentages[i].keys():
#             value_csv.loc[value_csv.shape[0]] = [i, j, 0]
#     # 保存df
#     if not os.path.exists(dir_prefix):
#         os.mkdir(dir_prefix)
#     value_csv.to_csv(os.path.join(dir_prefix, value_file), index=False, encoding='utf-8-sig')

# def save_or_init_value_csv(value_percentages):
#     value_file_path = os.path.join(dir_prefix, value_file)
#     # 检查文件是否存在
#     if not os.path.exists(value_file_path):
#         # 如果不存在，则创建一个新的 DataFrame
#         value_csv = pd.DataFrame(columns=["业务", "价值", "占比"])
#     else:
#         # 如果存在，则读取现有的 CSV 文件
#         value_csv = pd.read_csv(value_file_path)
    
#     # 更新 DataFrame 的数据
#     updated_data = []
#     for business, values in value_percentages.items():
#         for value_range, percentage in values.items():
#             updated_data.append([business, value_range, percentage])
    
#     # 如果有更新的数据，则重置 DataFrame
#     if updated_data:
#         value_csv = pd.DataFrame(updated_data, columns=["业务", "价值", "占比"])
    
#     # 保存 DataFrame 到 CSV 文件
#     value_csv.to_csv(value_file_path, index=False, encoding='utf-8-sig')

def save_or_update_value_csv(value_percentages):
    print("正在尝试保存数据到CSV...")
    value_file_path = os.path.join(dir_prefix, value_file)
    print(f"CSV路径：{value_file_path}")

    # 检查文件是否存在
    if not os.path.exists(value_file_path):
        print("CSV文件不存在，创建新文件。")
        # 如果不存在，则创建一个新的 DataFrame
        value_csv = pd.DataFrame(columns=["业务", "价值", "占比"])
    else:
        print("CSV文件存在，读取现有数据。")
        # 如果存在，则读取现有的 CSV 文件
        value_csv = pd.read_csv(value_file_path)

    print("当前value_percentages内容：", value_percentages)  # 打印当前的value_percentages字典

    # 将新的价值分配数据更新到 DataFrame
    for business, values in value_percentages.items():
        for value_range, percentage in values.items():
            row_index = value_csv[(value_csv['业务'] == business) & (value_csv['价值'] == value_range)].index
            if row_index.empty:
                print(f"添加新行：业务={business}, 价值={value_range}, 占比={percentage}")  # 打印将要添加的新行信息
                value_csv = value_csv.append({"业务": business, "价值": value_range, "占比": percentage}, ignore_index=True)
            else:
                print(f"更新现有行：业务={business}, 价值={value_range}, 占比={percentage}")  # 打印将要更新的行信息
                value_csv.loc[row_index, "占比"] = percentage

    print("更新后的DataFrame：")
    print(value_csv)  # 打印更新后的DataFrame

    # 保存 DataFrame 到 CSV 文件
    print(f"将要保存的数据：\n{value_csv}")  # 确认 DataFrame 中的数据是否正确
    value_csv.to_csv(value_file_path, index=False, encoding='utf-8-sig')
    print("数据保存成功。")


# test
if __name__ == '__main__':
    save_or_update_value_csv(generate_value_percentages(load_config()))    







