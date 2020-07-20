from pykml import parser
import pandas as pd

kml_file = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_feature/MuslimFoodies_Halal_Map_NYC.kml'

with open(kml_file) as f:
    doc = parser.parse(f).getroot()



df = pd.DataFrame(columns=['name', 'coordinates', 'category', 'url'])

# verified halal listings
start_rows = df.shape[0]
for e in doc.Document.Folder.Placemark:
    row = {'name' : e.name.text,
            'coordinates' : ','.join(e.Point.coordinates.text.split()[0].split(',')[:2]), # remove whitespaces and trailing ",0"
            'category' : 'MFoodies',
            'url' : None}
    df = df.append(row, ignore_index=True)
print('found {} restaurants in MFoodies list'.format(df.shape[0]-start_rows))

# partially halal listings
start_rows = df.shape[0]
for e in doc.Document.Folder[1].Placemark:
    row = {'name' : e.name.text,
            'coordinates' : ','.join(e.Point.coordinates.text.split()[0].split(',')[:2]), # remove whitespaces and trailing ",0"
            'category' : 'MFoodies_partial',
            'url' : None}
    df = df.append(row, ignore_index=True)
print('found {} restaurants in MFoodies partial list'.format(df.shape[0]-start_rows))

df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_feature/muslim_foodies_list.csv', index=False)
