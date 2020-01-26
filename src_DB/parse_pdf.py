from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import pdftitle
# from pdfminer.pdftype import PDFObjRef, resolver1

fp = open("./Books/[Michael_Dawson]_Beginning_C++_through_game_progra(BookZZ.org).pdf", 'rb')
parser = PDFParser(fp)
doc = PDFDocument(parser)

print(doc.info)

title = pdftitle.get_title_from_io(fp)
print(title)
# print(type(doc.info))
# print(doc.info[0]['Title'])