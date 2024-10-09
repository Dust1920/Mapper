"""
Georeference Summary of the gender form created by ISAF
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Levenshtein as lev
from Mapper import mapper as Mapper

# Auxiliar Functions

def lev_search(word, listwords):
    """
    Given a word list and a word, get the best word in the list using the lev distance.
    """
    if word in {np.nan, pd.NA}:
        return pd.NA
    dv = np.array([lev.distance(word, str(lw)) for lw in listwords])
    dmin = dv.min()
    best = np.where(dv == dmin)[0]
    return str(listwords[best[0]])

def form_to_maps_muns(data_mun):
    """
    Convert muns in data in muns for maps.
    """
    modif_muns = pd.DataFrame(index = data_mun, columns = ['InterMuns', 'Municipio Mapa'])
    modif_muns['InterMuns'] = list(modif_muns.index)
    modif_muns['InterMuns'] = modif_muns['InterMuns'].transform(
        lambda x: str(x).split(",",maxsplit= 1)[0])
    modif_muns['InterMuns'] = modif_muns['InterMuns'].str.replace("sonora", "")
    modif_muns['InterMuns'] = modif_muns['InterMuns'].str.replace("municipio de ", "")
    modif_muns['InterMuns'] = modif_muns['InterMuns'].str.rstrip(" ")
    modif_muns['InterMuns'] = modif_muns['InterMuns'].str.lstrip(" ")
    modif_muns['Municipio Mapa'] = modif_muns['InterMuns'].transform(
        lambda x: lev_search(x, form_muns))
    return modif_muns






# Sonora Map
sonora = Mapper.create_map(region = "Sonora", map_type = "Municipios")
sonora_form = sonora.copy()


# Get data
form = pd.read_excel("data\\Formularios\\Resumen Formularios.xlsx", sheet_name=None)
form_sheets = list(form.keys())
# print(form_sheets)


# Transform Data
catalogs = form['Catalogos']
form_muns = catalogs['Mapa Municipio']

# Question 6
responsible = form["6"]
resp_muns = responsible[6]
# Muns to Muns reference
ref_muns = form_to_maps_muns(resp_muns)
pre_index = [ref_muns.loc[x, 'Municipio Mapa'] for x in list(resp_muns)]
ref_index = []
for x in pre_index:
    if isinstance(x, str):
        ref_index.append(x)
    else:
        ref_index.append(x.iloc[0])
responsible['Municipio Mapa'] = ref_index
print(responsible)


# Creation Maps
PLOT_MAPS = 0
if PLOT_MAPS:
    ###
    # Municipios participantes
    sonora_form['Encuestado'] = "No"
    for mun in form_muns:
        if mun in sonora_form.index:
            sonora_form.loc[mun, 'Encuestado'] = "Si"
    resp, ax = plt.subplots(figsize = Mapper.FIGSIZE)
    sonora_form.plot('Encuestado', categorical = True,
                    legend = True, legend_kwds = {"title":"¿Respondió?"},
                    ax = ax)
    resp.suptitle('Encuestados en Genero')
    resp.tight_layout()
    ax.set_axis_off()
    plt.show()
    ###

    ###
    # Instituciones Responsables



    ###

