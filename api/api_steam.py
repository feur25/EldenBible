import os
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup

os.makedirs('data', exist_ok=True)

def json_extract(obj, key):
    """Extraction récursive des valeurs depuis un JSON imbriqué."""
    arr = []
    def extract(obj, arr, key):
        """Recherche récursive des valeurs de key dans l'arbre JSON."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

game_id = '1245620'
responses = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}&format=json")
df_name = json_extract(responses.json(), 'name')
df_percent = json_extract(responses.json(), 'percent')
test = np.column_stack((df_name, df_percent))
df_achievements = pd.DataFrame(test, columns=['ID', 'Percent'])

df_achievements.to_csv('./data/steam_api_data.csv', index=False)

achievement_names = df_name
achievement_percents = df_percent

ad = []
url = 'https://steamdb.info/app/1245620/stats/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

for row in achievement_names:
    sanitized_name = row.replace(' ', '%20').replace("'", "%27")
    achievement_url = f'https://steamdb.info/stats/{game_id}/achievements/?ach={sanitized_name}'

    reqs = requests.get(achievement_url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    achievement_row = soup.find('tr', id=f'achievement-{row}')
    if achievement_row:
        description = achievement_row.find_all('td')[1].text.strip()
        ad.append([row, description])
    else:
        ad.append([row, 'Description non trouvée'])

ads = pd.DataFrame(ad, columns=['Boss', 'Description'])

final_achievements = pd.merge(ads, df_achievements, left_on='Boss', right_on='ID', how='left')
final_achievements = final_achievements[['Boss', 'ID', 'Description', 'Percent']]

final_achievements.to_csv('./data/achievement_descriptions.csv', index=False)

url = 'https://eldenring.wiki.fextralife.com/Bosses'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

titles = []
urls = []

links = soup.find_all('a', class_='wiki_link')
for link in links:
    Title = link.get('title')
    HRef = link.get('href')
    titles.append(Title)
    urls.append(HRef)

test = np.column_stack((titles, urls))
df_boss_urls = pd.DataFrame(test, columns=['Title', 'URL'])

df_boss_urls.to_csv('./data/boss_urls.csv', index=False)

print("Les données ont été collectées et sauvegardées avec succès.")
