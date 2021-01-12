import re
import bibtexparser
import fitz

nime_files = ["nime2018.bib","nime2019.bib","nime2020.bib"]
url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

def add_variables(id, quant_pages, title, authors, abstract, link, urls, urls_debug):
    title_for_form = title.replace(' ','+')
    
    urls_html = '<ul>\n'
    for url in urls:
          urls_html += f'                    <li><a href=\"{url}\" target="_blank">{url}</a></li>\n'
    urls_html += '                </ul>'

    urls_html_debug = '<ul class=\"font-monospace collapse\" id=\"debug">\n'
    for url_d in urls_debug:
          urls_html_debug += f'                    <li><small>{url_d}</small></li>\n'
    urls_html_debug += '                </ul>'

    html_template = f'''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="description" content="">
            <meta name="author" content="Filipe Calegario, Mark Otto, Jacob Thornton, and Bootstrap contributors">
            <meta name="generator" content="Hugo 0.79.0">
            <title>Review Page</title>

            <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/album/">
            
            

            <!-- Bootstrap core CSS -->
        <link href="assets/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="assets/dist/js/bootstrap.bundle.min.js"></script>
            
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
                <h2 class="fw-light">{title}</h2>
                <h5 class="fw-light text-muted">{authors}</h5>
                <h6 class="fw-light text-muted">Length: {quant_pages} pages</h6>
                <h4 class="py-2 fw-light">Abstract</h4>
                <p class="text-muted">{abstract}</p>
                <h4 class="fw-light">Extracted URLs from PDF</h4>
                {urls_html}
                <a class="btn btn-primary" data-toggle="collapse" href="#debug" role="button" aria-expanded="false" aria-controls="debug">
                    Debug: if a extracted URL is malformed
                </a>
                {urls_html_debug}
                <p>
                <a href="{link}" target="_blank" class="btn btn-primary my-2">Original PDF</a>             
                </p>
            </div>
            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfbMV3dHjR6jDpctF5ogz3T9A5ncgJjMLVGx4cgOY3jITLZEg/viewform?embedded=true&usp=pp_url&entry.1767549064={id}&entry.54369149={title_for_form}" width="700" height="600" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
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
        
        </body>
        </html>
    '''
    return html_template

def process_bib_file_to_html(nime_file):
    print(f"Going to load: {nime_file}, hope that's ok.")

    with open(nime_file) as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
        
    print(f"Loaded {len(bib_database.entries)} entries.")
    review_sheet = []
    for e in bib_database.entries:
        print('.',end='')
        title = e['title']
        authors = e['author']
        pdf_file_url = e['url']
        year = e['year']
        abstract = e['abstract']
        local_pdf_file = pdf_file_url.replace('https','http').replace(f'http://www.nime.org/proceedings/{year}/','')
        id = local_pdf_file.replace('.pdf','')
        urls = []
        urls_debug = []
        quant_pages = ''
        with fitz.open(f'pdf_files/{year}/{local_pdf_file}') as pdf:
            text = ""
            quant_pages += str(len(pdf))
            for page in pdf:
                # extract text of each PDF page
                text += page.getText()
        # extract all urls using the regular expression
            for match in re.finditer(url_regex, text):
                url = match.group()
                _start = match.start()
                _end = match.end()
                url_d = text[_start:_end+100].replace('\n','')
                #print("[+] URL Found:", url)
                urls.append(url)
                urls_debug.append(url_d)
        output = add_variables(id, quant_pages, title, authors, abstract, pdf_file_url, urls, urls_debug)
        review_sheet.append(format_review_info(id,title,year))
        f = open(f"exported_html/{id}.html", "w")
        f.write(output)
        f.close()

    print('')    
    print('Exporting CSVs')
    sheet = open('csv_review_sheet/review_sheet.csv', 'a')
    print("Review Sheet:", len(review_sheet))
    for line in review_sheet:
        sheet.write(line + '\n')
    sheet.close()

def format_review_info(_id, _title,_year):
    return f"No,http://www.cin.ufpe.br/~fcac/NIME2021/DMI_Repl/{_id}.html,{_year},\"{_title}\""

def debug_template():
    id = 'id9999'
    title = 'AM MODE: Using AM and FM Synthesis for Acoustic Drum Set Augmentation'
    author = 'Cory Champion and Mo H Zareei'
    abstract = 'Many common and popular sound spatialisation techniques and methods rely on listeners being positioned in a "sweet-spot" for an optimal listening position in a circle of speakers. This paper discusses a stochastic spatialisation method and its first iteration as implemented for the exhibition Hot Pocket at The Museum of Contemporary Art in Oslo in 2017. This method is implemented in Max and offers a matrix-based amplitude panning methodology which can provide a flexible means for the spatialialisation of sounds.'
    link = 'http://www.nime.org/proceedings/2018/nime2018_paper0007.pdf'
    output = add_variables(id, title, author, abstract, link, ['url1','url2'],['url1d','url2d'])
    f = open(f"exported_html/debug_{id}.html", "w")
    f.write(output)
    f.close()

for nime in nime_files:
    process_bib_file_to_html(f'bib_files/{nime}')

# debug_template()