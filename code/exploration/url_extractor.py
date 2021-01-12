import re
import bibtexparser
import fitz

def add_variables(id, title, authors, abstract, link):
    html_template = f'''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="description" content="">
            <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
            <meta name="generator" content="Hugo 0.79.0">
            <title>Review Page</title>

            <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/album/">

            <!-- Bootstrap core CSS -->
        <link href="../assets/dist/css/bootstrap.min.css" rel="stylesheet">
            
        </head>
        <body>
            
        <header>
        <div class="navbar navbar-dark bg-dark shadow-sm">
            <div class="container">
            <a href="#" class="navbar-brand d-flex align-items-center">
                <strong>NIME 2021 - DMI Replicability - {id}</strong>
            </a>
            </div>
        </div>
        </header>

        <main>

        <section class="py-3 text-left container">
            <div class="row py-lg-5">
            <div class="col-lg-12 col-md-8 mx-auto">
                <h1 class="fw-light">{title}</h1>
                <h3 class="fw-light">{authors}</h3>
                <p class="py-2 lead text-muted">{abstract}</p>
                <p>
                <a href="{link}" class="btn btn-primary my-2">Go to the Review Form</a>
                </p>
            </div>
            </div>
        </section>

        </main>

        <footer class="text-muted py-5">
        <div class="container">
            <p class="float-end mb-1">
            <a href="#">Back to top</a>
            </p>
        </div>
        </footer>
            
        <script src="../assets/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
    '''
    return html_template


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
    file_name = pdf_file.replace(f'https://www.nime.org/proceedings/{year}/','').replace('.pdf','')
    file = open(f'{file_name}.txt', encoding='latin')
    line = file.read()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
    for url in urls:
        print(url)
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
            print('Recorte: ', text[_start,_end+100])
            url = match.group()
            print("[+] URL Found:", url)
            urls.append(url)
        print("[*] Total URLs extracted:", len(urls))
    print('==================================')

# file = open('merged-file.txt', encoding='latin')

# line = file.read().replace('\n', ' ')

# urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)



