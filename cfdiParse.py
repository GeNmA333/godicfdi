import os
import csv
import xml.etree.ElementTree as ET
import argparse
import sys

NOMINA12 = "{http://www.sat.gob.mx/nomina12}"
NOMINA = f"{NOMINA12}Nomina"
PERCEPCIONES = f"{NOMINA12}Percepciones"
PERCEPCION = f"{NOMINA12}Percepcion"
DEDUCCIONES = f"{NOMINA12}Deducciones"
DEDUCCION = f"{NOMINA12}Deduccion"

# Crear el parser de argumentos
parser = argparse.ArgumentParser(description="Convierte archivos XML a CSV")
parser.add_argument("--folder_path", default=".", help="Ruta al folder que contiene los archivos XML")
parser.add_argument("--csv_path", default="output.csv", help="Ruta al archivo CSV de salida")
args = parser.parse_args()

# Lista para almacenar los datos de todos los CFDIs
cfdi_data = []

# Iterar sobre todos los archivos XML del folder
for filename in os.listdir(args.folder_path):
    if filename.endswith(".xml"):
        # Ruta al archivo XML actual
        xml_path = os.path.join(args.folder_path, filename)

        # Leer el archivo XML y extraer los datos necesarios
        tree = ET.parse(xml_path)
        root = tree.getroot()
        version = root.attrib.get("Version")
        if(version=="3.3"):
            cfd = "{http://www.sat.gob.mx/cfd/3}"
        else:
            cfd = "{http://www.sat.gob.mx/cfd/4}"
        COMPLEMENTO = f"{cfd}Complemento"

        cfdi_dict = {}
        for child in root.findall(f"./{COMPLEMENTO}/{NOMINA}"):
            if(child.attrib.__len__!=0):
                cfdi_dict.update(child.attrib)

        if(cfdi_dict.__len__()!=0):
            cfdi_data.append(cfdi_dict)


if cfdi_data.__len__() == 0:
    print("No hubo CFDIs")
    sys.exit(0)

# Escribir los datos en un archivo CSV
with open(args.csv_path, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=cfdi_data[0].keys())
    writer.writeheader()
    for cfdi in cfdi_data:
        writer.writerow(cfdi)