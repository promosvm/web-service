from flask import Flask, request, jsonify, make_response, redirect, url_for, render_template
import flask
from markupsafe import escape
import numpy as np
from joblib import dump, load
from sklearn import datasets
import os
import pandas as pd

#помещяем сюда модель, что-бы кажый раз не перезапускать
knn = load('knn.pkl') 

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello best friend i am less. What are you name, and why are you here!</h1>"

@app.route('/user/<username>')
def show_user_profile(username):
    username = float(username) * float(username)
    return f'User {escape(username)}'

def average(numbers):
    return sum(numbers) / len(numbers)

@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    return str(average(nums))


@app.route('/badrequest')
def badrequest():
    resp = make_response("Record not found", 400)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.route('/iris/<param>')
def iris(param):
    try:
        param = param.split(',')
        param = [float(num) for num in param]
        #принт делаяется для того что-бы проверить что все ОК
        print(param)

        param = np.array(param).reshape(1, -1)

        predict = knn.predict(param)

        return(str(predict))
    
    except:
        return redirect(url_for(badrequest))


@app.route('/show_image')
def show_image():
    return '<img src="static/Kosaciec_szczecinkowaty_Iris_setosa.jpg" alt="Setosa">'
 

@app.route('/iris_post', methods=['POST'])
def add_message():
    content = request.get_json()

    param = content['flower'].split(',')
    param = [float(num) for num in param]

    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param)

    predict = {'class':str(predict[0])}

    return jsonify(predict)





from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField(validators=[])


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name.data)

        f = form.file.data
        filename = form.name.data + '.csv'
        # f.save(os.path.join(filename
        # ))

        df = pd.read_csv(f, header=None)
        predict = knn.predict(df)

        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)

        flask.send_file(filename, 
                        mimetype='text/csv', 
                        as_attachment=True,
                        download_name=filename)


    return render_template('submit.html', form=form)




import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file_download'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


