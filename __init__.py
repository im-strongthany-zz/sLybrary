from flask import Flask, flash, redirect, render_template, request, session, abort
from form import BookSearchForm
import os
import urllib.request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf'])
UPLOAD_FOLDER = './test_books'

app = Flask(__name__, template_folder='src_DB/templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are pdf')
			return redirect(request.url)

@app.route('/', methods=['GET','POST'])
def index():
    search = BookSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # else:
    #     return "Hello!"

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    # don't sdisplay results if empty, otherwise switch to results page
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('results.html', results=results)


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()

        if __name__ == "__main__":
            app.secret_key = os.urandom(12)
            app.run(debug=True,host='0.0.0.0', port=4000)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
