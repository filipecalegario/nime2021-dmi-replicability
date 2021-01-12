import fitz # pip install PyMuPDF
import re

# a regular expression of URLs
file = "pdf_files/2020/nime2020_paper98.pdf"
# extract raw text from pdf
# file = "1710.05006.pdf"
# file = "1810.04805.pdf"
# open the PDF file
url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
with fitz.open(file) as pdf:
    text = ""
    for page in pdf:
        # extract text of each PDF page
        text += page.getText()
    urls = []
# extract all urls using the regular expression
    for match in re.finditer(url_regex, text):
        _start = match.start()
        _end = match.end()
        url = match.group()
        print("[+] URL Found:", url)
        print('Recorte: ', text[_start:_end+100].replace('\n',''))
        urls.append(url)
    print("[*] Total URLs extracted:", len(urls))