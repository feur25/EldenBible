import requests
from bs4 import BeautifulSoup
import csv

url = "https://game8.co/games/Elden-Ring/archives/457048"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', class_='a-table a-table a-table table--fixed flexible-cell tablesorter')
if not table:
    raise ValueError("La table principale n'a pas été trouvée.")

data = []

rows = table.find_all('tr')
for row in rows:
    row_data = []

    centers = row.find_all('td', class_='center')
    for center in centers:
        a_link = center.find('a', class_='a-link')
        if a_link:
            link_text = a_link.get_text(strip=True)
            link_url = a_link.get('href')
            if link_url:
                link_response = requests.get(link_url)
                link_soup = BeautifulSoup(link_response.content, 'html.parser')

                first_table = link_soup.find('table', class_='a-table a-table a-table')
                if first_table:
                    first_td_text = first_table.find('td', class_='center').get_text(strip=True)

                    first_a_text = first_table.find('a', class_='a-link').get_text(strip=True)

                    first_b_text = first_table.find('b', class_='a-bold').find_next_sibling(text=True).strip().replace(": ", "") if first_table.find('b', class_='a-bold') else ''

                    second_table = link_soup.find_all('table', class_='a-table a-table a-table')[1]
                    if second_table:
                        second_center_texts = [td.get_text(strip=True) for td in second_table.find_all('td', class_='center')]

                        third_table = link_soup.find_all('table', class_='a-table a-table a-table')[2]
                        if third_table:
                            third_center_texts = [td.get_text(strip=True) for td in third_table.find_all('td', class_='center')]

                            fourth_table = link_soup.find_all('table', class_='a-table a-table a-table')[3]
                            if fourth_table:
                                fourth_center_texts = [td.get_text(strip=True) for td in fourth_table.find_all('td', class_='center')]

                                row_data.extend([first_a_text, first_b_text] + second_center_texts + third_center_texts + fourth_center_texts)

    data.append(row_data)

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['first_a_text', 'first_b_text'] + [f'second_center_{i}' for i in range(len(second_center_texts))] + [f'third_center_{i}' for i in range(len(third_center_texts))] + [f'fourth_center_{i}' for i in range(len(fourth_center_texts))]) 
    writer.writerows(data)

print("Les données ont été extraites et enregistrées dans 'output.csv'.")
