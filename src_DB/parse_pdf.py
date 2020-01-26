from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

fp = open("/home/marta/sLybrary/src_DB/Books/[Brian_W._Kernighan,_Dennis_M._Ritchie]_The__C_Pro(BookZZ.org).pdf")
parser = PDFParser(fp)
doc = PDFDocument(parser)

print(doc.info)