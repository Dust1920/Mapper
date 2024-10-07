"""
Mapper Aplication: Cobertura Educativa
"""
import matplotlib.pyplot as plt
import numpy as np
from Mapper import mapper as Mapper

ext_pd = Mapper.ext_pd


# Global Variables
intervals = [[0,19],[20,39],[40,59],[60,79],[80,99],[100,np.inf]]
color_codes = {
0: "white",
1: "#C7E1EF",
2: "#94C4DF",
3: "#4A98C9",
4: "#1764AB",
5: "#08306B"
}



# Sonora Map
sonora = Mapper.create_map(region = 'Sonora', map_type = "Municipios")


def set_interval_pos(value, **kwargs):
    """
    Connect Values in a Partition
    """
    global intervals
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

def map_output(mapa, mapa_name, **kwargs):
    """
    Create a Custom Map.
    """
    mapa.savefig(mapa_name)
    color = kwargs.get('colors', None)
    interval = kwargs.get('intervals', None)

    if color is not None and interval is not None:
        new_dict ={tuple(interval[k]): col for k, col in enumerate(color.values())}
        print(new_dict)


# Obtain Data
data = ext_pd.read_excel(r"data\Cobertura\Mapas Índice de Cobertura.xlsx", index_col = 0, dtype=str)
data_cols = ['Preescolar','Primaria','Secundaria']

for c in data_cols:
    data[c] = data[c].astype(float) * 100

sonorawdata = sonora.copy()


for c in data_cols:
    sonorawdata[c] = data[c]

# Legend Config
ley_educ = {"title": "Porcentaje"}

# Map 0: Preescolar
def plots():
    educ0, pres = plt.subplots(figsize = Mapper.FIGSIZE)
    sonorawdata.plot('Preescolar', scheme = "percentiles", cmap = "Blues", legend = True,
                    legend_kwds = ley_educ, ax = pres)
    sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = pres)
    for x in data.index:
        cve_mun = data.loc[x, 'CVE_MUN']
        pres.annotate(cve_mun[1:], sonorawdata.loc[x, 'geometry'].centroid.coords[0], fontsize = 8)
    pres.set_axis_off()
    pres.set_title("P1")

    # Map 1 : Primaria
    educ1, prim = plt.subplots(figsize = Mapper.FIGSIZE)
    sonorawdata.plot('Primaria', scheme = "percentiles", cmap = "Blues", legend = True,
                    legend_kwds = ley_educ, ax = prim)
    sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = prim)
    prim.set_title("P2")
    prim.set_axis_off()

    # Map 2: Secundaria
    educ2, secd = plt.subplots(figsize = Mapper.FIGSIZE)
    sonorawdata.plot('Secundaria', scheme = "percentiles", cmap = "Blues", legend = True,
                    legend_kwds = ley_educ, ax = secd)
    sonorawdata.boundary.plot(lw = 0.5, color = "black", ax = secd)
    secd.set_title("P3")
    secd.set_axis_off()

sonorawdata['Color_Pres'] = sonorawdata['Preescolar'].transform(set_interval_pos)
sonorawdata['Color_Prim'] = sonorawdata['Primaria'].transform(set_interval_pos)
sonorawdata['Color_Secd'] = sonorawdata['Secundaria'].transform(set_interval_pos)

def plot_maps():
    """
    Plot Maps
    """
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

def save_maps():
    """
    Save Maps
    """
    educ0.savefig('maps\\Preescolar.png')
    educ1.savefig('maps\\Primaria.png')
    educ2.savefig('maps\\Secundaria.png')

# map_output(educ0, 'maps\\Preescolar.png', colors = color_codes, intervals = intervals)
# map_output(educ1, 'maps\\Primaria.png', colors = color_codes, intervals = intervals)
# map_output(educ2, 'maps\\Secundaria.png', colors = color_codes, intervals = intervals)


data_ms = ext_pd.read_excel(r"data/Cobertura/Mapa Cobertura Media Superior.xlsx",
                            index_col = 0, dtype=str)

sonora_ms = sonora.copy()

for c in data_ms.columns:
    sonora_ms[c] = data_ms[c].astype(float).transform(lambda x: round(x, 4)) * 100

print(sonora_ms.columns)

sonora_ms['Color_Prep0'] = sonora_ms['Media Superior Escolarizada'].transform(set_interval_pos)
sonora_ms['Color_Prep1'] = sonora_ms['Media Superior Ambas'].transform(set_interval_pos)

educm0, ms0 = plt.subplots(figsize = Mapper.FIGSIZE)
sonora_ms.plot('Media Superior Escolarizada', color = sonora_ms['Color_Prep0'], ax = ms0)
sonora_ms.boundary.plot(lw = 0.5, color = "black", ax = ms0)
ms0.set_axis_off()
educm0.tight_layout()

educm1, ms1 = plt.subplots(figsize = Mapper.FIGSIZE)
sonora_ms.plot('Media Superior Ambas',color = sonora_ms['Color_Prep1'], ax = ms1)
sonora_ms.boundary.plot(lw = 0.5, color = "black", ax = ms1)
ms1.set_axis_off()
educm1.tight_layout()


educm0.savefig("maps\\MediaSuperiorEscolarizada.png")
educm1.savefig("maps\\MediaSuperior.png")
plt.show()
