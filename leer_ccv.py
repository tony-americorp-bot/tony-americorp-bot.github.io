import pandas as pd
import json
import time
import subprocess
from datetime import datetime

# =========================================
# CONFIGURACIÓN
# =========================================

CSV_FILE = r"C:\planta_monitor\medidor_energia_2026-05-21.csv"
JSON_FILE = r"C:\planta_monitor\datos.json"
REPO_DIR = r"C:\planta_monitor"

INTERVALO = 60  # segundos

# =========================================
# LEER CSV
# =========================================

df = pd.read_csv(CSV_FILE)

TOTAL = len(df)

print(f"TOTAL FILAS: {TOTAL}")

indice = 0

# =========================================
# LOOP PRINCIPAL
# =========================================

while True:

    try:

        fila = df.iloc[indice]

        print("\n============================")
        print(f"MOSTRANDO FILA: {indice + 1}")

        datos = {

            "registro_actual": indice + 1,
            "total_registros": TOTAL,

            "fecha_hora": str(fila["timestamp"]),

            "voltaje_r": round(float(fila["voltaje_r"]), 2),
            "voltaje_s": round(float(fila["voltaje_s"]), 2),
            "voltaje_t": round(float(fila["voltaje_t"]), 2),

            "corriente_r": round(float(fila["corriente_r"]), 2),
            "corriente_s": round(float(fila["corriente_s"]), 2),
            "corriente_t": round(float(fila["corriente_t"]), 2),

            "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # =========================================
        # GUARDAR JSON
        # =========================================

        with open(JSON_FILE, "w", encoding="utf-8") as f:

            json.dump(datos, f, indent=4)

        print("JSON ACTUALIZADO")

        # =========================================
        # GIT ADD
        # =========================================

        subprocess.run(
            ["git", "add", "."],
            cwd=REPO_DIR
        )

        # =========================================
        # GIT COMMIT
        # =========================================

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"registro_{indice + 1}"
            ],
            cwd=REPO_DIR
        )

        # =========================================
        # GIT PUSH
        # =========================================

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

        # =========================================
        # SIGUIENTE FILA
        # =========================================

        indice += 1

        if indice >= TOTAL:

            indice = 0

        print(f"SIGUIENTE FILA: {indice + 1}")

    except Exception as e:

        print("ERROR:", e)

    time.sleep(INTERVALO)