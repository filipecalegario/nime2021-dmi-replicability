import re
import bibtexparser
import fitz

nime_file = "bib_files/nime2020.bib"

## Load
print(f"Going to load: {nime_file}, hope that's ok.")

with open(nime_file) as bibtex_file:
    bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
    
print(f"Loaded {len(bib_database.entries)} entries.")

for e in bib_database.entries:
    print('==================================')
    title = e['title']
    print(title)
    pdf_file = e['url']
    print('PDF URL:', pdf_file)
    year = e['year']
    url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    with fitz.open(pdf_file.replace(f'https://www.nime.org/proceedings/{year}/','')) as pdf:
        text = ""
        for page in pdf:
            # extract text of each PDF page
            text += page.getText()
        urls = []
    # extract all urls using the regular expression
        for match in re.finditer(url_regex, text):
            _start = match.start()
            _end = match.end()
            print('Recorte: ', text[_start:_end+100])
            url = match.group()
            print("[+] URL Found:", url)
            urls.append(url)
        print("[*] Total URLs extracted:", len(urls))
    print('==================================')

# file = open('merged-file.txt', encoding='latin')

# line = file.read().replace('\n', ' ')

# urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)



