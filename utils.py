import os
import pandas as pd

# 数据路径
dir_prefix = './data'
project_file = 'ProjectData.csv'
value_file = 'ValueData.csv'

# request信息
req_info = ['project', 'designer', 'contact', 'start_date', 'end_date', 'duration', 'business_type', 'value', 'remarks']

# 新增一个字典来存储业务价值的占比
value_percentages = {
    '业务1': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务2': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务3': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务4': {'价值1': 0, '价值2': 0, '价值3': 0},
    '其他': {'价值1': 0, '价值2': 0, '价值3': 0}
}
