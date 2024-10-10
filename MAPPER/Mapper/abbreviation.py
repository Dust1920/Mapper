import tabula 
import urllib.request
import pandas as pd
import os

# Mexico states abbreviations

def load_mex_abrs():
    """
    Obtener las abreviaturas de los entidades federativas de México
    """
    country = "Mexico"
    if not os.path.exists(f"Mapper\\data_mapper\\{country}\\abr_1.csv"):
        url_abr = "https://www.ieec.org.mx/transparencia/doctos/art74/i/reglamentos/Reglamento_de_elecciones/anexo_7.pdf"
        pdf_abr_path = f"Mapper\\data_mapper\\{country}\\abr.pdf"
        if not os.path.exists(pdf_abr_path):
            urllib.request.urlretrieve(url_abr, f"Mapper\\data_mapper\\{country}\\abr.pdf")

        table = tabula.read_pdf(pdf_abr_path, stream=True)[0]
        table.set_index('ID_ESTADO', drop=True, inplace=True)
        table.to_csv(f"Mapper\\data_mapper\\{country}\\abr_1.csv")

    if not os.path.exists(f"Mapper\\data_mapper\\{country}\\abr.csv"):
        url_abr1 = "https://es.wikipedia.org/wiki/Anexo:Abreviaturas_en_M%C3%A9xico"
        tables = pd.read_html(url_abr1)
        abr = tables[0].loc[:, [0,4]]
        abr.columns = ["Estado","Abreviatura"]
        abr.drop(index = [0, 1, 2, 35], inplace=True)
        abr.index = [x for x in range(1,33)]
        abr.to_csv(f"Mapper\\data_mapper\\{country}\\abr.csv")
