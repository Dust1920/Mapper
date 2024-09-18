################################################################################
#   Mapas de Educación 
#   Objetivo:
#       * Mapa con el número de estudiantes.
#       * Mapa con el porcentaje de atención. 
################################################################################

#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")

# Librerias Requeridas
## Mapper
from Mapper import mapper as Mappper
from Mapper import general_tools as gtools
## Librerías estándar
import pandas as pd
import matplotlib.pyplot as plt

# Mapa de Sonora 
sonora = Mappper.create_map(region = "Sonora", map_type = "Municipios")

# Fuente de información.
data = pd.read_excel("Educación\\data\\mapas v2.xlsx")
data.set_index('Etiquetas de fila', inplace=True, drop=True)

# Verificamos tipos de datos
print(data.dtypes)

# Análisis de Información
map_muns = list(sonora.index)
muns = list(data.index)

# Calcular matriz de Levenshtein
mlev = gtools.matrix_lev(muns, map_muns)

# Crear un diccionario para emparejar los municipios
connect_muns = {}
for m in mlev.index:
    m_array = mlev.loc[m]
    array_min = m_array.min()
    array_index = list(m_array).index(array_min)
    m_element = map_muns[array_index]
    if len(m) == len(m_element):
        connect_muns[m_element] = m

# Asignación de valores (Estudiantes, Porcentaje de acercamiento)
edu_values = {x: data.loc[connect_muns[x], 'Total general'] for x in map_muns}
perc_values = {x: data.loc[connect_muns[x],'Porcentaje'] for x in map_muns}

# Asignar valores al DataFrame de Sonora
for m_son in sonora.index:
    sonora.loc[m_son, 'basica'] = edu_values[m_son]
    sonora.loc[m_son, 'perc_basica'] = perc_values[m_son]

# Ajuste de porcentaje para que esté entre 0 y 1
for s in sonora.index:
    p_s = sonora.loc[s, 'perc_basica']
    x = 1 if p_s >= 1 else p_s
    sonora.loc[s, 'perc_basica'] = x

# Mostrar DataFrame final
## print(sonora['perc_basica'])
## print(sonora.dtypes)

# Generación de gráficos
educ, basica = plt.subplots(ncols=2, nrows=1, figsize=(21, 13))
sonora.plot('basica', scheme="percentiles", cmap = "Blues",
            legend=True,
            legend_kwds = {"loc" : "lower left"},
            ax=basica[0])
sonora.boundary.plot(lw = 0.5, color = "black", ax = basica[0])
sonora.plot('perc_basica', scheme="quantiles", k = 6, cmap = "Blues",
            legend=True,
            legend_kwds = {"loc" : "lower left"},
            ax=basica[1])
sonora.boundary.plot(lw = 0.5, color = "black", ax = basica[1])
basica[0].set_axis_off()
basica[1].set_axis_off()
plt.show()
