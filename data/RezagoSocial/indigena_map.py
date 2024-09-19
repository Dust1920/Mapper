#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####

from Mapper import mapper as Mapper
import matplotlib.pyplot as plt
from Mapper import general_tools as gt
import pandas as pd

data = pd.read_excel('RezagoSocial\\data\\Resultados.xlsx', index_col = 0,dtype=str)
data.index = [str(d) for d in data.index]
sonora = Mapper.create_map(region = 'Sonora', map_type = 'Municipios')
sonora_lpr = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Puntuales Rur')
sonora_l = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Urb y Rur Amnzs')
print(sonora_lpr.shape)
print(sonora_l.shape)
rsl = sonora_l[['geometry','CVE_MUN']]
rslpr = sonora_lpr[['geometry','CVE_MUN']]

rsl['CVE'] = sonora_l['CVE_ENT'] + sonora_l['CVE_MUN'] + sonora_l['CVE_LOC']
rslpr['CVE'] = sonora_lpr['CVE_ENT'] + sonora_lpr['CVE_MUN'] + sonora_lpr['CVE_LOC']

rsl.set_index('CVE', inplace = True)
rslpr.set_index('CVE', inplace = True)


map_data = data[['2000','2005','2010','2020']]
map_data = map_data.astype(float)
print(map_data)

rslpr[['2000','2005','2010','2020']] = pd.NA
rsl[['2000','2005','2010','2020']] = pd.NA

print(rslpr)
print(rsl)

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
mapa, ax = plt.subplots(2,2, figsize = (20,15))
rslpr.plot('2000', scheme = 'percentiles', legend = True, ax = ax[0,0])
rslpr.plot('2005', scheme = 'percentiles', legend = True, ax = ax[0,1])
rslpr.plot('2010', scheme = 'percentiles', legend = True, ax = ax[1,0])
rslpr.plot('2020', scheme = 'percentiles', legend = True, ax = ax[1,1])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[0,0])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[0,1])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[1,0])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[1,1])
ax[0,0].set_axis_off()
ax[0,1].set_axis_off()
ax[1,0].set_axis_off()
ax[1,1].set_axis_off()
mapa.tight_layout()
mapa.savefig('MapaIndice.png')
plt.show()


map_check = rslpr.copy()

for y in ['2000','2005','2010','2020']:
    for md in rslpr.index:
        if pd.isna(rslpr.loc[md,y]):
            map_check.loc[md,y] = 0
        else:
            map_check.loc[md,y] = 1

print(map_check)

map_check = map_check.loc[map_data.index]

mapa2, ax = plt.subplots(2,2, figsize = (20,15))
map_check.plot('2000', legend = True, ax = ax[0,0])
map_check.plot('2005', legend = True, ax = ax[0,1])
map_check.plot('2010', legend = True, ax = ax[1,0])
map_check.plot('2020', legend = True, ax = ax[1,1])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[0,0])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[0,1])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[1,0])
sonora.boundary.plot(lw = 0.5, color = "black", ax = ax[1,1])
ax[0,0].set_axis_off()
ax[0,1].set_axis_off()
ax[1,0].set_axis_off()
ax[1,1].set_axis_off()
mapa2.tight_layout()
mapa2.savefig('Distribución.png')
plt.show()