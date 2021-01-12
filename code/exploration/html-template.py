def add_variables(id, title, authors, abstract, link, urls):
    title_for_form = title.replace(' ','+')
    
    urls_html = '<ul>'
    for url in urls:
          urls_html += f'<li><a href=\"{url}\" target="_blank">{url}</a></li>'
    urls_html += '</ul>'

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
                <h5 class="fw-light text-muted">{authors}</h5>
                <h4 class="py-2 fw-light">Abstract</h4>
                <p class="lead text-muted">{abstract}</p>
                <h4 class="fw-light">Extracted Links from PDF</h4>
                {urls_html}
                <p>
                <a href="{link}" target="_blank" class="btn btn-primary my-2">Original PDF</a>             
                </p>
            </div>
            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfbMV3dHjR6jDpctF5ogz3T9A5ncgJjMLVGx4cgOY3jITLZEg/viewform?embedded=true&usp=pp_url&entry.1767549064={id}&entry.54369149={title_for_form}" width="640" height="600" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
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

id = 'nime20_paper104'
urls='<p>link1</p><p>link2</p><p>link3</p><p>link4</p>'
output = add_variables(id, 'This is it', 'Filipe Calegario', 'The fabulous abstract that I created here', 'http://www.cin.ufpe.br',['http://www.cin.ufpe.br','http://www.cin.ufpe.br/~fcac'])
f = open(f"exported_html/{id}.html", "w")
f.write(output)
f.close()