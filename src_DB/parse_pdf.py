from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os

folderpath = r"./Books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
all_files = []

for path in filepaths:
    with open(path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        print(doc.info)

#fp = open("./Books/Linux-101-Hacks.pdf", "rb")
#parser = PDFParser(fp)
#doc = PDFDocument(parser)

#print(doc.info)
