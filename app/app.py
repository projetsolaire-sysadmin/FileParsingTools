import sqlite3
from flask import Flask, render_template, request, send_file
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from app.main import main

UPLOAD_FOLDER = 'upload_files'
ALLOWED_EXTENSIONS = {'csv'}
file_formatted =""

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lgjdslgfgjldfgjkfjhlsfdgvj1kltjqm'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
print(app.config['UPLOAD_FOLDER'])

app.config['output_file'] =""

def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    # conn.close()
    return render_template('index.html') #, posts=posts)

"""
@app.route('/', methods=('GET', 'POST'))
def post():
    print("hello")
    print(request.form.get('completerannee'))
    
    if request.method == 'POST':
        cb=request.form.get('completerannee')
        print(cb)
        if cb=="on": 
            completer_annee = True 
        else: 
            completer_annee = False
        print(completer_annee)
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return "traitement en cours..."
    # return render_template('post.html')
"""


@app.route('/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # print(1,request.files['file'])
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            print(f)
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            print("here")

            # print(os.path.join(UPLOAD_FOLDER, f.filename))
            app.config['output_file'] = os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename)
            
            return render_template('download.html')
            # return 'file uploaded successfully' #redirect(request.url)
        else:
            return "not csv file"


@app.route('/download/')
def Download_File():
    print('download')
    return send_file(app.config['output_file'],as_attachment=True)