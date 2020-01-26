
from PyPDF2 import PdfFileReader
import os
import pdftitle

#adds all the books to a list
folderpath = r"./Books"
filepaths = [os.path.join(folderpath,name) for name in os.listdir(folderpath)]
all_files = []

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

            # make sure first page can be text processed
            # by checking if it has a font
            page_data = pdf.getPage(0)
            print(page_data['/Resources'])
            if '/Font' in page_data['/Resources']:
                # process title using pdftitle by examining first page
                title = pdftitle.get_title_from_io(fp)
                if title is not None:
                    print("\tTITLE: " + title)
                else:
                    print("\tTITLE: (none extracted)")

            else:
                print("\tTitle: Cannot parse text on first page")

    else:
        print("\tNOT A PDF")