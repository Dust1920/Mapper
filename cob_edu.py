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


ley_educ = {"title": "Porcentaje"}


educ0, pres = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Preescolar', scheme = "percentiles", cmap = "Blues", legend = True, legend_kwds = ley_educ, ax = pres)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = pres)
for x in data.index:
    cve_mun = data.loc[x, 'CVE_MUN']
    pres.annotate(cve_mun[1:], sonorawdata.loc[x, 'geometry'].centroid.coords[0], fontsize = 8)
pres.set_axis_off()
pres.set_title("P1")


educ1, prim = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Primaria', scheme = "percentiles", cmap = "Blues", legend = True,  legend_kwds = ley_educ, ax = prim)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = prim)
prim.set_title("P2")
prim.set_axis_off()


educ2, secd = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Secundaria', scheme = "percentiles", cmap = "Blues", legend = True,  legend_kwds = ley_educ, ax = secd)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = secd)
secd.set_title("P3")
secd.set_axis_off()



def set_interval_pos(value, **kwargs):
    global color_codes 
    global intervals

    intervals = [[0,19],[20,39],[40,59],[60,79],[80,99],[100,np.inf]]
    color_codes = {
    0: "white",
    1: "#C7E1EF",
    2: "#94C4DF",
    3: "#4A98C9",
    4: "#1764AB",
    5: "#08306B"
    }
    intervals = kwargs.get('interval', intervals)
    cc = kwargs.get("code_color", color_codes)
    i_min = intervals[0][0]
    i_max = intervals[-1][1]
    if value < i_min:
        return -1
    if i_max != np.inf:
        if value > i_max:
            return -1
    k = 0
    while value>intervals[k][1]:
        k = k + 1
        if i_max == np.inf and k>len(intervals):
            k = len(intervals) - 1
            break
    return cc[k]
    

sonorawdata['Color_Pres'] = sonorawdata['Preescolar'].transform(set_interval_pos)
sonorawdata['Color_Prim'] = sonorawdata['Primaria'].transform(set_interval_pos)
sonorawdata['Color_Secd'] = sonorawdata['Secundaria'].transform(set_interval_pos)


educ0, pres = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Preescolar',color = sonorawdata['Color_Pres'], ax = pres)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = pres)
pres.set_axis_off()
educ0.tight_layout()

educ1, prim = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Primaria',color = sonorawdata['Color_Prim'], ax = prim)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = prim)
educ1.tight_layout()
prim.set_axis_off()

educ2, secd = plt.subplots(figsize = Mapper.FIGSIZE)
sonorawdata.plot('Secundaria',color = sonorawdata['Color_Secd'], ax = secd)
sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = secd)
secd.set_axis_off()
educ2.tight_layout()

plt.show()


educ0.savefig('maps\\Preescolar.png')
educ1.savefig('maps\\Primaria.png')
educ2.savefig('maps\\Secundaria.png')


def map_output(mapa, mapa_name, **kwargs):
    mapa.savefig(mapa_name)
    colors = kwargs.get('colors', None)
    intervals = kwargs.get('intervals', None)
    if colors != None and intervals != None:
        new_dict ={tuple(intervals[k]): col for k, col in enumerate(colors.values())}
        print(new_dict)


map_output(educ0, 'maps\\Preescolar.png', colors = color_codes, intervals = intervals)







"""
for x in data.index:
    cve_mun = data.loc[x, 'CVE_MUN']
    pres.annotate(cve_mun[1:], sonorawdata.loc[x, 'geometry'].centroid.coords[0], fontsize = 8)
"""