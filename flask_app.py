from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from io import BytesIO
import base64

from utils import value_percentages, csv_path
from functions import save_data_to_csv

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form
        data = {}
        data['project'] = request.form['project']
        data['designer'] = request.form['designer']
        data['contact'] = request.form['contact']
        data['start_date'] = request.form['start_date']
        data['end_date'] = request.form['end_date']
        data['duration'] = request.form['duration']
        data['business_type'] = request.form['business_type']
        data['value'] = request.form['value']
        data['remarks'] = request.form['remarks']

        save_data_to_csv(data, [])
        
        flash('数据已成功保存!')
        return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form
    data = {}
    data['project'] = request.form['project']
    data['designer'] = request.form['designer']
    data['contact'] = request.form['contact']
    data['start_date'] = request.form['start_date']
    data['end_date'] = request.form['end_date']
    data['duration'] = request.form['duration']
    data['business_type'] = request.form['business_type']
    data['value'] = request.form['value']
    data['remarks'] = request.form['remarks']

    save_data_to_csv(data)
    
    flash('数据已成功保存!')
    return redirect(url_for('index'))

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    # Load the data
    df = pd.read_csv(csv_path)

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
