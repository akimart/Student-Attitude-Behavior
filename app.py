from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Membuat folder 'uploads' jika belum ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

df = None  # Variabel global untuk menyimpan dataset

@app.route('/', methods=['GET', 'POST'])
def index():
    global df
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            df = pd.read_csv(filepath)
            return redirect(url_for('analysis'))
    return render_template('index.html')

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    global df
    if df is None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        query = request.form['query']
        result = None
        try:
            # Evaluasi query pengguna
            result = eval(f'df{query}')
        except Exception as e:
            result = f'Error: {e}'
        
        return render_template('analysis.html', tables=[result.to_html(classes='data') if isinstance(result, pd.DataFrame) else result], titles=[''])
    
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)