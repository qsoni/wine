import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from dotenv import load_dotenv

def main():
    load_dotenv()
    production_file_path = os.getenv('PATH_TO_FILE')
    drinks = pandas.read_excel(production_file_path, sheet_name='Лист1', na_values= None, keep_default_na=False).to_dict(orient='records')

    current_year = datetime.datetime.now().year
    foundation_year = 1920
    structured_drinks = collections.defaultdict(list)

    for wine in drinks:
        structured_drinks[wine ['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        years_since_the_foundation=current_year-foundation_year,
        drinks=structured_drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()