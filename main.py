# https://wkhtmltopdf.org/downloads.html
import jinja2
import pdfkit
import pandas as pd

TEMPLATE_FILE = "pdf_interest_report.html"
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(
    wkhtmltopdf=path_wkhtmltopdf
)
options = {
  "enable-local-file-access": None
}
def run():
    ### data ###
    interest_rates = [i * .01 for i in range(1, 11)]
    initial_account_sizes = [100, 500, 20000, 50000]
    data_frames = []
    for interest_rate in interest_rates:
        df = {}
        for initial_account_size in initial_account_sizes:
            df['Account Size: ' + str(initial_account_size)] = [initial_account_size * (1 + interest_rate) ** year for
                                                                year
                                                                in range(1, 21)]
        df = pd.DataFrame(df)
        df.index.name = 'year'
        data_frames.append({'df': df, 'interest_rate': interest_rate})

    ### html ###
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMPLATE_FILE)

    for d in data_frames:
        output_text = template.render(df=d['df'],
                                      interest_rate=d['interest_rate'])
        html_file = open('html/' + str(int(d['interest_rate'] * 100)) + '.html', 'w')
        html_file.write(output_text)
        html_file.close()

    ### pdf ###
    for i in range(1, 2):
        pdfkit.from_file(
            'html/' + str(i) + '.html',
            'pdf/' + str(i) + '.pdf',
            configuration=config,
            options=options
        )


if __name__ == '__main__':
    run()
