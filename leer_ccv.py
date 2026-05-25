import pandas as pd
import json
import time
import subprocess
import math
import random

from datetime import datetime

# =========================================
# CONFIGURACIÓN
# =========================================

CSV_FILE = r"C:\scada_monitor\csv\medidor_actual.csv"

JSON_FILE = r"C:\scada_monitor\datos.json"

TIMESTAMP_FILE = r"C:\scada_monitor\ultimo_timestamp.txt"

REPO_DIR = r"C:\scada_monitor"

INTERVALO = 60

# =========================================
# LOOP PRINCIPAL
# =========================================

while True:

    try:

        print("\n===================================")
        print("LEYENDO CSV...")

        # =====================================
        # LEER CSV SIN CABECERAS
        # =====================================

        df = pd.read_csv(

            CSV_FILE,

            header=None,

            names=[

                "timestamp",

                "voltaje_r",
                "voltaje_s",
                "voltaje_t",

                "corriente_r",
                "corriente_s",
                "corriente_t"

            ]

        )

        print("\nCSV LEIDO CORRECTAMENTE")

        # =====================================
        # CONVERTIR TIMESTAMP
        # =====================================

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        # =====================================
        # ORDENAR POR FECHA
        # =====================================

        df = df.sort_values("timestamp")

        # =====================================
        # LEER ULTIMO TIMESTAMP
        # =====================================

        with open(TIMESTAMP_FILE, "r") as f:

            ultimo_timestamp = f.read().strip()

        ultimo_timestamp = pd.to_datetime(
            ultimo_timestamp
        )

        print("\nULTIMO TIMESTAMP:")
        print(ultimo_timestamp)

        # =====================================
        # FILTRAR NUEVOS
        # =====================================

        nuevos = df[
            df["timestamp"] > ultimo_timestamp
        ]

        # =====================================
        # SI HAY NUEVOS
        # =====================================

        if len(nuevos) > 0:

            print(f"\nNUEVOS REGISTROS: {len(nuevos)}")

            # =================================
            # TOMAR SIGUIENTE FILA
            # =================================

            fila = nuevos.iloc[0]

            print("\nREGISTRO ENVIADO:")
            print(fila["timestamp"])

            # =================================
            # TIEMPO SIMULACION
            # =================================

            t = time.time()

            # =================================
            # VARIABLES BASE CSV
            # =================================

            voltaje_r_base = float(
                fila["voltaje_r"]
            )

            voltaje_s_base = float(
                fila["voltaje_s"]
            )

            voltaje_t_base = float(
                fila["voltaje_t"]
            )

            corriente_r_base = float(
                fila["corriente_r"]
            )

            corriente_s_base = float(
                fila["corriente_s"]
            )

            corriente_t_base = float(
                fila["corriente_t"]
            )

            # =================================
            # SIMULACION INDUSTRIAL
            # =================================

            voltaje_r = (

                voltaje_r_base
                +
                math.sin(t / 8) * 12
                +
                random.uniform(-1,1)

            )

            voltaje_s = (

                voltaje_s_base
                +
                math.sin(t / 15) * 5
                +
                random.uniform(-0.5,0.5)

            )

            voltaje_t = (

                voltaje_t_base
                +
                math.cos(t / 5) * 1.2
                +
                random.uniform(-0.2,0.2)

            )

            corriente_r = (

                corriente_r_base
                +
                math.cos(t / 10) * 3
                +
                random.uniform(-1,1)

            )

            corriente_s = (

                corriente_s_base
                +
                math.sin(t / 7) * 2
                +
                random.uniform(-1,1)

            )

            corriente_t = (

                corriente_t_base
                +
                math.sin(t / 20) * 50
                +
                random.uniform(-5,5)

            )

            # =================================
            # GENERAR JSON
            # =================================

            datos = {

                "fecha_hora":

                    str(fila["timestamp"]),

                "voltaje_r":

                    round(voltaje_r, 2),

                "voltaje_s":

                    round(voltaje_s, 2),

                "voltaje_t":

                    round(voltaje_t, 2),

                "corriente_r":

                    round(corriente_r, 2),

                "corriente_s":

                    round(corriente_s, 2),

                "corriente_t":

                    round(corriente_t, 2),

                "actualizado":

                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

            }

            # =================================
            # GUARDAR JSON
            # =================================

            with open(

                JSON_FILE,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(
                    datos,
                    f,
                    indent=4
                )

            print("\nJSON ACTUALIZADO")

            print("\nVALORES ENVIADOS:")

            print(datos)

            # =================================
            # GUARDAR NUEVO TIMESTAMP
            # =================================

            with open(TIMESTAMP_FILE, "w") as f:

                f.write(
                    str(fila["timestamp"])
                )

            print("\nTIMESTAMP ACTUALIZADO")

            # =================================
            # GIT ADD
            # =================================

            subprocess.run(

                ["git", "add", "."],

                cwd=REPO_DIR

            )

            # =================================
            # COMMIT
            # =================================

            subprocess.run(

                [

                    "git",

                    "commit",

                    "-m",

                    f"update {datetime.now()}"

                ],

                cwd=REPO_DIR

            )

            # =================================
            # PUSH
            # =================================

            subprocess.run(

                [

                    "git",

                    "push",

                    "origin",

                    "main"

                ],

                cwd=REPO_DIR

            )

            print("\nPUSH OK")

        else:

            print("\nNO HAY REGISTROS NUEVOS")

    except Exception as e:

        print("\nERROR GENERAL:")
        print(e)

    # =====================================
    # ESPERAR
    # =====================================

    print(f"\nESPERANDO {INTERVALO} SEGUNDOS...\n")

    time.sleep(INTERVALO)