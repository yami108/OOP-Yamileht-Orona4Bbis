import csv
import json
from abc import ABC, abstractmethod
from fpdf import FPDF

class Exporter(ABC):
    @abstractmethod
    def export(self, data, file_path):
        pass

class TXTExporter(Exporter):
    def export(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("--- REPORT DE PRODUCTOS ---\n")
            for product in data:
                file.write(f"ID: {product['id']} | Nombre: {product['nombre']} | Precio: ${product['precio']} | Stock: {product['stock']}\n")

class CSVExporter(Exporter):
    def export(self, data, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nombre", "Precio", "Stock"])
            for product in data:
                writer.writerow([product['id'], product['nombre'], product['precio'], product['stock']])

class JSONExporter(Exporter):
    def export(self, data, file_path):
        formatted_data = [
            {
                "id": product['id'],
                "nombre": product['nombre'],
                "precio": float(product['precio']),
                "stock": product['stock']
            }
            for product in data
        ]
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(formatted_data, file, indent=4, ensure_ascii=False)

class PDFExporter(Exporter):
    def export(self, data, file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="Reporte de Inventario de Productos", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", size=11)
        for product in data:
            line_text = f"ID: {product['id']} | Nombre: {product['nombre']} | Precio: ${product['precio']:.2f} | Stock: {product['stock']}"
            pdf.cell(190, 8, txt=line_text, ln=True)
            
        pdf.output(file_path)