#### Ajuste por Carpetas
import sys
sys.path.insert(1, "..\\Mapper\\Mapper")
sys.path.insert(1, "..\\Mapper")
####

from Mapper import mapper as Mapper
import matplotlib.pyplot as plt
from Mapper import general_tools as gt
import numpy as np


# Auxiliary Functions




# Data Paths
folder_edu = "..\\Mapper\\Educación"
path_data = "data\\educ-data.xlsx"
folder_out_data =  folder_edu + "\\out_data"

# Formatting Data
data = Mapper.ext_pd.read_excel(folder_edu + "\\" + path_data)
data = data.iloc[1:,1:]
data.columns = data.iloc[0]
data.drop(index = 1, inplace = True)
data.reset_index(drop = True, inplace = True)


# Agrouping data 
cicles = data['Ciclo'].unique()
data_cicle = {c:data[data['Ciclo'] == c] for c in cicles}

def cicle_data(cicle):
    df = data_cicle[cicle]
    df = df.iloc[:-1]
    df.reset_index(drop = True, inplace = True)
    return df
# Example Data
ex_cicle = cicles[0]
ex_data = cicle_data(ex_cicle)

# Create the Sonora Map. 
son = Mapper.create_map(region = 'Sonora', map_type = "Municipios")
sonora = son.copy()

# Homegenize municipies
## Lists of the Muns.
data_muns = ex_data['Municipio'] # Muns by Data
muns = list(sonora.index) # Muns by Map
## Levenshtein Distance
### Adjust the Muns names
data_muns = [dm.title() for dm in data_muns]
df_lev = gt.matrix_lev(data_muns, muns)

adjust_muns = []
for il in df_lev.index:
    mun_dists = df_lev.loc[il]
    min_dist = mun_dists.min()
    ldist = mun_dists.tolist()
    mun_id = ldist.index(min_dist)
    adjust_muns.append(muns[mun_id])

## Add New Muns
ex_data.index = adjust_muns
ex_data.index.name = "Municipios"

# Add Mun_data to Map

columns_plot = ["Escuelas","Alumnos","Alumnos Mujeres","Alumnos Hombres", "Docentes¹"]
for c in columns_plot:
    sonora[c] = ex_data[c].astype(int)

# Plot Data
plot_column = columns_plot[1]

#fig, ax = plt.subplots(figsize = (20,20))
#fig.suptitle(f"{plot_column} en el Estado de Sonora")
#sonora.plot(plot_column, legend = True, ax = ax, scheme = "quantiles",k = 4, cmap = "Blues")
# ax.set_axis_off()



## Calculate the top5 muns in plot
def calc_top(n):
    top = ex_data.copy()
    top = top.sort_values(plot_column, ascending = False).iloc[:n]
    return top

top5 = calc_top(5)

## Add annotations
ltop5 = list(top5.index)
for i_s in list(sonora.index):
        try:
            ti = ltop5.index(i_s)
            if ti >= 0:
                print(i_s)
                sonora.loc[i_s, 'Texto'] =f"{top5.loc[i_s, plot_column]:,}"   
        except:
            sonora.loc[i_s, 'Texto'] = ""

#for i_s in sonora.index:
#    ax.annotate(text = sonora.loc[i_s, 'Texto'], xy = sonora.loc[i_s].geometry.centroid.coords[0], color = "white")


# Correct Plot



fig, ax = plt.subplots(figsize = (20,20))
fig.suptitle(f"{plot_column} en el Estado de Sonora")
Mapper.read_preset(sonora, 'preset_1', ax)
ax.set_axis_off()
plt.show()
    

