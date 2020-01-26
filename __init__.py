from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from form import BookSearchForm
import os
import urllib.request
from werkzeug.utils import secure_filename
from pdf_to_mongo import pdfToMongo
from pymongo import MongoClient
from table import Results
from bson.objectid import ObjectId
import gridfs

ALLOWED_EXTENSIONS = set(['pdf'])
UPLOAD_FOLDER = '.'
DOWNLOAD_FOLDER = '~/home/downloads'

app = Flask(__name__, template_folder='templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

client = MongoClient("mongodb+srv://admin:openSourceTextbooks@slybrary-jbhct.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client["sLybrary"]
collection = db['test_books']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		# process file if a pdf
		if file and allowed_file(file.filename):
			# determine filename and transfer path, then save it at the path
			filename = secure_filename(file.filename)
			new_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(new_loc)

			# send file to mongoDB, then delete local version
			pdfToMongo(new_loc, collection)
			flash('File successfully uploaded')
			os.remove(new_loc)

			# send back to hompeage
			return redirect(url_for('index'))

		else:
			flash('Allowed file types are pdf')
			return redirect(request.url)

@app.route('/results', methods=['POST'])
def search_results(search):
	results = []
	search_string = search.data['search']

	results = collection.find({"$text":{"$search": search_string}})
	#.sort({"score": {"$meta": "textScore"}})
	print(results)
	# don't display results if empty, otherwise switch to results page
	if not results:
		flash('No results found!')
		return redirect('/')
	else:
		table = Results(results)
		table.border = True
		return render_template('results.html', table=table)

@app.route('/item/<id>', methods = ['GET', 'POST'])
def download(id):
	if id:
		qry = collection.find({id:'id'})
		# print(qry)
		if qry.count() > 0:
			file = qry[0]
			if file:
				print("Downloading...")
				file_out = open(os.path.join(	file['title'],'w'))
				file_out.write(file['file'])
				file_out.close()

		else:
			flash('file binary could not be retrieved at this time')

	return redirect(url_for('index'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0')
