import pandas as pd
import json
import time
import subprocess
import uuid
import os
import math
from datetime import datetime

# =====================================================
# CONFIGURACION
# =====================================================

CSV_FILE = r"C:\scada_monitor\csv\medidor_actual.csv"

JSON_FILE = r"C:\scada_monitor\datos.json"

ALARMAS_ACTIVAS = r"C:\scada_monitor\alarmas_activas.json"

HISTORIAL_ALARMAS = r"C:\scada_monitor\historial_alarmas.json"

TIMESTAMP_FILE = r"C:\scada_monitor\ultimo_timestamp.txt"

REPO_DIR = r"C:\scada_monitor"

INTERVALO = 60

# =====================================================
# CREAR ARCHIVOS SI NO EXISTEN
# =====================================================

if not os.path.exists(ALARMAS_ACTIVAS):
    with open(ALARMAS_ACTIVAS, "w") as f:
        json.dump([], f)

if not os.path.exists(HISTORIAL_ALARMAS):
    with open(HISTORIAL_ALARMAS, "w") as f:
        json.dump([], f)

# =====================================================
# FUNCIONES
# =====================================================

def cargar_json(ruta):

    try:

        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []

# =====================================================

def guardar_json(ruta, datos):

    with open(ruta, "w", encoding="utf-8") as f:

        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False
        )

# =====================================================

