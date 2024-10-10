"""
Georeference Summary of the gender form created by ISAF
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Levenshtein as lev
from matplotlib.colors import ListedColormap
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


# Municipios participantes
sonora_form['Encuestado'] = "No"
for mun in form_muns:
    if mun in sonora_form.index:
        sonora_form.loc[mun, 'Encuestado'] = "Si"


# Question 6 P1
responsible = form["6"]
resp_muns = responsible[6]
responsible.set_index(6, inplace=True, drop=True)
# print(catalogs)
# print(responsible)

# Muns to Muns reference
ref_muns = form_to_maps_muns(resp_muns)
refmap_muns = ref_muns.reset_index()
refmap_muns = refmap_muns.set_index('Municipio Mapa')  # Ref con indice de mapa
refmap_muns['NIndex'] = list(range(len(refmap_muns)))
# print(refmap_muns)
for x in refmap_muns.index.unique():
    u = refmap_muns.loc[x]
    if u.ndim > 1:
        us = u.iloc[-1]
        refmap_muns = refmap_muns.drop(index = x)
        refmap_muns.loc[x] = us
refmap_muns = refmap_muns.sort_values('NIndex')
refmap_muns.reset_index(inplace = True)
refmap_muns.set_index('NIndex', inplace = True, drop = True)
# print(refmap_muns)
select_index = refmap_muns.index
# Question 6 P2

# print(responsible)
responsible_data = responsible.reset_index()
responsible_data = responsible_data.loc[select_index]
# print(responsible_data)

for x in responsible_data.index:
    mun = refmap_muns.loc[x,'Municipio Mapa']
    resp_type= responsible_data.loc[x,'Tipo']
    if mun in sonora_form.index:
        sonora_form.loc[mun, 'Responsable Tipo'] = resp_type

print(form_sheets)
polits = form["9"]
polits = polits.loc[select_index]

for x in polits.index:
    mun = refmap_muns.loc[x,'Municipio Mapa']
    resp_type = polits.loc[x,'Respuesta Corta']
    if mun in sonora_form.index:
        sonora_form.loc[mun, 'Politicas'] = resp_type

#x = form["11"]
# print(x[11])

#x = form["13"]  ## Archivo
#print(x)
# print(x[11])

#x = form["18"]  ## Pendiente
#print(x)

#x = form["19"]  ## Pendiente
# print(x)

convents = form["20"]
convents = convents.loc[select_index]

for x in convents.index:
    mun = refmap_muns.loc[x,'Municipio Mapa']
    resp_type = convents.loc[x,'Respuesta']
    if mun in sonora_form.index:
        sonora_form.loc[mun, 'Convenios'] = resp_type

pmg = form["21"]
pmg = pmg.loc[select_index]

for x in pmg.index:
    mun = refmap_muns.loc[x,'Municipio Mapa']
    resp_type = pmg.loc[x,21]
    if mun in sonora_form.index:
        try:
            resp_type = resp_type.split(',')[0].capitalize()
        except ValueError:
            continue
        sonora_form.loc[mun, 'PlanM'] = resp_type
# print(sonora_form)

x = form["23"]  # Pendiente
# print(x)

discusion = form["24"]
discusion = discusion.loc[select_index]

for c in ['Plazo',"Veces", "Método"]:
    for x in discusion.index:
        mun = refmap_muns.loc[x,'Municipio Mapa']
        resp_type = discusion.loc[x, c]
        if mun in sonora_form.index:
            sonora_form.loc[mun, f"Dis_{c}"] = resp_type
# print(sonora_form)

program = form["25"]
program = program.loc[select_index]

for x in program.index:
    mun = refmap_muns.loc[x,'Municipio Mapa']
    resp_type = program.loc[x,25]
    if mun in sonora_form.index:
        try:
            resp_type = resp_type.split(',')[0].capitalize()
        except AttributeError:
            continue
        sonora_form.loc[mun, "Programa"] = resp_type
# print(sonora_form)




# Plot Maps
PLOT_MAPS = 1
SAVE_MAPS = 1
selection_maps = {
    "Municipios Partipantes": 1,
    "Responsables": 1,
    "Politicas": 1,
    "Convenios": 1,
    "PlanM": 1,
    "Dis_Plazo": 1,
    "Dis_V": 1,
    "Dis_Met": 1,
    "Programa": 1,
}

if PLOT_MAPS:
    if selection_maps['Municipios Partipantes']:
        resp, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Encuestado', categorical = True,
                        legend = True, legend_kwds = {"title":"¿Respondió?"},
                        ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        resp.suptitle('Encuestados en Genero')
        resp.tight_layout()
        ax.set_axis_off()
        plt.show()
    if selection_maps['Responsables']:
        respt, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Responsable Tipo', categorical = True, legend = True,
                        legend_kwds = {"title": "P. Responsable"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        respt.tight_layout()
        ax.set_axis_off()
    if selection_maps['Politicas']:
        pols, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Politicas', categorical = True, legend = True,
                        legend_kwds = {"title": "¿Politicas?"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        pols.tight_layout()
        ax.set_axis_off()
    if selection_maps['Convenios']:
        convs, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Convenios', categorical = True, legend = True,
                        legend_kwds = {"title": "¿Convenios?"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        convs.tight_layout()
        ax.set_axis_off()
    if selection_maps['PlanM']:
        plm, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('PlanM', categorical = True, legend = True,
                        legend_kwds = {"title": "¿PlanM?"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        plm.tight_layout()
        ax.set_axis_off()
    if selection_maps['Dis_Plazo']:
        dpl, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Dis_Plazo', categorical = True, legend = True,
                        legend_kwds = {"title": "Plazo"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        dpl.tight_layout()
        ax.set_axis_off()
    if selection_maps['Dis_V']:  # Pendiente
        dv, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Dis_Veces', legend = True,
                        legend_kwds = {"title": "Veces"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        dv.tight_layout()
        ax.set_axis_off()
    if selection_maps['Dis_Met']:
        dmet, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Dis_Método', categorical = True, legend = True,
                        legend_kwds = {"title": "Método"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        dmet.tight_layout()
        ax.set_axis_off()
    if selection_maps['Programa']:
        program, ax = plt.subplots(figsize = Mapper.FIGSIZE)
        sonora_form.plot('Programa', categorical = True, legend = True,
                        legend_kwds = {"title": "¿Programa?"}, ax = ax)
        sonora.boundary.plot(color = "black", lw = 0.5, ax = ax)
        program.tight_layout()
        ax.set_axis_off()
plt.show()


if SAVE_MAPS:
    save_maps = {
    "Municipios Partipantes": resp,
    "Responsables": respt,
    "Politicas": pols,
    "Convenios": convs,
    "PlanM": plm,
    "Dis_Plazo": dpl,
    "Dis_V": dv,
    "Dis_Met": dmet,
    "Programa": program,
    }
    for k, v in save_maps.items():
        v.savefig(f"{k}.png")
