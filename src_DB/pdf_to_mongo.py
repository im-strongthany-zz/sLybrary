from PyPDF2 import PdfFileReader
import pdftitle
# import pdfx
import os
from pymongo import MongoClient
import datetime
import pprint


folderpath = r"./books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
# create a variable for the database
client = MongoClient("mongodb+srv://admin:openSourceTextbooks@slybrary-jbhct.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client["sLybrary"]
collection = db['test_books']

# extract the metadata from the pdf object
# extract the references from the pdf
# create a python dictionary of the references
for path in filepaths:
    # print filepath
    print(path)

    # make sure it's a pdf
    extension = os.path.splitext(path)[1]
    if(extension == ".pdf"):
        # pdf = pdfx.PDFx(path)
        # metadata = pdf.get_metadata()
        # reference_dict = pdf.get_references_as_dict()

        # # extract the text from the PDF
        # # replace the return characters with nothing creating one long string
        # # split the string at the form feed characters
        # text = pdf.get_text()
        # text_to_mongo = text.replace('\n', '').split("\x0c")

        # # insert documents (stored as dictionaries in BSON (JSON) format (UTF-8))
        # # notice we can create the schema we want ad-hoc for our document
        # post = {
        #     "metadata": metadata,
        #     "text": text_to_mongo,
        #     "references": reference_dict,
        #     "import_date": datetime.datetime.utcnow(),
        #     "tags": ["pdf"]
        # }

        # use pypdf2 to read metadata
        fp = open(path, 'rb')
        pdf = PdfFileReader(fp)
        info = pdf.getDocumentInfo()
        print("\tMETADATA:")
        for k, v in info.items():
            print("\t\t", k, ": ", v)

        # make sure first page can be text processed
        # by checking if it has a font
        page_data = pdf.getPage(0)
        if '/Font' in page_data['/Resources']:
            # process title using pdftitle by examining first page
            title = pdftitle.get_title_from_io(fp)
            if title is not None:
                print("\tTITLE: " + title)
            else:
                print("\tTITLE: (none extracted)")

            post = {
                "title": title,
                "import_date": datetime.datetime.utcnow(),
                "tags": ["pdf"]
            }

            # create an object for your PDF data, then insert it into the database
            post_id = collection.insert_one(post).inserted_id

            # now check the output for your new MongoDB document
            # pprint.pprint(posts.find_one())  # search with dict keys or "_id" for Mongo UID
            # print(client.list_database_names())
            # print(db.list_collection_names())

        else:
            print("\tTitle: Cannot parse text on first page")

        
    
    else:
        print("\tNOT A PDF")
