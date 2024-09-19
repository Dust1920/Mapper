#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####


## Mapper y librerias 
from Mapper import mapper as Mapper
import pandas as pd
import matplotlib.pyplot as plt
import os


## Creando mapas
sonora = Mapper.create_map(region = 'Sonora', map_type = 'Municipios')

data = pd.read_excel(r"Participación\data\Participacion.xlsx", index_col = 0)

map_data = data[['¿Participó?','Grupo.1']]

sonora_data = sonora.copy()

sonora_data[['Participacion','Tipo Municipio']] = map_data


part, ax = plt.subplots(figsize = (20,20))
sonora_data.plot('Participacion', color = data['Color'], ax = ax)
sonora_data.boundary.plot(color = "black", lw = 0.5, ax = ax)
ax.set_axis_off()
plt.show()

for ent in sonora_data.index:
    partg = sonora_data.loc[ent,'Participacion']
    if partg:
        sonora_data.loc[ent, 'ColorYes'] = data.loc[ent, 'Color.1']
        sonora_data.loc[ent, 'ColorNo'] = 'white' 
    else:
        sonora_data.loc[ent, 'ColorNo'] = data.loc[ent, 'Color.1']
        sonora_data.loc[ent, 'ColorYes'] = 'white'

part1, ax = plt.subplots(figsize = (20,20))
sonora_data.plot('Tipo Municipio', color = sonora_data['ColorYes'], ax = ax)
sonora_data.boundary.plot(color = "black", lw = 0.5, ax = ax)
ax.set_axis_off()
plt.show()

part0, ax = plt.subplots(figsize = (20,20))
sonora_data.plot('Tipo Municipio', color = sonora_data['ColorNo'], ax = ax)
sonora_data.boundary.plot(color = "black", lw = 0.5, ax = ax)
ax.set_axis_off()
plt.show()

part.savefig('Participación\\maps\\Participacion.png')
part0.savefig('Participación\\maps\\ParticipacionPos.png')
part1.savefig('Participación\\maps\\ParticipacionNeg.png')