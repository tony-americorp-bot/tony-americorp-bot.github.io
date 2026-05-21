import os
import json
import pandas as pd
import time
import subprocess
from datetime import datetime

CARPETA = r"C:\planta_monitor"
JSON_FILE = r"C:\planta_monitor\datos.json"
CSV_FILE = r"C:\planta_monitor\SRV002.M3000CV004REF.F_CV.csv"

def leer_csv():
    df = pd.read_csv(CSV_FILE)
    ultimo = df.iloc[-1]
    return {
        "tagname": ultimo["tagname"],
        "value": float(ultimo["value"]),
        "timestamp": ultimo["timestampseconds"]
    }

def guardar_json(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("✅ JSON guardado")

def subir_github():
    os.chdir(CARPETA)
    subprocess.run(["git", "add", "datos.json"])
    subprocess.run(["git", "commit", "-m", f"actualizacion {datetime.now()}"])
    subprocess.run(["git", "push", "origin", "main"])
    print("🚀 Subido a GitHub")

print("📡 Monitoreando CSV...")
while True:
    datos = leer_csv()
    guardar_json(datos)
    subir_github()
    time.sleep(30)