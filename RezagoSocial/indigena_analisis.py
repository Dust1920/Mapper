#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####

from Mapper import mapper as Mapper
import matplotlib.pyplot as plt
from Mapper import general_tools as gt
import pandas as pd
import os

data = pd.read_excel('RezagoSocial\\data\\Resultados.xlsx', index_col = 0,dtype=str)
data.index = [str(d) for d in data.index]
sonora = Mapper.create_map(region = 'Sonora', map_type = 'Municipios')
sonora_lpr = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Puntuales Rur')
sonora_l = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Urb y Rur Amnzs')

rsl = sonora_l[['geometry','CVE_MUN']]
rslpr = sonora_lpr[['geometry','CVE_MUN']]

rsl['CVE'] = sonora_l['CVE_ENT'] + sonora_l['CVE_MUN'] + sonora_l['CVE_LOC']
rslpr['CVE'] = sonora_lpr['CVE_ENT'] + sonora_lpr['CVE_MUN'] + sonora_lpr['CVE_LOC']

rsl.set_index('CVE', inplace = True)
rslpr.set_index('CVE', inplace = True)


map_data = data[['2000','2005','2010','2020']]
map_data = map_data.astype(float)

rslpr[['2000','2005','2010','2020']] = pd.NA
rsl[['2000','2005','2010','2020']] = pd.NA


i,j = 0,0
for mp in map_data.index:
    mpd = map_data.loc[mp].to_list()
    try:
        rsl.loc[mp,['2000','2005','2010','2020']] = mpd
    except:
        rsl.loc[mp,['2000','2005','2010','2020']] = pd.NA
        i+= 1
    try:
        rslpr.loc[mp, ['2000','2005','2010','2020']] = mpd
    except:
        rslpr.loc[mp, ['2000','2005','2010','2020']] = pd.NA
        j+= 1


map_check = rslpr.copy()
map_check = map_check.loc[map_data.index]
map_check = map_check[map_check['geometry']!= None]
map_out = map_check[map_check['geometry']== None]
map_2000 = map_check[~map_check['2000'].isna()]
map_2005 = map_check[~map_check['2005'].isna()]
map_2010 = map_check[~map_check['2010'].isna()]
map_2020 = map_check[~map_check['2020'].isna()]
map_2000['2000'] = map_2000['2000'].astype(float)
map_2005['2005'] = map_2005['2005'].astype(float)
map_2010['2010'] = map_2010['2010'].astype(float)
map_2020['2020'] = map_2020['2020'].astype(float)


if not os.path.exists('RezagoSocial\\IndiceSonora2000'):
    os.mkdir('RezagoSocial\\IndiceSonora2000')
map_2000.to_file('RezagoSocial\\IndiceSonora2000\\SonoraIndice2000.shp')

if not os.path.exists('RezagoSocial\\IndiceSonora2005'):
    os.mkdir('RezagoSocial\\IndiceSonora2005')
map_2005.to_file('RezagoSocial\\IndiceSonora2005\\SonoraIndice2005.shp')

if not os.path.exists('RezagoSocial\\IndiceSonora2020'):
    os.mkdir('RezagoSocial\\IndiceSonora2020')
map_2020.to_file('RezagoSocial\\IndiceSonora2020\\SonoraIndice2020.shp')

if not os.path.exists('RezagoSocial\\IndiceSonora2010'):
    os.mkdir('RezagoSocial\\IndiceSonora2010')
map_2010.to_file('RezagoSocial\\IndiceSonora2010\\SonoraIndice2010.shp')
 

map_check = map_check[map_check['geometry']!= None]
map_check = map_check.loc[map_data.index]

# Error de Cobertura (Localidades y Población)
# Mapa Distribución de datos 2020
## Gráfico de Completitud de Datos (4,3,2,1)
## Gráfico de Cobertura Municipal
## Localidades Fantasma


for y in ['2000','2005','2010','2020']:
    for md in rslpr.index:
        if pd.isna(rslpr.loc[md,y]):
            map_check.loc[md,y] = 0
        else:
            map_check.loc[md,y] = 1

print(map_check)
x1 = map_check['2000'].sum() / len(map_check)
x2 = map_check['2005'].sum() / len(map_check)
x3 = map_check['2010'].sum() / len(map_check)
x4 = map_check['2020'].sum() / len(map_check)

print(x1,x2,x3,x4)