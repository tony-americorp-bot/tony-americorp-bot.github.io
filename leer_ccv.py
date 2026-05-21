import pandas as pd
import json
import time
import subprocess
from datetime import datetime

# =====================================
# CONFIGURACIÓN
# =====================================

CSV_FILE = r"C:\planta_monitor\medidor_energia_2026-05-21.csv"
JSON_FILE = r"C:\planta_monitor\datos.json"
REPO_DIR = r"C:\planta_monitor"

INTERVALO = 10  # segundos

# =====================================
# LEER CSV COMPLETO
# =====================================

df = pd.read_csv(CSV_FILE)

total_registros = len(df)

print(f"TOTAL REGISTROS: {total_registros}")

indice = 0

# =====================================
# LOOP PRINCIPAL
# =====================================

while True:

    try:

        fila = df.iloc[indice]

        datos = {

            "registro_actual": indice + 1,
            "total_registros": total_registros,

            "fecha_hora": str(fila["timestamp"]),

            "voltaje_r": round(float(fila["voltaje_r"]), 2),
            "voltaje_s": round(float(fila["voltaje_s"]), 2),
            "voltaje_t": round(float(fila["voltaje_t"]), 2),

            "corriente_r": round(float(fila["corriente_r"]), 2),
            "corriente_s": round(float(fila["corriente_s"]), 2),
            "corriente_t": round(float(fila["corriente_t"]), 2),

            "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # =====================================
        # GUARDAR JSON
        # =====================================

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

        print(f"REGISTRO ENVIADO: {indice + 1}")

        # =====================================
        # GIT ADD
        # =====================================

        subprocess.run(
            ["git", "add", "."],
            cwd=REPO_DIR
        )

        # =====================================
        # GIT COMMIT
        # =====================================

        subprocess.run(
            ["git", "commit", "-m", f"registro {indice + 1}"],
            cwd=REPO_DIR
        )

        # =====================================
        # GIT PUSH
        # =====================================

        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=REPO_DIR
        )

        # =====================================
        # SIGUIENTE FILA
        # =====================================

        indice += 1

        if indice >= total_registros:
            indice = 0

    except Exception as e:

        print("ERROR:", e)

    time.sleep(INTERVALO)