#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####

from Mapper import mapper as Mapper
import matplotlib.pyplot as plt
from Mapper import general_tools as gt
import numpy as np

ext_pd = Mapper.ext_pd


# Obtain Data
data = ext_pd.read_excel(r"data\Cobertura\Mapas Índice de Cobertura.xlsx", index_col = 0, dtype=str)
data_cols = ['Preescolar','Primaria','Secundaria']

for c in data_cols:
    data[c] = data[c].astype(float) * 100

# Sonora Map

sonora = Mapper.create_map(region = 'Sonora', map_type = "Municipios")

sonorawdata = sonora.copy()

for c in data_cols:
    sonorawdata[c] = data[c]

educ0, press = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Preescolar', scheme = "percentiles", cmap = "Blues", legend = True, ax = press)
press.set_axis_off()

educ1, prim = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Primaria', scheme = "percentiles", cmap = "Blues", legend = True, ax = prim)
prim.set_axis_off()

educ2, secd = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Secundaria', scheme = "percentiles", cmap = "Blues", legend = True, ax = secd)
secd.set_axis_off()

plt.show()