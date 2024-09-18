#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####

from Mapper import mapper as Mapper
ext_plt = Mapper.plt
import os
import pandas as pd

years = ['2000','2005','2010','2020']

y0 = years[0]

yfolder = f"IndiceRezagoSocial\\R{y0}"
rfolder = os.listdir(yfolder)


indrs = pd.read_excel(os.path.join(yfolder,rfolder[0]), index_col = 0)
inpi = pd.read_excel(os.path.join(yfolder,rfolder[1]), index_col = 0)
iter = pd.read_excel(os.path.join(yfolder,rfolder[2]), index_col = 0)

resumen = pd.DataFrame(index = iter.index, columns = ['Población Total','Indigena','Indice de Rezago Social'])

resumen['Población Total'] = iter['pobtot']
resumen['Indigena'] = 0

resumen.index = [str(x) for x in resumen.index]
indrs.index = [str(x) for x in indrs.index]
inpi.index = [str(x) for x in inpi.index]
iter.index = [str(x) for x in iter.index]

des_loc_ind  = 0
for x in indrs.index:
    if x in resumen.index:
        resumen.loc[x, 'Indice de Rezago Social'] = indrs.loc[x, 'Índice de rezago social']
    else:
        des_loc_ind += 1

des_loc_indp = des_loc_ind / len(indrs)
print(f"Hay {des_loc_ind} con indice de rezago social que no aparecen en el iter. Aproximadamente el {round(des_loc_indp * 100,2)}%")

des_loc_indg = 0
for x in inpi.index:
    if x in resumen.index:
        resumen.loc[x, 'Indigena'] = 1
    else:
        des_loc_indg += 1
        

des_loc_indpg = des_loc_indg / len(inpi)

print(f"Hay {des_loc_indg} localidades indigenas que no aparecen en el iter. Aproximadamente el {round(des_loc_indpg * 100,2)}%")


sonora = Mapper.create_map(region = 'Sonora', map_type = 'Municipios')
sonora_lpr = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Puntuales Rur')
sonora_l = Mapper.create_map(region = 'Sonora', map_type = 'Locs. Urb y Rur Amnzs')


sonora_locs = sonora_lpr.copy()

for x in sonora_l.index:
    if not x in sonora_locs.index:
        sonora_locs.loc[x] = sonora_l.loc[x]

sonora_locs['ITER'] = 0
sonora_locs['CVE'] = sonora_locs['CVE_ENT']+ sonora_locs['CVE_MUN'] + sonora_locs['CVE_LOC']
sonora_locs.set_index('CVE', inplace = True)
sonora_locs.drop(columns = ['CVE_ENT','CVE_MUN','CVE_LOC'], inplace = True)


des_loc_iter = 0
for x in resumen.index:
    if x in sonora_locs.index:
        sonora_locs.loc[str(x), ['Población Total','Indigena','Indice de Rezago Social']] = resumen.loc[x,['Población Total','Indigena','Indice de Rezago Social']]
        sonora_locs.loc[str(x), 'ITER'] = 1
    else:
        des_loc_iter += 1

des_loc_iterp = des_loc_iter / len(resumen)

print(f"Hay {des_loc_iter} localidades que no aparecerán en el mapa. Aproximadamente el {round(des_loc_iterp * 100,2)}%")

sonora_locs.drop(columns = ['CVE_AGEB','CVE_MZA','PLANO'], inplace = True)
sonora_locs['ITER'] = sonora_locs['ITER'].astype(str)
sonora_iter = sonora_locs[sonora_locs['ITER'] == '1']
sonora_iter['Indigena'] = sonora_iter['Indigena'].astype(int)
sonora_iter['Indigena'] = sonora_iter['Indigena'].astype(str)


def mapa_iter():
    itervsmap, ax = ext_plt.subplots(figsize = (20,20))
    ax.set_title(f"Localidades consideradas en el ITER {y0}")
    sonora_locs.plot('ITER', ax = ax, legend = True)
    sonora.boundary.plot(lw = 0.5, color = "black", ax = ax)
    ax.set_axis_off()
    ext_plt.show()
    return itervsmap


def mapa_iter_indigena():
    map_locind, ax = ext_plt.subplots(figsize = (20,20))
    ax.set_title(f"Localidades Indigenas en el ITER {y0}")
    sonora_iter.plot('Indigena', legend = True, ax = ax)
    ax.set_axis_off()
    sonora.boundary.plot(lw = 0.5, ax = ax)
    ext_plt.show()
    return map_locind


def mapa_indrs():
    map_locind, ax = ext_plt.subplots(figsize = (20,20))
    ax.set_title(f"Indice de Rezago Social {y0}")
    sonora_iter.plot('Indice de Rezago Social', legend = True, ax = ax)
    ax.set_axis_off()
    sonora.boundary.plot(lw = 0.5, ax = ax)
    ext_plt.show()
    return map_locind


def mapa_indrs_indigena():
    sonora_iterind = sonora_iter[sonora_iter['Indigena'] == "1"]
    map_locind, ax = ext_plt.subplots(figsize = (20,20))
    ax.set_title(f"Indice de Rezago Social Indigena {y0}")
    sonora_iterind.plot('Indice de Rezago Social', legend = True, ax = ax)
    sonora.boundary.plot(lw = 0.5, ax = ax)
    ax.set_axis_off()
    ext_plt.show()
    return map_locind


mapa_iter()
mapa_iter_indigena()
mapa_indrs()
mapa_indrs_indigena()