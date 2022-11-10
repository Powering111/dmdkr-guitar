# Entry Point
from backend import process
from threading import Thread

from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, send_file
from werkzeug.utils import secure_filename

import json
from datetime import datetime
import os
app = Flask(__name__)
app.secret_key = os.getenv('secret_key',b'\xe4\xd5\x91|\x06\x97\x89-\xf5\xdfP\xa5{\xb4\x13\x90\x1f\xa8o\xf6\x85\x15\xb9\x06\x94\xbeL\xd1\xc6\xad\x80\xe1')
app.config['UPLOAD_FOLDER'] = 'uploads'
port=80

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route("/upload", methods=["PUT"])
def upload_user_profile_image():
    if not request.form['title']:
        return {"valid":False, "code":"no title?"}
    if not request.files['video']:
        return {"valid":False, "code": "no video"}
    extension = os.path.splitext(request.files['video'].filename)[1]
    if extension in [".mp4",".mov",".avi",".mkv"]:
        # this is not secure method
        title = request.form['title']
        filename =title
        #filename += datetime.now().strftime(' %Y-%m-%d %H-%M-%S')
        filename += extension
        print("saving " + filename)
        request.files['video'].save(os.path.join(app.config["UPLOAD_FOLDER"],filename))

        # start processing file
        th = Thread(target=process,args=(filename,title))
        th.start()
        return {'valid':True, "code":"Successfully uploaded image!",'filename':filename}
    else:
        return {'valid':False,"code":"file extension err!"}

@app.route('/check')
def check_processed():
    filename=request.args.get('filename')
    #filename = secure_filename(filename)
    return {'finished':True} if os.path.isfile('processed/'+filename+'.musicxml') else {'finished':False}

@app.route('/list')
def check_list():
    li = os.listdir('processed')
    li2= []
    for x in li:
        li2.append(os.path.splitext(x)[0])
    return {'valid':True,'list':li2}

@app.route('/video/<filename>')
def return_video(filename):
    #very dangerous code!!!!
    return send_file("uploads/"+filename)

@app.route('/sheet/<filename>')
def return_sheet(filename):
    #very dangerous code!!!!
    return send_file("processed/"+filename)



app.run(host='0.0.0.0',port=port,debug=True)