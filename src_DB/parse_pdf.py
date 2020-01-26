from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os

#adds all the books to a list
folderpath = r"./Books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
all_files = []

#loops through the list and prints metadata for each book
for path in filepaths:
    with open(path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        print(doc.info)

