import transform_regions as tr
      
dict_maptypes = {'Estados': 'ent.shp',
                'Municipios': 'mun.shp',
                'AGEBRur': 'ar.shp',
                'Locs. Puntuales Rur': 'lpr.shp',
                'Insular': 'ti.shp',
                'Polys. Exts. Rurales': 'pe.shp',
                'Polys. Exts. Manzanas': 'pem.shp',
                'AGEB': 'a.shp',
                'Manzanas': 'm.shp',
                'Frentes Mzns': 'fm.shp',
                'Vialidad': 'e.shp',
                'Caserio Disperso': 'cd.shp',
                'Locs. Urb y Rur Amnzs': 'l.shp'}


def select_maptype(code, mtype):
    files_shp = {}
    region_path = f"Mapper\\data_geo\\select\\{tr.country}\\{code}"
    if not tr.gtools.os.path.exists(region_path):
        tr.unzip_region(code)
        tr.clean_region_f(code)
    for fr in tr.gtools.os.listdir(region_path):
        if fr.endswith('shp'):
            files_shp[fr] = tr.gtools.os.path.join(region_path, fr)
    try:
        mtype = dict_maptypes[mtype]
    except:
        print("Tu region no posee esté tipo de mapa. ")
        mtype = "ent"
    if code == "mg":
            code = '00'
    filecode = "".join([code, mtype])
    return files_shp[filecode]

