import pandas as pd
import json
import time
import subprocess
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================

CSV_FILE = r"C:\planta_monitor\medidor_energia_2026-05-21.csv"
JSON_FILE = r"C:\planta_monitor\datos.json"
REPO_DIR = r"C:\planta_monitor"

INTERVALO = 10  # segundos

# =========================
# LEER CSV
# =========================

def leer_csv():
    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            print("CSV vacío")
            return None

        ultimo = df.iloc[-1]

        datos = {
            "fecha_hora": str(ultimo["timestamp"]),
            "voltaje_r": round(float(ultimo["voltaje_r"]), 2),
            "voltaje_s": round(float(ultimo["voltaje_s"]), 2),
            "voltaje_t": round(float(ultimo["voltaje_t"]), 2),
            "corriente_r": round(float(ultimo["corriente_r"]), 2),
            "corriente_s": round(float(ultimo["corriente_s"]), 2),
            "corriente_t": round(float(ultimo["corriente_t"]), 2),
            "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return datos

    except Exception as e:
        print("ERROR leyendo CSV:", e)
        return None

# =========================
# GUARDAR JSON
# =========================

def guardar_json(datos):
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

        print("JSON actualizado")

    except Exception as e:
        print("ERROR guardando JSON:", e)

# =========================
# GIT PUSH
# =========================

def git_push():
    try:
        comandos = [
            ["git", "add", "."],
            ["git", "commit", "-m", f"update {datetime.now()}"],
            ["git", "push", "origin", "main"]
        ]

        for cmd in comandos:
            resultado = subprocess.run(
                cmd,
                cwd=REPO_DIR,
                capture_output=True,
                text=True
            )

            print("\nCMD:", " ".join(cmd))
            print(resultado.stdout)

            if resultado.stderr:
                print("ERROR:", resultado.stderr)

    except Exception as e:
        print("ERROR GIT:", e)

# =========================
# LOOP PRINCIPAL
# =========================

print("INICIANDO MONITOR...")

while True:

    datos = leer_csv()

    if datos:
        guardar_json(datos)
        git_push()

    print(f"Esperando {INTERVALO} segundos...\n")

    time.sleep(INTERVALO)