from tkinter import filedialog, messagebox
from Models.products_model import Producto
from Services.exporters import CSVExporter, TXTExporter, JSONExporter, PDFExporter

class ProductController:
    def __init__(self):
        self.model = Producto()
        self.exporters = {
            "CSV": CSVExporter,
            "TXT": TXTExporter,
            "JSON": JSONExporter,
            "PDF": PDFExporter
        }

    def exportar_reporte(self, formato_seleccionado):
        datos = self.model.obtener_todos()
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        extension = formato_seleccionado.lower()
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=f".{extension}",
            filetypes=[(f"Archivo {formato_seleccionado}", f"*.{extension}")],
            title="Guardar Reporte"
        )

        if not ruta_archivo:
            return

        exporter_class = self.exporters.get(formato_seleccionado)
        if exporter_class:
            try:
                instancia_exporter = exporter_class()
                instancia_exporter.export(datos, ruta_archivo)
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente en:\n{ruta_archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al exportar: {e}")