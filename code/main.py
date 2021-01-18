import re
import bibtexparser
import fitz
from os import path
from glob import glob

nime_files = ["bib_files/nime2018.bib","bib_files/nime2019.bib","bib_files/nime2020.bib"]
#nime_files = []
#nime_files = ["bib_files/nime_papers.bib"]
pdf_files_folder_path = "pdf_files"
#pdf_files_folder_path = "/Volumes/SDDMTL/NIME Proceedings/pdf_files"
url_regex = r"(https?:\/\/)(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

def add_variables(id, quant_pages, title, authors, abstract, link, urls, urls_debug):
    
    google_forms_prefilled_link = format_google_forms_prefilled_link(id, title)
    
    urls_html = ""
    urls_html_debug = ""

    if len(urls) > 0:
        urls_html = '<ul>\n'
        for url in urls:
            urls_html += f'                    <li><a href=\"{url}\" target="_blank">{url}</a></li>\n'
        urls_html += '                </ul>'

        urls_html_debug = '''
        <div class="alert alert-warning" role="alert">
                <a class="alert-link" data-toggle="collapse" href="#debug" aria-expanded="false" aria-controls="debug">
                    Debug: if a extracted URL is malformed
                </a>
                        <ul class=\"font-monospace collapse\" id=\"debug">\n
        '''
        for url_d in urls_debug:
            urls_html_debug += f'                    <li><small>{url_d}</small></li>\n'
        urls_html_debug += '''
                        </ul>
        </div>
        '''
    else:
        urls_html = '''
                <div class="alert alert-danger" role="alert">
                    No URL found in the paper.
                </div>
        '''

    

    html_template = f'''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="description" content="">
            <meta name="author" content="Filipe Calegario, Mark Otto, Jacob Thornton, and Bootstrap contributors">
            <meta name="generator" content="Hugo 0.79.0">
            <title>{id} - {title}</title>

            <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/album/">

            <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

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
           
                {urls_html_debug}
                <p>
                <p>
                <a href="{link}" target="_blank" class="btn btn-primary my-2">Original PDF</a>             
                </p>
            </div>
            <iframe src="{google_forms_prefilled_link}" width="700" height="600" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
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

def format_google_forms_prefilled_link(_id, _title):
    title_for_form = _title.replace(' ','+')
    # Google Form - Long Version:
    #return f'https://docs.google.com/forms/d/e/1FAIpQLSfbMV3dHjR6jDpctF5ogz3T9A5ncgJjMLVGx4cgOY3jITLZEg/viewform?embedded=true&usp=pp_url&entry.1767549064={_id}&entry.54369149={_title}"'
    # Google Form - Short Version:
    return f'https://docs.google.com/forms/d/e/1FAIpQLSeeNTTMW8wbwNWr8AYITCU_78yFpR5Uyn0YRZG9iOcisxUCzw/viewform?embedded=true&usp=pp_url&entry.702570504={_id}&entry.1715562253={title_for_form}'

def process_bib_file_to_html(nime_bib_file, pdf_files_folder_path):
    print(f"Going to load: {nime_bib_file}, hope that's ok.")

    with open(nime_bib_file) as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
        
    print(f"Loaded {len(bib_database.entries)} entries.")
    review_sheet = []
    url_joint_sheet = []
    for e in bib_database.entries:
        try:
            title = e['title']
            authors = e['author']
            pdf_file_url = e['url']
            year = e['year']
            local_pdf_file = pdf_file_url.replace('https','http').replace(f'http://www.nime.org/proceedings/{year}/','')
            id = local_pdf_file.replace('.pdf','')
            abstract = ''
            if 'abstract' in e:
                abstract = e['abstract']
            else:
                print(f'!ERROR: {id} NIME {year}\'s paper: \"{title}\" has no abstract')
            urls = []
            urls_debug = []
            quant_pages = ''
            with fitz.open(f'{pdf_files_folder_path}/{year}/{local_pdf_file}') as pdf:
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
                    url_d_clean = url_d.replace('\"','\'').replace('\n', ' ').replace('\t', ' ')
                    title_clean = title.replace('\"','\'').replace('\n', ' ').replace('\t', ' ')
                    url_joint_sheet.append(','.join([id,url.replace('\n',''),f'\"{url_d_clean}\"',f'\"{title_clean}\"']))
            output = add_variables(id, quant_pages, title, authors, abstract, pdf_file_url, urls, urls_debug)
            review_sheet.append(format_review_info(id,title,year,abstract))
            f = open(f"exported_html/{id}.html", "w")
            f.write(output)
            f.close()
        except:
            print(f'Error: in {nime_bib_file}')
    print('')
    export_list_to_csv(review_sheet, 'review_sheet')
    export_list_to_csv(url_joint_sheet, 'url_joint_sheet')

def export_list_to_csv(list, title):
    print('Exporting CSVs')
    sheet = open(f'exported_csv/{title}.csv', 'a')
    for line in list:
        sheet.write(line + '\n')
    sheet.close()

def format_review_info(_id, _title,_year, _abstract):
    form_link = format_google_forms_prefilled_link(_id,_title).replace('embedded=true&','')
    processed_abstract = _abstract.replace('\"','\'').replace('\n', ' ')
    #return f"No,http://www.cin.ufpe.br/~fcac/NIME2021/DMI_Repl/{_id}.html,{_year},{form_link},\"{_title}\",\"{_abstract}\""
    return f"{_id},{_year},\"{_title}\",\"{processed_abstract}\""

def debug_template():
    id = 'id9999'
    title = 'AM MODE: Using AM and FM Synthesis for Acoustic Drum Set Augmentation'
    author = 'Cory Champion and Mo H Zareei'
    abstract = 'Many common and popular sound spatialisation techniques and methods rely on listeners being positioned in a "sweet-spot" for an optimal listening position in a circle of speakers. This paper discusses a stochastic spatialisation method and its first iteration as implemented for the exhibition Hot Pocket at The Museum of Contemporary Art in Oslo in 2017. This method is implemented in Max and offers a matrix-based amplitude panning methodology which can provide a flexible means for the spatialialisation of sounds.'
    link = 'http://www.nime.org/proceedings/2018/nime2018_paper0007.pdf'
    #output = add_variables(id, 6, title, author, abstract, link, [],['url1d','url2d'])
    output = add_variables(id, 6, title, author, abstract, link, ['url1','url2'],['url1d','url2d'])
    f = open(f"exported_html/debug_{id}.html", "w")
    f.write(output)
    f.close()

def find_ext(dir, ext):
    return glob(path.join(dir,"*.{}".format(ext)))

bib_files_to_process = []

if len(nime_files) > 0:
    bib_files_to_process = nime_files
else:
    bib_files_to_process = sorted(find_ext('bib_files', 'bib'),reverse=True)
    print(bib_files_to_process)

for bib in bib_files_to_process:
    #process_bib_file_to_html(f'bib_files/{bib}',pdf_files_folder_path)
    process_bib_file_to_html(bib,pdf_files_folder_path)

#debug_template()