import glob
import pikepdf # pip3 install pikepdf

pdffiles = []
for file in glob.glob("*.pdf"):
    pdffiles.append(file)

print(pdffiles)

# file = "1810.04805.pdf"
file = "pdf_files/2020/nime2020_paper98.pdf"
# file = "1710.05006.pdf"
for file in pdffiles:
    try:
        print('=================================')
        print(f'##### {file} #####')
        pdf_file = pikepdf.Pdf.open(file)
        urls = []
        # iterate over PDF pages
        for page in pdf_file.pages:
            for annots in page.get("/Annots"):
                uri = annots.get("/A").get("/URI")
                if uri is not None:
                    print("[+] URL Found:", uri)
                    urls.append(uri)
        print('=================================')
    except TypeError:
        print('TypeError')
    except AttributeError:
        print('AttributeError')
    
# print("[*] Total URLs extracted:", len(urls))

# import pdfx 
  
# # reading pdf file 
# pdf = pdfx.PDFx("nime2020_paper0.pdf") 
  
# # display 
# print(pdf.get_metadata)

# import PyPDF2

# pdf = PyPDF2.PdfFileReader('1810.04805.pdf')

# urls = []
# for page in range(pdf.numPages):
#     pdfPage = pdf.getPage(page)
#     try:
#         for item in (pdfPage['/Annots']):
#             # print(type(item))
#             # urls.append(item['/A']['/URI'])
#     except KeyError:
#         pass

# import PyPDF2

# PDFFile = open('nime2020_paper98.pdf','rb')

# PDF = PyPDF2.PdfFileReader(PDFFile)
# pages = PDF.getNumPages()
# key = '/Annots'
# uri = '/URI'
# ank = '/A'

# for page in range(pages):

#     pageSliced = PDF.getPage(page)
#     pageObject = pageSliced.getObject()

#     if pageObject.has_key(key):
#         ann = pageObject[key]
#         for a in ann:
#             u = a.getObject()
#             if u[ank].has_key(uri):
#                 print(u[ank][uri])