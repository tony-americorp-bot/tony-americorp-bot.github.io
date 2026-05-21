import pandas as pd
import json
import time

while True:

    # Leer CSV
    df = pd.read_csv("SRV002.M3000CV004REF.F_CV.csv")

    # Última fila
    ultima = df.iloc[0]

    # Crear JSON
    datos = {
        "tag": ultima["tagname"],
        "valor": ultima["value"],
        "timestamp": ultima["timestampseconds"]
    }

    # Guardar JSON
    with open("variables.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

    print("JSON actualizado")

    # Esperar 30 segundos
    time.sleep(10)