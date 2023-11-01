import sqlite3
from flask import Flask, render_template, request, send_file, session, app, jsonify
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from app.main import main
from datetime import timedelta
from threading import Thread

UPLOAD_FOLDER = 'upload_files'
ALLOWED_EXTENSIONS = {'csv'}
file_formatted =""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lgjdslgfgjldfgjkfjhlsfdgvj1kltjqm'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

app.config['filename'] =""
app.config['output_file'] =""
# app.config['lancer_le_processus'] =False
app.config['finished']=True #remplacer par "status"
th = Thread()

import time
# app.config['TEMPLATES_AUTO_RELOAD'] = True

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

#https://flask.palletsprojects.com/en/1.1.x/quickstart/

"""Nouvelle version avec base.html"""
@app.route('/accueil', methods=('GET', 'POST'))
def accueil():
    return render_template('base+accueil.html')

@app.route('/about', methods=('GET', 'POST'))
def about():
    return render_template('base+about.html')

@app.route('/elance', methods=('GET', 'POST'))
def elance():
    return render_template('base+elance.html')

@app.route('/explorer', methods=('GET', 'POST'))
def explorer():
    return render_template('base+explorer.html')

@app.route('/', methods=('GET', 'POST'))
def upload():
    return render_template('base+upload.html')

def patch_app_app(s):
    if 'app/app' in s or 'app\\app' in s:
        return s.replace('app/app','app')
    else:
        return s
    
def do_work():
    app.config['output_file'] = main(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), app.config['filename']))
    print('traitement terminé')
    print(app.config['output_file'])
    app.config['finished']=True
    if app.config['output_file']=='PRODUCTION_FILE_ALREADY_PARSED_TYPE':
        return False
    else:
        # patch : car sur le serveur heroku ça réagit différemment
        print("patch error 'app/app' before :", app.config['output_file'])
        app.config['output_file']=patch_app_app(app.config['output_file'])
        app.config['output_file']= app.config['output_file'][4:]
        print("patch error 'app/app' after :", app.config['output_file'])
        return True
                
@app.route('/upload', methods=['GET', 'POST'])
def post():
    print("here at post")
    if request.method == 'POST':
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            print("here at post")
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            app.config['filename']=f.filename
            if do_work():
                print("here at post")
                return render_template('base+download.html')
            else:
                return render_template('base+download.html')


        else:
            return "not csv file"
        
@app.route('/production', methods=('GET', 'POST'))
def upload_production():
    return render_template('base+production.html')

@app.route('/prod', methods=['GET', 'POST'])
def postProductionFile():
    if request.method == 'POST':
        # print(1,request.files['file'])
        f = request.files['file']
        if secure_filename(f.filename)[-4:]==".csv":
            f.save(os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), f.filename))
            app.config['filename']=f.filename

            """ méthode 1 (sans loader)"""
            if do_work():
                return render_template('base+download.html')
            else:
                return "fichier déjà formaté"
            # return 'file uploaded successfully' #redirect(request.url)

        else:
            return "not csv file"
        
  
""" méthode 3 thread"""
@app.route('/status')
def thread_status():
    """ Return the status of the worker thread """
    # print('status : ',app.config['finished'])
    return jsonify(dict(status=('finished' if app.config['finished'] else 'running')))
  

@app.route('/loader', methods=['GET', 'POST'])
def loader():
    return render_template('base+loader.html')

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs
# -> https://stackoverflow.com/questions/72338204/flask-show-loading-page-while-another-time-consuming-function-is-running

@app.route('/download')
def download():
    file = app.config['output_file']
    print('user downloads the output file :', file)

    return send_file(file, as_attachment=True)

# https://stackoverflow.com/questions/43644038/flask-heroku-file-not-found-error-on-mobiles (sans réponse)
# https://stackoverflow.com/questions/72963901/heroku-python-filenotfounderror-errno-2-no-such-file-or-directory
# https://stackoverflow.com/questions/54086013/cannot-find-file-on-trying-to-deploy-to-heroku-works-locally

@app.route('/CO2', methods=('GET', 'POST'))
def CO2():
    return render_template('base+CO2.html')


