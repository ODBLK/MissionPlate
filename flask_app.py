from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from io import BytesIO
import base64
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

from utils import dir_prefix, project_file, value_file, req_info
from functions import save_data_to_csv, load_config, generate_value_percentages, save_or_update_value_csv

app = Flask(__name__)
app.secret_key = 'secret_key'
config_data = load_config()  # 初始加载配置数据
value_percentages = generate_value_percentages(config_data)

#读取config
# class ConfigFileHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         global config_data, value_percentages
#         if not event.is_directory and event.src_path.endswith('config.json'):
#             print(f"Detected modification: {event}")  # 打印事件详情
#             config_data = load_config()
#             value_percentages = generate_value_percentages(config_data)
#             print("Config reloaded and value percentages updated!")
class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global config_data, value_percentages
        if not event.is_directory and event.src_path.endswith('config.json'):
            print(f"Detected modification: {event}")  # 打印事件详情
            config_data = load_config()
            value_percentages = generate_value_percentages(config_data)
            # 在这里调用新的函数来更新 CSV 文件
            save_or_update_value_csv(value_percentages, os.path.join(dir_prefix, value_file))
            print("Config reloaded and value percentages updated!")

# 监控config修改并加载最新config
observer = Observer()
observer.schedule(ConfigFileHandler(), path='.', recursive=False)
observer.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form
        data = {}
        for i in req_info:
            data[i] = request.form[i]

        save_data_to_csv(data, 'project')
        flash('数据已成功保存!')
        return redirect(url_for('index'))

    return render_template('form.html', config=config_data)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form
    data = {}
    for i in req_info:
            data[i] = request.form[i]

    save_data_to_csv(data, 'project')
    
    flash('数据已成功保存!')
    return redirect(url_for('index'))

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    # Load the data
    df = pd.read_csv(os.path.join(dir_prefix, project_file))

    # Prepare the treemap data
    tree_data = df.groupby(['备注', '项目']).size().reset_index(name='counts')

    # Create the treemap
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.viridis
    mini = min(tree_data['counts'])
    maxi = max(tree_data['counts'])
    norm = plt.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in tree_data['counts']]
    squarify.plot(sizes=tree_data['counts'], label=tree_data['备注'] + '\n' + tree_data['项目'], alpha=0.6, color=colors, ax=ax)
    plt.title("矩形树图展示价值和业务类型的关系", fontsize=15)
    plt.axis('off')

    # Convert the plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('chart.html', graph_url=graph_url)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/gantt')
def gantt():
    return render_template('gantt.html')

@app.route('/value', methods=['GET', 'POST'])
def value():
    # 载入最新的配置
    config_data = load_config()
    # 生成初始的百分比字典
    value_percentages = generate_value_percentages(config_data)

    if request.method == 'POST':
        print(request.form)  # 打印表单数据以确保它们被接收
        # 遍历表单中的数据，更新 value_percentages 字典
        for key in value_percentages.keys():
            for subkey in value_percentages[key].keys():
                form_key = f"{key}_{subkey}"
                value_percentages[key][subkey] = float(request.form.get(form_key, 0))

        # # 验证每个业务类型的各价值占比总和是否为100%
        # for key, sub_dict in value_percentages.items():
        #     if sum(sub_dict.values()) != 100.0:
        #         flash(f'{key}的价值占比总和不为100%', 'danger')
        #         return redirect(url_for('value'))

        # 保存更新后的 value_percentages 到 CSV 文件
        save_or_update_value_csv(value_percentages)
        flash('数据已更新!', 'success')
        return redirect(url_for('index'))

    # 如果是 GET 请求，或者表单验证未通过，则渲染价值分配界面
    # 此处需要从 CSV 文件读取当前的价值分配情况，并传递到模板中
    return render_template('value.html', values=value_percentages, config=config_data)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        observer.stop()
    observer.join()
