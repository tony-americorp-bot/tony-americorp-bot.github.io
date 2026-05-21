import os
import json
import pandas as pd
import time
import subprocess
from datetime import datetime

CARPETA = r"C:\planta_monitor"
JSON_FILE = r"C:\planta_monitor\datos.json"
CSV_FILE = r"C:\planta_monitor\medidor_energia_2026-05-21.csv"

def leer_todo_csv():
    """Lee TODAS las filas del CSV"""
    try:
        df = pd.read_csv(CSV_FILE)
        
        todos_los_datos = []
        for _, fila in df.iterrows():
            registro = {
                "timestamp": fila["timestamp"],
                "voltaje_r": float(fila["voltaje_r"]),
                "voltaje_s": float(fila["voltaje_s"]),
                "voltaje_t": float(fila["voltaje_t"]),
                "corriente_r": float(fila["corriente_r"]),
                "corriente_s": float(fila["corriente_s"]),
                "corriente_t": float(fila["corriente_t"]),
                "potencia_kw": round((
                    fila["voltaje_r"] * fila["corriente_r"] +
                    fila["voltaje_s"] * fila["corriente_s"] +
                    fila["voltaje_t"] * fila["corriente_t"]
                ) / 1000, 2)
            }
            todos_los_datos.append(registro)
        
        datos = {
            "ultima_actualizacion": datetime.now().isoformat(),
            "total_registros": len(todos_los_datos),
            "historial": todos_los_datos,
            "ultimo": todos_los_datos[-1] if todos_los_datos else None
        }
        
        print(f"  ✅ Leídos {len(todos_los_datos)} registros")
        print(f"  📊 Último: {todos_los_datos[-1]['timestamp']} | Potencia: {todos_los_datos[-1]['potencia_kw']} kW")
        return datos
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"error": str(e), "total_registros": 0, "historial": []}

def guardar_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("✅ JSON guardado")

def subir_github():
    os.chdir(CARPETA)
    subprocess.run(["git", "add", "datos.json"], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"actualizacion {datetime.now()}"], capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], capture_output=True)
    print("🚀 Subido a GitHub")

print("📡 Monitoreando medidor_energia_2026-05-21.csv")
print("=" * 50)

while True:
    print(f"\n🔄 Actualización: {datetime.now().strftime('%H:%M:%S')}")
    datos = leer_todo_csv()
    guardar_json(datos)
    subir_github()
    time.sleep(30)