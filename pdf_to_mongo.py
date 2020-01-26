from PyPDF2 import PdfFileReader
import pdftitle
# import pdfx
import os
import datetime
import pprint
from bson.binary import Binary
from pdf2image import convert_from_path
from tesserocr import PyTessBaseAPI, iterate_level, RIL
import gridfs

# folderpath = r"./books"
# filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
# create a variable for the database
temp_file = ".temp_frontpage.jpg"

def extractTitle(fp, pdf, page):
    # make sure first page can be text processed
    # by checking if it has a font
    page_data = pdf.getPage(page)  
    # print(page_data['/Resources'])
    if '/Font' in page_data['/Resources']:
        # process title using pdftitle by examining first page
        title = pdftitle.get_title_from_io(fp)
        return title

def orcTitle(path):
     # make first page into jpeg
    page = convert_from_path(path, first_page=0, last_page = 1)[0]
    page.save(temp_file, 'JPEG') 

    # use ocr to extract title
    # image = Image.open(temp_file)
    with PyTessBaseAPI() as api:
        api.SetImageFile(temp_file)
        api.Recognize()  # required to get result from the next line
        ri = api.GetIterator()

        # loop through and find largest text size
        level = RIL.TEXTLINE
        maxSize = 0
        for r in iterate_level(ri, level):
            # extract line of text
            text = r.GetUTF8Text(level)

            # get line's font size
            fontSize = r.WordFontAttributes()['pointsize']

            # check to see if current max
            # remove extra spaces/newlines/tabs (etc.) when testing min length req
            if len(''.join(text.split())) > 1 and fontSize > maxSize:
                maxSize = fontSize


        # loop through again and concatenate largest words
        ri = api.GetIterator()
        level = RIL.TEXTLINE
        title_list = []
        for r in iterate_level(ri, level):
            text = r.GetUTF8Text(level)
            fontSize = ri.WordFontAttributes()['pointsize']
            if len(''.join(text.split())) > 1 and fontSize > maxSize - 15:
                # add title words to list
                title_list.extend(r.GetUTF8Text(level).split())

        # concatenate them back together
        title = ' '.join(title_list)

        os.remove(temp_file)
        return title
        
def pdfToMongo(path, collection):
    # print filepath
    print(path)

    # make sure it's a pdf
    extension = os.path.splitext(path)[1]
    if(extension == ".pdf"):
        # use pypdf2 to read metadata
        fp = open(path, 'rb')
        pdf = PdfFileReader(fp)
        info = pdf.getDocumentInfo()
        encoded = Binary(fp.read())
        # print("\tMETADATA:")
        # for k, v in info.items():
        #     print("\t\t", k, ": ", v)

        # use title from metadata
        title = info.title

        # if not present
        if title is None or title == '':
            # extract title from first page
            title = extractTitle(fp, pdf, 0)

            #if cannot extract
            if title is None or title == '':
                # attempt to extract from image
                title = orcTitle(path)

        post = {
            "title": title,
            "import_date": datetime.datetime.utcnow(),
            "file": encoded,
            "tags": ["pdf"]
        }

        # create an object for your PDF data, then insert it into the database
        post_id = collection.insert_one(post).inserted_id        
    
    else:
        print("\tNOT A PDF")
