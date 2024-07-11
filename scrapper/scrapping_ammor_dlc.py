import requests
from bs4 import BeautifulSoup
import csv
import os

if 'csv' in os.listdir(os.path.dirname(__file__)):
    raise ImportError("Le fichier csv.py existe dans le répertoire et entre en conflit avec le module csv standard.")

url = "https://game8.co/games/Elden-Ring/archives/458621"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', class_='a-table a-table a-table table--fixed flexible-cell')
if not table:
    raise ValueError("La table principale n'a pas été trouvée.")

data = []

links = table.find_all('a', class_='a-link')
if not links:
    raise ValueError("Aucun élément avec la classe 'a-link' n'a été trouvé.")

for link in links:
    row = []
    link_text = link.get_text(strip=True)
    row.append(link_text)
    
    img = link.find('img')
    img_src = img.get('src', '') if img else ''
    row.append(img_src)

    link_url = link.get('href')
    print(link_url)
    if link_url:
        link_response = requests.get(link_url)
        print(link_response)
        link_soup = BeautifulSoup(link_response.content, 'html.parser')

        new_table = link_soup.find('table', class_='a-table a-table a-table table--fixed')
        if new_table:
            type_text = new_table.find('b', text='Type')
            if type_text:
                type_link = type_text.find_next_sibling('a', class_='a-link')
                if type_link:
                    type_value = type_link.get_text(strip=True)
                    row.append(type_value)

            weight_text = new_table.find('b', text='Weight')
            print(weight_text)
            if weight_text:
                weight_content = weight_text.next_sibling
                if weight_content and isinstance(weight_content, str):
                    weight_value = weight_content.strip().replace(": ", "")
                    row.append(weight_value)
                    print(weight_value)

            for td in new_table.find_all('td', class_='center'):
                td_text = td.get_text(strip=True)
                try:
                    num_value = float(td_text) if '.' in td_text else int(td_text)
                    row.append(num_value)
                except ValueError:
                    pass

    data.append(row)

print("Données collectées:")
for row in data:
    print(row)
    
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Les données ont été extraites et enregistrées dans 'output.csv'.")
