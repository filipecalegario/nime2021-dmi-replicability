fh = open('code/exploration/step_3.txt')
output = open(f'code/exploration/step_3_output.txt', 'w')
for line in fh:
    parts = line.replace('\n','').split('\t')
    paper_id = parts[0]
    paper_title = parts[1].replace(' ','+')
    gf_link = f'=HYPERLINK(\"https://docs.google.com/forms/d/e/1FAIpQLSfH2cig2VCYzj3qlnQwJc87L-SWkco2A1KJQ4wu_7PWEVAsWQ/viewform?usp=pp_url&entry.282779438={paper_id}&entry.1720267214={paper_title}\",\"review form\")\n'
    output.write(gf_link)
    print(gf_link)
fh.close()
output.close()