import general_tools as gtools
import abbreviation
import requests
# Country Urls Auxiliar
## Mexico
mex_1 = "https://www.inegi.org.mx/contenidos/productos/prod_serv"
mex_2 = "/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551067314_s.zip"

# Contries Urls

country_urls = {
    "Mexico" : mex_1 + mex_2
}
folder_maps = 'data_geo'
path_folder_maps = gtools.os.path.join("Mapper",folder_maps)
gtools.create_folder(path_folder_maps)

def select_country(country):
    """
    Descargar la información de 
    """
    extension = ".zip"
    filename = country + extension
    if not gtools.os.path.exists(gtools.os.path.join(path_folder_maps, filename)):
        data = requests.get(country_urls[country], stream = True)
        with open(gtools.os.path.join(path_folder_maps, filename), "wb") as f:
            for c, chunk in enumerate(data.iter_content(chunk_size=512)):
                print(f"{round(100 * c / 6246342, 2)} %" ) # Aprox Size Charge Bar
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print("El archivo ya existe, borre la ubicación antes de descargar")
    gtools.create_folder("Mapper\\data_mapper")
    gtools.create_folder(f"Mapper\\data_mapper\\{country}")




country = "Mexico"


select_country(country)
abbreviation.load_mex_abrs()