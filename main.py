from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1',  na_values= None , keep_default_na=False).to_dict(orient='records')

now = datetime.datetime.now()
year_of_foundation = 1920
year = now.year

d = collections.defaultdict(list)

for wine in excel_data_df:
    d[wine ['Категория']].append(wine)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
rendered_page = template.render(
    years=year-year_of_foundation,
    wines=d
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
