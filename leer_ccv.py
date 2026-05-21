import pandas as pd
import json
import time
import subprocess
from datetime import datetime

# =========================================
# CONFIG
# =========================================

CSV_FILE = r"C:\planta_monitor\medidor_energia_2026-05-21.csv"
JSON_FILE = r"C:\planta_monitor\datos.json"
REPO_DIR = r"C:\planta_monitor"

INTERVALO = 10

# =========================================
# LEER CSV
# =========================================

df = pd.read_csv(CSV_FILE)

TOTAL = len(df)

print(f"TOTAL FILAS: {TOTAL}")

indice = 0

# =========================================
# LOOP
# =========================================

while True:

    try:

        # =====================================
        # TOMAR FILA ACTUAL
        # =====================================

        fila = df.iloc[indice]

        print("\n========================")
        print(f"MOSTRANDO FILA: {indice + 1}")

        datos = {

            "registro_actual": indice + 1,
            "total_registros": TOTAL,

            "fecha_hora": str(fila["timestamp"]),

            "voltaje_r": float(fila["voltaje_r"]),
            "voltaje_s": float(fila["voltaje_s"]),
            "voltaje_t": float(fila["voltaje_t"]),

            "corriente_r": float(fila["corriente_r"]),
            "corriente_s": float(fila["corriente_s"]),
            "corriente_t": float(fila["corriente_t"]),

            "actualizado": datetime.now().strftime("%H:%M:%S")
        }

        # =====================================
        # GUARDAR JSON
        # =====================================

        with open(JSON_FILE, "w", encoding="utf-8") as f:

            json.dump(datos, f, indent=4)

        print("JSON ACTUALIZADO")

        # =====================================
        # GIT ADD
        # =====================================

        subprocess.run(
            ["git", "add", "."],
            cwd=REPO_DIR
        )

        # =====================================
        # COMMIT
        # =====================================

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"registro_{indice+1}"
            ],
            cwd=REPO_DIR
        )

        # =====================================
        # PUSH
        # =====================================

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

        # =====================================
        # SIGUIENTE FILA
        # =====================================

        indice = indice + 1

        # VOLVER AL INICIO
        if indice >= TOTAL:

            indice = 0

        print(f"SIGUIENTE FILA: {indice + 1}")

    except Exception as e:

        print("ERROR:", e)

    time.sleep(INTERVALO)