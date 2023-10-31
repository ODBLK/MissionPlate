
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from io import BytesIO
import base64
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

def save_data_to_csv(project, business_type, value, contact, start_date, end_date, duration, remarks):
    csv_path = './data/ProjectData.csv'
    # 读取现有的数据
    df_existing = pd.read_csv(csv_path)

    # 创建新数据的DataFrame
    new_data = pd.DataFrame({
        '项目': [project],
        '对接人': [contact],
        '开始日期': [start_date],
        '结束日期': [end_date],
        '耗时/天': [duration],
        '业务类型': [business_type],
        '价值': [value],
        '备注': [remarks]
    })

    # 将新数据追加到现有的数据
    df_combined = pd.concat([df_existing, new_data], ignore_index=True)

    # 将合并后的数据保存回CSV
    df_combined.to_csv(csv_path, mode='a', header=False, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form
        project = request.form['project']
        business_type = request.form['business_type']
        value = request.form['value']
        contact = request.form['contact']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        duration = request.form['duration']
        remarks = request.form['remarks']

        save_data_to_csv(project, business_type, value, contact, start_date, end_date, duration, remarks)
        
        flash('数据已成功保存!')
        return redirect(url_for('index'))

    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form
    project = request.form['project']
    business_type = request.form.get('business_type', '')
    value = request.form.get('value', '')
    contact = request.form['contact']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    duration = request.form.get('duration', '')
    remarks = request.form.get('remarks', '')

    save_data_to_csv(project, business_type, value, contact, start_date, end_date, duration, remarks)
    
    flash('数据已成功保存!')
    return redirect(url_for('index'))


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    # Load the data
    df = pd.read_excel('项目分析.xlsx')

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




# 读取Excel文件
data_path = "项目分析.xlsx"
df = pd.read_excel(data_path, sheet_name="数据源")

# 新增一个字典来存储业务价值的占比
value_percentages = {
    '业务1': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务2': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务3': {'价值1': 0, '价值2': 0, '价值3': 0},
    '业务4': {'价值1': 0, '价值2': 0, '价值3': 0},
    '其他': {'价值1': 0, '价值2': 0, '价值3': 0}
}

@app.route('/value', methods=['GET', 'POST'])
def value():
    if request.method == 'POST':
        for key in value_percentages.keys():
            for subkey in value_percentages[key].keys():
                value_percentages[key][subkey] = float(request.form.get(f"{key}_{subkey}", 0))

        # 验证三项加起来是否为100%
        for key, sub_dict in value_percentages.items():
            if sum(sub_dict.values()) != 100.0:
                flash(f'{key}的价值占比总和不为100%', 'danger')
                return redirect(url_for('value'))

        # 这里可以将value_percentages保存到Excel表3.2
        save_to_excel(value_percentages)

        flash('数据已更新!', 'success')
        return redirect(url_for('index'))

    return render_template('value.html', values=value_percentages)

if __name__ == '__main__':
    app.run(debug=True)
