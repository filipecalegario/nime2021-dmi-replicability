fh = open('code/exploration/step_3_link_output.txt')
output = open(f'code/exploration/step_3_link_original_pdf.txt', 'w')
for line in fh:
    parts = line.replace('\n','').split('\t')
    paper_id = parts[0]
    paper_year = parts[1]
    gf_link = f'=HYPERLINK(\"https://www.nime.org/proceedings/{paper_year}/{paper_id}.pdf\",\"original PDF\")\n'
    output.write(gf_link)
    print(gf_link)
fh.close()
output.close()