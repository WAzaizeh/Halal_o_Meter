import requests, re
import pandas as pd
from bs4 import BeautifulSoup

cities = {'Manhattan' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Manhattan/NEwhtS6OzN',
        'Brooklyn' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Brooklyn/3avrh3Cth4',
        'Queens' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Queens/9Gku594eh7',
        'The Bronx' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/The-Bronx/eIqsntUUuI',
        'Staten Island' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Staten-Island/84zPaAaBZd',
        'North Jersey' : 'https://www.zabihah.com/sub/United-States/New-Jersey/North-Jersey/E2mHNVQ3ta',
        'San Francisco' : 'https://www.zabihah.com/sub/United-States/California/SF-Bay-Area/San-Francisco/OB9InUnes0',
        'Berkley & Oakland' 'https://www.zabihah.com/sub/United-States/California/SF-Bay-Area/Berkeley-amp-Oakland/vmCKU6sHEm',
        'Long Island' : 'https://www.zabihah.com/sub/United-States/New-York/Long-Island/H89S4GDa2Y',
        'Los Angeles Inland Empire' : 'https://www.zabihah.com/sub/United-States/California/Los-Angeles/Inland-Empire/gSl0Smz6EY',
        'Los Angeles Orange County' : 'https://www.zabihah.com/sub/United-States/California/Los-Angeles/Orange-County/AuvKfMSq2N'}

df = pd.DataFrame(columns=['name', 'coordinates', 'borough', 'url'])

for city in cities:
    html_text = requests.get(cities[city]).text
    soup = BeautifulSoup(html_text, 'html.parser')
    tracks = soup.find_all('script')
    map_data = tracks[17]
    start_rows = df.shape[0]
    for line in map_data.string.split('\n'):
        if 'coordinate' in line and 'title' in line:
            coord = re.search(r'(?<=Coordinate\()(.*)(?=\), )', line).group(0)
            coord = coord.replace(' ', '')
            title = re.search(r'(?<=title: \")(.*)(?=\", )', line).group(0)
            url = re.search(r'(?<=url: \")(.*)(?=\" })', line).group(0)
            row = {'name' : title,
                    'coordinates' : coord,
                    'category' : 'zabiha.com',
                    'url' : 'https://www.zabihah.com' + url}
    df = df.append(row, ignore_index=True)
    print('found {0} restaurants in {1}'.format(df.shape[0]-start_rows, city))
df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_feature/zabiha_list.csv', index=False)
