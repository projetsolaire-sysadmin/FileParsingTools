import sqlite3
from flask import Flask, render_template, request, send_file, session, app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from app.main import main
from datetime import timedelta

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

app.config['filename'] =""
app.config['output_file'] =""



@app.before_request #https://www.codegrepper.com/code-examples/python/how+to+set+request+timeout+in+flask
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    # conn.close()
    return render_template('base+upload.html') #, posts=posts)

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
"""
@app.route('/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # print(1,request.files['file'])
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))

            # print(os.path.join(UPLOAD_FOLDER, f.filename))
            app.config['output_file'] = main(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            
            # patch :
            print("patch error app/app :", app.config['output_file'][4:])
            app.config['output_file']= app.config['output_file'][4:]
            print("patch error app/app :",app.config['output_file'])
            
            return render_template('download.html')
            # return 'file uploaded successfully' #redirect(request.url)
        else:
            return "not csv file"


@app.route('/download/')
def Download_File():
    print('download')
    print(app.config['output_file'])
    return send_file(app.config['output_file'], as_attachment=True)
    """

def loader2():
    return render_template('base+loader.html')

#https://flask.palletsprojects.com/en/1.1.x/quickstart/

"""Nouvelle version avec base.html"""
@app.route('/about', methods=('GET', 'POST'))
def about():
    return render_template('base+about.html')

@app.route('/elance', methods=('GET', 'POST'))
def elance():
    return render_template('base+elance.html')

@app.route('/', methods=('GET', 'POST'))
def upload():
    return render_template('base+upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # print(1,request.files['file'])
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            render_template('base+elance.html')
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))

            # print(os.path.join(UPLOAD_FOLDER, f.filename))
            app.config['output_file'] = main(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            
            # patch :
            print("patch error app/app :", app.config['output_file'][4:])
            app.config['output_file']= app.config['output_file'][4:]
            print("patch error app/app :",app.config['output_file'])
            
            return render_template('base+download.html')
            # return 'file uploaded successfully' #redirect(request.url)
        else:
            return "not csv file"

"""
@app.route('/loader')
def loader():
    return render_template('base+download.html')
"""
"""
@app.route('/upload', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # print(1,request.files['file'])
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            app.config['filename'] =f.filename
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            
            return render_template('base+loader.html')
        else:
            return "not csv file"
"""
"""
@app.route("/loadingDone", methods=['GET', 'POST'])
def loadingDone():
    print("test")
    return render_template('base+download.html')
"""
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs
# -> https://stackoverflow.com/questions/72338204/flask-show-loading-page-while-another-time-consuming-function-is-running
"""@app.route('/loader')
def loader():
    print("loader")
    
    # print(os.path.join(UPLOAD_FOLDER, f.filename))
    app.config['output_file'] = main(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), app.config['filename']))
            
    # patch :
    print("patch error app/app :", app.config['output_file'][4:])
    app.config['output_file']= app.config['output_file'][4:]
    print("patch error app/app :",app.config['output_file'])

    # return 'file uploaded successfully' #redirect(request.url)
    return render_template('base+download.html')"""


@app.route('/download')
def download():
    print('download')
    print(app.config['output_file'])
    return send_file(app.config['output_file'], as_attachment=True)
   

@app.route('/CO2', methods=('GET', 'POST'))
def CO2():
    return render_template('base+CO2.html')

