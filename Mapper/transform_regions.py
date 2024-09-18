import general_tools as gtools
import shutil

country = "Mexico"
path_country = f"Mapper\\data_geo\\{country}"
folder_select = f"Mapper\\data_geo\\select"
folder_state = f"Mapper\\data_geo\\select\\{country}"
gtools.create_folder(folder_select)
gtools.create_folder(folder_state)
files = gtools.os.listdir(path_country)

dict_code_state = {f[:2] : f for f in files}

def region_path(code):
    return gtools.os.path.join(path_country,dict_code_state[code])

def unzip_region(code):
    path = region_path(code)
    folder_region = gtools.os.path.join(folder_state, code)
    gtools.create_folder(folder_region)
    gtools.unzip(folder_region, path)

def clean_region_f(code):
    folder_region = gtools.os.path.join(folder_state, code)
    for f in gtools.os.listdir(folder_region):
        if not f.startswith('conjunto'):
            try:
                shutil.rmtree(gtools.os.path.join(folder_region,f))
            except:
                continue
        else:
            y = f
    for f in gtools.os.listdir(gtools.os.path.join(folder_region, y)):
        gtools.os.rename(gtools.os.path.join(gtools.os.path.join(folder_region, y),f),gtools.os.path.join(folder_region,f))
    gtools.os.removedirs(gtools.os.path.join(folder_region,y))
