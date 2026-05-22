import pandas as pd
import json
import time
import subprocess
from datetime import datetime

# =========================================
# CONFIGURACIÓN
# =========================================

CSV_FILE = r"C:\planta_monitor\csv\medidor_actual.csv"

JSON_FILE = r"C:\planta_monitor\datos.json"

TIMESTAMP_FILE = r"C:\planta_monitor\ultimo_timestamp.txt"

REPO_DIR = r"C:\planta_monitor"

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

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # ordenar por tiempo
        df = df.sort_values("timestamp")

        # =====================================
        # LEER ÚLTIMO TIMESTAMP
        # =====================================

        with open(TIMESTAMP_FILE, "r") as f:

            ultimo_timestamp = f.read().strip()

        ultimo_timestamp = pd.to_datetime(ultimo_timestamp)

        print("\nULTIMO TIMESTAMP:")
        print(ultimo_timestamp)

        # =====================================
        # FILTRAR NUEVOS
        # =====================================

        nuevos = df[df["timestamp"] > ultimo_timestamp]

        # =====================================
        # SI HAY NUEVOS
        # =====================================

        if len(nuevos) > 0:

            print(f"\nNUEVOS REGISTROS: {len(nuevos)}")

            # TOMAR EL SIGUIENTE REGISTRO
            fila = nuevos.iloc[0]

            print("\nREGISTRO ENVIADO:")
            print(fila["timestamp"])

            datos = {

                "fecha_hora": str(fila["timestamp"]),

                "voltaje_r": round(float(fila["voltaje_r"]), 2),
                "voltaje_s": round(float(fila["voltaje_s"]), 2),
                "voltaje_t": round(float(fila["voltaje_t"]), 2),

                "corriente_r": round(float(fila["corriente_r"]), 2),
                "corriente_s": round(float(fila["corriente_s"]), 2),
                "corriente_t": round(float(fila["corriente_t"]), 2),

                "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # =================================
            # GUARDAR JSON
            # =================================

            with open(JSON_FILE, "w", encoding="utf-8") as f:

                json.dump(datos, f, indent=4)

            print("\nJSON ACTUALIZADO")

            # =================================
            # GUARDAR NUEVO TIMESTAMP
            # =================================

            with open(TIMESTAMP_FILE, "w") as f:

                f.write(str(fila["timestamp"]))

            print("TIMESTAMP ACTUALIZADO")

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

            print("PUSH OK")

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