def segundos_a_texto(segundos):

    horas = int(segundos // 3600)

    minutos = int((segundos % 3600) // 60)

    seg = int(segundos % 60)

    return f"{horas:02}:{minutos:02}:{seg:02}"

# =====================================================
# LOOP PRINCIPAL
# =====================================================

while True:

    try:

        print("\n======================================")
        print("LEYENDO CSV...")

        # =================================================
        # LEER CSV
        # =================================================

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

        # =================================================
        # TIMESTAMP
        # =================================================

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            dayfirst=True
        )

        df = df.sort_values("timestamp")

        # =================================================
        # ULTIMO TIMESTAMP
        # =================================================

        with open(TIMESTAMP_FILE, "r") as f:

            ultimo_timestamp = f.read().strip()

        ultimo_timestamp = pd.to_datetime(ultimo_timestamp)

        # =================================================
        # FILTRAR NUEVOS
        # =================================================

        nuevos = df[df["timestamp"] > ultimo_timestamp]

        # =================================================
        # SI HAY NUEVOS
        # =================================================

        if len(nuevos) > 0:

            fila = nuevos.iloc[0]

            fecha_csv = fila["timestamp"]





            # =========================
            # SIMULACION DINAMICA /////////////////////////////////////////////////////////////////////////////
            # =========================

            voltaje_r = float(fila["voltaje_r"])
            voltaje_s = float(fila["voltaje_s"])
            voltaje_t = float(fila["voltaje_t"])
            corriente_r = float(fila["corriente_r"])
            corriente_s = float(fila["corriente_s"])
            corriente_t = float(fila["corriente_t"])
            segundo = time.time()
            voltaje_r = voltaje_r + math.sin(segundo / 20) * 4
            voltaje_s = voltaje_s + math.cos(segundo / 25) * 3
            voltaje_t = voltaje_t + math.sin(segundo / 30) * 2
            corriente_r = corriente_r + math.cos(segundo / 18) * 5
            corriente_s = corriente_s + math.sin(segundo / 22) * 4
            corriente_t = corriente_t + math.cos(segundo / 28) * 3




            # =============================================
            # DATOS TIEMPO REAL
            # =============================================

            datos = {

                "fecha_hora": str(fecha_csv),

                "voltaje_r": round(voltaje_r, 2),
                "voltaje_s": round(voltaje_s, 2),
                "voltaje_t": round(voltaje_t, 2),

                "corriente_r": round(corriente_r, 2),
                "corriente_s": round(corriente_s, 2),
                "corriente_t": round(corriente_t, 2),

                "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            }
            #datos = {

             #   "fecha_hora": str(fecha_csv),

             #   "voltaje_r": round(float(fila["voltaje_r"]), 2),
             #   "voltaje_s": round(float(fila["voltaje_s"]), 2),
              #  "voltaje_t": round(float(fila["voltaje_t"]), 2),

               # "corriente_r": round(float(fila["corriente_r"]), 2),
                #"corriente_s": round(float(fila["corriente_s"]), 2),
                #"corriente_t": round(float(fila["corriente_t"]), 2),

                #"actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            #}

            # =============================================
            # GUARDAR DATOS.JSON
            # =============================================

            guardar_json(JSON_FILE, datos)

            print("DATOS.JSON ACTUALIZADO")

            # =============================================
            # CARGAR ALARMAS
            # =============================================

            activas = cargar_json(ALARMAS_ACTIVAS)

            historial = cargar_json(HISTORIAL_ALARMAS)

            # =============================================
            # DEFINIR ALARMAS
            # =============================================

            condiciones = [

                {
                    "tag": "MT-001",
                    "mensaje": "VOLTAJE ALTO",
                    "valor": datos["voltaje_r"],
                    "unidad": "V",
                    "condicion": datos["voltaje_r"] > 223.80,
                    "severity": "WARNING"
                },

                {
                    "tag": "MT-002",
                    "mensaje": "CORRIENTE ALTA",
                    "valor": datos["corriente_r"],
                    "unidad": "A",
                    "condicion": datos["corriente_r"] > 106.10,
                    "severity": "ALARM"
                },

                {
                    "tag": "VC-001",
                    "mensaje": "VIBRACION ALTA",
                    "valor": datos["voltaje_t"],
                    "unidad": "mm/s",
                    "condicion": datos["voltaje_t"] > 3,
                    "severity": "WARNING"
                },

                {
                    "tag": "VFD-001",
                    "mensaje": "TEMPERATURA ALTA",
                    "valor": datos["voltaje_s"],
                    "unidad": "°C",
                    "condicion": datos["voltaje_s"] > 70,
                    "severity": "TRIP"
                }

            ]

            # =============================================
            # PROCESAR ALARMAS
            # =============================================

            for c in condiciones:

                alarma_existente = next(

                    (
                        a for a in activas

                        if a["tag"] == c["tag"]
                        and a["mensaje"] == c["mensaje"]
                    ),

                    None

                )

                # =========================================
                # SI CONDICION ACTIVA
                # =========================================

                if c["condicion"]:

                    # =====================================
                    # CREAR NUEVA
                    # =====================================

                    if alarma_existente is None:

                        nueva = {

                            "id": str(uuid.uuid4()),

                            "tag": c["tag"],

                            "mensaje": c["mensaje"],

                            "valor": f'{c["valor"]} {c["unidad"]}',

                            "inicio": str(fecha_csv),

                            "duracion": "00:00:00",

                            "reviewed": False,

                            "severity": c["severity"],

                            "activa": True

                        }

                        activas.append(nueva)

                        historial.append(nueva.copy())

                        print(f'ALARMA NUEVA: {c["mensaje"]}')

                    # =====================================
                    # ACTUALIZAR DURACION
                    # =====================================

                    else:

                        inicio = pd.to_datetime(
                            alarma_existente["inicio"]
                        )

                        segundos = (
                            fecha_csv - inicio
                        ).total_seconds()

                        alarma_existente["duracion"] = segundos_a_texto(segundos)

                        alarma_existente["valor"] = f'{c["valor"]} {c["unidad"]}'

                        # =================================
                        # ACTUALIZAR HISTORIAL
                        # =================================

                        for h in historial:

                            if h["id"] == alarma_existente["id"]:

                                h["duracion"] = alarma_existente["duracion"]

                                h["valor"] = alarma_existente["valor"]

                # =========================================
                # SI CONDICION DESAPARECE
                # =========================================

                else:

                    if alarma_existente is not None:

                        alarma_existente["activa"] = False

                        alarma_existente["fin"] = str(fecha_csv)

                        inicio = pd.to_datetime(
                            alarma_existente["inicio"]
                        )

                        segundos = (
                            fecha_csv - inicio
                        ).total_seconds()

                        alarma_existente["duracion"] = segundos_a_texto(segundos)

                        # =================================
                        # ACTUALIZAR HISTORIAL
                        # =================================

                        for h in historial:

                            if h["id"] == alarma_existente["id"]:

                                h["activa"] = False

                                h["fin"] = str(fecha_csv)

                                h["duracion"] = alarma_existente["duracion"]

                        # =================================
                        # ELIMINAR DE ACTIVAS
                        # =================================

                        activas = [

                            a for a in activas

                            if a["id"] != alarma_existente["id"]

                        ]

                        print(f'ALARMA RESUELTA: {c["mensaje"]}')

            # =============================================
            # MAXIMO 50 ACTIVAS
            # =============================================

            activas = activas[-50:]

            # =============================================
            # GUARDAR JSONS
            # =============================================

            guardar_json(ALARMAS_ACTIVAS, activas)

            guardar_json(HISTORIAL_ALARMAS, historial)

            print("ALARMAS ACTUALIZADAS")

            # =============================================
            # GUARDAR TIMESTAMP
            # =============================================

            with open(TIMESTAMP_FILE, "w") as f:

                f.write(str(fecha_csv))

            # =============================================
            # GIT ADD
            # =============================================

            subprocess.run(
                [
                    "git",
                    "add",
                    "datos.json",
                    "alarmas_activas.json",
                    "historial_alarmas.json"
                ],
                cwd=REPO_DIR
            )

            # =============================================
            # COMMIT
            # =============================================

            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"update {datetime.now()}"
                ],
                cwd=REPO_DIR
            )

            # =============================================
            # PUSH
            # =============================================

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

            print("NO HAY DATOS NUEVOS")

    except Exception as e:

        print("\nERROR GENERAL:")
        print(e)

    # =====================================================
    # ESPERAR
    # =====================================================

    print(f"\nESPERANDO {INTERVALO} SEGUNDOS...\n")

    time.sleep(INTERVALO)