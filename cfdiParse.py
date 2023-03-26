import os
import csv
import xml.etree.ElementTree as ET
import argparse

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

        cfdi_dict = {}
        for child in root.iter("{http://www.sat.gob.mx/cfd/3}Comprobante"):
            cfdi_dict.update(child.attrib)

        cfdi_data.append(cfdi_dict)

# Escribir los datos en un archivo CSV
with open(args.csv_path, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=cfdi_data[0].keys())
    writer.writeheader()
    for cfdi in cfdi_data:
        writer.writerow(cfdi)