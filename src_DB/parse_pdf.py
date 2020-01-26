
from PyPDF2 import PdfFileReader
import pdftitle
from pdf2image import convert_from_path
import textract
import pytesseract
from tesserocr import PyTessBaseAPI, iterate_level, RIL
import os
from PIL import Image
import io

#adds all the books to a list
folderpath = r"../test_books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
all_files = []

temp_file = ".temp_frontpage.jpg"

def extractTitle(fp, page):
    # make sure first page can be text processed
    # by checking if it has a font
    page_data = pdf.getPage(page)  
    # print(page_data['/Resources'])
    if '/Font' in page_data['/Resources']:
        # process title using pdftitle by examining first page
        title = pdftitle.get_title_from_io(fp)
        return title

def orcTitle():
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
        return title
    

#loops through the list and prints metadata for each book
for path in filepaths:
    # print filepath
    print(path)

    # make sure it's a pdf
    extension = os.path.splitext(path)[1]
    if(extension == ".pdf"):
        with open(path, 'rb') as fp:
            # use pypdf2 to read metadata
            pdf = PdfFileReader(fp)
            info = pdf.getDocumentInfo()
            print("\tMETADATA:")
            for k, v in info.items():
                print("\t\t", k, ": ", v)

            # use title from metadata
            title = info.title

            # if not present
            if title is None or title == '':
                # extract title from first page
                title = extractTitle(fp, 0)

                #if cannot extract
                if title is None or title == '':
                    # attempt to extract from image
                    title = orcTitle()
                    # text = textract.process(temp_file)
                    # print(text)
                    # os.remove(temp_file)
                    # print("\tTitle: Cannot parse text on first page")

            if title is not None:
                print("\tTITLE: '" + title + "'")
            else:
                print("\tTITLE: (none extracted)")

    else:
        print("\tNOT A PDF")