import general_tools as gtools

country = "Mexico"
path_maps_zip = f"Mapper\\data_geo\\{country}.zip"
path_states = f"Mapper\\data_geo\\{country}"
gtools.create_folder(path_states)
gtools.unzip(path_states, path_maps_zip)
