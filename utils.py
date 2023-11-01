import os
import pandas as pd

# 数据路径
csv_dir = './data'
csv_file = 'ProjectData.csv'
csv_path = os.path.join(csv_dir, csv_file)

# 新增一个字典来存储业务价值的占比
value_percentages = {
    '业务1': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务2': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务3': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务4': {'价值1': 0, '价值2': 0, '价值3': 0},
    '其他': {'价值1': 0, '价值2': 0, '价值3': 0}
}
