import requests
import time
from datetime import datetime

# =========================================
# CONFIGURACIÓN
# =========================================

URL = "http://13.222.228.90:1880/descargar-csv"

DESTINO = r"C:\planta_monitor\csv\medidor_actual.csv"

INTERVALO = 60  # segundos

# =========================================
# LOOP INFINITO
# =========================================

while True:

    try:

        print("\n===================================")
        print("DESCARGANDO CSV...")

        respuesta = requests.get(URL)

        if respuesta.status_code == 200:

            with open(DESTINO, "wb") as archivo:

                archivo.write(respuesta.content)

            print("CSV ACTUALIZADO")

            print("ARCHIVO:")
            print(DESTINO)

            print("HORA:")
            print(datetime.now())

        else:

            print("ERROR DESCARGA:")
            print(respuesta.status_code)

    except Exception as e:

        print("ERROR:")
        print(e)

    # ESPERAR 1 MINUTO
    time.sleep(INTERVALO)