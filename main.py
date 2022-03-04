from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections

if __name__ == '__main__':

    excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1',  na_values= None , keep_default_na=False).to_dict(orient='records')

    now = datetime.datetime.now()
    year_of_foundation = 1920
    year = now.year

    drinks = collections.defaultdict(list)

    for wine in excel_data_df:
        drinks[wine ['Категория']].append(wine)


    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        years=year-year_of_foundation,
        drinks=drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
