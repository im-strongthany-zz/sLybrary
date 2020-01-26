import pdfx
import os
from pymongo import MongoClient
import datetime
import pprint


folderpath = r"./Books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]

# extract the metadata from the pdf object
# extract the references from the pdf
# create a python dictionary of the references
for path in filepaths:
    pdf = pdfx.PDFx(path)
    metadata = pdf.get_metadata()
    reference_dict = pdf.get_references_as_dict()

# extract the text from the PDF
# replace the return characters with nothing creating one long string
# split the string at the form feed characters
text = pdf.get_text()
text_to_mongo = text.replace('\n', '').split("\x0c")

# insert documents (stored as dictionaries in BSON (JSON) format (UTF-8))
# notice we can create the schema we want ad-hoc for our document
post = {
    "metadata": metadata,
    "text": text_to_mongo,
    "references": reference_dict,
    "import_date": datetime.datetime.utcnow(),
    "tags": ["pdf"]
}

# create a variable for the database
client = MongoClient('localhost', 27017)
db = client["sLybrary"]

# create an object for your PDF data, then insert it into the database
posts = db.posts
post_id = posts.insert_one(post).inserted_id

# now check the output for your new MongoDB document
pprint.pprint(posts.find_one())  # search with dict keys or "_id" for Mongo UID
