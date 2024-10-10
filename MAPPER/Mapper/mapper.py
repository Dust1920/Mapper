import sys
sys.path.insert(1, "..\\Mapper\\Mapper")

# Central Mapper Tool
import types_maps as tym
import geopandas as gpd
import matplotlib.pyplot as plt



ext_pd = tym.tr.gtools.pd
ext_pd.options.mode.copy_on_write = True

plt.rcParams["font.family"] = "monospace"
FIGSIZE = (20,20)




country = "Mexico"

df_states = ext_pd.read_csv(f"..\\Mapper\\Mapper\\data_mapper\\{country}\\states_code.csv", index_col=1)

def create_map(**kwargs):
    region = kwargs.get("region", "mg")
    region = df_states.loc[region, 'CVE_ENT']
    region = f'0{region}' if region<10 else str(region)
    mtp = kwargs.get("map_type", "Estados")
    map_file = tym.select_maptype(region,mtp)
    df = gpd.read_file(map_file)
    df = df.to_crs("WGS84")
    if region == "mg":
        df.drop(columns = ['CVEGEO'], inplace = True)
        df.set_index('CVE_ENT', drop = True, inplace = True)
        for cve in df.index:
            text = df.loc[cve, 'NOMGEO']
            text_s = text.split(" ")
            try:
                if text_s[1] == "de" and text_s[-1] != "México":
                    text = text_s[0]
            except:
                text = text
            df.loc[cve, 'NOMGEO'] = text
        df.set_index('NOMGEO', inplace = True, drop = True)
    else:
        df.sort_values("CVE_MUN", inplace = True)
        df.drop(columns = ['CVEGEO'], inplace = True)
        df.set_index("NOMGEO", inplace = True, drop = True)
    return df


def read_preset(map, file, ax):
    preset = ext_pd.read_excel(f"Presets\\{file}.xlsx", index_col = 0)
    map['Data'] = preset['Data']
    map.plot('Data', legend = True, ax = ax, scheme = "quantiles",k = 4, cmap = "Blues")
    for i in map.index:
        text_i = preset.loc[i,'Text']
        # text_i = "●" if not Mapper.pd.isna(text_i) else ""
        text_i = text_i if not ext_pd.isna(text_i) else ""
        ax.annotate(text = text_i, xy = (preset.loc[i,'text_x'],preset.loc[i,'text_y']),
                    color = preset.loc[i, 'text_color'],
                    fontsize = preset.loc[i, 'text_size'])
        

def custom_legend(mapa, data, **kwargs):
    
    return 0
